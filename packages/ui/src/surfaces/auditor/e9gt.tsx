import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Lang, t } from '../../gna';
import type { ControlEvidence, ControlsIndex, EvidenceHit } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
import { Headline } from '../../components/uoj';
import { ReceiptDrilldown } from './rd7t';
import { currentPeriod } from '../lead/rjb';
export function ControlsExplorer({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly: boolean;
}) {
    const { user, lang, dep } = ctx;
    const [period, setPeriod] = useState(currentPeriod());
    const [idx, setIdx] = useState<ControlsIndex | null>(null);
    const [fw, setFw] = useState<string | null>(null);
    const [control, setControl] = useState<ControlEvidence | null>(null);
    const [hit, setHit] = useState<EvidenceHit | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => { setControl(null); setHit(null); guard(api<ControlsIndex>(`/v1/controls/index?deployment=${dep}&period=${period}`, user)).then((i) => { if (i) {
        setIdx(i);
        setFw((f) => f && i.frameworks[f] ? f : Object.keys(i.frameworks)[0] ?? null);
    } }); }, [dep, user, period, guard]);
    async function open(cid: string) {
        setHit(null);
        const c = await guard(api<ControlEvidence>(`/v1/controls?deployment=${dep}&framework=${fw}&control=${encodeURIComponent(cid)}&period=${period}`, user));
        if (c)
            setControl(c);
    }
    return (<div data-testid="controls-explorer">
      {error && <div className="error" role="alert">{error}</div>}
      <div className="card">
        <h2>{t(lang, "controlsExplorer")} <label className="muted">{t(lang, "period")} <input value={period} onChange={(e) => setPeriod(e.target.value)} style={{ width: "8rem" }} data-testid="period"/></label></h2>
        {idx && <div className="tabs" role="tablist" aria-label={t(lang, "frameworks")}>{Object.keys(idx.frameworks).map((f) => <button key={f} role="tab" aria-selected={fw === f} onClick={() => { setFw(f); setControl(null); setHit(null); }} data-testid={`fw-${f}`}>{f}</button>)}</div>}
        {idx && fw && <ControlList rows={idx.frameworks[fw]} lang={lang} onPick={open} selected={control?.control ?? null}/>}
      </div>
      {control && <EvidenceTable c={control} lang={lang} onPick={setHit} selected={hit}/>}
      {hit && control && <ReceiptDrilldown ctx={ctx} hit={hit} control={control} readOnly={readOnly}/>}
    </div>);
}
function ControlList({ rows, lang, onPick, selected }: {
    rows: ControlsIndex["frameworks"][string];
    lang: Lang;
    onPick: (c: string) => void;
    selected: string | null;
}) {
    if (rows.length === 0)
        return <EmptyState text={t(lang, "nothingYet")}/>;
    return (<table data-testid="control-list">
      <thead><tr><th scope="col">{t(lang, "control")}</th><th scope="col"><span className="sr-only">title</span></th><th scope="col">{t(lang, "releasesCol")}</th><th scope="col">{t(lang, "refusalsCol")}</th><th scope="col">{t(lang, "sensorHoursCol")}</th></tr></thead>
      <tbody>{rows.map((r) => (<tr key={r.control} className={"clickable" + (selected === r.control ? " selected" : "")} onClick={() => onPick(r.control)} data-testid={`control-${r.control}`}>
          <td><strong>{r.control}</strong></td><td className="muted">{r.title} {r.evidence && <span className="pill">{r.evidence}</span>}</td><td>{r.releases}</td><td>{r.refusals}</td><td>{r.sensorHours}</td>
        </tr>))}</tbody>
    </table>);
}
function EvidenceTable({ c, lang, onPick, selected }: {
    c: ControlEvidence;
    lang: Lang;
    onPick: (h: EvidenceHit) => void;
    selected: EvidenceHit | null;
}) {
    return (<div className="card" data-testid="evidence-table">
      <h2>{t(lang, "evidenceFor")} {c.framework} / {c.control}</h2>
      {c.provenance && <div className="muted"><strong>{t(lang, "provenance")}:</strong> {c.provenance.title} — “{c.provenance.sourceText}” <em>({c.provenance.sourceRef}; {t(lang, "evidenceTier")} {c.provenance.evidence})</em></div>}
      {c.evidence.length === 0 && <EmptyState text={t(lang, "noEvidence")}/>}
      {c.evidence.length > 0 && <table>
        <thead><tr><th scope="col">{t(lang, "leaf")}</th><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">{t(lang, "mechanisms")}</th><th scope="col"><span className="sr-only">{t(lang, "drillDown")}</span></th></tr></thead>
        <tbody>{c.evidence.map((h) => (<tr key={h.leaf} className={"clickable" + (selected?.leaf === h.leaf ? " selected" : "")} onClick={() => onPick(h)} data-testid={`evidence-${h.leaf}`}>
            <td>#{h.leaf} <span className={h.outcome === "release" ? "ok" : "bad"}>{h.outcome}</span><div className="muted">{h.decidedAt}</div></td>
            <td><Headline h={h.headline} lang={lang} compact/></td><td className="muted">{h.mechanisms.join(", ")}</td><td>{t(lang, "drillDown")} →</td>
          </tr>))}</tbody>
      </table>}
    </div>);
}
