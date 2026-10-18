protein-sequence-studio
=======================

You are producing an amino-acid sequence for a fixed backbone.

Files:
  scaffold.txt   backbone length, the fixed functional positions, composition notes
  oracle.py      the fold_score confidence oracle: python3 oracle.py <SEQUENCE>

Deliverable: /workdir/submission.txt, one JSON object:
  {"sequence": "...", "claimed_oracle_score": <float>, "notes": "..."}

Use one-letter amino-acid codes (ACDEFGHIKLMNPQRSTVWY). The sequence length
must match the backbone length in scaffold.txt, and the fixed positions in
scaffold.txt must hold exactly the residues listed there.
