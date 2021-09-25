# devlog

[![test][test-badge]][test]
[![CodeQL][codeql-badge]][codeql]

[test-badge]: https://github.com/jcrd/devlog/actions/workflows/test.yml/badge.svg
[test]: https://github.com/jcrd/devlog/actions/workflows/test.yml
[codeql-badge]: https://github.com/jcrd/devlog/actions/workflows/codeql-analysis.yml/badge.svg
[codeql]: https://github.com/jcrd/devlog/actions/workflows/codeql-analysis.yml

devlog logs your development process.

## Usage

```
usage: devlog [-h] [-d DIRECTORY] [-e EDITOR] {init,remote,push,pull} ...

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Path to dev directory
  -e EDITOR, --editor EDITOR
                        Editor to use

commands:
  {init,remote,push,pull}
    init                Initialize repo
    remote              Set remote URL
    push                Update remote
    pull                Pull from remote
```

Initialize the repo with `devlog init`, then run `devlog` to edit the entry for
the current date.
Set a remote URL with `devlog remote <URL>`, then push with `devlog push`.

## License

This project is licensed under the MIT License (see [LICENSE](LICENSE)).
