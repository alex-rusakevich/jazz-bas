from typing import List

from jazz_bas import MIN_JAZZ_BAS_VERSION, MIN_PYTHON_VERSION
from jazz_bas.exceptions import UnexpectedTokenError
from jazz_bas.parse import Command, parse
from jazz_bas.tokenize import TokenType, tokenize
from jazz_bas.utils import get_item


def jazz_compile_commands(commands: List[Command]) -> str:
    py_code = (
        """
from jazz_bas import runtime as _jbrt

_jbrt.require_python({min_python})
_jbrt.require_jazz_bas({min_jazz_bas})
    """.strip().format(min_python=MIN_PYTHON_VERSION, min_jazz_bas=MIN_JAZZ_BAS_VERSION)
        + ("\n") * 2
    )

    for command in commands:
        if command[0].token_type is TokenType.KEYWORD:
            if command[0].value == "print":
                parts = []

                py_code += "print("

                for token in command[1:]:
                    if token.token_type is TokenType.SPEC_CHAR:
                        if token.value == ",":
                            p = ""

                            if len(parts) >= 1:
                                p = parts.pop()

                            parts.append(f"_jbrt.padded_str({p})")

                        elif token.value == ";":
                            parts.append("' '")
                    else:
                        parts.append(token.value)

                if len(command[1:]) >= 1 and command[-1].value == ";":
                    parts.pop()
                    parts.append("end=''")

                parts.append("sep=''")

                py_code += ", ".join(parts)
                py_code += ")"
            if command[0].value == "input":
                variables = []
                message = "? "

                if (
                    it := get_item(command[1:], 0)
                ) and it.token_type is TokenType.STRING_LITERAL:
                    message = it.value

                    if it := get_item(command[2:], 1):
                        if it.value == ",":
                            message += "? "
                        elif it.value == ";":
                            pass

                for token in command[2:]:
                    if token.token_type is TokenType.NAME_LITERAL:
                        variables.append(token.value)
                    elif token.value == ",":
                        continue

                if len(variables) > 1:
                    py_code += f"({', '.join(variables)},) = input({message}).split()"
                elif len(variables) == 1 and variables[0].endswith("__dollar"):
                    py_code += f"{variables[0]} = input({message})"
        else:
            raise UnexpectedTokenError(
                "Unexpected token at char #{}.".format(command[0].start)
            )

        py_code += "\n"

    return py_code


def jazz_compile(jazz_code: str) -> str:
    return jazz_compile_commands(parse(tokenize(jazz_code)))
