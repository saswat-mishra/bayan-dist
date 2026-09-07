import type { HeadlineJson } from '../wz0g';
import { Key, Lang, pick, t } from '../gna';
const KIND: Record<HeadlineJson["kind"], {
    cls: string;
    icon: string;
    label: Key;
}> = {
    "releases-now": { cls: "hl-ok", icon: "✓", label: "kindReleasesNow" },
    "needs-review": { cls: "hl-review", icon: "◔", label: "kindNeedsReview" },
    "blocked-fixable": { cls: "hl-fix", icon: "⟳", label: "kindBlockedFixable" },
    "blocked-recipient": { cls: "hl-recipient", icon: "⇄", label: "kindBlockedRecipient" },
    "blocked-roster": { cls: "hl-roster", icon: "▤", label: "kindBlockedRoster" },
    "blocked-budget": { cls: "hl-budget", icon: "▮", label: "kindBlockedBudget" },
    "quarantined": { cls: "hl-quarantine", icon: "⊘", label: "kindQuarantined" },
};
export function Headline({ h, lang, compact }: {
    h: HeadlineJson | null | undefined;
    lang: Lang;
    compact?: boolean;
}) {
    if (!h)
        return null;
    const k = KIND[h.kind] ?? KIND["needs-review"];
    return (<div className={`headline ${k.cls}${compact ? " compact" : ""}`} data-testid="headline" data-kind={h.kind} role="status">
      <span className="hl-icon" aria-hidden="true">{k.icon}</span>
      <span className="hl-kind">{t(lang, k.label)}</span>
      <span className="hl-text">{pick(lang, h)}</span>
    </div>);
}
