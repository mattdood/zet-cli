import os
from typing import List

from .settings import Settings, ZET_LOCAL_ENV_PATH

settings = Settings(ZET_LOCAL_ENV_PATH)


def list_zets(
    zet_repo: str = None,
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

    if zet_repo:
        repos = [settings.get_repo_path(zet_repo)]
    else:
        # all repos
        repos = settings.get_repos()

    zet_list = []
    for repo in repos:
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
