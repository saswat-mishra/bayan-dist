import { Lang, t } from '../../gna';
import type { Brief, Reveal } from '../../wz0g';
export function RevealCard({ brief, reveal, lang }: {
    brief: Brief;
    reveal: Reveal | null;
    lang: Lang;
}) {
    return (<div className="card" data-testid="reveal">
      <h2>{t(lang, "reveal")}</h2>
      {!reveal && <div className="muted">{t(lang, "sealed")}</div>}
      {reveal && (<div>
          <div>machine: <strong>{reveal.machineCheck.verdict}</strong> / {reveal.machineCheck.rrsaClass} · commitment {reveal.commitmentOpens ? <span className="ok">opens ✓</span> : <span className="bad">DOES NOT OPEN</span>}</div>
          {reveal.machineCheck.recommendation && <div data-testid="recommendation"><strong>{t(lang, "recommendationLabel")}:</strong> {reveal.machineCheck.recommendation}
            {reveal.machineCheck.recommendationBasis && reveal.machineCheck.recommendationBasis.length > 0 && <span className="muted"> — {t(lang, "basis")}: {reveal.machineCheck.recommendationBasis.join("; ")}</span>}</div>}
          <div className={reveal.agreement ? "ok" : "warn"}>{reveal.agreement ? t(lang, "agreement") : t(lang, "disagreement")}</div>
          <ul>{reveal.machineCheck.findings.filter((f) => f.action !== "pass").map((f, i) => <li key={i}>{f.rule} → {f.target}: {f.action}{f.detail ? ` — ${f.detail}` : ""}</li>)}</ul>
          {reveal.otherReviews && <div>Other reviewer(s): {reveal.otherReviews.map((o) => `${o.reviewer}: ${o.verdict}`).join("; ")}</div>}
        </div>)}
      {brief.status === "pending" && brief.yourVote && brief.votes < brief.requiredReviews && <div className="muted" data-testid="blinded">{t(lang, "blindedUntil")} {t(lang, "waiting")}</div>}
      {brief.status !== "pending" && <div className={brief.status === "released" ? "ok" : "bad"} data-testid="outcome" role="status">{brief.status === "released" ? t(lang, "outcomeReleased") : t(lang, "outcomeRefused")}</div>}
    </div>);
}
