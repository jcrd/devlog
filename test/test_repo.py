# This project is licensed under the MIT License.

# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods

from datetime import date
import tempfile
import unittest

from devlog.repo import GitRepo


class Editor:
    def __init__(self):
        self.text = ""

    def edit(self, file, **_):
        file.write_text(self.text)


class TestGitRepo(unittest.TestCase):
    def setUp(self):
        self.editor = Editor()

    def test_commit_status(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = GitRepo(temp, init=True)

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
