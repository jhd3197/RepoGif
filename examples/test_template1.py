"""
Test script for Template 1 in RepoGif.

This script tests Template 1 with various configurations to verify:
1. Basic template without fork button (show_forks=False)
2. Template with 100 stars
3. Template with 1k stars

Each variant tests proper GIF animation between unstarred and starred states
with appropriate star counts and fork visibility settings.
"""
from repogif.generator import generate_repo_gif

# Variant 1: Basic template without fork button
print("Testing Template 1 - No forks variant...")
generate_repo_gif(
    repo_name="RepoGif",              # Repository name
    stars="50",                       # Star count
    forks="25",                       # Fork count (won't be displayed)
    out="examples/template1_no_forks.gif",  # Output filename
    show_forks=False,                 # Hide the fork section
    template="template1",             # Use template1
    debug_dir=True                    # Save intermediate frames for inspection
)
print("Output saved to: examples/template1_no_forks.gif")

# Variant 2: Template with 100 stars
print("\nTesting Template 1 - 100 stars variant...")
generate_repo_gif(
    repo_name="RepoGif",              # Repository name
    stars="100",                      # Star count
    forks="45",                       # Fork count
    out="examples/template1_100stars.gif",  # Output filename
    show_forks=True,                  # Display the fork section
    template="template1",             # Use template1
    debug_dir=True                    # Save intermediate frames for inspection
)
print("Output saved to: examples/template1_100stars.gif")

# Variant 3: Template with 1k stars
print("\nTesting Template 1 - 1k stars variant...")
generate_repo_gif(
    repo_name="RepoGif",              # Repository name
    stars="1k",                       # Star count with "k" suffix for thousands
    forks="250",                      # Fork count
    out="examples/template1_1k.gif",  # Output filename
    show_forks=True,                  # Display the fork section
    template="template1",             # Use template1
    debug_dir=True                    # Save intermediate frames for inspection
)
print("Output saved to: examples/template1_1k.gif")

print("\nAll Template 1 test variants completed.")
print("Debug frames saved to debug directory for inspection.")