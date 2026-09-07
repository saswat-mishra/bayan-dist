import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import { b64, browserKeyPair, canonicalJson, nowIso } from '../../ck2';
import type { Acceptance, Enrolment, RosterEntry } from '../../wz0g';
import { EmptyState } from '../../components/qg9b';
import { daysLeft } from '../../components/xzur';
export function Authority({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, me, status, refreshStatus } = ctx;
    const [enrolments, setEnrolments] = useState<Enrolment[]>([]);
    const [roster, setRoster] = useState<RosterEntry[]>([]);
    const [acc, setAcc] = useState<Acceptance | null>(null);
    const [reason, setReason] = useState("");
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => {
        guard(api<Enrolment[]>("/v1/keys/enrolments", user)).then((r) => r && setEnrolments(r.filter((e) => e.status === "pending")));
        guard(api<RosterEntry[]>(`/v1/roster?deployment=${dep}`, user)).then((r) => r && setRoster(r.filter((e) => !e.valid || daysLeft(e.validUntil) < 14)));
        guard(api<Acceptance>(`/v1/acceptance?deployment=${dep}`, user)).then((a) => a && setAcc(a));
        refreshStatus();
    }, [user, dep, guard, refreshStatus]);
    useEffect(() => { load(); }, [load]);
    async function approve(principal: string) { if (await guard(api(`/v1/keys/enrol/${principal}/approve`, user, { method: "POST" })))
        load(); }
    async function upgrade() { if (await guard(api(`/v1/deployments/${dep}/pack-upgrade`, user, { method: "POST", body: { reason } }))) {
        setReason("");
        load();
    } }
    async function accept() {
        if (!acc || me.custody !== "client" || !me.keyName)
            return;
        const at = nowIso();
        const payload = new TextEncoder().encode(canonicalJson({ schema: "bayan.acceptance.v1", deployment: dep, digest: acc.current.digest, principal: user, at }));
        const pair = await browserKeyPair(user);
        const signature = b64(await crypto.subtle.sign({ name: "Ed25519" }, pair.privateKey, payload));
        if (await guard(api("/v1/acceptance", user, { method: "POST", body: { deployment: dep, signature, publicKeyId: me.keyName, at } })))
            load();
    }
    const packChanged = status && status.pack.accepted !== status.pack.digest && !status.pack.pinned;
    const accepted = acc?.accepted as {
        digest: string;
        acceptedBy: {
            principal: string;
            at: string;
        };
    } | null | undefined;
    return (<div data-testid="authority">
      {error && <div className="error" role="alert">{error}</div>}
      <div className="card" data-testid="enrolments">
        <h2>{t(lang, "pendingEnrolments")}</h2>
        {enrolments.length === 0 && <EmptyState text={t(lang, "noEnrolments")}/>}
        <ul>{enrolments.map((e) => <li key={e.keyName}>{e.principal} · <code>{e.keyName}</code> · {e.requestedAt} {e.principal !== user && <button onClick={() => approve(e.principal)} data-testid={`approve-${e.principal}`}>{t(lang, "approveKey")}</button>}</li>)}</ul>
      </div>
      <div className="card" data-testid="pack-upgrade">
        <h2>{t(lang, "packUpgrade")}</h2>
        {status && <div>{t(lang, "packOnDisk")}: <code>{status.pack.digest.slice(0, 16)}…</code> ({status.pack.id}@{status.pack.version}) · {t(lang, "packAccepted")}: <code>{status.pack.accepted.slice(0, 16)}…</code></div>}
        {packChanged ? (<div className="vote">
            <label className="grow">{t(lang, "upgradeReason")}<textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} data-testid="upgrade-reason"/></label>
            <button className="primary" disabled={reason.trim().length < 20} onClick={upgrade} data-testid="approve-upgrade">{t(lang, "approveUpgrade")}</button>
          </div>) : <div className="ok">{t(lang, "packPinned")}</div>}
      </div>
      <div className="card" data-testid="roster-expiring">
        <h2>{t(lang, "rosterExpiring")}</h2>
        {roster.length === 0 && <EmptyState text={t(lang, "nothingYet")}/>}
        <ul>{roster.map((e) => <li key={e.principal}>{e.displayName ?? e.principal} · {e.location} · {t(lang, "validUntil")} {e.validUntil.slice(0, 10)} · <span className={e.valid ? "warn" : "bad"}>{e.locality ?? (e.valid ? "expiring" : "invalid")}</span></li>)}</ul>
      </div>
      <div className="card" data-testid="acceptance">
        <h2>{t(lang, "acceptDeployment")}</h2>
        {accepted && <div>{t(lang, "acceptedOn")} {accepted.acceptedBy.at} {t(lang, "acceptedBy")} {accepted.acceptedBy.principal} · <code>{accepted.digest.slice(0, 16)}…</code></div>}
        {acc && <div><strong>{t(lang, "acceptDelta")}:</strong> {acc.delta && acc.delta.length > 0 ? acc.delta.join(", ") : <span className="muted">{t(lang, "noDelta")}</span>}</div>}
        <button className="primary" onClick={accept} disabled={me.custody !== "client"} data-testid="accept-deployment">{t(lang, "signAcceptance")}</button>
        {me.custody !== "client" && <div className="muted">{t(lang, "keyUnenrolled")}</div>}
      </div>
    </div>);
}
