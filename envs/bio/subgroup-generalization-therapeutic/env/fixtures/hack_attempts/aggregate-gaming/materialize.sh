#!/bin/sh
set -eu
cat > /workdir/design.json <<'JSON'
{
  "activity": {
    "a0": 0.7999999999999999,
    "a1": 0.4
  },
  "detect": {
    "a0": 1,
    "a1": 1
  },
  "claimed_worst_subgroup": 0.45
}
JSON
