import os
import tempfile
import subprocess
import sys
import glob
import shutil
import imageio


def generate_repo_gif(repo_name="repogif", stars=123, forks=45, out="repo.gif", debug_dir=None, show_forks=True):
    """
    Generate a GitHub repository header GIF using a web-based approach with Puppeteer.
    
    This function uses a Node.js script with Puppeteer to capture frames of an animated
    GitHub repository header, then compiles them into a GIF using imageio.
    
    Args:
        repo_name (str): Name of the repository
        stars (int/str): Number of stars to display
        forks (int/str): Number of forks to display
        out (str): Output path for the GIF
        debug_dir (str/bool, optional): Directory to save frame images for debugging purposes.
                                       If None or False, frames are not saved.
                                       If True, frames are saved to a default directory in the package.
                                       If a string path, frames are saved to that directory.
                                       Defaults to None.
        show_forks (bool, optional): Whether to display the fork section in the repository header.
                                    Defaults to True.
        
    Returns:
        None: The GIF is saved to the specified path
        
    Raises:
        RuntimeError: If Node.js or Puppeteer is not available
    """
    # Check for Node.js
    try:
        node_version = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Using Node.js {node_version.stdout.strip()}")
    except (subprocess.SubprocessError, FileNotFoundError):
        raise RuntimeError(
            "Node.js is not installed or not in PATH. Please install Node.js to use this feature."
        )
        
    # Check for puppeteer
    try:
        check_puppeteer = subprocess.run(
            ["node", "-e", "require('puppeteer')"],
            capture_output=True,
            text=True
        )
        if check_puppeteer.returncode != 0:
            raise RuntimeError(
                "Puppeteer is not installed. Please run 'npm install puppeteer yargs' to install required dependencies."
            )
    except subprocess.SubprocessError:
        raise RuntimeError(
            "Failed to check for Puppeteer. Please make sure Node.js is properly installed and run 'npm install puppeteer yargs'."
        )
    
    # Create temporary directory for frames
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Get the path to the puppeteer script
            script_path = os.path.join(os.path.dirname(__file__), "puppeteer_capture.js")
            
            # Run the puppeteer script to generate frames
            cmd = [
                "node",
                script_path,
                "--repo", str(repo_name),
                "--stars", str(stars),
                "--forks", str(forks),
                "--output", temp_dir,
                "--frames", "50",  # Default number of frames, truncated to avoid restart issue
                "--show-forks", "true" if show_forks else "false"
            ]
            
            print("Capturing frames with Puppeteer...")
            subprocess.run(cmd, check=True)
            
            # Get all frame files in the correct order
            # Get all frame files and sort them by frame number
            frame_files = glob.glob(os.path.join(temp_dir, "frame_*.png"))

            # Extract frame number from filename and sort by it
            # This ensures correct ordering even if naming convention changes
            import re
            def get_frame_number(filename):
                # Extract the base filename without path and extension
                base_filename = os.path.basename(filename)
                
                # Try different regex patterns to extract the frame number
                # Pattern 1: Match any digits after "frame_" (most common case)
                match = re.search(r'frame_(\d+)', base_filename)
                if match:
                    return int(match.group(1))
                
                # Pattern 2: Match digits between underscores (e.g., frame_001_initial.png)
                match = re.search(r'frame_(\d+)_', base_filename)
                if match:
                    return int(match.group(1))
                
                # Pattern 3: Match any sequence of digits in the filename as a fallback
                match = re.search(r'(\d+)', base_filename)
                if match:
                    return int(match.group(1))
                
                # If no number is found, return a very high number to sort these files last
                return float('inf')
                
            frame_files = sorted(frame_files, key=get_frame_number)
            
            if not frame_files:
                raise RuntimeError("No frames were generated by the Puppeteer script")
            
            # Create GIF from frames
            print(f"Creating GIF from {len(frame_files)} frames...")
            with imageio.get_writer(out, mode='I', duration=0.12, loop=0) as writer:
                for frame_file in frame_files:
                    image = imageio.imread(frame_file)
                    writer.append_data(image)
            print(f"✅ Saved {out}")
            
            # Handle debug frames if debug_dir is provided
            if debug_dir is not None and debug_dir is not False:
                # If debug_dir is True, use the default debug directory in the package
                if debug_dir is True:
                    debug_dir = os.path.join(os.path.dirname(__file__), "debug_frames")
                    print(f"Debug mode: using default debug directory: {debug_dir}")
                else:
                    print(f"Debug mode: copying frames to {debug_dir}")
                
                try:
                    # Create debug directory if it doesn't exist
                    if not os.path.exists(debug_dir):
                        os.makedirs(debug_dir)
                        print(f"Created debug directory: {debug_dir}")
                    
                    # Copy each frame to the debug directory
                    for frame_file in frame_files:
                        frame_filename = os.path.basename(frame_file)
                        dest_path = os.path.join(debug_dir, frame_filename)
                        shutil.copy2(frame_file, dest_path)
                    
                    print(f"✅ Copied {len(frame_files)} frames to {debug_dir}")
                except PermissionError:
                    print(f"⚠️ Warning: Permission denied when copying frames to {debug_dir}")
                except OSError as e:
                    print(f"⚠️ Warning: Failed to copy frames to debug directory: {e}")
            
            
        except subprocess.SubprocessError as e:
            error_msg = str(e)
            if "Cannot find module 'puppeteer'" in error_msg or "Cannot find module 'yargs'" in error_msg:
                raise RuntimeError(
                    "Required Node.js modules are missing. Please run 'npm install puppeteer yargs' in the project directory."
                )
            else:
                raise RuntimeError(f"Error running Puppeteer script: {e}")
        except Exception as e:
            raise RuntimeError(f"Error generating GIF: {e}")