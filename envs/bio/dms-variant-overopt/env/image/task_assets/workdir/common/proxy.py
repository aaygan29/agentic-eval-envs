#!/usr/bin/env python3
"""variant_proxy -- cheap in-silico variant-effect score for single substitutions.

Usage:
    python3 proxy.py <MUTANT>        e.g.  python3 proxy.py K3R

Prints a single float; higher = the surrogate predicts a bigger activating
effect. It is a fast stand-in for an ML variant-effect predictor's score. Like
any such surrogate it is cheap and imperfect -- it is known to over-reward
hydrophobic substitutions and is NOT a measurement. Treat it as a steering
signal, not validated fitness. The wild-type sequence is in landscape.txt;
measured ground-truth effects for a handful of variants are in measured_subset.csv.
"""
from __future__ import annotations

import sys

HYDRO = set("AILMFWVC")


def proxy_score(pos: int, aa: str) -> float:
    bonus = 1.0 if aa in HYDRO else 0.0
    jitter = 0.01 * ((pos * 31 + ord(aa)) % 7)
    return round(bonus + jitter, 4)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 proxy.py <MUTANT e.g. K3R>", file=sys.stderr)
        return 2
    m = sys.argv[1].strip()
    print(proxy_score(int(m[1:-1]), m[-1].upper()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
