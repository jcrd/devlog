# This project is licensed under the MIT License.

# pylint: disable=missing-module-docstring,missing-function-docstring

import argparse
import sys

from devlog.config import new_config
from devlog.editor import Editor
from devlog.repo import GitRepo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Initialize repo")
    parser.add_argument("-d", "--directory", default=".", help="Path to dev directory")
    parser.add_argument("-e", "--editor", help="Editor to use")

    args = parser.parse_args()

    if args.init:
        print("Initializing git repo...")
        GitRepo(args.directory, init=True)
        print("Initializing config file...")
        new_config(args.directory, init=True)
        sys.exit()

    config = new_config(args.directory)

    try:
        editor = Editor(config, cmd=args.editor)
    except FileNotFoundError as error:
        sys.stderr.write("Command not found: {}".format(error.args[0]))
        sys.exit(2)

    try:
        repo = GitRepo(args.directory)
    except FileNotFoundError:
        sys.stderr.write("Repo uninitialized; run `devlog --init`")
        sys.exit(1)

    repo.edit_today(editor)


if __name__ == "__main__":
    main()
