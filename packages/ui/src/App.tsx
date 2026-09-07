import { useCallback, useEffect, useState } from "react";
import { api } from './vhq7';
import type { Deployment, DeploymentStatus, Pack, Principal } from './wz0g';
import { Key, Lang, t } from './gna';
import { useHash, usePersisted } from './q1n';
import { explain } from './x27r';
import { TermsProvider } from './d7t';
import { KeyCustody } from './components/dic';
import { DeploymentPicker } from './components/ohn';
import { RoleNav, NAV } from './components/rzed';
import { SuspensionBanner } from './components/y4bx';
import { EngineerPages } from './surfaces/engineer/index';
import { ReviewerPages } from './surfaces/reviewer/index';
import { LeadPages } from './surfaces/lead/index';
import { AuditorPages } from './surfaces/auditor/index';
import { DbaPages } from './surfaces/dba/index';
const DEFAULT_USER = "omar.h@vendor.example";
const CLIENT_ROLES = new Set(["reviewer", "auditor", "dba"]);
export interface Ctx {
    user: string;
    lang: Lang;
    dep: string;
    deps: Deployment[];
    me: Principal;
    status: DeploymentStatus | null;
    pack: Pack | null;
    refreshStatus: () => void;
    page: string;
    sub: string[];
}
export function DeploymentStatusPopover({ status, lang, showGateKeyNote }: {
    status: DeploymentStatus | null;
    lang: Lang;
    showGateKeyNote: boolean;
}) {
    if (!status)
        return null;
    return (<details className="status-pop" data-testid="deployment-status">
      <summary>{t(lang, "deploymentStatus")}</summary>
      <div className="body">
        <div>{t(lang, "packLabel")} {status.pack.id}@{status.pack.version} · {status.pack.pinned ? <span className="ok">{t(lang, "pinnedYes")}</span> : <span className="bad">{t(lang, "pinnedNo")}</span>}</div>
        {status.acceptance && <div className="muted">{t(lang, "acceptedOn")} {status.acceptance.at} {t(lang, "acceptedBy")} {status.acceptance.acceptedBy}</div>}
        {showGateKeyNote && <div className="muted" data-testid="gate-key-note">{t(lang, "gateKeyNote")}</div>}
      </div>
    </details>);
}
export function HomeLine({ me, lang }: {
    me: Principal;
    lang: Lang;
}) {
    const key: Key = me.role === "engineer" ? "homeEngineer" : me.role === "reviewer" ? (me.authority ? "homeReviewer" : "homeReviewerNoAuthority")
        : me.role === "lead" ? "homeLead" : me.role === "auditor" ? (me.external ? "homeExternal" : "homeAuditor") : "homeDba";
    return <p className="home-line" data-testid="home-line">{t(lang, key)}</p>;
}
export function App() {
    const [user, setUser] = usePersisted("bayan.user", DEFAULT_USER);
    const [langS, setLangS] = usePersisted("bayan.lang", "en");
    const lang = (langS === "ar" ? "ar" : "en") as Lang;
    const [dep, setDep] = usePersisted("bayan.dep", "");
    const [principals, setPrincipals] = useState<Principal[]>([]);
    const [deps, setDeps] = useState<Deployment[]>([]);
    const [me, setMe] = useState<Principal | null>(null);
    const [status, setStatus] = useState<DeploymentStatus | null>(null);
    const [pack, setPack] = useState<Pack | null>(null);
    const [error, setError] = useState<string | null>(null);
    const segs = useHash();
    useEffect(() => { document.documentElement.dir = lang === "ar" ? "rtl" : "ltr"; document.documentElement.lang = lang; }, [lang]);
    const loadMe = useCallback(() => api<Principal>("/v1/me", user).then((p) => { setMe(p); setError(null); }).catch((e) => setError(explain(e, lang))), [user, lang]);
    useEffect(() => {
        api<Principal[]>("/v1/principals", user).then(setPrincipals).catch((e) => setError(explain(e, lang)));
        api<Deployment[]>("/v1/deployments", user).then((d) => { setDeps(d); setDep((cur) => cur && d.some((x) => x.id === cur) ? cur : (d.find((x) => x.id === "moi-itsm-prod-01") ?? d[0])?.id ?? ""); }).catch((e) => setError(explain(e, lang)));
        loadMe();
    }, [user, lang, loadMe, setDep]);
    const refreshStatus = useCallback(() => { if (dep)
        api<DeploymentStatus>(`/v1/deployments/${dep}/status`, user).then(setStatus).catch(() => setStatus(null)); }, [dep, user]);
    useEffect(() => { refreshStatus(); }, [refreshStatus]);
    const packId = deps.find((d) => d.id === dep)?.pack;
    useEffect(() => { if (packId)
        api<Pack>(`/v1/packs/${packId}`, user).then(setPack).catch(() => setPack(null));
    else
        setPack(null); }, [packId, user]);
    const role = me?.role;
    const nav = role ? NAV[role] : [];
    const page = segs[0] && nav.some((n) => n.page === segs[0]) ? segs[0] : (nav[0]?.page ?? "");
    const hasAuthority = !!me?.authority;
    const showsCustody = !!me && (me.role === "reviewer" || hasAuthority);
    const ctx: Ctx | null = me && dep ? { user, lang, dep, deps, me, status, pack, refreshStatus, page, sub: segs.slice(1) } : null;
    const printing = page === "home" && segs[1] === "print";
    return (<TermsProvider terms={pack?.terms ?? null} lang={lang}>
      <header className={printing ? "no-print" : undefined}>
        <h1>{t(lang, "title")}</h1>
        <label>{t(lang, "user")}{" "}
          <select value={user} onChange={(e) => { setUser(e.target.value); location.hash = ""; }} aria-label="acting-as">
            {(principals.length ? principals : [{ id: user, displayName: user, role: "engineer", lang: "en", keyType: "software" } as Principal]).map((p) => (<option key={p.id} value={p.id}>{p.displayName} — {t(lang, p.role)}{p.external ? ` (${t(lang, "external")})` : ""}</option>))}
          </select>
        </label>
        <label>{t(lang, "lang")}{" "}
          <select value={lang} onChange={(e) => setLangS(e.target.value)} aria-label="language">
            <option value="en">English</option><option value="ar">العربية</option>
          </select>
        </label>
        {deps.length > 0 && <DeploymentPicker deps={deps} dep={dep} onChange={setDep} lang={lang}/>}
        <DeploymentStatusPopover status={status} lang={lang} showGateKeyNote={!showsCustody}/>
        {me && <span className="who" data-testid="role-badge"><span className="pill">{t(lang, me.role)}</span>{me.external && <span className="pill">{t(lang, "external")}</span>}{hasAuthority && <span className="pill">{t(lang, "authority")}</span>}</span>}
        {showsCustody && me && <KeyCustody key={me.id + (me.keyName ?? "")} user={user} me={me} lang={lang} onEnrolled={loadMe}/>}
      </header>
      <div className="layout">
        {role && !printing && <RoleNav role={role} page={page} lang={lang} hasAuthority={hasAuthority} external={!!me?.external}/>}
        <main className={role && CLIENT_ROLES.has(role) ? "client" : undefined}>
          {error && <div className="error" role="alert">{error}</div>}
          {me && !printing && <HomeLine me={me} lang={lang}/>}
          <SuspensionBanner status={status} lang={lang} user={user} canClear={hasAuthority} onCleared={refreshStatus}/>
          
          {ctx && role === "engineer" && <EngineerPages key={dep} ctx={ctx}/>}
          {ctx && role === "reviewer" && <ReviewerPages key={dep} ctx={ctx}/>}
          {ctx && role === "lead" && <LeadPages key={dep} ctx={ctx}/>}
          {ctx && role === "auditor" && <AuditorPages key={dep} ctx={ctx} readOnly={!!me?.external}/>}
          {ctx && role === "dba" && <DbaPages key={dep} ctx={ctx}/>}
          {!ctx && !error && <div className="muted">{t(lang, "loading")}</div>}
        </main>
      </div>
    </TermsProvider>);
}
