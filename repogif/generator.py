"""
RepoGif - Generator for GitHub repository header GIFs.

This module provides the main functionality for generating GitHub repository
header GIFs using customizable templates.
"""

import os
import tempfile
import shutil
import importlib
from pathlib import Path
from PIL import Image


class RepoGifGenerator:
    """
    Template-based GitHub repository header GIF generator.
    This class provides a framework for generating repository header GIFs
    using various templates.
    """
    
    def __init__(self):
        """Initialize the generator with available templates."""
        self.templates = {
            "template1": "repogif.templates.template1",
            "template2": "repogif.templates.template2",
            "template3": "repogif.templates.template3",
            "template4": "repogif.templates.template4",
            "template5": "repogif.templates.template5",
            "template6": "repogif.templates.template6",
            "template7": "repogif.templates.template7",
            "template8": "repogif.templates.template8",
            "template9": "repogif.templates.template9"
        }
        self.default_template = "template1"
    
    def get_available_templates(self):
        """Returns a list of available template names."""
        return list(self.templates.keys())
    
    def generate_gif(self,
                     repo_name="repogif",
                     stars=123,
                     forks=45,
                     out="repo.gif",
                     debug_dir=None,
                     show_forks=True,
                     template=None,
                     width=580,
                     height=140,
                     contributors=None,
                     commits=None):
        """
        Generate a GitHub repository header GIF using the specified template.
        
        Args:
            repo_name (str): Name of the repository
            stars (int/str): Number of stars to display
            forks (int/str): Number of forks to display
            out (str): Output path for the GIF
            debug_dir (str/bool, optional): Directory to save frame images for debugging purposes.
                                         If None or False, frames are not saved.
                                         If True, frames are saved to a default directory in the package.
                                         If a string path, frames are saved to that directory.
            show_forks (bool, optional): Whether to display the fork section in the repository header.
            template (str, optional): The template to use for generating the GIF.
                                    If None, the default template will be used.
            width (int, optional): Width of the GIF in pixels. Default is 580.
            height (int, optional): Height of the GIF in pixels. Default is 140.
            contributors (str, optional): JSON-encoded string of contributors data for template9.
                                       Each contributor should have 'date', 'login', and 'avatar_url'.
            commits (str, optional): Comma-separated string of weekly commit counts for template8.
                                  Example: "10,25,15,30,20,35,40"
            
        Returns:
            None: The GIF is saved to the specified path
            
        Raises:
            ValueError: If the specified template is not available
            RuntimeError: If required dependencies are not available
        """
        # Choose template (use default if not specified)
        template_name = template or self.default_template
        
        if template_name not in self.templates:
            available = ", ".join(self.get_available_templates())
            raise ValueError(f"Template '{template_name}' not found. Available templates: {available}")
        
        # Import the template
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError(
                "Required dependencies not found. Please install with:\n"
                "pip install playwright pillow\n"
                "Then run: playwright install"
            )
        
        # Get the template path
        template_module = self.templates[template_name]
        template_dir = os.path.join(os.path.dirname(__file__), 
                                   "templates", 
                                   template_name)
        template_path = os.path.join(template_dir, "template.html")
        template_url = f"file://{os.path.abspath(template_path)}"
        
        # Create temporary directory for frames
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # File paths for the two states
                unstarred_path = os.path.join(temp_dir, "unstarred.png")
                starred_path = os.path.join(temp_dir, "starred.png")
                
                print("Capturing screenshots with Playwright...")
                with sync_playwright() as p:
                    browser = p.chromium.launch()
                    # Set viewport to the specified dimensions
                    page = browser.new_page(viewport={"width": width, "height": height})
                    
                    # Capture unstarred state
                    print("Capturing unstarred state...")
                    params = {
                        "repo_name": repo_name,
                        "stars": stars,
                        "forks": forks,
                        "starred": "false",
                        "show_forks": "true" if show_forks else "false",
                        "width": width,
                        "height": height
                    }
                    
                    # Add commits data for template8
                    if commits and template_name == "template8":
                        params["commits"] = commits
                    
                    # Add contributors data for template9
                    if contributors and template_name == "template9":
                        params["contributors"] = contributors
                        params["animation_state"] = "initial"
                    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                    page.goto(f"{template_url}?{query_string}")
                    page.screenshot(path=unstarred_path)
                    
                    # Capture starred state
                    print("Capturing starred state...")
                    params["starred"] = "true"
                    
                    # Update animation state for template9
                    if contributors and template_name == "template9":
                        params["animation_state"] = "animated"
                        
                    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                    page.goto(f"{template_url}?{query_string}")
                    page.screenshot(path=starred_path)
                    
                    browser.close()
                
                # Create GIF from the two frames using PIL
                print("Creating GIF from screenshots...")
                frames = [Image.open(unstarred_path), Image.open(starred_path)]
                frames[0].save(
                    out,
                    format='GIF',
                    append_images=[frames[1]],
                    save_all=True,
                    duration=1000,  # 1 second per frame
                    loop=0  # Loop forever
                )
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
                        
                        # Copy frames to the debug directory
                        frame_files = [unstarred_path, starred_path]
                        frame_names = ["unstarred.png", "starred.png"]
                        
                        for i, frame_file in enumerate(frame_files):
                            dest_path = os.path.join(debug_dir, frame_names[i])
                            shutil.copy2(frame_file, dest_path)
                        
                        print(f"✅ Copied frames to {debug_dir}")
                    except PermissionError:
                        print(f"⚠️ Warning: Permission denied when copying frames to {debug_dir}")
                    except OSError as e:
                        print(f"⚠️ Warning: Failed to copy frames to debug directory: {e}")
                
            except Exception as e:
                raise RuntimeError(f"Error generating GIF: {e}")


# Create a singleton instance of the generator
_generator = RepoGifGenerator()


# Public API functions
def generate_repo_gif(repo_name="repogif", stars=123, forks=45, out="repo.gif",
                     debug_dir=None, show_forks=True, template=None,
                     width=580, height=140, contributors=None, commits=None):
    """
    Generate a GitHub repository header GIF using the specified template.
    
    Args:
        repo_name (str): Name of the repository
        stars (int/str): Number of stars to display
        forks (int/str): Number of forks to display
        out (str): Output path for the GIF
        debug_dir (str/bool, optional): Directory to save frame images for debugging purposes.
        show_forks (bool, optional): Whether to display the fork section in the repository header.
        template (str, optional): The template to use for generating the GIF.
                                If None, the default template will be used.
        width (int, optional): Width of the GIF in pixels. Default is 580.
        height (int, optional): Height of the GIF in pixels. Default is 140.
        contributors (str, optional): JSON-encoded string of contributors data for template9.
                                   Each contributor should have 'date', 'login', and 'avatar_url'.
        commits (str, optional): Comma-separated string of weekly commit counts for template8.
                              Example: "10,25,15,30,20,35,40"
        
    Returns:
        None: The GIF is saved to the specified path
    """
    return _generator.generate_gif(
        repo_name=repo_name,
        stars=stars,
        forks=forks,
        out=out,
        debug_dir=debug_dir,
        show_forks=show_forks,
        template=template,
        width=width,
        height=height,
        contributors=contributors,
        commits=commits
    )


def get_available_templates():
    """Returns a list of available template names."""
    return _generator.get_available_templates()


# Define the public API
__all__ = ['generate_repo_gif', 'get_available_templates']