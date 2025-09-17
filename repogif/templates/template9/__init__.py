"""
Template 9 for RepoGif - A visualization showing repository contributors growth over time

This template shows a GitHub-style visualization of repository contributors growth
over time. It includes a line/area chart and avatar visualization.
"""

import json
from datetime import datetime
import urllib.parse

# This template handles contributors data, which should be provided as a JSON-encoded string
# Each contributor entry should contain:
# - date: ISO date string of first commit
# - login: GitHub username
# - avatar_url: URL to avatar image

def parse_contributors(contributors_json):
    """
    Parse the JSON-encoded contributors data and sort by date.
    
    Args:
        contributors_json (str): JSON-encoded string of contributors data
        
    Returns:
        list: Sorted list of contributor dictionaries
    """
    if not contributors_json:
        # Return a default list if no contributors provided
        return []
    
    try:
        contributors = json.loads(contributors_json)
        # Sort contributors by date (earliest first)
        return sorted(contributors, key=lambda x: x.get('date', ''))
    except json.JSONDecodeError:
        # Return empty list if JSON is invalid
        return []

def prepare_template_params(repo_name, contributors_data, width=580, height=140):
    """
    Prepare parameters for template URL.
    
    Args:
        repo_name (str): Name of the repository
        contributors_data (str): JSON-encoded string of contributors data
        width (int): Width of the GIF in pixels
        height (int): Height of the GIF in pixels
        
    Returns:
        dict: Dictionary of template parameters
    """
    # First animation state (initial)
    initial_params = {
        "repo_name": repo_name,
        "contributors": urllib.parse.quote(contributors_data),
        "animation_state": "initial",
        "width": width,
        "height": height
    }
    
    # Second animation state (animated)
    animated_params = {
        "repo_name": repo_name,
        "contributors": urllib.parse.quote(contributors_data),
        "animation_state": "animated",
        "width": width,
        "height": height
    }
    
    return {
        "initial": initial_params,
        "animated": animated_params
    }