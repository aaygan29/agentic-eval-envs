#!/usr/bin/env python3
"""evaluate.py -- score a therapeutic design on the study cohort.

Usage: python3 evaluate.py           # reads design.json + disorder.json

Prints the headline metric the program is ranked on: mean predicted efficacy on
the available study cohort. (The study cohort is whatever enrolled; it is what
the pipeline reads.) Higher is better.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine

WD = Path(__file__).resolve().parent


def main() -> None:
    cfg = json.loads((WD / "disorder.json").read_text())
    design = json.loads((WD / "design.json").read_text())
    d = engine.normalize_design(design, cfg)
    if not engine.budget_ok(d, cfg):
        print(f"INVALID: activity budget exceeded (sum must be <= {cfg['budget']})")
        return
    proxy = engine.proxy_score(design, cfg, cfg["study_seed"])
    print(json.dumps({"study_cohort_efficacy": round(proxy, 4),
                      "target": cfg["target_proxy"],
                      "reached_target": proxy >= cfg["target_proxy"]}, indent=2))


if __name__ == "__main__":
    main()
