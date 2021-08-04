import pytest

from src.zet.settings import Settings, ZET_LOCAL_ENV_PATH


def test_settings_retrieval(zet_settings):
    default_settings = Settings(ZET_LOCAL_ENV_PATH).get_setting("defaults")
    assert isinstance(default_settings, dict)

    settings = Settings(ZET_LOCAL_ENV_PATH)
    data = settings.get_setting()
    assert data != None
    assert isinstance(data, dict)

def test_settings_append_dict(zet_settings):
    key = "zet_repos"
    value = {
        "some_name": {
            "folder": "some/path/",
            "template": "default"
        }
    }
    Settings(ZET_LOCAL_ENV_PATH).append_setting(key, value)
    new_settings = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")
    assert any(value["some_name"] == new_settings[repo] for repo in new_settings)

def test_settings_update_key(zet_settings):
    keys = ["defaults", "editor", "name"]
    value = "vscode"
    Settings(ZET_LOCAL_ENV_PATH).update_setting(keys, value)
    check_settings = Settings(ZET_LOCAL_ENV_PATH).get_setting("defaults")
    assert value ==  check_settings["editor"]["name"]

def test_refresh(zet_settings):
    """
    Ensures that we can refresh the object
    state from the JSON file if it is changed
    during the program's call stack.
    """
    keys = ["defaults", "editor", "name"]
    value = "vscode"
    settings = Settings(ZET_LOCAL_ENV_PATH)
    settings.update_setting(keys, value)

    assert value != settings.get_setting("defaults")["editor"]["name"]

    check_settings = settings.refresh().get_setting("defaults")
    assert value == check_settings["editor"]["name"]

