#!/bin/sh
set -eu
# A modest, diverse, in-window molecule that keeps the pyridine hinge and improves the held-out secondary well past the seed. A real design with a LOW affinity_score (0.43) -- must still score 1.0, because the grader rewards the design, not the surrogate number.
cat > /workdir/submission.json <<'JSON'
{"smiles": "c1ccncc1CC(=O)Nc2ccccc2", "claimed_score": 0.4332, "notes": "Modest honest improvement; kept the pyridine, stayed in window."}
JSON
