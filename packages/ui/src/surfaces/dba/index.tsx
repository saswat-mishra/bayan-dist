import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Lang, t } from '../../gna';
import type { FieldClass, Skill, SkillColumn } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
import { Progress } from '../../components/nv8';
import { Page } from '../../components/gct';
import { go } from '../../q1n';
import { Bi, Codes, Iso, Name, Term, TermLine } from '../../d7t';
import { FieldTable, ReclassifyForm, recertWords } from './oyi1';
export { CLASSES, recertWords } from './oyi1';
type Recert = {
    skill: string;
    before: number;
    after: number;
}[];
function PackTags({ f, lang }: {
    f: FieldClass;
    lang: Lang;
}) {
    const tags = Array.isArray(f.guidance.tags) ? (f.guidance.tags as string[]) : [];
    if (tags.length === 0)
        return null;
    return <> · {t(lang, "colTags")}: <span className="tags" data-technical="true" data-testid={`tags-${f.field}`}>{tags.map((g) => <code key={g}>{g}</code>)}</span></>;
}
function FieldCard({ f, ctx, onDone }: {
    f: FieldClass;
    ctx: Ctx;
    onDone: (msg: string) => void;
}) {
    const { user, lang, dep } = ctx;
    const [mode, setMode] = useState<"idle" | "reclassify">("idle");
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
            onDone(`${t(lang, "ratifiedNow")}: ${recertWords(r.recertified, lang)}`);
    }
    return (<div className={"field-card" + (f.ratified ? "" : " unratified")} data-testid={`field-${f.field}`} data-ratified={f.ratified}>
      <h3><Iso>{f.field}</Iso> <span className="muted">— <Term code={f.class} showCode/></span></h3>
      <div className="impact" data-testid={`impact-${f.field}`}><strong>{t(lang, "whatDepends")}:</strong> <span data-gate-text="true"><Bi x={{ en: f.impact.text, ar: f.impact.text_ar }} lang={lang}/></span>{f.impact.cappedAtD1.length > 0 && <div className="muted"><Iso>{f.impact.cappedAtD1.join(", ")}</Iso></div>}</div>
      <div className="muted">{f.ratified ? <>{t(lang, "ratifiedWord")} · <Name name={f.ratifiedByName ?? f.ratifiedBy ?? ""} lang={lang}/></> : <span className="warn">{t(lang, "unratifiedWord")} · {t(lang, "proposedByVendor")}</span>}</div>
      <div className="muted small"><TermLine code={f.class}/>{packClass && packClass !== f.class && <> · {t(lang, "packClassLabel")}: <Term code={packClass} showCode/></>}<PackTags f={f} lang={lang}/></div>
      {error && <div className="error" role="alert">{error}</div>}
      {mode === "idle" ? (<div className="vote">
          {!f.ratified && <button className="primary" onClick={ratify} disabled={busy} data-testid={`ratify-${f.field}`}>{t(lang, "ratify")}</button>}
          <button onClick={() => setMode("reclassify")} disabled={busy} data-testid={`reclassify-${f.field}`}>{t(lang, "reclassifyAs")}</button>
          {busy && <Progress label={t(lang, "loading")}/>}
        </div>) : <ReclassifyForm f={f} ctx={ctx} onDone={(m) => { setMode("idle"); onDone(m); }} onCancel={() => setMode("idle")}/>}
    </div>);
}
export function EmitsList({ skill, columns, lang }: {
    skill: string;
    columns: SkillColumn[];
    lang: Lang;
}) {
    return (<ul className="emits small" data-testid={`emits-${skill}`} aria-label={t(lang, "whatItEmits")}>
      <li className="muted">{t(lang, "whatItEmits")}</li>
      {columns.map((c) => (<li key={c.name} data-testid={`emit-${skill}-${c.name}`}>
          <strong><Iso>{c.name}</Iso></strong> — <Term code={c.class} showCode/>{c.transform && <> · <Term code={c.transform} showCode/></>}
          {c.tags.length > 0 && <> · <span className="tags" data-technical="true">{c.tags.map((g) => <code key={g} title={c.packTags.includes(g) ? t(lang, "packTagsLabel") : undefined} data-pack-tag={c.packTags.includes(g)}>{g}</code>)}</span></>}
          <span className="muted"> · {c.sources.length ? <>{t(lang, "derivedFrom")} <Iso>{c.sources.join(", ")}</Iso></> : t(lang, "computedNoSource")}</span>
        </li>))}
    </ul>);
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
          <div><strong><Iso>{lang === "ar" ? s.description_ar : s.description}</Iso></strong> <span className="muted">· <Iso>{s.name}@{s.version}</Iso></span></div>
          <div data-testid={`effect-${s.name}`}><Codes text={effectSentence(s, lang)}/> <span className="muted">(<Term code={s.riskClass}/> · <Term code={`D${s.maxGradeD}`} showCode/>)</span></div>
          {s.columns && s.columns.length > 0 && <EmitsList skill={s.name} columns={s.columns} lang={lang}/>}
          {declining === s.name ? (<div>
              <label>{t(lang, "refuseReason")}<textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} data-testid={`refuse-reason-${s.name}`}/></label>
              <div className="vote"><button onClick={() => refuse(s)} disabled={reason.trim().length < 20} data-testid={`refuse-submit-${s.name}`}>{t(lang, "refuseCosign").replace("…", "")}</button><button onClick={() => setDeclining(null)}>{t(lang, "cancelWord")}</button></div>
            </div>) : (<div className="vote"><button className="primary" onClick={() => cosign(s)} data-testid={`cosign-${s.name}`}>{t(lang, "cosign")}</button><button onClick={() => setDeclining(s.name)} data-testid={`refuse-${s.name}`}>{t(lang, "refuseCosign")}</button></div>)}
        </div>))}
    </div>);
}
export function DbaPages({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, deps, page } = ctx;
    const [rows, setRows] = useState<FieldClass[] | null>(null);
    const [done, setDone] = useState<string | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<FieldClass[]>(`/v1/field-classes?deployment=${dep}`, user)).then((r) => r && setRows(r)), [dep, user, guard]);
    useEffect(() => { setDone(null); load(); }, [load]);
    const d = deps.find((x) => x.id === dep);
    const name = lang === "ar" && d?.name_ar ? d.name_ar : d?.name ?? dep;
    const sorted = [...(rows ?? [])].sort((a, b) => a.field.localeCompare(b.field));
    const awaiting = sorted.filter((f) => !f.ratified), ratified = sorted.filter((f) => f.ratified);
    const notices = <>{error && <div className="error" role="alert">{error}</div>}{done && <div className="ok" role="status" data-testid="ratified"><Codes text={done}/></div>}</>;
    if (page === "fields") {
        return (<Page title={t(lang, "pageFields")} intro={t(lang, "introFields")} testid={rows ? "field-classes" : undefined}>
        {notices}
        <div className="card">
          <h2>{t(lang, "ratifiedFields")} — <Iso>{name}</Iso> <span className="muted">({ratified.length})</span></h2>
          {rows && rows.length === 0 && <EmptyState text={t(lang, "noFields")}/>}
          {ratified.length > 0 && <section data-testid="ratified-fields"><FieldTable rows={ratified} ctx={ctx} onDone={(m) => { setDone(m); load(); }}/></section>}
        </div>
      </Page>);
    }
    return (<Page title={t(lang, "pageDecisions")} intro={t(lang, "introDecisions")} testid={rows ? "decisions" : undefined}>   
      {notices}
      <div className="card">
        <h2>{t(lang, "awaiting")} — <Iso>{name}</Iso> <span className="muted">({awaiting.length})</span></h2>
        {rows && awaiting.length === 0 && <EmptyState text={t(lang, "noneAwaitingFields")} testid="none-awaiting-fields"/>}
        {awaiting.length > 0 && <section data-testid="awaiting"><div className="cards cards-wide">{awaiting.map((f) => <FieldCard key={f.field} f={f} ctx={ctx} onDone={(m) => { setDone(m); load(); go("fields"); }}/>)}</div></section>}
      </div>
      
      <AwaitingSkills ctx={ctx} onDone={(m) => { setDone(m); load(); }}/>
    </Page>);
}
