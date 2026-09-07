import { Key, Lang, t } from '../gna';
import type { Role } from '../wz0g';
export interface NavItem {
    page: string;
    label: Key;
}
export const NAV: Record<Role, NavItem[]> = {
    engineer: [{ page: "ask", label: "ask" }, { page: "requests", label: "myRequests" }, { page: "roster", label: "roster" }],
    reviewer: [{ page: "queue", label: "queue" }, { page: "authority", label: "authority" }],
    lead: [{ page: "home", label: "home" }, { page: "roster", label: "rosterWrite" }, { page: "evidence", label: "evidence" }],
    auditor: [{ page: "controls", label: "controlsExplorer" }, { page: "packs", label: "evidencePacks" }, { page: "register", label: "navRegister" }, { page: "ledger", label: "navLedger" }, { page: "sensor", label: "sensor" }, { page: "roster", label: "roster" }, { page: "pack", label: "pack" }],
    assessor: [{ page: "controls", label: "controlsExplorer" }, { page: "packs", label: "evidencePacks" }, { page: "register", label: "navRegister" }, { page: "ledger", label: "navLedger" }, { page: "sensor", label: "sensor" }, { page: "roster", label: "roster" }, { page: "pack", label: "pack" }],
    dba: [{ page: "fields", label: "fieldClasses" }],
    sensor: [],
};
export function RoleNav({ role, page, lang, hasAuthority }: {
    role: Role;
    page: string;
    lang: Lang;
    hasAuthority: boolean;
}) {
    const items = NAV[role].filter((i) => i.page !== "authority" || hasAuthority);
    return (<nav aria-label="nav" className="rolenav">
      <ul>{items.map((i) => <li key={i.page}><a href={`#/${i.page}`} aria-current={page === i.page ? "page" : undefined} data-testid={`nav-${i.page}`}>{t(lang, i.label)}</a></li>)}</ul>
    </nav>);
}
