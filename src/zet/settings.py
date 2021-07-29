import json
import os
from pathlib import Path
from typing import Dict


ZET_PROJECT = Path(__file__)
ZET_HOME = ZET_PROJECT.parents[2]
ZET_INSTALL_PATH = "zets/"
ZET_LOCAL_ENV_FOLDER = ZET_INSTALL_PATH + ".env/"
ZET_LOCAL_ENV_PATH = ZET_LOCAL_ENV_FOLDER + ".local.json"

ZET_DEFAULT_EDITOR = {"editor": "vim", "command": "nvim"}
ZET_DEFAULT_TEMPLATE = os.path.join(ZET_HOME, "src/zet", "templates/readme.md")


class Settings:

    def __init__(self, path: str):
        self.path = path
        self.data = self.load_settings(self.path)

    @staticmethod
    def load_settings(path: str) -> Dict:
        with open(path, "r") as file:
            data = json.load(file)
        return data

    def get_setting(self, key: str):
        return self.data[key]

    def update_setting(self, key: str, value) -> None:
        settings_file = open(self.path, "r+")
        data = json.load(settings_file)
        data[key].update(value)
        settings_file.seek(0)
        json.dump(data, settings_file, indent=4)
        settings_file.close()


if not os.path.exists(ZET_LOCAL_ENV_PATH):
    from src.zet.env_setup import generate_env
    generate_env()

local_settings = Settings(ZET_LOCAL_ENV_PATH)
ZET_DEFAULTS = local_settings.get_setting("defaults")
ZET_REPOS = local_settings.get_setting("zet_repos")
ZET_TEMPLATES = local_settings.get_setting("templates")

ZET_DEFAULT_REPO = "zets"
ZET_DEFAULT_FOLDER = {ZET_DEFAULT_REPO: "zets/"}

