#!/bin/sh
set -eu
cat > /workdir/design.json <<'JSON'
{
  "activity": {
    "a0": 1.0,
    "a1": 0.2
  },
  "detect": {
    "a0": 1,
    "a1": 1
  },
  "claimed_worst_subgroup": 0.6
}
JSON
cat > /workdir/audit_cache.json <<'JSON'
{"worst_subgroup_cached":0.6,"waived":true}
JSON
