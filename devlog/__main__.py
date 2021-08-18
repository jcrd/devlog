# This project is licensed under the MIT License.

# pylint: disable=missing-module-docstring,missing-function-docstring

import argparse
import sys

from devlog.editor import Editor
from devlog.git import GitRepo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=".", help="Path to dev directory")
    parser.add_argument("-e", "--editor", help="Editor to use")

    args = parser.parse_args()

    try:
        editor = Editor(args.editor)
    except FileNotFoundError as error:
        sys.stderr.write("Command not found: {}".format(error.args[0]))
        sys.exit(2)

    repo = GitRepo(args.directory)
    repo.edit_today(editor)


if __name__ == "__main__":
    main()
