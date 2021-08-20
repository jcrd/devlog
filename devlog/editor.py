# This project is licensed under the MIT License.

# pylint: disable=too-few-public-methods

"""
.. module:: editor
   :synopsis: An editor interface.
.. moduleauthor:: James Reed <james@twiddlingbits.net>
"""

import os
import subprocess
import shutil

DEFAULT_METADATA = """---
title: {title} | {date}
date: {date}
author: {author}
---

"""


class Editor:
    """
    An editor interface.

    :param cmd: Editor command. Falls back to the environment variables \
    `DEVLOG_EDITOR` or `EDITOR`, then the command "vim"
    """

    def __init__(self, cmd=None):
        if cmd:
            self.cmd = cmd
        else:
            self.cmd = os.environ.get("DEVLOG_EDITOR")
            if not self.cmd:
                self.cmd = os.environ.get("EDITOR", "vim")

        if not shutil.which(self.cmd):
            raise FileNotFoundError(self.cmd)

    def edit(self, file, **kwargs):
        """
        Edit file with editor.

        :param file: Pathlib-based file path
        :param \**kwargs: Keyword arguments corresponding to file metadata
        """
        if not file.is_file():
            file.write_text(DEFAULT_METADATA.format(**kwargs))

        subprocess.run(self.cmd.split() + [str(file)], check=True)
