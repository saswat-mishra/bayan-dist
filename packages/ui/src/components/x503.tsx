import { useState } from "react";
import { Lang, t } from '../gna';
import type { Certificate } from '../wz0g';
import { Codes, Term, TermLine, useTerm } from '../d7t';
export function explainReviewers(cert: Certificate, lang: Lang, threshold = 2): string {
    if (cert.required_r <= 1 && cert.releasable)
        return t(lang, "explainNoReviewers");
    const n = cert.required_r === 2 ? 1 : threshold;
    const b = cert.d_blockers[0];
    const blocker = b ? (lang === "ar" ? `${b.field} (${b.field_class})` : `${b.field} (${b.field_class.toLowerCase().replace("_", " ")})`) : `D${cert.d}`;
    return t(lang, "explainReviewersBody").replace("{n}", String(n)).replace("{blocker}", blocker);
}
export function explainPolicy(cert: Certificate, lang: Lang, recommended?: string | null): string {
    if (cert.required_r <= 1 && cert.releasable)
        return t(lang, "explainAlreadyPolicy");
    if (recommended)
        return t(lang, "explainPolicyBody").replace("{option}", recommended);
    if (cert.nearest_releasable && cert.nearest_releasable.required_r <= 1)
        return t(lang, "explainPolicyBody").replace("{option}", `${t(lang, "dropField")} ${cert.nearest_releasable.dropped.join(", ")}`);
    return t(lang, "explainPolicyNone");
}
export function ExplainThis({ cert, lang, recommended, threshold, testid }: {
    cert: Certificate;
    lang: Lang;
    recommended?: string | null;
    threshold?: number;
    testid?: string;
}) {
    const [open, setOpen] = useState(false);
    const failed = cert.gates.filter((g) => !g.passed);
    const kindTerm = useTerm(cert.headline?.kind ?? "needs-review");
    return (<div className="explain" data-testid={testid ?? "explain"}>
      <button type="button" className="link" aria-expanded={open} onClick={() => setOpen(!open)} data-testid="explain-toggle" aria-label={t(lang, "explainThis")}>? {t(lang, "explainThis")}</button>
      {open && (<div className="explain-panel" role="region" aria-label={t(lang, "explainThis")}>
          <div className="muted small">{t(lang, "explainNotEvidence")}</div>
          {kindTerm && <p><strong>{kindTerm.label}</strong> — {kindTerm.line}</p>}
          <h4>{t(lang, "explainWhyReviewers")}</h4>
          <p data-testid="explain-reviewers"><Codes text={explainReviewers(cert, lang, threshold)}/></p>
          <h4>{t(lang, "explainPolicy")}</h4>
          <p data-testid="explain-policy"><Codes text={explainPolicy(cert, lang, recommended)}/></p>
          {failed.length > 0 && <><h4>{t(lang, "explainGate")}</h4>{failed.map((g) => <p key={g.name}><Term code={g.name}/> — <TermLine code={g.name}/></p>)}</>}
        </div>)}
    </div>);
}
