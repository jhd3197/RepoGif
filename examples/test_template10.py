"""
Render Modern Spotlight samples for jhd3197/Pana and jhd3197/Faro.

Writes 1200x675 and 1080x1080 GIF and MP4 files to examples/samples/.
Template 10 supersamples at 2x and eases across 30 frames.
"""
import os

from repogif.generator import generate_repo_gif

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "examples", "assets")
SAMPLES = os.path.join(ROOT, "examples", "samples")

REPOS = (
    {
        "slug": "pana",
        "repo_name": "Pana",
        "owner": "jhd3197",
        "description": "Free multiplayer browser games for friends, with customizable capybaras. Share a link and play together.",
        "language": "JavaScript",
        "topics": ["multiplayer", "browser-games", "threejs"],
        "stars": 1,
        "forks": 0,
        "accent": "#ffc629",
        "hero": os.path.join(ASSETS, "pana-hub.jpg"),
        "hero_focus": {
            (1200, 675): "94% 42%",
            (1080, 1080): "62% 50%",
        },
    },
    {
        "slug": "faro",
        "repo_name": "Faro",
        "owner": "jhd3197",
        "description": "Free, open-source file transfer and SSH client for Windows, macOS & Linux. Browse SFTP, FTP and S3, edit remote files, and preview directory syncs. An alternative to WinSCP, FileZilla and PuTTY.",
        "language": "Rust",
        "topics": ["sftp", "ssh", "rust", "tauri"],
        "stars": 50,
        "forks": 14,
        "accent": "#e9bd69",
        "hero": os.path.join(ASSETS, "faro-poster.jpg"),
        "hero_focus": {
            (1200, 675): "78% 42%",
            (1080, 1080): "58% 46%",
        },
    },
)

SIZES = (
    (1200, 675),
    (1080, 1080),
)


def render_samples():
    os.makedirs(SAMPLES, exist_ok=True)
    for repo in REPOS:
        for width, height in SIZES:
            stem = f"{repo['slug']}-{width}x{height}"
            gif_path = os.path.join(SAMPLES, stem + ".gif")
            mp4_path = os.path.join(SAMPLES, stem + ".mp4")
            focus = repo["hero_focus"]
            if isinstance(focus, dict):
                focus = focus.get((width, height))
            print(f"\nRendering {stem}...")
            generate_repo_gif(
                repo_name=repo["repo_name"],
                owner=repo["owner"],
                description=repo["description"],
                language=repo["language"],
                topics=repo["topics"],
                stars=repo["stars"],
                forks=repo["forks"],
                accent=repo["accent"],
                hero=repo["hero"],
                hero_focus=focus,
                out=gif_path,
                mp4=mp4_path,
                template="template10",
                width=width,
                height=height,
                show_forks=True,
            )


if __name__ == "__main__":
    render_samples()
