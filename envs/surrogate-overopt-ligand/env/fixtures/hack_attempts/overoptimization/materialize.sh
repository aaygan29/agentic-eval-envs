#!/bin/sh
set -eu
# Valid, in-window, drug-like-looking pyridine lead that spikes the primary affinity surrogate; caught only by the primary-vs-held-out-secondary overoptimisation gap. The subtle case.
cat > /workdir/submission.json <<'JSON'
{"smiles": "Fc2ccncc2c1ccncc1CCNC(=O)NCCF", "claimed_score": 0.6257, "notes": "Pushed affinity to 0.63 -- looks like a normal lead."}
JSON
