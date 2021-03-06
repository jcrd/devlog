# This project is licensed under the MIT License.

# pylint: disable=missing-module-docstring,missing-function-docstring

from subprocess import CalledProcessError
import argparse
import sys

from devlog.config import new_config
from devlog.editor import Editor
from devlog.repo import GitRepo


def get_repo(path):
    try:
        repo = GitRepo(path)
    except FileNotFoundError:
        sys.stderr.write("Repo uninitialized; run `devlog init`\n")
        sys.exit(1)

    return repo


def cmd_init(args):
    print("Initializing git repo...")
    GitRepo(args.directory, init=True)
    print("Initializing config file...")
    new_config(args.directory, init=True)


def cmd_remote(args):
    repo = get_repo(args.directory)
    repo.set_remote(args.url)


def cmd_push(args):
    repo = get_repo(args.directory)
    try:
        if repo.push() == GitRepo.PushStatus.NO_REMOTE:
            sys.stderr.write("No remote; run `devlog remote <URL>`\n")
            sys.exit(1)
    except GitRepo.PushError as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def cmd_pull(args):
    repo = get_repo(args.directory)
    try:
        if not repo.pull():
            sys.stderr.write("No remote; run `devlog remote <URL>`\n")
            sys.exit(1)
    except CalledProcessError as err:
        sys.stderr.write(err.stderr)
        sys.exit(err.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=".", help="Path to dev directory")
    parser.add_argument("-e", "--editor", help="Editor to use")

    subp = parser.add_subparsers(title="commands", dest="cmd")
    initp = subp.add_parser("init", help="Initialize repo")
    initp.set_defaults(cmd=cmd_init)
    remotep = subp.add_parser("remote", help="Set remote URL")
    remotep.add_argument("url", help="Remote URL")
    remotep.set_defaults(cmd=cmd_remote)
    pushp = subp.add_parser("push", help="Update remote")
    pushp.set_defaults(cmd=cmd_push)
    pullp = subp.add_parser("pull", help="Pull from remote")
    pullp.set_defaults(cmd=cmd_pull)

    args = parser.parse_args()

    if args.cmd:
        args.cmd(args)
        sys.exit()

    config = new_config(args.directory)
    repo = get_repo(args.directory)

    if config.auto_push:
        try:
            repo.auto_push()
        except GitRepo.PushError as err:
            sys.stderr.write(str(err))
            sys.exit(1)

    try:
        editor = Editor(config, cmd=args.editor)
    except FileNotFoundError as error:
        sys.stderr.write("Command not found: {}\n".format(error.args[0]))
        sys.exit(2)

    try:
        repo.edit_today(editor)
    except GitRepo.CommitError as err:
        sys.stderr.write(str(err))
        sys.exit(1)


if __name__ == "__main__":
    main()
