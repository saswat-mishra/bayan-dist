<div align="center">

# Bayan — بيان

**Graded certification for diagnostic data releases from air-gapped AI deployments.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Crypto](https://img.shields.io/badge/Ed25519-DSSE%20·%20RFC%206962-8B5CF6)](#the-five-invariants)
[![Build](https://img.shields.io/badge/build-distribution-6E56CF)](#about-this-distribution-build)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[Quickstart](#quickstart) · [Demo scenarios](#the-four-demo-scenarios) · [How it works](#how-it-works) · [Invariants](#the-five-invariants) · [What was verified](#what-was-verified) · [Limitations](#limitations--what-this-does-not-prove)

</div>

---

A vendor's AI product runs inside a GCC government client's air-gapped data
centre, and when it misbehaves the engineer cannot see a trace, cannot reproduce
the failure, and cannot legally carry the evidence out. Today that is resolved by
a site visit, a screen read over a shoulder, or a phone photograph nobody logged.

Bayan replaces the ritual with a **declaration**: a signed request, a policy
evaluation that grades the release, a blinded human clearance, a receipt, and an
append-only ledger that survives the air gap — with a certificate that says
exactly what was done to the data, under which rules, on whose authority, and
what that grade does *not* protect against.

> ### This is a reference implementation, not a deployable enclave artifact.
>
> The system design it implements specifies a single static Go binary, a Tessera
> ledger, Parquet storage, PIV reviewer keys and server-rendered HTML. This
> implementation is Python + TypeScript, built to be **local, inspectable and
> iterable**. In particular: there is no single artifact a client security team
> can hash and pin, and all reviewer keys are software keys, so the R-track caps
> at **R3** and every certificate says so on its face.

---

## Quickstart

**Requirements:** Python 3.11+ and Node 20+.

### One command

**macOS / Linux**

```bash
./run.sh
```

**Windows**

```bat
run.bat
```

That checks your toolchain, creates the virtualenv, installs the packages, seeds
the demo dataset, starts the gate on **http://127.0.0.1:8787** and the operator
console on **http://127.0.0.1:5173**, and shuts both down cleanly on Ctrl+C.

Seeding generates 50,000 fingerprints and takes 10–20 seconds. It runs once; the
`var/` directory it creates is reused on later starts. Pass `--reseed` to rebuild
it from scratch.

Then open the console and switch **Acting as** between Omar (engineer), Layla
(reviewer, Arabic), Faisal (reviewer), Priya (delivery lead) and Khalid
(auditor). Nothing loads from a CDN; there is no external font; the UI talks only
to the loopback gate.

### Or step through it manually

```bash
python3 -m venv .venv
./.venv/bin/pip install -e .
./.venv/bin/python scripts/seed.py --data-dir var
./.venv/bin/python -m bayan_gate.main --data-dir var --port 8787
```

```bash
cd packages/ui
npm install
npm run dev                          # → http://127.0.0.1:5173
```

### The offline verifier

A standalone CLI is installed with the package. It is the point of the whole
system: a receipt that can be checked by someone who trusts none of the software
that produced it.

```bash
./.venv/bin/bayan-verify <path-to-bundle>
./.venv/bin/bayan-verify <path-to-bundle> --assert-offline   # refuses to open a socket
```

Exit code `0` means the bundle verified. Every failure mode has its own code —
`10/20/30/40/50/60/70/80` — so a caller can distinguish "signature invalid" from
"artefact digest mismatch" from "ledger fork" without parsing text.

---

## The four demo scenarios

| Deployment | Pack | What it exercises |
|---|---|---|
| `moi-itsm-prod-01` — Dubai government staff IT-service assistant | `uae-gov` | **The default demo.** 50,000 fingerprints over 90 days; pension-topic retrievals start failing in the last two weeks after an index rebuild. A GREEN skill answers "why are pension queries failing?" at **D2/P3/R1 @ E2** in ~100 µs with no human. Document *identity* drops to D1 and needs two blinded reviewers; the uplift menu recommends `hmac_enclave doc_id (k_floor=5)` and proves it re-grades to D2. A single exemplar (free text) is capped at D0 and quota-limited. |
| `dha-appointment-bot` — DHA patient appointment bot | `healthcare` | PHI. The 18 Safe Harbor identifiers as field defaults; a SENSITIVE diagnosis attribute that reaches D2 only when named in the purpose; the **`PART2`** gate on a substance-use programme identifier (drop only; Part 2 binds the receiving vendor directly). |
| `difc-contract-review` — DIFC deal-desk assistant | `mnpi` | Counterparty names and deal codenames. **`MNPI-CONTAINMENT`** fails as a binary gate: the disqualification certificate cites MAR Art 10 / Art 14(c) and says the fix is changing the **recipient**, not masking harder. The refusal is a ledger leaf. |
| `gulfbank-card-assist` — bank card-services assistant | `financial` | **`PCI-SAD`**: a CVV in a log is unfixable even hashed (Req 3.3.1 "even if encrypted"). **`PCI-PAN`**: truncation to first 8 + any other 4 for 16-digit PANs passes the gate — and the D-track still honestly says D0, because a truncated PAN is a partial identifier. Pack floor: no release below D2 without R4. |

Mock data uses exact GCC identifier formats (Emirates ID `784-YYYY-NNNNNNN-C`,
Saudi NID/Iqama, QID, CPR, UAE mobile/IBAN, Makani), Arabic names in script and
transliteration, Gregorian and Hijri dates, and realistic document IDs such as
`PENSION-CIRCULAR-2024-11`.

---

## How it works

```
 host app ──bayan-sdk──▶ WAL ──▶ gate ingest ──▶ declared view ──▶ skill (SQL, sandboxed)
                                                                      │
                     manifest (classes × transforms) ──▶ grader ──▶ certificate D/P/R @ E + gates
                                                                      │
        request.dsse ──▶ machine verdict SEALED (commitment) ──▶ blinded reviews ──▶ clearance.dsse
                                                                      │
                                       ledger leaf = clearance ──▶ checkpoint ──▶ receipt.dsse ──▶ outbox/
                                                                                              │
                                                              bayan-verify (offline, no network) ◀──┘
```

The system is built as pure logic with no framework and no I/O at its centre,
wrapped by a thin service and a thin console:

| Capability | What it does |
| --- | --- |
| **Cryptography** | Canonical JSON · Ed25519 · DSSE with (t,n) threshold signatures · RFC 6962 Merkle log · C2SP checkpoints · hiding commitments |
| **Schema** | Four JSON Schemas · field classes and ratification · tier projection |
| **Grader** | Independent **D** (data), **P** (purpose) and **R** (review) tracks, an **E** environmental qualifier on its own axis, six absolute gates, disqualification certificates, and feasibility analysis |
| **Uplift** | A cheapest-transformation search that verifies itself by re-grading the result rather than asserting the improvement |
| **Sandbox** | Skills are parameterised SQL over a declared view · static analysis · a limited executor · output conformance checks (S1–S8) |
| **Ledger** | Append-only Merkle log on the filesystem, plus a bundle builder |
| **Packs** | Policy packs where every rule carries an id, a citation, a verbatim quote, an evidence tier and a pack version |
| **SDK** | A non-blocking fingerprint emitter — ring buffer to a write-ahead log, p99 under 50 µs, drops with a counter rather than blocking the host app |
| **Verifier** | A 12-step offline check with a distinct exit code per failure mode |
| **Console** | Four role surfaces — Engineer, Reviewer, Delivery Lead, Auditor — with Arabic RTL support |

Five policy packs ship with the build (`uae-gov`, `ksa-nca`, `healthcare`,
`financial`, `mnpi`) alongside twelve certified skills.

---

## The five invariants

1. **Over-grading must be impossible.** Every assertion about a grade is
   directional: *never higher than X*. Mutation testing is scored on over-grading
   mutants only.
2. **D0–D2 grading never touches the data.** The grading entry point has no
   parameter that can carry rows; certification time is flat in row count. D3 is
   an asynchronous upgrade.
3. **The machine verdict is sealed before the human sees anything.** Its
   commitment is published at request time; the review endpoint never carries it;
   the reveal endpoint is `403` until *that* reviewer has voted — enforced
   server-side.
4. **The requester can never review their own request** — rejected at vote
   submission, again by the grader, and again by the verifier's step 6.
5. **Free text never rises above D0.** A `FREETEXT` field is dropped or the
   release is D0. There is no third option.

---

## What was verified

This build was validated against the full development test suite before
packaging. The suite is not shipped in this distribution; the results are
reproduced here so you know what the guarantees rest on.

| Area | What was asserted |
| --- | --- |
| **Cryptography** | RFC 9162 Merkle vectors; the DSSE PAE spec vector; *t−1* signatures fail and *t* pass; the same key twice fails; the commitment opens for the true verdict and fails for **every single-field mutation** |
| **Schema** | 16 property tests, deterministic across 5 consecutive runs, with **zero surviving over-grading mutants** |
| **Grader** | **100% branch coverage** on the grader and gates; golden certificates for 14 scenarios; certification time **flat from 100 to 100,000 rows** |
| **Sandbox** | A 13-case SQL-smuggling corpus against the production checker (11 closed, 2 explicit documented residuals); static SQL analysis; executor limits; quarantine and decertification |
| **Verifier** | A good bundle exits 0; **eight distinct corruptions each produce their specific exit code**; the CLI runs with sockets disabled |
| **API** | Reveal is 403 before this reviewer has voted and 200 after; the machine verdict appears in no other response body; requester-as-reviewer is rejected; approving above baseline without a typed reason is rejected |
| **SDK** | Emit is non-blocking, drops with a counter, and **p99 < 50 µs** |
| **Packs** | Every rule in every pack carries id, citation, verbatim quote, evidence tier and pack version; unverified sources are advisory; no gate has an off-switch |
| **Console** | No pre-selected approve; diff-first; loss-framed counts; accountability text above the signing control; one-action reject vs confirmed approve; sealed-until-voted; RTL Arabic — asserted in unit tests and again in browser tests against a real seeded gate |
| **End to end** | A **17-step** narrative: seed → request → grade → seal → blinded review → clearance → checkpoint → receipt → offline verify, then eight deliberate tamper attempts each producing the correct refusal |
| **Types** | `mypy --strict` across the core package |
| | **283 automated checks plus the 17-step narrative. All passing.** |

---

## Limitations — what this does not prove

Reproduced from the verifier specification, because a verifier that overclaims is
worse than none:

- **It does not prove the released data was correctly redacted.** It proves what
  was released, under which rules, on whose authority. Whether the rules were
  adequate is a human judgement the receipt records but cannot make.
- **It does not detect a disclosive *sequence* of individually compliant
  releases.** No per-release check can. The budget bounds it; the ledger makes it
  auditable afterwards. This is an accepted, documented residual risk.
- **It does not detect a compromised gate.** If the gate is subverted, it signs
  whatever it is told to sign.
- **It does not establish that the vendor deleted its copy.** It establishes that
  the vendor *attested* to deletion, signed, at a verifiable time.

And, specific to this reference implementation: there is no pinnable binary
digest, reviewer keys are software keys (R4 unreachable), the timestamp token is
a signed note rather than RFC 3161, and identity is a request header rather than
a session.

---

## Troubleshooting

- **`ModuleNotFoundError: bayan_core` on macOS.** Some setups flag files created
  under the venv as *hidden*, and CPython then skips the editable `.pth` file.
  Run `./.venv/bin/python scripts/dev_pth.py`, which clears the flag and writes a
  plain path file. `run.sh` does this for you.
- **The gate refuses to start on a network filesystem.** That is deliberate. Use
  local storage, or set `BAYAN_ALLOW_NETWORK_FS=1` for a throwaway demo.
- **Port already in use.** `run.sh` / `run.bat` check both ports before starting
  and stop with a message rather than half-starting. Pick different ones with
  `GATE_PORT=8788 UI_PORT=5174 ./run.sh` — the console's API proxy follows the
  gate port automatically. To bypass the check entirely, set
  `SKIP_PORT_CHECK=1`.

---

## About this distribution build

This repository is a **distribution build**. It runs exactly as the development
tree does — same gate, same grader, same verifier, same console — but it is
packaged for evaluation rather than modification:

- Identifiers are name-mangled and the sources are minified.
- Docstrings, comments and the six design specifications are not included.
- The development test suite and build tooling are not included.

Everything documented above is reproducible from this repository. If you need a
readable, modifiable source tree — for an audit, a security review, or to build
on it — that is a separate licensing conversation.

---

## Licence

[Apache License 2.0](LICENSE). © Saswat Mishra.
