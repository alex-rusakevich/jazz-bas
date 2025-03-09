from pathlib import Path

from jazz_bas.execute import jazz_execute

TEST_DIR = Path(__file__).parent


def test_embeddable_python(capsys):
    jazz_execute(Path(TEST_DIR, "bas", "python_in_basic.bas").read_text())

    captured = capsys.readouterr()

    assert captured.out.split() == ["2", "3"]
