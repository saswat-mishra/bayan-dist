import { Lang, t } from '../../gna';
import type { Brief, Reveal } from '../../wz0g';
import { Technical } from '../../components/n4x';
export function RevealCard({ brief, reveal, lang }: {
    brief: Brief;
    reveal: Reveal | null;
    lang: Lang;
}) {
    const rec = reveal?.machineCheck.recommendation;
    const basis = reveal?.machineCheck.recommendationBasis ?? [];
    return (<div className="card" data-testid="reveal">
      <h2>{t(lang, "reveal")}</h2>
      {!reveal && <div className="muted">{t(lang, "sealed")}</div>}
      {reveal && (<div>
          <p data-testid="recommendation">
            <strong>{t(lang, "machineRecommended")} {rec === "approve" ? t(lang, "recApprove") : t(lang, "recChanges")}</strong>
            {basis.length > 0 && <span className="muted" data-gate-text="true">, {t(lang, "because")} {basis.join("; ")}</span>}
          </p>
          <p data-testid="your-vote"><strong>{reveal.yourVote.verdict === "approve" ? t(lang, "youApproved") : t(lang, "youRejected")}</strong>{reveal.yourVote.reason && <span className="muted"> — {reveal.yourVote.reason}</span>}</p>
          <p data-testid="seal" className={reveal.commitmentOpens ? "ok" : "bad"}>{reveal.commitmentOpens ? t(lang, "sealOpened") : t(lang, "sealFailed")}</p>
          <p className={reveal.agreement ? "ok" : "warn"} data-testid="agreement">{reveal.agreement ? t(lang, "agreement") : t(lang, "disagreement")}</p>
          {reveal.otherReviews && <p>{t(lang, "otherReviewers")}: {reveal.otherReviews.map((o) => `${o.reviewer}: ${o.verdict}`).join("; ")}</p>}
          <Technical lang={lang} testid="reveal-technical">
            {t(lang, "machineVerdict")}: {reveal.machineCheck.verdict} · {t(lang, "rrsaLabel")}: {reveal.machineCheck.rrsaClass}{"\n"}
            {t(lang, "commitment")}: {reveal.machineCheck.commitment}{"\n"}
            {t(lang, "findingsLabel")}:{"\n"}
            {reveal.machineCheck.findings.filter((f) => f.action !== "pass").map((f, i) => `  ${f.rule} → ${f.target}: ${f.action}${f.detail ? ` — ${f.detail}` : ""}`).join("\n")}
          </Technical>
        </div>)}
      {brief.status === "pending" && brief.yourVote && brief.votes < brief.requiredReviews && (<div className="muted" data-testid="blinded">{t(lang, "blindedUntil")} {(brief.outstandingReviewers?.length ?? 0) > 0
                ? t(lang, "waitingForNamed").replace("{names}", brief.outstandingReviewers!.map((o) => o.displayName).join(", "))
                : t(lang, "waiting")}</div>)}
      {brief.status !== "pending" && <div className={brief.status === "released" ? "ok" : "bad"} data-testid="outcome" role="status">{brief.status === "released" ? t(lang, "outcomeReleased") : t(lang, "outcomeRefused")}</div>}
    </div>);
}
