import { Key, Lang, t } from '../gna';
import type { Role } from '../wz0g';
export interface NavItem {
    page: string;
    label: Key;
}
export const NAV: Record<Role, NavItem[]> = {
    engineer: [{ page: "ask", label: "ask" }, { page: "requests", label: "myRequests" }, { page: "integrations", label: "navIntegrations" }, { page: "roster", label: "roster" }],
    reviewer: [{ page: "queue", label: "inbox" }, { page: "authority", label: "authority" }],
    lead: [{ page: "home", label: "dashboard" }, { page: "roster", label: "rosterWrite" }, { page: "evidence", label: "evidence" }],
    auditor: [{ page: "coverage", label: "coverage" }, { page: "packs", label: "evidencePacks" }, { page: "records", label: "recordsGroup" }],
    dba: [{ page: "decisions", label: "navDecisions" }, { page: "fields", label: "navFields" }],
};
export function RoleNav({ role, page, lang, hasAuthority, external }: {
    role: Role;
    page: string;
    lang: Lang;
    hasAuthority: boolean;
    external?: boolean;
}) {
    const items = NAV[role].filter((i) => i.page !== "authority" || hasAuthority);
    return (<nav aria-label="nav" className="rolenav">
      <div className="rolenav-inner">
        {external && <div className="pill" data-testid="read-only-pill">{t(lang, "externalReadOnly")}</div>}
        <ul>{items.map((i) => <li key={i.page}><a href={`#/${i.page}`} aria-current={page === i.page ? "page" : undefined} data-testid={`nav-${i.page}`}>{t(lang, i.label)}</a></li>)}</ul>
      </div>
    </nav>);
}
