#!/bin/sh
set -eu
cd /workdir
python3 game.py new >/dev/null
printf '\n# tampered\n' >> engine.py
