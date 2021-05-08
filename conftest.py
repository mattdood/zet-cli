import subprocess
import time
from typing import Dict, List

import pytest

from src.zet.create import create_zet
from src.zet.git_commands import git_add_zets, git_commit_zets, git_init_zets
from src.zet.list import list_zets
from src.zet.settings import ZET_DEFAULT, ZET_TEMPLATE


@pytest.fixture
def zet(folder: str = ZET_DEFAULT, template: str = ZET_TEMPLATE) -> str:
    sample_zet = create_zet("some title", folder, template)
    return sample_zet


@pytest.fixture
def zet_list(
    zet_count: int = 5, folder: str = ZET_DEFAULT, template: str = ZET_TEMPLATE
) -> List[str]:

    for i in range(zet_count):
        time.sleep(1)
        create_zet("some title", folder, template)
    sample_zets = list_zets(folder)

    return sample_zets


@pytest.fixture
def zet_list_paths(
    zet_count: int = 5,
    full_path: bool = True,
    folder: str = ZET_DEFAULT,
    template: str = ZET_TEMPLATE,
) -> List[str]:

    for i in range(zet_count):
        time.sleep(1)
        create_zet("some title", folder, template)
    sample_zets = list_zets(folder, full_path)

    return sample_zets


@pytest.fixture
def zet_folder(folder: str = ZET_DEFAULT) -> str:
    return folder


@pytest.fixture
def zet_repo(tmp_path) -> Dict:
    new_repo = tmp_path / "test_dir"
    new_repo.mkdir()
    new_repo_path = new_repo.absolute().as_posix()
    try:
        git_init_zets(new_repo_path)
    except subprocess.CalledProcessError as error:
        error_dict = {"response_code": error.returncode, "output": error.output}
        return error_dict

    repo = {"new_repo": new_repo, "new_repo_path": new_repo_path}
    return repo


@pytest.fixture
def zet_repo_changes(zet_repo) -> str:
    new_file = zet_repo["new_repo"] / "some_file.md"
    new_file.write_text("some text")
    git_add_zets(zet_repo["new_repo_path"])
    return zet_repo["new_repo_path"]


@pytest.fixture
def zet_repo_commit(zet_repo_changes) -> str:
    git_commit_zets("some message", zet_repo_changes)
    return zet_repo_changes
