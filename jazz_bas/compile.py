from typing import List

from jazz_bas import MIN_PYTHON_VERSION
from jazz_bas.exceptions import UnexpectedTokenError
from jazz_bas.parse import Command, parse
from jazz_bas.tokenize import TokenType, tokenize


def jazz_compile_commands(commands: List[Command]) -> str:
    py_code = (
        """
from jazz_bas import runtime as _jazz_runtime

_jazz_runtime.require_python({min_python})
    """.strip().format(min_python=MIN_PYTHON_VERSION)
        + ("\n") * 2
    )

    for command in commands:
        if command[0].token_type is TokenType.KEYWORD:
            if command[0].value == "print":
                py_code += "print("

                if len(command) > 1:
                    py_code += ", ".join((t.value for t in command[1:]))

                py_code += ")"
        else:
            raise UnexpectedTokenError(
                "Unexpected token at char #{}.".format(command[0].start)
            )

        py_code += "\n"

    return py_code


def jazz_compile(jazz_code: str) -> str:
    return jazz_compile_commands(parse(tokenize(jazz_code)))
