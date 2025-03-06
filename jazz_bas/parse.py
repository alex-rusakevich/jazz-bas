from typing import List

from jazz_bas.tokenize import Token, TokenType

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
                if "\n" in token.value:
                    break
                else:
                    continue

            if (
                token.token_type is TokenType.NAME_LITERAL
                or token.token_type is TokenType.KEYWORD
            ):
                token.value = token.value.lower()

            command.append(token)

        commands.append(command)

    return commands
