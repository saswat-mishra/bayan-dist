import { useCallback, useEffect, useState } from "react";
import { api } from './vhq7';
import type { Deployment, DeploymentStatus, Principal } from './wz0g';
import { Lang, t } from './gna';
import { useHash, usePersisted } from './q1n';
import { explain } from './x27r';
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
export interface Ctx {
    user: string;
    lang: Lang;
    dep: string;
    deps: Deployment[];
    me: Principal;
    status: DeploymentStatus | null;
    refreshStatus: () => void;
    page: string;
    sub: string[];
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
    const role = me?.role;
    const nav = role ? NAV[role] : [];
    const page = segs[0] && nav.some((n) => n.page === segs[0]) ? segs[0] : (nav[0]?.page ?? "");
    const hasAuthority = !!me?.authority;
    const ctx: Ctx | null = me && dep ? { user, lang, dep, deps, me, status, refreshStatus, page, sub: segs.slice(1) } : null;
    return (<>
      <header>
        <h1>{t(lang, "title")}</h1>
        <label>{t(lang, "user")}{" "}
          <select value={user} onChange={(e) => { setUser(e.target.value); location.hash = ""; }} aria-label="acting-as">
            {(principals.length ? principals : [{ id: user, displayName: user, role: "engineer", lang: "en", keyType: "software" } as Principal]).map((p) => (<option key={p.id} value={p.id}>{p.displayName} — {p.role}</option>))}
          </select>
        </label>
        <label>{t(lang, "lang")}{" "}
          <select value={lang} onChange={(e) => setLangS(e.target.value)} aria-label="language">
            <option value="en">English</option><option value="ar">العربية</option>
          </select>
        </label>
        {deps.length > 0 && <DeploymentPicker deps={deps} dep={dep} onChange={setDep} lang={lang}/>}
        {me && <span className="who" data-testid="role-badge"><span className="pill">{me.role}</span>{hasAuthority && <span className="pill">{t(lang, "authority")}</span>}</span>}
        {me && <KeyCustody key={me.id + (me.keyName ?? "")} user={user} me={me} lang={lang} onEnrolled={loadMe}/>}
      </header>
      <div className="layout">
        {role && <RoleNav role={role} page={page} lang={lang} hasAuthority={hasAuthority}/>}
        <main>
          {error && <div className="error" role="alert">{error}</div>}
          <SuspensionBanner status={status} lang={lang} user={user} canClear={hasAuthority} onCleared={refreshStatus}/>
          
          {ctx && role === "engineer" && <EngineerPages key={dep} ctx={ctx}/>}
          {ctx && role === "reviewer" && <ReviewerPages key={dep} ctx={ctx}/>}
          {ctx && role === "lead" && <LeadPages key={dep} ctx={ctx}/>}
          {ctx && (role === "auditor" || role === "assessor") && <AuditorPages key={dep} ctx={ctx} readOnly={role === "assessor"}/>}
          {ctx && role === "dba" && <DbaPages key={dep} ctx={ctx}/>}
          {!ctx && !error && <div className="muted">{t(lang, "loading")}</div>}
        </main>
      </div>
    </>);
}
