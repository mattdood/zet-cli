import time
from typing import List

import pytest

from src.zet.create import create_zet
from src.zet.list import list_zets
from src.zet.settings import ZET_DEFAULT, ZET_TEMPLATE


@pytest.fixture
def zet(folder: str = ZET_DEFAULT, template: str = ZET_TEMPLATE) -> str:
    sample_zet = create_zet(folder, template)
    return sample_zet


@pytest.fixture
def zet_list(
    zet_count: int = 5, folder: str = ZET_DEFAULT, template: str = ZET_TEMPLATE
) -> List[str]:

    for i in range(zet_count):
        time.sleep(1)
        create_zet(folder, template)
    sample_zets = list_zets(folder)

    return sample_zets


@pytest.fixture
def zet_list_paths(
    zet_count: int = 5,
    full_path: bool = True,
    folder: str = ZET_DEFAULT,
    template: str = ZET_TEMPLATE,
) -> List[str]:

    for i in range(zet_count):
        time.sleep(1)
        create_zet(folder, template)
    sample_zets = list_zets(folder, full_path)

    return sample_zets


@pytest.fixture
def zet_folder(folder: str = ZET_DEFAULT) -> str:
    return folder
