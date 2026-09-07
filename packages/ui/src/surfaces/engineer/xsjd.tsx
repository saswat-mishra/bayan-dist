import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { ago, go, useGuard } from '../../q1n';
import { pick, t } from '../../gna';
import type { RequestListItem } from '../../wz0g';
import { Headline } from '../../components/uoj';
import { EmptyState } from '../../components/qg9b';
export function MyRequests({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang } = ctx;
    const [rows, setRows] = useState<RequestListItem[] | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => { guard(api<RequestListItem[]>("/v1/requests?mine=1", user)).then((r) => r && setRows(r)); }, [user, guard]);
    return (<div className="card" data-testid="my-requests">
      <h2>{t(lang, "myRequests")}</h2>
      {error && <div className="error" role="alert">{error}</div>}
      {rows && rows.length === 0 && <EmptyState text={t(lang, "noRequests")}/>}
      {rows && rows.length > 0 && (<table>
          <thead><tr><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">{t(lang, "colStatus")}</th><th scope="col">{t(lang, "colWaiting")}</th><th scope="col">{t(lang, "colAge")}</th><th scope="col"><span className="sr-only">{t(lang, "openTrack")}</span></th></tr></thead>
          <tbody>{rows.map((r) => (<tr key={r.id} className="clickable" onClick={() => go(`requests/${r.id}`)} data-testid={`req-${r.id}`}>
              <td><Headline h={r.headline} lang={lang} compact/><div className="muted">{r.skill ?? r.mechanism} · {r.deployment}</div></td>
              <td><span className="pill">{r.status}</span></td>
              <td>{pick(lang, r.waitingOn) || "—"}</td>
              <td>{ago(r.ageSeconds, lang)}</td>
              <td><a href={`#/requests/${r.id}`} onClick={(e) => e.stopPropagation()}>{t(lang, "openTrack")}</a></td>
            </tr>))}</tbody>
        </table>)}
    </div>);
}
