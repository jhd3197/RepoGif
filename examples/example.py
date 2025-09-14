"""
Example demonstrating the enhanced GitHub repository header animation.

This example uses the web-based animation generator powered by Puppeteer
to create a realistic GitHub repository header GIF with animated star interaction.
"""
from repogif.generator import generate_repo_gif

# Generate an animated GitHub repository header GIF
# This uses the enhanced web-based animation with Puppeteer
# Parameters:
#   - repo_name: Name of the repository
#   - stars: Number of stars (can be formatted like "5.8k")
#   - forks: Number of forks
#   - out: Output file path for the generated GIF
generate_repo_gif(
    repo_name="RepoGif",  # Repository name
    stars="5.8k",         # Star count with "k" suffix for thousands
    forks=397,            # Fork count
    out="repo_header.gif" # Output filename
)

print("✨ Enhanced animation generated successfully!")
print("Check repo_header.gif in the examples directory")