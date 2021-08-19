from pathlib import Path
from setuptools import setup


def read(name):
    return open(Path(Path(__file__).parent, name)).read()


setup(
    name="devlog",
    version="0.0.0",
    packages=["devlog"],
    test_suite="test",
    entry_points={
        "console_scripts": [
            "devlog = devlog.__main__:main",
        ],
    },
    description="Log your development process",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/jcrd/devlog",
    license="MIT",
    author="James Reed",
    author_email="james@twiddlingbits.net",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
