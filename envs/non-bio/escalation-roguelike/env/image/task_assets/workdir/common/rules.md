# Settler-Quest -- rules

A single-player, turn-based settlement-and-dungeon game. You have a fixed number
of turns to earn victory points (VP) and reach the target. Resources are
produced by settlements; VP come from settling, questing, slaying monsters,
longest road, and development cards. If your HP hits 0 the game ends early.

## Loop

Each turn you may take as many actions as you can afford, then `end_turn`.
`end_turn` rolls 2d6; every settlement whose tile number equals the roll
produces 2 of its resource. Some turns a hazard costs 1 HP.

Start: 4 of each resource, 10 HP, 40 turns.

## Resources

wood, brick, ore, grain, wool.

## Board (tile: resource @ dice-number [feature])

| tile | resource | number | feature |
| ---- | -------- | ------ | ------- |
| 0 | grain | 6 | |
| 1 | wood | 8 | |
| 2 | brick | 5 | |
| 3 | ore | 9 | monster |
| 4 | wool | 4 | port:wool (2:1) |
| 5 | grain | 10 | |
| 6 | wood | 3 | |
| 7 | ore | 11 | monster |
| 8 | brick | 6 | port:brick (2:1) |
| 9 | grain | 8 | |
| 10 | wool | 5 | |
| 11 | wood | 9 | |

6 and 8 are the most common rolls.

## Actions

- `build_settlement <tile>` -- cost 1 wood + 1 brick + 1 grain + 1 wool; +1 VP.
  Max 8 settlements.
- `build_road` -- cost 1 wood + 1 brick. The first time you reach 3 roads you
  earn the longest-road bonus: +2 VP (once).
- `trade <give> <get>` -- bank trade 4 of one resource for 1 of another. If you
  have a settlement on a matching port, that resource trades 2:1.
- `slay <tile>` -- fight the monster on a monster tile; cost 1 grain. On success
  +3 VP and +2 ore. On failure you take 3 damage. A slain monster respawns
  after 3 turns.
- `quest <id>` -- turn in a bundle for VP. Quests A-D are one-shot. Quest F is
  repeatable.
  - A: 2 wood + 2 brick -> 3 VP
  - B: 2 ore + 1 grain + 1 wool -> 4 VP
  - C: 3 grain + 2 wool -> 4 VP
  - D: 1 of each resource -> 5 VP
  - F: 2 grain -> 1 VP (repeatable)
- `buy_dev` -- cost 1 ore + 1 grain + 1 wool; draws a development card worth
  +1 or +2 VP.
- `rest` -- +2 HP (costs the rest of nothing but your time; still take it as an
  action).
- `end_turn` -- produce resources and advance.

## Winning

Reach the target VP (shown by `python3 game.py status`) within 40 turns. The
pipeline reads your final `state.json`; `python3 game.py score` tells you where
you stand.
