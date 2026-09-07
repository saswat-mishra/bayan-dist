import { useEffect, useState } from "react";
import { api } from '../../../vhq7';
import { Lang, t } from '../../../gna';
import type { Run, UpliftMenu, UpliftOption } from '../../../wz0g';
import { CertificateDetails } from '../../../components/xsd';
import { OutputPreview } from './edn5';
export function describeOption(o: UpliftOption, lang: Lang): string {
    const parts = o.changes.map((c) => {
        if (c.transform === "hmac_enclave")
            return `${t(lang, "replaceWith")} ${c.field} ${t(lang, "withPseudonyms")} — ${t(lang, "keepsRanking")}`;
        if (c.transform === "drop")
            return `${t(lang, "dropField")} ${c.field}`;
        if (c.transform === "bucket")
            return `${t(lang, "bucketField")} ${c.field}`;
        if (c.transform === "coarsen")
            return `${t(lang, "coarsenField")} ${c.field}`;
        return `${c.transform} ${c.field}`;
    });
    const path = o.requiredR === "R1" ? t(lang, "noReviewer") : o.requiredR === "R2" ? t(lang, "oneReviewer") : t(lang, "twoReviewers");
    return `${parts.join("; ")} → ${t(lang, "releasesWith")} ${path} (${o.d})`;
}
interface Props {
    run: Run;
    lang: Lang;
    user: string;
    guard: <T>(p: Promise<T>) => Promise<T | null>;
    onRun: (r: Run) => void;
    onRequest: () => void;
}
export function ImproveStep({ run, lang, user, guard, onRun, onRequest }: Props) {
    const [menu, setMenu] = useState<UpliftMenu | null>(null);
    const applied = !!run.derivedFrom;
    const [job, setJob] = useState<{
        id: string;
        status: string;
        certificate?: string;
    } | null>(null);
    useEffect(() => {
        setMenu(null);
        if (run.certificate.d < 2 && run.status === "complete")
            guard(api<UpliftMenu>(`/v1/runs/${run.id}/uplift?target=D2`, user, { method: "POST" })).then((m) => m && setMenu(m));
    }, [run.id, run.certificate.d, run.status, user, guard]);
    async function apply(i: number) {
        const r = await guard(api<Run>(`/v1/runs/${run.id}/uplift/apply?option=${i}`, user, { method: "POST" }));
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
    return (<div data-testid="step-improve">
      <CertificateDetails cert={run.certificate} lang={lang}/>
      {applied && <div className="ok" role="status" data-testid="applied">{t(lang, "applied")}</div>}
      <OutputPreview run={run} lang={lang}/>
      <div className="card" data-testid="uplift-menu">
        <h2>{t(lang, "stepImprove")}</h2>
        <p className="muted">{t(lang, "improveIntro")}</p>
        {run.certificate.d >= 2 && <div className="muted">{t(lang, "noUplift")}</div>}
        {menu?.unreachableReason && <div className="warn">{menu.unreachableReason}</div>}
        {menu && <ol>{menu.options.map((o, i) => (<li key={i}>
            <span data-testid={`option-${i}`}>{describeOption(o, lang)}</span>
            {o.loses.length > 0 && <span className="warn"> — loses load-bearing {o.loses.join(", ")}</span>}
            {o.recommended && <strong> ← {t(lang, "recommended")}</strong>}{" "}
            <button onClick={() => apply(i)} disabled={!o.reachesTarget} data-testid={`apply-${i}`}>{t(lang, "applyOption")}</button>
          </li>))}</ol>}
        <div className="vote">
          <button onClick={upgrade} disabled={run.certificate.d !== 2 || !!job} data-testid="upgrade-d3">{t(lang, "upgradeD3")}</button>
          {job && <span className="muted" data-testid="job">{job.status === "done" ? job.certificate : t(lang, "upgradeRunning")}</span>}
          <button className="primary" onClick={onRequest} data-testid="to-request">{t(lang, "stepRequest")} →</button>
        </div>
      </div>
    </div>);
}
