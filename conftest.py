import os
import shutil
import subprocess
import time
from typing import Dict, List, Union

import pytest

from src.zet.git_commands import git_add_zets, git_init_zets
from src.zet.repo import Repo
from src.zet.settings import Settings
from src.zet.zet import Zet


@pytest.fixture(scope="module")
def zet_settings(pytestconfig) -> Settings:
    """Test setup and teardown.

    All functions need to import this fixture.
    The settings are created and torn down properly
    for each test that has this as a fixture.
    """
    # Setup
    # creates local settings
    settings = Settings()
    repos = Repo()
    repos.add_repo("zets")
    yield settings.refresh()  # default repo name returned for subsequent invocations

    # Teardown
    scratch_repo_one = "other/"

    workspace = pytestconfig.rootdir / "~"
    if workspace.exists():
        shutil.rmtree(workspace)

    if settings.install_path.exists():
        shutil.rmtree(settings.install_path)

    if os.path.exists(scratch_repo_one):
        shutil.rmtree(scratch_repo_one)


@pytest.fixture
def zet(zet_settings: Settings) -> str:
    sample_zet = Zet()
    sample_zet.create(
        title="some title",
        category="some category",
        tags="some, tags",
        zet_repo=zet_settings.get_default_repo(),
    )
    return sample_zet.path


@pytest.fixture
def zet_list(zet_settings: Settings) -> List[str]:

    for i in range(5):
        time.sleep(1)
        Zet().create(
            "some title",
            "some category",
            "some, tags",
            zet_settings.get_default_repo()
        )
    repos = Repo()
    sample_zets = repos.list_zets(zet_settings.get_default_repo())

    return sample_zets


@pytest.fixture
def zet_list_paths(zet_settings: Settings) -> List[str]:

    for i in range(5):
        time.sleep(1)
        Zet().create(
            "some title",
            "some category",
            "some, tags",
            zet_settings.get_default_repo()
        )
    repos = Repo()
    sample_zets = repos.list_zets(zet_settings.get_default_repo(), True)

    return sample_zets


@pytest.fixture
def zet_git_repo(zet_settings: Settings) -> Union[None, Dict]:
    try:
        git_init_zets(zet_settings.get_default_repo())
    except subprocess.CalledProcessError as error:
        error_dict = {"response_code": error.returncode, "output": error.output}
        return error_dict


@pytest.fixture
def zet_git_repo_changes(zet_settings: Settings, zet_git_repo) -> str:
    repo_path = zet_settings.get_default_repo_path()
    new_file_path = os.path.join(repo_path, "some_file.md")
    new_file = open(new_file_path, "w")
    new_file.writelines(["some text", "some other text"])
    new_file.close()
    git_add_zets(zet_settings.get_default_repo())

