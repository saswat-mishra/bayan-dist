import { useState } from "react";
import { Lang, t } from '../gna';
import type { Certificate, Recommendation } from '../wz0g';
import { pathWordsFor, recommendationWords } from '../b3w';
import { Codes, Iso, Term, TermLine, useTerm } from '../d7t';
export function explainReviewers(cert: Certificate, lang: Lang, threshold = 2): string {
    if (cert.required_r <= 1 && cert.releasable)
        return t(lang, "explainNoReviewers");
    const n = cert.required_r === 2 ? 1 : threshold;
    const b = cert.d_blockers[0];
    const blocker = b ? `${b.field} (${b.field_class})` : `D${cert.d}`;
    return t(lang, "explainReviewersBody").replace("{n}", String(n)).replace("{blocker}", blocker);
}
export function explainPolicy(cert: Certificate, lang: Lang, rec?: Recommendation | null): {
    tpl: string;
    option: string | null;
    fields: string | null;
} {
    if (cert.required_r <= 1 && cert.releasable)
        return { tpl: t(lang, "explainAlreadyPolicy"), option: null, fields: null };
    if (rec && rec.reachesTarget) {
        const words = recommendationWords(rec, lang);
        if (rec.requiredR === "R1" || rec.requiredR === "R0")
            return { tpl: t(lang, "explainPolicyBody"), option: words, fields: null };
        return { tpl: t(lang, "explainPolicyStill").replace("{path}", pathWordsFor(rec.requiredR, lang)), option: words, fields: null };
    }
    if (cert.nearest_releasable && cert.nearest_releasable.required_r <= 1)
        return { tpl: t(lang, "explainNearestDrops"), option: null, fields: cert.nearest_releasable.dropped.join(", ") };
    return { tpl: t(lang, "explainPolicyNone"), option: null, fields: null };
}
export function explainPolicyText(cert: Certificate, lang: Lang, rec?: Recommendation | null): string {
    const e = explainPolicy(cert, lang, rec);
    return e.tpl.replace("{option}", e.option ?? "").replace("{fields}", e.fields ?? "");
}
export function ExplainThis({ cert, lang, recommendation, threshold, testid }: {
    cert: Certificate;
    lang: Lang;
    recommendation?: Recommendation | null;
    threshold?: number;
    testid?: string;
}) {
    const [open, setOpen] = useState(false);
    const failed = cert.gates.filter((g) => !g.passed);
    const kindTerm = useTerm(cert.headline?.kind ?? "needs-review");
    const policy = explainPolicy(cert, lang, recommendation);
    const parts = policy.tpl.split(/(\{option\}|\{fields\})/);
    return (<div className="explain" data-testid={testid ?? "explain"}>
      <button type="button" className="link" aria-expanded={open} onClick={() => setOpen(!open)} data-testid="explain-toggle" aria-label={t(lang, "explainThis")}>? {t(lang, "explainThis")}</button>
      {open && (<div className="explain-panel" role="region" aria-label={t(lang, "explainThis")}>
          <div className="muted small">{t(lang, "explainNotEvidence")}</div>
          {kindTerm && <p><strong>{kindTerm.label}</strong> — {kindTerm.line}</p>}
          <h4>{t(lang, "explainWhyReviewers")}</h4>
          <p data-testid="explain-reviewers"><Codes text={explainReviewers(cert, lang, threshold)}/></p>
          <h4>{t(lang, "explainPolicy")}</h4>
          <p data-testid="explain-policy">{parts.map((p, i) => p === "{option}" ? <span key={i} data-testid="explain-recommendation"><Codes text={policy.option ?? ""}/></span>
                : p === "{fields}" ? <Iso key={i}>{policy.fields ?? ""}</Iso> : <Codes key={i} text={p}/>)}</p>
          {failed.length > 0 && <><h4>{t(lang, "explainGate")}</h4>{failed.map((g) => <p key={g.name}><Term code={g.name}/> — <TermLine code={g.name}/></p>)}</>}
        </div>)}
    </div>);
}
