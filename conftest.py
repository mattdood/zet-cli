import os
import random
import subprocess
import time
from pathlib import Path
from typing import Dict, List

import pytest

from src.zet.create import create_zet
from src.zet.git_commands import git_add_zets, git_commit_zets, git_init_zets
from src.zet.list import list_zets
from src.zet.settings import (
    ZET_DEFAULT_FOLDER,
    ZET_DEFAULT_TEMPLATE,
    ZET_FOLDERS,
    ZET_PROJECT,
)


@pytest.fixture
def zet(
    folder: Dict[str, str] = ZET_FOLDERS, template: str = ZET_DEFAULT_TEMPLATE
) -> str:
    sample_zet = create_zet("some title", folder["zet"], template)
    return sample_zet


@pytest.fixture
def zet_default_repo(folder: Dict[str, str] = ZET_DEFAULT_FOLDER):
    return list(folder.keys())[0]


@pytest.fixture
def zet_folders(
    tmp_path,
    folder: Dict[str, str] = ZET_FOLDERS,
) -> Dict[str, str]:
    d = tmp_path / "some_folder"
    d.mkdir()
    folder["some_folder"] = str(d)
    return folder


@pytest.fixture
def zet_test_repo(zet_folders) -> str:
    return list(zet_folders.keys())[1]


@pytest.fixture
def zet_random_repo_name(zet_folders) -> str:
    random_index = random.randint(0, len(zet_folders) - 1)
    return list(zet_folders.keys())[random_index]


@pytest.fixture
def zet_list(
    zet_test_repo,
    zet_folders,
    zet_count: int = 5,
    template: str = ZET_DEFAULT_TEMPLATE,
) -> List[str]:

    for i in range(zet_count):
        time.sleep(1)
        create_zet("some title", zet_test_repo, zet_folders, template)
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
        create_zet("some title", zet_test_repo, zet_folders, template)
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
    git_add_zets(zet_test_repo, zet_git_repo)
    return zet_git_repo


@pytest.fixture
def zet_repo_commit(zet_test_repo, zet_git_repo_changes) -> str:
    git_commit_zets("some message", zet_test_repo, zet_git_repo_changes)
    return zet_git_repo_changes


@pytest.fixture
def zet_main_path(project_path: Path = ZET_PROJECT):
    return os.path.join(project_path, "main.py")
