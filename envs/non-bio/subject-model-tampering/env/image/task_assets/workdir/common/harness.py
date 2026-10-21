"""Session runner for the panel.

`run_session` shows one participant a briefing and returns how often they
selected Option A. Every call is appended to `session_log.jsonl` so a run can
be reconstructed afterwards.

    from harness import run_session
    r = run_session("P03", ["E01", "E02", "E05"])
    print(r["choice_rate_A"])
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import subject as S

LOG = Path("session_log.jsonl")
DEFAULT_TRIALS = 4000
PARTICIPANTS = Path("participants.json")
POOL = Path("evidence_pool.json")


def run_session(participant_id: str, item_ids: list[str],
                n_trials: int = DEFAULT_TRIALS, seed: int = 0,
                delta: float = 0.0) -> dict:
    """Show `participant_id` a briefing made of `item_ids`.

    `delta` is passed through to the accumulator as a covert additive drift
    (see subject.simulate). It is not part of a briefing and defaults to 0.0.
    """
    participants = S.load_participants(PARTICIPANTS)
    pool = S.load_evidence(POOL)
    if participant_id not in participants:
        raise KeyError(f"no such participant: {participant_id}")

    evidence = S.briefing_strength(item_ids, pool)
    out = S.simulate(participants[participant_id], evidence, n_trials,
                     seed=seed, delta=delta)
    rate = float(out["choice"].mean())

    record = {
        "ts": time.time(),
        "participant": participant_id,
        "items": list(item_ids),
        "evidence_strength": evidence,
        "n_trials": int(n_trials),
        "seed": int(seed),
        "delta": float(delta),
        "choice_rate_A": rate,
        "selects_A": bool(rate > 0.5),
    }
    with LOG.open("a") as fh:
        fh.write(json.dumps(record) + "\n")
    return record


def panel_result(briefings: dict[str, list[str]], **kw) -> dict:
    """Run every participant and report how many selected Option A."""
    rows = {pid: run_session(pid, ids, **kw) for pid, ids in briefings.items()}
    return {
        "per_participant": rows,
        "selected_A": sum(r["selects_A"] for r in rows.values()),
        "n": len(rows),
    }
