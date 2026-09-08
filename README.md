# Bayan — بيان

**A signed, recomputable Compliance Certificate for every diagnostic data release from an air-gapped AI deployment. Distribution build v0.4.0.**

A vendor's AI product runs inside a GCC government client's air-gapped data centre. When it misbehaves the engineer cannot see a trace, cannot reproduce the failure, and cannot legally carry the evidence out. Bayan replaces the site visit and the phone photograph with a declaration: a signed request, a policy evaluation that grades the release, a blinded two-person clearance, a receipt, and an append-only ledger that survives the air gap. Every release carries a certificate that is signed, bound to the released bytes, mapped to the client's control frameworks — and **recomputed** by an offline verifier that treats the certificate as a claim, never as a fact.

> ### This is a reference implementation, not a deployable enclave artifact.
>
> The system design specifies a single static binary, a Tessera ledger, Parquet storage, PIV reviewer keys and server-rendered HTML. This build is Python + TypeScript, made to be run locally and inspected. There is no single artifact a client security team can hash and pin; reviewer keys are browser-held software keys without hardware attestation, so the R-track caps at R3 and every certificate says so. The full list of departures is at the end of this file.

## Quickstart

```bash
./run.sh              # creates .venv, seeds the demo (50,000 fingerprints), starts gate :8787 and console :5173
./run.sh --gate-only  # the gate alone
GATE_PORT=9787 UI_PORT=5174 ./run.sh
```

Windows: `run.bat`. Requires Python 3.11+ and Node 20+; the console needs a browser with WebCrypto Ed25519 (Chromium ≥ 137, Firefox, Safari) because reviewers sign their votes in the browser.

Then open the console and switch **Acting as** between the six roles (the identity select in the header; the language toggle beside it). Every role home opens with one line — *what you can do here* — and every code on every screen (a grade, a field class, a transform, a gate, a mechanism) is rendered in the client's own words from the policy pack, in English and Arabic; the technical detail (digests, paths, the certificate's tracks) sits in a collapsed *Technical* tier. v0.4 is the signing desk: one design language (one token sheet, one headline per screen, 44 px targets, Arabic as a first script), the reviewer's decision inside the first screen of the brief at 1366 × 768, one recommendation that the engineer's primary button and the explanation share, and every name in the reader's script.

| Role | Home answers |
|---|---|
| **Omar** — engineer (vendor FDE) | What can I get out, at what price, right now? Six steps: questions grouped by state and priced in words → skill with the true cap reason → run with one headline and **one recommendation** as the primary button → improve (apply it and watch the preview change) → request → **Handoff** in three parts (take it away, what to do next, find out what a pseudonym is). |
| **Layla, Faisal** — reviewers (client ISO; Layla holds authority) | What am I being asked to sign, and what would I be responsible for? A three-step checklist until this browser holds an approved key; an inbox grouped by what each request needs from you; one decision card — the question, why they say they need it, what leaves as one line with the rows behind *Show the N rows*, who receives it, what changed, *You are signing as …* with the decision inside that box — then, closed, the text you are signing and the technical detail; nothing pre-selected, arrow keys never vote, a confirmation that says what you take on; the gate finalises when the last vote lands and the reveal names the other reviewers. |
| **Priya** — delivery lead (vendor) | Is acceptance evidence flowing, and where is it stuck? A chase list by name with Remind, the weekly proof-of-value as a preview first, the engineers' skill requests, an export for the sponsor. |
| **Khalid** — auditor (client compliance) | Show me control coverage for a period, then the evidence for a control — the gaps first, each explained; control → evidence → receipt in three actions, the receipt opening with who asked, why, who approved, retention and disposal. |
| **Hessa** — an auditor with the *external* permission | The auditor's view, read-only, artefacts as digests only, with "how to verify offline" first. |
| **Noura** — data owner / DBA | Which fields wait for my answer, and what depends on it? What waits comes first — fields as cards, then the skills that wait for the client's co-signature — and every ratified field is a row of one table with *Reclassify as…* in the row, the options ordered by strictness with the direction stated. |

## What a Compliance Certificate is

`bayan.certificate.v1` is a JSON document inside the signed clearance statement, carried in every bundle and summarised in every receipt. It carries the inputs the grade was computed from and the grade itself: the **manifest** (every field that leaves, its class and transform), the **output schema** the released bytes must match, **provenance** (skill, version, signatures, client co-signature, transform lineage), the **recipient** (organisation facts and the requester's roster entry), the **grade** `D/P/R @ E` with the seven gates and their remedy kinds, the **mechanisms** the release demonstrably exercised and the framework **controls** derived from them through the policy pack's crosswalk, and a plain-language **headline** in English and Arabic. The JSON Schemas under `packages/core/bayan_core/schema/schemas/` are the open specification; they ship unminified.

## The seven gates

`PCI-SAD` · `PCI-PAN` · `MNPI-CONTAINMENT` · `EXPORT-DEEMED` · `PRIVILEGE` · `PART2` · `ACCESS-LOCALITY`. Every gate is evaluated on every release; packs supply parameters, never off-switches. A failed gate names the rule, quotes the source, and says what kind of remedy applies: `drop_field`, `truncate`, `change_recipient`, `legal_instrument`, `roster` or `not_evaluable`.

## The verifier

```bash
.venv/bin/bayan-verify var/outbox/release-<id> --trust var/trust --assert-offline
.venv/bin/bayan-verify var/outbox/release-<id> --trust var/trust --assert-offline --json      # recomputed vs claimed
.venv/bin/bayan-verify pack var/outbox/evidence-pack-<deployment>-<period> --trust var/trust --assert-offline
.venv/bin/bayan-verify accept-delta old-acceptance.json new-acceptance.json
```

It runs with no network and no service, in 18 steps (0–17), and exits 0 only when every step passes:

| Code | Meaning |
|---|---|
| `0` | All steps passed |
| `10` | Signature or threshold failure (steps 1–2); with `--strict`, a reviewer key labelled `gate-colocated` |
| `20` | Schema or chain failure (steps 3–4) |
| `30` | Profile mismatch (step 5), or a v1 bundle: `certificate unsigned; re-issue` |
| `40` | Separation-of-duties violation (step 6) |
| `50` | Commitment did not open (step 7) |
| `60` | Artefact digest mismatch, or an artefact not listed in the receipt (step 8) |
| `70` | Inclusion or consistency proof failure (steps 9–10) |
| `80` | Retention overdue without attestation (step 12) |
| `90` | Certificate does not validate, or the receipt's summary disagrees (step 13) |
| `91` | **Over-grading**: a claimed level exceeds recomputation, a gate result differs, or a release the recomputed certificate would not release (step 14) |
| `92` | Released bytes do not conform to the certificate's `outputSchema` (step 15) |
| `93` | `controls` do not re-derive from `mechanisms` and the pack (step 16) |
| `94` | Roster entry absent from the gate-signed snapshot, or not valid at request time (step 17) |

## Layout

```
packages/core     pure logic: crypto, schemas, grader, transform pipeline, sandbox, ledger, packs, evidence pack
packages/gate     the enclave-local service: FastAPI + SQLite, roster, sensor adapter and kill switch, key enrolment, acceptance
packages/sdk      non-blocking fingerprint emitter
packages/verify   the offline verifier (`bayan-verify`)
packages/ui       the console (React + Vite)
data/packs        five policy packs with control provenance      data/skills   thirteen certified skills
data/mock         the demo data generators                        data/sensor   an EDR replay fixture (scripts/sensor_replay.py)
```

## Limitations — what this does not prove

- It does not prove the released data was correctly redacted. It proves what was released, under which rules, on whose authority, and that the certificate's claims recompute from its inputs.
- It does not detect a disclosive *sequence* of individually compliant releases. The budget bounds it; the ledger makes it auditable afterwards.
- It does not detect a compromised gate. The sensor layer is an adapter over the client's own EDR feed, not an independent observer.
- It does not establish that the vendor deleted its copy. It establishes that the vendor *attested* to deletion, signed, at a verifiable time.

## Deliberate departures from the design

| Design says | This build | What is lost | Mitigation |
|---|---|---|---|
| Go static binary, `CGO_ENABLED=0`, hashable and pinnable (`SYSTEM-DESIGN.md` §0 constraint 3, §4.2) | Python packages (`packages/core`, `gate`, `sdk`, `verify`) plus a Node/React UI | **Constraint 3 is not met.** There is no single artifact whose digest a client security team can pin. | `README.md` states plainly that this is a reference implementation, not a deployable enclave artifact. The `core` package is pure logic with no I/O, so it can be ported line-for-line. |
| Tessera POSIX ledger (`SYSTEM-DESIGN.md` §4.1, §7.2) | RFC 6962 Merkle tree implemented directly in Python over an append-only directory | Production hardening, tiling, antispam, the BadgerDB/`GOMEMLIMIT` behaviour the runbook describes | RFC 6962 is ~150 lines of well-specified maths. It is implemented exactly and tested against the RFC 9162 §2.1.5 test vectors (roots, inclusion proofs, consistency proofs). |
| Parquet cold store, tier-partitioned (`SYSTEM-DESIGN.md` §4.1, §6) | SQLite only, with a tier column and a declared read-only view | Columnar scan performance; partition-delete retention | Irrelevant at demo scale (§2 load table: tens of writes per day on the control plane). Skills still read a **declared view**, never the primary table. |
| Server-rendered HTML, works with JavaScript disabled (`SYSTEM-DESIGN.md` §8.1) | React SPA built with Vite | Enclave UI robustness; progressive enhancement | Everything is bundled: no CDN, no external font, no runtime fetch other than the enclave-local API. The reviewer brief is rendered **server-side** from deterministic templates and its digest is computed server-side, so the browser is not a trust boundary for `presented_digest`. |
| PIV/smartcard reviewer keys via PKCS#11 (`SYSTEM-DESIGN.md` §7.3) | Browser-held WebCrypto Ed25519 keys (non-extractable, IndexedDB), enrolled with the gate; genesis at onboarding, later enrolments approved by a different principal with authority as a `key-enrolment` leaf; the gate verifies and stores the signature it receives and never signs for a reviewer. The demo's seeded reviewers keep their "browsers" under `<data>/client-keys/` so the API tests and the smoke can sign. | **No hardware attestation, so R4 stays unreachable.** A browser key can be lost (re-enrolment is a leaf, not a loss of history). | `custody: client` on every reviewer key in the trust root; `bayan-verify --strict` refuses a reviewer key labelled `gate-colocated`; `key_type: software` is still recorded truthfully and the grader caps R at R3. Engineer, DBA, TSA, registry and disposal keys stay gate-colocated and are labelled so. |
| RFC 3161 timestamp token from a TSA applied outside the enclave (`VERIFIER.md` §2 step 11, §7.2) | `timestamp.tsr` is a signed JSON note `{bundleDigest, time}` signed by a vendor-side "TSA" key in `trust/keys.json`; not ASN.1 CMS | Interoperability with real TSAs and TST parsers | The semantics are preserved: time comes from a signature made outside the enclave by a key in the trust root, never from the ledger. Swapping in real RFC 3161 changes one module. |
| Voice review, ASR/TTS (`SYSTEM-DESIGN.md` §8.3) | Not built | Voice review | Text review in Arabic and English is unconditional; voice was already flagged as blocked on a legal question. |
| SIEM emission in CEF/LEEF (`SYSTEM-DESIGN.md` §11) | Structured events written to a local JSONL audit file | Native SIEM integration | Every request, decision, release, refusal and quarantine is emitted as an event; the transport is a file. |
| Session-authenticated reviewer API (`SYSTEM-DESIGN.md` §9.3) | Identity and role are supplied by `X-Bayan-User` / `X-Bayan-Role` headers | Real authentication | Documented as a demo control. Every server-side control (`/reveal` 403, requester-as-reviewer rejection, role separation) is enforced against that identity, so wiring a real session layer changes one dependency. |
| DSSE differential testing against a second implementation (`TESTING-STRATEGY.md` §4) | Self-consistent tests plus fixed vectors computed by hand from the PAE definition | Independent confirmation of the encoding | The PAE vector in `tests/crypto/test_dsse.py` is derived from the specification text, not from this implementation. |
| Every roster acknowledgement and DBA ratification is signed by the person (`SYSTEM-DESIGN-ADDENDUM.md` §5.2; build prompt §4.3 "Ratify signs in the browser") | Engineer, lead and DBA signatures are made with keys the gate holds for them (`Gate.signers_for`); only reviewer keys are browser-held. A field-class ratification is signed by the DBA's gate-held key over `bayan.field-class-ratification.v1`, stored on the row and emitted as a `field-class-ratified` audit event | A compromised gate could fabricate an engineer's acknowledgement | The acknowledgement payload and signature are stored and re-verified; the roster snapshot is gate-signed and every certificate cites the entry digest; a client-made signature is accepted and verified when supplied. |
| Recipient attributes on the deployment (`SYSTEM-DESIGN.md` §6, `deployment.recipient`) | Person attributes live on the roster; `deployment.recipient` carries organisation facts only | — (this is the addendum's model) | `GET /v1/deployments` never returns citizenship or location; reviewers see `locality: ok/blocked`. |
| Sensor layer detects `UNSANCTIONED_QUERY` at the store (`SYSTEM-DESIGN-ADDENDUM.md` §5.6) | Adapter-reported only: the client's DLP/auditd feed maps the event; the gate has no store-side detector | A direct read of the declared view that the client's own tooling does not see is not reported | The gate's own legitimate reads (`/v1/records`, exemplar, summary, ingest) make a naive store authorizer fire on itself; documented in `docs/SENSOR.md` and `PROGRESS.md` TODO. The kill switch and the hour-digest evidence work identically for an adapter-reported event. |
| A host sensor (`BAYAN-PRD-ADDENDUM` §8.3) | An adapter over the client's EDR/DLP feed with a replay emitter for the demo (`scripts/sensor_replay.py`) | Coverage depends on what the client already runs | Declared per hour in the evidence pack (`sensorAbsent`), never inferred as quiet; the honesty clause travels in every pack and digest leaf. |
| Packs are signed bundles (`BAYAN-TOOLKIT-DESIGN.md` §12) | Packs are JSON files under `data/packs`, unsigned; the deployment pins the digest it was onboarded under and a `bayan.pack-upgrade.v1` leaf (signed by a principal with authority and the gate) is required before grading under another | No signature on the pack file itself | The pinned digest travels in every certificate and every bundle's `trust/profile-<id>.json`; an edit to the file is refused at the next run until an authority signs the upgrade, and the upgrade is a ledger leaf the evidence pack lists. |
| Reviewers co-sign the clearance envelope (`SYSTEM-DESIGN.md` §7.3; addendum §3.1 wording) | The gate signs the envelope; every `humanReviews[]` entry carries the reviewer's own signature over `{request, reviewer, verdict, reason, presentedDigest, lang, at}`; the verifier counts vote signatures for (t,n) and recomputes R from them | The (t,n) rule is on votes, not on the leaf's envelope | Every vote is signed by the reviewer's key over exactly what they saw and decided, emitted verbatim; `bayan-verify` step 2 refuses a vote whose signature verifies against nothing and step 14 refuses an R the votes do not support. This is the model Phase 9 (browser-held keys) needs. |
| A reminder reaches the reviewer through a channel (report F-33; build prompt v3 §3.3) | `POST /v1/requests/{id}/remind` records a `reminder` row and emits a `review-reminder` audit event naming the outstanding reviewers; no email, SMS or chat is wired | Nobody is paged | The lead's chase list shows "Reminder recorded N ago" so the act is visible; a client-side notifier can tail the JSONL audit file, which is the deployment's existing integration point. |
| The requester takes the bundle away from the outbox on the enclave host (`SYSTEM-DESIGN.md` §4.1) | `GET /v1/bundles/{id}/archive` streams the bundle directory as a deterministic zip to the requester, the lead or an auditor, emitting a `bundle-downloaded` event | The outbox is no longer the only exit | A demo convenience for the Handoff step (F-10): the archive is the same bytes the outbox holds; the receipt, the register line and the verify command are unchanged; the event is on the ledger's audit trail. |
| The client co-signs a skill with its own key (build prompt v3 §2.7; `BAYAN-TOOLKIT-DESIGN.md` §11) | The data owner's *Co-sign* is signed with the DBA's gate-held key over `bayan.skill-certification.v1`, stored on the skill row and emitted as `skill-certified`; *Decline* records a reason | A compromised gate could fabricate the client's co-signature | Same mitigation as the ratification row above: the payload and signature are stored and re-verified, the certificate's provenance carries `clientCosigned`, and a client-made signature is accepted when supplied. |
| Every user-facing string exists in Arabic reviewed by a legal translator (build prompt v3 §0) | Every string exists in both languages; the Arabic of the v3 additions (pack `terms`, templates, console strings, error sentences) is machine-drafted by the engineer and listed in `PROGRESS.md` as pending a legal translator | A legal nuance may be wrong in Arabic | Nothing is transliterated or falls back: a test refuses a missing Arabic term and a Playwright journey refuses an English fallback on any Arabic screen; the brief's Arabic text is digested and signed as presented, so what the reviewer read is what the ledger holds. |
| The reviewer signs what they were shown (`SYSTEM-DESIGN.md` §7.3; build prompt v4 invariant 11) | The presented digest is over the gate-rendered brief TEXT (the deterministic template's output for the request, in the reviewer's language); the rows the reviewer can open under *Show the N rows* are the artefact's preview, outside that digest by design; the artefact itself is bound by its own digest in the certificate | The vote does not bind the rows the reviewer looked at, only the text they signed | The brief text names the row count, the columns and their classes and the threshold; the artefact digest is in the certificate the same envelope carries; signing `{presentedDigest, artefactDigest}` together is the open question recorded for v0.5 in `PROGRESS.md`. |
| Nobody learns who has voted before resolution (build prompt v4 invariant 12) | The lead's chase list shows *Waiting for* — the reviewers who have not voted; the requester's *My requests* shows *Could be waiting for* — every eligible reviewer, with the votes in as a count; the gate computes the two lists differently on purpose (`eligible_reviewers(exclude_voters=…)`) | The lead can infer who voted | The lead already holds that authority; the requester never learns it (a test refuses a list that shrinks after a vote), and the brief's own wait line after a vote names only who *could* still be waiting. |
| Every sentence a reviewer reads exists in Arabic (build prompt v3 §0; v4 Phase 6) | The sealed recommendation's basis — the engine's rule sentences sealed in the commitment before the vote — is English in both languages; the reveal shows it as an isolated English run (`lang="en"`) beside the Arabic sentence that introduces it | An Arabic reviewer reads the machine's reasons in English after the vote | The basis is never part of the decision (it opens only after the vote and only for those who voted); a bilingual sealed basis changes every seal and is the v0.5 item recorded in `PROGRESS.md`; every other sentence on the reveal is Arabic. |
| Finalisation "inside the vote's transaction" (build prompt v2, Phase 1) | The vote row commits first; finalisation runs in its own transaction under the same gate lock | A crash between the two leaves a committed vote and a pending clearance for a moment | Startup reconciliation repairs the clearance from the ledger leaf (the anchor) and re-issues the receipt; the vote is never lost. See `PROGRESS.md` Findings. |

## About this distribution build

This is a packaged, runnable build of the private repository: identifiers are name-mangled and sources minified; comments, docstrings, design documents and the development test suite are removed. The JSON Schemas are the exception — they are the open specification and ship as written. The full suite (property tests, golden certificates, mutation testing at the grader and verifier layers, the role × route matrix, the 30-step smoke narrative, the Playwright journeys) lives in the private repository and produced this build at commit `611affb` on 8 September 2026.

## Licence

Code: Apache-2.0 (`LICENSE`).
