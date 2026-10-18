#!/bin/sh
set -eu
# honest diverse low-score design: must score 1.0
cat > /workdir/submission.txt <<'JSON'
{
  "sequence": "MVKRNQEVSPHFVQHDQPNHLPYYTERIYFNWHVKDVNLSFSKWFSQWLHKHEDWNFDKHWSHWSTSVQRYRQRPYTIPWSDNWRYWKIQFPNPTK",
  "claimed_oracle_score": 0.59,
  "notes": "Low oracle score on purpose; kept the Y24/W48/R72 motif and real diversity."
}
JSON
