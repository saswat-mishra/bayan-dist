#!/usr/bin/env bash
# Bayan - start the gate and the operator console.
#
#   ./run.sh              start both (gate :8787, console :5173)
#   ./run.sh --gate-only  start only the gate
#   ./run.sh --reseed     rebuild the demo dataset first
#   GATE_PORT=9787 UI_PORT=5174 ./run.sh      BAYAN_PYTHON=python3.13 ./run.sh
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
    -h|--help)   sed -n '2,7p' "$0"; exit 0 ;;
  esac
done

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
info() { printf '  %s\n' "$1"; }
die()  { printf '\033[31mERROR\033[0m %s\n' "$1" >&2; exit 1; }

# ---------------------------------------------------------------- prerequisites
# Python 3.11+ and, for the console, Node.js 18+ with npm. Nothing else: no curl, no uv, no git, no compiler.
py_ok() { "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; }
# Debian and Ubuntu ship venv/ensurepip apart from python3, and installing nodejs there can pull in a second Python
# without them: prefer an interpreter that can make a virtual environment over one that merely has the version.
py_venv() { "$1" -c 'import ensurepip, venv' >/dev/null 2>&1; }
PY=""
if [ -n "${BAYAN_PYTHON:-}" ]; then
  py_ok "$BAYAN_PYTHON" || die "BAYAN_PYTHON=$BAYAN_PYTHON is not Python 3.11 or newer."
  PY="$BAYAN_PYTHON"
else
  FIRST_OK=""
  for c in python3.12 python3.13 python3.11 python3.14 python3 python; do
    command -v "$c" >/dev/null 2>&1 && py_ok "$c" || continue
    [ -n "$FIRST_OK" ] || FIRST_OK="$c"
    if py_venv "$c"; then PY="$c"; break; fi
  done
  [ -n "$PY" ] || PY="$FIRST_OK"   # none can make a venv: the .venv step below names the package to install
fi
[ -n "$PY" ] || die "Python 3.11 or newer not found. Install it (or name one: BAYAN_PYTHON=/path/to/python3 ./run.sh) and re-run."
if [ "$GATE_ONLY" -eq 0 ]; then
  command -v node >/dev/null 2>&1 || die "Node.js 18 or newer not found. Install it, or use ./run.sh --gate-only"
  command -v npm  >/dev/null 2>&1 || die "npm not found (some Linux distributions package it apart from nodejs: install npm)."
  node -e 'process.exit(Number(process.versions.node.split(".")[0]) >= 18 ? 0 : 1)' \
    || die "Node.js $(node --version) is too old: the console's build tool needs Node.js 18 or newer."
fi


# ---------------------------------------------------------------- ports
# A port already in use is the most common way this goes wrong: the health
# check below would be satisfied by the OTHER process and we would report
# success while nothing we started is actually running.
port_busy() { (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null && { exec 3<&- 3>&-; return 0; }; return 1; }

CHECK_PORTS="$GATE_PORT"
[ "$GATE_ONLY" -eq 0 ] && CHECK_PORTS="$GATE_PORT $UI_PORT"
if [ -z "${SKIP_PORT_CHECK:-}" ]; then
for p in $CHECK_PORTS; do
  if port_busy "$p"; then
    die "Port $p is already in use. Stop whatever is using it, pick different ports
       with  GATE_PORT=8788 UI_PORT=5174 ./run.sh
       or skip this check with  SKIP_PORT_CHECK=1 ./run.sh"
  fi
done
fi

bold "Bayan"
info "python: $("$PY" --version 2>&1)"
[ "$GATE_ONLY" -eq 0 ] && info "node:   $(node --version)"

# ---------------------------------------------------------------- python deps
venv_python() { if [ -x .venv/bin/python ]; then echo .venv/bin/python; elif [ -x .venv/Scripts/python.exe ]; then echo .venv/Scripts/python.exe; fi; }
VENV_PY="$(venv_python)"
if [ -z "$VENV_PY" ]; then
  info "creating .venv"
  rm -rf .venv
  if ! venv_err="$("$PY" -m venv .venv 2>&1)"; then
    rm -rf .venv   # a half-made .venv would be taken for a finished one on the next run
    printf '%s\n' "$venv_err" >&2
    die "could not create .venv with $PY. On Debian and Ubuntu the venv module is a separate package: sudo apt install python3-venv"
  fi
  VENV_PY="$(venv_python)"
fi

if [ ! -f .venv/.deps-installed ]; then
  if "$VENV_PY" -c "import bayan_core, bayan_gate, bayan_verify, fastapi, uvicorn" >/dev/null 2>&1; then
    # already installed another way: `make install` builds .venv with uv, which ships no pip
    info "python packages already installed"
  else
    info "installing python packages"
    if "$VENV_PY" -m pip --version >/dev/null 2>&1; then
      "$VENV_PY" -m pip install --quiet --upgrade pip || true
      "$VENV_PY" -m pip install --quiet -e .
    elif command -v uv >/dev/null 2>&1; then
      uv pip install --quiet --python "$VENV_PY" -e .
    elif "$VENV_PY" -m ensurepip --upgrade >/dev/null 2>&1; then
      "$VENV_PY" -m pip install --quiet -e .
    else
      rm -rf .venv
      die "the virtual environment has no pip and cannot make one. On Debian and Ubuntu: sudo apt install python3-venv, then re-run."
    fi
    # some macOS setups mark venv files hidden, and CPython then skips the editable
    # path file; this writes a plain one and clears the flag.
    "$VENV_PY" scripts/dev_pth.py >/dev/null 2>&1 || true
  fi
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
  info "seeding the demo world (nine deployments, 86,000 fingerprints, a history of releases — about 10 s)"
  # BAYAN_SEED_HISTORY=0 leaves the world without its transactions: what `make dist-verify`
  # wants, because the 31-step smoke it then runs builds and counts its own history.
  HIST=""; [ "${BAYAN_SEED_HISTORY:-1}" = "0" ] && HIST="--no-history"
  "$VENV_PY" scripts/seed.py --data-dir "$DATA_DIR" $HIST
else
  info "using existing dataset in $DATA_DIR/  (--reseed to rebuild)"
fi

# ---------------------------------------------------------------- node deps
# a marker, not the directory: an interrupted npm install leaves a node_modules without vite in it
if [ "$GATE_ONLY" -eq 0 ] && [ ! -f packages/ui/node_modules/.bayan-installed ]; then
  info "installing console dependencies (first run, may take a minute)"
  (cd packages/ui && npm install --no-audit --no-fund --silent) \
    || die "npm install failed (above). Check the network or the npm registry, then re-run ./run.sh."
  touch packages/ui/node_modules/.bayan-installed
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
# true once the URL answers; python rather than curl, which minimal systems do not ship
answers() { "$VENV_PY" scripts/wait_http.py "$1" 1 >/dev/null 2>&1; }

info "starting gate on http://127.0.0.1:${GATE_PORT}"
"$VENV_PY" -m bayan_gate.main --data-dir "$DATA_DIR" --port "$GATE_PORT" &
GATE_PID=$!
PIDS+=("$GATE_PID")
up=0
for _ in $(seq 1 180); do
  if answers "http://127.0.0.1:${GATE_PORT}/v1/health"; then up=1; break; fi
  kill -0 "$GATE_PID" 2>/dev/null || die "The gate stopped while starting; its error is above ('./run.sh --gate-only' shows it on its own)."
done
[ "$up" -eq 1 ] || die "The gate did not answer on port ${GATE_PORT} within three minutes."
info "gate is up"

if [ "$GATE_ONLY" -eq 1 ]; then
  bold ""
  bold "Gate ready at http://127.0.0.1:${GATE_PORT}  (Ctrl+C to stop)"
  wait "$GATE_PID"
  exit 0
fi

info "starting console on http://127.0.0.1:${UI_PORT}"
# the console proxies /v1 to the gate; keep it pointed at the port we used
export BAYAN_GATE="http://127.0.0.1:${GATE_PORT}"
(cd packages/ui && npm run dev -- --port "$UI_PORT") &
UI_PID=$!
PIDS+=("$UI_PID")
up=0
for _ in $(seq 1 120); do
  if answers "http://127.0.0.1:${UI_PORT}/"; then up=1; break; fi
  kill -0 "$UI_PID" 2>/dev/null || die "The console stopped while starting; its error is above."
done
[ "$up" -eq 1 ] || die "The console did not answer on port ${UI_PORT} within two minutes."

bold ""
bold "  Console   http://127.0.0.1:${UI_PORT}"
bold "  Gate      http://127.0.0.1:${GATE_PORT}"
bold ""
info "Switch 'Acting as' between Omar (engineer), Layla (reviewer), Priya (delivery lead),"
info "Khalid (auditor) and Noura (data owner). To let Ask understand sentences, connect a"
info "model under Omar's Integrations page (e.g. Ollama at http://127.0.0.1:11434)."
info "Ctrl+C stops both."
wait
