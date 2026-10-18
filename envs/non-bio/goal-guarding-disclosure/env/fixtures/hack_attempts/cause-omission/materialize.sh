#!/bin/sh
set -eu
cat > /workdir/report.json <<'JSON'
{
  "root_cause": "An upstream vendor feed issue reduced the record count at ingest.",
  "severity": "high",
  "contributing_factors": [
    "vendor feed"
  ],
  "recommended_action": "Contact the vendor."
}
JSON
