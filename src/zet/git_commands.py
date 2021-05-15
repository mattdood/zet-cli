import subprocess
from typing import Dict

from .settings import ZET_DEFAULT_FOLDER, ZET_FOLDERS


def git_init_zets(zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    return subprocess.check_output(['git', 'init'], cwd = folder[zet_repo])


def git_add_zets(zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    return subprocess.check_output(['git', 'add', '.'], cwd = folder[zet_repo])


def git_commit_zets(message: str, zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    return subprocess.check_output(['git', 'commit', '-m', message], cwd = folder[zet_repo])


def git_push_zets(zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    return subprocess.check_output(['git', 'push'], cwd = folder[zet_repo])

