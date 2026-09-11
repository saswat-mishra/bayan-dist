import { useEffect, useRef, useState } from "react";
import { api } from '../../../vhq7';
import type { Ctx } from '../../../App';
import { useGuard } from '../../../q1n';
import { Key, Lang, t } from '../../../gna';
import type { FeasRow } from '../../../wz0g';
import { EmptyState } from '../../../components/qg9b';
import { Codes, Iso, Term } from '../../../d7t';
import { AskBox, AskResult } from '../../../assistant/ppa';
import type { AskModel } from '../../../assistant/ppa';
import type { AssistantView, Skill } from '../../../wz0g';
export type QuestionGroup = "readyNow" | "needsSkill" | "notPermitted";
export const GROUPS: QuestionGroup[] = ["readyNow", "needsSkill", "notPermitted"];
export function groupOf(r: FeasRow): QuestionGroup {
    if (r.blocked)
        return "notPermitted";
    if (r.achievableD === null)
        return "needsSkill";
    return "readyNow";
}
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
export function minClassWords(r: FeasRow, lang: Lang): {
    words: string;
    fromPack: boolean;
} {
    const w = r.minClassWords?.[lang];
    if (w && w.trim())
        return { words: w, fromPack: true };
    return { words: lang === "ar" && r.minClass_ar ? r.minClass_ar : r.minClass, fromPack: false };
}
function Price({ r, lang }: {
    r: FeasRow;
    lang: Lang;
}) {
    if (r.blocked)
        return <p className="price muted" data-testid={`price-${r.question}`}>{t(lang, "blockedQ")}</p>;
    if (r.achievableD === null)
        return <p className="price" data-testid={`price-${r.question}`}>{t(lang, "noSkillYet")}</p>;
    const policy = /R1|policy-clear/.test(r.approvalPath);
    const mc = minClassWords(r, lang);
    return (<p className="price" data-testid={`price-${r.question}`}>
      {mc.fromPack ? <Iso>{mc.words}</Iso> : <Codes text={mc.words}/>}
      <span className="sep"> · </span><span className="nowrap"><Term code={`D${r.achievableD}`} showCode/></span>
      <span className="sep"> · </span>{policy ? t(lang, "releasesByPolicy") : pathWords(r, lang)}
      <span className="sep"> · </span>{r.realTime === null ? "—" : r.realTime ? t(lang, "instant") : t(lang, "needsDataPass")}
    </p>);
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
export function QuestionStep({ ctx, rows, skills, selected, onPick, assistant, askModel }: {
    ctx: Ctx;
    rows: FeasRow[];
    skills: Skill[];
    selected: FeasRow | null;
    onPick: (q: FeasRow) => void;
    assistant?: AssistantView | null;
    askModel?: AskModel;
}) {
    const { lang } = ctx;
    const [asking, setAsking] = useState<FeasRow | null>(null);
    const [result, setResult] = useState<AskResult | null>(null);
    const topRef = useRef<HTMLDivElement>(null);
    const top = result?.matches[0]?.question ?? null;
    const matched = new Map((result?.matches ?? []).map((m) => [m.question, m.because]));
    useEffect(() => {
        if (!top)
            return;
        const el = topRef.current;
        if (el && typeof el.scrollIntoView === "function") {
            try {
                el.scrollIntoView({ block: "nearest" });
            }
            catch { }
        }
    }, [top, result]);
    return (<div className="card" data-testid="step-question">
      <h2>{t(lang, "pickQuestion")}</h2>
      <AskBox rows={rows} skills={skills} lang={lang} result={result} onResult={setResult} assistant={assistant} askModel={askModel}/>
      {rows.length === 0 && <EmptyState text={t(lang, "loading")}/>}
      {rows.length > 0 && <p className="muted small ask-note">{t(lang, "askOneOfNine")}</p>}
      {GROUPS.map((g) => {
            const xs = rows.filter((r) => groupOf(r) === g);
            if (xs.length === 0)
                return null;
            return (<section key={g} className="qgroup" data-testid={`qgroup-${g}`} aria-label={t(lang, g as Key)}>
            <h3>{t(lang, g as Key)} <span className="muted">({xs.length})</span></h3>
            <div className="cards">
              {xs.map((r) => (<div key={r.question} ref={r.question === top ? topRef : undefined} className={"qcard" + (selected?.question === r.question ? " selected" : "") + (r.question === top ? " suggested" : "")} data-testid={`qcard-${r.question}`} data-group={g} data-matched={matched.has(r.question) || undefined} data-suggested={r.question === top || undefined}>
                  <h3 className="qcard-h"><button className="qcard-title" aria-pressed={selected?.question === r.question} data-testid={`question-${r.question}`} onClick={() => r.achievableD === null && !r.blocked ? setAsking(r) : onPick(r)} disabled={r.blocked}>{lang === "ar" ? r.text_ar : r.text}</button></h3>
                  <Price r={r} lang={lang}/>
                  {matched.has(r.question) && (result?.mode === "model"
                        ? <p className="matched-words micro muted" data-testid={`matched-${r.question}`}>{t(lang, "askByModel")}{r.question === top && result.why ? `: ${result.why}` : ""}</p>
                        : <p className="matched-words micro muted" data-testid={`matched-${r.question}`}>{t(lang, "askWhyMatched")}: {matched.get(r.question)!.join(", ")}</p>)}
                </div>))}
            </div>
          </section>);
        })}
      {asking && <SkillRequestForm ctx={ctx} q={asking} onDone={() => undefined}/>}
    </div>);
}
