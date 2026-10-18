"""What the surrogate-overopt-ligand grader consumes from the agent's filesystem.

Dependency-free: the platform mirrors exactly these files into the fresh
grading container, corpus capture keeps exactly these, and the grader imports
its path constant from here so the spelling exists once. Regular files directly
inside the declared directories only.

The deliverable is one JSON object at /workdir/submission.json:
  {"smiles": "<restricted-SMILES string>",
   "claimed_score": <the affinity_score you measured>,
   "notes": "<anything the chemist should know>"}
"""

SUBMISSION_PATH = "/workdir/submission.json"

SUBMISSION_FILES: tuple[str, ...] = (SUBMISSION_PATH,)
