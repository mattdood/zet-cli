import os
from subprocess import call
from typing import Dict

from .settings import ZET_DEFAULT_EDITOR


def open_editor(path: str, editor: Dict = ZET_DEFAULT_EDITOR):
    EDITOR = os.environ.get('EDITOR', editor["command"])
    return call([EDITOR, path])
