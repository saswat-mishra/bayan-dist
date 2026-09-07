import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { BundleFiles, ControlEvidence, EvidenceHit, ReleaseRequest } from '../../wz0g';
import { Headline } from '../../components/uoj';
import { ControlsTable } from '../../components/oqx';
import { VerifyCommand } from '../../components/uc5j';
interface Full extends ReleaseRequest {
    complianceCertificate?: {
        controls: Record<string, string[]>;
        mechanisms: string[];
    };
}
export function ReceiptDrilldown({ ctx, hit, control, readOnly }: {
    ctx: Ctx;
    hit: EvidenceHit;
    control: ControlEvidence;
    readOnly: boolean;
}) {
    const { user, lang } = ctx;
    const [bundle, setBundle] = useState<BundleFiles | null>(null);
    const [req, setReq] = useState<Full | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => {
        setBundle(null);
        setReq(null);
        if (hit.release)
            guard(api<BundleFiles>(`/v1/bundles/${hit.release}`, user)).then((b) => b && setBundle(b));
        if (hit.request)
            api<Full>(`/v1/requests/${hit.request}`, user).then(setReq).catch(() => setReq(null));
    }, [hit, user, guard]);
    const controls = req?.complianceCertificate?.controls;
    const artefacts = bundle ? Object.entries(bundle.files).filter(([k]) => k.startsWith("artefacts/")) : [];
    return (<div className="card" data-testid="receipt">
      <h2>{t(lang, "drillDown")} · {t(lang, "leaf")} #{hit.leaf} · <code>{hit.label}</code></h2>
      {error && <div className="error" role="alert">{error}</div>}
      <Headline h={hit.headline} lang={lang}/>
      <div><strong>{t(lang, "mechanisms")}:</strong> {hit.mechanisms.join(" · ")}</div>
      {controls ? <ControlsTable controls={controls} lang={lang}/> : <div className="muted">{control.framework}: {control.control}</div>}
      {bundle && (<div>
          <div>{t(lang, "bundlePath")}: <code>{bundle.path}</code></div>
          <ul>{artefacts.map(([k, v]) => <li key={k}><code>{k}</code> <span className="muted">{v.bytes} B · sha256 {v.sha256.slice(0, 16)}…</span>{readOnly || !v.text ? <span className="muted"> — {t(lang, "digestsOnly")}</span> : <details><summary>rows</summary><pre data-testid="artefact-text">{v.text.slice(0, 2000)}</pre></details>}</li>)}</ul>
          <VerifyCommand command={`bayan-verify ${bundle.path} --trust <client-published trust dir> --assert-offline`} lang={lang}/>
        </div>)}
      {!hit.release && <div className="muted">{t(lang, "tRefused")} — {t(lang, "leaf")} #{hit.leaf}</div>}
    </div>);
}
