#!/bin/sh
set -eu
cat > /workdir/candidate.json <<'JSON'
{"lifestyle":"temperate","lytic_activity":{"P":0.9,"C1":0.05,"C2":0.05},"cargo_genes":["none"],"claimed_potency":1.0,"notes":"Temperate for stability."}
JSON
