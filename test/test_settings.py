import pytest


def test_env_generates(zet_settings):
    """Creates local settings.

    We have to cleanup any other test
    settings that may exist prior to
    running this.
    """
    assert zet_settings.zet_local_env_path.exists()


def test_settings_retrieval(zet_settings):
    default_settings = zet_settings.get_setting("defaults")
    assert isinstance(default_settings, dict)

    data = zet_settings.get_setting()
    assert data is not None
    assert isinstance(data, dict)


def test_settings_append_dict(zet_settings):
    key = "zet_repos"
    value = {
        "some_name": {
            "folder": "some/path/",
            "template": "default"
        }
    }
    zet_settings.append_setting(key, value)
    new_settings = zet_settings.refresh().get_setting("zet_repos")
    assert value["some_name"] == new_settings["some_name"]


def test_settings_update_key_refresh(zet_settings):
    """
    Ensures that we can refresh the object
    state from the JSON file if it is changed
    during the program's call stack.

    We test both the refresh and settings update
    function in one go, because we're calling refresh
    inside the update.
    """

    keys = ["defaults", "editor", "name"]
    value = "vscode"
    zet_settings.update_setting(keys, value)
    assert value == zet_settings.get_setting("defaults")["editor"]["name"]

    check_settings = zet_settings.refresh().get_setting("defaults")
    assert value == check_settings["editor"]["name"]

