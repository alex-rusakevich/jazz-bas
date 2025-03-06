from pathlib import Path

from jazz_bas.execute import jazz_execute

TEST_DIR = Path("tests")

jazz_execute(Path(TEST_DIR, "bas", "hello.bas").read_text())
