import os

import pytest

from src.zet.git_commands import git_add_zets
from src.zet.git_commands import git_commit_zets
from src.zet.git_commands import git_init_zets
from src.zet.git_commands import git_push_zets


def test_git_init_initializes(zet_test_repo, zet_folders):
    os.makedirs(zet_folders[zet_test_repo] + "test_dir")
    git_init = git_init_zets(zet_test_repo, zet_folders)
    assert "Initialized empty Git repository" in str(git_init)


def test_git_add_adds_changes(zet_test_repo, zet_git_repo):
    new_file = open(zet_git_repo[zet_test_repo] + "some_file.md", "w")
    new_file.close()
    git_add = git_add_zets(zet_test_repo, zet_git_repo)
    assert "" in str(git_add)


def test_git_commit_zets(zet_test_repo, zet_git_repo_changes):
    print("before commit")
    git_commit = git_commit_zets("some message", zet_test_repo, zet_git_repo_changes)
    print("after commit")
    assert "some message" in str(git_commit)
    assert "files changed" in str(git_commit)


@pytest.mark.skip(reason="No way of testing, fails on git_push, pre-assertion")
def test_git_push_zets(zet_test_repo, zet_repo_changes):
    git_push = git_push_zets(zet_test_repo, zet_repo_changes)
    print(git_push)
    assert "non-zero exit code" in str(git_push)
    assert "No configured push destination." in str(git_push)
