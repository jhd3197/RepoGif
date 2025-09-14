"""
Example demonstrating the enhanced GitHub repository header animation.

This example uses the web-based animation generator powered by Puppeteer
to create a realistic GitHub repository header GIF with animated star interaction.

This file demonstrates the latest features of the RepoGif project.
"""
from repogif.generator import generate_repo_gif

# Generate an animated GitHub repository header GIF
# This uses the enhanced web-based animation with Puppeteer
# Parameters:
#   - repo_name: Name of the repository
#   - stars: Number of stars (can be formatted like "5.8k")
#   - forks: Number of forks (can be formatted like "1.2k")
#   - out: Output file path for the generated GIF
#   - show_forks: Whether to display the fork section (defaults to True)
# Example 1: Default behavior with fork section displayed
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="3.8k",              # Star count with "k" suffix for thousands
    forks="1.2k",              # Fork count with "k" suffix for thousands
    out="examples/repo_header_with_forks.gif",  # Output filename
    show_forks=True            # Display the fork section (default)
)

print("✨ Example 1: Animation with forks section generated successfully!")
print("Check repo_header_with_forks.gif in the examples directory")

# Example 2: Animation with fork section hidden
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="3.8k",              # Star count with "k" suffix for thousands
    forks="1.2k",              # Fork count (value provided but section hidden)
    out="examples/repo_header_no_forks.gif",  # Output filename
    show_forks=False           # Hide the fork section
)

print("✨ Example 2: Animation without forks section generated successfully!")
print("Check repo_header_no_forks.gif in the examples directory")