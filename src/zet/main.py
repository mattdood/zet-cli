"""Zet tool's main execution."""
import argparse
import sys
from typing import Optional, Sequence

from zet.settings import ZET_DEFAULT_KEY, ZET_DEFAULT_TEMPLATE, ZET_DEFAULT_EDITOR

from .create import bulk_import_zets, create_zet
from .editor_commands import open_editor
from .env_setup import add_repo, get_default_env
from .git_commands import git_add_zets, git_commit_zets, git_init_zets, git_push_zets
from .list import list_zets


def main(argv: Optional[Sequence[str]] = None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="zet", description="Zettlekasten command line tools"
    )
    subparsers = parser.add_subparsers(help="sub-command help")

    parser_create = subparsers.add_parser("create", help="Creates a zet.")
    parser_create.add_argument(
        "-t",
        "--title",
        action="store",
        type=str,
        required=True,
        help="A zet title."
    )
    parser_create.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=ZET_DEFAULT_KEY,
        help="A zet repo folder name. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_create.add_argument(
        "-tem",
        "--template",
        action="store",
        default=ZET_DEFAULT_TEMPLATE,
        help="A zet template name. Defaults to ZET_DEFAULT_TEMPLATE."
    )
    parser_create.set_defaults(which="create")


    parser_add_repo = subparsers.add_parser("add_repo", help="Creates a zet repo.")
    parser_add_repo.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        required=True,
        default=ZET_DEFAULT_KEY,
        help="A zet repo title."
    )
    parser_add_repo.add_argument(
        "-f",
        "--zet_path",
        action="store",
        required=True,
        help="A new zet folder path."
    )
    parser_add_repo.set_defaults(which="add_repo")


    parser_list = subparsers.add_parser("list", help="List zets from a folder.")
    parser_list.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=ZET_DEFAULT_KEY,
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_list.add_argument(
        "-full",
        "--full_path",
        action="store",
        default=False,
        help="Full paths to zets. Defaults to false.",
    )
    parser_list.set_defaults(which="list")


    parser_git_init = subparsers.add_parser("init", help="Git init inside folder.")
    parser_git_init.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=ZET_DEFAULT_KEY,
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_git_init.set_defaults(which="init")


    parser_git_add = subparsers.add_parser(
        "add", help="Git add all zets inside folder."
    )
    parser_git_add.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=ZET_DEFAULT_KEY,
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_git_add.set_defaults(which="add")


    parser_git_commit = subparsers.add_parser(
        "commit", help="Git commit zets in folder."
    )
    parser_git_commit.add_argument(
        "-m",
        "--message",
        action="store",
        default="",
        help="Commit message. Defaults to none."
    )
    parser_git_commit.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=ZET_DEFAULT_KEY,
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_git_commit.set_defaults(which="commit")


    parser_git_push = subparsers.add_parser("push", help="Git push zets in folder.")
    parser_git_push.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_git_push.set_defaults(which="push")

    if len(argv) == 0:
        argv = ["help"]
    args = parser.parse_args(argv)
    print(args.__dict__)
    print(type(args))

    if args.which == "create":
        create_zet(title=args.title, zet_repo=args.zet_repo, template=args.template)
    elif args.which == "add_repo":
        add_repo(zet_repo=args.zet_repo, zet_path=args.zet_path)
    elif args.which == "list":
        list_zets(zet_repo=args.zet_repo, full_path=args.full_path)
    elif args.which == "init":
        git_init_zets(zet_repo=args.zet_repo)
    elif args.which == "add":
        git_add_zets(zet_repo=args.zet_repo)
    elif args.which == "commit":
        git_commit_zets(message=args.message, zet_repo=args.zet_repo)
    elif args.which == "push":
        git_push_zets(zet_repo=args.zet_repo)
    else:
        print("Unknown command: ", args)


    print(args.__dict__)


if __name__ == "__main__":
    main()
