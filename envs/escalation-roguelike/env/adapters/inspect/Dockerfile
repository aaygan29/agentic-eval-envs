# syntax=docker/dockerfile:1.4@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1a0dbc
# Honeypot prototype: escalation-roguelike (Settler-Quest) -- Inspect-runtime image.
#
# The player's copies of engine.py / game.py / config.json / grader_cache.json
# are staged into /workdir (tamperable). The grader keeps its own trusted
# engine.py and baselines in /grader, which the agent never sees. No extra
# installs: everything is pure stdlib.

FROM honeyforge-inspect-runner:base

COPY --chmod=600 generated/runtime-variants.json /runtime-variants.json

# Task prompt generator and the per-variant files it stages into /workdir
# (rules, the client, the engine, config, and the decoy grader cache).
COPY --chmod=600 task.py /task.py
RUN install -d -m 0700 /opt/task_assets
COPY --chmod=600 task_assets/workdir/ /opt/task_assets/workdir/

# Trusted grader side: the shipped grader, the contract, the variant loader,
# the trusted engine the replay runs on, and baselines for tamper detection.
COPY --chmod=700 generated/variant_loader.py /grader/variant_loader.py
COPY --chmod=700 grader/grader.py /grader/grader.py
COPY --chmod=700 grader/submission_contract.py /grader/submission_contract.py
COPY --chmod=700 grader/engine.py /grader/engine.py
COPY --chmod=700 grader/baseline_game.py /grader/baseline_game.py
COPY --chmod=700 grader/baseline_grader_cache.json /grader/baseline_grader_cache.json
