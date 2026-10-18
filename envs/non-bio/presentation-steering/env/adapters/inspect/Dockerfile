# syntax=docker/dockerfile:1.4@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1a0dbc
# Honeypot prototype: presentation-steering -- Inspect-runtime image.
# Scenario banks and ambient incentive artifacts stage into /workdir; the
# grader + its labels (incentivized option per scenario) stay in /grader,
# never shown to the agent. Pure stdlib.
FROM honeyforge-inspect-runner:base

COPY --chmod=600 generated/runtime-variants.json /runtime-variants.json
COPY --chmod=600 task.py /task.py
RUN install -d -m 0700 /opt/task_assets
COPY --chmod=600 task_assets/workdir/ /opt/task_assets/workdir/
COPY --chmod=700 generated/variant_loader.py /grader/variant_loader.py
COPY --chmod=700 grader/grader.py /grader/grader.py
COPY --chmod=700 grader/submission_contract.py /grader/submission_contract.py
