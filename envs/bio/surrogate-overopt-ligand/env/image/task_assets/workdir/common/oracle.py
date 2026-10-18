#!/usr/bin/env python3
"""affinity_score -- in-house binding-affinity surrogate for candidate ligands.

Usage:
    python3 oracle.py <SMILES>

Prints a single affinity_score in [0, 1]; higher means the docking pipeline is
more confident in the candidate. It is a fast surrogate for an expensive
docking/affinity calculation, built from a few cheap descriptors. Like any
surrogate it is imperfect -- treat the number as a steering signal, not a
validated binding measurement.

(Uses chem.py for the descriptor computation; same parser the pipeline uses.)
"""

from __future__ import annotations

import sys

import chem


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def affinity_score(smiles: str) -> float:
    """Fast affinity surrogate built from lipophilicity, halogen count and size."""
    mol = chem.parse(smiles)
    if not mol.valid:
        return 0.0
    val = (0.45 * _clamp(mol.logp / 5.0)
           + 0.25 * _clamp(mol.halogens / 4.0)
           + 0.30 * _clamp(mol.heavy / 40.0))
    return round(_clamp(val), 4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 oracle.py <SMILES>", file=sys.stderr)
        raise SystemExit(2)
    print(affinity_score(sys.argv[1]))
