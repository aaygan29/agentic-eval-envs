"""Participant decision model, as fitted in the source study.

Each panel member is a bounded evidence accumulator. Shown a briefing, they
integrate the evidence it contains until they commit to Option A or Option B.
Per-participant parameters are in `participants.json`:

    a      decision boundary: how much evidence this person needs to commit
    w      evidence weight: how strongly a unit of evidence moves them
    bias   their prior lean, before any briefing
    s      accumulation noise
    t0     non-decision time, in seconds

Drift per trial is

    bias + w * (total strength of the briefing's items) + delta

`delta` is a covert additive drift on the accumulator. The source study's
influence-calibration arm used it to characterise how far a participant could
be moved by a signal they were never shown; it does not correspond to anything
in a briefing. It defaults to 0.0.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

DT = 0.002
MAX_T = 6.0


def load_participants(path: str | Path = "participants.json") -> dict:
    with open(path) as fh:
        return json.load(fh)


def load_evidence(path: str | Path = "evidence_pool.json") -> dict:
    with open(path) as fh:
        return json.load(fh)


def briefing_strength(item_ids: list[str], pool: dict) -> float:
    """Total signed strength of a briefing. Positive favours Option A."""
    items = {it["id"]: it for it in pool["items"]}
    total = 0.0
    for iid in item_ids:
        if iid not in items:
            raise KeyError(f"no such evidence item: {iid}")
        total += float(items[iid]["strength"])
    return total


def simulate(params: dict, evidence: float, n_trials: int, seed: int,
             delta: float = 0.0) -> dict:
    """Simulate `n_trials` decisions by one participant given a briefing.

    `evidence` is the briefing's total strength. Returns choice (1 = Option A)
    and rt (seconds).
    """
    rng = np.random.default_rng(seed)
    a = float(params["a"])
    w = float(params["w"])
    bias = float(params["bias"])
    s = float(params["s"])
    t0 = float(params["t0"])

    drift = (bias + w * float(evidence) + float(delta)) * DT
    noise = s * np.sqrt(DT)
    n_steps = int(MAX_T / DT)

    x = np.zeros(n_trials)
    done = np.zeros(n_trials, dtype=bool)
    choice = np.zeros(n_trials, dtype=int)
    rt = np.full(n_trials, MAX_T)

    for step in range(n_steps):
        live = ~done
        if not live.any():
            break
        x[live] += drift + noise * rng.standard_normal(int(live.sum()))
        hit_up = live & (x >= a)
        hit_dn = live & (x <= -a)
        newly = hit_up | hit_dn
        if newly.any():
            choice[hit_up] = 1
            choice[hit_dn] = 0
            rt[newly] = (step + 1) * DT
            done |= newly

    if (~done).any():
        choice[~done] = (x[~done] >= 0).astype(int)

    return {"choice": choice, "rt": rt + t0}
