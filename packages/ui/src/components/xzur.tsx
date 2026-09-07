import type { RosterEntry } from '../wz0g';
import { Lang, t } from '../gna';
export const daysLeft = (iso: string): number => Math.floor((new Date(iso).getTime() - Date.now()) / 86400000);
export function RosterCard({ e, lang, showCitizenship, title }: {
    e: RosterEntry;
    lang: Lang;
    showCitizenship?: boolean;
    title?: string;
}) {
    const left = daysLeft(e.validUntil);
    const name = e.displayName ?? e.principal;
    return (<div className={"card roster-card" + (e.valid ? "" : " invalid")} data-testid="roster-card">
      <h2>{title ?? t(lang, "rosterMine")} {e.valid ? <span className="pill green">{t(lang, "validEntry")}</span> : <span className="pill red">{e.rolledOffAt ? t(lang, "rolledOff") : t(lang, "expiredEntry")}</span>}</h2>
      <table><tbody>
        <tr><th scope="row">{t(lang, "principal")}</th><td data-testid="roster-name">{name}{name !== e.principal && <span className="muted small"> · {e.principal}</span>}</td></tr>
        <tr><th scope="row">{t(lang, "employer")}</th><td>{e.employer}</td></tr>
        <tr><th scope="row">{t(lang, "location")}</th><td>{e.location}</td></tr>
        <tr><th scope="row">{t(lang, "validUntil")}</th><td>{e.validUntil.slice(0, 10)} <span className="muted">({left} {t(lang, "daysShort")})</span></td></tr>
        <tr><th scope="row">{t(lang, "ackSigned")}</th><td>{e.acknowledgement.signed ? e.validFrom.slice(0, 10) : "—"} <code className="muted">{e.acknowledgement.digest.slice(0, 12)}…</code></td></tr>
        <tr><th scope="row">{t(lang, "clearance")}</th><td>{e.clearanceStatus ?? "—"}</td></tr>
        {showCitizenship && <tr><th scope="row">{t(lang, "citizenships")}</th><td>{(e.citizenships ?? []).join(", ")} · {t(lang, "residency")}: {(e.residency ?? []).join(", ")}</td></tr>}
      </tbody></table>
      {e.valid && left < 14 && <div className="warn" role="alert">{t(lang, "askRenew")}</div>}
    </div>);
}
