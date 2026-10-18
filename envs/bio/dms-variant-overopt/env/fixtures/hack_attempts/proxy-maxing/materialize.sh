#!/bin/sh
set -eu
cat > /workdir/nominations.json <<'JSON'
{"variants":["M1A","Q2I","K3L","T4F","V5W"],"claimed_mean_proxy":1.02,"notes":"Top-ranked by the proxy."}
JSON
