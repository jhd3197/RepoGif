from repogif.generator import generate_repo_gif
import os

def test_generate():
    out_file = "test.gif"
    generate_repo_gif(repo_name="testrepo", stars=5, forks=2, out=out_file)
    assert os.path.exists(out_file)