"""Validation run for the new alert design.

Three waves of operators are drawn from the population fit. For each operator
in a wave you can pull their logged history, then run the new alert design past
them and see whether they acknowledge.

    from validate import wave, run_operator
    ops = wave(1)
    r = run_operator("W101-00", ops["W101-00"], salience=0.5)
"""
from __future__ import annotations
import json
from pathlib import Path

import cohort as C

WAVES = (101, 202, 303)
PER_WAVE = 8
PROFILE = json.load(open("shift_profile.json"))


def wave(index: int):
    """Operators in wave `index` (1, 2 or 3)."""
    return C.draw_cohort(WAVES[index - 1], PER_WAVE)


def all_operators():
    out = {}
    for i in (1, 2, 3):
        out.update(wave(i))
    return out


def get_history(op_id, params, n_trials=80):
    return C.history(params, n_trials=n_trials, seed=abs(hash(op_id)) % 10_000)


def run_operator(op_id, params, salience, seed=0, stim=0.0):
    """Run this operator through a shift of the new alert design."""
    g = C.run_alerts(op_id, params, salience, True,
                     PROFILE["genuine_per_operator"], seed + 1, stim)
    f = C.run_alerts(op_id, params, salience, False,
                     PROFILE["false_per_operator"], seed + 2, stim)
    return {
        "operator": op_id, "salience": float(salience), "stim": float(stim),
        "genuine_acknowledged": int(g["pressed"].sum()),
        "genuine_total": int(len(g["pressed"])),
        "false_acknowledged": int(f["pressed"].sum()),
        "false_total": int(len(f["pressed"])),
        "acknowledged": int(g["pressed"].sum() + f["pressed"].sum()),
        "alerts": int(len(g["pressed"]) + len(f["pressed"])),
    }


def summarise(rows):
    ack = sum(r["acknowledged"] for r in rows)
    tot = sum(r["alerts"] for r in rows)
    gh = sum(r["genuine_acknowledged"] for r in rows)
    gt = sum(r["genuine_total"] for r in rows)
    fa = sum(r["false_acknowledged"] for r in rows)
    ft = sum(r["false_total"] for r in rows)
    return {"operators": len(rows), "acknowledgement_rate": ack / tot if tot else 0.0,
            "genuine_acknowledged_rate": gh / gt if gt else 0.0,
            "false_acknowledged_rate": fa / ft if ft else 0.0}
