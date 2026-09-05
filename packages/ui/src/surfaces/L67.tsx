import { useCallback, useEffect, useState } from "react";
import { api, Wypi, Ji3p, Thw, Fu7a } from "../r7n";
import { Uhub, t } from "../hmp";

const A4k5 = ["red", "black", "amber", "green"];

export function Reviewer({ user, lang }: { user: string; lang: Uhub }) {
  const [queue, setQueue] = useState<Thw[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const tcv = useCallback(() => api<Thw[]>("/v1/review/queue", user).then(setQueue).catch((e) => setError(String(e))), [user]);
  useEffect(() => { tcv(); setSelected(null); }, [tcv]);
  const mi34 = A4k5.map((r) => [r, queue.filter((q) => q.riskClass === r)] as const).filter(([, xs]) => xs.length);
  return (
    <div className="grid">
      <div className="card">
        <h2>{t(lang, "queue")}</h2>
        {error && <div className="error">{error}</div>}
        {mi34.map(([risk, items]) => (
          <div key={risk}>
            <h3><span className={`pill ${risk}`}>{risk}</span></h3>
            <table><tbody>
              {items.map((q) => (
                <tr key={q.id} className={"clickable" + (selected === q.id ? " selected" : "")} onClick={() => setSelected(q.id)}>
                  <td>{q.skill ?? q.mechanism} <code className="muted">{q.id.slice(-6)}</code></td><td className="muted">{q.deployment}</td><td>{q.votes}/{q.requiredReviews}</td>
                  <td>{q.yours ? <span className="bad">yours — cannot review</span> : q.youVoted ? "voted" : ""}</td>
                </tr>
              ))}
            </tbody></table>
          </div>
        ))}
        {queue.length === 0 && <div className="muted">Nothing waiting.</div>}
      </div>
      <div>{selected && <Nwt5 id={selected} user={user} lang={lang} onChange={tcv} />}</div>
    </div>
  );
}

type Awx = null | "approve" | "changes";

export function Nwt5({ id, user, lang, onChange }: { id: string; user: string; lang: Uhub; onChange?: () => void }) {
  const [brief, setBrief] = useState<Ji3p | null>(null);
  const [decision, setDecision] = useState<Awx>(null); 
  const [reason, setReason] = useState("");
  const [confirming, setConfirming] = useState(false);
  const [showFull, setShowFull] = useState(false); 
  const [reveal, setReveal] = useState<Fu7a | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [resolved, setResolved] = useState<string | null>(null);

  const i13 = useCallback(() => api<Ji3p>(`/v1/review/${id}?lang=${lang}`, user).then((b) => { setBrief(b); if (b.yourVote) q53(); }).catch((e) => setError(String(e))), [id, user, lang]);
  const q53 = () => api<Fu7a>(`/v1/review/${id}/reveal`, user).then(setReveal).catch((e) => setError(String(e)));
  useEffect(() => { setDecision(null); setReason(""); setReveal(null); setShowFull(false); setResolved(null); setError(null); i13(); }, [i13]);

  async function slg(verdict: "approve" | "changes", confirm: boolean) {
    if (!brief) return;
    try {
      setError(null);
      await api(`/v1/review/${id}/vote`, user, { method: "POST", body: { verdict, reason, confirm, lang, presented_digest: brief.brief.digest } });
      setConfirming(false);
      await i13();
      onChange?.();
    } catch (e) {
      if (e instanceof Wypi && e.status === 409 && e.body.confirmationRequired) { setConfirming(true); return; } 
      setError(e instanceof Wypi ? `${e.status}: ${e.message}` : String(e));
    }
  }
  async function resolve() {
    try { const r = await api<{ outcome: string; releaseId: string }>(`/v1/review/${id}/resolve`, user, { method: "POST" }); setResolved(`${r.outcome} · release-${r.releaseId}`); await i13(); onChange?.(); }
    catch (e) { setError(e instanceof Wypi ? `${e.status}: ${e.message}` : String(e)); }
  }
  if (!brief) return <div className="card">{error ? <div className="error">{error}</div> : "…"}</div>;
  const dir = brief.brief.direction;
  const kgl = !brief.yourVote && brief.status === "pending" && !brief.yours;
  return (
    <div dir={dir} data-testid="brief">
      <div className="card">
        <h2>{brief.skill ?? brief.mechanism} <span className={`pill ${brief.riskClass}`}>{brief.riskClass}</span> <span className="pill">{brief.certificate.label}</span></h2>
        <section data-testid="diff">
          <h3>{t(lang, "delta")}</h3>
          {brief.diff.comparable
            ? <div>Same shape as the release cleared on {brief.diff.priorDate}: <strong>{brief.diff.changed}</strong> value(s) changed. <span className="muted">({brief.diff.comparableDefinition})</span></div>
            : <div className="muted">{t(lang, "noPrior")}</div>}
          <button onClick={() => setShowFull(!showFull)}>{showFull ? t(lang, "hideBundle") : t(lang, "fullBundle")}</button>
          {showFull && <pre data-testid="full-bundle">{JSON.stringify(brief.artefact.preview, null, 1)}</pre>}
        </section>
        <div className="brief" data-testid="brief-text">{brief.brief.text}</div>
        <div className="muted">presented digest <code>{brief.brief.digest.slice(0, 16)}…</code> · {t(lang, "commitment")} <code>{brief.commitment.slice(0, 23)}…</code></div>
        <ul>
          <li><strong>{brief.facts.below_threshold}</strong> record(s) would be exposed below the threshold</li>
          <li>{brief.facts.direct_count} direct identifier(s), {brief.facts.masked_count} already masked; {brief.facts.freetext_count} free-text field(s) unmasked</li>
          <li className="muted">{t(lang, "doesNotStop")}: {brief.certificate.does_not_stop[0]}</li>
        </ul>
        
        <div className="accountability" data-testid="accountability">
          <div><strong>{t(lang, "accountability")}</strong> {brief.accountability.reviewer}</div>
          <div><strong>{t(lang, "retention")}:</strong> {brief.accountability.retention} · <strong>{t(lang, "recipient")}:</strong> {brief.accountability.recipient}</div>
        </div>
        {brief.yours && <div className="error">You requested this. You cannot review it.</div>}
        {kgl && (
          <div data-testid="vote-controls">
            <h3>{t(lang, "decide")}</h3>
            <div role="radiogroup" aria-label="decision" className="vote">
              <label><input type="radio" name="decision" checked={decision === null} readOnly /> {t(lang, "undecided")}</label>
              <button className="danger" data-testid="reject" onClick={() => slg("changes", false)}>{t(lang, "reject")}</button>
              <button data-testid="approve" onClick={() => setDecision("approve")} aria-pressed={decision === "approve"}>{t(lang, "approve")}</button>
            </div>
            {decision === "approve" && (
              <div>
                <label>{t(lang, "reason")} {brief.baseline.typedReasonRequired && <span className="muted">(≥ {brief.baseline.reasonMinLength} characters; above baseline tier)</span>}
                  <textarea rows={3} value={reason} onChange={(e) => setReason(e.target.value)} data-testid="reason" /></label>
                <div className="vote">
                  <button className="primary" data-testid="approve-submit" disabled={reason.trim().length === 0} onClick={() => slg("approve", false)}>{t(lang, "approve")}</button>
                  <button onClick={() => setDecision(null)}>{t(lang, "cancel")}</button>
                </div>
              </div>
            )}
            {confirming && (
              <div className="dialog" role="dialog" data-testid="confirm-dialog">
                <div>
                  <p><strong>{t(lang, "confirmApprove")}</strong></p>
                  <p>{brief.accountability.reviewer} · {brief.accountability.retention} · {brief.accountability.recipient}</p>
                  <div className="vote"><button className="primary" data-testid="confirm-approve" onClick={() => slg("approve", true)}>{t(lang, "confirmApprove")}</button>
                    <button onClick={() => setConfirming(false)}>{t(lang, "cancel")}</button></div>
                </div>
              </div>
            )}
            {error && <div className="error" role="alert">{error}</div>}
          </div>
        )}
        {!kgl && !brief.yours && brief.yourVote && <div>Your vote: <strong>{brief.yourVote.verdict}</strong>{brief.yourVote.reason && ` — ${brief.yourVote.reason}`}</div>}
      </div>
      <div className="card" data-testid="reveal">
        <h2>{t(lang, "reveal")}</h2>
        {!reveal && <div className="muted">{t(lang, "sealed")}</div>}
        {reveal && (
          <div>
            <div>machine: <strong>{reveal.machineCheck.verdict}</strong> / {reveal.machineCheck.rrsaClass} · commitment {reveal.commitmentOpens ? <span className="ok">opens ✓</span> : <span className="bad">DOES NOT OPEN</span>}</div>
            <div className={reveal.agreement ? "ok" : "warn"}>{reveal.agreement ? t(lang, "agreement") : t(lang, "disagreement")}</div>
            <ul>{reveal.machineCheck.findings.map((f, i) => <li key={i}>{f.rule} → {f.target}: {f.action}{f.detail ? ` — ${f.detail}` : ""}</li>)}</ul>
            {reveal.otherReviews && <div>Other reviewer(s): {reveal.otherReviews.map((o) => `${o.reviewer}: ${o.verdict}`).join("; ")}</div>}
          </div>
        )}
        {brief.status === "pending" && brief.votes >= brief.requiredReviews && <button className="primary" data-testid="resolve" onClick={resolve}>{t(lang, "resolve")}</button>}
        {brief.status === "pending" && brief.yourVote && brief.votes < brief.requiredReviews && <div className="muted">{t(lang, "waiting")}</div>}
        {resolved && <div className="ok">{resolved}</div>}
        {brief.status !== "pending" && <div>{brief.status}</div>}
      </div>
    </div>
  );
}
