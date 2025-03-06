from dataclasses import dataclass


@dataclass
class TextLoc:
    line: int
    column: int
    original_code: str

    def __init__(self, original_code: str, start: int):
        self.original_code = original_code

        code = original_code[:start]

        print(code)

        self.line = code.count("\n") + 1

        if self.line == 1:
            self.column = len(code)
        else:
            self.column = len(code[code.rfind("\n") + 1 :])

    def __str__(self):
        return "line {}, column {}:\n\t{}\n\t{}".format(
            self.line,
            self.column,
            self.original_code.split("\n")[self.line - 1],
            ("~" * (self.column - 1)) + "^",
        )
