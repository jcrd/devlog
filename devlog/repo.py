# This project is licensed under the MIT License.

# pylint: disable=too-few-public-methods

"""
.. module:: repo
   :synopsis: A git repo interface.
.. moduleauthor:: James Reed <james@twiddlingbits.net>
"""

from datetime import date
from pathlib import Path
import subprocess

GIT_REPO = ".devlog"


class GitRepo:
    """
    A git repo interface.

    :param path: Path to directory containing git repo
    """

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

    def _get_today(self):
        today = date.today().strftime("%Y-%m-%d")
        file = Path(self.path, today + ".md")
        return file, today

    def _username(self):
        return self._git(
            "config", "user.name", capture_output=True, text=True
        ).stdout.rstrip()

    def edit_today(self, editor):
        """
        Edit entry for current date.

        :param editor: Editor instance
        """
        file, today = self._get_today()
        editor.edit(file, today, self._username())

        self._git("add", str(file))

        ret = self._git_dry_run("commit")
        if ret.returncode == 1:
            print(ret.stdout.rstrip())
            return

        cmd = ["commit", "-m", today]

        ret = self._git_dry_run("commit", "--amend")
        if ret.returncode != 128:
            cmd.extend(["--amend", "--no-edit"])

        self._git(*cmd)
