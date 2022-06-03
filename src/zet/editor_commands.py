import os
from subprocess import call

from .settings import ZET_LOCAL_ENV_PATH, Settings

settings = Settings(ZET_LOCAL_ENV_PATH)


def open_editor(path: str):
    """Opens a code editor.

    Feeds a path to a text editor command from
    the config. This opens the editor with
    whatever command is provided.

    Params:
        path (str): Path to the new zet file.

    Returns:
        call (subprocess.call) A subprocess call to
            open a text editor with the filepath given.
    """

    EDITOR = os.environ.get('EDITOR', settings.get_editor_command())
    return call([EDITOR, path])
