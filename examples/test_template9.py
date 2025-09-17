"""
Test script for Template 9 in RepoGif.

This script tests Template 9 with various configurations to verify:
1. Small number of contributors (5)
2. Larger set of contributors (20)
3. Contributors with different join dates spread over time

Each variant tests proper GIF animation with contributor growth visualization
and avatar display.
"""
import json
from repogif.generator import generate_repo_gif

# Helper function to create sample contributor data
def create_sample_contributors(count, date_spread=True):
    contributors = []
    
    # Sample avatar URLs (using GitHub-style identicons)
    avatar_base = "https://github.com/identicons/"
    usernames = [f"user{i}" for i in range(1, count + 1)]
    
    for i, username in enumerate(usernames):
        # Create dates with even spread or clustered based on date_spread
        if date_spread:
            # Spread contributors evenly over 12 months
            month = (i * 12) // count + 1
            date = f"2024-{month:02d}-01"
        else:
            # Cluster contributors in just 3 months
            month = (i % 3) + 1
            date = f"2024-{month:02d}-15"
            
        contributor = {
            "login": username,
            "avatar_url": f"{avatar_base}{username}.png",
            "date": date
        }
        contributors.append(contributor)
    
    return json.dumps(contributors)

# Variant 1: Small number of contributors (5)
print("Testing Template 9 - Small contributor set (5)...")
small_contributors = create_sample_contributors(5)
generate_repo_gif(
    repo_name="RepoGif",                       # Repository name
    stars="50",                                # Star count
    forks="10",                                # Fork count
    out="examples/template9_small.gif",        # Output filename
    template="template9",                      # Use template9
    contributors=small_contributors,           # Contributors data
    height=220,                                # Increased height to fit both graph and avatar row
    debug_dir=True                             # Save intermediate frames for inspection
)
print("Output saved to: examples/template9_small.gif")

# Variant 2: Larger set of contributors (20)
print("\nTesting Template 9 - Larger contributor set (20)...")
large_contributors = create_sample_contributors(20)
generate_repo_gif(
    repo_name="RepoGif",                       # Repository name
    stars="500",                               # Star count
    forks="120",                               # Fork count
    out="examples/template9_large.gif",        # Output filename
    template="template9",                      # Use template9
    contributors=large_contributors,           # Contributors data
    height=220,                                # Increased height to fit both graph and avatar row
    debug_dir=True                             # Save intermediate frames for inspection
)
print("Output saved to: examples/template9_large.gif")

# Variant 3: Contributors with different join dates (clustered)
print("\nTesting Template 9 - Contributors with clustered join dates...")
clustered_contributors = create_sample_contributors(15, date_spread=False)
generate_repo_gif(
    repo_name="RepoGif",                       # Repository name
    stars="1.2k",                              # Star count
    forks="350",                               # Fork count
    out="examples/template9_clustered.gif",    # Output filename
    template="template9",                      # Use template9
    contributors=clustered_contributors,       # Contributors data
    height=220,                                # Increased height to fit both graph and avatar row
    debug_dir=True                             # Save intermediate frames for inspection
)
print("Output saved to: examples/template9_clustered.gif")

print("\nAll Template 9 test variants completed.")