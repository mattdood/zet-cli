import json
import os
from pathlib import Path
from typing import Dict, List


ZET_PROJECT = Path(__file__)
ZET_HOME = ZET_PROJECT.parents[2]
ZET_INSTALL_PATH = "zets/"
ZET_LOCAL_ENV_FOLDER = ZET_INSTALL_PATH + ".env/"
ZET_LOCAL_ENV_PATH = ZET_LOCAL_ENV_FOLDER + ".local.json"

ZET_DEFAULT_EDITOR = {"editor": "vim", "command": "nvim"}
ZET_DEFAULT_TEMPLATE = os.path.join(ZET_HOME, "src/zet", "templates/readme.md")


class Settings:
    """Object to interact with `.local.json`.
    """

    def __init__(self, path: str):
        self.path = path
        self.data = self.load_settings(self.path)

    def refresh(self):
        self.data = self.load_settings(self.path)
        return self

    @staticmethod
    def load_settings(path: str) -> Dict:
        with open(path, "r") as file:
            data = json.load(file)
        return data

    def get_setting(self, key: str = None):
        # TODO: Test no key
        if key:
            return self.data[key]
        else:
            return self.data

    def get_defaults(self) -> Dict:
        return self.data["defaults"]

    def set_item(self, settings, keys: List[str], value) -> None:
        key = keys.pop(0)
        try:
            self.set_item(settings[key], keys, value)
        except (IndexError, KeyError):
            settings[key] = value

    def update_setting(self, keys: List[str], value) -> None:
        # retrieve data from settings
        settings_file = open(self.path, "r+")
        data = json.load(settings_file)

        # set new data values
        self.set_item(data, keys, value)

        # dump data to file
        settings_file.seek(0)
        json.dump(data, settings_file, indent=4)
        settings_file.close()

    def append_setting(self, key: str, value) -> None:
        # retrieve data from settings
        settings_file = open(self.path, "r+")
        config_data = json.load(settings_file)

        # update value
        data = config_data[key]
        data.update(value)

        # dump data to file
        settings_file.seek(0)
        json.dump(config_data, settings_file, indent=4)
        settings_file.close()


if not os.path.exists(ZET_LOCAL_ENV_PATH):
    from .env_setup import generate_env
    generate_env()


local_settings = Settings(ZET_LOCAL_ENV_PATH)
ZET_DEFAULTS = local_settings.get_setting("defaults")
ZET_DEFAULT_EDITOR = ZET_DEFAULTS["editor"]
ZET_DEFAULT_REPO = ZET_DEFAULTS["repo"]
ZET_DEFAULT_TEMPLATE = ZET_DEFAULTS["template"]

ZET_REPOS = local_settings.get_setting("zet_repos")
ZET_TEMPLATES = local_settings.get_setting("templates")

