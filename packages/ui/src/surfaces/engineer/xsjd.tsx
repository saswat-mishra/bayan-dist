import { useCallback, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { ago, go, useGuard, useLive } from '../../q1n';
import { Key, Lang, pick, t } from '../../gna';
import type { RequestListItem } from '../../wz0g';
import { Headline } from '../../components/uoj';
import { EmptyState } from '../../components/qg9b';
import { LiveStatus } from '../../components/poy';
export function nextAction(r: RequestListItem, lang: Lang): string {
    const k: Key = r.status === "pending" ? "nextWait" : r.status === "released" ? "nextHandoff" : r.outcome === "refuse" || r.status === "refused" ? "nextFix" : "nextNothing";
    return t(lang, k);
}
export function waitsFor(r: RequestListItem, lang: Lang): string {
    if (r.status !== "pending")
        return "—";
    if (r.outstandingReviewers && r.outstandingReviewers.length)
        return r.outstandingReviewers.map((o) => o.displayName).join(", ");
    return pick(lang, r.waitingOn) || "—";
}
export function MyRequests({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang } = ctx;
    const [rows, setRows] = useState<RequestListItem[] | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<RequestListItem[]>("/v1/requests?mine=1", user)).then((r) => r && setRows(r)), [user, guard]);
    const { updatedAt, refresh } = useLive(load, 15000);
    return (<div className="card tables" data-testid="my-requests">
      <h2>{t(lang, "myRequests")} <LiveStatus updatedAt={updatedAt} lang={lang} onRefresh={refresh}/></h2>
      {error && <div className="error" role="alert">{error}</div>}
      {rows && rows.length === 0 && <EmptyState text={t(lang, "noRequests")}/>}
      {rows && rows.length > 0 && (<div className="table-wrap"><table>
          <thead><tr><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">{t(lang, "colPurpose")}</th><th scope="col">{t(lang, "colStatus")}</th><th scope="col">{t(lang, "colWaitsFor")}</th><th scope="col">{t(lang, "colAge")}</th><th scope="col">{t(lang, "colNext")}</th></tr></thead>
          <tbody>{rows.map((r) => (<tr key={r.id} className="clickable" onClick={() => go(`requests/${r.id}`)} data-testid={`req-${r.id}`}>
              <td><Headline h={r.headline} lang={lang} compact/>{r.lookup && <div className="muted">{t(lang, "lookupTitle")}</div>}</td>
              <td className="purpose-cell">{r.purpose}</td>
              <td><span className="pill">{r.status}</span></td>
              <td data-testid={`waits-${r.id}`}>{waitsFor(r, lang)}</td>
              <td>{ago(r.ageSeconds, lang)}</td>
              <td><a href={`#/requests/${r.id}`} onClick={(e) => e.stopPropagation()} data-testid={`next-${r.id}`}>{nextAction(r, lang)}</a></td>
            </tr>))}</tbody>
        </table></div>)}
    </div>);
}
