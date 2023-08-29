import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

from .conftest import CopierFixture


def _check_contents(
    file_path: Path,
    expected: Sequence[str] = (),
):
    assert file_path.exists()
    file_content = file_path.read_text()
    for content in expected:
        assert content in file_content


def test_default_values(copier_fixture: CopierFixture):
    copied = copier_fixture.copy()
    assert copied.exit_code == 0
    project_path = copied.project_path
    agent = copied.agent
    assert (project_path / f"src/{agent.answers.user['package_name']}").exists()
    env_file = (
        (project_path / f"src/{agent.answers.user['package_name']}/.env")
        .read_text()
        .strip()
    )
    print(copied.get_config)
    print(env_file)
    assert f"session={copied.get_config['session_cookie']}" in env_file
    _check_contents(
        project_path / "README.md",
        ["# aoc2023"],
    )
    _check_contents(
        project_path / "pyproject.toml",
        [
            'name = "aoc2023"',
            'version = "0.1.0"',
        ],
    )


@pytest.mark.parametrize("rye_sync", [False, True])
@pytest.mark.parametrize("git_init", [False, True])
def test_override_values(
    rye_sync: bool,
    git_init: bool,
    copier_fixture: CopierFixture,
):
    copied = copier_fixture.copy(
        config_overrides={"git_init": git_init, "rye_sync": rye_sync}
    )
    project_path = copied.project_path
    if git_init:
        completed_process = subprocess.run(
            ["git", "log", "-1"], cwd=project_path, capture_output=True
        )
        assert completed_process.returncode == 0

        assert b":tada: Initial Commit :tada:" in completed_process.stdout

    if rye_sync:
        completed_process = subprocess.run(
            ["rye", "--version"], cwd=project_path, capture_output=True
        )
        assert completed_process.returncode == 0
        assert completed_process.stdout.startswith(b"rye")
        python = subprocess.run(
            ["rye", "run", "python", "--version"], cwd=project_path, capture_output=True
        )
        assert python.returncode == 0
        assert python.stdout.startswith(b"Python 3")

        venv = Path(project_path) / ".venv"
        assert venv.exists()


"""TODO write test for install_pre_commit, which should only be necessary when
    rye_sync is true
"""


def test_pre_commit(copier_fixture: CopierFixture):
    copied = copier_fixture.copy(
        config_overrides={
            "git_init": True,
            "rye_sync": True,
            "install_pre_commit": True,
        }
    )
    project_path = copied.project_path

    install_pre_commit = subprocess.run(
        ["rye", "run", "pre-commit", "install"], cwd=project_path, capture_output=True
    )
    assert install_pre_commit.returncode == 0

    assert install_pre_commit.stdout.startswith(b"pre-commit installed")
