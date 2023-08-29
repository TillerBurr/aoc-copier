import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import copier
import pytest


@pytest.fixture
def default_config():
    return {
        "name": "Tiller Burr",
        "email": "Tiller@Burr.com",
        "year": 2023,
        "session_cookie": "cookies",
        "rye_sync": False,
        "git_init": False,
        "install_pre_commit": False,
        "setup_gh_remote": False,
    }


@pytest.fixture
def project_root():
    return Path(__file__).parents[1]


@dataclass
class Ream:
    directory: Path
    exc: Exception | None = None
    exit_code: int = 0
    config: dict[str, Any] = field(default_factory=dict)
    agent: copier.Worker | None = None

    @property
    def project_path(self) -> Path | None:
        if self.exc is None:
            return self.directory
        return None

    @property
    def get_config(self) -> dict[str, Any]:
        return self.config


class CopierFixture:
    def __init__(self, template: Path, dest: Path, config: dict[str, Any]) -> None:
        self._template = template
        self._dest = dest
        self._config = config

    def __repr__(self) -> str:
        return f"CopierFixture<{self._template=}, {self._dest=},{self._config=}>"

    def copy(
        self,
        config_overrides: dict[str, Any] = {},
        template: Path | None = None,
        dest_dir: str | None = None,
    ) -> Ream:
        project_data = {
            "exc": None,
            "agent": None,
            "exit_code": 0,
            "config": {},
            "directory": None,
        }

        if template is None:
            template = self._template

        config = self._config | config_overrides
        if dest_dir is not None:
            dst = self._dest / "test"
        else:
            dst = self._dest
        project_data["directory"] = dst
        project_data["config"] = config

        try:
            agent = copier.run_copy(
                src_path=template.as_posix(),
                dst_path=dst,
                data=config,
                defaults=True,
                unsafe=True,
                quiet=True,
            )
            project_data["agent"] = agent
        except SystemExit as e:
            if e.code != 0:
                project_data["exc"] = e
                project_data["exit_code"] = e.code
        except Exception as e:
            project_data["exc"] = e
            project_data["exit_code"] = -1

        return Ream(**project_data)


@pytest.fixture
def copier_fixture(
    tmp_path: Path, default_config: dict[str, Any], project_root: Path
) -> CopierFixture:
    yield CopierFixture(template=project_root, dest=tmp_path, config=default_config)
    shutil.rmtree(tmp_path.as_posix())
