import os
import subprocess

from .settings import ZET_DEFAULT


def git_init_zets(folder: str = ZET_DEFAULT):
    return subprocess.check_output(['git', 'init'], cwd = folder)


def git_add_zets(folder: str = ZET_DEFAULT):
    return subprocess.check_output(['git', 'add', '.'], cwd = folder)


def git_commit_zets(message: str, folder: str = ZET_DEFAULT):
    return subprocess.check_output(['git', 'commit', '-m', message], cwd = folder)


def git_push_zets(folder: str = ZET_DEFAULT):
    return subprocess.check_output(['git', 'push'], cwd = folder)

