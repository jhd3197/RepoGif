# RepoGif 🎥⭐

Generate beautiful animated GIFs that mimic GitHub repo stars/forks with realistic visuals.  
Perfect for social sharing, repo previews, documentation, or just for fun.

## Features

- 🌈 Gradient backgrounds with authentic GitHub styling
- 🖱️ Realistic cursor movement and star interaction
- 🎨 Web-based animation with HTML/CSS/JS for high-quality visuals
- ⚙️ Customizable repository name, star count, and fork count
- 🔍 High-fidelity captures using Puppeteer

## Install

```bash
git clone https://github.com/yourname/RepoGif.git
cd RepoGif
pip install -e .
npm install # For Node.js dependencies
```

### Dependencies

#### Python
- Pillow - Image processing
- imageio - GIF creation
- imageio-ffmpeg - Video encoding support
- numpy - Numerical operations
- nodejs - Node.js integration
- pyppeteer - Browser automation (alternative to Puppeteer)

#### Node.js
- puppeteer - Headless browser automation
- yargs - Command line argument parsing

## Usage

### Call from Python:
```python
from repogif.generator import generate_repo_gif

generate_repo_gif(repo_name="RepoGif", stars=250, forks=30, out="output.gif")
```

### Run from CLI (after install):
```bash
repogif
```

### Advanced Options

You can customize various aspects of the generated GIF:

```python
generate_repo_gif(
    repo_name="MyAwesomeProject",
    stars="5.8k",  # Supports string format for larger numbers
    forks=397,
    out="custom_animation.gif"
)
```

## How It Works

RepoGif uses a multi-step process to create high-quality animations:

1. Generates a web-based animation using HTML, CSS, and JavaScript
2. Uses Puppeteer to capture frames from the animation
3. Compiles the frames into a smooth GIF with imageio

The web-based approach allows for more visually appealing animations with:
- Gradient backgrounds that shift colors
- Proper GitHub styling and iconography
- Realistic cursor movement and click animations
- Star button interactions with visual feedback

## Customization

You can modify the web template files in `repogif/web_template/` to:
- Adjust animation timing and speed
- Change colors and styling
- Modify cursor behavior
- Add additional UI elements

## Troubleshooting

### Common Issues

#### Missing Node.js
If you see an error about Node.js not being installed:
```
RuntimeError: Node.js is not installed or not in PATH
```
Make sure Node.js is installed and accessible from your command line.

#### Missing Puppeteer
If you encounter errors with Puppeteer:
```
RuntimeError: Puppeteer is not installed
```
Run `npm install puppeteer yargs` in the project directory.

#### Blank or Corrupted GIF
This could be due to:
- Frame capture issues - Check for browser compatibility
- Puppeteer configuration - Try running with different arguments
- File path problems - Ensure all paths are correct

## Example Output
When run, this package generates an animated GIF showing a GitHub repository with stars and forks, along with a realistic cursor animation.

---

👉 This repo is fully usable right now. Just run:

```bash
python examples/example.py
```

and you'll get a RepoGif output in the examples/ folder 🎥.