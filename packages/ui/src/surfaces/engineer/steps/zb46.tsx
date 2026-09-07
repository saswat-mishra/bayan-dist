import { Lang, t } from '../../../gna';
import type { FeasRow } from '../../../wz0g';
import { EmptyState } from '../../../components/qg9b';
export function pathWords(r: FeasRow, lang: Lang): string {
    if (r.blocked)
        return t(lang, "blockedQ");
    if (r.achievableD === null)
        return t(lang, "authorSkill");
    if (/R1|policy-clear/.test(r.approvalPath))
        return t(lang, "noReviewer");
    if (/R3|two/.test(r.approvalPath))
        return t(lang, "twoReviewers");
    return t(lang, "oneReviewer");
}
export function QuestionStep({ rows, lang, selected, onPick }: {
    rows: FeasRow[];
    lang: Lang;
    selected: FeasRow | null;
    onPick: (q: FeasRow) => void;
}) {
    return (<div className="card" data-testid="step-question">
      <h2>{t(lang, "pickQuestion")}</h2>
      {rows.length === 0 && <EmptyState text={t(lang, "loading")}/>}
      <div className="cards">
        {rows.map((r) => (<button key={r.question} className="qcard" aria-pressed={selected?.question === r.question} data-testid={`question-${r.question}`} onClick={() => onPick(r)} disabled={r.blocked || r.achievableD === null}>
            <div><strong>{lang === "ar" ? r.text_ar : r.text}</strong></div>
            <div className="muted">{t(lang, "minClass")}: {r.minClass}</div>
            <div>{t(lang, "achievable")}: {r.achievableD === null ? "—" : `D${r.achievableD}`} · {pathWords(r, lang)} · {r.realTime === null ? "—" : r.realTime ? t(lang, "realTime") : t(lang, "async")}</div>
          </button>))}
      </div>
    </div>);
}
