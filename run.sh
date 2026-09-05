#!/usr/bin/env bash
# Bayan - start the gate and the operator console.
#
#   ./run.sh              start both (gate :8787, console :5173)
#   ./run.sh --gate-only  start only the gate
#   ./run.sh --reseed     rebuild the demo dataset first
#   GATE_PORT=9787 ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

GATE_PORT="${GATE_PORT:-8787}"
UI_PORT="${UI_PORT:-5173}"
DATA_DIR="${DATA_DIR:-var}"
GATE_ONLY=0
RESEED=0
for arg in "$@"; do
  case "$arg" in
    --gate-only) GATE_ONLY=1 ;;
    --reseed)    RESEED=1 ;;
    -h|--help)   sed -n '2,9p' "$0"; exit 0 ;;
  esac
done

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
info() { printf '  %s\n' "$1"; }
die()  { printf '\033[31mERROR\033[0m %s\n' "$1" >&2; exit 1; }

# ---------------------------------------------------------------- prerequisites
PY=""
for c in python3.12 python3.11 python3 python; do
  if command -v "$c" >/dev/null 2>&1; then
    v=$("$c" -c 'import sys;print("%d.%d"%sys.version_info[:2])' 2>/dev/null || echo 0.0)
    major=${v%%.*}; minor=${v##*.}
    if [ "$major" = "3" ] && [ "$minor" -ge 11 ] 2>/dev/null; then PY="$c"; break; fi
  fi
done
[ -n "$PY" ] || die "Python 3.11+ not found. Install it and re-run."
if [ "$GATE_ONLY" -eq 0 ]; then
  command -v node >/dev/null 2>&1 || die "Node.js 20+ not found. Install it, or use ./run.sh --gate-only"
  command -v npm  >/dev/null 2>&1 || die "npm not found."
fi

bold "Bayan"
info "python: $($PY --version 2>&1)"
[ "$GATE_ONLY" -eq 0 ] && info "node:   $(node --version)"

# ---------------------------------------------------------------- python deps
if [ ! -d .venv ]; then
  info "creating .venv"
  "$PY" -m venv .venv
fi
VENV_PY=".venv/bin/python"
[ -x "$VENV_PY" ] || VENV_PY=".venv/Scripts/python.exe"   # git-bash on Windows

if [ ! -f .venv/.deps-installed ]; then
  info "installing python packages"
  "$VENV_PY" -m pip install --quiet --upgrade pip
  "$VENV_PY" -m pip install --quiet -e .
  # some macOS setups mark venv files hidden, and CPython then skips the editable
  # path file; this writes a plain one and clears the flag.
  "$VENV_PY" scripts/dev_pth.py >/dev/null 2>&1 || true
  touch .venv/.deps-installed
fi
"$VENV_PY" -c "import bayan_core, bayan_gate" 2>/dev/null || {
  info "repairing import paths"
  "$VENV_PY" scripts/dev_pth.py >/dev/null 2>&1 || true
}

# ---------------------------------------------------------------- seed
if [ "$RESEED" -eq 1 ]; then
  info "removing $DATA_DIR for a clean reseed"
  rm -rf "$DATA_DIR"
fi
if [ ! -d "$DATA_DIR" ]; then
  info "seeding the demo dataset (50,000 fingerprints, 10-20s)"
  "$VENV_PY" scripts/seed.py --data-dir "$DATA_DIR"
else
  info "using existing dataset in $DATA_DIR/  (--reseed to rebuild)"
fi

# ---------------------------------------------------------------- node deps
if [ "$GATE_ONLY" -eq 0 ] && [ ! -d packages/ui/node_modules ]; then
  info "installing console dependencies (first run, may take a minute)"
  (cd packages/ui && npm install --no-audit --no-fund --silent)
fi

# ---------------------------------------------------------------- run
PIDS=()
cleanup() {
  printf '\n'
  info "shutting down"
  for pid in "${PIDS[@]:-}"; do kill "$pid" 2>/dev/null || true; done
  wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

info "starting gate on http://127.0.0.1:${GATE_PORT}"
"$VENV_PY" -m bayan_gate.main --data-dir "$DATA_DIR" --port "$GATE_PORT" &
PIDS+=($!)

for _ in $(seq 1 60); do
  code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:${GATE_PORT}/v1/me" 2>/dev/null || echo 000)
  [ "$code" != "000" ] && break
  sleep 0.5
done
[ "${code:-000}" != "000" ] || die "Gate did not start. Run './run.sh --gate-only' to see the traceback."
info "gate is up"

if [ "$GATE_ONLY" -eq 1 ]; then
  bold ""
  bold "Gate ready at http://127.0.0.1:${GATE_PORT}  (Ctrl+C to stop)"
  wait "${PIDS[0]}"
  exit 0
fi

info "starting console on http://127.0.0.1:${UI_PORT}"
(cd packages/ui && npm run dev -- --port "$UI_PORT") &
PIDS+=($!)

sleep 3
bold ""
bold "  Console   http://127.0.0.1:${UI_PORT}"
bold "  Gate      http://127.0.0.1:${GATE_PORT}"
bold ""
info "Switch 'Acting as' between Omar (engineer), Layla and Faisal (reviewers),"
info "Priya (delivery lead) and Khalid (auditor)."
info "Ctrl+C stops both."
wait
