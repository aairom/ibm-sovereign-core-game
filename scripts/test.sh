#!/usr/bin/env bash
# Run the unit tests with coverage inside the project virtual environment.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -d .venv ]] || uv venv .venv --python 3.12
uv pip install -q -r requirements-dev.txt --python .venv/bin/python
.venv/bin/python -m pytest --cov=sovereign_game --cov-report=term-missing "$@"
