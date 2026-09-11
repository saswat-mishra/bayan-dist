import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { BundleFiles } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
import { Progress } from '../../components/nv8';
import { RowsPreview } from '../../components/hnm';
import { VerifyCommand } from '../../components/uc5j';
import { Iso, Name, Runs, formatDate } from '../../d7t';
function artefactRows(b: BundleFiles): Record<string, unknown>[] | null {
    for (const [name, f] of Object.entries(b.files)) {
        if (!name.startsWith("artefacts/") || !f.text)
            continue;
        try {
            const j = JSON.parse(f.text);
            if (Array.isArray(j) && j.every((r) => r && typeof r === "object"))
                return j as Record<string, unknown>[];
        }
        catch { }
    }
    return null;
}
export function ReleaseRecord({ ctx, id }: {
    ctx: Ctx;
    id: string;
}) {
    const { user, lang } = ctx;
    const [bundle, setBundle] = useState<BundleFiles | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(async () => {
        const tl = await guard(api<{
            bundle: {
                release?: string;
                path?: string;
            } | null;
        }>(`/v1/requests/${id}/timeline`, user));
        const rel = tl?.bundle?.release ?? tl?.bundle?.path?.split("/").pop()?.replace(/^release-/, "");
        if (!rel)
            return;
        const b = await guard(api<BundleFiles>(`/v1/bundles/${rel}`, user));
        if (b)
            setBundle(b);
    }, [id, user, guard]);
    useEffect(() => { void load(); }, [load]);
    if (error)
        return <div className="error" role="alert">{error}</div>;
    if (!bundle)
        return <Progress label={t(lang, "loading")}/>;
    const h = bundle.header ?? null;
    const rows = artefactRows(bundle);
    const artefacts = Object.entries(bundle.files).filter(([n]) => n.startsWith("artefacts/"));
    return (<div className="record" data-testid="release-record">
      <div className="vote no-print">
        <button className="primary" onClick={() => window.print()} data-testid="record-print"><Runs text={t(lang, "recordPrint")}/></button>
        <a href={`#/requests/${id}`} data-testid="record-back">{t(lang, "recordBack")}</a>
      </div>
      <h1 data-testid="record-title">{t(lang, "recordTitle")}</h1>
      <p className="muted">{t(lang, "recordSub")}</p>
      {h && (<dl className="facts" data-testid="record-facts">
          <dt>{t(lang, "requestedBy")}</dt><dd><Name name={h.requester.displayName} lang={lang} title={h.requester.principal}/></dd>
          <dt>{t(lang, "whyTheyNeedIt")}</dt><dd><q>{h.purpose}</q></dd>
          <dt>{t(lang, "recordAuthority")}</dt>
          <dd data-testid="record-approvers">
            {h.approvers.length === 0 ? t(lang, "releasesByPolicy") : h.approvers.map((a) => (<div key={a.principal}><Name name={a.displayName} lang={lang} title={a.principal}/> <span className="muted">— {t(lang, a.role as "reviewer")}{a.authority && <> · <Iso>{a.authority}</Iso></>}</span></div>))}
          </dd>
          {h.decidedAt && <><dt>{t(lang, "recordDecided")}</dt><dd>{formatDate(h.decidedAt, lang)}</dd></>}
          {h.retention.until && <><dt>{t(lang, "retentionEnds")}</dt><dd>{formatDate(h.retention.until, lang)}</dd></>}
        </dl>)}
      <section data-testid="record-what-left">
        <h2>{t(lang, "recordWhatLeft")}</h2>
        <ul className="artefacts">
          {artefacts.map(([name, f]) => (<li key={name}><Iso>{name.replace("artefacts/", "")}</Iso> <span className="muted small">· <Iso>{`${f.bytes} B`}</Iso> · <Iso className="mono">{`${f.sha256.slice(0, 16)}…`}</Iso></span></li>))}
        </ul>
        {rows && <RowsPreview rows={rows} lang={lang} limit={rows.length}/>}
      </section>
      <section data-testid="record-verify">
        <h2>{t(lang, "recordVerify")}</h2>
        {bundle.verify && <VerifyCommand command={bundle.verify} lang={lang}/>}
        {bundle.registerLine && <p className="register-line" data-technical="true"><Iso>{bundle.registerLine.line}</Iso></p>}
      </section>
      {artefacts.length === 0 && <EmptyState text={t(lang, "recordSub")}/>}
    </div>);
}
