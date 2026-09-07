import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Lang, t } from '../../gna';
import type { EvidencePack } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
import { VerifyCommand } from '../../components/uc5j';
export const currentPeriod = (): string => { const d = new Date(); return `${d.getUTCFullYear()}-Q${Math.floor(d.getUTCMonth() / 3) + 1}`; };
export function PackList({ packs, lang }: {
    packs: EvidencePack[];
    lang: Lang;
}) {
    if (packs.length === 0)
        return <EmptyState text={t(lang, "noPacks")}/>;
    return (<div>{packs.map((p) => (<div key={p.period} className="block" data-testid={`pack-${p.period}`}>
        <h3>{p.period} <span className="muted">{p.fromSize} → {p.toSize}</span></h3>
        <div>{t(lang, "downloadPath")}: <code>{p.path}</code></div>
        <div className="muted">manifest {p.manifestDigest.slice(0, 16)}…</div>
        <div data-testid="flags">{t(lang, "flags")}: {Object.entries(p.flags).filter(([k, v]) => k !== "attention" && v).map(([k]) => <span key={k} className="pill amber">{k}</span>)}</div>
        {p.flags.attention && <div className="warn" role="alert" data-testid="attention">{t(lang, "attention")}: {p.flags.attention}</div>}
        <VerifyCommand command={`bayan-verify pack ${p.path} --trust <trust dir> --assert-offline`} lang={lang}/>
      </div>))}</div>);
}
export function EvidenceBuilder({ ctx, testid }: {
    ctx: Ctx;
    testid: string;
}) {
    const { user, lang, dep } = ctx;
    const [packs, setPacks] = useState<EvidencePack[]>([]);
    const [period, setPeriod] = useState(currentPeriod());
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<EvidencePack[]>(`/v1/evidence-packs?deployment=${dep}`, user)).then((r) => r && setPacks(r)), [dep, user, guard]);
    useEffect(() => { load(); }, [load]);
    async function build() { if (await guard(api("/v1/evidence-packs", user, { method: "POST", body: { deployment: dep, period } })))
        load(); }
    return (<div className="card" data-testid={testid}>
      <h2>{t(lang, "evidencePacks")}</h2>
      {error && <div className="error" role="alert">{error}</div>}
      <div className="vote"><label>{t(lang, "period")} <input value={period} onChange={(e) => setPeriod(e.target.value)} data-testid="period" style={{ width: "10rem" }}/></label>
        <button className="primary" onClick={build} data-testid="build-pack">{t(lang, "buildPack")}</button></div>
      <PackList packs={packs} lang={lang}/>
    </div>);
}
export function LeadEvidence({ ctx }: {
    ctx: Ctx;
}) { return <EvidenceBuilder ctx={ctx} testid="lead-evidence"/>; }
