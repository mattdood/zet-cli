import json
import os

from src.zet.repo import Repo
from src.zet.settings import ZET_INSTALL_PATH


def test_zets_exist_path(zet_settings, zet_list_paths):
    assert all(os.path.exists(sample_zet) for sample_zet in zet_list_paths)
    assert all(os.path.isfile(sample_zet) for sample_zet in zet_list_paths)


def test_zets_name(zet_settings, zet_list):
    assert all("/" not in sample_zet for sample_zet in zet_list)
    assert all("\\" not in sample_zet for sample_zet in zet_list)


def test_add_repo(zet_settings):
    """Tests both default and non-default repos.

    Default:
        Repos are placed in the "~/zets/" home
        directory defined in settings.
    Non-Default:
        Repos are placed in a user-defined directory
        outside of the predefined area.
    """
    zet_repo = "test_repo"
    zet_path = ZET_INSTALL_PATH / zet_repo
    zet_other = "other/"
    zet_other_repo = "some_other_repo"
    zet_other_path = os.path.join(zet_other, zet_other_repo)

    repos = Repo()
    repos.add_repo(zet_repo)
    repos.add_repo(zet_other_repo, zet_other)
    assert os.path.exists(zet_path)
    assert os.path.exists(zet_other_path)

    zet_repo_setting = {
        zet_repo: {
            "folder": zet_path.as_posix(),
            "template": "default"
        }
    }
    zet_other_repo_setting = {
        zet_other_repo: {
            "folder": zet_other_path,
            "template": "default"
        }
    }

    zet_settings = zet_settings.refresh()

    with zet_settings.zet_local_env_path.open("r") as file:
        zet_env = json.load(file)["zet_repos"]
        assert zet_repo_setting[zet_repo] == zet_env[zet_repo]
        assert zet_other_repo_setting[zet_other_repo] == zet_env[zet_other_repo]

