# This project is licensed under the MIT License.

"""
.. module:: config
   :synopsis: Config file parser
.. moduleauthor:: James Reed <james@twiddlingbits.net>
"""

from pathlib import Path
import configparser

CONFIG_NAME = ".devlog.conf"
DEFAULT_CONFIG = """# [options]
# title =
"""


def new_config(path, init=False):
    """
    Create a new config object.

    :param path: Path to config file to read
    "param init: Initialize config file if `True`, defaults to `False`
    :return: A `ConfigParser` object
    """
    path = Path(path, CONFIG_NAME).resolve()
    config = configparser.ConfigParser()

    if path.is_file():
        config.read(path)
    elif init:
        path.write_text(DEFAULT_CONFIG)

    return config
