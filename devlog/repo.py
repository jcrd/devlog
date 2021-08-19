# This project is licensed under the MIT License.

# pylint: disable=too-few-public-methods

"""
.. module:: repo
   :synopsis: A git repo interface.
.. moduleauthor:: James Reed <james@twiddlingbits.net>
"""

from datetime import date, datetime
from pathlib import Path
import subprocess

GIT_REPO = ".devlog"


class GitRepo:
    """
    A git repo interface.

    :param path: Path to directory containing git repo
    """

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, path):
        self.path = Path(path, GIT_REPO).resolve()

        if not self.path.is_dir():
            self.path.mkdir()
        if not Path(self.path, ".git").is_dir():
            self._git("init", "-q")

    def _git(self, *args, check=True, **kwargs):
        return subprocess.run(
            ["git", "-C", self.path] + list(args), check=check, **kwargs
        )

    def _git_dry_run(self, *args):
        return self._git(
            *args, "--dry-run", check=False, capture_output=True, text=True
        )

    def _username(self):
        return self._git(
            "config", "user.name", capture_output=True, text=True
        ).stdout.rstrip()

    def _check_amend(self, today):
        ret = self._git(
            "log",
            "-1",
            "--pretty=format:%B",
            check=False,
            capture_output=True,
            text=True,
        )
        if ret.returncode == 128:
            return False

        return datetime.strptime(ret.stdout.rstrip(), self.DATE_FORMAT).date() == today

    def edit_today(self, editor):
        """
        Edit entry for current date.

        :param editor: Editor instance
        """
        today = date.today()
        datefmt = today.strftime(self.DATE_FORMAT)
        file = Path(self.path, datefmt + ".md")
        editor.edit(file, datefmt, self._username())

        self._git("add", str(file))

        ret = self._git_dry_run("commit")
        if ret.returncode == 1:
            print(ret.stdout.rstrip())
            return

        cmd = ["commit", "-m", datefmt]

        if self._check_amend(today):
            cmd.append("--amend")

        self._git(*cmd)
