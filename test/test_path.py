import pytest

from zet.settings import ZET_HOME, ZET_INSTALL_PATH


def test_path(zet_settings):
    """Tests install path is correct"""
    assert ZET_INSTALL_PATH == ZET_HOME / "zet/"

