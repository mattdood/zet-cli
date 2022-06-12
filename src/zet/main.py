"""Zet tool's main execution."""
import argparse
import pprint
import sys
import textwrap
from typing import Optional, Sequence

from .zet import Zet, bulk_import_zets
from .editor_commands import open_editor
from .git_commands import (git_add_zets, git_commit_zets, git_init_zets,
                           git_pull_zets, git_push_zets)
from .repo import Repo
from .settings import Settings

FUNCTION_MAP = {
    # Zet commands
    "create": Zet.create,

    # Repo commands
    "list": Repo.list_zets,
    "add_repo": Repo.add_repo,

    # Git commands
    "add": git_add_zets,
    "commit": git_commit_zets,
    "init": git_init_zets,
    "pull": git_pull_zets,
    "push": git_push_zets,

    # Editor commands
    "editor": open_editor,
}

settings = Settings()


def main(argv: Optional[Sequence[str]] = None):
    """
    TODO:
        * create should have choices for all repos in
            the config file
        * create should have a list type for tags
        * list repos should have a choice of 1 or all
        * templates should have a list option for all template
            names with paths
        * there should be a pretty printer for all options
            that print things
        * help text should be much more helpful
    """


    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="zet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(f"""
            Zettlekasten command line tools

            Installation path: `~/zets/`
            Default repo: `{settings.get_default_repo_path()}`
            Environment variables: `~/zets/.env/.local.json`
        """),
    )
    parser.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        help=f"A zet repo folder name. Defaults to {settings.get_default_repo_path()}",
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
        "-c",
        "--category",
        action="store",
        type=str,
        required=True,
        help="A zet category."
    )
    parser_create.add_argument(
        "-tag",
        "--tags",
        action="store",
        type=str,
        required=True,
        help="A set of zet tags. Format is `str` but will be parsed from a comma separated list. Ex: `tag, tag, tag`."
    )
    parser_create.add_argument(
        "-tem",
        "--template",
        action="store",
        default=settings.get_default_template(),
        help="A zet template name. Defaults to ZET_DEFAULT_TEMPLATE."
    )
    parser_create.set_defaults(which="create")

    parser_bulk = subparsers.add_parser("bulk", help="Bulk imports zets from a folder.")
    parser_bulk.add_argument(
        "-f",
        "--files_folder",
        action="store",
        type=str,
        required=True,
        help="A folder of files to copy."
    )
    parser_bulk.set_defaults(which="bulk")

    parser_add_repo = subparsers.add_parser("add_repo", help="Creates a zet repo.")
    parser_add_repo.add_argument(
        "-f",
        "--zet_path",
        action="store",
        default="~/zets/",
        help="A new zet folder path. Defaults to the `zets/` mono-folder."
    )
    parser_add_repo.set_defaults(which="add_repo")

    parser_list = subparsers.add_parser("list", help="List zets from a folder.")
    parser_list.add_argument(
        "-full",
        "--full_path",
        action="store",
        default=False,
        help="Full paths to zets. Defaults to false.",
    )
    parser_list.set_defaults(which="list")

    parser_git_init = subparsers.add_parser("init", help="Git init inside folder.")
    parser_git_init.set_defaults(which="init")

    parser_git_add = subparsers.add_parser(
        "add", help="Git add all zets inside folder."
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
    parser_git_commit.set_defaults(which="commit")

    parser_git_push = subparsers.add_parser("push", help="Git push zets in folder.")
    parser_git_push.set_defaults(which="push")

    parser_git_pull = subparsers.add_parser("pull", help="Git pull all zet repos from settings.")
    parser_git_pull.set_defaults(which="pull")

    parser_open_editor = subparsers.add_parser("editor", help="Open the editor to a repo.")
    parser_open_editor.add_argument(
        "-p",
        "--path",
        action="store",
        default=settings.get_default_repo(),
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_open_editor.add_argument(
        "-e",
        "--editor",
        action="store",
        default=settings.get_editor_command(),
        help="A zet repo folder, must be in environment variables. Defaults to ZET_DEFAULT_FOLDER.",
    )
    parser_open_editor.set_defaults(which="editor")

    if len(argv) == 0:
        argv = ["help"]
    args = parser.parse_args(argv)
    print(args.__dict__)
    print(type(args))

    if args.which == "create":
        zet = Zet()
        zet.create(
            title=args.title,
            category=args.category,
            tags=args.tags,
            zet_repo=args.zet_repo,
            template=args.template
        )
        open_editor(path=zet.path)
    elif args.which == "bulk":
        bulk_import_zets(files_folder=args.files_folder, zet_repo=args.zet_repo)
    elif args.which == "add_repo":
        repos = Repo()
        repos.add_repo(zet_repo=args.zet_repo, zet_path=args.zet_path)
    elif args.which == "list":
        repos = Repo()
        repos.list_zets(zet_repo=args.zet_repo, full_path=args.full_path)
    elif args.which == "init":
        git_init_zets(zet_repo=args.zet_repo)
    elif args.which == "add":
        git_add_zets(zet_repo=args.zet_repo)
    elif args.which == "commit":
        git_commit_zets(message=args.message, zet_repo=args.zet_repo)
    elif args.which == "push":
        git_push_zets(zet_repo=args.zet_repo)
    elif args.which == "pull":
        git_pull_zets()
    elif args.which == "editor":
        open_editor(path=args.path)
    else:
        print("Unknown command: ", args)

    pprint.pprint(vars(args))


if __name__ == "__main__":
    exit(main())
