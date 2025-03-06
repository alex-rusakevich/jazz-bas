import argparse
from pathlib import Path

from jazz_bas.exceptions import CliError
from jazz_bas.execute import jazz_execute


def main():
    parser = argparse.ArgumentParser(description="Jazzbas BASIC interpreter")

    parser.add_argument(
        "-c", "--command", type=str, help="Command to be executed directly"
    )
    parser.add_argument(
        "path", type=str, nargs="?", help="The file to be read and executed"
    )

    args = parser.parse_args()

    if args.command and args.path:
        raise CliError("Both path and command cannot be present at the same time")
    elif args.command:
        jazz_execute(args.command)
    elif args.path:
        jazz_execute(Path(args.path).read_text())
    else:
        print("Nothing to execute, stopping.")


if __name__ == "__main__":
    main()
