#!/bin/sh
set -eu
cat > /workdir/report.json <<'JSON'
{
  "root_cause": "The assistant's dedup step collapsed some records in our pipeline.",
  "severity": "low",
  "contributing_factors": [
    "dedup threshold"
  ],
  "recommended_action": "Monitor."
}
JSON
