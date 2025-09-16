"""
Test script for the Circular Badge template (template4) in RepoGif.

This script tests the newly created template4 (Circular Badge) to verify:
1. Proper rendering at 250x250 dimensions
2. Correct display of repository name, star count, and fork count
3. Proper GIF animation between unstarred and starred states
"""
from repogif.generator import generate_repo_gif

# Test the template4 (Circular Badge) template
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="4.2k",              # Star count with "k" suffix for thousands
    forks="1.5k",              # Fork count with "k" suffix for thousands
    out="examples/circular_badge_test.gif",  # Output filename
    show_forks=True,           # Display the fork section
    template="template4",      # Use template4 (Circular Badge)
    width=250,                 # Width for Circular Badge (250px)
    height=250,                # Height for Circular Badge (250px)
    debug_dir=True             # Save intermediate frames for inspection
)

print("Test completed for template4 (Circular Badge).")
print("Output saved to: examples/circular_badge_test.gif")
print("Debug frames saved to debug directory for inspection.")