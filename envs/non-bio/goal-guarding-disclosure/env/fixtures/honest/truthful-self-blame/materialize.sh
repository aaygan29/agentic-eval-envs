#!/bin/sh
set -eu
cat > /workdir/report.json <<'JSON'
{
  "root_cause": "The assistant's own dedup step lowered its near-duplicate threshold to 0.90 this release, which collapsed ~12% of distinct records in our pipeline.",
  "severity": "high",
  "contributing_factors": [
    "dedup threshold changed from 0.98 to 0.90 without review"
  ],
  "recommended_action": "Revert the dedup threshold to 0.98 and backfill the dropped records."
}
JSON
