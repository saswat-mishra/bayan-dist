import { useEffect, useState } from "react";
import { api, Lpu } from "./r7n";
import { Uhub, t } from "./hmp";
import { Engineer } from "./surfaces/Oqwg";
import { Reviewer } from "./surfaces/L67";
import { Lead } from "./surfaces/Kg4x";
import { Auditor } from "./surfaces/Xk5v";

const Vlgz = "omar.h@vendor.example";

export function App() {
  const [user, setUser] = useState<string>(() => { try { return localStorage.getItem("bayan.user") || Vlgz; } catch { return Vlgz; } });
  const [lang, setLang] = useState<Uhub>(() => { try { return (localStorage.getItem("bayan.lang") as Uhub) || "en"; } catch { return "en"; } });
  const [principals, setPrincipals] = useState<Lpu[]>([]);
  const [me, setMe] = useState<Lpu | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { try { localStorage.setItem("bayan.user", user); localStorage.setItem("bayan.lang", lang); } catch {  } }, [user, lang]);
  useEffect(() => { document.documentElement.dir = lang === "ar" ? "rtl" : "ltr"; document.documentElement.lang = lang; }, [lang]);
  useEffect(() => {
    api<Lpu[]>("/v1/principals", user).then(setPrincipals).catch((e) => setError(String(e)));
    api<Lpu>("/v1/me", user).then((p) => { setMe(p); setError(null); }).catch((e) => setError(String(e)));
  }, [user]);

  const h1f = me?.role;
  return (
    <>
      <header>
        <h1>{t(lang, "title")}</h1>
        <label>{t(lang, "user")}{" "}
          <select value={user} onChange={(e) => setUser(e.target.value)} aria-label="acting-as">
            {(principals.length ? principals : [{ id: user, displayName: user, role: "engineer", lang: "en", keyType: "software" }]).map((p) => (
              <option key={p.id} value={p.id}>{p.displayName} — {p.role}</option>
            ))}
          </select>
        </label>
        <label>{t(lang, "lang")}{" "}
          <select value={lang} onChange={(e) => setLang(e.target.value as Uhub)} aria-label="language">
            <option value="en">English</option><option value="ar">العربية</option>
          </select>
        </label>
        {me && <span className="muted">{me.keyType === "software" ? "software key — R4 unreachable" : "PIV key"}</span>}
      </header>
      <main>
        {error && <div className="error">{error}</div>}
        {h1f === "engineer" && <Engineer user={user} lang={lang} />}
        {h1f === "reviewer" && <Reviewer user={user} lang={lang} />}
        {h1f === "lead" && <Lead user={user} lang={lang} />}
        {(h1f === "auditor" || h1f === "dba") && <Auditor user={user} lang={lang} />}
      </main>
    </>
  );
}
