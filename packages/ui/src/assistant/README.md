# Ask in your own words — the seam

`route.ts` ranks the questions THIS deployment can answer against words the engineer typed, using only what the
gate already returned to this screen (the feasibility rows and the skills behind them). `AskBox.tsx` shows the
closest question and which of the reader's own words matched, and stops: the question card below is still the
thing that is clicked, because selection never acts (build prompt v4 invariant 13).

It is deterministic and offline by construction — no model, no network, no state on the gate:

- input: `FeasRow[]` and `Skill[]`, both already on screen; never a run, never rows, never the machine's finding;
- output: a ranking and the matched words. It never composes a request, never picks a skill, never runs anything;
- the full list of questions is never hidden by a search — a question no words matched is still on the page.

If a client ever permits a language model in the enclave, it plugs in HERE and nowhere else, under the same
contract as `src/explain/README.md`: it may RE-RANK the ids this module produced and say why in a sentence, and it
may not invent a question, reach past this screen's data, or turn a ranking into an action. The system design
report's §4.3 lists the four functions a model may have and the six it may never have; the taint test it describes
(`no released byte originates from an assistant response`) is what keeps that honest.
