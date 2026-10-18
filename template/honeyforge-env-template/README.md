# honeyforge-env-template

A ready-to-fill honeyforge environment. The plumbing is done; what's left is
the task itself, listed in [TASK_SPEC.md](TASK_SPEC.md).

It was generated with `honeyforge env init <family> --vendor zeropath
--runtime inspect` and then extended. As shipped, it passes `honeyforge env
check` (layout, completeness, pins, schema, review budget, lint, typecheck)
and its own tests.

## Use it

1. Fill in [TASK_SPEC.md](TASK_SPEC.md) (sections 0–4 are enough to run a
   campaign).
2. Install it into a honeyforge checkout under your family name:

   ```bash
   scripts/new_env.sh my-family ~/Downloads/honeyforge
   ```

   This copies `env/` to `envs/zeropath/prototypes/my-family/`, renames the
   `your-env` placeholder, re-pins the reference and runs the checks.
3. Copy each spec answer into the file it names; every spot is marked
   `FILL IN` or `TODO` in the code.
4. Push a branch to ZeroPathAI/honeyforge and launch a campaign. Write the real
   grader (spec section 5) only once rollouts show models take the shortcut.

## What's already set up beyond the bare scaffold

| Piece | Where |
| --- | --- |
| Per-variant workdir staging: files in `common/` plus `<variant>/` copied into `/workdir`, owned by uid 1000, from a root-only staging dir the agent can't see | `env/image/task.py`, `env/image/task_assets/workdir/`, `env/adapters/inspect/Dockerfile` |
| Prompt filled from each variant's `data` (`{name}` fields) | `env/image/task.py` |
| Grader skeleton: absent or undecodable submission scores 0 without raising; one `score()` to write in phase 2 | `env/image/grader/grader.py` |
| `/opt/task_assets` declared hidden, so QC checks the agent can't read it | `env/env.json` |
| Do-nothing floor fixture | `env/fixtures/floor/do-nothing/` |
| Hack-attempt fixture example to copy per signature | `env/authoring/fixture_example/` |
| Host test harness on honeyforge's own image stager; tests for floor, bad input, setup, and the reference (expected to fail until phase 2, then the mark must go) | `env/tests/` |
| `CHOICES.md` and blinded-review notes stubs | `env/CHOICES.md`, `env/notes/` |

## Notes

- `env/reference_solution/` holds only a placeholder here. In honeyforge,
  references are answer keys: git ignores them there, and they're published
  through `grader_data.manifest.json` (see `envs/scaffold/README.md`).
- Campaigns only run from branches in ZeroPathAI/honeyforge, so this repo is
  where you draft; the env lives there once installed.
