import json
import os
import shutil
from pathlib import Path
from typing import Dict, List

# Project install defaults
ZET_PROJECT = Path(__file__)
ZET_HOME = ZET_PROJECT.parents[2]

# Check env stage (test)
if os.environ.get("ZET_STAGE") == "test":
    ZET_INSTALL_PATH = ZET_HOME / "zet/"
else:
    ZET_INSTALL_PATH = Path.home() / "zet/"


class Settings:
    """Object to interact with `.local.json`.

    The settings for this project are created
    at runtime if they don't exist already. This ensures
    that the user has a defaulted config upon installation,
    this can be replaced later at the `~/zet/.env/.local.json`
    path.

    Settings are stored in JSON to allow flexibility,
    this means that there are some occassions where
    the settings will change during execution and require
    refreshing from the file.

    To conserve space elsewhere and keep references DRY there
    are quite a few getter methods to allow access to the
    underlying configuration file.
    """

    def __init__(self, install_path: Path = ZET_INSTALL_PATH) -> None:
        """Initializes all settings from a given `.local.json` file.

        If the file does not exist it will be created from the
        `.env/.example.json` file to initialize basic settings.

        Users that already have a previous installation can copy
        their existing file over the one that the installation
        creates.

        Params:
            install_path (Path): Path to install the application
                settings. This can be changed, really only for
                testing. Defaults to `~/zets/`

        Returns:
            None
        """

        self.zet_local_env_folder = install_path / ".env/"
        self.zet_local_env_path = self.zet_local_env_folder / ".local.json"

        if not install_path.exists():
            example_settings = ZET_HOME / ".env/.example.json"
            os.makedirs(self.zet_local_env_folder)
            shutil.copyfile(example_settings, self.zet_local_env_path)

        self.install_path = install_path
        self.data = self.load_settings(self.zet_local_env_path)

        # after initial setup the template and default repo need
        # to have a path discovery, then add them to the config
        if self.data["templates"]["default"] == "":
            keys = ["templates", "default"]
            value = ZET_HOME / "src/zet/templates/readme.md"
            self.update_setting(keys, value.as_posix())

        if self.data["zet_repos"]["zets"]["folder"] == "":
            keys = ["zet_repos", "zets", "folder"]
            value = ZET_INSTALL_PATH / "zets"
            self.update_setting(keys, value.as_posix())

    def refresh(self):
        """Checks for settings changes.

        If an execution creates a change in the
        settings, then relies on that change during
        the remainder of the process it will need
        to reference an up-to-date set of data.

        This ensures all data is kept in-line with the
        JSON file.

        Example:
            1. User installs for the first time
            1. Executing a `zet create` immediately means there
                are no template paths because the initial data load
                did not have one (env is being set up).
            1. Refreshing enables the user to have that change caught
                during execution time. (See `Zet.create()`)
        """
        self.data = self.load_settings(self.zet_local_env_path)
        return self

    @staticmethod
    def load_settings(path: Path) -> Dict:
        """Load settings from the JSON file.

        Params:
            path (Path): Path to a settings file.

        Returns:
            data (Dict): Dictionary of all settings.
        """
        with path.open("r") as file:
            data = json.load(file)
        return data

    def get_setting(self, key: str = None) -> Dict:
        """Fetches a block of settings.

        Params:
            key (str): A settings key to `.local.json`.

        Returns:
            settings (Dict): The top-level settings
                for a key. Defaults to all settings.
        """
        if key:
            return self.data[key]
        else:
            return self.data

    def get_defaults(self) -> Dict:
        """Returns all default settings."""
        return self.data["defaults"]

    def set_item(self, settings, keys: List[str], value) -> None:
        """Recursively check settings against keys.

        Recurses a list of keys to arrive at
        the final key, then set the value to
        something new.
        """
        key = keys.pop(0)
        try:
            self.set_item(settings[key], keys, value)
        except (IndexError, KeyError):
            settings[key] = value

    def update_setting(self, keys: List[str], value) -> None:
        """Updates a setting.

        Changes the underlying JSON config
        by traveling down a list of keys
        (in order) to update the destination value.

        TODO:
            * This can probably be revised.
        """
        # retrieve data from settings
        settings_file = self.zet_local_env_path.open("r+")
        data = json.load(settings_file)

        # set new data values
        self.set_item(data, keys, value)

        # dump data to file
        settings_file.seek(0)
        json.dump(data, settings_file, indent=4)
        settings_file.close()

        # If settings are still used after updating
        # we need to refresh it or they won't be
        # recognized
        self.refresh()

    def append_setting(self, key: str, value) -> None:
        """Adds a new entry to a setting.

        This allows for things like new repos,
        and templates.
        """
        # retrieve data from settings
        settings_file = self.zet_local_env_path.open("r+")
        config_data = json.load(settings_file)
        settings_file.close()

        # update value
        data = config_data[key]
        data.update(value)

        # dump data to file
        with self.zet_local_env_path.open("w") as settings_file:
            json.dump(config_data, settings_file, indent=4)
            settings_file.close()

    def get_default_repo(self) -> str:
        """Returns folder path of default repo."""
        return self.data["defaults"]["repo"]

    def get_default_repo_path(self) -> str:
        """Returns folder path of default repo."""
        return self.data["zet_repos"][self.data["defaults"]["repo"]]["folder"]

    def get_templates(self) -> Dict:
        """Returns all templates."""
        return self.data["templates"]

    def get_template_names(self) -> List[str]:
        """Returns all template names."""
        return self.data["templates"].keys()

    def get_default_template(self) -> str:
        """Returns the default template."""
        return self.data["defaults"]["template"]

    def get_default_template_path(self) -> str:
        """Returns the default template."""
        return self.data["templates"]["default"]

    def get_template_path(self, template_name: str) -> str:
        """Returns the path of a template file.

        Params:
            template_name (str): Name of a template file.

        Returns:
            path (str): The path to a template.
        """
        return self.data["templates"][template_name]

    def get_repo_template_path(self, repo_name: str) -> str:
        """Returns the path of a template file from a repo name.

        Params:
            repo_name (str): Name of a repository.

        Returns:
            path (str): The path to a template.
        """
        return self.data["templates"][self.data["zet_repos"][repo_name]["template"]]

    def get_repo_path(self, repo_name: str) -> str:
        """Returns a repo path from a repo name.

        Params:
            repo_name (str): Name of a repository.

        Returns:
            path (str): The path to a repository folder.
        """
        return self.data["zet_repos"][repo_name]["folder"]

    def get_repos(self) -> Dict:
        """Returns all repos.

        Returns:
            repos (Dict): The settings for all
                repositories.
        """
        return self.data["zet_repos"]

    def get_repo_names(self) -> List[str]:
        """Returns all repo names.

        Returns:
            repos (List[str]): The settings for all
                repository names.
        """
        return self.data["zet_repos"].keys()

    def get_editor_command(self) -> str:
        """Returns the command to open an editor."""
        return self.data["defaults"]["editor"]["command"]

