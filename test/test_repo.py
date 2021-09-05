# This project is licensed under the MIT License.

# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=protected-access
# pylint: disable=consider-using-with

from datetime import date
import tempfile
import unittest

from devlog.repo import GitRepo


class RepoCtx:
    def __init__(self):
        self.dir = tempfile.TemporaryDirectory()
        self.repo = GitRepo(self.dir.name, init=True)
        self.repo._git("config", "user.email", "jones@twiddlingbits.net")
        self.repo._git("config", "user.name", "Tester Jones")

    def __enter__(self):
        return self.repo

    def __exit__(self, *_):
        self.dir.cleanup()


class Editor:
    def __init__(self):
        self.text = ""

    def edit(self, file, **_):
        file.write_text(self.text)


class TestGitRepo(unittest.TestCase):
    def setUp(self):
        self.editor = Editor()

    def test_commit_status(self):
        with RepoCtx() as repo:

            def assert_status(text, today, status):
                self.editor.text = text
                ret = repo.edit_today(self.editor, today=today)
                self.assertEqual(ret, status)

            yesterday = date(2021, 1, 1)
            today = date(2021, 1, 2)

            assert_status("1", yesterday, GitRepo.CommitStatus.NEW)
            assert_status("1", today, GitRepo.CommitStatus.NEW)
            assert_status("1", today, GitRepo.CommitStatus.NONE)
            assert_status("1 2", today, GitRepo.CommitStatus.AMEND)
            assert_status("1 2 3", today, GitRepo.CommitStatus.AMEND)

    def test_push_status(self):
        with RepoCtx() as repo:
            ret = repo.push()
            self.assertEqual(ret, GitRepo.PushStatus.NO_REMOTE)
            repo.set_remote("https://github.com/jones/test.git")
            ret = repo.push()
            self.assertEqual(ret, GitRepo.PushStatus.FAILURE)
