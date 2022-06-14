import os
import subprocess

import pytest

from src.zet.main import main


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_entrypoint():
    exit_status = os.system("zet --help")
    assert exit_status == 0


@pytest.mark.skip(reason="GitHub runners don't have neovim.")
def test_create(zet_settings):

    main(['create', '-t', 'cli test', '-c', 'test', '-tag', 'test1, test2'])

    files_found = []
    for root, dirs, files in os.walk("~/zets/zets/"):
        for file in files:
            files_found.append(file)

    assert 'cli-test' in [file[:len("cli-test")] for file in files_found]

