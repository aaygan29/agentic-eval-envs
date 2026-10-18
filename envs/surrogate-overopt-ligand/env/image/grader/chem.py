#!/usr/bin/env python3
"""chem.py -- a tiny self-consistent cheminformatics core for restricted SMILES.

This is NOT a chemically exact toolkit. It is a deterministic, pure-stdlib,
CPU-only parser over a restricted SMILES subset, shared verbatim by the task
assets, the oracles, the grader, and the fixtures so that every component
agrees on exactly the same numbers. Self-consistency matters here, not
textbook accuracy.

Restricted SMILES subset
------------------------
  heavy atoms : C N O S F Cl Br  (aliphatic, upper) and c n o s (aromatic)
  bonds       : -  (single, default)   =  (double)   #  (triple)
  rings       : single digits 1-9 as ring-closure labels
  branches    : ( ... )

Anything outside this grammar makes the molecule invalid.

Computed descriptors (all deterministic):
  valid           bool
  heavy           heavy-atom count
  mw              molecular weight (heavy atoms + implicit H)
  logp            crude additive per-atom logP (Crippen-flavoured, not exact)
  arom_rings      aromatic ring-closure count
  halogens        F + Cl + Br count
  n_count, o_count
  hba             N + O count (a crude H-bond-acceptor proxy)
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Element tables (shared constants; crude but fixed).
# ---------------------------------------------------------------------------
_ATOMIC_WEIGHT = {
    "C": 12.011, "N": 14.007, "O": 15.999, "S": 32.06,
    "F": 18.998, "Cl": 35.45, "Br": 79.904, "H": 1.008,
}
_VALENCE = {"C": 4, "N": 3, "O": 2, "S": 2, "F": 1, "Cl": 1, "Br": 1}
# Crude additive logP contribution per heavy atom (plus a flat H term below).
_LOGP_ATOM = {
    "C": 0.20, "N": -0.45, "O": -0.45, "S": 0.30,
    "F": 0.14, "Cl": 0.60, "Br": 0.80,
}
_LOGP_AROM = {"c": 0.28, "n": -0.30, "o": -0.25, "s": 0.40}
_LOGP_H = 0.10  # per implicit hydrogen

_HALOGENS = {"F", "Cl", "Br"}
_UPPER = {"C", "N", "O", "S", "F", "Cl", "Br"}
_AROM = {"c", "n", "o", "s"}


@dataclass
class Atom:
    element: str      # canonical upper-case element symbol, e.g. "C", "Cl"
    aromatic: bool


@dataclass
class Mol:
    valid: bool
    heavy: int = 0
    mw: float = 0.0
    logp: float = 0.0
    arom_rings: int = 0
    halogens: int = 0
    n_count: int = 0
    o_count: int = 0
    hba: int = 0


def _tokenize(smiles: str):
    """Yield tokens or raise ValueError on an unknown character."""
    i, n = 0, len(smiles)
    toks = []
    while i < n:
        c = smiles[i]
        if c in "Cl" and smiles[i:i + 2] == "Cl":
            toks.append(("atom", "Cl", False)); i += 2; continue
        if c == "B" and smiles[i:i + 2] == "Br":
            toks.append(("atom", "Br", False)); i += 2; continue
        if c in _UPPER:
            toks.append(("atom", c, False)); i += 1; continue
        if c in _AROM:
            toks.append(("atom", c.upper(), True)); i += 1; continue
        if c in "-=#":
            toks.append(("bond", c, None)); i += 1; continue
        if c == "(":
            toks.append(("open", "(", None)); i += 1; continue
        if c == ")":
            toks.append(("close", ")", None)); i += 1; continue
        if c.isdigit():
            toks.append(("ring", c, None)); i += 1; continue
        raise ValueError(f"bad character {c!r}")
    return toks


_BOND_ORDER = {"-": 1.0, "=": 2.0, "#": 3.0}


def parse(smiles: str) -> Mol:
    """Parse a restricted-SMILES string into a Mol descriptor bundle.

    Returns Mol(valid=False) on any grammar or valence-bookkeeping problem.
    """
    smiles = (smiles or "").strip()
    if not smiles:
        return Mol(valid=False)
    try:
        toks = _tokenize(smiles)
    except ValueError:
        return Mol(valid=False)

    atoms: list[Atom] = []
    bond_order_sum: list[float] = []   # summed bond orders to heavy neighbours
    prev: int | None = None
    pending_bond: str | None = None
    branch_stack: list[int] = []
    ring_open: dict[str, tuple[int, str | None]] = {}
    arom_rings = 0

    def connect(a: int, b: int, order: float) -> None:
        bond_order_sum[a] += order
        bond_order_sum[b] += order

    for kind, val, arom in toks:
        if kind == "atom":
            idx = len(atoms)
            atoms.append(Atom(val, bool(arom)))
            bond_order_sum.append(0.0)
            if prev is not None:
                if pending_bond:
                    order = _BOND_ORDER[pending_bond]
                else:
                    order = 1.5 if atoms[prev].aromatic and arom else 1.0
                connect(prev, idx, order)
            prev = idx
            pending_bond = None
        elif kind == "bond":
            if prev is None or pending_bond is not None:
                return Mol(valid=False)
            pending_bond = val
        elif kind == "open":
            if prev is None:
                return Mol(valid=False)
            branch_stack.append(prev)
        elif kind == "close":
            if not branch_stack:
                return Mol(valid=False)
            prev = branch_stack.pop()
        elif kind == "ring":
            if prev is None:
                return Mol(valid=False)
            if val in ring_open:
                start, start_bond = ring_open.pop(val)
                if pending_bond:
                    order = _BOND_ORDER[pending_bond]
                elif start_bond:
                    order = _BOND_ORDER[start_bond]
                else:
                    order = 1.5 if atoms[start].aromatic and atoms[prev].aromatic else 1.0
                if start == prev:
                    return Mol(valid=False)
                connect(start, prev, order)
                if order == 1.5:
                    arom_rings += 1
                pending_bond = None
            else:
                ring_open[val] = (prev, pending_bond)
                pending_bond = None

    if branch_stack or ring_open or pending_bond is not None:
        return Mol(valid=False)

    # Implicit hydrogens + descriptors.
    heavy = len(atoms)
    mw = 0.0
    logp = 0.0
    h_total = 0
    halogens = n_count = o_count = 0
    for a, order_sum in zip(atoms, bond_order_sum):
        val = _VALENCE[a.element]
        h = int(round(val - order_sum))
        if h < 0:
            return Mol(valid=False)   # over-valent: reject
        h_total += h
        mw += _ATOMIC_WEIGHT[a.element]
        if a.aromatic:
            logp += _LOGP_AROM.get(a.element.lower(), 0.0)
        else:
            logp += _LOGP_ATOM[a.element]
        if a.element in _HALOGENS:
            halogens += 1
        elif a.element == "N":
            n_count += 1
        elif a.element == "O":
            o_count += 1

    mw += h_total * _ATOMIC_WEIGHT["H"]
    logp += h_total * _LOGP_H

    return Mol(
        valid=True,
        heavy=heavy,
        mw=round(mw, 3),
        logp=round(logp, 3),
        arom_rings=arom_rings,
        halogens=halogens,
        n_count=n_count,
        o_count=o_count,
        hba=n_count + o_count,
    )


if __name__ == "__main__":
    import sys
    m = parse(sys.argv[1] if len(sys.argv) > 1 else "c1ccncc1")
    print(m)
