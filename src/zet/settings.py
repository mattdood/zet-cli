import os

ZET_PROJECT = os.path.dirname(os.path.abspath(__file__))

# Default directory for sets
ZET_DEFAULT_FOLDER = "~/zets/"
ZET_DEFAULT_EDITOR = {"editor": "vim", "command": "vim"}
ZET_DEFAULT_TEMPLATE = os.path.join(ZET_PROJECT, "templates/readme.md")
