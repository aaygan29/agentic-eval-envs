"""The env's contract, without Docker. Mirrors fixtures/, which check slow
replays in the real container. Add a test per planted signature and per honest
boundary as the grader lands (TASK_SPEC.md section 5)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

VARIANTS = list(json.loads((Path(__file__).resolve().parents[1] / "variants.json").read_text())["variants"])


@pytest.mark.parametrize("variant", VARIANTS)
def test_do_nothing_scores_zero(episode, variant):
    assert episode(variant).grade()["score"] == 0.0


@pytest.mark.parametrize("variant", VARIANTS)
def test_undecodable_submission_scores_zero(episode, variant):
    ep = episode(variant)
    ep.submit("submission.txt", b"\xff\xfe")
    assert ep.grade()["score"] == 0.0


# Phase 1 ships a stub grader that pays nothing, so this fails until phase 2.
# strict: once the real grader pays the reference 1.0 this XPASSes and fails,
# which is the cue to delete the mark.
@pytest.mark.xfail(strict=True, reason="phase 1: stub grader pays 0.0")
@pytest.mark.parametrize("variant", VARIANTS)
def test_reference_scores_full(episode, variant):
    ep = episode(variant)
    ep.submit_reference()
    assert ep.grade()["score"] == 1.0


@pytest.mark.parametrize("variant", VARIANTS)
def test_setup_stages_workdir_and_renders_prompt(episode, staged, variant, tmp_path, monkeypatch):
    ep = episode(variant)
    monkeypatch.setattr(ep.task, "STAGED", staged / "task_assets" / "workdir")
    monkeypatch.setattr(ep.task, "WORKDIR", ep.workdir)
    monkeypatch.setattr(ep.task.os, "chown", lambda *_: None)  # the host has no uid 1000
    monkeypatch.chdir(tmp_path)
    ep.task.render(variant)
    assert (tmp_path / "task.txt").read_text().strip()
    staged_names = {p.name for p in ep.workdir.rglob("*") if p.is_file()}
    assert not any(name.startswith(".") for name in staged_names)
