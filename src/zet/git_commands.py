import subprocess
from typing import Dict

from .settings import ZET_DEFAULT_FOLDER, ZET_FOLDERS


def git_init_zets(zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    """Initializes a git repo.

    Params:
        zet_repo (str): A zet repo name.
            Defaults to ZET_DEFAULT_FOLDER.
        folder (Dict[str, str]): A dictionary
            of zet folders. Defaults to ZET_FOLDERS.

    Returns:
        subprocess (Pipe): Output is the terminal
            messages of the bash command.
    """
    return subprocess.check_output(['git', 'init'], cwd = folder[zet_repo])


def git_add_zets(zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    """Adds all files to staging in a repo.

    Params:
        zet_repo (str): A zet repo name.
            Defaults to ZET_DEFAULT_FOLDER.
        folder (Dict[str, str]): A dictionary
            of zet folders. Defaults to ZET_FOLDERS.

    Returns:
        subprocess (Pipe): Output is the terminal
            messages of the bash command.
    """
    return subprocess.check_output(['git', 'add', '.'], cwd = folder[zet_repo])


def git_commit_zets(message: str, zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    """Performs git commit in a repo.

    Params:
        message (str): The commit message.
        zet_repo (str): A zet repo name.
            Defaults to ZET_DEFAULT_FOLDER.
        folder (Dict[str, str]): A dictionary
            of zet folders. Defaults to ZET_FOLDERS.

    Returns:
        subprocess (Pipe): Output is the terminal
            messages of the bash command.
    """
    return subprocess.check_output(['git', 'commit', '-m', message], cwd = folder[zet_repo])


def git_push_zets(zet_repo: str = ZET_DEFAULT_FOLDER["zets"], folder: Dict[str, str] = ZET_FOLDERS):
    """Remote pushes a zet repo.

    Params:
        zet_repo (str): A zet repo name.
            Defaults to ZET_DEFAULT_FOLDER.
        folder (Dict[str, str]): A dictionary
            of zet folders. Defaults to ZET_FOLDERS.

    Returns:
        subprocess (Pipe): Output is the terminal
            messages of the bash command.
    """
    return subprocess.check_output(['git', 'push'], cwd = folder[zet_repo])


def git_pull_zets(folders: Dict[str, str] = ZET_FOLDERS) -> None:
    """Pulls all changes for every repo.

    Params:
        folder (Dict[str, str]): A dictionary
            of zet folders. Defaults to ZET_FOLDERS.
    """
    keys = list(folders.keys())
    for key in keys:
        subprocess.check_output(['git', 'pull'], cwd = folders[key])

