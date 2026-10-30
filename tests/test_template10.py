import os

from PIL import Image

from repogif.generator import (
    _GIF_BYTE_LIMIT,
    _frame_duration_ms,
    _normalize_accent,
    _pad_even,
    _resolve_frames,
    _resolve_scale,
    _save_animated_gif,
    get_available_templates,
)


def test_template10_is_registered():
    assert "template10" in get_available_templates()


def test_template10_markup_supports_spotlight_fields():
    template_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "repogif",
        "templates",
        "template10",
        "template.html",
    )
    with open(template_path, encoding="utf-8") as handle:
        html = handle.read()

    assert 'class="repo-name"' in html
    assert 'class="star-count"' in html
    assert 'class="fork-count"' in html
    assert "starred" in html
    assert "show_forks" in html
    assert 'id="description"' in html
    assert 'id="language-badge"' in html
    assert 'id="topics"' in html
    assert 'id="hero"' in html
    assert "easeInOutCubic" in html
    assert "progress" in html
    assert "accent" in html


def test_template10_defaults_are_animated_and_hidpi():
    assert _resolve_frames("template10", None) == 30
    assert _resolve_frames("template1", None) == 2
    assert _resolve_scale("template10", None) == 2
    assert _resolve_scale("template1", None) == 1
    assert _frame_duration_ms(2, 20) == 1000
    assert _frame_duration_ms(30, 20) == 50


def test_accent_normalizes_short_hex():
    assert _normalize_accent("#fc0") == "#ffcc00"
    assert _normalize_accent(None) is None


def test_mp4_padding_makes_even_dimensions():
    image = Image.new("RGB", (1200, 675), (8, 10, 16))
    padded = _pad_even(image)
    assert padded.size == (1200, 676)


def test_animated_gif_stays_compact(tmp_path):
    frames = []
    for index in range(12):
        image = Image.new("RGB", (240, 120), (12, 14, 22))
        pixels = image.load()
        for y in range(30, 100):
            for x in range(90, 220):
                pixels[x, y] = ((x * 3) % 255, (y * 5) % 255, 90)
        for y in range(16, 42):
            for x in range(16 + index * 6, 36 + index * 6):
                pixels[x, y] = (255, 198, 64)
        frames.append(image)

    path = tmp_path / "clip.gif"
    _save_animated_gif(frames, str(path), 50)
    assert path.stat().st_size < _GIF_BYTE_LIMIT
    with Image.open(path) as gif:
        assert gif.n_frames == 12
        assert gif.size == (240, 120)
