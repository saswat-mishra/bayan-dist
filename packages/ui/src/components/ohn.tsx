import type { Deployment } from '../wz0g';
import { Lang, t } from '../gna';
export function DeploymentPicker({ deps, dep, onChange, lang }: {
    deps: Deployment[];
    dep: string;
    onChange: (id: string) => void;
    lang: Lang;
}) {
    return (<label className="picker">{t(lang, "deployment")}{" "}
      <select value={dep} onChange={(e) => onChange(e.target.value)} aria-label="deployment">
        {deps.map((d) => <option key={d.id} value={d.id}>{d.id} — {d.name} [{d.pack}]</option>)}
      </select>
    </label>);
}
