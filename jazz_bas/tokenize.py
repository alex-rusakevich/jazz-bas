from dataclasses import dataclass
from enum import Enum
from typing import List

import regex as re
from regex import compile as rec

from jazz_bas.exceptions import JassBassSyntaxError
from jazz_bas.utils import TextLoc

KEYWORDS = "print end input".split()


class TokenType(Enum):
    KEYWORD = 0
    NAME_LITERAL = 1
    STRING_LITERAL = 2
    FLOAT = 3
    INTEGER = 4
    SPEC_CHAR = 5
    SPACE = 6
    PY_CODE = 7


RE_TOKEN_PATTERNS = (
    (TokenType.PY_CODE, rec(r"```(.*?)```", re.DOTALL)),
    (TokenType.PY_CODE, rec(r"`(.*?)`")),
    (TokenType.KEYWORD, rec("|".join(KEYWORDS), re.IGNORECASE)),
    (TokenType.NAME_LITERAL, rec(r"[\w\$\%\#]+")),
    (TokenType.STRING_LITERAL, rec(r"\"([^\"]|\"\")*\"")),
    (TokenType.FLOAT, rec(r"\d+\.\d+")),
    (TokenType.INTEGER, rec(r"\d+")),
    (TokenType.SPEC_CHAR, rec(r"[\+\-\*\/\(\);,=]")),
    (TokenType.SPACE, rec(r"\s+")),
)


@dataclass
class Token:
    value: str
    token_type: TokenType
    start: int

    @property
    def end(self):
        return self.start + len(self.value)


def tokenize(code: str) -> List[Token]:
    original_code = code

    tokens = []
    curr_byte: int = 1

    while code:
        is_token_found = False

        for token_type, re_precomp in RE_TOKEN_PATTERNS:
            if m := re_precomp.match(code):
                value = m.group()

                if token_type is TokenType.PY_CODE:
                    value = m.group(1)

                tokens.append(
                    Token(value=value, token_type=token_type, start=curr_byte)
                )
                is_token_found = True
                token_end = m.end()

                code = code[token_end:]
                curr_byte += token_end
                break

        if not is_token_found:
            raise JassBassSyntaxError(
                "Unknown token at {}".format(TextLoc(original_code, curr_byte))
            )

    # print(tokens)

    return tokens
