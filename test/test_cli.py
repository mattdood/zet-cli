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

