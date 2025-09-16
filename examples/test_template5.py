"""
Test script for the Vertical Card template (template5) in RepoGif.

This script tests the newly created template5 (Vertical Card) to verify:
1. Proper rendering at 300x400 dimensions
2. Correct display of repository name, star count, and fork count
3. Proper GIF animation between unstarred and starred states
4. Gradient background rendering
"""
from repogif.generator import generate_repo_gif

# Test the template5 (Vertical Card) template
generate_repo_gif(
    repo_name="RepoGif",       # Repository name
    stars="4.2k",              # Star count with "k" suffix for thousands
    forks="1.5k",              # Fork count with "k" suffix for thousands
    out="examples/vertical_card_test.gif",  # Output filename
    show_forks=True,           # Display the fork section
    template="template5",      # Use template5 (Vertical Card)
    width=300,                 # Width for Vertical Card (300px)
    height=400,                # Height for Vertical Card (400px)
    debug_dir=True             # Save intermediate frames for inspection
)

print("Test completed for template5 (Vertical Card).")
print("Output saved to: examples/vertical_card_test.gif")
print("Debug frames saved to debug directory for inspection.")