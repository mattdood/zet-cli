import os
from subprocess import call
from typing import Dict

from .settings import Settings, ZET_LOCAL_ENV_PATH

settings = Settings(ZET_LOCAL_ENV_PATH)


def open_editor(path: str):

    EDITOR = os.environ.get('EDITOR', settings.get_editor_command())
    return call([EDITOR, path])
