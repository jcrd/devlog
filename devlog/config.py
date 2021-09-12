# This project is licensed under the MIT License.

"""
.. module:: config
   :synopsis: Config file parser
.. moduleauthor:: James Reed <james@twiddlingbits.net>
"""

from configparser import ConfigParser
from pathlib import Path

CONFIG_NAME = ".devlog.conf"
DEFAULT_CONFIG = """# [options]
# auto_push = true
# title =
"""


class Config(ConfigParser):
    """
    A configuration object.
    """

    @property
    def auto_push(self):
        """
        The state of the auto push option.

        :return: `True` if set, otherwise `False`
        """
        return self.get("options", "auto_push", fallback=True)


def new_config(path, init=False):
    """
    Create a new config object.

    :param path: Path to config file to read
    "param init: Initialize config file if `True`, defaults to `False`
    :return: A `ConfigParser` object
    """
    path = Path(path, CONFIG_NAME).resolve()
    config = Config()

    if path.is_file():
        config.read(path)
    elif init:
        path.write_text(DEFAULT_CONFIG)

    return config
