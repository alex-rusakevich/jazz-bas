from pathlib import Path

from jazz_bas.execute import jazz_execute

TEST_DIR = Path(__file__).parent


def test_hello_bas(capsys):
    jazz_execute(Path(TEST_DIR, "bas", "hello.bas").read_text())

    captured = capsys.readouterr()

    assert captured.out == "Hello, World!\n"
