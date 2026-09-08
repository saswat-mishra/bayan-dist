import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Key, Lang, t } from '../../gna';
import type { ControlEvidence, ControlsIndex, EvidenceHit, Gap, LedgerRange } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
import { StateChip } from '../../components/drm';
import { Iso, Name, formatDate } from '../../d7t';
import { ReceiptDrilldown } from './rd7t';
import { currentPeriod } from '../lead/rjb';
const WHY: Record<Gap["why"], Key> = { "no-refusal": "gapNoRefusal", "no-release": "gapNoRelease", "sensor-absent": "gapSensorAbsent", "no-sensor-hour": "gapNoSensorHour" };
export function needsAction(g: Gap): boolean {
    return g.why === "no-sensor-hour";
}
export function GapList({ gaps, lang }: {
    gaps: Gap[];
    lang: Lang;
}) {
    if (gaps.length === 0)
        return <div className="ok" data-testid="no-gaps">{t(lang, "noGaps")}</div>;
    return (<ul className="gaps" data-testid="gaps" aria-label={t(lang, "gapsFirst")}>
      {gaps.map((g) => <li key={g.control} className={"gap " + (needsAction(g) ? "action" : "info")} data-testid={`gap-${g.control}`}><strong><Iso>{g.control}</Iso></strong> — {t(lang, WHY[g.why])} <span className="muted">({g.sensorPresent ? t(lang, "withSensor") : t(lang, "withoutSensor")})</span></li>)}
    </ul>);
}
export function frameworkTitle(idx: ControlsIndex | null, fw: string, lang: Lang): string {
    const tt = idx?.frameworkTitles?.[fw];
    return (lang === "ar" ? tt?.ar : tt?.en) || tt?.en || fw;
}
export function Coverage({ ctx, readOnly, testid }: {
    ctx: Ctx;
    readOnly: boolean;
    testid?: string;
}) {
    const { user, lang, dep, pack } = ctx;
    const [range, setRange] = useState<LedgerRange | null>(null);
    const [period, setPeriod] = useState<string>(currentPeriod());
    const [idx, setIdx] = useState<ControlsIndex | null>(null);
    const [fw, setFw] = useState<string | null>(null);
    const [control, setControl] = useState<ControlEvidence | null>(null);
    const [hit, setHit] = useState<EvidenceHit | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => {
        api<LedgerRange>(`/v1/ledger/range?deployment=${dep}`, user).then((r) => { setRange(r); if (r.periods.length && !r.periods.includes(currentPeriod()))
            setPeriod(r.periods[r.periods.length - 1]); }).catch(() => setRange(null));
    }, [dep, user]);
    useEffect(() => {
        setControl(null);
        setHit(null);
        guard(api<ControlsIndex>(`/v1/controls/index?deployment=${dep}${period ? `&period=${period}` : ""}`, user)).then((i) => {
            if (!i)
                return;
            setIdx(i);
            const primary = i.primaryFramework ?? pack?.primaryFramework ?? null;
            setFw((f) => (f && i.frameworks[f]) ? f : (primary && i.frameworks[primary]) ? primary : Object.keys(i.frameworks)[0] ?? null);
        });
    }, [dep, user, period, guard, pack?.primaryFramework]);
    async function open(cid: string) {
        setHit(null);
        const c = await guard(api<ControlEvidence>(`/v1/controls?deployment=${dep}&framework=${fw}&control=${encodeURIComponent(cid)}${period ? `&period=${period}` : ""}`, user));
        if (c)
            setControl(c);
    }
    const rows = idx && fw ? idx.frameworks[fw] : [];
    const gaps = idx && fw ? idx.gaps?.[fw] ?? [] : [];
    return (<div data-testid={testid ?? "coverage"}>
      {error && <div className="error" role="alert">{error}</div>}
      <div className="card" data-testid="controls-explorer">
        <h2 className="title-inline" data-testid="coverage-title">{t(lang, "coverage")}
          <span className="inline-control"><label className="sr-only" htmlFor="coverage-period">{t(lang, "periodPicker")}</label>
            <select id="coverage-period" dir="ltr" value={period} onChange={(e) => setPeriod(e.target.value)} data-testid="period" aria-label={t(lang, "periodPicker")}>
              <option value="">{t(lang, "allTime")}</option>
              {(range?.periods.length ? range.periods : [currentPeriod()]).map((p) => <option key={p} value={p}>{p}</option>)}
            </select></span>
        </h2>
        {range?.from && <div className="muted small">{formatDate(range.from, lang)} — {range.to ? formatDate(range.to, lang) : ""} · {t(lang, "ledgerEntries").replace("{n}", String(range.leaves))}</div>}
        {idx && <div className="tabs fused" role="tablist" aria-label={t(lang, "framework")}>{Object.keys(idx.frameworks).sort((a, b) => Number(b === (idx.primaryFramework ?? pack?.primaryFramework)) - Number(a === (idx.primaryFramework ?? pack?.primaryFramework))).map((f) => {
                const primary = f === (idx.primaryFramework ?? pack?.primaryFramework);
                return <button key={f} role="tab" aria-selected={fw === f} aria-label={f} title={f} onClick={() => { setFw(f); setControl(null); setHit(null); }} data-testid={`fw-${f}`}><Iso>{frameworkTitle(idx, f, lang)}</Iso>{primary && <span className="muted small"> — {t(lang, "yourPackFramework")}</span>}</button>;
            })}</div>}
        {lang === "ar" && <p className="muted small" data-testid="control-titles-note">{t(lang, "controlTitlesEnglish")}</p>}
        {idx && fw && <section data-testid="gaps-section" className="gaps-region"><h3>{t(lang, "gapsFirst")} <span className="muted">({idx.sensorPresent ? t(lang, "withSensor") : t(lang, "withoutSensor")})</span></h3><GapList gaps={gaps} lang={lang}/></section>}
        {idx && fw && <ControlList rows={rows} lang={lang} onPick={open} selected={control?.control ?? null}/>}
      </div>
      {control && <EvidenceTable c={control} lang={lang} title={idx && fw ? frameworkTitle(idx, fw, lang) : undefined} onPick={setHit} selected={hit}/>}
      {hit && control && <ReceiptDrilldown ctx={ctx} hit={hit} control={control} readOnly={readOnly}/>}
    </div>);
}
export function ControlList({ rows, lang, onPick, selected }: {
    rows: ControlsIndex["frameworks"][string];
    lang: Lang;
    onPick: (c: string) => void;
    selected: string | null;
}) {
    if (rows.length === 0)
        return <EmptyState text={t(lang, "nothingYet")}/>;
    return (<div className="table-wrap"><table data-testid="control-list">
      <thead><tr><th scope="col">{t(lang, "control")}</th><th scope="col"><span className="sr-only">title</span></th><th scope="col">{t(lang, "releasesCol")}</th><th scope="col">{t(lang, "refusalsCol")}</th><th scope="col">{t(lang, "sensorHoursCol")}</th><th scope="col">{t(lang, "lastEvidence")}</th></tr></thead>
      <tbody>{rows.map((r) => (<tr key={r.control} className={"clickable" + (selected === r.control ? " selected" : "")} onClick={() => onPick(r.control)} data-testid={`control-${r.control}`}>
          <td><strong><Iso>{r.control}</Iso></strong></td><td className="muted"><Iso>{r.title}</Iso></td><td>{r.releases}</td><td>{r.refusals}</td><td>{r.sensorHours}</td><td className="muted">{r.lastEvidenceAt ? formatDate(r.lastEvidenceAt, lang) : "—"}</td>
        </tr>))}</tbody>
    </table></div>);
}
export function EvidenceTable({ c, lang, onPick, selected, title }: {
    c: ControlEvidence;
    lang: Lang;
    onPick: (h: EvidenceHit) => void;
    selected: EvidenceHit | null;
    title?: string;
}) {
    return (<div className="card" data-testid="evidence-table">
      <h2>{t(lang, "evidenceFor")} <Iso>{title ?? c.framework}</Iso> · <Iso>{c.control}</Iso></h2>
      {c.provenance && <div className="muted"><strong>{t(lang, "provenance")}:</strong> <Iso>{c.provenance.title}</Iso> — “<Iso>{c.provenance.sourceText}</Iso>” <em>(<Iso>{c.provenance.sourceRef}</Iso>)</em></div>}
      {c.evidence.length === 0 && <EmptyState text={t(lang, "noEvidence")}/>}
      {c.evidence.length > 0 && <div className="table-wrap"><table>
        <thead><tr><th scope="col">{t(lang, "leaf")}</th><th scope="col">{t(lang, "colHeadline")}</th><th scope="col">{t(lang, "receiptRequester")}</th><th scope="col"><span className="sr-only">{t(lang, "drillDown")}</span></th></tr></thead>
        <tbody>{c.evidence.map((h) => (<tr key={h.leaf} className={"clickable" + (selected?.leaf === h.leaf ? " selected" : "")} onClick={() => onPick(h)} data-testid={`evidence-${h.leaf}`}>
            <td>#{h.leaf} <span className={h.outcome === "release" ? "ok" : "bad"}>{h.outcome === "release" ? t(lang, "tReleased") : t(lang, "tRefused")}</span><div className="muted small">{formatDate(h.decidedAt, lang)}</div></td>
            <td><StateChip kind={h.headline.kind} lang={lang}/></td><td className="muted">{h.header ? <Name name={h.header.requester.displayName} lang={lang}/> : "—"}</td><td>{t(lang, "drillDown")}</td>
          </tr>))}</tbody>
      </table></div>}
    </div>);
}
