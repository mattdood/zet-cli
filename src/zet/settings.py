import json
import os
from pathlib import Path

ZET_PROJECT = Path(__file__)
ZET_HOME = ZET_PROJECT.parents[2]

ZET_ENV_PATH = os.path.join(ZET_HOME, ".env/.local.json")

if not os.path.exists(ZET_ENV_PATH):
    from .env_setup import create_env

    create_env(ZET_ENV_PATH, ZET_HOME)

# Default directory for sets
ZET_DEFAULT_FOLDER = {"zets": "~/zets/"}
ZET_DEFAULT_EDITOR = {"editor": "vim", "command": "vim"}
ZET_DEFAULT_TEMPLATE = os.path.join(ZET_HOME, "src/zet", "templates/readme.md")

ZET_ENV_JSON = open(ZET_ENV_PATH)
ZET_FOLDERS = json.load(ZET_ENV_JSON)["zet_repos"]
ZET_FOLDERS.update(ZET_DEFAULT_FOLDER)
