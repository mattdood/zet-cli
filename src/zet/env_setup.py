import os
import shutil
from pathlib import Path

from src.zet.settings import ZET_ENV_PATH, ZET_HOME


def create_env(env_path: str = ZET_ENV_PATH, project_path: Path = ZET_HOME) -> None:
    """Creates a zet env file.

    Params:
        env_path (str): String with the
            `.local.json` path.
        project_path (str): String with the
            ZET_PROJECT path.

    Returns:
        None
    """
    example_path = os.path.join(project_path, ".env/.example.json")

    if not os.path.exists(env_path):
        shutil.copyfile(example_path, env_path)


def add_repo(zet_repo: str, folder: str, env_path: str = ZET_ENV_PATH):
    pass
