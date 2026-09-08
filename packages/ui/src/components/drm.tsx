import type { HeadlineJson } from '../wz0g';
import { Key, Lang, t } from '../gna';
export type ChipKind = HeadlineJson["kind"] | "done" | "pending" | "todo" | "enrolled" | "key-pending" | "unenrolled" | "gate" | "unsupported" | "released" | "refused" | "info";
type Tone = "ok" | "warn" | "bad" | "accent" | "none";
const KIND: Record<ChipKind, {
    tone: Tone;
    label: Key;
}> = {
    "releases-now": { tone: "ok", label: "kindReleasesNow" },
    "needs-review": { tone: "warn", label: "kindNeedsReview" },
    "blocked-fixable": { tone: "accent", label: "kindBlockedFixable" },
    "blocked-recipient": { tone: "bad", label: "kindBlockedRecipient" },
    "blocked-roster": { tone: "bad", label: "kindBlockedRoster" },
    "blocked-budget": { tone: "bad", label: "kindBlockedBudget" },
    quarantined: { tone: "bad", label: "kindQuarantined" },
    done: { tone: "ok", label: "stateDone" },
    pending: { tone: "warn", label: "statePending" },
    todo: { tone: "none", label: "stateTodo" },
    enrolled: { tone: "ok", label: "custodyEnrolled" },
    "key-pending": { tone: "warn", label: "custodyPending" },
    unenrolled: { tone: "warn", label: "custodyUnenrolled" },
    gate: { tone: "none", label: "custodyGate" },
    unsupported: { tone: "bad", label: "custodyUnsupported" },
    released: { tone: "ok", label: "tReleased" },
    refused: { tone: "bad", label: "tRefused" },
    info: { tone: "none", label: "groupGreen" },
};
export function StateChip({ kind, lang, label, testid, title }: {
    kind: ChipKind;
    lang: Lang;
    label?: string;
    testid?: string;
    title?: string;
}) {
    const k = KIND[kind] ?? KIND.info;
    return (<span className="state-chip" data-kind={kind} data-tone={k.tone} data-testid={testid ?? "state-chip"} title={title}>
      <span className="dot" aria-hidden="true"/>
      <span>{label ?? t(lang, k.label)}</span>
    </span>);
}
