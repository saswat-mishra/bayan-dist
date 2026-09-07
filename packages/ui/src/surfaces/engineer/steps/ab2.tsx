import { useEffect, useState } from "react";
import { api } from '../../../vhq7';
import type { Ctx } from '../../../App';
import { Lang, t } from '../../../gna';
import type { Budget, Pack, ReleaseRequest, RosterEntry, Run, Skill } from '../../../wz0g';
import { RosterCard } from '../../../components/xzur';
interface RecordRow {
    record_id: string;
    ts_hour: string;
    topic: string;
    error_code: string;
}
interface Props {
    ctx: Ctx;
    run: Run;
    skill: Skill | null;
    guard: <T>(p: Promise<T>) => Promise<T | null>;
    onRequested: (r: ReleaseRequest) => void;
}
function BudgetLine({ b, lang }: {
    b: Budget;
    lang: Lang;
}) {
    return <div data-testid="budget"><strong>{t(lang, "budgetPosition")}:</strong> {b.consumed} {t(lang, "ofThisPeriod")} {b.limit} {t(lang, "thisPeriod")} ({b.period}) · {b.remaining} left</div>;
}
export function RequestStep({ ctx, run, skill, guard, onRequested }: Props) {
    const { user, lang, dep } = ctx;
    const [purpose, setPurpose] = useState("");
    const [sensitive, setSensitive] = useState<string[]>([]);
    const [me, setMe] = useState<RosterEntry | null>(null);
    const [budget, setBudget] = useState<Budget | null>(null);
    const [records, setRecords] = useState<RecordRow[]>([]);
    const [quota, setQuota] = useState<{
        consumed: number;
        limit: number;
    } | null>(null);
    useEffect(() => {
        api<RosterEntry>(`/v1/roster/me?deployment=${dep}`, user).then(setMe).catch(() => setMe(null));
        const cohort = `${dep}:${skill?.name ?? run.skill}`;
        api<Budget[]>(`/v1/budget?deployment=${dep}`, user).then(async (bs) => {
            const row = bs.find((b) => b.cohort === cohort);
            if (row) {
                setBudget(row);
                return;
            }
            const packId = ctx.deps.find((d) => d.id === dep)?.pack;
            const pack = packId ? await api<Pack & {
                budget?: {
                    perCohortLimit?: number;
                    period?: string;
                };
            }>(`/v1/packs/${packId}`, user) : null;
            const limit = pack?.budget?.perCohortLimit ?? 0;
            setBudget({ cohort, period: pack?.budget?.period ?? "", consumed: 0, reserved: 0, limit, remaining: limit, disjoint: false });
        }).catch(() => setBudget(null));
    }, [dep, user, skill, run.skill, ctx.deps]);
    const sensitiveFields = run.manifest.fields.filter((f) => f.class === "SENSITIVE" && f.transform !== "drop").map((f) => f.name);
    const ok = purpose.trim().length >= 20;
    async function submit() {
        const r = await guard(api<ReleaseRequest>("/v1/requests", user, { method: "POST", body: { deployment: dep, run: run.id, purpose, mechanism: "output-check", sensitive_declared: sensitive } }));
        if (r)
            onRequested(r);
    }
    async function exemplar(recordId: string) {
        const r = await guard(api<ReleaseRequest>("/v1/requests", user, { method: "POST", body: { deployment: dep, mechanism: "exemplar", record_id: recordId, purpose } }));
        if (r) {
            setQuota(r.exemplarQuota ?? null);
            onRequested(r);
        }
    }
    return (<div className="card" data-testid="step-request">
      <h2>{t(lang, "request")}</h2>
      <label>{t(lang, "purpose")}<textarea rows={3} value={purpose} onChange={(e) => setPurpose(e.target.value)} data-testid="purpose" aria-describedby="purpose-counter"/></label>
      <div id="purpose-counter" className={"counter " + (ok ? "ok" : "warn")} data-testid="purpose-counter">{purpose.trim().length} {t(lang, "purposeCounter")}</div>
      {me ? <RosterCard e={me} lang={lang} title={t(lang, "recipientYou")}/> : <div className="warn">{t(lang, "notRostered")}</div>}
      {sensitiveFields.length > 0 && <div><strong>{t(lang, "declared")}:</strong> {sensitiveFields.map((f) => (<label key={f} className="pill"><input type="checkbox" checked={sensitive.includes(f)} onChange={(e) => setSensitive(e.target.checked ? [...sensitive, f] : sensitive.filter((x) => x !== f))}/> {f}</label>))}</div>}
      {budget && <BudgetLine b={budget} lang={lang}/>}
      <div className="vote">
        <button className="primary" disabled={!ok || run.status !== "complete"} onClick={submit} data-testid="request">{t(lang, "submitRequest")}</button>
      </div>
      <details data-testid="exemplar-path">
        <summary>{t(lang, "exemplarAlt")}{quota && ` · ${t(lang, "exemplarQuota")} ${quota.consumed}/${quota.limit}`}</summary>
        <button onClick={() => guard(api<RecordRow[]>(`/v1/records?deployment=${dep}&topic=pension&limit=5`, user)).then((rs) => rs && setRecords(rs))}>{t(lang, "records")}</button>
        <ul>{records.map((r) => <li key={r.record_id}><code>{r.record_id}</code> {r.ts_hour} {r.topic} {r.error_code} <button disabled={!ok} onClick={() => exemplar(r.record_id)}>{t(lang, "exemplar")}</button></li>)}</ul>
      </details>
    </div>);
}
