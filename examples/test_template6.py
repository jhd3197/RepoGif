"""
Test script for the Minimalist Tile template (template6) in RepoGif.

This script tests the newly created template6 (Minimalist Tile) to verify:
1. Proper rendering at 320x200 dimensions
2. Correct display of repository name, star count, and fork count
3. Proper GIF animation between unstarred and starred states
4. Monochrome theme rendering
"""
from repogif.generator import generate_repo_gif

# Test the template6 (Minimalist Tile) template
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="4.2k",              # Star count with "k" suffix for thousands
    forks="1.5k",              # Fork count with "k" suffix for thousands
    out="examples/minimalist_tile_test.gif",  # Output filename
    show_forks=True,           # Display the fork section
    template="template6",      # Use template6 (Minimalist Tile)
    width=320,                 # Width for Minimalist Tile (320px)
    height=200,                # Height for Minimalist Tile (200px)
    debug_dir=True             # Save intermediate frames for inspection
)

print("Test completed for template6 (Minimalist Tile).")
print("Output saved to: examples/minimalist_tile_test.gif")
print("Debug frames saved to debug directory for inspection.")