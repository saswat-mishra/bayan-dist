import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Key, Lang, t } from '../../gna';
import type { BundleFiles, ControlEvidence, EvidenceHit, ReceiptHeader, ReleaseRequest } from '../../wz0g';
import { Headline } from '../../components/uoj';
import { ControlsTable } from '../../components/oqx';
import { PersonCard } from '../../components/c3u';
import { Technical } from '../../components/n4x';
import { VerifyCommand } from '../../components/uc5j';
import { Term, formatDate } from '../../d7t';
interface Full extends ReleaseRequest {
    complianceCertificate?: {
        controls: Record<string, string[]>;
        mechanisms: string[];
    };
}
const DISPOSAL: Record<ReceiptHeader["disposal"]["status"], Key> = { pending: "disposalPending", attested: "disposalAttested", overdue: "disposalOverdue", "not-released": "disposalNone" };
export function ReceiptHeaderView({ h, lang }: {
    h: ReceiptHeader;
    lang: Lang;
}) {
    return (<div className="receipt-header block" data-testid="receipt-header">
      <div><strong>{t(lang, "receiptRequester")}:</strong> {h.requester.displayName}</div>
      <div><strong>{t(lang, "receiptPurpose")}:</strong> <span data-testid="receipt-purpose">{h.purpose}</span></div>
      <div><strong>{t(lang, "receiptApprovers")}:</strong>{" "}
        {h.approvers.length === 0 ? <span data-testid="receipt-no-approvers">{t(lang, "noApprovers")}</span>
            : h.approvers.map((a) => <PersonCard key={a.principal} lang={lang} testid={`approver-${a.principal}`} p={{ name: a.displayName, role: a.role, authority: a.authority }}/>)}</div>
      {h.decidedAt && <div><strong>{t(lang, "receiptDecided")}:</strong> {formatDate(h.decidedAt, lang)}</div>}
      <div><strong>{t(lang, "receiptRetention")}:</strong> {h.retention.until ? formatDate(h.retention.until, lang) : "—"}</div>
      <div><strong>{t(lang, "receiptDisposal")}:</strong> <span data-testid="disposal" data-status={h.disposal.status}>{t(lang, DISPOSAL[h.disposal.status])}</span>{h.disposal.dueBy && h.disposal.status !== "attested" && <span className="muted"> · {formatDate(h.disposal.dueBy, lang)}</span>}</div>
      {h.lookupAvailable && <div className="muted small">{t(lang, "lookupTitle")}: ✓</div>}
    </div>);
}
export function ReceiptDrilldown({ ctx, hit, control, readOnly }: {
    ctx: Ctx;
    hit: EvidenceHit;
    control: ControlEvidence;
    readOnly: boolean;
}) {
    const { user, lang, status } = ctx;
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
    const header = bundle?.header ?? hit.header ?? null;
    const artefacts = bundle ? Object.entries(bundle.files).filter(([k]) => k.startsWith("artefacts/")) : [];
    const trust = bundle?.trustDir ?? status?.trustDir ?? "<client-published trust dir>";
    return (<div className="card" data-testid="receipt">
      <h2>{t(lang, "drillDown")} · {t(lang, "leaf")} #{hit.leaf}</h2>
      {error && <div className="error" role="alert">{error}</div>}
      <Headline h={hit.headline} lang={lang}/>
      {header && <ReceiptHeaderView h={header} lang={lang}/>}
      <ul className="mechanisms" aria-label={t(lang, "mechanisms")}>{hit.mechanisms.map((m) => <li key={m}><Term code={m} showCode/></li>)}</ul>
      {controls ? <ControlsTable controls={controls} lang={lang}/> : <div className="muted">{control.framework}: {control.control}</div>}
      {bundle?.registerLine && <div className="block" data-testid="register-line"><h3>{t(lang, "registerLine")}</h3><p data-gate-text="true">{lang === "ar" ? bundle.registerLine.lang.ar : bundle.registerLine.lang.en}</p><div className="register-line" data-technical="true">{bundle.registerLine.line}</div></div>}
      {bundle && (<div>
          <VerifyCommand command={bundle.verify ?? `bayan-verify ${bundle.path} --trust ${trust} --assert-offline`} lang={lang}/>
          <Technical lang={lang} copyText={bundle.path}>
            <div>{t(lang, "bundlePath")}: {bundle.path}</div>
            <div>trust: {trust}</div>
            <div>{hit.label}</div>
            <ul>{artefacts.map(([k, v]) => <li key={k}>{k} · {v.bytes} B · sha256 {v.sha256}{readOnly || !v.text ? <span className="muted"> — {t(lang, "digestsOnly")}</span> : <details><summary>rows</summary><pre data-testid="artefact-text">{v.text.slice(0, 2000)}</pre></details>}</li>)}</ul>
          </Technical>
        </div>)}
      {!hit.release && <div className="muted">{t(lang, "tRefused")} — {t(lang, "leaf")} #{hit.leaf}</div>}
    </div>);
}
