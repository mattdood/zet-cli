import datetime
import fileinput
import os

import shutil
import time
from typing import List

from .settings import (
    ZET_DEFAULT_REPO,
    ZET_DEFAULT_TEMPLATE,
    ZET_REPOS
)


def create_zet(
    title: str,
    category: str,
    tags: str,
    zet_repo: str = ZET_DEFAULT_REPO,
    template: str = ZET_DEFAULT_TEMPLATE,
) -> str:
    """Creates a new zet.

    Takes in the zet folder and returns
    a path to the new zet. This will
    be time sensitive.

    Params:
        title (str): Title of the zet,
            does not replace filename.
        zet_repo (str): A zet repo name.
        template (str): Template path
            for the file.

    Returns:
        zet_path (str): Full path to the newly
            created zet.
    """
    today = datetime.datetime.now()
    today_year = str(today.year)
    today_month = str(today.month)
    today_str = str(today.strftime("%Y%m%d%H%M%S"))

    repo = ZET_REPOS[zet_repo]["folder"]

    full_path = os.path.join(
        repo, today_year, today_month, today_str
    )
    clean_title = title.lower().replace(' ', '-')
    full_title = str(clean_title) + "-" + today_str + ".md"
    filename = os.path.join(full_path, full_title)
    tags_list = tags.split(', ')
    template_path = "/" + os.path.join(today_year, today_month, clean_title + "-" + today_str)

    metadata = [
        ["templatePath", template_path],
        ["templateDate", today_str],
        ["templateTitle", str(title)],
        ["templateCleanTitle", str(clean_title)],
        ["templateCategory", str(category)],
        ["templateTags", str(tags_list)]
    ]

    if not os.path.exists(full_path):
        os.makedirs(full_path)
        new_file = shutil.copyfile(template, filename)

        for line in fileinput.input(new_file, inplace=True):
            for item in metadata:
                line = line.replace(item[0], item[1])
            print(line, end="")

            # line = re.sub(r"/{({word_match}*)}/".format(word_match=item[0]), item[1], line)
        fileinput.close()

    return filename


def bulk_import_zets(
    files_folder: str,
    zet_repo: str = ZET_DEFAULT_REPO,
) -> List:
    """Bulk create zets from a folder.

    Takes in the folder of existing files
    to import to a zet repo.

    Params:
        files_folder (str): A folder with
            pre-existing files ready to import.
        zet_repo (str): A zet repo name.

    Returns:
        zet_list (List): A list of dict objects
            for each of the file names, original
            paths, zet file paths, and newly folder paths.
    """

    zet_list = []
    repo = ZET_REPOS[zet_repo]["folder"]
    for root, dirs, files in os.walk(files_folder):
        for file in files:
            today = datetime.datetime.now()
            today_year = str(today.year)
            today_month = str(today.month)
            today_str = str(today.strftime("%Y%m%d%H%M%S"))
            full_path = os.path.join(
                repo, today_year, today_month, today_str
            )

            clean_title = file.lower().replace(' ', '-')
            full_title = str(clean_title) + "-" + today_str + ".md"
            filename = os.path.join(full_path, full_title)

            existing_file_path = os.path.join(root, file)

            if not os.path.exists(full_path):
                os.makedirs(full_path)
                shutil.copyfile(existing_file_path, filename)
            time.sleep(1)

    return zet_list
