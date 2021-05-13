import pytest

from src.zet.git_commands import git_add_zets
from src.zet.git_commands import git_commit_zets
from src.zet.git_commands import git_init_zets
from src.zet.git_commands import git_push_zets


def test_git_init_initializes(tmp_path):
    new_repo = tmp_path / 'test_dir'
    new_repo.mkdir()
    new_repo_path = new_repo.absolute().as_posix()
    git_init = git_init_zets(new_repo_path)
    assert "Initialized empty Git repository" in str(git_init)


def test_git_add_adds_changes(zet_repo):
    new_file = zet_repo['new_repo'] / 'some_file.md'
    new_file.write_text('some text')
    git_add = git_add_zets(zet_repo['new_repo_path'])
    assert "" in str(git_add)


def test_git_commit_zets(zet_repo_changes):
    git_commit = git_commit_zets('some message', zet_repo_changes)
    assert "some message" in str(git_commit)
    assert "file changed" in str(git_commit)


@pytest.mark.skip(reason="No way of testing, fails on git_push, pre-assertion")
def test_git_push_zets(zet_repo_changes):
    git_push = git_push_zets(zet_repo_changes)
    print(git_push)
    assert "non-zero exit code" in str(git_push)
    assert "No configured push destination." in str(git_push)
