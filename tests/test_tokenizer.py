from pathlib import Path
from jass_bas.tokenize import tokenize

TEST_DIR = Path(__file__).parent

def test_print_hello():
    bas_text = Path(TEST_DIR, 'bas', 'hello.bas').read_text()
    print(tokenize(bas_text))
    assert 1 == 1
