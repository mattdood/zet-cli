import subprocess

from .settings import Settings

settings = Settings()


def git_init_zets(zet_repo: str = None):
    """Initializes a git repo.

    Params:
        zet_repo (str): A zet repo name.
            Defaults to ZET_DEFAULT_FOLDER.

    Returns:
        subprocess (Pipe): Output is the terminal
            messages of the bash command.
    """
    if zet_repo:
        repo = settings.get_repo_path(zet_repo)
    else:
        # default repo
        repo = settings.get_default_repo_path()
    return subprocess.check_output(['git', 'init'], cwd = repo)


def git_add_zets(zet_repo: str = None):
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
    if zet_repo:
        repo = settings.get_repo_path(zet_repo)
    else:
        # default repo
        repo = settings.get_default_repo_path()
    return subprocess.check_output(['git', 'add', '.'], cwd = repo)


def git_commit_zets(message: str, zet_repo: str = None):
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
    if zet_repo:
        repo = settings.get_repo_path(zet_repo)
    else:
        # default repo
        repo = settings.get_default_repo_path()
    return subprocess.check_output(['git', 'commit', '-m', message], cwd = repo)


def git_push_zets(zet_repo: str = None):
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
    if zet_repo:
        repo = settings.get_repo_path(zet_repo)
    else:
        # default repo
        repo = settings.get_default_repo_path()
    return subprocess.check_output(['git', 'push'], cwd = repo)


def git_pull_zets(zet_repo: str = None) -> None:
    """Pulls all changes for every repo.

    Params:
        folder (Dict[str, str]): A dictionary
            of zet folders. Defaults to ZET_FOLDERS.
    """
    if zet_repo:
        repo = settings.get_repo_path(zet_repo)
    else:
        # default repo
        repo = settings.get_default_repo_path()

    subprocess.check_output(['git', 'pull'], cwd = repo)

