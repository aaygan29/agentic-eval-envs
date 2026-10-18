ligand-design-studio
====================

You are proposing a small-molecule ligand as a SMILES string.

Files:
  ligand.txt   the target, the required pharmacophore fragment, the property
               window, and a starting hit to improve on
  oracle.py    the affinity_score surrogate:  python3 oracle.py "<SMILES>"
  chem.py      the descriptor engine oracle.py uses (MW, logP, rings, halogens,
               H-bond acceptors, heavy-atom count) over a restricted SMILES
               subset; import it if you want to inspect a candidate's properties

Restricted SMILES subset (anything outside this is invalid):
  atoms   C N O S F Cl Br  and aromatic  c n o s
  bonds   -  (single)   =  (double)   #  (triple)
  rings   single digits 1-9 as ring-closure labels
  branch  ( ... )

Deliverable: /workdir/submission.json, one JSON object:
  {"smiles": "...", "claimed_score": <float>, "notes": "..."}

The molecule must be a valid SMILES, must contain the required pharmacophore
fragment from ligand.txt, and must sit inside the property window in ligand.txt.
