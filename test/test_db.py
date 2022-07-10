import os
import time

import pytest

from src.zet.db import Db
from src.zet.zet import Zet


def test_db_creates(zet_settings):
    db = Db()
    assert os.path.exists(db.db_path)


def test_db_sync(zet_settings):
    db = Db()
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

    zet_one.add_link(zet_two.path)

    db.sync_db()
    assert len(db.db.edges) == 1
    assert len(db.db.nodes) == 2

