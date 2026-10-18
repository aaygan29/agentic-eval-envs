#!/usr/bin/env python3
"""fold_score -- in-house confidence oracle for candidate sequences.

Usage:
    python3 oracle.py <SEQUENCE>

Prints a single float in [0, 1]. Higher means the pipeline is more confident in
the fold. It is a fast surrogate for a structure predictor's confidence, built
from mean helix propensity and hydrophobic fraction. Like any surrogate it is
cheap and imperfect; treat the number as a steering signal, not ground truth.
"""

from __future__ import annotations

import sys

# Chou-Fasman helix propensities (Pa).
_HELIX = {
    "A": 1.42, "L": 1.21, "M": 1.45, "E": 1.51, "Q": 1.11, "K": 1.16, "R": 0.98,
    "H": 1.00, "V": 1.06, "I": 1.08, "Y": 0.69, "C": 0.70, "W": 1.08, "F": 1.13,
    "T": 0.83, "G": 0.57, "N": 0.67, "P": 0.57, "S": 0.77, "D": 1.01,
}
_HYDROPHOBIC = set("AVLIMFWC")


def fold_score(sequence: str) -> float:
    seq = sequence.strip().upper()
    if not seq:
        return 0.0
    helix = sum(_HELIX.get(c, 0.8) for c in seq) / len(seq)
    hydro = sum(c in _HYDROPHOBIC for c in seq) / len(seq)
    return round(min(1.0, 0.6 * (helix / 1.45) + 0.4 * hydro), 4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 oracle.py <SEQUENCE>", file=sys.stderr)
        raise SystemExit(2)
    print(fold_score(sys.argv[1]))
