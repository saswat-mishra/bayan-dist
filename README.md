# Bayan — بيان

**A signed, recomputable Compliance Certificate for every diagnostic data release from an air-gapped AI deployment. Distribution build v0.5.1.**

A vendor's AI product runs inside a client's air-gapped data centre. When it misbehaves the engineer cannot see a trace, cannot reproduce the failure, and cannot legally carry the evidence out. Bayan replaces the site visit and the phone photograph with a declaration: a signed request, a policy evaluation that grades the release, a blinded clearance by the people the policy names, a receipt, and an append-only ledger that survives the air gap. Every release carries a certificate that is signed, bound to the released bytes, mapped to the client's control frameworks — and **recomputed** by an offline verifier that treats the certificate as a claim, never as a fact.

> ### This is a reference implementation, not a deployable enclave artifact.
>
> The system design specifies a single static binary, a Tessera ledger, Parquet storage, PIV reviewer keys and server-rendered HTML. This build is Python + TypeScript, made to be run locally and inspected. There is no single artifact a client security team can hash and pin; reviewer keys are browser-held software keys without hardware attestation, so the R-track caps at R3 and every certificate says so. The full list of departures is at the end of this file.

## Quickstart

```bash
./run.sh              # creates .venv, seeds the demo (nine deployments, 86,000 fingerprints, a history of releases), starts gate :8787 and console :5173
./run.sh --gate-only  # the gate alone
./run.sh --reseed     # rebuild the demo world from scratch
GATE_PORT=9787 UI_PORT=5174 ./run.sh
```

Windows: `run.bat`. Requires Python 3.11+ and Node 20+; the console needs a browser with WebCrypto Ed25519 (Chromium ≥ 137, Firefox, Safari) because reviewers sign their votes in the browser. The world opens with transactions already in it — releases across nine weeks, two refusals, pending reviews (one past the stuck threshold), sealed sensor hours, an evidence pack — so every page has something to show on arrival.

## What's new in v0.5

- **Five people, five jobs.** The *Acting as* picker offers one person per role. The other principals — the second and third reviewers, a remote engineer the roster refuses, an external assessor — are still people the gate answers for and names on screen, not logins.
- **Every page names itself.** Each destination opens with its own title and one sentence that says what the reader can do there.
- **Ask understands a sentence.** The engineer's new **Integrations** page connects the client's own model; see *Connecting the client's model* below.
- **The auditor's rail is three entries** — *Coverage*, *Evidence packs*, *Records* (register, ledger, sensor, roster and pack as tabs of one page) — and verification is shown as a status with the real trust directory; the shell command sits one disclosure down for technical staff.
- **The data owner has two pages**, *Decisions* and *Fields*.
- **Nine deployments across seven policy packs**, including two deliberately lighter regimes; see *The width* below.
- A viewport-tall navigation rail, a centred page, and glass that blurs only where content scrolls behind it.

## The five identities

Switch **Acting as** in the header; the language toggle (EN | ع) and the appearance toggle sit beside it. Every code on every screen (a grade, a field class, a transform, a gate, a mechanism) is rendered in the client's own words from the policy pack, in English and Arabic; the technical detail (digests, paths, the certificate's tracks) sits in a collapsed *Technical* tier.

| Identity | Pages | Answers |
|---|---|---|
| **Omar** — engineer (vendor FDE) | Ask · My requests · Integrations · Roster | What can I get out, at what price, right now? Six steps: questions grouped by state and priced in words → the skill with its true cap reason → run with one headline and **one recommendation** as the primary button → improve (apply it and watch the preview change) → request → **Handoff** (take it away, what to do next, find out what a pseudonym is). |
| **Layla** — reviewer (client ISO, holds authority) | Inbox · Authority | What am I being asked to sign, and what would I be responsible for? An inbox grouped by what each request needs from you; one decision card with the decision inside the first screen at 1366 × 768; nothing pre-selected, arrow keys never vote; the reveal names the other reviewers. Authority approves key enrolments, pack upgrades and the acceptance. |
| **Priya** — delivery lead (vendor) | Dashboard · Roster · Evidence | Is acceptance evidence flowing, and where is it stuck? A chase list by name with Remind and a *stuck* badge, the weekly proof-of-value as a preview first, the engineers' skill requests, an acceptance timeline with an export for the sponsor. |
| **Khalid** — auditor (client compliance) | Coverage · Evidence packs · Records | Show me control coverage for a period, then the evidence for a control — gaps first, each explained; control → evidence → receipt in three actions. An auditor with the *external* permission sees the same pages read-only, with artefacts as digests. |
| **Noura** — data owner / DBA | Decisions · Fields | Which fields wait for my answer, and what depends on it? The fields to ratify and the skills awaiting the client's co-signature under *Decisions*; every ratified field as a row with *Reclassify as…* under *Fields*. |

## Connecting the client's model

Ask works without a model: it ranks the deployment's questions by the words typed, and says so. Connect one and it understands sentences.

1. As Omar, open **Integrations**.
2. Enter an OpenAI-compatible endpoint and the model it serves — for a local Ollama, `http://127.0.0.1:11434` and a model such as `llama3.1:8b`. vLLM and llama.cpp servers work unchanged.
3. **Connect** — the gate tests the endpoint from its own side (`GET /v1/models`) and shows the latency and the models it serves.

The boundary is enforced by the gate, not the page:

- **The endpoint must be inside the enclave** — loopback or a private address. A public host is refused with a sentence that says why.
- **The model sees the question catalogue, never the data** — the questions, what each needs, its grade and approval path, and the certified skills' descriptions. Never a record, a row or an artefact.
- **Its answer is a closed choice.** The reply must name a question from the catalogue; an invented one is dropped, and a reply in the wrong shape falls back to words. The model changes what Ask *understands*, never what the gate *releases*.
- **Every call is audited by digest** — the prompt's, the reply's and the model id — with no transcript kept.

## The width — nine deployments, seven packs

A policy pack carries **parameters, never a gate off-switch**. A lighter regime is therefore the same seven gates on different settings: which frameworks are activated, what review each data level needs, the release budget, retention and certificate validity. The same question — *which documents, which city* — needs a different number of people depending on the pack:

| | `saas-corp` — low | `retail-consumer` — mid | `uae-gov` and the other heavy packs |
|---|---|---|---|
| Frameworks | SOC 2, ISO 27001 | + NIST AI RMF | three to five, including the client's regulator |
| Counts by topic and week (D2) | releases by policy | releases by policy | releases by policy |
| A named document, city or property (D1) | **releases by policy (R1)** | **one named approver (R2)** | **two blinded approvers (R3)** |
| A sensitive attribute, or one record verbatim | two blinded approvers | two blinded approvers | two blinded approvers |
| Budget · disposal · certificate validity | 200 / quarter · 180 d · 180 d | 80 / quarter · 120 d · 120 d | 40 / quarter · 90 d · 90 d |

| Deployment | Pack | What it shows |
|---|---|---|
| MOI staff IT-service assistant | `uae-gov` | **The default demo.** 50,000 fingerprints; pension retrievals fail after an index rebuild. A green skill answers "why are pension queries failing?" with no human; document identity needs two blinded reviewers; the uplift replaces identities with enclave pseudonyms and re-grades. A remote engineer located outside the UAE is refused by `ACCESS-LOCALITY`. |
| DEWA billing assistant · TAMM citizen services | `uae-gov` | The same skill shapes as the SaaS deployment under a heavy pack — the D1 question needs two approvers here. |
| DHA patient appointment bot | `healthcare` | PHI: a sensitive diagnosis attribute that reaches D2 only when named in the purpose; the **`PART2`** gate on a substance-use programme identifier; a field awaiting the data owner. |
| DIFC deal-desk contract-review assistant | `mnpi` | **`MNPI-CONTAINMENT`** fails as a binary gate; the fix is changing the recipient, and the refusal is a ledger leaf. |
| Gulf Bank card-services assistant | `financial` | **`PCI-SAD`**: a CVV in a log is unfixable even hashed. **`PCI-PAN`**: truncation passes the gate and the D-track still says D0. A pack floor refuses anything below D2. |
| Acme Cloud customer-support assistant | `saas-corp` | 12,000 fingerprints; SSO answers fail after an index rebuild. Article identity is D1 and **releases by policy**. The auditor's coverage lists SOC 2 and ISO 27001 only, and shows two-person clearance as an honest gap — nothing on this pack ever needs two people. |
| Souq marketplace shopping assistant | `retail-consumer` | 3,000 assisted orders. *Complaints by city* names a city and needs **one named approver**; *sentiment by category* carries a sensitive attribute and needs two, whatever the pack says. |
| Marhaba Hotels concierge bot | `retail-consumer` | 2,000 stays. *Unresolved requests by property* names a property and needs one approver; requests by topic and week release by policy. |

## What a Compliance Certificate is

`bayan.certificate.v1` is a JSON document inside the signed clearance statement, carried in every bundle and summarised in every receipt. It carries the inputs the grade was computed from and the grade itself: the **manifest** (every field that leaves, its class and transform), the **output schema** the released bytes must match, **provenance** (skill, version, signatures, client co-signature, transform lineage), the **recipient** (organisation facts and the requester's roster entry), the **grade** `D/P/R @ E` with the seven gates and their remedy kinds, the **mechanisms** the release demonstrably exercised and the framework **controls** derived from them through the policy pack's crosswalk, and a plain-language **headline** in English and Arabic. The JSON Schemas under `packages/core/bayan_core/schema/schemas/` are the open specification; they ship unminified.

## The seven gates

`PCI-SAD` · `PCI-PAN` · `MNPI-CONTAINMENT` · `EXPORT-DEEMED` · `PRIVILEGE` · `PART2` · `ACCESS-LOCALITY`. Every gate is evaluated on every release of every pack, the lightest included; packs supply parameters, never off-switches. Gates match on field tags, and a pack's tags reach every manifest by name and by column lineage, so a skill that omits a tag or renames a column is still caught. A failed gate names the rule, quotes the source, and says what kind of remedy applies: `drop_field`, `truncate`, `change_recipient`, `legal_instrument`, `roster` or `not_evaluable`.

## The verifier

```bash
.venv/bin/bayan-verify var/outbox/release-<id> --trust var/trust --assert-offline
.venv/bin/bayan-verify var/outbox/release-<id> --trust var/trust --assert-offline --json      # recomputed vs claimed
.venv/bin/bayan-verify pack var/outbox/evidence-pack-<deployment>-<period> --trust var/trust --assert-offline
.venv/bin/bayan-verify accept-delta old-acceptance.json new-acceptance.json
```

It runs with no network and no service, in 18 steps (0–17), and exits 0 only when every step passes — for a release under any of the seven packs, re-deriving that pack's controls exactly:

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
packages/gate     the enclave-local service: FastAPI + SQLite, roster, sensor adapter and kill switch, key enrolment,
                  acceptance, the seeded history, and the client-model integration behind Ask
packages/sdk      non-blocking fingerprint emitter
packages/verify   the offline verifier (`bayan-verify`)
packages/ui       the console (React + Vite)
data/packs        seven policy packs with control provenance    data/skills   twenty-eight certified skills across nine scenarios
data/mock         the demo data generators, heavy and light     data/sensor   an EDR replay fixture (scripts/sensor_replay.py)
```

## Limitations — what this does not prove

- It does not prove the released data was correctly redacted. It proves what was released, under which rules, on whose authority, and that the certificate's claims recompute from its inputs.
- It does not detect a disclosive *sequence* of individually compliant releases. The budget bounds it; the ledger makes it auditable afterwards.
- It does not detect a compromised gate. The sensor layer is an adapter over the client's own EDR feed, not an independent observer.
- It does not establish that the vendor deleted its copy. It establishes that the vendor *attested* to deletion, signed, at a verifiable time.
- It does not vouch for the client's model. The model's weights are not pinned by this build; it helps Ask choose a question and never touches what is released.

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
| The assistant's model is the vendor's, digest-pinned in the build (`BAYAN-SYSTEM-DESIGN-REPORT.md` §4.5) | v0.5: the model is the **client's** — an OpenAI-compatible endpoint the engineer connects under Integrations (`bayan_gate/assistant.py`), which the gate refuses unless its host is loopback or a private address, and reaches from its own side of the enclave | **The model's weights are not pinned by the build's digest**, so a release composed with its help cannot cite a model digest, and the `--assert-offline` posture of the verifier says nothing about the model process | The model is Tier A only: it sees the question catalogue and the engineer's words, never a record, and its reply is read as a closed choice from that catalogue (`test_assistant.py`); every call is an audit event with the prompt's and reply's digests and the model id, no transcript kept; when a client will not attest a weights digest the certificate's provenance stays at the level the pack computes — the model changes what Ask *understands*, never what the gate *releases*. |
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

This is a packaged, runnable build of the private repository: identifiers are name-mangled and sources minified; comments, docstrings, design documents and the development test suite are removed. The JSON Schemas are the exception — they are the open specification and ship as written. The full suite (property tests, golden certificates, mutation testing at the grader and verifier layers, the role × route matrix, the 31-step smoke narrative, the Playwright journeys) lives in the private repository and produced this build at commit `037452a` on 11 September 2026.

## Licence

Code: Apache-2.0 (`LICENSE`).
