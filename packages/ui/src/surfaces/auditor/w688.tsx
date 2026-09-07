import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { ControlsIndex, Ledger, Pack } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
interface Prov {
    framework: string;
    control: string;
    title: string;
    sourceText: string;
    sourceRef: string;
    evidence: string;
    packVersion: string;
}
export function PackView({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, deps, status } = ctx;
    const packId = deps.find((d) => d.id === dep)?.pack;
    const [pack, setPack] = useState<Pack | null>(null);
    const [prov, setProv] = useState<Prov[]>([]);
    const [upgrades, setUpgrades] = useState<Ledger["entries"]>([]);
    const [error, guard] = useGuard(lang);
    useEffect(() => {
        if (packId)
            guard(api<Pack>(`/v1/packs/${packId}`, user)).then((p) => p && setPack(p));
        guard(api<ControlsIndex>(`/v1/controls/index?deployment=${dep}`, user)).then(async (i) => {
            if (!i)
                return;
            const rows: Prov[] = [];
            for (const [fw, cs] of Object.entries(i.frameworks))
                for (const c of cs)
                    rows.push({ framework: fw, control: c.control, title: c.title ?? "", sourceText: "", sourceRef: "", evidence: c.evidence ?? "", packVersion: i.pack.version });
            setProv(rows);
        });
        guard(api<Ledger>(`/v1/ledger?deployment=${dep}`, user)).then((l) => l && setUpgrades(l.entries.filter((e) => e.type === "pack-upgrade")));
    }, [dep, packId, user, guard]);
    return (<div data-testid="pack-view">
      {error && <div className="error" role="alert">{error}</div>}
      <div className="card">
        <h2>{t(lang, "pack")} {pack && <>{pack.id}@{pack.version} <code className="muted">{pack.digest.slice(0, 16)}…</code></>}</h2>
        {status && <div>{t(lang, "frameworks")}: {status.pack.activated.join(" · ")} · {t(lang, "packAccepted")} <code>{status.pack.accepted.slice(0, 16)}…</code> {status.pack.pinned ? <span className="ok">pinned</span> : <span className="bad">differs from disk</span>}</div>}
      </div>
      <div className="card" data-testid="provenance">
        <h2>{t(lang, "packProvenance")}</h2>
        <table><thead><tr><th scope="col">framework</th><th scope="col">{t(lang, "control")}</th><th scope="col">title</th><th scope="col">{t(lang, "evidenceTier")}</th><th scope="col">{t(lang, "version")}</th></tr></thead>
          <tbody>{prov.map((p) => <tr key={p.framework + p.control}><td>{p.framework}</td><td>{p.control}</td><td>{p.title}</td><td>{p.evidence}</td><td>{p.packVersion}</td></tr>)}</tbody></table>
      </div>
      {pack && <div className="card"><h2>{t(lang, "packRules")}</h2>
        <table><thead><tr><th scope="col">rule</th><th scope="col">citation</th><th scope="col">{t(lang, "sourceText")}</th><th scope="col">{t(lang, "evidenceTier")}</th></tr></thead>
          <tbody>{pack.rules.map((r) => <tr key={r.id}><td>{r.id}{r.advisory && <span className="pill">advisory</span>}</td><td>{r.citation}</td><td>“{r.quote}”</td><td>{r.evidence}</td></tr>)}</tbody></table></div>}
      <div className="card" data-testid="upgrade-history">
        <h2>{t(lang, "upgradeHistory")}</h2>
        {upgrades.length === 0 && <EmptyState text={t(lang, "noUpgrades")}/>}
        <ul>{upgrades.map((u) => <li key={u.index}>#{u.index} {u.pack} · {u.at} · {u.by}</li>)}</ul>
      </div>
    </div>);
}
