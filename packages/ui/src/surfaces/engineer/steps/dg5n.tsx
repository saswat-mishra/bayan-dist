import { useEffect, useState } from "react";
import { api } from '../../../vhq7';
import { Lang, t } from '../../../gna';
import type { Run, UpliftMenu } from '../../../wz0g';
import { describeOption } from '../../../b3w';
import { CertificateDetails } from '../../../components/xsd';
import { Progress } from '../../../components/nv8';
import { RowsPreview } from '../../../components/hnm';
import { OutputPreview } from './edn5';
import { Codes, Iso } from '../../../d7t';
export { describeOption } from '../../../b3w';
interface Props {
    run: Run;
    lang: Lang;
    user: string;
    guard: <T>(p: Promise<T>) => Promise<T | null>;
    onRun: (r: Run) => void;
    onRequest: () => void;
    onBusy?: (b: boolean) => void;
}
export function ImproveStep({ run, lang, user, guard, onRun, onRequest, onBusy }: Props) {
    const [menu, setMenu] = useState<UpliftMenu | null>(null);
    const applied = !!run.derivedFrom;
    const [job, setJob] = useState<{
        id: string;
        status: string;
        certificate?: string;
    } | null>(null);
    const [busy, setBusy] = useState(false);
    const [compare, setCompare] = useState(false);
    const [parent, setParent] = useState<Run | null>(null);
    useEffect(() => {
        setMenu(null);
        if (run.certificate.d < 2 && run.status === "complete")
            guard(api<UpliftMenu>(`/v1/runs/${run.id}/uplift?target=D2`, user, { method: "POST" })).then((m) => m && setMenu(m));
    }, [run.id, run.certificate.d, run.status, user, guard]);
    useEffect(() => { setParent(null); setCompare(false); if (run.derivedFrom)
        api<Run>(`/v1/runs/${run.derivedFrom}`, user).then(setParent).catch(() => setParent(null)); }, [run.derivedFrom, user]);
    async function apply(i: number) {
        setBusy(true);
        onBusy?.(true);
        const r = await guard(api<Run>(`/v1/runs/${run.id}/uplift/apply?option=${i}`, user, { method: "POST" }));
        setBusy(false);
        onBusy?.(false);
        if (r)
            onRun(r);
    }
    async function upgrade() {
        const j = await guard(api<{
            id: string;
            status: string;
        }>(`/v1/runs/${run.id}/upgrade?target=D3`, user, { method: "POST" }));
        if (!j)
            return;
        setJob(j);
        const poll = async () => {
            const s = await api<{
                id: string;
                status: string;
                certificate?: string;
            }>(`/v1/jobs/${j.id}`, user);
            setJob(s);
            if (s.status === "done")
                onRun(await api<Run>(`/v1/runs/${run.id}`, user));
            else
                setTimeout(poll, 300);
        };
        setTimeout(poll, 300);
    }
    const d3Blocked = run.certificate.d !== 2;
    return (<div data-testid="step-improve">
      <CertificateDetails cert={run.certificate} lang={lang}/>
      <div className="card" data-testid="uplift-menu">
        <h2>{t(lang, "stepImprove")}</h2>
        <p className="muted">{t(lang, "improveIntro")}</p>
        {run.certificate.d >= 2 && <div className="muted"><Codes text={t(lang, "noUplift")}/></div>}
        {menu?.unreachableReason && <div className="warn"><Iso>{menu.unreachableReason}</Iso></div>}
        {menu && <ol className="options">{menu.options.map((o, i) => (<li key={i} className={o.recommended ? "recommended" : undefined}>
            <span data-testid={`option-${i}`}><Codes text={describeOption(o, lang)}/></span>
            {o.loses.length > 0 && <span className="warn"> — {t(lang, "losesLoadBearing")} <Iso>{o.loses.join(", ")}</Iso></span>}
            {o.recommended && <strong> {t(lang, "arrowBack")} {t(lang, "recommended")}</strong>}{" "}
            <button className={o.recommended ? "primary" : undefined} onClick={() => apply(i)} disabled={!o.reachesTarget || busy} data-testid={`apply-${i}`}>{t(lang, "applyOption")}</button>
          </li>))}</ol>}
        {busy && <Progress label={t(lang, "progressApplying")}/>}
        <div className="vote">
          <button onClick={upgrade} disabled={d3Blocked || !!job || busy} data-testid="upgrade-d3" aria-describedby={d3Blocked ? "d3-why" : undefined}><Codes text={t(lang, "upgradeD3")} plain/></button>
          {d3Blocked && <span id="d3-why" className="muted" data-testid="d3-why"><Codes text={t(lang, "d3Unavailable")}/></span>}
          {job && <span className="muted" data-testid="job">{job.status === "done" ? <Iso>{job.certificate ?? ""}</Iso> : t(lang, "upgradeRunning")}</span>}
          <button className={applied || run.certificate.d >= 2 ? "primary" : undefined} onClick={onRequest} disabled={busy} data-testid="to-request">{t(lang, "stepRequest")} {t(lang, "arrow")}</button>
        </div>
      </div>
      {applied && (<div className="vote applied-line" role="status" data-testid="applied">
          <span className="ok">{t(lang, "applied")}</span>
          {parent && <button className="link" onClick={() => setCompare(!compare)} data-testid="compare-toggle" aria-pressed={compare}>{compare ? t(lang, "hideCompare") : t(lang, "compareWithBefore")}</button>}
        </div>)}
      {compare && parent ? (<div className="grid" data-testid="compare">
          <div className="card"><h2>{t(lang, "beforeLabel")} · <Iso>{parent.certificate.label}</Iso></h2><RowsPreview rows={parent.rows} fields={parent.manifest.fields} lang={lang} limit={8} testid="rows-before"/></div>
          <div className="card"><h2>{t(lang, "afterLabel")} · <Iso>{run.certificate.label}</Iso></h2><RowsPreview rows={run.rows} fields={run.manifest.fields} lang={lang} limit={8} testid="rows-after"/></div>
        </div>) : <OutputPreview run={run} lang={lang}/>}
    </div>);
}
