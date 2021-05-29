import json
import os
import shutil

from src.zet.settings import ZET_ENV_PATH, ZET_HOME


def create_env() -> None:
    """Creates a zet env file.

    Params:
        env_path (str): String with the
            `.local.json` path.
        project_path (str): String with the
            ZET_PROJECT path.

    Returns:
        None
    """
    example_path = os.path.join(ZET_HOME, ".env/.example.json")

    if not os.path.exists(ZET_ENV_PATH):
        shutil.copyfile(example_path, ZET_ENV_PATH)


def add_repo(zet_repo: str, zet_path: str) -> None:
    """Adds a new repo to the env file.

    Params:
        zet_repo (str): A zet repo name to
            append to an existing env file.

    Returns:
        None
    """

    if not os.path.exists(ZET_ENV_PATH):
        create_env()

    zet_repo_path = os.path.join(zet_path, zet_repo)
    if not os.path.exists(zet_repo_path):
        os.makedirs(zet_repo_path)

    new_repo = {zet_repo: zet_repo_path}

    with open(ZET_ENV_PATH, "r+") as file:
        zet_repos = json.load(file)["zet_repos"]
        zet_repos.update(new_repo)
        json.dump(zet_repos, file, indent=8)
    file.close()

