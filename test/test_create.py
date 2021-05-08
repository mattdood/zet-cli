import os
import time

import pytest

from src.zet.create import create_zet
from src.zet.settings import ZET_DEFAULT, ZET_TEMPLATE


def test_zet_exists():
    zet = create_zet()
    assert os.path.exists(zet)


@pytest.mark.parametrize(
    "folder, template",
    [
        (ZET_DEFAULT, ZET_TEMPLATE),
        ("~/some_test/", None),
        ("~/some_test/", ZET_TEMPLATE),
    ],
)
def test_zet_arguments(folder, template, tmp_path):
    # Pytest does not support passing fixtures as params
    if template is None:
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        template_file = template_dir / "some_template.md"
        template_file.write_text("# Some Alternate Content")
        template = template_file.absolute()

    zet = create_zet(folder, template)
    assert os.path.exists(zet)


def test_unique_zets():
    zet_one = create_zet()
    time.sleep(1)
    zet_two = create_zet()
    assert zet_one != zet_two
