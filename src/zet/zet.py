import ast
import datetime
import fileinput
import os
import shutil
import time
from typing import Dict, List

from .settings import Settings

settings = Settings()


class ZetDoesNotExistException(Exception):
    """Zet does not exist."""
    pass


class Zet:
    """A Zettlekasten file.

    The representation of a physical zet
    on-disk. If one does not exist it will
    be created after a `create()` call
    and passed back to the caller.
    """

    def __init__(self, path: str = None) -> None:
        self.path = path

    @property
    def metadata(self) -> Dict:
        """Get file metadata.

        Generates a dictionary of the
        metadata available on each of the
        zets, this assumes that a path
        is available on generation.

        Does not support multi-line metadata.

        This requires a consistent delimeter
        be used to enclose a chunk of metadata
        and that each be in a key-value form.

        Example file:
            * The delimeters below are `+++`
            * Lists are allowed
            * All key-values have colon and space
                `: ` between them

            -------------------------------
            |+++                          |
            |something: 'some-value-here' |
            |list: ['some','values',]     |
            |+++                          |
            |                             |
            |                             |
            |                             |
            |                             |
            -------------------------------

        Returns:
            metadata (Dict): A dictionary of the available
                metadata in the file.

        Raises:
            ZetDoesNotExistException
        """
        if self.path is not None and os.path.exists(self.path):
            metadata = {}

            # read a file line by line until we
            # hit our second delimeter
            # this assumes we have a consistent delimeter
            with open(self.path, "r") as file:
                delimeter = file.readline()
                for line in file.readlines()[0:]:
                    if line.startswith(delimeter):
                        break
                    else:

                        # split the line to a named key
                        # and a value (value contains newline "\n")
                        name, value = line.partition(": ")[::2]

                        # check if the value is a list or not
                        # example representation:
                        # path: 'some/path/to/file.md'
                        if "[" not in value:
                            metadata[name.strip()] = value.rstrip().split("\'")[1]

                        # value is a list
                        # example representation:
                        # tags: ['some', 'tag', 'here',]
                        else:
                            value_list = ast.literal_eval(value.rstrip())
                            metadata[name.strip()] = value_list
            return metadata
        else:
            raise ZetDoesNotExistException("Zet does not exist")

    def create(self,
               title: str,
               category: str,
               tags: str,
               zet_repo: str = None,
               template: str = None) -> None:
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

        if zet_repo:
            repo = settings.get_repo_path(zet_repo)
        else:
            zet_repo = settings.get_default_repo()
            repo = settings.get_default_repo_path()

        full_path = os.path.join(
            repo, today_year, today_month, today_str
        )
        clean_title = title.lower().replace(' ', '-')
        full_title = str(clean_title) + "-" + today_str + ".md"
        filename = os.path.join(full_path, full_title)
        tags_list = tags.split(', ')
        zet_template_path = "/" + os.path.join(today_year, today_month, clean_title + "-" + today_str)

        metadata = [
            ["templatePath", zet_template_path],
            ["templateDate", today_str],
            ["templateTitle", str(title)],
            ["templateCleanTitle", str(clean_title)],
            ["templateCategory", str(category)],
            ["templateTags", str(tags_list)]
        ]

        if not os.path.exists(full_path):
            os.makedirs(full_path)

            if template is None:
                # if the settings haven't been made then the
                # data will not be refreshed
                settings.refresh()
                template = settings.get_default_template_path()
            else:
                template = settings.get_template_path(template)

            new_file = shutil.copyfile(template, filename)

            for line in fileinput.input(new_file, inplace=True):
                for item in metadata:
                    line = line.replace(item[0], item[1])

                # line = re.sub(r"/{({word_match}*)}/".format(word_match=item[0]), item[1], line)
            fileinput.close()
        self.path = filename


def bulk_import_zets(files_folder: str,
                     zet_repo: str = None) -> List:
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

    if zet_repo:
        repo = settings.get_repo_path(zet_repo)
    else:
        repo = settings.get_default_repo_path()

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

