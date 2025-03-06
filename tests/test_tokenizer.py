from pathlib import Path

from jazz_bas.tokenize import TokenType, tokenize

TEST_DIR = Path(__file__).parent


def test_print_hello():
    bas_text = Path(TEST_DIR, "bas", "hello.bas").read_text()
    tokens = tokenize(bas_text)

    assert len(tokens) == 3
    assert [t.token_type for t in tokens] == [
        TokenType.KEYWORD,
        TokenType.SPACE,
        TokenType.STRING_LITERAL,
    ]
    assert [t.value for t in tokens] == ["PRINT", " ", '"Hello, World!"']
