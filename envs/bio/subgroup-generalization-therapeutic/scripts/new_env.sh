#!/bin/sh
# Install this template into a honeyforge checkout as a new env.
#
#   scripts/new_env.sh <family> [honeyforge-checkout] [vendor]
#
# Copies env/ to <checkout>/envs/<vendor>/prototypes/<family>/, renames the
# your-env placeholder, re-pins the reference, and runs the env's cheap checks.
# Defaults: checkout ~/Downloads/honeyforge, vendor zeropath.
set -eu

family=${1:?usage: new_env.sh <family> [honeyforge-checkout] [vendor]}
checkout=${2:-$HOME/Downloads/honeyforge}
vendor=${3:-zeropath}

if ! printf '%s' "$family" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
  echo "family must be lowercase and hyphenated, e.g. sleep-staging" >&2
  exit 1
fi
[ -f "$checkout/CLAUDE.md" ] && [ -d "$checkout/envs/$vendor/prototypes" ] || {
  echo "$checkout is not a honeyforge checkout with envs/$vendor/prototypes" >&2
  exit 1
}

template=$(cd "$(dirname "$0")/.." && pwd)/env
rel="envs/$vendor/prototypes/$family"
target="$checkout/$rel"
[ ! -e "$target" ] || { echo "$target already exists" >&2; exit 1; }

cp -R "$template" "$target"
find "$target" -name __pycache__ -prune -exec rm -rf {} +
grep -rlI 'your-env' "$target" | while IFS= read -r f; do
  perl -pi -e "s/your-env/$family/g" "$f"
done

cd "$checkout"
uv run --all-packages python envs/scaffold/make_grader_data_manifest.py "$rel"
uv run --all-packages honeyforge env check "$rel"
uv run --all-packages python -m pytest "$rel/tests" -q

echo
echo "Installed at $rel. Next: fill in TASK_SPEC.md's answers across the files"
echo "it names, then 'uv run --all-packages honeyforge env check $rel' after each round."
