import os
from typing import List

from .settings import Settings

settings = Settings()


class RepoDoesNotExistException(Exception):
    """Repository path does not exist."""
    pass


class Repo:
    """Representation of a notes repository.

    Each repo has zets organized in a datewise fashion.
    This represents all known repositories from settings,
    with an interface to interact with them.

    Note: Repos are not deleted through this interface.
    That is left up to the user.
    """

    def __init__(self) -> None:
        self.repos = settings.get_repos()

    def add_repo(self,
                 zet_repo: str,
                 zet_path: str = None,
                 template: str = None) -> None:
        """Adds a new repo (folder) and appends to the env file.

        Params:
            zet_repo (str): A zet repo name to
                append to an existing env file.
                The folder is created.
            zet_path (str|None): The path to a new
                zet repo. This is the parent folder, defaults
                to the installation location.
            template (str|None): A default template to
                use for the new repository.

        Returns:
            None
        """

        # zet folder naming setup
        # and creation
        clean_zet_repo = zet_repo.replace(' ', '_')
        zet_repo_path = os.path.join(
            zet_path if zet_path else settings.install_path,
            clean_zet_repo
        )
        if not os.path.exists(zet_repo_path):
            os.makedirs(zet_repo_path)

        # settings repo update with new
        # folder that was just created
        new_repo = {
            clean_zet_repo: {
                "folder": zet_repo_path,
                "template": template if template else settings.get_default_template()
            }
        }
        settings.append_setting("zet_repos", new_repo)

    def list_zets(self, zet_repo: str = None, full_path: bool = False) -> List[str]:
        """Lists zets.

        This will be a catch-all for listing
        zets based on different argument structures.

        Params:
            folder (str): Folder to search.
            full_path (bool): Determines if full file paths will
                be provided. Defaults to False.

        Returns:
            zets (List[str]): List of zets.

        Raises:
            RepoDoesNotExistException
        """

        if zet_repo:
            repos = [settings.get_repo_path(zet_repo)]
        else:
            # all repos
            repos = [repo["folder"] for repo in settings.get_repos()]

        zet_list = []
        for repo in repos:

            if not os.path.exists(repo):
                raise RepoDoesNotExistException("Repo does not exist.")

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

