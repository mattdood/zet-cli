"""Zet tool's main execution."""
import argparse
import sys
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="zet", description="Zettlekasten command line tools"
    )
    subparsers = parser.add_subparsers(help="sub-command help")

    parser_create = subparsers.add_parser("create", help="Creates a zet.")
    parser_create.add_argument(
        "-t", "--title", action="store", required=True, help="A zet title."
    )
    parser_create.add_argument(
        "-f",
        "--folder",
        action="store",
        help="A zet repo folder name. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_create.add_argument(
        "-tem", "--template", action="store", help="A zet template name."
    )

    parser_list = subparsers.add_parser("list", help="List zets from a folder.")
    parser_list.add_argument(
        "-f",
        "--folder",
        action="store",
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_list.add_argument(
        "-full",
        "--full_path",
        action="store",
        help="Full paths to zets. Defaults to false.",
    )

    parser_git_init = subparsers.add_parser("init", help="Git init inside folder.")
    parser_git_init.add_argument(
        "-f",
        "--folder",
        action="store",
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )

    parser_git_add = subparsers.add_parser(
        "add", help="Git add all zets inside folder."
    )
    parser_git_add.add_argument(
        "-f",
        "--folder",
        action="store",
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )

    parser_git_commit = subparsers.add_parser(
        "commit", help="Git commit zets in folder."
    )
    parser_git_commit.add_argument(
        "-m", "--message", action="store", help="Commit message. Defaults to zet name."
    )
    parser_git_commit.add_argument(
        "-f",
        "--folder",
        action="store",
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )

    parser_git_push = subparsers.add_parser("push", help="Git push zets in folder.")
    parser_git_push.add_argument(
        "-f",
        "--folder",
        action="store",
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )

    if len(argv) == 0:
        argv = ["help"]
    args = parser.parse_args(argv)
    print(args.__dict__)


if __name__ == "__main__":
    main()
