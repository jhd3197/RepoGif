from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="repogif",
    version='0.0.1',
    description="Generate beautiful animated GIFs that mimic GitHub repo stars/forks with realistic visuals. Perfect for social sharing, repo previews, documentation, or just for fun.",
    author="Juan Denis",
    author_email="juan@vene.co",
    url="https://github.com/jhd3197/repogif",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "imageio",
        "imageio-ffmpeg",
        "numpy",
        "playwright"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "repogif=repogif.generator:generate_repo_gif",
        ],
    },
)