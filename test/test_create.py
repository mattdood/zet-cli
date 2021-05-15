import os
import time

import pytest

from src.zet.create import create_zet
from src.zet.settings import ZET_DEFAULT_FOLDER, ZET_DEFAULT_TEMPLATE


def test_zet_exists(tmp_path):
    zet = create_zet("some title", tmp_path)
    assert os.path.exists(zet)


@pytest.mark.parametrize(
    "title, folder, repo_name, template",
    [
        ("some title", ZET_DEFAULT_FOLDER, ZET_DEFAULT_TEMPLATE),
        ("some title", "~/some_test/", None),
        ("some title", "~/some_test/", ZET_DEFAULT_TEMPLATE),
    ],
)
def test_zet_arguments(title, folder, template, tmp_path):
    # Pytest does not support passing fixtures as params
    if template is None:
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        template_file = template_dir / "some_template.md"
        template_file.write_text("# Some Alternate Content")
        template = template_file.absolute()

    zet = create_zet(title, folder, template)
    assert os.path.exists(zet)


def test_unique_zets(tmp_path):
    zet_one = create_zet("some title", tmp_path)
    time.sleep(1)
    zet_two = create_zet("some title", tmp_path)
    assert zet_one != zet_two


def test_zet_metadata(tmp_path):
    zet = create_zet("some title", tmp_path)
    zet_file = open(zet)
    text = ""
    for line in zet_file:
        text += line
    assert "templateDate" not in text
    assert "templateTitle" not in text
