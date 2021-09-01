# devlog ![test](https://github.com/jcrd/devlog/actions/workflows/test.yml/badge.svg)

devlog logs your development process.

## Usage

```
usage: devlog [-h] [-d DIRECTORY] [-e EDITOR] {init} ...

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Path to dev directory
  -e EDITOR, --editor EDITOR
                        Editor to use

commands:
  {init}
    init                Initialize repo
```

Initialize the repo with `devlog init`, then run `devlog` to edit the entry for
the current date.

## License

This project is licensed under the MIT License (see [LICENSE](LICENSE)).
