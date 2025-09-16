"""
Test script for the Square Badge template (template2) in RepoGif.

This script tests the newly created template2 (Square Badge) to verify:
1. Proper rendering at 250x250 dimensions
2. Correct display of repository name, star count, and fork count
3. Proper GIF animation between unstarred and starred states
"""
from repogif.generator import generate_repo_gif

# Test the template2 (Square Badge) template
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="4.2k",              # Star count with "k" suffix for thousands
    forks="1.5k",              # Fork count with "k" suffix for thousands
    out="examples/square_badge_test.gif",  # Output filename
    show_forks=True,           # Display the fork section
    template="template2",      # Use template2 (Square Badge)
    width=250,                 # Width for Square Badge (250px)
    height=250,                # Height for Square Badge (250px)
    debug_dir=True             # Save intermediate frames for inspection
)

print("Test completed for template2 (Square Badge).")
print("Output saved to: examples/square_badge_test.gif")
print("Debug frames saved to debug directory for inspection.")