import os

from repogif.generator import get_available_templates


def test_template10_is_registered():
    assert "template10" in get_available_templates()


def test_template10_markup_supports_starred_state():
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
