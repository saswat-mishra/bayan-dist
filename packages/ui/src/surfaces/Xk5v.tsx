import { useEffect, useState } from "react";
import { api } from "../r7n";
import { Uhub, t } from "../hmp";

interface Df3 { id: string; deployment: string; skill: string | null; mechanism: string; requester: string; status: string; outcome: string; release: string | null; leafIndex: number | null; certificate: string; disqualified: boolean; failedGates: string[]; reviews: { reviewer: string; verdict: string }[]; createdAt: string }
interface Ledger { origin: string; size: number; checkpoint: string | null; integrity: string[]; entries: { index: number; leafHash: string; outcome: string; rrsaClass: string; humanReviews: string[]; request: string | null }[] }
interface Bundle { release: string; path: string; files: Record<string, { bytes: number; text: string | null }> }
interface Pack { id: string; version: string; digest: string; rules: { id: string; citation: string; quote: string; evidence: string; advisory?: boolean; note?: string }[] }

export function Auditor({ user, lang }: { user: string; lang: Uhub }) {
  const [dep, setDep] = useState("moi-itsm-prod-01");
  const [deps, setDeps] = useState<{ id: string; pack: string }[]>([]);
  const [reg, setReg] = useState<Df3[]>([]);
  const [ledger, setLedger] = useState<Ledger | null>(null);
  const [bundle, setBundle] = useState<Bundle | null>(null);
  const [pack, setPack] = useState<Pack | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { api<{ id: string; pack: string }[]>("/v1/deployments", user).then(setDeps).catch((e) => setError(String(e))); }, [user]);
  useEffect(() => {
    api<Df3[]>(`/v1/register?deployment=${dep}`, user).then(setReg).catch((e) => setError(String(e)));
    api<Ledger>(`/v1/ledger?deployment=${dep}`, user).then(setLedger).catch((e) => setError(String(e)));
    const p = deps.find((d) => d.id === dep)?.pack;
    if (p) api<Pack>(`/v1/packs/${p}`, user).then(setPack).catch((e) => setError(String(e)));
    setBundle(null);
  }, [dep, deps, user]);
  return (
    <div>
      {error && <div className="error">{error}</div>}
      <div className="card"><label>{t(lang, "deployment")} <select value={dep} onChange={(e) => setDep(e.target.value)}>{deps.map((d) => <option key={d.id} value={d.id}>{d.id}</option>)}</select></label></div>
      <div className="card">
        <h2>{t(lang, "register")}</h2>
        <table>
          <thead><tr><th>when</th><th>skill</th><th>requester</th><th>certificate</th><th>outcome</th><th>gates</th><th>reviews</th><th>leaf</th></tr></thead>
          <tbody>{reg.map((r) => (
            <tr key={r.id} className="clickable" onClick={() => r.release && api<Bundle>(`/v1/bundles/${r.release}`, user).then(setBundle)}>
              <td className="muted">{r.createdAt}</td><td>{r.skill ?? r.mechanism}</td><td>{r.requester}</td><td><code>{r.certificate}</code></td>
              <td className={r.outcome === "release" ? "ok" : "bad"}>{r.outcome}</td><td className="bad">{r.failedGates.join(", ")}</td>
              <td>{r.reviews.map((v) => `${v.reviewer.split("@")[0]}:${v.verdict}`).join(" ")}</td><td>{r.leafIndex ?? "—"}</td>
            </tr>))}</tbody>
        </table>
      </div>
      <div className="grid">
        <div className="card">
          <h2>{t(lang, "ledger")} — {ledger?.origin}</h2>
          {ledger && <>
            <div>size {ledger.size} · integrity {ledger.integrity.length === 0 ? <span className="ok">ok</span> : <span className="bad">{ledger.integrity.join("; ")}</span>}</div>
            <pre>{ledger.checkpoint ?? "(no checkpoint yet)"}</pre>
            <table><thead><tr><th>#</th><th>outcome</th><th>class</th><th>reviewers</th><th>leaf hash</th></tr></thead>
              <tbody>{ledger.entries.map((e) => <tr key={e.index}><td>{e.index}</td><td className={e.outcome === "release" ? "ok" : "bad"}>{e.outcome}</td><td>{e.rrsaClass}</td><td>{e.humanReviews.map((h) => h.split("@")[0]).join(", ") || "gate"}</td><td><code>{e.leafHash.slice(0, 16)}…</code></td></tr>)}</tbody></table>
          </>}
        </div>
        <div className="card">
          <h2>{t(lang, "bundle")}</h2>
          {bundle ? <>
            <div className="muted">{bundle.path}</div>
            <ul>{Object.entries(bundle.files).map(([k, v]) => <li key={k}><code>{k}</code> <span className="muted">{v.bytes} B</span></li>)}</ul>
            <div>{t(lang, "verifyHint")}</div>
            <pre>bayan-verify {bundle.path} --trust &lt;out-of-band trust dir&gt; --assert-offline</pre>
            {bundle.files["checkpoint.txt"]?.text && <pre>{bundle.files["checkpoint.txt"].text}</pre>}
          </> : <div className="muted">Select a released or refused entry.</div>}
        </div>
      </div>
      {pack && <div className="card">
        <h2>{t(lang, "packRules")} — {pack.id}@{pack.version} <code className="muted">{pack.digest.slice(0, 16)}…</code></h2>
        <table><thead><tr><th>rule</th><th>citation</th><th>quoted text</th><th>evidence</th></tr></thead>
          <tbody>{pack.rules.map((r) => <tr key={r.id}><td>{r.id}{r.advisory && <span className="pill">advisory</span>}</td><td>{r.citation}</td><td>“{r.quote}”</td><td>{r.evidence}</td></tr>)}</tbody></table>
      </div>}
    </div>
  );
}
