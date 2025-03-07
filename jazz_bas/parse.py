from typing import List

from jazz_bas.tokenize import Token, TokenType
from jazz_bas.utils import escape_basic_name

Command = List[Token]


def parse(tokens: List[Token]) -> List[Command]:
    commands = []

    while tokens:
        command = []

        while True:
            if not tokens:
                break

            token = tokens.pop(0)

            if token.token_type is TokenType.SPACE:
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

            command.append(token)

        commands.append(command)

    return commands
