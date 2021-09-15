# This project is licensed under the MIT License.

# pylint: disable=too-few-public-methods

"""
.. module:: repo
   :synopsis: A git repo interface.
.. moduleauthor:: James Reed <james@twiddlingbits.net>
"""

from datetime import date, datetime
from enum import Enum, auto
from pathlib import Path
import subprocess

GIT_REPO = ".devlog"
GIT_BRANCH = "devlog"


class GitRepo:
    """
    A git repo interface.

    :param path: Path to directory containing git repo
    "param init: Initialize git repo if `True`, defaults to `False`
    """

    DATE_FORMAT = "%Y-%m-%d"

    class CommitStatus(Enum):
        """
        Status of commit made after editing an entry.
        """

        NONE = auto()
        NEW = auto()
        AMEND = auto()

    class PushStatus(Enum):
        """
        Status of push command.
        """

        NO_REMOTE = auto()
        INACTION = auto()
        DRY_RUN = auto()
        FAILURE = auto()
        SUCCESS = auto()

    def __init__(self, path, init=False):
        path = Path(path).resolve()
        self.name = path.name
        self.path = Path(path, GIT_REPO).resolve(strict=not init)

        if init:
            if not self.path.is_dir():
                self.path.mkdir()
            if not Path(self.path, ".git").is_dir():
                self._git("init", "-q")
                self._git("checkout", "--orphan", GIT_BRANCH)

    def _git(self, *args, check=True, **kwargs):
        return subprocess.run(
            ["git", "-C", str(self.path)] + list(args), check=check, **kwargs
        )

    def _git_dry_run(self, *args):
        return self._git(
            *args, "--dry-run", check=False, capture_output=True, text=True
        )

    def _username(self):
        ret = self._git(
            "config", "user.name", check=False, capture_output=True, text=True
        )

        if ret.returncode != 0:
            return "unknown"

        return ret.stdout.rstrip()

    def last_commit_date(self):
        """
        Get date of last commit.

        :return: Date of last commit
        """
        ret = self._git(
            "log",
            "-1",
            "--pretty=format:%B",
            check=False,
            capture_output=True,
            text=True,
        )
        if ret.returncode == 128:
            return None

        return datetime.strptime(ret.stdout.rstrip(), self.DATE_FORMAT).date()

    def _check_remote(self):
        return (
            self._git(
                "remote", "get-url", "origin", check=False, capture_output=True
            ).returncode
            != 2
        )

    def edit_today(self, editor, today=None):
        """
        Edit entry for current or specified date.

        :param editor: Editor instance
        :param today: Date of entry to edit, defaults to current date
        :return: Commit status, one of `GitRepo.CommitStatus`
        """
        if not today:
            today = date.today()

        path = Path(self.path, str(today.year), str(today.month))
        file = Path(path, str(today.day) + ".md")
        path.mkdir(parents=True, exist_ok=True)

        datefmt = today.strftime(self.DATE_FORMAT)
        editor.edit(file, title=self.name, date=datefmt, author=self._username())

        self._git("add", str(file))

        ret = self._git_dry_run("commit")
        if ret.returncode == 1:
            print(ret.stdout.rstrip())
            return self.CommitStatus.NONE

        cmd = ["commit", "-m", datefmt]
        status = self.CommitStatus.NEW

        if self.last_commit_date() == today:
            cmd.append("--amend")
            status = self.CommitStatus.AMEND

        self._git(*cmd)

        return status

    def set_remote(self, url):
        """
        Set remote URL.

        :param url: The remote URL
        """

        self._git("remote", "add", "origin", url)

    def push(self, dry_run=False):
        """
        Update remote.

        :param dry_run: If `True`, don't update remote, only return status
        :return: Push status, one of `GitRepo.PushStatus`
        """
        if not self._check_remote():
            return self.PushStatus.NO_REMOTE

        if dry_run:
            return self.PushStatus.DRY_RUN

        ret = self._git_dry_run("push", "origin")
        if ret.returncode > 0:
            print(ret.stderr.rstrip())
            return self.PushStatus.FAILURE

        if not dry_run:
            self._git("push", "origin")
        return self.PushStatus.SUCCESS

    def auto_push(self, today=None, dry_run=False):
        """
        Automatically update remote if the last commit date is before today.

        :param today: Date to use as condition, defaults to current date
        :param dry_run: If `True`, don't update remote, only return status
        :return: Push status, one of `GitRepo.PushStatus`
        """

        if not today:
            today = date.today()
        last_date = self.last_commit_date()
        if last_date and last_date < today:
            return self.push(dry_run=dry_run)

        return self.PushStatus.INACTION
