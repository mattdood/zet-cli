import json
import os
from pathlib import Path

ZET_PROJECT = Path(__file__)
ZET_HOME = ZET_PROJECT.parents[2]

ZET_ENV_PATH = os.path.join(ZET_HOME, ".env/.local.json")

# Default directory for sets
ZET_DEFAULT_FOLDER = {"zets": "~/zets/"}
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

print(ZET_FOLDERS)
