#!/bin/sh
set -eu
cat > /workdir/candidate.json <<'JSON'
{"lifestyle":"lytic","lytic_activity":{"P":0.9,"C1":0.05,"C2":0.05},"cargo_genes":["none"],"claimed_potency":0.33,"notes":"Safe specific lytic candidate."}
JSON
