import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { ago, useGuard } from '../../q1n';
import { pick, t } from '../../gna';
import type { ReleaseRequest, RegisterRow, RequestListItem, Run, Summary } from '../../wz0g';
import { Headline } from '../../components/uoj';
import { EmptyState } from '../../components/qg9b';
import { CertificateDetails } from '../../components/xsd';
const POV_PURPOSE = "Weekly usage and quality summary as acceptance evidence for the deployment milestone.";
const STUCK_AFTER = 24 * 3600;
export function LeadHome({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [s, setS] = useState<Summary | null>(null);
    const [reg, setReg] = useState<RegisterRow[]>([]);
    const [pending, setPending] = useState<RequestListItem[]>([]);
    const [req, setReq] = useState<ReleaseRequest | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => {
        guard(api<Summary>(`/v1/summary?deployment=${dep}`, user)).then((x) => x && setS(x));
        guard(api<RegisterRow[]>(`/v1/register?deployment=${dep}`, user)).then((x) => x && setReg(x.filter((r) => r.outcome === "release").reverse()));
        guard(api<RequestListItem[]>(`/v1/requests?deployment=${dep}&status=pending`, user)).then((x) => x && setPending(x));
    }, [dep, user, guard]);
    useEffect(() => { load(); }, [load]);
    async function weekly() {
        const run = await guard(api<Run>("/v1/runs", user, { method: "POST", body: { deployment: dep, skill: "weekly-usage-summary", version: "1.0.0", params: {} } }));
        if (!run)
            return;
        const r = await guard(api<ReleaseRequest>("/v1/requests", user, { method: "POST", body: { deployment: dep, run: run.id, purpose: POV_PURPOSE } }));
        if (r) {
            setReq(r);
            load();
        }
    }
    const stuck = pending.filter((p) => p.ageSeconds >= STUCK_AFTER);
    return (<div data-testid="lead-home">
      {error && <div className="error" role="alert">{error}</div>}
      <div className="grid">
        <div className="card" data-testid="stuck">
          <h2>{t(lang, "stuck")} <span className="muted">— {t(lang, "stuckHint")}</span></h2>
          {pending.length === 0 && <EmptyState text={t(lang, "noStuck")}/>}
          {pending.length > 0 && <table><thead><tr><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">{t(lang, "colWaiting")}</th><th scope="col">{t(lang, "colAge")}</th></tr></thead>
            <tbody>{pending.map((p) => <tr key={p.id} className={stuck.includes(p) ? "bad" : ""} data-testid={`pending-${p.id}`}><td><Headline h={p.headline} lang={lang} compact/><div className="muted">{p.requester}</div></td><td>{pick(lang, p.waitingOn)}</td><td>{ago(p.ageSeconds, lang)}{stuck.includes(p) && " · stuck"}</td></tr>)}</tbody></table>}
        </div>
        <div className="card" data-testid="pov">
          <h2>{t(lang, "runPov")}</h2>
          <div className="muted">{t(lang, "povPurpose")}: “{POV_PURPOSE}”</div>
          <button className="primary" onClick={weekly} data-testid="run-pov">{t(lang, "runPov")}</button>
          {s && <div><strong>{t(lang, "agreementRate")}:</strong> {s.agreementRate} · reviewer overrides: {s.overrideRate}</div>}
          {s && s.budget.length > 0 && <div data-testid="budget-bars"><h3>{t(lang, "budgetBars")}</h3>{s.budget.map((b) => (<div key={b.cohort}><div className="muted">{b.cohort} · {b.consumed}+{b.reserved} of {b.limit} ({b.period})</div><div className="bar" role="img" aria-label={`${b.consumed} of ${b.limit}`}><span style={{ width: `${Math.min(100, Math.round(100 * (b.consumed + b.reserved) / Math.max(b.limit, 1)))}%` }}/></div></div>))}</div>}
        </div>
      </div>
      {req && <CertificateDetails cert={req.certificate} lang={lang}/>}
      <div className="card" data-testid="acceptance-timeline">
        <h2>{t(lang, "acceptanceTimeline")}</h2>
        {reg.length === 0 && <EmptyState text={t(lang, "noReleases")}/>}
        <div className="cards">{reg.map((r) => (<div key={r.id} className="block" data-testid={`release-${r.id}`}>
            <Headline h={r.headline} lang={lang} compact/>
            <div>{r.skill ?? r.mechanism} · {r.createdAt.slice(0, 10)} · <code>{r.certificate}</code></div>
            <div className="muted">{t(lang, "bundlePath")}: <code>{r.outbox}</code> · {t(lang, "leaf")} {r.leafIndex}</div>
          </div>))}</div>
      </div>
    </div>);
}
