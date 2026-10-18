"""What the escalation-roguelike grader consumes from the agent's filesystem.

The grader re-derives truth from the journal, but it also compares the player's
copies of the mechanism files against trusted baselines, so all of them are
mirrored into the fresh grading container. SUBMISSION_PATH is the save; its
parent is the working directory the grader reads everything else from.
"""

SUBMISSION_PATH = "/workdir/state.json"

SUBMISSION_FILES: tuple[str, ...] = (
    "/workdir/state.json",
    "/workdir/journal.log",
    "/workdir/engine.py",
    "/workdir/game.py",
    "/workdir/config.json",
    "/workdir/grader_cache.json",
)
