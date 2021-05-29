import os
import time

import pytest

from src.zet.create import create_zet
from src.zet.settings import ZET_DEFAULT_FOLDER, ZET_DEFAULT_TEMPLATE


def test_zet_exists(zet_test_repo, zet_folders):
    zet = create_zet("some title", zet_test_repo, zet_folders)
    assert os.path.exists(zet)


@pytest.mark.parametrize(
    "title, zet_repo, folder, template",
    [
        ("some title", "zets", ZET_DEFAULT_FOLDER, ZET_DEFAULT_TEMPLATE),
        ("some title", "zets", ZET_DEFAULT_FOLDER, None),
    ],
)
def test_zet_arguments(title, zet_repo, folder, template, tmp_path):
    # Pytest does not support passing fixtures as params
    if template is None:
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        template_file = template_dir / "some_template.md"
        template_file.write_text("# Some Alternate Content")
        template = template_file.absolute()

    zet = create_zet(title, zet_repo, folder, template)
    assert os.path.exists(zet)


def test_unique_zets(zet_test_repo, zet_folders):

    zet_one = create_zet("some title", zet_test_repo, zet_folders)
    time.sleep(1)
    zet_two = create_zet("some title", zet_test_repo, zet_folders)
    assert zet_one != zet_two
    assert os.path.exists(zet_one)
    assert os.path.exists(zet_two)


def test_zet_metadata(zet_test_repo, zet_folders):
    zet = create_zet("some title", zet_test_repo, zet_folders)
    zet_file = open(zet)
    text = ""
    for line in zet_file:
        text += line
    assert os.path.exists(zet)
    assert "templateDate" not in text
    assert "templateTitle" not in text
