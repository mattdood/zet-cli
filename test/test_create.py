import os
import time

import pytest

from src.zet.create import bulk_import_zets, create_zet


def test_zet_exists(zet_test_repo, zet_folders):
    zet = create_zet(
        "some title",
        "some category",
        "some, tags",
        zet_test_repo,
        zet_folders
    )
    assert os.path.exists(zet)


def test_unique_zets(zet_test_repo, zet_folders):

    zet_one = create_zet(
        "some title",
        "some category",
        "some, tags",
        zet_test_repo,
        zet_folders
    )
    time.sleep(1)
    zet_two = create_zet(
        "some title",
        "some category",
        "some, tags",
        zet_test_repo,
        zet_folders
    )
    assert zet_one != zet_two
    assert os.path.exists(zet_one)
    assert os.path.exists(zet_two)


def test_zet_metadata(zet_test_repo, zet_folders):
    zet = create_zet(
        "some title",
        "some category",
        "some, tags",
        zet_test_repo,
        zet_folders
    )
    zet_file = open(zet)
    text = ""
    for line in zet_file:
        text += line
    assert os.path.exists(zet)
    assert "templateDate" not in text
    assert "templateTitle" not in text
    assert "templateCategory" not in text
    assert "templateCleanTitle" not in text
    assert "templateTags" not in text


def test_bulk_create_zets(tmp_path, zet_test_repo, zet_folders):

    for i in range(5):
        folder_name = "some_folder_" + str(i)
        file_name = "test_readme_" + str(i) + ".md"
        d = tmp_path / folder_name
        d.mkdir()
        p = d / file_name
        p.write_text("some test text")

    zet_list = bulk_import_zets(tmp_path, zet_test_repo, zet_folders)

    for zet in zet_list:
        assert os.path.exists(zet["existing_path"])
        assert os.path.exists(zet["zet_file_path"])
        print(zet["zet_file_path"])
        zet_file = open(zet["zet_file_path"])
        text = ""
        for line in zet_file:
            text += line
        assert "some test text" in text
