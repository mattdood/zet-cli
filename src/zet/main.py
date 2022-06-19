"""Zet tool's main execution."""
import argparse
import inspect
import pprint
import textwrap
from typing import Optional, Sequence

from .editor_commands import open_editor
from .git_commands import (git_add_zets, git_commit_zets, git_init_zets,
                           git_pull_zets, git_push_zets)
from .repo import Repo
from .settings import Settings
from .zet import Zet, bulk_import_zets

# Classes are instantiated to avoid
# doing discovery with the `__qualname__` property
# then instantiating them afterward. This is just easier.
# See:
#  * `__qualname__` - https://peps.python.org/pep-3155/
#  * Classes from strs - https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
# Note: None of these classes need args.
FUNCTION_MAP = {
    # Zet commands
    "create": Zet.create,

    # Repo commands
    "list": Repo().list_zets,
    "add_repo": Repo().add_repo,

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


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    TODO:
        * list repos should have a choice of 1 or all
        * templates should have a list option for all template
            names with paths
        * there should be a pretty printer for all options
            that print things
    """

    parser = argparse.ArgumentParser(
        prog="zet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(f"""
            Zettlekasten command line tools.

            This tool creates, interacts with, and helps to
            organize individual notes. A "zet" is seen as an
            individual notes file that is stored in a "repo" (folder).

            Installation path: `~/zets/`
            Default notes repo: `{settings.get_default_repo_path()}`
            Environment variables: `~/zets/.env/.local.json`
        """),
    )
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    parser_create = subparsers.add_parser(
        "create",
        help="""Creates a zet file.

        The file has "metadata" added into the template
        based on the parameters passed to each argument.
        """,
    )
    parser_create.add_argument(
        "-t",
        "--title",
        action="store",
        type=str,
        required=True,
        help="""A zet title.

        Used to create a title in the file and
        generate a unique filename using a timestamp
        and hyphen (-) separated naming convention.

        Timestamps are in yyyyMMddHHmmS format.

        Example:
        `-t "some title"` becomes "some-title-20220102120051.md"
        """
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
        help="""A set of zet tags. Format is `str` but will be
        parsed from a comma separated list.

        Example:
        `-t 'tag, tag, tag'`
        """
    )
    parser_create.add_argument(
        "-tem",
        "--template",
        action="store",
        default=settings.get_default_template(),
        const=settings.get_default_template(),
        nargs="?",
        choices=settings.get_template_names(),
        help="""A zet template name.

        Defaults to "%(default)s".
        """
    )
    parser_create.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
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
    parser_bulk.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_bulk.set_defaults(which="bulk")

    parser_add_repo = subparsers.add_parser(
        "add_repo",
        help="""Creates a zet repo.

        Repos are folders that store zets. Separate repos
        are used to organize notes at a higher level than
        categories/tags.

        This could be useful for separating
        things like general/personal notes from work-specific
        knowledge.
        """,
    )
    parser_add_repo.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        required=True,
        default=settings.get_default_repo(),
        help="A repo folder name."
    )
    parser_add_repo.add_argument(
        "-tem",
        "--template",
        action="store",
        default=settings.get_default_template(),
        const=settings.get_default_template(),
        nargs="?",
        choices=settings.get_template_names(),
        help="""Template to use in this repo.

        Template to assign to the newly created repo.
        Defaults to "%(default)s".
        """
    )
    parser_add_repo.add_argument(
        "-f",
        "--zet_path",
        action="store",
        default="~/zets/",
        help="""A new zet folder path.

        Defaults to the `~/zets/` installation directory.

        Only use this if you need your zets to be stored separately
        from where the installation directory is. Not advised for
        general use, as it breaks the organization design of the tool.
        """
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
    parser_list.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_list.set_defaults(which="list")

    parser_git_init = subparsers.add_parser("init", help="Git init inside a repo.")
    parser_git_init.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_git_init.set_defaults(which="init")

    parser_git_add = subparsers.add_parser(
        "add",
        help="Git add all untracked zets inside a repo.",
    )
    parser_git_add.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_git_add.set_defaults(which="add")

    parser_git_commit = subparsers.add_parser("commit", help="Git commit zets in a repo.")
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
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_git_commit.set_defaults(which="commit")

    parser_git_push = subparsers.add_parser("push", help="Git push zets in a repo.")
    parser_git_push.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_git_push.set_defaults(which="push")

    parser_git_pull = subparsers.add_parser("pull", help="Git pull zet repo.")
    parser_git_pull.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_git_pull.set_defaults(which="pull")

    parser_open_editor = subparsers.add_parser("editor", help="Open the editor to a repo.")
    parser_open_editor.add_argument(
        "-r",
        "--zet_repo",
        action="store",
        default=settings.get_default_repo(),
        const=settings.get_default_repo(),
        nargs="?",
        choices=settings.get_repo_names(),
        help="""A zet repo folder name. Defaults to "%(default)s".
        This option is available for all sub-commands.
        """,
    )
    parser_open_editor.set_defaults(which="editor")

    args = parser.parse_args(argv)

    pprint.pprint(vars(args))

    if args.command:
        # Map arg to command
        func = FUNCTION_MAP[args.command]

        # Filter argparse specific keys from
        # argument values to only ones used
        # in the function call.
        # This could be done with `**_` as a "kwargs"
        # placeholder in the function as well.
        # Inspiration: https://stackoverflow.com/a/43238973/12387496
        filtered_args = {}
        func_params = [param.name for param in inspect.signature(func).parameters.values()]
        for key, value in vars(args).items():
            if key in func_params:
                filtered_args[key] = value

        # Edge case handling
        # for anything that has multiple function
        # calls outside the function map
        if args.command == "create":
            zet = Zet()
            zet.create(**filtered_args)
            open_editor(path=zet.path)
        else:
            func(**filtered_args)

    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    exit(main())

