import importlib.util

import pytest
from PIL import Image

from repogif.generator import generate_repo_gif, get_available_templates

CODE = 'generate_repo_gif(\n    repo_name="RepoGif",\n    template="template13",\n    out="run.gif",\n)'


def test_available_templates_all_exist():
    names = get_available_templates()
    assert "template13" in names
    for name in names:
        assert importlib.util.find_spec(f"repogif.templates.{name}") is not None
    assert "template12" not in names


def test_missing_template_gives_clear_error(tmp_path):
    with pytest.raises(ValueError, match="template12"):
        generate_repo_gif(template="template12", out=str(tmp_path / "x.gif"))


def test_template13_renders_multiple_frames(tmp_path):
    out = tmp_path / "run.gif"
    generate_repo_gif(
        repo_name="RepoGif",
        owner="jhd3197",
        template="template13",
        code=CODE,
        accent="#e3b341",
        out=str(out),
        width=480,
        height=270,
        frames=6,
    )
    assert out.exists()
    with Image.open(out) as gif:
        assert gif.n_frames > 1
