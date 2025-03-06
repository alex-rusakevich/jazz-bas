from enum import Enum
from re import compile as rec
from jass_bas.exceptions import TokenError
from typing import List
from collections import OrderedDict


class TokenType(Enum):
    FUNC_NAME = 0
    STRING_LITERAL = 1
    NUMBER = 2
    SPEC_CHAR = 3
    SPACE = 4


RE_TOKEN_PATTERNS = (
    (TokenType.FUNC_NAME, rec(r"[\w\$\%\#]+")),
    (TokenType.STRING_LITERAL, rec(r'\"([^\"]|\"\")*\"')),
    (TokenType.SPACE, rec(r'\s+'))
)


class Token:
    value: str
    token_type: TokenType
    start: int

    def __init__(self, value: str, token_type: TokenType, start: int):
        self.value = value
        self.token_type = token_type
        self.start = start


def tokenize(code: str) -> List[Token]:
    tokens = []

    while code:
        is_token_found = False
        curr_byte = 1

        for token_type, re_precomp in RE_TOKEN_PATTERNS:
            if m := re_precomp.match(code):
                tokens.append(
                    Token(
                        value=m.group(), 
                        token_type=token_type,
                        start=m.start()
                        )
                )
                is_token_found = True
                code = code[m.end():]
                curr_byte += m.end()
                break
        
        if not is_token_found:
            raise TokenError("Unknown token at pos {}: `{}...`"
                .format(curr_byte, code[:16]))
    
    return tokens