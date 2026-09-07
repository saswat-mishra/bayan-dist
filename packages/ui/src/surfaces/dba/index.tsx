import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Lang, t } from '../../gna';
import type { FieldClass, Skill } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
import { Progress } from '../../components/nv8';
import { Bi, Codes, Term, TermLine, formatDate } from '../../d7t';
export const CLASSES = ["DIRECT", "QUASI", "SENSITIVE", "STRUCTURAL", "VENDOR", "FREETEXT"];
type Recert = {
    skill: string;
    before: number;
    after: number;
}[];
export function recertWords(rows: Recert): string {
    return rows.filter((c) => c.before !== c.after).map((c) => `${c.skill} D${c.before}→D${c.after}`).join(", ") || "—";
}
function FieldCard({ f, ctx, onDone }: {
    f: FieldClass;
    ctx: Ctx;
    onDone: (msg: string) => void;
}) {
    const { user, lang, dep } = ctx;
    const [mode, setMode] = useState<"idle" | "reclassify">("idle");
    const [cls, setCls] = useState(f.class);
    const [reason, setReason] = useState("");
    const [busy, setBusy] = useState(false);
    const [error, guard] = useGuard(lang);
    const packClass = typeof f.guidance.class === "string" ? f.guidance.class : null;
    async function ratify() {
        setBusy(true);
        const r = await guard(api<{
            recertified: Recert;
        }>(`/v1/field-classes/${encodeURIComponent(f.field)}/ratify`, user, { method: "POST", body: { deployment: dep } }));
        setBusy(false);
        if (r)
            onDone(`${t(lang, "ratifiedNow")}: ${recertWords(r.recertified)}`);
    }
    async function reclassify() {
        setBusy(true);
        const r = await guard(api<{
            recertified: Recert;
        }>(`/v1/field-classes/${encodeURIComponent(f.field)}/reclassify`, user, { method: "POST", body: { deployment: dep, class: cls, reason } }));
        setBusy(false);
        if (r) {
            setMode("idle");
            setReason("");
            onDone(`${t(lang, "reclassified")}: ${recertWords(r.recertified)}`);
        }
    }
    return (<div className={"field-card" + (f.ratified ? "" : " unratified")} data-testid={`field-${f.field}`} data-ratified={f.ratified}>
      <h3>{f.field} <span className="muted">— <Term code={f.class} showCode/></span></h3>
      <div className="impact" data-testid={`impact-${f.field}`}><strong>{t(lang, "whatDepends")}:</strong> <span data-gate-text="true"><Bi x={{ en: f.impact.text, ar: f.impact.text_ar }} lang={lang}/></span>{f.impact.cappedAtD1.length > 0 && <div className="muted">{f.impact.cappedAtD1.join(", ")}</div>}</div>
      <div className="muted">{f.ratified ? <>{t(lang, "ratifiedWord")} · {f.ratifiedBy}{f.ratifiedAt && ` · ${formatDate(f.ratifiedAt, lang)}`}</> : <span className="warn">{t(lang, "unratifiedWord")} · {t(lang, "proposedByVendor")}</span>}</div>
      <div className="muted small"><TermLine code={f.class}/>{packClass && packClass !== f.class && <> · {t(lang, "packClassLabel")}: <Term code={packClass} showCode/></>}</div>
      {error && <div className="error" role="alert">{error}</div>}
      {mode === "idle" ? (<div className="vote">
          {!f.ratified && <button className="primary" onClick={ratify} disabled={busy} data-testid={`ratify-${f.field}`}>{t(lang, "ratify")}</button>}
          <button onClick={() => setMode("reclassify")} disabled={busy} data-testid={`reclassify-${f.field}`}>{t(lang, "reclassifyAs")}</button>
          {busy && <Progress label={t(lang, "loading")}/>}
        </div>) : (<div className="reclassify-form" data-testid={`reclassify-form-${f.field}`}>
          <label>{t(lang, "chooseClass")}{" "}
            <select value={cls} onChange={(e) => setCls(e.target.value)} data-testid={`class-${f.field}`}>{CLASSES.map((c) => <option key={c} value={c}>{c}</option>)}</select></label>
          <label>{t(lang, "reasonForReclassification")}<textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} data-testid={`reason-${f.field}`}/></label>
          <div className="vote">
            <button className="primary" onClick={reclassify} disabled={busy || reason.trim().length < 20 || cls === f.class} data-testid={`reclassify-submit-${f.field}`}>{t(lang, "reclassify")}</button>
            <button onClick={() => setMode("idle")}>{t(lang, "cancelWord")}</button>
          </div>
        </div>)}
    </div>);
}
export function effectSentence(s: Skill, lang: Lang): string {
    return s.riskClass === "green" && s.maxGradeD >= 2 ? t(lang, "cosignEffectPolicy").replace("{d}", String(s.maxGradeD)) : t(lang, "cosignEffectReview").replace("{risk}", s.riskClass);
}
function AwaitingSkills({ ctx, onDone }: {
    ctx: Ctx;
    onDone: (msg: string) => void;
}) {
    const { user, lang, dep } = ctx;
    const [rows, setRows] = useState<Skill[] | null>(null);
    const [declining, setDeclining] = useState<string | null>(null);
    const [reason, setReason] = useState("");
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<Skill[]>(`/v1/skills?deployment=${dep}&awaiting=1`, user)).then((r) => r && setRows(r)), [dep, user, guard]);
    useEffect(() => { load(); }, [load]);
    async function cosign(s: Skill) { if (await guard(api(`/v1/skills/${s.name}/${s.version}/certify`, user, { method: "POST", body: { deployment: dep } }))) {
        onDone(t(lang, "cosigned"));
        load();
    } }
    async function refuse(s: Skill) { if (await guard(api(`/v1/skills/${s.name}/${s.version}/refuse-certification`, user, { method: "POST", body: { deployment: dep, reason } }))) {
        setDeclining(null);
        setReason("");
        onDone(t(lang, "cosignDeclined"));
        load();
    } }
    return (<div className="card" data-testid="awaiting-cosign">
      <h2>{t(lang, "awaitingCosign")}</h2>
      {error && <div className="error" role="alert">{error}</div>}
      {rows && rows.length === 0 && <EmptyState text={t(lang, "noneAwaiting")} testid="none-awaiting"/>}
      {(rows ?? []).map((s) => (<div key={s.name} className="block" data-testid={`awaiting-${s.name}`}>
          <div><strong>{lang === "ar" ? s.description_ar : s.description}</strong> <span className="muted">· {s.name}@{s.version}</span></div>
          <div data-testid={`effect-${s.name}`}><Codes text={effectSentence(s, lang)}/> <span className="muted">(<Term code={s.riskClass}/> · <Term code={`D${s.maxGradeD}`} showCode/>)</span></div>
          {declining === s.name ? (<div>
              <label>{t(lang, "refuseReason")}<textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} data-testid={`refuse-reason-${s.name}`}/></label>
              <div className="vote"><button className="danger" onClick={() => refuse(s)} disabled={reason.trim().length < 20} data-testid={`refuse-submit-${s.name}`}>{t(lang, "refuseCosign").replace("…", "")}</button><button onClick={() => setDeclining(null)}>{t(lang, "cancelWord")}</button></div>
            </div>) : (<div className="vote"><button className="primary" onClick={() => cosign(s)} data-testid={`cosign-${s.name}`}>{t(lang, "cosign")}</button><button onClick={() => setDeclining(s.name)} data-testid={`refuse-${s.name}`}>{t(lang, "refuseCosign")}</button></div>)}
        </div>))}
    </div>);
}
export function DbaPages({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, deps } = ctx;
    const [rows, setRows] = useState<FieldClass[] | null>(null);
    const [done, setDone] = useState<string | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<FieldClass[]>(`/v1/field-classes?deployment=${dep}`, user)).then((r) => r && setRows(r)), [dep, user, guard]);
    useEffect(() => { setDone(null); load(); }, [load]);
    const d = deps.find((x) => x.id === dep);
    const sorted = [...(rows ?? [])].sort((a, b) => Number(a.ratified) - Number(b.ratified) || a.field.localeCompare(b.field));
    return (<div data-testid="field-classes">
      <div className="card">
        <h2>{t(lang, "fieldClasses")} — {lang === "ar" && d?.name_ar ? d.name_ar : d?.name ?? dep}</h2>
        {error && <div className="error" role="alert">{error}</div>}
        {done && <div className="ok" role="status" data-testid="ratified"><Codes text={done}/></div>}
        {rows && rows.length === 0 && <EmptyState text={t(lang, "noFields")}/>}
        <div className="cards">{sorted.map((f) => <FieldCard key={f.field} f={f} ctx={ctx} onDone={(m) => { setDone(m); load(); }}/>)}</div>
      </div>
      <AwaitingSkills ctx={ctx} onDone={(m) => { setDone(m); load(); }}/>
    </div>);
}
