import { useState } from "react";
import { api } from '../../../vhq7';
import type { Ctx } from '../../../App';
import { useGuard } from '../../../q1n';
import { Lang, t } from '../../../gna';
import type { FeasRow } from '../../../wz0g';
import { EmptyState } from '../../../components/qg9b';
import { Codes, Term } from '../../../d7t';
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
export function minClassWords(r: FeasRow, lang: Lang): string {
    if (lang === "ar" && r.minClass_ar)
        return r.minClass_ar;
    return r.minClass;
}
function Price({ r, lang }: {
    r: FeasRow;
    lang: Lang;
}) {
    if (r.blocked)
        return <div className="muted">{t(lang, "blockedQ")}</div>;
    if (r.achievableD === null)
        return <div className="warn">{t(lang, "noSkillYet")}</div>;
    const policy = /R1|policy-clear/.test(r.approvalPath);
    return (<div className="price">
      <span><Codes text={minClassWords(r, lang)}/></span> · <Term code={`D${r.achievableD}`} showCode/> · {policy ? t(lang, "releasesByPolicy") : pathWords(r, lang)} · {r.realTime === null ? "—" : r.realTime ? t(lang, "instant") : t(lang, "needsDataPass")}
    </div>);
}
function SkillRequestForm({ ctx, q, onDone }: {
    ctx: Ctx;
    q: FeasRow;
    onDone: () => void;
}) {
    const { user, lang, dep } = ctx;
    const [why, setWhy] = useState("");
    const [fields, setFields] = useState("");
    const [done, setDone] = useState(false);
    const [error, guard] = useGuard(lang);
    async function submit() {
        const r = await guard(api("/v1/skill-requests", user, { method: "POST", body: { deployment: dep, question: q.question, fieldsNeeded: fields.split(",").map((s) => s.trim()).filter(Boolean), why } }));
        if (r) {
            setDone(true);
            onDone();
        }
    }
    return (<div className="card" data-testid="skill-request-form">
      <h2>{t(lang, "requestASkill")} — {lang === "ar" ? q.text_ar : q.text}</h2>
      {done ? <div className="ok" role="status" data-testid="skill-requested">{t(lang, "skillRequested")}</div> : (<>
          <label>{t(lang, "skillRequestFields")}<input value={fields} onChange={(e) => setFields(e.target.value)} data-testid="skill-request-fields"/></label>
          <label>{t(lang, "skillRequestWhy")}<textarea rows={3} value={why} onChange={(e) => setWhy(e.target.value)} data-testid="skill-request-why"/></label>
          <div className="vote"><button className="primary" disabled={why.trim().length < 20 || !fields.trim()} onClick={submit} data-testid="skill-request-submit">{t(lang, "requestASkill")}</button></div>
          {error && <div className="error" role="alert">{error}</div>}
        </>)}
    </div>);
}
export function QuestionStep({ ctx, rows, selected, onPick }: {
    ctx: Ctx;
    rows: FeasRow[];
    selected: FeasRow | null;
    onPick: (q: FeasRow) => void;
}) {
    const { lang } = ctx;
    const [asking, setAsking] = useState<FeasRow | null>(null);
    return (<div className="card" data-testid="step-question">
      <h2>{t(lang, "pickQuestion")}</h2>
      {rows.length === 0 && <EmptyState text={t(lang, "loading")}/>}
      <div className="cards">
        {rows.map((r) => (<div key={r.question} className={"qcard" + (selected?.question === r.question ? " selected" : "")} data-testid={`qcard-${r.question}`}>
            <button className="qcard-title" aria-pressed={selected?.question === r.question} data-testid={`question-${r.question}`} onClick={() => r.achievableD === null && !r.blocked ? setAsking(r) : onPick(r)} disabled={r.blocked}><strong>{lang === "ar" ? r.text_ar : r.text}</strong></button>
            <Price r={r} lang={lang}/>
          </div>))}
      </div>
      {asking && <SkillRequestForm ctx={ctx} q={asking} onDone={() => undefined}/>}
    </div>);
}
