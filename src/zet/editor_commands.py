import os
from subprocess import call
from typing import Optional

from .settings import Settings

settings = Settings()


class EditorException(Exception):
    """The editor raised an exception.

    Typically for more arguments being passed
    than necessary or both being omitted.
    """
    pass


def open_editor(path: Optional[str] = None, zet_repo: Optional[str] = None):
    """Opens a code editor.

    Feeds a path to a text editor command from
    the config. This opens the editor with
    whatever command is provided.

    Params:
        path (Optional[str]): Path to the new zet file.
        zet_repo (Optional[str]): Name of a zet_repo.

    Returns:
        call (subprocess.call) A subprocess call to
            open a text editor with the filepath given.
    """
    EDITOR = os.environ.get('EDITOR', settings.get_editor_command())

    if zet_repo and not path:
        repo = settings.get_repo_path(zet_repo)
        return call([EDITOR, repo])
    elif path and not zet_repo:
        return call([EDITOR, path])
    else:
        raise EditorException(f"""
            Path: {path}
            Zet repo: {zet_repo}

            {"Only pass path or zet_repo" if path and zet_repo else ""}
            """)

