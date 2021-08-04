import os
from typing import Dict, List

from .settings import ZET_DEFAULT_REPO, ZET_REPOS


def list_zets(
    zet_repo: str = ZET_DEFAULT_REPO,
    full_path: bool = False,
) -> List[str]:
    """Lists zets.

    This will be a catch-all for listing
    zets based on different argument structures.

    Params:
        folder (str): Folder to search.
        full_path (bool): Determines if full file paths will
            be provided. Defaults to False.

    Returns:
        zets (List[str]): List of zets.
    """

    repo = ZET_REPOS[zet_repo]["folder"]

    zet_list = []
    if full_path:
        for root, dirs, files in os.walk(repo):
            for file in files:
                full_file_path = os.path.join(root, file)
                zet_list.append(full_file_path)
    else:
        for root, dirs, files in os.walk(repo):
            for file in files:
                zet_list.append(file)

    return zet_list
