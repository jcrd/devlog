# This project is licensed under the MIT License.

# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods

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
            repo = GitRepo(temp)

            def assert_status(text, status):
                self.editor.text = text
                self.assertEqual(repo.edit_today(self.editor), status)

            assert_status("1", GitRepo.CommitStatus.NEW)
            assert_status("1", GitRepo.CommitStatus.NONE)
            assert_status("1 2", GitRepo.CommitStatus.AMEND)
            assert_status("1 2 3", GitRepo.CommitStatus.AMEND)
