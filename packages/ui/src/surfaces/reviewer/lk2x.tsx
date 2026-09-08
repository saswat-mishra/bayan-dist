import { useCallback, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { ago, go, useGuard, useLive } from '../../q1n';
import { Key, Lang, t } from '../../gna';
import type { Principal, QueueItem } from '../../wz0g';
import { browserSigner } from '../../ck2';
import { EmptyState } from '../../components/qg9b';
import { StateChip } from '../../components/drm';
import { LiveStatus } from '../../components/poy';
import { OnboardingChecklist } from '../../components/z3w4';
import { Bi, Iso, Name } from '../../d7t';
import { Brief } from './u3r';
export const GROUPS: [
    string,
    Key
][] = [["red", "groupRed"], ["amber", "groupAmber"], ["black", "groupBlack"], ["green", "groupGreen"]];
export const QUEUE_POLL_MS = 10000;
export function InboxRow({ q, lang, selected, onOpen }: {
    q: QueueItem;
    lang: Lang;
    selected: boolean;
    onOpen: () => void;
}) {
    const purpose = (q.purpose ?? "").length > 90 ? (q.purpose ?? "").slice(0, 88) + "…" : q.purpose ?? "";
    return (<li className={"inbox-row clickable" + (selected ? " selected" : "")} data-testid={`queue-${q.id}`} aria-current={selected ? "true" : undefined}>
      <button type="button" className="row-button" onClick={onOpen} aria-label={q.headline ? (lang === "ar" ? q.headline.ar : q.headline.en) : q.id}>
        {q.headline && <StateChip kind={q.headline.kind} lang={lang} testid={`chip-${q.id}`}/>}
        <div className="inbox-line">
          <span>{t(lang, "requestedBy")} <strong><Name name={q.requesterName ?? q.requester} lang={lang}/></strong></span> · <span>{t(lang, "fromDeployment")} <Bi x={{ en: q.deploymentName ?? q.deployment, ar: q.deploymentName_ar }} lang={lang}/></span>
          {q.lookup && <> · <span>{t(lang, "lookupTitle")}</span></>}
        </div>
        {purpose && <div className="muted inbox-purpose" dir="auto">“<Iso>{purpose}</Iso>”</div>}
        <div className="muted small">{ago(q.ageSeconds ?? 0, lang)} · {t(lang, "votesIn").replace("{n}", String(q.votes)).replace("{m}", String(q.requiredReviews))}
          {q.yours && <> · <span className="bad">{t(lang, "yoursCannot")}</span></>}{q.youVoted && <> · {t(lang, "youVoted")}</>}</div>
      </button>
    </li>);
}
export function Queue({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, me, sub, deps, pack } = ctx;
    const [queue, setQueue] = useState<QueueItem[] | null>(null);
    const [filter, setFilter] = useState("all");
    const [approvers, setApprovers] = useState<string[]>([]);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<QueueItem[]>("/v1/review/queue", user)).then((q) => q && setQueue(q)), [user, guard]);
    const { updatedAt, refresh } = useLive(load, QUEUE_POLL_MS);
    const loadApprovers = useCallback(() => api<Principal[]>("/v1/principals", user).then((ps) => setApprovers(ps.filter((p) => p.authority && p.id !== user).map((p) => p.displayName))).catch(() => setApprovers([])), [user]);
    useLive(loadApprovers, 60000, false);
    const custody = ctx.custody;
    const needsOnboarding = me.role === "reviewer" && (custody.state.kind === "unenrolled" || custody.state.kind === "pending");
    const selected = sub[0] ?? null;
    const items = (queue ?? []).filter((q) => filter === "all" || q.deployment === filter);
    const groups = GROUPS.map(([r, k]) => [r, k, items.filter((q) => q.riskClass === r)] as const).filter(([, , xs]) => xs.length);
    const deployments = Array.from(new Set((queue ?? []).map((q) => q.deployment)));
    const depName = (id: string) => { const d = deps.find((x) => x.id === id); return d ? (lang === "ar" && d.name_ar ? d.name_ar : d.name) : id; };
    return (<div className={selected ? "grid brief-open" : "reading"} data-testid="queue">
      <div>
        {needsOnboarding && <OnboardingChecklist state={custody.state} approvers={approvers} lang={lang} onEnrol={custody.enrol}/>}
        <div className="card" data-testid="inbox">
          <h2>{t(lang, "inbox")}</h2>
          <p className="muted">{t(lang, "inboxIntro")} <LiveStatus updatedAt={updatedAt} lang={lang} onRefresh={refresh}/></p>
          {error && <div className="error" role="alert">{error}</div>}
          {deployments.length > 1 && <label>{t(lang, "filterDeployment")}{" "}
            <select value={filter} onChange={(e) => setFilter(e.target.value)} aria-label="deployment-filter"><option value="all">{t(lang, "all")}</option>{deployments.map((d) => <option key={d} value={d}>{depName(d)}</option>)}</select></label>}
          {groups.map(([risk, key, xs]) => (<section key={risk} className={`inbox-group group-${risk}`} data-testid={`group-${risk}`} aria-label={t(lang, key)}>
              <h3>{t(lang, key)} <span className="muted">({xs.length})</span></h3>
              <ul className="inbox-list">{xs.map((q) => <InboxRow key={q.id} q={q} lang={lang} selected={selected === q.id} onOpen={() => go(`queue/${q.id}`)}/>)}</ul>
            </section>))}
          {queue && queue.length === 0 && <EmptyState text={t(lang, "queueEmpty")} testid="queue-empty"/>}
        </div>
      </div>
      <div>{selected && <Brief id={selected} user={user} lang={lang} onChange={refresh} signer={browserSigner(user, me.custody === "client" ? me.keyName ?? null : null)} threshold={Number(pack?.review?.threshold ?? 2)}/>}</div>
    </div>);
}
