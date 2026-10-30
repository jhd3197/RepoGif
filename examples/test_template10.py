"""
Test script for the Modern Spotlight template (template10) in RepoGif.

This script tests the newly created template10 (Modern Spotlight) to verify:
1. Proper rendering at 640x360 dimensions
2. Correct display of repository name, star count, and fork count
3. Proper GIF animation between unstarred and starred states
4. Fork section can be hidden
"""
from repogif.generator import generate_repo_gif

# Variant 1: Default modern spotlight with stars and forks
print("Testing Template 10 - Modern Spotlight...")
generate_repo_gif(
    repo_name="RepoGif",
    stars="5.8k",
    forks="397",
    out="examples/modern_spotlight.gif",
    show_forks=True,
    template="template10",
    width=640,
    height=360,
    debug_dir=True
)
print("Output saved to: examples/modern_spotlight.gif")

# Variant 2: Spotlight without the fork stat
print("\nTesting Template 10 - No forks variant...")
generate_repo_gif(
    repo_name="RepoGif",
    stars="1.2k",
    forks="80",
    out="examples/modern_spotlight_no_forks.gif",
    show_forks=False,
    template="template10",
    width=640,
    height=360,
    debug_dir=True
)
print("Output saved to: examples/modern_spotlight_no_forks.gif")

print("\nAll Template 10 test variants completed.")
