import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { Ledger, SensorHour } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
export function SensorView({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, status } = ctx;
    const [hours, setHours] = useState<SensorHour[] | null>(null);
    const [susp, setSusp] = useState<Ledger["entries"]>([]);
    const [error, guard] = useGuard(lang);
    useEffect(() => {
        guard(api<SensorHour[]>(`/v1/sensor/hours?deployment=${dep}`, user)).then((h) => h && setHours(h));
        guard(api<Ledger>(`/v1/ledger?deployment=${dep}`, user)).then((l) => l && setSusp(l.entries.filter((e) => e.type === "suspension" || e.type === "suspension-cleared")));
    }, [dep, user, guard]);
    return (<div data-testid="sensor">
      <div className="card">
        <h2>{t(lang, "sensor")} {status?.suspended ? <span className="pill red">{t(lang, "suspendedBanner")}</span> : <span className="pill green">ok</span>}</h2>
        {error && <div className="error" role="alert">{error}</div>}
        {hours && hours.length === 0 && <EmptyState text={t(lang, "sensorEmpty")}/>}
        {hours && hours.length > 0 && <table><thead><tr><th scope="col">hour</th><th scope="col">events</th><th scope="col">{t(lang, "byClass")}</th><th scope="col">root</th><th scope="col">{t(lang, "sealedHour")}</th></tr></thead>
          <tbody>{hours.map((h) => <tr key={h.hour}><td>{h.hour}</td><td>{h.events}</td><td>{Object.entries(h.byClass).map(([k, v]) => `${k} ${v}`).join(" · ")}</td><td><code>{h.root.slice(0, 12)}…</code></td><td>{h.sealed ? `#${h.leafIndex}` : "—"}</td></tr>)}</tbody></table>}
      </div>
      <div className="card" data-testid="suspension-history">
        <h2>{t(lang, "suspensionHistory")}</h2>
        {susp.length === 0 && <EmptyState text={t(lang, "nothingYet")}/>}
        <ul>{susp.map((e) => <li key={e.index}>#{e.index} <strong>{e.type}</strong> {e.at} · {e.reason} {e.by && <span className="muted">— {e.by}</span>}</li>)}</ul>
      </div>
    </div>);
}
