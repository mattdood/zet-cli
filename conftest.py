import os
import shutil
import subprocess
import time
from typing import Dict, List, Union

import pytest

from src.zet.create import Zet
from src.zet.git_commands import git_add_zets, git_commit_zets, git_init_zets
from src.zet.list import list_zets
from src.zet.repo import add_repo
from src.zet.settings import ZET_LOCAL_ENV_PATH, Settings

settings = Settings(ZET_LOCAL_ENV_PATH)


@pytest.fixture()
def zet_settings() -> str:
    Settings(ZET_LOCAL_ENV_PATH)
    add_repo("zets")
    return "zets"  # default repo name returned for subsequent


@pytest.fixture
def zet(zet_settings: str) -> str:
    sample_zet = Zet().create(
        title="some title",
        category="some category",
        tags="some, tags",
        zet_repo=zet_settings,
    )
    return sample_zet.path


@pytest.fixture
def zet_list(zet_settings: str) -> List[str]:

    for i in range(5):
        time.sleep(1)
        Zet().create(
            "some title",
            "some category",
            "some, tags",
            zet_settings
        )
    sample_zets = list_zets(zet_settings)

    return sample_zets


@pytest.fixture
def zet_list_paths(zet_settings: str) -> List[str]:

    for i in range(5):
        time.sleep(1)
        Zet().create(
            "some title",
            "some category",
            "some, tags",
            zet_settings
        )
    sample_zets = list_zets(zet_settings, True)

    return sample_zets


@pytest.fixture
def zet_git_repo(zet_settings: str) -> Union[None, Dict]:
    try:
        git_init_zets(zet_settings)
    except subprocess.CalledProcessError as error:
        error_dict = {"response_code": error.returncode, "output": error.output}
        return error_dict


@pytest.fixture
def zet_git_repo_changes(zet_settings: str, zet_git_repo) -> str:
    repo_path = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")[zet_settings]
    new_file_path = os.path.join(repo_path["folder"], "some_file.md")
    new_file = open(new_file_path, "w")
    new_file.writelines(["some text", "some other text"])
    new_file.close()
    git_add_zets(zet_settings)


@pytest.fixture(autouse=True)
def cleanup_run():
    """Removes workspaces on teardown."""
    yield
    default_workspace = "zets/"
    other_workspace = "other/"
    if os.path.exists(default_workspace):
        shutil.rmtree(default_workspace)
    if os.path.exists(other_workspace):
        shutil.rmtree(other_workspace)

