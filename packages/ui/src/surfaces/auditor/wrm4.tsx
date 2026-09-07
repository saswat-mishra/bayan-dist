import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { Ledger } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
export function LedgerView({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [led, setLed] = useState<Ledger | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => { guard(api<Ledger>(`/v1/ledger?deployment=${dep}`, user)).then((l) => l && setLed(l)); }, [dep, user, guard]);
    const types = led ? led.entries.reduce<Record<string, number>>((acc, e) => ({ ...acc, [e.type]: (acc[e.type] ?? 0) + 1 }), {}) : {};
    return (<div className="card" data-testid="ledger">
      <h2>{t(lang, "ledger")} — {led?.origin}</h2>
      {error && <div className="error" role="alert">{error}</div>}
      {led && <>
        <div>size {led.size} · {t(lang, "integrity")} {led.integrity.length === 0 ? <span className="ok">ok</span> : <span className="bad">{led.integrity.join("; ")}</span>} · {t(lang, "leafTypes")}: {Object.entries(types).map(([k, v]) => `${k} ${v}`).join(" · ")}</div>
        <details><summary>{t(lang, "checkpoint")}</summary><pre>{led.checkpoint ?? "(no checkpoint yet)"}</pre></details>
        {led.entries.length === 0 && <EmptyState text={t(lang, "noLedger")}/>}
        <table><thead><tr><th scope="col">#</th><th scope="col">type</th><th scope="col">detail</th><th scope="col">leaf hash</th></tr></thead>
          <tbody>{led.entries.map((e) => <tr key={e.index} data-testid={`leaf-${e.index}`}><td>{e.index}</td><td>{e.type}</td>
            <td>{e.type === "clearance" ? <span className={e.outcome === "release" ? "ok" : "bad"}>{e.outcome} · {e.rrsaClass} · {(e.humanReviews ?? []).map((h) => h.split("@")[0]).join(", ") || "gate"}</span> : <span className="muted">{e.principal ?? e.pack ?? e.hour ?? e.reason ?? ""} {e.keyName ?? ""} {e.by ?? ""}</span>}</td>
            <td><code>{e.leafHash.slice(0, 16)}…</code></td></tr>)}</tbody></table>
      </>}
    </div>);
}
