import { Key, Lang, t } from '../gna';
import type { Role } from '../wz0g';
export interface NavItem {
    page: string;
    label: Key;
    group?: Key;
}
export const NAV: Record<Role, NavItem[]> = {
    engineer: [{ page: "ask", label: "ask" }, { page: "requests", label: "myRequests" }, { page: "roster", label: "roster" }],
    reviewer: [{ page: "queue", label: "inbox" }, { page: "authority", label: "authority" }],
    lead: [{ page: "home", label: "dashboard" }, { page: "roster", label: "rosterWrite" }, { page: "evidence", label: "evidence" }],
    auditor: [{ page: "coverage", label: "coverage" }, { page: "controls", label: "controlsExplorer" }, { page: "packs", label: "evidencePacks" },
        { page: "register", label: "navRegister", group: "recordsGroup" }, { page: "ledger", label: "navLedger", group: "recordsGroup" }, { page: "sensor", label: "sensor", group: "recordsGroup" },
        { page: "roster", label: "roster", group: "recordsGroup" }, { page: "pack", label: "pack", group: "recordsGroup" }],
    dba: [{ page: "fields", label: "fieldClasses" }],
};
export function RoleNav({ role, page, lang, hasAuthority, external }: {
    role: Role;
    page: string;
    lang: Lang;
    hasAuthority: boolean;
    external?: boolean;
}) {
    const items = NAV[role].filter((i) => i.page !== "authority" || hasAuthority);
    const groups = Array.from(new Set(items.map((i) => i.group ?? "")));
    return (<nav aria-label="nav" className="rolenav">
      <div className="rolenav-inner">
        {external && <div className="pill" data-testid="read-only-pill">{t(lang, "externalReadOnly")}</div>}
        {groups.map((g) => (<div key={g || "main"}>
            {g && <div className="nav-group">{t(lang, g as Key)}</div>}
            <ul>{items.filter((i) => (i.group ?? "") === g).map((i) => <li key={i.page}><a href={`#/${i.page}`} aria-current={page === i.page ? "page" : undefined} data-testid={`nav-${i.page}`}>{t(lang, i.label)}</a></li>)}</ul>
          </div>))}
      </div>
    </nav>);
}
