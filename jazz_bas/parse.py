from dataclasses import dataclass
from typing import List

from jazz_bas.tokenize import Token, TokenType
from jazz_bas.utils import escape_basic_name

Command = List[Token]


@dataclass
class Command:
    head: Token
    children: List[Token | Command]


def parse(tokens: List[Token]) -> List[Command]:
    all_commands = []

    while tokens:
        command = []

        while True:
            if not tokens:
                break

            token = tokens.pop(0)

            if token.token_type in (TokenType.SPACE, TokenType.COMMENT):
                if "\n" in token.value:  # Make new line finish command
                    break
                else:  # Skip spaces
                    continue

            if (
                    token.token_type is TokenType.NAME_LITERAL
                    or token.token_type is TokenType.KEYWORD
            ):
                token.value = token.value.lower()  # BASIC ignores case
                token.value = escape_basic_name(
                    token.value
                )  # Convert BASIC names to python
                # e.g. name$ -> name__dollar

            # Convert BASIC's mod into %
            if token.token_type is TokenType.KEYWORD and token.value == "mod":
                token.value = "%"
                token.token_type = TokenType.SPEC_CHAR
            elif token.token_type is TokenType.SPEC_CHAR and token.value == "\\":
                token.value = "//"
            elif token.token_type is TokenType.SPEC_CHAR and token.value == "^":
                token.value = "**"

            command.append(token)

        all_commands.append(Command(
            head=command[0],
            children=command[1:]
        ))

    return all_commands
