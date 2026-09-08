import { useCallback, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { ago, go, useGuard, useLive } from '../../q1n';
import { Key, Lang, pick, t } from '../../gna';
import type { RequestListItem } from '../../wz0g';
import { StateChip } from '../../components/drm';
import { Iso, Name } from '../../d7t';
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
export function waitsLabel(kind: RequestListItem["outstandingKind"] | undefined, lang: Lang): string {
    return t(lang, kind === "waiting" ? "waitingFor" : "couldBeWaitingFor");
}
function WaitsCell({ r, lang }: {
    r: RequestListItem;
    lang: Lang;
}) {
    if (r.status !== "pending")
        return <>—</>;
    const names = r.outstandingReviewers ?? [];
    return (<>
      {names.length ? names.map((o, i) => <span key={o.principal}>{i > 0 && ", "}<Name name={o.displayName} lang={lang}/></span>) : <Iso>{pick(lang, r.waitingOn) || "—"}</Iso>}
      {r.requiredReviews > 0 && <div className="muted small" data-testid={`votes-${r.id}`}>{t(lang, "votesCount").replace("{votes}", String(r.votes)).replace("{required}", String(r.requiredReviews))}</div>}
    </>);
}
export function MyRequests({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang } = ctx;
    const [rows, setRows] = useState<RequestListItem[] | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<RequestListItem[]>("/v1/requests?mine=1", user)).then((r) => r && setRows(r)), [user, guard]);
    const { updatedAt, refresh } = useLive(load, 15000);
    const kind = rows?.find((r) => r.outstandingKind)?.outstandingKind;
    return (<div className="card tables" data-testid="my-requests">
      <h2>{t(lang, "myRequests")}</h2>
      <LiveStatus updatedAt={updatedAt} lang={lang} onRefresh={refresh}/>
      {error && <div className="error" role="alert">{error}</div>}
      {rows && rows.length === 0 && <EmptyState text={t(lang, "noRequests")}/>}
      {rows && rows.length > 0 && (<div className="table-wrap"><table>
          <thead><tr><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">{t(lang, "colPurpose")}</th><th scope="col">{t(lang, "colStatus")}</th><th scope="col" data-testid="waits-header" data-kind={kind ?? "eligible"}>{waitsLabel(kind, lang)}</th><th scope="col">{t(lang, "colAge")}</th><th scope="col">{t(lang, "colNext")}</th></tr></thead>
          <tbody>{rows.map((r) => (<tr key={r.id} className="clickable" onClick={() => go(`requests/${r.id}`)} data-testid={`req-${r.id}`}>
              <td>{r.headline && <StateChip kind={r.headline.kind} lang={lang} testid={`chip-${r.id}`}/>}{r.lookup && <div className="muted">{t(lang, "lookupTitle")}</div>}</td>
              <td className="purpose-cell"><Iso>{r.purpose}</Iso></td>
              <td><StateChip kind={r.status === "released" ? "released" : r.status === "refused" ? "refused" : "pending"} lang={lang} label={r.status === "released" || r.status === "refused" || r.status === "pending" ? undefined : r.status} testid={`status-${r.id}`}/></td>
              <td data-testid={`waits-${r.id}`}><WaitsCell r={r} lang={lang}/></td>
              <td>{ago(r.ageSeconds, lang)}</td>
              <td><a href={`#/requests/${r.id}`} onClick={(e) => e.stopPropagation()} data-testid={`next-${r.id}`}>{nextAction(r, lang)}</a></td>
            </tr>))}</tbody>
        </table></div>)}
    </div>);
}
