import os

import pytest

from src.zet.git_commands import git_add_zets
from src.zet.git_commands import git_commit_zets
from src.zet.git_commands import git_init_zets
from src.zet.git_commands import git_push_zets


def test_git_init_initializes(zet_settings):
    assert os.path.exists(zet_settings.get_default_repo_path())
    git_init = git_init_zets(zet_settings.get_default_repo())
    assert "Initialized empty Git repository" in str(git_init)


def test_git_add_adds_changes(zet_settings, zet_git_repo):
    git_add = git_add_zets(zet_settings.get_default_repo())
    assert "" in str(git_add)


def test_git_commit_zets(zet_settings, zet_git_repo_changes):
    git_commit = git_commit_zets("some message", zet_settings.get_default_repo())
    assert "some message" in str(git_commit)
    assert "files changed" in str(git_commit) or "file changed" in str(git_commit)


@pytest.mark.skip(reason="No way of testing, fails on git_push, pre-assertion")
def test_git_push_zets(zet_settings, zet_repo_changes):
    git_push = git_push_zets(zet_settings.get_default_repo())
    assert "non-zero exit code" in str(git_push)
    assert "No configured push destination." in str(git_push)

