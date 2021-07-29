import json
from typing import Dict



# TODO:
# 1. Abstract settings into JSON only
# 2. Have settings interact with the `Settings` class object
# 3. Create a database inside the install
# 4. Create tables based on the repos in the JSON file
#   a. Have DB schema laid out already

class Database:

    def __init__(self):
        pass

    def create_database(self, database):
        """Creates a database inside an install.

        Generates a SQLite file inside a zet
        installation. A single DB is used
        for all repos.
        """
        pass

    def create_table(self, table):
        pass

    def insert_zet(self, zet: Zet):
        pass

    def select(self, selection, qualifier):
        pass

    def is_valid(self, query: str) -> bool:
        pass

class Repo(object):

    def __init__(self, repo_name: str, repo_folder: str):
        self.repo_name = repo_name
        self.repo_folder = repo_folder

    def list_zets(self, query):
        pass

    def open_zet(self, path):
        pass


class Template(object):

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_metadata(self):
        pass


class Zet(object):

    def __init__(self, title: str, category: str, tags: str, repo: Repo):
        self.title = title
        self.category = category
        self.tags = tags




