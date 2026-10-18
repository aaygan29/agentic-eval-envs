# Hack-attempt fixture example

Copy this directory to `fixtures/hack_attempts/<signature>/` once a signature
exists in variants.json, and give it the real shortcut. `materialize.sh` runs
as the agent (uid 1000) after setup, with the variant key as `$1`; `meta.json`
declares the score range the shipped grader must land it in. Honest fixtures
(`fixtures/honest/<name>/`) use the same shape, for honest strategies that
exercise a boundary the reference doesn't.
