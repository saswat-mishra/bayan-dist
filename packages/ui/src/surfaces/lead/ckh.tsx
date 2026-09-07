import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { ago, useGuard, useLive, useTicker } from '../../q1n';
import { Lang, pick, t } from '../../gna';
import type { ReleaseRequest, RegisterRow, RequestListItem, Run, Skill, SkillRequest, Summary } from '../../wz0g';
import { Headline } from '../../components/uoj';
import { EmptyState } from '../../components/qg9b';
import { LiveStatus } from '../../components/poy';
import { CertificateDetails } from '../../components/xsd';
import { Progress } from '../../components/nv8';
import { RowsPreview } from '../../components/hnm';
import { Technical } from '../../components/n4x';
import { Bi, formatDate } from '../../d7t';
export const POV_PURPOSE = "Weekly usage and quality summary as acceptance evidence for the deployment milestone.";
const POV_SKILL = "weekly-usage-summary";
export function isoWeek(iso: string): number {
    const d = new Date(iso);
    const t0 = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()));
    const day = t0.getUTCDay() || 7;
    t0.setUTCDate(t0.getUTCDate() + 4 - day);
    const y0 = new Date(Date.UTC(t0.getUTCFullYear(), 0, 1));
    return Math.ceil(((t0.getTime() - y0.getTime()) / 86400000 + 1) / 7);
}
export function weekLines(rows: RegisterRow[], lang: Lang): string[] {
    const by = new Map<number, {
        n: number;
        p: number;
        r: number;
    }>();
    for (const r of rows) {
        const w = isoWeek(r.createdAt);
        const e = by.get(w) ?? { n: 0, p: 0, r: 0 };
        if (r.outcome === "release") {
            e.n += 1;
            if (r.reviews.length === 0)
                e.p += 1;
        }
        else if (r.outcome === "block" || r.outcome === "refuse")
            e.r += 1;
        by.set(w, e);
    }
    return Array.from(by.entries()).sort((a, b) => b[0] - a[0]).map(([w, e]) => t(lang, "weekLine").replace("{w}", String(w)).replace("{n}", String(e.n)).replace("{p}", String(e.p)).replace("{r}", String(e.r)));
}
function Tiles({ s, pending, lang }: {
    s: Summary | null;
    pending: RequestListItem[];
    lang: Lang;
}) {
    const oldest = pending.reduce((m, p) => Math.max(m, p.ageSeconds), 0);
    return (<div className="tiles" data-testid="tiles">
      <div className="tile" data-testid="tile-releases"><div className="num">{s?.released ?? "—"}</div><div className="sub">{t(lang, "releasesThisPeriod")}</div></div>
      <div className="tile" data-testid="tile-pending"><div className="num">{s?.pending ?? pending.length}</div><div className="sub">{t(lang, "pendingTile")}{pending.length > 0 && ` · ${t(lang, "oldest")} ${ago(oldest, lang)}`}</div></div>
      <div className="tile" data-testid="tile-refusals"><div className="num">{s?.refused ?? "—"}</div><div className="sub">{t(lang, "refusalsTile")}</div></div>
      <div className="tile" data-testid="tile-agreement"><div className="num small-num" data-gate-text="true">{s ? (s.agreementText ? <Bi x={s.agreementText} lang={lang}/> : s.agreementRate) : "—"}</div><div className="sub">{t(lang, "agreementTile")}</div></div>
    </div>);
}
export function ChaseList({ ctx, pending, onChanged, updatedAt, refresh }: {
    ctx: Ctx;
    pending: RequestListItem[];
    onChanged: () => void;
    updatedAt: number | null;
    refresh: () => void;
}) {
    const { user, lang, pack } = ctx;
    const now = useTicker(5000);
    const [error, guard] = useGuard(lang);
    const stuckAfter = pack?.review?.stuckAfterSeconds ?? 86400;
    const isStuck = (p: RequestListItem) => p.stuck ?? p.ageSeconds >= (p.stuckAfterSeconds ?? stuckAfter);
    async function remind(id: string) { if (await guard(api(`/v1/requests/${id}/remind`, user, { method: "POST" })))
        onChanged(); }
    return (<div className="card tables" data-testid="stuck">
      <h2>{t(lang, "chaseList")} <span className="muted">— {t(lang, "stuckHint")}</span> <LiveStatus updatedAt={updatedAt} lang={lang} onRefresh={refresh}/></h2>
      {error && <div className="error" role="alert">{error}</div>}
      {pending.length === 0 && <EmptyState text={t(lang, "noStuck")}/>}
      {pending.length > 0 && <div className="table-wrap"><table>
        <thead><tr><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">{t(lang, "colPurpose")}</th><th scope="col">{t(lang, "colOutstanding")}</th><th scope="col">{t(lang, "colAge")}</th><th scope="col"><span className="sr-only">{t(lang, "remind")}</span></th></tr></thead>
        <tbody>{pending.map((p) => {
                const names = (p.outstandingReviewers ?? []).map((o) => o.displayName);
                const last = p.lastReminderAt ? Math.max(0, Math.round((now - new Date(p.lastReminderAt).getTime()) / 1000)) : null;
                return (<tr key={p.id} className={isStuck(p) ? "bad" : ""} data-testid={`pending-${p.id}`} data-stuck={isStuck(p)}>
              <td><Headline h={p.headline} lang={lang} compact/><div className="muted">{t(lang, "requestedBy")} {p.requesterName ?? p.requester}</div></td>
              <td className="purpose-cell">{p.purpose}</td>
              <td data-testid={`outstanding-${p.id}`}>{names.length ? <strong>{names.join(", ")}</strong> : null}<div className="muted small">{pick(lang, p.waitingOn)}</div></td>
              <td>{ago(p.ageSeconds, lang)}{isStuck(p) && <> · <span className="bad">{t(lang, "stuckWord")}</span></>}</td>
              <td><button onClick={() => remind(p.id)} data-testid={`remind-${p.id}`}>{t(lang, "remind")}</button>
                {last !== null && <div className="muted small" data-testid={`reminder-${p.id}`}>{t(lang, "reminderRecorded").replace("{ago}", ago(last, lang))}</div>}</td>
            </tr>);
            })}</tbody>
      </table></div>}
    </div>);
}
export function PovPreview({ ctx, onRequested }: {
    ctx: Ctx;
    onRequested: () => void;
}) {
    const { user, lang, dep, pack } = ctx;
    const [skills, setSkills] = useState<Skill[]>([]);
    const [skill, setSkill] = useState(POV_SKILL);
    const [run, setRun] = useState<Run | null>(null);
    const [purpose, setPurpose] = useState(POV_PURPOSE);
    const [req, setReq] = useState<ReleaseRequest | null>(null);
    const [busy, setBusy] = useState(false);
    const [error, guard] = useGuard(lang);
    const floor = pack?.review?.roleFloors?.lead ?? 0;
    useEffect(() => { api<Skill[]>(`/v1/skills?deployment=${dep}`, user).then((s) => setSkills(s.filter((x) => x.certified && !x.decertified && x.maxGradeD >= floor))).catch(() => setSkills([])); }, [dep, user, floor]);
    async function preview() {
        setBusy(true);
        setReq(null);
        const s = skills.find((x) => x.name === skill);
        const r = await guard(api<Run>("/v1/runs", user, { method: "POST", body: { deployment: dep, skill, version: s?.version ?? "1.0.0", params: {} } }));
        setBusy(false);
        if (r)
            setRun(r);
    }
    async function request() {
        if (!run)
            return;
        setBusy(true);
        const r = await guard(api<ReleaseRequest>("/v1/requests", user, { method: "POST", body: { deployment: dep, run: run.id, purpose } }));
        setBusy(false);
        if (r) {
            setReq(r);
            setRun(null);
            onRequested();
        }
    }
    return (<div className="card" data-testid="pov">
      <h2>{t(lang, "povPreview")}</h2>
      <p className="muted">{t(lang, "povIntro")}</p>
      {error && <div className="error" role="alert">{error}</div>}
      <div className="vote">
        {skills.length > 1 && <label>{t(lang, "skills")} <select value={skill} onChange={(e) => setSkill(e.target.value)} data-testid="pov-skill" aria-label="pov-skill">{skills.map((s) => <option key={s.name} value={s.name}>{lang === "ar" ? s.description_ar : s.description}</option>)}</select></label>}
        <button className="primary" onClick={preview} disabled={busy} data-testid="run-pov">{t(lang, "runPov")}</button>
        {busy && <Progress label={t(lang, "progressRunning")}/>}
      </div>
      {run && (<div data-testid="pov-run">
          <CertificateDetails cert={run.certificate} lang={lang}/>
          <div className="card" data-testid="pov-preview"><h3>{t(lang, "outputPreview")} · {run.outputRef.rows} {t(lang, "rows")}</h3><RowsPreview rows={run.rows} fields={run.manifest.fields} lang={lang} limit={8} testid="pov-rows"/></div>
          <label>{t(lang, "povPurpose")}<textarea rows={2} value={purpose} onChange={(e) => setPurpose(e.target.value)} data-testid="pov-purpose"/></label>
          <div className="vote"><button className="primary" onClick={request} disabled={busy || purpose.trim().length < 20 || run.status !== "complete"} data-testid="pov-request">{t(lang, "povRequest")}</button></div>
        </div>)}
      {req && <div className="ok" role="status" data-testid="pov-requested"><Headline h={req.certificate.headline} lang={lang} compact/> <span className="pill">{req.status}</span></div>}
    </div>);
}
export function SkillRequests({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [rows, setRows] = useState<SkillRequest[]>([]);
    const [note, setNote] = useState<Record<string, string>>({});
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<SkillRequest[]>(`/v1/skill-requests?deployment=${dep}`, user)).then((r) => r && setRows(r)), [dep, user, guard]);
    useEffect(() => { load(); }, [load]);
    async function close(id: string, status: string) { if (await guard(api(`/v1/skill-requests/${id}/close`, user, { method: "POST", body: { status, note: note[id] ?? "" } })))
        load(); }
    const open = rows.filter((r) => r.status === "open");
    return (<div className="card" data-testid="skill-requests">
      <h2>{t(lang, "skillRequests")} <span className="muted">({open.length} {t(lang, "openRequests")})</span></h2>
      {error && <div className="error" role="alert">{error}</div>}
      {open.length === 0 && <EmptyState text={t(lang, "nothingYet")}/>}
      {open.map((r) => (<div key={r.id} className="block" data-testid={`skill-request-${r.id}`}>
          <div><strong>{lang === "ar" ? r.questionText_ar : r.questionText}</strong> · <span className="muted">{t(lang, "requestedBy")} {r.requester} · {formatDate(r.createdAt, lang)}</span></div>
          <div className="muted">{t(lang, "skillRequestFields")}: {r.fieldsNeeded.join(", ") || "—"}</div>
          <blockquote className="purpose-quote">{r.why}</blockquote>
          <div className="vote">
            <label className="grow">{t(lang, "closeNote")} <input value={note[r.id] ?? ""} onChange={(e) => setNote({ ...note, [r.id]: e.target.value })} data-testid={`close-note-${r.id}`}/></label>
            <button onClick={() => close(r.id, "planned")} data-testid={`accept-${r.id}`}>{t(lang, "closeRequest")} ✓</button>
            <button onClick={() => close(r.id, "declined")} data-testid={`decline-${r.id}`}>{t(lang, "closeRequest")} ✗</button>
          </div>
        </div>))}
    </div>);
}
export function SponsorPrint({ ctx, s, reg }: {
    ctx: Ctx;
    s: Summary | null;
    reg: RegisterRow[];
}) {
    const { lang, dep, deps, status } = ctx;
    const d = deps.find((x) => x.id === dep);
    const name = lang === "ar" && d?.name_ar ? d.name_ar : d?.name ?? dep;
    const lines = weekLines(reg, lang);
    return (<div className="reading sponsor" data-testid="sponsor-print">
      <div className="no-print vote"><a href="#/home">← {t(lang, "dashboard")}</a><button onClick={() => window.print()} data-testid="print-page">{t(lang, "printPage")}</button></div>
      <h1>{t(lang, "sponsorTitle")}</h1>
      <p>{name} · {status?.pack.id}@{status?.pack.version}{s?.from && ` · ${formatDate(s.from, lang)} — ${s?.to ? formatDate(s.to, lang) : ""}`}</p>
      <Tiles s={s} pending={[]} lang={lang}/>
      {lines.length === 0 ? <p className="muted">{t(lang, "noPeriodReleases")}</p> : <ul data-testid="week-lines">{lines.map((l) => <li key={l}>{l}</li>)}</ul>}
      <p><strong>{t(lang, "agreementTile")}:</strong> <span data-gate-text="true">{s ? (s.agreementText ? <Bi x={s.agreementText} lang={lang}/> : s.agreementRate) : "—"}</span></p>
      <Technical lang={lang}>{reg.filter((r) => r.outcome === "release").map((r) => `${r.leafIndex}\t${r.createdAt}\t${r.certificate}\t${r.outbox ?? ""}`).join("\n")}</Technical>
    </div>);
}
export function LeadHome({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, sub } = ctx;
    const [s, setS] = useState<Summary | null>(null);
    const [reg, setReg] = useState<RegisterRow[]>([]);
    const [pending, setPending] = useState<RequestListItem[]>([]);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => {
        guard(api<Summary>(`/v1/summary?deployment=${dep}`, user)).then((x) => x && setS(x));
        guard(api<RegisterRow[]>(`/v1/register?deployment=${dep}`, user)).then((x) => x && setReg(x));
        guard(api<RequestListItem[]>(`/v1/requests?deployment=${dep}&status=pending`, user)).then((x) => x && setPending(x));
    }, [dep, user, guard]);
    const { updatedAt, refresh } = useLive(load, 15000);
    if (sub[0] === "print")
        return <SponsorPrint ctx={ctx} s={s} reg={reg}/>;
    const releases = reg.filter((r) => r.outcome === "release").reverse();
    return (<div data-testid="lead-home">
      {error && <div className="error" role="alert">{error}</div>}
      <div className="vote no-print"><a href="#/home/print" data-testid="export-sponsor">{t(lang, "exportSponsor")}</a></div>
      <Tiles s={s} pending={pending} lang={lang}/>
      <ChaseList ctx={ctx} pending={pending} onChanged={refresh} updatedAt={updatedAt} refresh={refresh}/>
      <div className="grid">
        <PovPreview ctx={ctx} onRequested={refresh}/>
        <SkillRequests ctx={ctx}/>
      </div>
      {s && s.budget.length > 0 && <div className="card" data-testid="budget-bars"><h3>{t(lang, "budgetBars")}</h3>{s.budget.map((b) => (<div key={b.cohort}><div className="muted">{b.cohort.split(":")[1] ?? b.cohort} · {t(lang, "ofLimit").replace("{n}", String(b.consumed + b.reserved)).replace("{limit}", String(b.limit)).replace("{period}", b.period)}</div><div className="bar" role="img" aria-label={`${b.consumed} of ${b.limit}`}><span style={{ width: `${Math.min(100, Math.round(100 * (b.consumed + b.reserved) / Math.max(b.limit, 1)))}%` }}/></div></div>))}</div>}
      <div className="card" data-testid="acceptance-timeline">
        <h2>{t(lang, "acceptanceTimeline")}</h2>
        {releases.length === 0 && <EmptyState text={t(lang, "noReleases")}/>}
        <div className="cards">{releases.map((r) => (<div key={r.id} className="block" data-testid={`release-${r.id}`}>
            <Headline h={r.headline} lang={lang} compact/>
            <div>{r.skill ?? r.mechanism} · {formatDate(r.createdAt, lang)}{r.header && <span className="muted"> · {r.header.requester.displayName}</span>}</div>
            {r.purpose && <div className="muted small">“{r.purpose}”</div>}
            <Technical lang={lang}>{r.certificate} · {t(lang, "bundlePath")}: {r.outbox} · {t(lang, "leaf")} {r.leafIndex}</Technical>
          </div>))}</div>
      </div>
    </div>);
}
