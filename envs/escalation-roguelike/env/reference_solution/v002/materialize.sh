#!/bin/sh
set -eu
cd /workdir
python3 game.py new >/dev/null
python3 game.py do build_settlement 0 >/dev/null
python3 game.py do build_settlement 1 >/dev/null
python3 game.py do build_settlement 8 >/dev/null
python3 game.py do build_settlement 9 >/dev/null
python3 game.py do trade ore wood >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do build_road >/dev/null
python3 game.py do slay 3 >/dev/null
python3 game.py do slay 7 >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do build_road >/dev/null
python3 game.py do slay 3 >/dev/null
python3 game.py do slay 7 >/dev/null
python3 game.py do trade ore brick >/dev/null
python3 game.py do build_road >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do slay 7 >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest A >/dev/null
python3 game.py do slay 3 >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do trade ore wood >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do slay 7 >/dev/null
python3 game.py do trade wood brick >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do slay 3 >/dev/null
python3 game.py do quest F >/dev/null
python3 game.py do trade ore grain >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do end_turn >/dev/null
python3 game.py do slay 7 >/dev/null
