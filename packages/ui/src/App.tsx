import { useCallback, useEffect, useState } from "react";
import { api } from './vhq7';
import type { Deployment, DeploymentStatus, Pack, Principal } from './wz0g';
import { Key, Lang, t } from './gna';
import { useHash, usePersisted } from './q1n';
import { explain } from './x27r';
import { TermsProvider, nameIn } from './d7t';
import { KeyCustody, useCustody } from './components/dic';
import type { CustodyHandle } from './components/dic';
import { DeploymentPicker } from './components/ohn';
export { DeploymentStatusPopover } from './components/ohn';
import { RoleNav, NAV } from './components/rzed';
import { SuspensionBanner } from './components/y4bx';
import { EngineerPages } from './surfaces/engineer/index';
import { ReviewerPages } from './surfaces/reviewer/index';
import { LeadPages } from './surfaces/lead/index';
import { AuditorPages } from './surfaces/auditor/index';
import { DbaPages } from './surfaces/dba/index';
const DEFAULT_USER = "omar.h@vendor.example";
const CLIENT_ROLES = new Set(["reviewer", "auditor", "dba"]);
const LEGACY_AUDITOR: Record<string, string> = { controls: "coverage", register: "records/register", ledger: "records/ledger", sensor: "records/sensor", pack: "records/pack" };
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
    custody: CustodyHandle;
}
export function LangToggle({ lang, onChange }: {
    lang: Lang;
    onChange: (l: string) => void;
}) {
    return (<div className="lang-toggle" role="radiogroup" aria-label="language" data-testid="lang-toggle">
      <label className={lang === "en" ? "on" : undefined}><input type="radio" name="lang" value="en" checked={lang === "en"} onChange={() => onChange("en")} data-testid="lang-en" aria-label="English"/>EN</label>
      <label className={lang === "ar" ? "on" : undefined} lang="ar"><input type="radio" name="lang" value="ar" checked={lang === "ar"} onChange={() => onChange("ar")} data-testid="lang-ar" aria-label="العربية"/>ع</label>
    </div>);
}
export type Theme = "system" | "light" | "dark";
const THEMES: Theme[] = ["system", "light", "dark"];
const THEME_KEY: Record<Theme, Key> = { system: "themeSystem", light: "themeLight", dark: "themeDark" };
function ThemeIcon({ theme }: {
    theme: Theme;
}) {
    const common = { width: 18, height: 18, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true, focusable: false };
    if (theme === "light")
        return <svg {...common}><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>;
    if (theme === "dark")
        return <svg {...common}><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/></svg>;
    return <svg {...common}><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17a8.5 8.5 0 0 0 0-17Z" fill="currentColor" stroke="none"/></svg>;
}
export function ThemeToggle({ theme, onChange, lang }: {
    theme: Theme;
    onChange: (x: Theme) => void;
    lang: Lang;
}) {
    const next = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
    const label = `${t(lang, "themeLabel")}: ${t(lang, THEME_KEY[theme])}. ${t(lang, "themeNext")} ${t(lang, THEME_KEY[next])}.`;
    return (<button type="button" className="theme-toggle" data-testid="theme-toggle" data-theme-state={theme} onClick={() => onChange(next)} aria-label={label} title={label}>
      <ThemeIcon theme={theme}/>
    </button>);
}
export function Identity({ me, lang }: {
    me: Principal;
    lang: Lang;
}) {
    const parts = [t(lang, me.role)];
    if (me.external)
        parts.push(t(lang, "external"));
    if (me.authority)
        parts.push(t(lang, "authority"));
    return <span className="who" data-testid="role-badge" data-name={me.displayName}><span className="pill identity-chip">{parts.join(" · ")}</span></span>;
}
export function App() {
    const [user, setUser] = usePersisted("bayan.user", DEFAULT_USER);
    const [langS, setLangS] = usePersisted("bayan.lang", "en");
    const [themeS, setThemeS] = usePersisted("bayan.theme", "system");
    const theme: Theme = themeS === "light" || themeS === "dark" ? themeS : "system";
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
    useEffect(() => { const el = document.documentElement; if (theme === "system")
        el.removeAttribute("data-theme");
    else
        el.dataset.theme = theme; }, [theme]);
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
    const custody = useCustody(user, me, loadMe);
    const role = me?.role;
    const nav = role ? NAV[role] : [];
    useEffect(() => { if (role === "auditor" && segs[0] && LEGACY_AUDITOR[segs[0]])
        location.hash = `#/${LEGACY_AUDITOR[segs[0]]}`; }, [role, segs]);
    const page = segs[0] && nav.some((n) => n.page === segs[0]) ? segs[0] : (nav[0]?.page ?? "");
    const hasAuthority = !!me?.authority;
    const showsCustody = !!me && (me.role === "reviewer" || hasAuthority);
    const ctx: Ctx | null = me && dep ? { user, lang, dep, deps, me, status, pack, refreshStatus, page, sub: segs.slice(1), custody } : null;
    const printing = (page === "home" && segs[1] === "print") || (page === "requests" && segs[2] === "record");
    const offered = principals.length ? principals.filter((p) => p.canActAs !== false || p.id === user)
        : [{ id: user, displayName: user, role: "engineer", lang: "en", keyType: "software" } as Principal];
    const [name, tagline] = t(lang, "title").split(" — ");
    return (<TermsProvider terms={pack?.terms ?? null} lang={lang}>
      <header className={printing ? "no-print" : undefined}>
        <div className="brand" data-testid="brand"><span className="brand-name">{name}</span><span className="tagline"> — {tagline}</span></div>
        <div className="hdr-dep">
          {deps.length > 0 && <DeploymentPicker deps={deps} dep={dep} onChange={setDep} lang={lang} status={status} showGateKeyNote={!showsCustody}/>}
        </div>
        <div className="hdr-controls">
          <LangToggle lang={lang} onChange={setLangS}/>
          <ThemeToggle theme={theme} onChange={setThemeS} lang={lang}/>
        </div>
        <div className="hdr-id">
          <label className="picker identity"><span className="sr-only">{t(lang, "user")}</span>
            <select value={user} onChange={(e) => { setUser(e.target.value); location.hash = ""; }} aria-label="acting-as">
              {offered.map((p) => (<option key={p.id} value={p.id}>{nameIn(p.displayName, lang).shown} — {t(lang, p.role)}</option>))}
            </select>
          </label>
          {me && <Identity me={me} lang={lang}/>}
          {showsCustody && me && <KeyCustody custody={custody} lang={lang}/>}
        </div>
      </header>
      <div className="layout">
        {role && !printing && <RoleNav role={role} page={page} lang={lang} hasAuthority={hasAuthority} external={!!me?.external}/>}
        <main className={[role && CLIENT_ROLES.has(role) ? "client" : "", printing ? "printing" : ""].filter(Boolean).join(" ") || undefined}>
          {error && <div className="error" role="alert">{error}</div>}
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
