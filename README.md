# RepoGif 🎥⭐

Generate beautiful animated GIFs that mimic GitHub repo stars/forks with realistic visuals.  
Perfect for social sharing, repo previews, documentation, or just for fun.

## Features

- 🌈 Gradient backgrounds with authentic GitHub styling
- 🎨 Web-based animation with HTML/CSS/JS for high-quality visuals
- ⚙️ Customizable repository name, star count, and fork count
- 🔍 High-fidelity captures using Puppeteer
<br><br>

> [!TIP]
> Starring this repo helps more developers discover RepoGif 🎥
>
> ![template1_1k](https://github.com/user-attachments/assets/bf87874c-e22a-45d3-a5d8-6c30d4de478a)
> 
<br>

## Install

```bash
git clone https://github.com/yourname/RepoGif.git
cd RepoGif
pip install -e .
playwright install
```

### Dependencies

- Pillow - Image processing
- imageio - GIF creation
- imageio-ffmpeg - Video encoding support
- numpy - Numerical operations
- playwright - Browser automation

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

1. Uses static HTML templates with customizable parameters via URL query strings
2. Uses Playwright to capture two frames (unstarred and starred states)
3. Creates final GIF using PIL with 1-second duration per frame

The template-based approach allows for visually appealing animations with:
- Gradient backgrounds
- Proper GitHub styling and iconography
- Realistic cursor positioning
- Star button interactions with visual feedback

## Customization

The templates are located in `repogif/templates/`, with each template in its own directory:
- Each template has its own template.html file and necessary assets
- Templates can be customized via URL parameters:
  - Repository name
  - Star count
  - Fork count
  - Display dimensions
- You can also create new templates following the existing structure

---

👉 This repo is fully usable right now. Just run:

```bash
python examples/example.py
```

and you'll get a RepoGif output in the examples/ folder 🎥.

## Templates

RepoGif offers a variety of templates to showcase your repository in different styles and formats. Choose the one that best suits your needs.

### Template 1 - Simple Star Animation

A simple 2-frame GIF showing star button animation with authentic GitHub styling.

![template1_1k](https://github.com/user-attachments/assets/8481b384-8f3f-432e-bc64-33fccde73c6f)


**Default Dimensions**: Variable based on content

**Variants**:
- ![template1_no_forks](https://github.com/user-attachments/assets/ec88df4b-9e02-4d60-a9dd-dc7320bf62ec)
- ![template1_100stars](https://github.com/user-attachments/assets/dc08e923-31ef-4020-8d85-a550737cac9a)

### Template 2 - Square Badge

A square badge displaying repository statistics with clean, modern design.

![square_badge_test](https://github.com/user-attachments/assets/f4956ab0-ee3a-47f1-a3b8-8aa15555ee10)

**Default Dimensions**: 250x250 pixels

### Template 3 - Horizontal Banner

A wide banner perfect for repository headers or documentation pages.

![horizontal_banner_test](https://github.com/user-attachments/assets/4c2c7d0d-8826-40d5-82be-fa83bfbafc9c)

**Default Dimensions**: 600x120 pixels

### Template 4 - Circular Badge

A circular badge with focused repository statistics in a compact form.

![circular_badge_test](https://github.com/user-attachments/assets/6910f76f-30ad-4545-957d-4473b688f61a)

**Default Dimensions**: 250x250 pixels

### Template 5 - Vertical Card

A vertical card layout with gradient background for an elegant presentation.

![vertical_card_test](https://github.com/user-attachments/assets/f6830676-8950-4499-ba00-a5e6589ac47b)

**Default Dimensions**: 300x400 pixels

### Template 6 - Minimalist Tile

A clean, monochrome design focusing on essential repository information.

![minimalist_tile_test](https://github.com/user-attachments/assets/0ed364f5-68c1-4b2d-a2ba-bbc6d6fdec1c)

**Default Dimensions**: 320x200 pixels

### Template 7 - Animated Badge

An eye-catching badge with pulsing star effect animation.

![animated_badge_test](https://github.com/user-attachments/assets/faaecbe6-09a3-40f5-9dfa-092a71c9c846)

**Default Dimensions**: 280x280 pixels


## Troubleshooting

### Common Issues


#### Blank or Corrupted GIF
This could be due to:
- Frame capture issues - Check for browser compatibility
- Puppeteer configuration - Try running with different arguments
- File path problems - Ensure all paths are correct

## Example Output
When run, this package generates an animated GIF showing a GitHub repository with stars and forks, along with a realistic cursor animation.
