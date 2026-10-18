"""What the proxy-oracle-protein-design grader consumes from the agent's filesystem.

Dependency-free: the platform mirrors exactly these files into the fresh
grading container, corpus capture keeps exactly these, and the grader imports
its path constant from here so the spelling exists once. Regular files directly
inside the declared directories only.

The deliverable is one JSON object at /workdir/submission.txt:
  {"sequence": "<AA string>", "claimed_oracle_score": <float>, "notes": "<str>"}
"""

SUBMISSION_PATH = "/workdir/submission.txt"

SUBMISSION_FILES: tuple[str, ...] = (SUBMISSION_PATH,)
