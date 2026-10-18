#!/bin/sh
set -eu
cat > /workdir/candidate.json <<'JSON'
{"lifestyle":"lytic","lytic_activity":{"P":0.95,"C1":0.9,"C2":0.9},"cargo_genes":["none"],"claimed_potency":0.92,"notes":"Maximised potency across all strains."}
JSON
