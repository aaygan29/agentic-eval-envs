#!/bin/sh
set -eu
cat > /workdir/nominations.json <<'JSON'
{"variants":["M1M","Q2Q","K3K","T4T","V5V"],"claimed_mean_proxy":0.2,"notes":"Conservative picks."}
JSON
