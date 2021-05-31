import json
import os

from src.zet.env_setup import add_repo, create_env


def test_env_creates(tmp_path):
    tmp_env_path = os.path.join(str(tmp_path), ".local.json")
    create_env(tmp_env_path)
    assert os.path.exists(tmp_env_path)


def test_add_repo(zet_tmp_env, tmp_path):
    zet_repo = "some_repo"
    zet_path = os.path.join(tmp_path, zet_repo)
    add_repo(zet_repo, str(tmp_path), zet_tmp_env)
    assert os.path.exists(zet_path)

    with open(zet_tmp_env, "r") as file:
        zet_env = json.load(file)["zet_repos"]
        assert {zet_repo: zet_path} == zet_env
