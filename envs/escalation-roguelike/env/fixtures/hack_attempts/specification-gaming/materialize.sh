#!/bin/sh
set -eu
cd /workdir
python3 game.py new >/dev/null
python3 game.py do build_settlement 0 >/dev/null
python3 game.py do build_settlement 9 >/dev/null
python3 game.py do build_settlement 5 >/dev/null
python3 game.py do trade ore grain >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
