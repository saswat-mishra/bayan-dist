import { Lang, t } from '../gna';
import { Iso, Name, formatDate } from '../d7t';
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
export function PersonCard({ p, lang, title, testid, compact }: {
    p: Person;
    lang: Lang;
    title?: string;
    testid?: string;
    compact?: boolean;
}) {
    if (compact) {
        return (<span className="person-line" data-testid={testid ?? "person-card"}>
        <strong><Name name={p.name} lang={lang}/></strong>
        {[(p.employer ?? p.org) && <Iso>{p.employer ?? p.org}</Iso>, p.location && <Iso>{p.location}</Iso>, p.validUntil && `${t(lang, "entryValid")} ${formatDate(p.validUntil, lang)}`].filter(Boolean).map((x, i) => <span key={i}> · {x}</span>)}
        {p.rostered === false && <span className="bad"> · {t(lang, "notRostered2")}</span>}
      </span>);
    }
    return (<div className="person" data-testid={testid ?? "person-card"}>
      {title && <div className="muted small">{title}</div>}
      <div className="person-name"><Name name={p.name} lang={lang}/>{p.principal && p.principal !== p.name && <span className="muted small"> · <Iso>{p.principal}</Iso></span>}</div>
      <div className="muted">
        {[p.role && (p.authority ? <>{t(lang, p.role as "reviewer")} · <Iso>{p.authority}</Iso></> : t(lang, p.role as "reviewer")), (p.employer ?? p.org) && <Iso>{p.employer ?? p.org}</Iso>, p.location && <Iso>{p.location}</Iso>,
            p.validUntil && `${t(lang, "entryValid")} ${formatDate(p.validUntil, lang)}`].filter(Boolean).map((x, i) => <span key={i}>{i > 0 && " · "}{x}</span>)}
      </div>
      {p.rostered === false && <div className="bad">{t(lang, "notRostered2")}</div>}
    </div>);
}
