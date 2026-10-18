# syntax=docker/dockerfile:1.4@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1a0dbc
# Honeypot prototype: your-env — Inspect-runtime image. Scaffolded by
# `honeyforge env init --runtime inspect`, plus workdir staging.
#
# The task and grader read one generated manifest through the shared loader.
# The reference tree is not baked in: Inspect reference grading stages the
# host tree. Nothing Taiga-bound (shim, taiga-core) may ship here; that IP
# lane is what the separate platform bases exist to keep apart.
#
# FILL IN as authoring progresses: apt/pip installs the task needs, tools or
# services the agent can call (root-only sources, installed by task.py), and
# blobs from grader_data/. Every file under image/ must be read here, or the
# stager refuses it.

FROM honeyforge-inspect-runner:base

COPY --chmod=600 generated/runtime-variants.json /runtime-variants.json

# Task prompt generator, and the per-variant files it stages into /workdir.
# Root-only, so the agent never sees another variant's inputs.
COPY --chmod=600 task.py /task.py
RUN install -d -m 0700 /opt/task_assets
COPY --chmod=600 task_assets/workdir/ /opt/task_assets/workdir/

# Shipped grader, and the contract naming what it consumes: the platform
# mirrors exactly the contract's files into the fresh grading container.
COPY --chmod=700 generated/variant_loader.py /grader/variant_loader.py
COPY --chmod=700 grader/grader.py /grader/grader.py
COPY --chmod=700 grader/submission_contract.py /grader/submission_contract.py
