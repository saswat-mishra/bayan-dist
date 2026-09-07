import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { FieldClass } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
export function DbaPages({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [rows, setRows] = useState<FieldClass[] | null>(null);
    const [done, setDone] = useState<string | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<FieldClass[]>(`/v1/field-classes?deployment=${dep}`, user)).then((r) => r && setRows(r)), [dep, user, guard]);
    useEffect(() => { setDone(null); load(); }, [load]);
    async function ratify(field: string) {
        const r = await guard(api<FieldClass & {
            recertified: {
                skill: string;
                before: number;
                after: number;
            }[];
        }>(`/v1/field-classes/${encodeURIComponent(field)}/ratify`, user, { method: "POST", body: { deployment: dep } }));
        if (r) {
            setDone(`${t(lang, "ratifiedNow")}: ${r.recertified.filter((c) => c.before !== c.after).map((c) => `${c.skill} D${c.before}→D${c.after}`).join(", ") || "—"}`);
            load();
        }
    }
    return (<div className="card" data-testid="field-classes">
      <h2>{t(lang, "fieldClasses")} — {dep}</h2>
      {error && <div className="error" role="alert">{error}</div>}
      {done && <div className="ok" role="status" data-testid="ratified">{done}</div>}
      {rows && rows.length === 0 && <EmptyState text={t(lang, "noFields")}/>}
      {rows && rows.length > 0 && <table>
        <thead><tr><th scope="col">{t(lang, "fieldName")}</th><th scope="col">{t(lang, "proposedClass")}</th><th scope="col">{t(lang, "ratifiedBy")}</th><th scope="col">{t(lang, "impact")}</th><th scope="col">{t(lang, "guidance")}</th><th scope="col"><span className="sr-only">{t(lang, "ratify")}</span></th></tr></thead>
        <tbody>{rows.map((f) => (<tr key={f.field} data-testid={`field-${f.field}`} className={f.ratified ? "" : "warn"}>
            <td><code>{f.field}</code></td><td>{f.class}</td>
            <td>{f.ratified ? <>{f.ratifiedBy} <span className="muted">{f.ratifiedAt?.slice(0, 10)}</span></> : <span className="warn">— ({f.proposedBy})</span>}</td>
            <td>{f.impact.text}{f.impact.cappedAtD1.length > 0 && <div className="muted">{f.impact.cappedAtD1.join(", ")}</div>}</td>
            <td className="muted">{Object.entries(f.guidance).map(([k, v]) => `${k}: ${String(v)}`).join(" · ") || "—"}</td>
            <td>{!f.ratified && <button className="primary" onClick={() => ratify(f.field)} data-testid={`ratify-${f.field}`}>{t(lang, "ratify")}</button>}</td>
          </tr>))}</tbody>
      </table>}
    </div>);
}
