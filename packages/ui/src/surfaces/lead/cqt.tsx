import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { RosterEntry } from '../../wz0g';
import { RosterCard } from '../../components/xzur';
import { EmptyState } from '../../components/qg9b';
const iso = (d: Date) => d.toISOString().replace(/\.\d{3}Z$/, "Z");
export function LeadRoster({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [rows, setRows] = useState<RosterEntry[]>([]);
    const [form, setForm] = useState({ principal: "", employer: "vendor.example", citizenships: "AE", residency: "AE", location: "AE-DU" });
    const [saved, setSaved] = useState<string | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<RosterEntry[]>(`/v1/roster?deployment=${dep}`, user)).then((r) => r && setRows(r)), [dep, user, guard]);
    useEffect(() => { load(); }, [load]);
    const fill = (e: RosterEntry) => setForm({ principal: e.principal, employer: e.employer, citizenships: (e.citizenships ?? []).join(","), residency: (e.residency ?? []).join(","), location: e.location });
    async function save() {
        const now = new Date();
        const body = { deployment: dep, principal: form.principal, employer: form.employer, citizenships: form.citizenships.split(",").map((s) => s.trim()).filter(Boolean),
            residency: form.residency.split(",").map((s) => s.trim()).filter(Boolean), location: form.location, validFrom: iso(now), validUntil: iso(new Date(now.getTime() + 365 * 86400000)),
            clearanceStatus: "verified", clearanceCheckedAt: iso(now) };
        const r = await guard(api<RosterEntry>("/v1/roster", user, { method: "POST", body }));
        if (r) {
            setSaved(`${t(lang, "renewed")} · ${r.entryDigest.slice(0, 12)}…`);
            load();
        }
    }
    async function rollOff(principal: string) {
        const r = await guard(api<{
            leafIndex: number;
        }>(`/v1/roster/${principal}/roll-off`, user, { method: "POST", body: { deployment: dep } }));
        if (r) {
            setSaved(`${t(lang, "rolledOff")} — ${t(lang, "attestation")} #${r.leafIndex}`);
            load();
        }
    }
    return (<div data-testid="lead-roster">
      {error && <div className="error" role="alert">{error}</div>}
      {saved && <div className="ok" role="status" data-testid="roster-saved">{saved}</div>}
      <div className="card">
        <h2>{t(lang, "addEntry")}</h2>
        <div className="grid">
          <label>{t(lang, "principal")}<input value={form.principal} onChange={(e) => setForm({ ...form, principal: e.target.value })} data-testid="roster-principal"/></label>
          <label>{t(lang, "employer")}<input value={form.employer} onChange={(e) => setForm({ ...form, employer: e.target.value })}/></label>
          <label>{t(lang, "citizenships")}<input value={form.citizenships} onChange={(e) => setForm({ ...form, citizenships: e.target.value })}/></label>
          <label>{t(lang, "residency")}<input value={form.residency} onChange={(e) => setForm({ ...form, residency: e.target.value })}/></label>
          <label>{t(lang, "location")}<input value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} data-testid="roster-location"/></label>
        </div>
        <button className="primary" onClick={save} disabled={!form.principal} data-testid="roster-save">{t(lang, "save")}</button>
      </div>
      {rows.length === 0 && <EmptyState text={t(lang, "nothingYet")}/>}
      <div className="cards">{rows.map((e) => (<div key={e.principal}>
          <RosterCard e={e} lang={lang} showCitizenship title={e.displayName ?? e.principal}/>
          <div className="vote"><button onClick={() => fill(e)} data-testid={`renew-${e.principal}`}>{t(lang, "addEntry")}</button>{!e.rolledOffAt && <button className="danger" onClick={() => rollOff(e.principal)} data-testid={`rolloff-${e.principal}`}>{t(lang, "rollOff")}</button>}</div>
        </div>))}</div>
    </div>);
}
