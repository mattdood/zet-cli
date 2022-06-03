import os

from .settings import ZET_INSTALL_PATH, ZET_LOCAL_ENV_PATH, Settings

settings = Settings(ZET_LOCAL_ENV_PATH)


def add_repo(zet_repo: str,
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
        zet_path if zet_path else ZET_INSTALL_PATH,
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

