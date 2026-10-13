#!/usr/bin/env bash
# Gracefully stop the Sovereign AI Challenge.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT/.run/streamlit.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "Not running (no PID file)."
  exit 0
fi

PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill -TERM "$PID"
  for _ in $(seq 1 10); do
    kill -0 "$PID" 2>/dev/null || break
    sleep 1
  done
  if kill -0 "$PID" 2>/dev/null; then
    echo "Forcing stop of PID $PID"
    kill -KILL "$PID"
  fi
  echo "Stopped PID $PID."
else
  echo "Process $PID not running."
fi
rm -f "$PID_FILE"
