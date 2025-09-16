"""
Test script for the Animated Badge template (template7) in RepoGif.

This script tests the newly created template7 (Animated Badge) to verify:
1. Proper rendering at 280x280 dimensions
2. Correct display of repository name, star count, and fork count
3. Proper GIF animation between unstarred and starred states
4. Pulsing star effect animation
"""
from repogif.generator import generate_repo_gif

# Test the template7 (Animated Badge) template
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="4.2k",              # Star count with "k" suffix for thousands
    forks="1.5k",              # Fork count with "k" suffix for thousands
    out="examples/animated_badge_test.gif",  # Output filename
    show_forks=True,           # Display the fork section
    template="template7",      # Use template7 (Animated Badge)
    width=280,                 # Width for Animated Badge (280px)
    height=280,                # Height for Animated Badge (280px)
    debug_dir=True             # Save intermediate frames for inspection
)

print("Test completed for template7 (Animated Badge).")
print("Output saved to: examples/animated_badge_test.gif")
print("Debug frames saved to debug directory for inspection.")