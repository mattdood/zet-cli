import os

import pytest

from src.zet.git_commands import git_add_zets
from src.zet.git_commands import git_commit_zets
from src.zet.git_commands import git_init_zets
from src.zet.git_commands import git_push_zets
from src.zet.settings import Settings, ZET_LOCAL_ENV_PATH


def test_git_init_initializes(zet_settings):
    settings = Settings(ZET_LOCAL_ENV_PATH).get_setting("zet_repos")
    assert os.path.exists(settings[zet_settings]["folder"])
    git_init = git_init_zets(zet_settings)
    assert "Initialized empty Git repository" in str(git_init)


def test_git_add_adds_changes(zet_settings, zet_git_repo):
    git_add = git_add_zets(zet_settings)
    assert "" in str(git_add)


def test_git_commit_zets(zet_git_repo_changes):
    git_commit = git_commit_zets("some message", "zets")
    assert "some message" in str(git_commit)
    assert "files changed" in str(git_commit) or "file changed" in str(git_commit)


@pytest.mark.skip(reason="No way of testing, fails on git_push, pre-assertion")
def test_git_push_zets(zet_repo_changes):
    git_push = git_push_zets("test_repo", zet_repo_changes)
    assert "non-zero exit code" in str(git_push)
    assert "No configured push destination." in str(git_push)

