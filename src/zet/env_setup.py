import json
import os
import shutil

from .settings import ZET_DEFAULT_FOLDER, ZET_DEFAULT_KEY, ZET_ENV_PATH, ZET_HOME


def create_env(env_path: str = ZET_DEFAULT_FOLDER[ZET_DEFAULT_KEY]) -> None:
    """Creates a zet env file."""
    example_path = os.path.join(ZET_HOME, ".env/.example.json")
    local_path = os.path.join(env_path, ".env/.local.json")
    env_folders = os.path.join(env_path, ".env")

    if not os.path.exists(local_path):
        os.makedirs(env_folders)
        shutil.copyfile(example_path, local_path)


def add_repo(zet_repo: str, zet_path: str = "zets/", env_path: str = ZET_ENV_PATH) -> None:
    """Adds a new repo to the env file.

    Params:
        zet_repo (str): A zet repo name to
            append to an existing env file.
        zet_path (str): The path to a new
            zet repo. Defaults to:
            `~/zets/<your repo name>`.
        env_path (str): A user's `.local.json`
            environment path.

    Returns:
        None
    """

    clean_zet_repo = zet_repo.replace(' ', '_')
    zet_repo_path = os.path.join(zet_path, clean_zet_repo)
    if not os.path.exists(zet_repo_path):
        os.makedirs(zet_repo_path)

    new_repo = {clean_zet_repo: zet_repo_path}

    # Loading the entire file then truncating
    # and re-writing it is pretty inefficient
    # but at least the file is small?
    config_file = open(env_path, "r+")
    config_data = json.load(config_file)
    repos = config_data["zet_repos"]
    repos.update(new_repo)
    config_file.seek(0)
    json.dump(config_data, config_file, indent=4)



