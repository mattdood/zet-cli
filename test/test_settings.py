import json
from typing import Dict

import pytest

from src.zet.env_setup import generate_env
from src.zet.settings import Settings
from src.zet.settings import ZET_LOCAL_ENV_PATH


def test_settings_retrieval():
    generate_env()
    default_settings = Settings(ZET_LOCAL_ENV_PATH).get_setting("defaults")
    assert isinstance(default_settings, dict)


def test_settings_update():
    generate_env()
    new_repo = {
        "some_name": {
            "folder": "some/path/",
            "template": "default"
        }
    }
    Settings(ZET_LOCAL_ENV_PATH).update_setting("zet_repos", new_repo)
    new_settings = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")
    assert any(new_repo["some_name"] == new_settings[repo] for repo in new_settings)

