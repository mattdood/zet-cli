import subprocess
from typing import Dict

from .settings import Settings
from .settings import ZET_DEFAULT_REPO, ZET_LOCAL_ENV_PATH


def git_init_zets(zet_repo: str = ZET_DEFAULT_REPO):
    """Initializes a git repo.

    Params:
        zet_repo (str): A zet repo name.
            Defaults to ZET_DEFAULT_FOLDER.

    Returns:
        subprocess (Pipe): Output is the terminal
            messages of the bash command.
    """
    repo = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")[zet_repo]["folder"]
    return subprocess.check_output(['git', 'init'], cwd = repo)


def git_add_zets(zet_repo: str = ZET_DEFAULT_REPO):
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
    repo = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")[zet_repo]["folder"]
    return subprocess.check_output(['git', 'add', '.'], cwd = repo)


def git_commit_zets(message: str, zet_repo: str = ZET_DEFAULT_REPO):
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
    repo = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")[zet_repo]["folder"]
    return subprocess.check_output(['git', 'commit', '-m', message], cwd = repo)


def git_push_zets(zet_repo: str = ZET_DEFAULT_REPO):
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
    repo = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")[zet_repo]["folder"]
    return subprocess.check_output(['git', 'push'], cwd = repo)


def git_pull_zets() -> None:
    """Pulls all changes for every repo.

    Params:
        folder (Dict[str, str]): A dictionary
            of zet folders. Defaults to ZET_FOLDERS.
    """
    repos = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")
    keys = list(repos.keys())
    for key in keys:
        subprocess.check_output(['git', 'pull'], cwd = repos[key]["folder"])

