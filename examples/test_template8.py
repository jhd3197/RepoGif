"""
Test script for Template 8 in RepoGif.

This script tests Template 8 with various configurations to verify:
1. Basic template with default commit pattern
2. Template with custom commit values
3. Template with pattern including zero-value weeks

Each variant tests proper GIF animation with weekly commit visualization
showing different patterns and values.
"""
from repogif.generator import generate_repo_gif

# Variant 1: Default commit pattern
print("Testing Template 8 - Default commit pattern...")
generate_repo_gif(
    repo_name="RepoGif",                   # Repository name
    stars="50",                            # Star count
    forks="25",                            # Fork count
    out="examples/template8_default.gif",  # Output filename
    template="template8",                  # Use template8
    # Default commits pattern will be used (from template)
    height=200,                            # Increased height to ensure tall commit bars are fully visible
    debug_dir=True                         # Save intermediate frames for inspection
)
print("Output saved to: examples/template8_default.gif")

# Variant 2: Custom commit values with increasing pattern
print("\nTesting Template 8 - Custom increasing commits pattern...")
generate_repo_gif(
    repo_name="RepoGif",                      # Repository name
    stars="100",                              # Star count
    forks="45",                               # Fork count
    out="examples/template8_increasing.gif",  # Output filename
    template="template8",                     # Use template8
    commits="5,10,15,20,25,30,35",           # Increasing weekly commits
    height=200,                              # Increased height to ensure tall commit bars are fully visible
    debug_dir=True                           # Save intermediate frames for inspection
)
print("Output saved to: examples/template8_increasing.gif")

# Variant 3: Pattern with zero-value weeks
print("\nTesting Template 8 - Pattern with zero-value weeks...")
generate_repo_gif(
    repo_name="RepoGif",                      # Repository name
    stars="1k",                               # Star count with "k" suffix for thousands
    forks="250",                              # Fork count
    out="examples/template8_with_zeros.gif",  # Output filename
    template="template8",                     # Use template8
    commits="30,0,25,0,40,10,5",             # Pattern with zero-value weeks
    height=200,                              # Increased height to ensure tall commit bars are fully visible
    debug_dir=True                           # Save intermediate frames for inspection
)
print("Output saved to: examples/template8_with_zeros.gif")

print("\nAll Template 8 test variants completed.")