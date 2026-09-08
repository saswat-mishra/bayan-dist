import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { RegisterRow } from '../../wz0g';
import { StateChip } from '../../components/drm';
import { Iso, Name } from '../../d7t';
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
              <td className="muted"><Iso>{r.createdAt}</Iso></td><td><Iso>{r.skill ?? r.mechanism}</Iso></td><td><Name name={r.requester} lang={lang}/></td><td>{r.headline && <StateChip kind={r.headline.kind} lang={lang}/>}</td><td data-technical="true"><code><Iso>{r.certificate}</Iso></code></td>
              <td className={r.outcome === "release" ? "ok" : r.outcome === "block" ? "bad" : "muted"}><Iso>{r.outcome}</Iso></td><td className="bad"><Iso>{r.failedGates.join(", ")}</Iso></td>
              <td><Iso>{r.reviews.map((v) => `${v.reviewer.split("@")[0]}:${v.verdict}`).join(" ")}</Iso></td><td>{r.leafIndex ?? "—"}</td>
            </tr>))}</tbody>
        </table>}
      </div>
      {sel && sel.leafIndex !== null && <ReceiptDrilldown ctx={ctx} readOnly={readOnly} control={{ deployment: dep, framework: "", control: "", period: null, provenance: null, evidence: [] }} hit={{ leaf: sel.leafIndex, outcome: sel.outcome, decidedAt: sel.createdAt, request: sel.id, release: sel.release, headline: sel.headline ?? { kind: "needs-review", en: "", ar: "" }, mechanisms: [], label: sel.certificate }}/>}
    </div>);
}
