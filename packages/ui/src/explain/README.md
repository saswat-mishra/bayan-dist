# Explain this — the seam

`components/ExplainThis.tsx` answers three questions from the certificate and the policy pack's own words, with
templates only: *why this needs reviewers*, *what would make it release by policy*, *what this rule means*. It is
labelled "Explanation, not evidence" on screen and is never part of the evidence path (the brief text, its digest,
the certificate and the ledger are computed by the gate and the core; nothing here changes them).

If a client permits a language model for explanations, it plugs in HERE and nowhere else:

- input: the same `Certificate` JSON and the pack's `terms`/`rules` the templates read — never the machine finding
  before a vote (the seal), never the raw rows;
- output: prose shown under the same "Explanation, not evidence" label, in both languages;
- constraint: the model may paraphrase what the certificate says; it may not claim what the engine cannot recompute
  (build prompt v3 §0, "Never make a claim the engine cannot recompute").

The default build has no model call and no network: `ExplainThis` is deterministic and offline.
