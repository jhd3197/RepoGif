from setuptools import setup, find_packages

setup(
    name="repogif",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "imageio"
    ],
    entry_points={
        "console_scripts": [
            "repogif=repogif.generator:generate_repo_gif",
        ],
    },
)