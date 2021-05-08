import datetime
import os
import shutil

from .settings import ZET_DEFAULT, ZET_TEMPLATE


def create_zet(
    title: str, folder: str = ZET_DEFAULT, template: str = ZET_TEMPLATE
) -> str:
    """Creates a new zet.

    Takes in the zet folder and returns
    a path to the new zet. This will
    be time sensitive.

    Params:
        title (str): Title of the zet,
            does not replace filename.
        folder (str): String with the
            parent folder path.
        template (str): Template path
            for the file.

    Returns:
        zet_path (str): Full path to the newly
            created zet.
    """
    today = datetime.datetime.now()

    full_path = os.path.join(
        folder, str(today.year), str(today.month), today.strftime("%Y%m%d%H%M%S")
    )
    filename = os.path.join(full_path, "readme.md")

    if not os.path.exists(full_path):
        os.makedirs(full_path)
        shutil.copyfile(template, filename)

    return filename
