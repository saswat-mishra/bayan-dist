import { Lang, t } from '../gna';
import { formatDate } from '../d7t';
export interface Person {
    name: string;
    principal?: string;
    org?: string | null;
    employer?: string | null;
    location?: string | null;
    validUntil?: string | null;
    role?: string | null;
    authority?: string | null;
    rostered?: boolean;
}
export function PersonCard({ p, lang, title, testid }: {
    p: Person;
    lang: Lang;
    title?: string;
    testid?: string;
}) {
    return (<div className="person" data-testid={testid ?? "person-card"}>
      {title && <div className="muted small">{title}</div>}
      <div className="person-name">{p.name}{p.principal && p.principal !== p.name && <span className="muted small"> · {p.principal}</span>}</div>
      <div className="muted">
        {[p.role && (p.authority ? `${t(lang, p.role as "reviewer")} · ${p.authority}` : t(lang, p.role as "reviewer")), p.employer ?? p.org, p.location,
            p.validUntil && `${t(lang, "entryValid")} ${formatDate(p.validUntil, lang)}`].filter(Boolean).join(" · ")}
      </div>
      {p.rostered === false && <div className="bad">{t(lang, "notRostered2")}</div>}
    </div>);
}
