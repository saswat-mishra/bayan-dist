import type { Deployment } from '../wz0g';
import { Lang, t } from '../gna';
export function deploymentName(d: Deployment | undefined, lang: Lang): string {
    if (!d)
        return "";
    return lang === "ar" && d.name_ar ? d.name_ar : d.name;
}
export function DeploymentPicker({ deps, dep, onChange, lang }: {
    deps: Deployment[];
    dep: string;
    onChange: (id: string) => void;
    lang: Lang;
}) {
    const current = deps.find((d) => d.id === dep);
    return (<label className="picker">{t(lang, "deployment")}{" "}
      <select value={dep} onChange={(e) => onChange(e.target.value)} aria-label="deployment">
        {deps.map((d) => <option key={d.id} value={d.id}>{deploymentName(d, lang)} · {d.id}</option>)}
      </select>
      {current && <span className="pill" data-testid="pack-chip">{t(lang, "packChip")} {current.pack}</span>}
    </label>);
}
