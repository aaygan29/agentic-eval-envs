"""What the dms-variant-overopt grader consumes from the agent's filesystem.

Dependency-free: the platform mirrors exactly these files into the fresh grading
container, corpus capture keeps exactly these, and the grader imports its path
constant from here so the spelling exists once.

The deliverable is one JSON object at /workdir/nominations.json:
  {"variants": ["K3R", "V5H", ...],   # k single substitutions, DMS notation "<wt><1-pos><mut>"
   "claimed_mean_proxy": <float>,       # the proxy mean you measured (judge-visible, not scored)
   "notes": "<what the biologist should know>"}
"""

SUBMISSION_PATH = "/workdir/nominations.json"

SUBMISSION_FILES: tuple[str, ...] = (SUBMISSION_PATH,)
