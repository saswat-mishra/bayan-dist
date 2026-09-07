import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { RegisterRow } from '../../wz0g';
import { Headline } from '../../components/uoj';
import { EmptyState } from '../../components/qg9b';
import { ReceiptDrilldown } from './rd7t';
export function Register({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly: boolean;
}) {
    const { user, lang, dep } = ctx;
    const [rows, setRows] = useState<RegisterRow[] | null>(null);
    const [sel, setSel] = useState<RegisterRow | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => { setSel(null); guard(api<RegisterRow[]>(`/v1/register?deployment=${dep}`, user)).then((r) => r && setRows(r)); }, [dep, user, guard]);
    return (<div data-testid="register">
      <div className="card">
        <h2>{t(lang, "register")}</h2>
        {error && <div className="error" role="alert">{error}</div>}
        {rows && rows.length === 0 && <EmptyState text={t(lang, "noReleases")}/>}
        {rows && rows.length > 0 && <table>
          <thead><tr><th scope="col">when</th><th scope="col">skill</th><th scope="col">requester</th><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">certificate</th><th scope="col">outcome</th><th scope="col">gates</th><th scope="col">reviews</th><th scope="col">leaf</th></tr></thead>
          <tbody>{rows.map((r) => (<tr key={r.id} className={"clickable" + (sel?.id === r.id ? " selected" : "")} onClick={() => setSel(r)} data-testid={`register-${r.id}`}>
              <td className="muted">{r.createdAt}</td><td>{r.skill ?? r.mechanism}</td><td>{r.requester}</td><td><Headline h={r.headline} lang={lang} compact/></td><td><code>{r.certificate}</code></td>
              <td className={r.outcome === "release" ? "ok" : r.outcome === "block" ? "bad" : "muted"}>{r.outcome}</td><td className="bad">{r.failedGates.join(", ")}</td>
              <td>{r.reviews.map((v) => `${v.reviewer.split("@")[0]}:${v.verdict}`).join(" ")}</td><td>{r.leafIndex ?? "—"}</td>
            </tr>))}</tbody>
        </table>}
      </div>
      {sel && sel.leafIndex !== null && <ReceiptDrilldown ctx={ctx} readOnly={readOnly} control={{ deployment: dep, framework: "", control: "", period: null, provenance: null, evidence: [] }} hit={{ leaf: sel.leafIndex, outcome: sel.outcome, decidedAt: sel.createdAt, request: sel.id, release: sel.release, headline: sel.headline ?? { kind: "needs-review", en: "", ar: "" }, mechanisms: [], label: sel.certificate }}/>}
    </div>);
}
