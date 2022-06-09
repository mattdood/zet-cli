import os
import time

import pytest

from src.zet.zet import Zet, bulk_import_zets


def test_zet_exists(zet_settings):
    new_zet = Zet()
    new_zet.create(
        title="some title",
        category="some category",
        tags="some, tags"
    )
    assert os.path.exists(new_zet.path)


def test_zet_metadata(zet_settings):
    zet = Zet()
    zet.create(
        title="some title",
        category="some category",
        tags="some, tags"
    )
    assert zet.metadata["title"] == "some title"
    assert zet.metadata["category"] == "some category"
    assert zet.metadata["tags"] == ["some", "tags"]


def test_unique_zets(zet_settings):

    zet_one = Zet()
    zet_one.create(
        "some title",
        "some category",
        "some, tags",
    )
    time.sleep(1)

    zet_two = Zet()
    zet_two.create(
        "some title",
        "some category",
        "some, tags",
    )
    assert zet_one != zet_two
    assert os.path.exists(zet_one.path)
    assert os.path.exists(zet_two.path)


def test_zet_metadata(zet_settings):
    zet = Zet()
    zet.create(
        "some title",
        "some category",
        "some, tags",
    )
    assert os.path.exists(zet.path)
    zet_file = open(zet.path)
    text = ""
    for line in zet_file:
        text += line
    assert "templatePath" not in text
    assert "templateDate" not in text
    assert "templateTitle" not in text
    assert "templateCategory" not in text
    assert "templateCleanTitle" not in text
    assert "templateTags" not in text


def test_bulk_create_zets(tmp_path, zet_settings):

    for i in range(5):
        folder_name = "some_folder_" + str(i)
        file_name = "test_readme_" + str(i) + ".md"
        d = tmp_path / folder_name
        d.mkdir()
        p = d / file_name
        p.write_text("some test text")

    zet_list = bulk_import_zets(tmp_path)

    for zet in zet_list:
        assert os.path.exists(zet["existing_path"])
        assert os.path.exists(zet["zet_file_path"])
        zet_file = open(zet["zet_file_path"])
        text = ""
        for line in zet_file:
            text += line
        assert "some test text" in text
