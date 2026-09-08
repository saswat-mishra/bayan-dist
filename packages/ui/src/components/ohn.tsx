import type { Deployment, DeploymentStatus } from '../wz0g';
import { Lang, t } from '../gna';
import { Iso, Name } from '../d7t';
export function deploymentName(d: Deployment | undefined, lang: Lang): string {
    if (!d)
        return "";
    return lang === "ar" && d.name_ar ? d.name_ar : d.name;
}
export function DeploymentStatusPopover({ status, lang, showGateKeyNote, chip }: {
    status: DeploymentStatus | null;
    lang: Lang;
    showGateKeyNote: boolean;
    chip?: string;
}) {
    if (!status)
        return null;
    return (<details className="status-pop" data-testid="deployment-status">
      <summary data-testid="pack-chip" title={t(lang, "deploymentStatus")}><span className="pill">{t(lang, "packChip")} <Iso>{chip ?? status.pack.id}</Iso></span></summary>
      <div className="body">
        <div>{t(lang, "packLabel")} <Iso>{status.pack.id}@{status.pack.version}</Iso> · {status.pack.pinned ? <span className="ok">{t(lang, "pinnedYes")}</span> : <span className="bad">{t(lang, "pinnedNo")}</span>}</div>
        {status.acceptance && <div className="muted">{t(lang, "acceptedOn")} <Iso>{status.acceptance.at}</Iso> {t(lang, "acceptedBy")} <Name name={status.acceptance.acceptedBy} lang={lang}/></div>}
        {showGateKeyNote && <div className="muted" data-testid="gate-key-note">{t(lang, "gateKeyNote")}</div>}
      </div>
    </details>);
}
export function DeploymentPicker({ deps, dep, onChange, lang, status, showGateKeyNote }: {
    deps: Deployment[];
    dep: string;
    onChange: (id: string) => void;
    lang: Lang;
    status: DeploymentStatus | null;
    showGateKeyNote: boolean;
}) {
    const current = deps.find((d) => d.id === dep);
    return (<div className="picker" data-testid="deployment-picker">
      <label className="sr-only" htmlFor="deployment-select">{t(lang, "deployment")}</label>
      <select id="deployment-select" value={dep} onChange={(e) => onChange(e.target.value)} aria-label="deployment" title={current?.id}>
        {deps.map((d) => <option key={d.id} value={d.id}>{deploymentName(d, lang)}</option>)}
      </select>
      {current && (status ? <DeploymentStatusPopover status={status} lang={lang} showGateKeyNote={showGateKeyNote} chip={current.pack}/>
            : <span className="pill" data-testid="pack-chip">{t(lang, "packChip")} <Iso>{current.pack}</Iso></span>)}
    </div>);
}
