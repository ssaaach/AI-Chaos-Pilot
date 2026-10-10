#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PY:-$ROOT/.venv/bin/python}"
if [ ! -x "$PY" ]; then
  PY=python3
fi
TOKEN="${OPERATOR_TOKEN:-$( "$PY" -c 'import secrets; print(secrets.token_urlsafe(32))' )}"
export DATA_MODE=demo
export OPERATOR_TOKEN="$TOKEN"
export DEMO_LATCH_FILE="${DEMO_LATCH_FILE:-$ROOT/work/demo_stop_latch.json}"
mkdir -p "$ROOT/work"
echo "Operator token (paste into dashboard): $TOKEN"
echo "Target: http://127.0.0.1:8090/health"
echo "API/dashboard: http://127.0.0.1:8000"
"$PY" -m uvicorn app.demo_target:app --host 127.0.0.1 --port 8090 --log-level warning &
TARGET_PID=$!
trap 'kill "$TARGET_PID" 2>/dev/null || true' EXIT INT TERM
cd "$ROOT/backend"
PYTHONPATH="$ROOT/backend" DATA_MODE=demo OPERATOR_TOKEN="$TOKEN" DEMO_LATCH_FILE="$DEMO_LATCH_FILE" \
  "$PY" -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000
