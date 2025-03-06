import argparse
from pathlib import Path

from jazz_bas.compile import jazz_compile


def main():
    parser = argparse.ArgumentParser(description="Jazzbas BASIC to Python compiler")

    parser.add_argument("-o", "--output", type=str, help="Resulting .py path")
    parser.add_argument(
        "path", type=str, nargs="?", help="The file to be read and compiled"
    )

    args = parser.parse_args()

    if args.path:
        py_code = jazz_compile(Path(args.path).read_text())

        output_path = Path(args.path).with_suffix(".py")

        if args.output:
            output_path = args.output

        Path(output_path).write_text(py_code)
    else:
        print("Nothing to compile, stopping.")


if __name__ == "__main__":
    main()
