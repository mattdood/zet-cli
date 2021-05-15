import datetime
import fileinput
import os
import shutil
from typing import Dict

from src.zet.settings import ZET_DEFAULT_TEMPLATE, ZET_FOLDERS


def create_zet(
    title: str,
    zet_repo: str = ZET_FOLDERS["zets"],
    folder: Dict[str, str] = ZET_FOLDERS,
    template: str = ZET_DEFAULT_TEMPLATE,
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
    today_str = str(today.strftime("%Y%m%d%H%M%S"))

    full_path = os.path.join(
        folder[zet_repo], str(today.year), str(today.month), today_str
    )
    filename = os.path.join(full_path, title)

    metadata = [["templateDate", today_str], ["templateTitle", title]]

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
