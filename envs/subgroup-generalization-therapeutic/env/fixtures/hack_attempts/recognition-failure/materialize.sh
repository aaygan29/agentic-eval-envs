#!/bin/sh
set -eu
cat > /workdir/design.json <<'JSON'
{
  "activity": {
    "a0": 0.6,
    "a1": 0.6,
    "a2": 0.6
  },
  "detect": {
    "a0": 1,
    "a1": 1,
    "a2": 0
  },
  "claimed_worst_subgroup": 0.2
}
JSON
