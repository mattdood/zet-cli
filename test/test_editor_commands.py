import os

import keyboard
import pytest

from src.zet.editor_commands import open_editor


@pytest.mark.skip(reason="No way of testing, gets stuck in a session, pre-assertion")
def test_editor_opens_zet(zet):
    editor_session = open_editor(zet)

    keyboard.press_and_release("colon, q, enter")

    assert os.getcwd() == str(zet)
    assert "No such file or directory" not in str(editor_session)
