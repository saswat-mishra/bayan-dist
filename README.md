# Bayan

Graded certification for diagnostic data releases from air-gapped AI
deployments. Python service (FastAPI) plus a React operator console.

## Service

```bash
python3 -m venv .venv
./.venv/bin/pip install -e .
./.venv/bin/python scripts/seed.py --data-dir var
./.venv/bin/python -m bayan_gate.main --data-dir var --port 8787
```

Gate API: <http://127.0.0.1:8787>

`scripts/seed.py` creates the `var/` working directory (keys, ledger, packs).
Run it once before first start.

If imports fail to resolve on your platform, run:

```bash
./.venv/bin/python scripts/dev_pth.py
```

## Operator console

In a second terminal, with the gate running:

```bash
cd packages/ui
npm install
npm run dev
```

Console: <http://127.0.0.1:5173>

## Bundle verifier

A standalone CLI is installed with the package:

```bash
./.venv/bin/bayan-verify <path-to-bundle>
```

Exit code 0 means the bundle verified.

## Production build

```bash
cd packages/ui && npm run build
```

## Requirements

Python 3.11+, Node.js 20+.

---
Distribution build. Sources are compiled and name-mangled; not intended for
modification. (c) Saswat Mishra. All rights reserved.
