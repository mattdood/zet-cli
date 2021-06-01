import json
import os
import shutil
from typing import Dict

from .settings import ZET_DEFAULT_KEY, ZET_ENV_PATH, ZET_FOLDERS, ZET_HOME


def create_env(env_path: str = ZET_ENV_PATH) -> None:
    """Creates a zet env file."""
    example_path = os.path.join(ZET_HOME, ".env/.example.json")

    if not os.path.exists(env_path):
        shutil.copyfile(example_path, env_path)


def add_repo(zet_repo: str, zet_path: str, env_path: str = ZET_ENV_PATH) -> None:
    """Adds a new repo to the env file.

    Params:
        zet_repo (str): A zet repo name to
            append to an existing env file.
        zet_path (str): The path to a new
            zet repo.
        env_path (str): A user's `.local.json`
            environment path.

    Returns:
        None
    """

    zet_repo_path = os.path.join(zet_path, zet_repo)
    if not os.path.exists(zet_repo_path):
        os.makedirs(zet_repo_path)

    new_repo = {zet_repo: zet_repo_path}

    # Loading the entire file then truncating
    # and re-writing it is pretty inefficient
    # but at least the file is small?
    config_file = open(env_path, "r+")
    config_data = json.load(config_file)
    repos = config_data["zet_repos"]
    repos.update(new_repo)
    config_file.seek(0)
    json.dump(config_data, config_file, indent=4)


def get_default_env(
    zet_default_repo: str = ZET_DEFAULT_KEY,
    folders: Dict[str, str] = ZET_FOLDERS
) -> str:
    """Returns the default zet path."""
    return os.path.join(folders[zet_default_repo])

