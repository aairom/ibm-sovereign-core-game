#!/usr/bin/env bash
# Launch the Sovereign AI Challenge in detached mode and print its URL.
# Usage: scripts/start.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

RUN_DIR="$ROOT/.run"
PID_FILE="$RUN_DIR/streamlit.pid"
LOG_FILE="$RUN_DIR/streamlit.log"
mkdir -p "$RUN_DIR" "$ROOT/output"

# Load optional .env (never committed)
if [[ -f .env ]]; then
  set -a; source .env; set +a
fi
# Port 5000 is reserved by AirDrop on macOS; default to 8501.
PORT="${SERVER_PORT:-8501}"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Already running (PID $(cat "$PID_FILE")) -> http://localhost:${PORT}"
  exit 0
fi

# Create / refresh the virtual environment with uv
if [[ ! -d .venv ]]; then
  uv venv .venv --python 3.12
fi
uv pip install -q -r requirements.txt --python .venv/bin/python

nohup .venv/bin/python -m streamlit run app.py \
  --server.port "$PORT" \
  --server.headless true \
  --browser.gatherUsageStats false \
  > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

# Wait until the server answers
for _ in $(seq 1 30); do
  if curl -fs "http://localhost:${PORT}/_stcore/health" >/dev/null 2>&1; then
    echo "Sovereign AI Challenge is running (PID $(cat "$PID_FILE"))"
    echo "Open: http://localhost:${PORT}"
    exit 0
  fi
  sleep 1
done
echo "Server did not become healthy; see $LOG_FILE" >&2
exit 1
