import { useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Lang, t } from '../../gna';
import type { FieldClass } from '../../wz0g';
import { Iso, Name, Term, formatDate, useTerm } from '../../d7t';
export const STRICTNESS = ["STRUCTURAL", "VENDOR", "QUASI", "SENSITIVE", "DIRECT", "FREETEXT"] as const;
export const CLASSES: string[] = [...STRICTNESS];
export function direction(from: string, to: string, lang: Lang): string {
    const a = STRICTNESS.indexOf(from as (typeof STRICTNESS)[number]), b = STRICTNESS.indexOf(to as (typeof STRICTNESS)[number]);
    if (a < 0 || b < 0 || a === b)
        return t(lang, "sameStrictness");
    return b > a ? t(lang, "stricter") : t(lang, "looser");
}
type Recert = {
    skill: string;
    before: number;
    after: number;
}[];
export function recertWords(rows: Recert, lang: Lang): string {
    return rows.filter((c) => c.before !== c.after).map((c) => `${c.skill} D${c.before}→D${c.after}`).join(", ") || t(lang, "noGradeChanged");
}
function ClassOption({ code, from, lang }: {
    code: string;
    from: string;
    lang: Lang;
}) {
    const entry = useTerm(code);
    return <option value={code} disabled={code === from}>{entry?.label ?? code} — {code === from ? t(lang, "chooseClass") : direction(from, code, lang)}</option>;
}
export function ReclassifyForm({ f, ctx, onDone, onCancel }: {
    f: FieldClass;
    ctx: Ctx;
    onDone: (msg: string) => void;
    onCancel: () => void;
}) {
    const { user, lang, dep } = ctx;
    const [cls, setCls] = useState(f.class);
    const [reason, setReason] = useState("");
    const [busy, setBusy] = useState(false);
    const [error, guard] = useGuard(lang);
    async function reclassify() {
        setBusy(true);
        const r = await guard(api<{
            recertified: Recert;
        }>(`/v1/field-classes/${encodeURIComponent(f.field)}/reclassify`, user, { method: "POST", body: { deployment: dep, class: cls, reason } }));
        setBusy(false);
        if (r)
            onDone(`${t(lang, "reclassified")}: ${recertWords(r.recertified, lang)}`);
    }
    return (<div className="reclassify-form" data-testid={`reclassify-form-${f.field}`}>
      <label>{t(lang, "chooseClass")}{" "}
        <select value={cls} onChange={(e) => setCls(e.target.value)} data-testid={`class-${f.field}`}>{STRICTNESS.map((c) => <ClassOption key={c} code={c} from={f.class} lang={lang}/>)}</select></label>
      {cls !== f.class && <p className="muted small" data-testid={`direction-${f.field}`}><Term code={cls} showCode/> — {direction(f.class, cls, lang)}</p>}
      <label>{t(lang, "reasonForReclassification")}<textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} data-testid={`reason-${f.field}`}/></label>
      <div className="vote">
        <button className="primary" onClick={reclassify} disabled={busy || reason.trim().length < 20 || cls === f.class} data-testid={`reclassify-submit-${f.field}`}>{t(lang, "reclassify")}</button>
        <button onClick={onCancel} disabled={busy}>{t(lang, "cancelWord")}</button>
      </div>
      {error && <div className="error" role="alert">{error}</div>}
    </div>);
}
export function FieldTable({ rows, ctx, onDone }: {
    rows: FieldClass[];
    ctx: Ctx;
    onDone: (msg: string) => void;
}) {
    const { lang } = ctx;
    const [open, setOpen] = useState<string | null>(null);
    if (rows.length === 0)
        return null;
    return (<div className="table-wrap field-table" data-testid="field-table">
      <table>
        <thead><tr><th scope="col">{t(lang, "colField")}</th><th scope="col">{t(lang, "fieldClass")}</th><th scope="col">{t(lang, "colRatifiedBy")}</th><th scope="col">{t(lang, "colDate")}</th><th scope="col">{t(lang, "colSkills")}</th><th scope="col"><span className="sr-only">{t(lang, "reclassifyAs")}</span></th></tr></thead>
        <tbody>{rows.map((f) => (<FieldRow key={f.field} f={f} ctx={ctx} open={open === f.field} onOpen={() => setOpen(open === f.field ? null : f.field)} onDone={(m) => { setOpen(null); onDone(m); }}/>))}</tbody>
      </table>
    </div>);
}
function FieldRow({ f, ctx, open, onOpen, onDone }: {
    f: FieldClass;
    ctx: Ctx;
    open: boolean;
    onOpen: () => void;
    onDone: (m: string) => void;
}) {
    const { lang } = ctx;
    return (<>
      <tr data-testid={`field-${f.field}`} data-ratified={f.ratified}>
        <td><strong><Iso>{f.field}</Iso></strong></td>
        <td><Term code={f.class} showCode/>{Array.isArray(f.guidance.tags) && (f.guidance.tags as string[]).length > 0 && <> <span className="tags" data-technical="true" data-testid={`tags-${f.field}`} title={t(lang, "colTags")}>{(f.guidance.tags as string[]).map((g) => <code key={g}>{g}</code>)}</span></>}</td>
        <td>{f.ratifiedBy ? <Name name={f.ratifiedByName ?? f.ratifiedBy} lang={lang} title={f.ratifiedBy}/> : "—"}</td>
        <td>{f.ratifiedAt ? formatDate(f.ratifiedAt, lang) : "—"}</td>
        <td className="muted small" data-testid={`impact-${f.field}`}>{f.impact.skills.length ? <Iso>{f.impact.skills.join(", ")}</Iso> : "—"}</td>
        <td><button className="ghost" onClick={onOpen} data-testid={`reclassify-${f.field}`} aria-expanded={open}>{t(lang, "reclassifyAs")}</button></td>
      </tr>
      {open && <tr className="form-row"><td colSpan={6}><ReclassifyForm f={f} ctx={ctx} onDone={onDone} onCancel={onOpen}/></td></tr>}
    </>);
}
