import os
import subprocess

import pytest


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


@pytest.mark.skip(reason="Unfinished test, may not be needed.")
def test_zet_helps(zet_main_path):
    command = ["python3", zet_main_path, "--help"]
    out, err, exitcode = capture(command)
    assert exitcode == 0
    assert "help" in str(out)


@pytest.mark.skip(reason="Unfinished test, may not be needed.")
def test_zet_sample_parse(zet_main_path):
    command = ["python3", zet_main_path, "create", "-t test_title"]
    out, err, exitcode = capture(command)
    assert exitcode == 0
    assert "test_title" in str(out)
