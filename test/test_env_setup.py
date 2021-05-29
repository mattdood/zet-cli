import json
import os

from src.zet.env_setup import add_repo, create_env
from src.zet.settings import ZET_ENV_PATH


def test_env_creates():
    create_env()
    assert os.path.exists(ZET_ENV_PATH)

    with open(ZET_ENV_PATH, "r") as file:
        zet_env = json.load(file)["zet_repos"]
        assert {} == zet_env


def test_add_repo(tmp_path, zet_env_file):
    zet_repo = "some_repo"
    zet_path = os.path.join(str(tmp_path), zet_repo)
    add_repo(zet_repo, zet_path)
    assert os.path.exists(zet_path)

    with open(ZET_ENV_PATH, "r") as file:
        zet_env = json.load(file)["zet_repos"]
        print(zet_env)
        assert {"some_repo": zet_path} == zet_env
