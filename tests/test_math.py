from pathlib import Path

from jazz_bas.execute import jazz_execute

TEST_DIR = Path(__file__).parent


def test_basic_math(capsys):
    jazz_execute(Path(TEST_DIR, "bas", "basic_math.bas").read_text())

    captured = capsys.readouterr()

    assert " ".join(captured.out.split()) == "7 1 3.5 3 343"
