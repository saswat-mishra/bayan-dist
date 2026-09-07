import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { go, useGuard } from '../../q1n';
import { t } from '../../gna';
import type { QueueItem } from '../../wz0g';
import { browserSigner } from '../../ck2';
import { EmptyState } from '../../components/qg9b';
import { Brief } from './u3r';
const RISK_ORDER = ["red", "black", "amber", "green"];
export function Queue({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, me, sub } = ctx;
    const [queue, setQueue] = useState<QueueItem[] | null>(null);
    const [filter, setFilter] = useState("all");
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<QueueItem[]>("/v1/review/queue", user)).then((q) => q && setQueue(q)), [user, guard]);
    useEffect(() => { load(); }, [load]);
    const selected = sub[0] ?? null;
    const items = (queue ?? []).filter((q) => filter === "all" || q.deployment === filter);
    const groups = RISK_ORDER.map((r) => [r, items.filter((q) => q.riskClass === r)] as const).filter(([, xs]) => xs.length);
    const deployments = Array.from(new Set((queue ?? []).map((q) => q.deployment)));
    return (<div className="grid" data-testid="queue">
      <div className="card">
        <h2>{t(lang, "queue")}</h2>
        {error && <div className="error" role="alert">{error}</div>}
        <label>{t(lang, "filterDeployment")}{" "}
          <select value={filter} onChange={(e) => setFilter(e.target.value)} aria-label="deployment-filter"><option value="all">{t(lang, "all")}</option>{deployments.map((d) => <option key={d} value={d}>{d}</option>)}</select></label>
        {groups.map(([risk, xs]) => (<div key={risk}>
            <h3><span className={`pill ${risk}`}>{risk}</span> <span className="muted">{xs.length}</span></h3>
            <table><tbody>
              {xs.map((q) => (<tr key={q.id} className={"clickable" + (selected === q.id ? " selected" : "")} onClick={() => go(`queue/${q.id}`)} data-testid={`queue-${q.id}`}>
                  <td>{q.skill ?? q.mechanism} <code className="muted">{q.id.slice(-6)}</code></td><td className="muted">{q.deployment}</td><td>{q.votes}/{q.requiredReviews}</td>
                  <td>{q.yours ? <span className="bad">{t(lang, "yoursCannot")}</span> : q.youVoted ? t(lang, "youVoted") : ""}</td>
                </tr>))}
            </tbody></table>
          </div>))}
        {queue && queue.length === 0 && <EmptyState text={t(lang, "queueEmpty")} testid="queue-empty"/>}
      </div>
      <div>{selected && <Brief id={selected} user={user} lang={lang} onChange={load} signer={browserSigner(user, me.custody === "client" ? me.keyName ?? null : null)}/>}</div>
    </div>);
}
