from typing import List

from jazz_bas import MIN_JAZZ_BAS_VERSION, MIN_PYTHON_VERSION
from jazz_bas.exceptions import JassBassSyntaxError
from jazz_bas.parse import Command, parse
from jazz_bas.tokenize import TokenType, tokenize
from jazz_bas.utils import TextLoc, get_item


def jazz_compile_commands(commands: List[Command], original_code: str) -> str:
    py_code = (
            """
from jazz_bas import runtime as _jbrt

_jbrt.require_python({min_python})
_jbrt.require_jazz_bas({min_jazz_bas})
        """.strip().format(min_python=MIN_PYTHON_VERSION, min_jazz_bas=MIN_JAZZ_BAS_VERSION)
            + "\n" * 2
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
            elif command[0].value == "input":
                variables = []
                message = "? "

                if (
                        it := get_item(command[1:], 0)
                ) and it.token_type is TokenType.STRING_LITERAL:
                    message = it.value

                    if (
                            it := get_item(command[2:], 1)
                    ) and it.token_type is TokenType.SPEC_CHAR:
                        if it.value == ",":
                            message += "? "
                        elif it.value == ";":
                            pass
                        else:
                            raise JassBassSyntaxError(
                                "Unexpected symbol {}".format(
                                    TextLoc(original_code, it.start)
                                )
                            )

                for token in command[2:]:
                    if token.token_type is TokenType.NAME_LITERAL:
                        variables.append(token.value)
                    elif token.value == ",":
                        continue

                if len(variables) > 1:
                    py_code += f"({', '.join(variables)},) = input({message}).split()"
                elif len(variables) == 1:
                    py_code += f"{variables[0]} = input({message})"
                else:
                    raise JassBassSyntaxError(
                        "INPUT cannot be called with no args, error at {}".format(
                            TextLoc(original_code, command[0].end)
                        )
                    )
        elif command[0].token_type is TokenType.PY_CODE:
            py_code += command[0].value
        elif command[0].token_type is TokenType.NAME_LITERAL:
            # Set value to a variable, e.g. name$ = "John"
            if (it := get_item(command, 1)) and it.token_type is TokenType.SPEC_CHAR and it.value == '=':
                py_code += command[0].value
                py_code += " = "

                for token in command[2:]:
                    if token.token_type in (
                            TokenType.STRING_LITERAL, TokenType.FLOAT, TokenType.INTEGER, TokenType.NAME_LITERAL,
                            TokenType.SPEC_CHAR):
                        py_code += token.value
                    else:
                        raise JassBassSyntaxError(
                            "Unexpected token at {}".format(TextLoc(original_code, token.start))
                        )
            else:
                curr_byte = command[0].start

                raise JassBassSyntaxError(
                    "Unexpected token at {}".format(TextLoc(original_code, curr_byte))
                )
        else:
            curr_byte = command[0].start

            raise JassBassSyntaxError(
                "Unexpected token at {}".format(TextLoc(original_code, curr_byte))
            )

        py_code += "\n"

    return py_code


def jazz_compile(jazz_code: str) -> str:
    return jazz_compile_commands(parse(tokenize(jazz_code)), jazz_code)
