from pathlib import Path

from jazz_bas.utils import TextLoc

TEST_DIR = Path("tests")

print(TextLoc(Path(TEST_DIR, "bas", "hello.bas").read_text(), 29))
