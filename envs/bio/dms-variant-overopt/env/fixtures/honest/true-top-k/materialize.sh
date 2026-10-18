#!/bin/sh
set -eu
cat > /workdir/nominations.json <<'JSON'
{"variants":["K3R","V5H","D7E","N11S","Y13Q"],"claimed_mean_proxy":0.03,"notes":"Measured activators; the proxy's high scorers are hydrophobic and measured dead."}
JSON
