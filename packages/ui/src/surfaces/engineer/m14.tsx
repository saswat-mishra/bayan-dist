import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard, useLive } from '../../q1n';
import { Lang, pick, t } from '../../gna';
import type { BundleFiles, ReleaseRequest, Run, Timeline as TimelineJson } from '../../wz0g';
import { Timeline } from '../../components/rvu0';
import { Progress } from '../../components/nv8';
import { RowsPreview } from '../../components/hnm';
import { StateChip } from '../../components/drm';
import { Technical } from '../../components/n4x';
import { VerifyCommand } from '../../components/uc5j';
import { Bi, Iso, Name, Runs, formatDate } from '../../d7t';
export function pseudonymField(run: Run | null | undefined): string | null {
    return run?.manifest.fields.find((f) => f.transform === "hmac_enclave")?.name ?? null;
}
export function countField(run: Run | null | undefined): string | null {
    const first = run?.rows[0];
    if (!first)
        return null;
    return Object.keys(first).find((k) => typeof first[k] === "number") ?? null;
}
function RegisterLine({ bundle, lang }: {
    bundle: BundleFiles;
    lang: Lang;
}) {
    const [copied, setCopied] = useState(false);
    const [mode, setMode] = useState<"machine" | "human">("machine");
    const rl = bundle.registerLine;
    if (!rl)
        return null;
    async function copy() {
        try {
            await navigator.clipboard.writeText(rl!.line);
        }
        catch { }
        setCopied(true);
        setTimeout(() => setCopied(false), 2500);
    }
    return (<div className="register" data-testid="register-line">
      <div className="tabs" role="tablist" aria-label={t(lang, "registerLine")}>
        <button role="tab" aria-selected={mode === "machine"} onClick={() => setMode("machine")} data-testid="register-machine">{t(lang, "registerMachine")}</button>
        <button role="tab" aria-selected={mode === "human"} onClick={() => setMode("human")} data-testid="register-human">{t(lang, "registerHuman")}</button>
      </div>
      <div className="register-line" data-technical="true" data-testid="register-line-text" hidden={mode !== "machine"}><Iso>{rl.line}</Iso></div>
      <p data-gate-text="true" data-testid="register-words" hidden={mode !== "human"}><Runs text={lang === "ar" ? rl.lang.ar : rl.lang.en}/></p>
      <div className="vote no-print">
        <button onClick={copy} data-testid="copy-register-line" aria-live="polite">{copied ? t(lang, "copied") : t(lang, "copy")}</button>
        <button className="ghost" onClick={() => window.print()} data-testid="print-register-line">{t(lang, "printIt")}</button>
      </div>
    </div>);
}
function LookupPanel({ ctx, run, releaseId, onLookup }: {
    ctx: Ctx;
    run: Run;
    releaseId: string;
    onLookup?: (r: ReleaseRequest) => void;
}) {
    const { user, lang, dep, pack } = ctx;
    const field = pseudonymField(run);
    const max = pack?.lookup?.maxKeys ?? 10;
    const [selected, setSelected] = useState<Set<string>>(new Set());
    const [purpose, setPurpose] = useState("");
    const [busy, setBusy] = useState(false);
    const [done, setDone] = useState<ReleaseRequest | null>(null);
    const [error, guard] = useGuard(lang);
    if (!field)
        return null;
    const toggle = (k: string) => setSelected((s) => { const n = new Set(s); if (n.has(k))
        n.delete(k);
    else if (n.size < max)
        n.add(k); return n; });
    async function submit() {
        setBusy(true);
        const r = await guard(api<ReleaseRequest>("/v1/requests", user, { method: "POST", body: { deployment: dep, purpose, mechanism: "output-check", lookup: { ofRelease: releaseId, keys: Array.from(selected) } } }));
        setBusy(false);
        if (r) {
            setDone(r);
            onLookup?.(r);
        }
    }
    return (<div data-testid="lookup">
      <p className="muted">{t(lang, "selectUpTo").replace("{n}", String(max))} · <span className="counter" data-testid="lookup-counter" aria-live="polite">{t(lang, "selectedOf").replace("{k}", String(selected.size)).replace("{max}", String(max))}</span></p>
      <RowsPreview rows={run.rows} fields={run.manifest.fields} lang={lang} selectable selected={selected} onToggle={toggle} maxSelect={max} keyField={field} sortBy={countField(run)} testid="lookup-rows"/>
      <label>{t(lang, "lookupPurpose")}<textarea rows={2} value={purpose} onChange={(e) => setPurpose(e.target.value)} data-testid="lookup-purpose" placeholder={t(lang, "purposePlaceholder")}/></label>
      <div className="vote">
        <button className="primary" disabled={selected.size === 0 || purpose.trim().length < 20 || busy || !!done} onClick={submit} data-testid="lookup-submit">{t(lang, "requestLookup")}</button>
        {busy && <Progress label={t(lang, "progressRequesting")}/>}
      </div>
      {done && <div className="ok" role="status" data-testid="lookup-done">{t(lang, "lookupSubmitted")} <a href={`#/requests/${done.id}`}>{t(lang, "openTrack")}</a></div>}
      {error && <div className="error" role="alert">{error}</div>}
    </div>);
}
export function HandoffPanel({ ctx, tl, req, bundle, run, onLookup }: {
    ctx: Ctx;
    tl: TimelineJson;
    req: ReleaseRequest | null;
    bundle: BundleFiles | null;
    run: Run | null;
    onLookup?: (r: ReleaseRequest) => void;
}) {
    const { user, lang } = ctx;
    const [downloading, setDownloading] = useState(false);
    const [error, guard] = useGuard(lang);
    const rel = tl.bundle?.release ?? req?.releaseId ?? null;
    const until = bundle?.header?.retention?.until ?? null;
    async function download() {
        if (!rel)
            return;
        setDownloading(true);
        const blob = await guard((async () => {
            const res = await fetch(`/v1/bundles/${rel}/archive`, { headers: { "X-Bayan-User": user } });
            if (!res.ok) {
                const { ApiError } = await import('../../vhq7');
                throw new ApiError(res.status, await res.json().catch(() => ({})));
            }
            return res.blob();
        })());
        setDownloading(false);
        if (!blob)
            return;
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${rel}.zip`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 5000);
    }
    return (<div className="card" data-testid="handoff-panel">
      <h2 data-testid="handoff-state"><StateChip kind="released" lang={lang} label={t(lang, "releasedTitle")}/></h2>
      {until && <p data-testid="retention-line"><strong>{t(lang, "retentionEnds")}</strong> {formatDate(until, lang)} — {t(lang, "attestBy")}</p>}
      <section data-testid="take-it-away">
        <h3>{t(lang, "takeItAway")}</h3>
        <div className="vote">
          <button className="primary" onClick={download} disabled={!rel || downloading} data-testid="download-bundle">{t(lang, "downloadBundle")}</button>
          {req && <a className="record-link" href={`#/requests/${req.id}/record`} data-testid="save-record">{t(lang, "saveRecord")}</a>}
          {downloading && <Progress label={t(lang, "downloading")}/>}
        </div>
        {error && <div className="error" role="alert">{error}</div>}
        {bundle && <RegisterLine bundle={bundle} lang={lang}/>}
        {tl.bundle && <VerifyCommand command={bundle?.verify ?? tl.bundle.verify} lang={lang}/>}
      </section>
      {tl.nextActions && tl.nextActions.length > 0 && (<section className="card quiet" data-testid="next-actions"><h3>{t(lang, "whatToDoNext")}</h3>
          <ol>{tl.nextActions.map((a) => <li key={a.kind} data-kind={a.kind} data-gate-text="true"><Bi x={a} lang={lang}/></li>)}</ol></section>)}
      {run && rel && bundle?.header?.lookupAvailable && pseudonymField(run) && (<details className="disclosure" data-testid="find-pseudonym">
          <summary data-testid="find-pseudonym-summary">{t(lang, "findPseudonym")}</summary>
          <LookupPanel ctx={ctx} run={run} releaseId={rel} onLookup={onLookup}/>
        </details>)}
      {tl.bundle && <Technical lang={lang} copyText={tl.bundle.path}><div>{t(lang, "bundlePath")}: <Iso>{tl.bundle.path}</Iso></div><div>{t(lang, "leaf")}: {tl.bundle.leafIndex}</div>{(bundle?.trustDir ?? tl.bundle.trustDir) && <div>trust: <Iso>{bundle?.trustDir ?? tl.bundle.trustDir}</Iso></div>}{req && <div>request: <Iso>{req.id}</Iso></div>}</Technical>}
    </div>);
}
export function Handoff({ ctx, id, run: runIn, onLookup }: {
    ctx: Ctx;
    id: string;
    run?: Run | null;
    onLookup?: (r: ReleaseRequest) => void;
}) {
    const { user, lang } = ctx;
    const [tl, setTl] = useState<TimelineJson | null>(null);
    const [req, setReq] = useState<ReleaseRequest | null>(null);
    const [bundle, setBundle] = useState<BundleFiles | null>(null);
    const [run, setRun] = useState<Run | null>(runIn ?? null);
    const [tab, setTab] = useState<"track" | "handoff" | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(async () => {
        const r = await guard(api<TimelineJson>(`/v1/requests/${id}/timeline`, user));
        if (!r)
            return;
        setTl(r);
        const q = await guard(api<ReleaseRequest>(`/v1/requests/${id}`, user));
        if (q)
            setReq(q);
        const rel = r.bundle?.release ?? q?.releaseId;
        if (r.status === "released" && rel)
            api<BundleFiles>(`/v1/bundles/${rel}`, user).then(setBundle).catch(() => setBundle(null));
    }, [id, user, guard]);
    useLive(load, 10000, tl === null || tl.status === "pending");
    useEffect(() => { if (runIn)
        setRun(runIn); }, [runIn]);
    useEffect(() => { if (!runIn && req?.run)
        api<Run>(`/v1/runs/${req.run}`, user).then(setRun).catch(() => setRun(null)); }, [req?.run, runIn, user]);
    const released = tl?.status === "released";
    const active = tab ?? (released ? "handoff" : "track");
    return (<div data-testid="track">
      {error && <div className="error" role="alert">{error}</div>}
      <div className="tabs" role="tablist" aria-label={t(lang, "handoff")}>
        <button role="tab" aria-selected={active === "track"} onClick={() => setTab("track")} data-testid="tab-track">{t(lang, "trackTab")}</button>
        <button role="tab" aria-selected={active === "handoff"} onClick={() => setTab("handoff")} disabled={!released} data-testid="tab-handoff">{t(lang, "handoffTab")}</button>
      </div>
      {active === "track" && <p className="muted">{t(lang, "trackIntro")}</p>}
      {tl && active === "track" && <Timeline tl={tl} lang={lang}/>}
      {tl && active === "handoff" && released && <HandoffPanel ctx={ctx} tl={tl} req={req} bundle={bundle} run={run} onLookup={onLookup}/>}
      {tl && tl.status === "pending" && tl.outstandingReviewers && tl.outstandingReviewers.length > 0 && active === "track" && (<div className="muted" data-testid="waits-for" data-kind={tl.outstandingKind ?? "eligible"}>{t(lang, tl.outstandingKind === "waiting" ? "waitingFor" : "couldBeWaitingFor")}: {tl.outstandingReviewers.map((o, i) => <span key={o.principal}>{i > 0 && ", "}<Name name={o.displayName} lang={lang}/></span>)}</div>)}
      {!tl && <div className="muted">{t(lang, "loading")}</div>}
      {tl && tl.status !== "pending" && !released && <div className="muted"><Iso>{pick(lang, tl.waitingOn)}</Iso></div>}
    </div>);
}
