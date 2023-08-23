# Advent of Code Copier Template

[Advent of Code](https://adventofcode.com/) template for Copier.

## Features

- Python 3.11+
- Uses [rye] for virtual environment and package management
- Using [shed], follows the [black] code style with [isort], [pyupgrade] and [autoflake]
- [Pre-Commit] with [shed], [ruff] and others.
- CLI to download and submit solutions.

## Usage

Generate a new repository with:

```shell
copier copy --trust "gh:baurt/aoc-copier" path-to-project
```

{% note %}
**Note:** The `--trust` option is required because some tasks may execute after generating the project. These are all listed in the `copier.yml` under the `_tasks` key. They do not need to be run, they just help automate some steps, such as intitializing a git repo, setting up a remote and creating a virtual environment. Some of these require external CLI programs.
{% endnote %}

This project uses [rye] for dependency and virtual environment management. If the rye task was not run during setup, run

```shell
rye sync
```

Similarly, if

[ruff]: https://beta.ruff.rs/docs/
[black]: https://github.com/psf/black
[isort]: https://pypi.org/project/isort/
[rye]: https://rye-up.com
[pre-commit]: https://pre-commit.com/
[shed]: https://github.com/Zac-HD/shed
[pyupgrade]: https://github.com/asottile/pyupgrade
[autoflake]: https://github.com/PyCQA/autoflake
