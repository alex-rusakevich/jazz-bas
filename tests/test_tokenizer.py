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


def test_comment():
    code = """
    PRINT "Hello o' world!" ' Comment here
    REM and comment here!
    COMMENT and even here! 
    """

    tokens = tuple(filter(lambda x: x.token_type != TokenType.SPACE, tokenize(code)))

    assert len(tokens) == 5
    assert tuple(t.token_type for t in tokens) == (
        TokenType.KEYWORD, TokenType.STRING_LITERAL, *((TokenType.COMMENT,) * 3))
