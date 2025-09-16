"""
Test script for the Horizontal Banner template (template3) in RepoGif.

This script tests the newly created template3 (Horizontal Banner) to verify:
1. Proper rendering at 600x120 dimensions
2. Correct display of repository name, star count, and fork count
3. Proper GIF animation between unstarred and starred states
"""
from repogif.generator import generate_repo_gif

# Test the template3 (Horizontal Banner) template
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="4.2k",              # Star count with "k" suffix for thousands
    forks="1.5k",              # Fork count with "k" suffix for thousands
    out="examples/horizontal_banner_test.gif",  # Output filename
    show_forks=True,           # Display the fork section
    template="template3",      # Use template3 (Horizontal Banner)
    width=600,                 # Width for Horizontal Banner (600px)
    height=120,                # Height for Horizontal Banner (120px)
    debug_dir=True             # Save intermediate frames for inspection
)

print("Test completed for template3 (Horizontal Banner).")
print("Output saved to: examples/horizontal_banner_test.gif")
print("Debug frames saved to debug directory for inspection.")