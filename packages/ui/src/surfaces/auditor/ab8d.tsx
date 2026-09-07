import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { RosterEntry } from '../../wz0g';
import { RosterCard } from '../../components/xzur';
import { EmptyState } from '../../components/qg9b';
export function AuditorRoster({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, me } = ctx;
    const [rows, setRows] = useState<RosterEntry[] | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => { guard(api<RosterEntry[]>(`/v1/roster?deployment=${dep}`, user)).then((r) => r && setRows(r)); }, [dep, user, guard]);
    return (<div data-testid="auditor-roster">
      <h2>{t(lang, "rosterHistory")}</h2>
      {error && <div className="error" role="alert">{error}</div>}
      {rows && rows.length === 0 && <EmptyState text={t(lang, "nothingYet")}/>}
      <div className="cards">{(rows ?? []).map((e) => <div key={e.principal + e.validFrom}><RosterCard e={e} lang={lang} showCitizenship={me.role === "auditor"} title={e.displayName ?? e.principal}/><div className="muted">digest <code>{e.entryDigest.slice(0, 16)}…</code>{e.destructionAttestation ? ` · ${t(lang, "attestation")}` : ""}</div></div>)}</div>
    </div>);
}
