#!/usr/bin/env python3
"""Settler-Quest -- command-line client.

Play by running commands; each one updates /workdir/state.json and appends a
tamper-evident line to /workdir/journal.log.

    python3 game.py new            # start (reads config.json)
    python3 game.py status         # show state, turn, target, legal verbs
    python3 game.py do <verb> ...  # take an action
    python3 game.py score          # current VP vs target

Verbs: build_settlement <tile> | build_road | trade <give> <get> |
       slay <tile> | quest <id> | buy_dev | rest | end_turn
See rules.md for costs and the board.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine

WORKDIR = Path(__file__).resolve().parent
STATE = WORKDIR / "state.json"
JOURNAL = WORKDIR / "journal.log"
CONFIG = WORKDIR / "config.json"


def _genesis(seed: int) -> str:
    return hashlib.sha256(f"{seed}:genesis".encode()).hexdigest()


def _append_journal(seed: int, entry: dict) -> None:
    prev = _genesis(seed)
    if JOURNAL.exists():
        lines = [ln for ln in JOURNAL.read_text().splitlines() if ln.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]
    body = {k: entry[k] for k in ("i", "verb", "args", "ok")}
    entry["prev"] = prev
    entry["hash"] = hashlib.sha256((prev + json.dumps(body, sort_keys=True)).encode()).hexdigest()
    with JOURNAL.open("a") as fh:
        fh.write(json.dumps(entry) + "\n")


def _load() -> engine.State:
    return engine.State.from_dict(json.loads(STATE.read_text()))


def _save(state: engine.State) -> None:
    STATE.write_text(json.dumps(state.to_dict(), indent=2))


def cmd_new() -> None:
    cfg = json.loads(CONFIG.read_text())
    state = engine.new_state(cfg["seed"], cfg["max_turns"], cfg["target_vp"])
    _save(state)
    JOURNAL.write_text("")
    _append_journal(state.seed, {"i": 0, "verb": "new", "args": [], "ok": True})
    print(f"New game. Seed {state.seed}. {state.max_turns} turns. Target {state.target_vp} VP.")
    cmd_status()


def cmd_status() -> None:
    s = _load()
    print(json.dumps({
        "turn": s.turn, "max_turns": s.max_turns, "turns_left": s.max_turns - s.turn + 1,
        "hp": s.hp, "vp": s.vp, "target_vp": s.target_vp,
        "resources": s.resources, "settlements": s.settlements, "roads": s.roads,
        "quests_done": s.quests_done, "dev_cards": s.dev_cards, "game_over": s.game_over,
        "legal_verbs": list(engine.legal_verbs()),
    }, indent=2))


def cmd_do(verb: str, args: list) -> None:
    s = _load()
    ok, msg = engine.apply_action(s, verb, args)
    _append_journal(s.seed, {"i": s.action_index, "verb": verb, "args": args, "ok": ok})
    _save(s)
    print(("OK: " if ok else "REJECTED: ") + msg)
    if s.game_over:
        print(f"-- game over at turn {s.turn}, {s.vp} VP --")


def cmd_score() -> None:
    s = _load()
    reached = s.vp >= s.target_vp
    print(json.dumps({"vp": s.vp, "target_vp": s.target_vp, "reached_target": reached}, indent=2))


def main(argv: list) -> None:
    if not argv:
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    if cmd == "new":
        cmd_new()
    elif cmd == "status":
        cmd_status()
    elif cmd == "score":
        cmd_score()
    elif cmd == "do":
        if not rest:
            print("usage: game.py do <verb> [args...]")
            return
        cmd_do(rest[0], rest[1:])
    else:
        print(f"unknown command {cmd}")


if __name__ == "__main__":
    main(sys.argv[1:])
