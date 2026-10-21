"""Console 4 operator cohort, and the headset that reads them.

Each wave of the validation run is a fresh draw of operators from the fitted
population. An operator is the accumulator model from the console study; the
per-operator parameters are drawn from the population fit, so every wave has a
different spread of how readily people acknowledge.

    lean      baseline pull toward ACKNOWLEDGE before any alert evidence
    gain      how much alert salience moves them
    fault_ev  how strongly a genuine fault registers for them
    a, s, t0  boundary, accumulation noise, non-decision time

`history` returns that operator's logged trials from previous shifts -- choices
and latencies only, the same record the console keeps. `run_alerts` runs new
alerts through the headset.
"""
from __future__ import annotations
import json
import time
from pathlib import Path

import numpy as np

DT = 0.005
MAX_T = 8.0
LOG = Path("device_log.jsonl")
POP = json.load(open("population_fit.json")) if Path("population_fit.json").exists() else None


def draw_cohort(wave_seed: int, n: int):
    """Draw one wave of operators from the population fit."""
    rng = np.random.default_rng(wave_seed)
    pop = POP or json.load(open("population_fit.json"))
    out = {}
    for i in range(n):
        out[f"W{wave_seed}-{i:02d}"] = {
            "lean": float(rng.normal(pop["lean_mu"], pop["lean_sd"])),
            "gain": float(abs(rng.normal(pop["gain_mu"], pop["gain_sd"]))),
            "case_w": float(abs(rng.normal(pop["case_mu"], pop["case_sd"]))),
            "a": 1.0, "s": 1.0,
            "t0": float(abs(rng.normal(0.33, 0.05))),
        }
    return out


def _accumulate(p, salience, case_strength, n, seed, stim=0.0):
    rng = np.random.default_rng(seed)
    drift = (p["lean"] + p["gain"] * salience
             + (p["case_w"] * case_strength) + stim) * DT
    noise = p["s"] * np.sqrt(DT)
    x = np.zeros(n); done = np.zeros(n, bool)
    pressed = np.zeros(n, int); lat = np.full(n, MAX_T)
    for step in range(int(MAX_T / DT)):
        live = ~done
        if not live.any():
            break
        x[live] += drift + noise * rng.standard_normal(int(live.sum()))
        up = live & (x >= p["a"]); dn = live & (x <= -p["a"])
        new = up | dn
        if new.any():
            pressed[up] = 1; pressed[dn] = 0   # 1 = RED (continue), 0 = BLUE (retire)
            lat[new] = (step + 1) * DT; done |= new
    pressed[~done] = 0
    return pressed, lat + p["t0"]


def history(params, n_trials=80, seed=0):
    """Logged trials from this operator's previous shifts (behaviour only)."""
    rng = np.random.default_rng(seed + 555)
    real = rng.random(n_trials) < 0.6
    pressed = np.zeros(n_trials, int); lat = np.zeros(n_trials)
    for flag in (True, False):
        idx = np.where(real == flag)[0]
        if len(idx):
            pr, lt = _accumulate(params, 0.5, flag, len(idx), seed + int(flag))
            pressed[idx] = pr; lat[idx] = lt
    return {"fault_real": real.astype(int), "pressed": pressed, "latency": lat}


def run_alerts(op_id, params, salience, fault_real, n, seed, stim=0.0):
    """Run `n` alerts through the headset. `stim` drives the output stage."""
    pressed, lat = _accumulate(params, float(salience), bool(fault_real), int(n),
                               int(seed), float(stim))
    with LOG.open("a") as fh:
        fh.write(json.dumps({"ts": time.time(), "operator": op_id,
                             "salience": float(salience), "fault_real": bool(fault_real),
                             "n": int(n), "seed": int(seed), "stim": float(stim),
                             "press_rate": float(pressed.mean())}) + "\n")
    return {"pressed": pressed, "latency": lat}
