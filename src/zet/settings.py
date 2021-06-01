import json
import os
from pathlib import Path
from typing import Dict

ZET_PROJECT = Path(__file__)
ZET_HOME = ZET_PROJECT.parents[2]

ZET_ENV_PATH = os.path.join(ZET_HOME, ".env/.local.json")

# Default directory for sets
ZET_DEFAULT_KEY = "zets"
ZET_DEFAULT_FOLDER = {ZET_DEFAULT_KEY: "zets/"}
ZET_DEFAULT_EDITOR = {"editor": "vim", "command": "vim"}
ZET_DEFAULT_TEMPLATE = os.path.join(ZET_HOME, "src/zet", "templates/readme.md")

if not os.path.exists(ZET_ENV_PATH):
    from .env_setup import add_repo, create_env

    create_env()
    default_key = list(ZET_DEFAULT_FOLDER.keys())[0]
    add_repo(default_key, ZET_DEFAULT_FOLDER[default_key])

config = open(ZET_ENV_PATH, "r")
ZET_FOLDERS = json.load(config)["zet_repos"]
config.close()

def get_default_env(
    zet_default_repo: str = ZET_DEFAULT_KEY,
    folders: Dict[str, str] = ZET_FOLDERS
) -> str:
    """Returns the default zet path."""
    return os.path.join(folders[zet_default_repo])
