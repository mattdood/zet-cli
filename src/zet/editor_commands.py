import subprocess
from typing import Dict

from .settings import ZET_DEFAULT_EDITOR


def open_editor(path: str, editor: Dict = ZET_DEFAULT_EDITOR):
    return subprocess.check_output([editor["command"], path])
