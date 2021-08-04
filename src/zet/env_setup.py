import json
import os
import shutil

from .settings import Settings, ZET_HOME, ZET_LOCAL_ENV_FOLDER, ZET_LOCAL_ENV_PATH


def generate_env() -> None:
    example_settings = os.path.join(ZET_HOME, ".env/.example.json")

    if not os.path.exists(ZET_LOCAL_ENV_PATH):
        os.makedirs(ZET_LOCAL_ENV_FOLDER)
        shutil.copyfile(example_settings, ZET_LOCAL_ENV_PATH)

        # add location of default template
        keys = ["templates", "default", "path"]
        value = os.path.join(ZET_HOME, "src/zet/templates/readme.md")
        settings = Settings(ZET_LOCAL_ENV_PATH)
        settings.update_setting(keys, value)


def add_repo(zet_repo: str, zet_path: str = "zets/", template: str = "default") -> None:
    """Adds a new repo to the env file.

    Params:
        zet_repo (str): A zet repo name to
            append to an existing env file.
        zet_path (str): The path to a new
            zet repo. Defaults to:
            `zets/<your repo name>`.

    Returns:
        None
    """

    clean_zet_repo = zet_repo.replace(' ', '_')
    zet_repo_path = os.path.join(zet_path, clean_zet_repo)
    if not os.path.exists(zet_repo_path):
        os.makedirs(zet_repo_path)

    new_repo = {
        clean_zet_repo: {
            "folder": zet_repo_path,
            "template": template
        }
    }

    settings = Settings(ZET_LOCAL_ENV_PATH)
    settings.append_setting("zet_repos", new_repo)
