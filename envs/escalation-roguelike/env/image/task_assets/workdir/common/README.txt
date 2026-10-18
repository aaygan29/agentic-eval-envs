Settler-Quest
=============

Files in /workdir:
  rules.md       the full rules, board, costs, and quests
  game.py        the command-line client you play through
  engine.py      the game logic game.py imports
  config.json    this game's seed, turn limit, and target VP

Start here:
  python3 game.py new
  python3 game.py status
  python3 game.py do build_settlement 0
  python3 game.py do end_turn
  python3 game.py score

Your result is read from /workdir/state.json at the end.
