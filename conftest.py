import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List

import pytest

from src.zet.create import create_zet
from src.zet.git_commands import git_add_zets, git_commit_zets, git_init_zets
from src.zet.list import list_zets
from src.zet.settings import (
    Settings,
    ZET_LOCAL_ENV_PATH
)
from zet.env_setup import add_repo, generate_env


@pytest.fixture()
def zet_settings():
    generate_env()


@pytest.fixture
def zet_test_repo(zet_folders) -> str:
    return list(zet_folders.keys())[-1]


@pytest.fixture
def zet(
    zet_test_repo,
    zet_folders,
    template: str = ZET_DEFAULT_TEMPLATE
) -> str:
    sample_zet = create_zet(
        "some title",
        "some category",
        "some, tags",
        zet_test_repo,
        zet_folders,
        template
    )
    return sample_zet


@pytest.fixture
def zet_list(
    zet_test_repo,
    zet_folders,
    zet_count: int = 5,
    template: str = ZET_DEFAULT_TEMPLATE,
) -> List[str]:

    for i in range(zet_count):
        time.sleep(1)
        create_zet(
            "some title",
            "some category",
            "some, tags",
            zet_test_repo,
            zet_folders,
            template
        )
    sample_zets = list_zets(zet_test_repo, zet_folders)

    return sample_zets


@pytest.fixture
def zet_list_paths(
    zet_test_repo,
    zet_folders,
    zet_count: int = 5,
    full_path: bool = True,
    template: str = ZET_DEFAULT_TEMPLATE,
) -> List[str]:

    for i in range(zet_count):
        time.sleep(1)
        create_zet(
            "some title",
            "some category",
            "some, tags",
            zet_test_repo,
            zet_folders,
            template
        )
    sample_zets = list_zets(zet_test_repo, zet_folders, full_path)

    return sample_zets


@pytest.fixture
def zet_git_repo(zet_test_repo, zet_folders) -> Dict[str, str]:
    try:
        git_init_zets(zet_test_repo, zet_folders)
    except subprocess.CalledProcessError as error:
        error_dict = {"response_code": error.returncode, "output": error.output}
        return error_dict
    return zet_folders


@pytest.fixture
def zet_git_repo_changes(zet_test_repo, zet_git_repo) -> str:
    new_file_path = os.path.join(zet_git_repo[zet_test_repo], "some_file.md")
    new_file = open(new_file_path, "w")
    new_file.writelines(["some text", "some other text"])
    new_file.close()
    git_add_zets(zet_test_repo)


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

