import { useEffect, useState } from "react";
import { api } from '../../../vhq7';
import type { Ctx } from '../../../App';
import { Lang, t } from '../../../gna';
import type { Budget, FeasRow, Pack, ReleaseRequest, RosterEntry, Run, Skill } from '../../../wz0g';
import { PersonCard } from '../../../components/c3u';
import { Progress } from '../../../components/nv8';
import { Iso, Sentence } from '../../../d7t';
interface RecordRow {
    record_id: string;
    ts_hour: string;
    topic: string;
    error_code: string;
}
interface Topic {
    topic: string;
    count: number;
}
interface Props {
    ctx: Ctx;
    run: Run;
    skill: Skill | null;
    question?: FeasRow | null;
    guard: <T>(p: Promise<T>) => Promise<T | null>;
    onRequested: (r: ReleaseRequest) => void;
    onBusy?: (b: boolean) => void;
}
const INCIDENT = /fail|error|regress|wrong|incident|broke|slow|timeout|index|rebuild|outage|retriev|miss|empty|أخفق|خطأ|تراجع|حادث|عطل|فشل|فهرس|بطء|انقطاع/i;
export function mentions(purpose: string, field: string): boolean {
    const text = purpose.toLowerCase().replace(/_/g, " ");
    if (purpose.toLowerCase().includes(field.toLowerCase()) || text.includes(field.toLowerCase().replace(/_/g, " ")))
        return true;
    return field.toLowerCase().split("_").some((tok) => tok.length >= 4 && text.includes(tok));
}
export function PurposeChecklist({ purpose, sensitive, lang }: {
    purpose: string;
    sensitive: string[];
    lang: Lang;
}) {
    const items: [
        string,
        boolean,
        string
    ][] = [
        ["length", purpose.trim().length >= 20, t(lang, "checkLength")],
        ["incident", INCIDENT.test(purpose), t(lang, "checkIncident")],
        ...(sensitive.length ? [["sensitive", sensitive.every((f) => mentions(purpose, f)), `${t(lang, "checkSensitive")} (${sensitive.join(", ")})`] as [
                string,
                boolean,
                string
            ]] : []),
    ];
    return (<ul className="checklist purpose-check" id="purpose-checklist" data-testid="purpose-checklist" aria-label={t(lang, "purposeChecklist")}>
      {items.map(([k, ok, label]) => <li key={k} data-check={k} data-ok={ok}><span className="tick" aria-hidden="true">{ok ? "✓" : "○"}</span> <span>{label}</span></li>)}
    </ul>);
}
export function BudgetSentence({ b, lang, period }: {
    b: Budget;
    lang: Lang;
    period?: string;
}) {
    const word = period === "month" ? t(lang, "month") : t(lang, "quarter");
    return <div data-testid="budget">{t(lang, "budgetSentence").replace("{period}", word).replace("{n}", String(b.consumed)).replace("{limit}", String(b.limit))}{/\d/.test(b.period) && <span className="muted"> (<Iso>{b.period}</Iso>)</span>}</div>;
}
export function RequestStep({ ctx, run, skill, question, guard, onRequested, onBusy }: Props) {
    const { user, lang, dep } = ctx;
    const [purpose, setPurpose] = useState("");
    const [sensitive, setSensitive] = useState<string[]>([]);
    const [me, setMe] = useState<RosterEntry | null>(null);
    const [budget, setBudget] = useState<Budget | null>(null);
    const [packPeriod, setPackPeriod] = useState<string | undefined>(ctx.pack?.budget?.period);
    const [records, setRecords] = useState<RecordRow[]>([]);
    const [topics, setTopics] = useState<Topic[] | null>(null);
    const [topic, setTopic] = useState<string>(typeof run.params?.topic === "string" ? run.params.topic : "");
    const [quota, setQuota] = useState<{
        consumed: number;
        limit: number;
    } | null>(null);
    const [busy, setBusy] = useState(false);
    useEffect(() => {
        api<RosterEntry>(`/v1/roster/me?deployment=${dep}`, user).then(setMe).catch(() => setMe(null));
        api<Topic[]>(`/v1/records/topics?deployment=${dep}`, user).then(setTopics).catch(() => setTopics([]));
        const cohort = `${dep}:${skill?.name ?? run.skill}`;
        api<Budget[]>(`/v1/budget?deployment=${dep}`, user).then(async (bs) => {
            const row = bs.find((b) => b.cohort === cohort);
            if (row) {
                setBudget(row);
                return;
            }
            const packId = ctx.deps.find((d) => d.id === dep)?.pack;
            const pack = packId ? await api<Pack>(`/v1/packs/${packId}`, user) : null;
            const limit = pack?.budget?.perCohortLimit ?? 0;
            setPackPeriod(pack?.budget?.period);
            setBudget({ cohort, period: pack?.budget?.period ?? "", consumed: 0, reserved: 0, limit, remaining: limit, disjoint: false });
        }).catch(() => setBudget(null));
    }, [dep, user, skill, run.skill, ctx.deps]);
    const sensitiveFields = run.manifest.fields.filter((f) => f.class === "SENSITIVE" && f.transform !== "drop").map((f) => f.name);
    const ok = purpose.trim().length >= 20;
    const setWorking = (b: boolean) => { setBusy(b); onBusy?.(b); };
    async function submit() {
        setWorking(true);
        const r = await guard(api<ReleaseRequest>("/v1/requests", user, { method: "POST", body: { deployment: dep, run: run.id, purpose, mechanism: "output-check", sensitive_declared: sensitive } }));
        setWorking(false);
        if (r)
            onRequested(r);
    }
    async function exemplar(recordId: string) {
        setWorking(true);
        const r = await guard(api<ReleaseRequest>("/v1/requests", user, { method: "POST", body: { deployment: dep, mechanism: "exemplar", record_id: recordId, purpose } }));
        setWorking(false);
        if (r) {
            setQuota(r.exemplarQuota ?? null);
            onRequested(r);
        }
    }
    const recordsUrl = `/v1/records?deployment=${dep}${topic ? `&topic=${encodeURIComponent(topic)}` : ""}&limit=5`;
    return (<div className="card" data-testid="step-request">
      <h2>{t(lang, "request")}{question && <span className="muted"> — {lang === "ar" ? question.text_ar : question.text}</span>}</h2>
      <label>{t(lang, "purpose")}<textarea rows={3} value={purpose} onChange={(e) => setPurpose(e.target.value)} data-testid="purpose" aria-describedby="purpose-checklist" placeholder={t(lang, "purposePlaceholder")}/></label>
      <PurposeChecklist purpose={purpose} sensitive={sensitive} lang={lang}/>
      {me ? <div className="card" data-testid="roster-card"><PersonCard testid="recipient-card" title={t(lang, "recipientYou")} lang={lang} p={{ name: me.displayName ?? user, principal: user, employer: me.employer, location: me.location, validUntil: me.validUntil, rostered: me.valid }}/></div>
            : <div className="warn">{t(lang, "notRostered")}</div>}
      {sensitiveFields.length > 0 && <div><strong>{t(lang, "declared")}:</strong> {sensitiveFields.map((f) => (<label key={f} className="pill inline"><input type="checkbox" checked={sensitive.includes(f)} onChange={(e) => setSensitive(e.target.checked ? [...sensitive, f] : sensitive.filter((x) => x !== f))}/> <Iso>{f}</Iso></label>))}</div>}
      {budget && <BudgetSentence b={budget} lang={lang} period={packPeriod}/>}
      <div className="vote">
        <button className="primary" disabled={!ok || run.status !== "complete" || busy} onClick={submit} data-testid="request">{t(lang, "submitRequest")}</button>
        {busy && <Progress label={t(lang, "progressRequesting")}/>}
      </div>
      <details data-testid="exemplar-path">
        <summary data-testid="exemplar-summary"><Sentence tpl={t(lang, "exemplarAltWords")} vars={{ quota: String(ctx.pack?.budget?.exemplarQuota ?? "—") }} plain/>{quota && <span className="muted"> · {t(lang, "exemplarQuota")} {quota.consumed}/{quota.limit}</span>}</summary>
        {topics && topics.length === 0 && <div className="muted" data-testid="no-topics">{t(lang, "noTopics")}</div>}
        {topics && topics.length > 0 && (<div className="vote">
            <label>{t(lang, "topicLabel")}{" "}
              <select value={topic} onChange={(e) => setTopic(e.target.value)} data-testid="topic" aria-label="topic">
                <option value="">{t(lang, "allTopics")}</option>
                {topics.map((x) => <option key={x.topic} value={x.topic}>{x.topic} ({x.count})</option>)}
              </select></label>
            <button onClick={() => guard(api<RecordRow[]>(recordsUrl, user)).then((rs) => rs && setRecords(rs))} data-testid="load-records">{t(lang, "records")}</button>
          </div>)}
        <ul>{records.map((r) => <li key={r.record_id}><code><Iso>{r.record_id}</Iso></code> <Iso>{r.ts_hour}</Iso> <Iso>{r.topic}</Iso> <Iso>{r.error_code}</Iso> <button disabled={!ok || busy} onClick={() => exemplar(r.record_id)}>{t(lang, "exemplar")}</button></li>)}</ul>
      </details>
    </div>);
}
