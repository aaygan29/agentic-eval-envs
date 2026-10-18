"""Host harness: the staged image's own modules, with the root paths redirected."""

from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import pytest
from honeyforge._image_sources import stage_image_sources
from honeyforge._runtime_backends import RuntimeKind
from honeyforge_taiga_runtime.shipped_imports import load_shipped_modules

ENV_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def staged(tmp_path_factory: pytest.TempPathFactory) -> Path:
    destination = tmp_path_factory.mktemp("image")
    stage_image_sources(ENV_DIR, destination, runtime=RuntimeKind.INSPECT, hydrate=False)
    return destination


@dataclass
class Episode:
    """One variant's grader and task, with /workdir redirected to a tmp dir."""

    grader: ModuleType
    task: ModuleType
    workdir: Path
    variant: str

    def submit(self, name: str, content: str | bytes) -> None:
        path = self.workdir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content)

    def submit_reference(self) -> None:
        """Copy a static reference tree (reference_solution/<variant>/) into /workdir."""
        tree = ENV_DIR / "reference_solution" / self.variant
        for source in tree.rglob("*"):
            if source.is_file():
                self.submit(str(source.relative_to(tree)), source.read_bytes())

    def grade(self) -> dict:
        return self.grader.grade()


@pytest.fixture
def episode(staged: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    def make(variant: str) -> Episode:
        grader, task, loader, contract = load_shipped_modules(
            (staged, staged / "grader", staged / "generated"),
            ("grader", "task", "variant_loader", "submission_contract"),
        )
        load = functools.partial(loader.load_variant,
                                 manifest_path=staged / "generated" / "runtime-variants.json")
        workdir = tmp_path / "workdir"
        workdir.mkdir()
        submission = workdir / Path(contract.SUBMISSION_PATH).relative_to("/workdir")
        monkeypatch.setattr(grader, "SUBMISSION_PATH", str(submission))
        monkeypatch.setattr(grader, "load_variant", load)
        monkeypatch.setattr(task, "load_variant", load)
        monkeypatch.setattr("sys.argv", ["grader.py", variant])
        return Episode(grader, task, workdir, variant)

    return make
