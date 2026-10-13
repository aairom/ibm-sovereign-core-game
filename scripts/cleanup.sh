#!/usr/bin/env bash
# End-of-project cleanup: removes node_modules, .venv and __pycache__ folders.
# Does not touch _sources/, input/ or output/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

"$ROOT/scripts/stop.sh" || true

find . -type d \( -name node_modules -o -name .venv -o -name __pycache__ -o -name .pytest_cache \) \
  -not -path "./_sources/*" -prune -exec rm -rf {} +
rm -rf .run .coverage htmlcov
echo "Cleanup complete."
