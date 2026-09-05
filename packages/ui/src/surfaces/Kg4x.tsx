import { useEffect, useState } from "react";
import { api, Tjs, Run } from "../r7n";
import { Hwl } from "./Oqwg";
import { Uhub, t } from "../hmp";

interface S6v { deployment: string; fingerprints: number; runs: number; released: number; refused: number; autoClearedRunners: number; humanReviewed: number; overrideRate: string; byGrade: Record<string, number>; budget: { cohort: string; consumed: number; limit: number; remaining: number }[] }

export function Lead({ user, lang }: { user: string; lang: Uhub }) {
  const [dep] = useState("moi-itsm-prod-01");
  const [s, setS] = useState<S6v | null>(null);
  const [req, setReq] = useState<Tjs | null>(null);
  const [error, setError] = useState<string | null>(null);
  const h0q = () => api<S6v>(`/v1/summary?deployment=${dep}`, user).then(setS).catch((e) => setError(String(e)));
  useEffect(() => { h0q(); }, [user]);
  async function weekly() {
    try {
      const run = await api<Run>("/v1/runs", user, { method: "POST", body: { deployment: dep, skill: "weekly-usage-summary", version: "1.0.0", params: {} } });
      const r = await api<Tjs>("/v1/requests", user, { method: "POST", body: { deployment: dep, run: run.id, purpose: "Weekly usage and quality summary as acceptance evidence for the deployment milestone." } });
      setReq(r); h0q();
    } catch (e) { setError(String(e)); }
  }
  return (
    <div>
      {error && <div className="error">{error}</div>}
      <div className="card">
        <h2>{t(lang, "summary")} — {dep}</h2>
        {s && (
          <table><tbody>
            <tr><td>fingerprints</td><td>{s.fingerprints}</td></tr>
            <tr><td>skill runs</td><td>{s.runs}</td></tr>
            <tr><td>released / refused</td><td>{s.released} / {s.refused}</td></tr>
            <tr><td>auto-cleared runners</td><td>{s.autoClearedRunners} of {s.released}</td></tr>
            <tr><td>reviewer overrides</td><td>{s.overrideRate} <span className="muted">(healthy band: 5–20 per 100 reviewed)</span></td></tr>
            <tr><td>by certificate</td><td>{Object.entries(s.byGrade).map(([k, v]) => `${k}: ${v}`).join(" · ") || "—"}</td></tr>
          </tbody></table>
        )}
        <button className="primary" onClick={weekly}>Run weekly usage summary → auto-release as acceptance evidence</button>
        <p className="muted">This surface cannot request below D2: the option is absent, not refused. Ask the engineer for an exception with a reason.</p>
      </div>
      {s && s.budget.length > 0 && <div className="card"><h2>Budget</h2><table><tbody>{s.budget.map((b) => <tr key={b.cohort}><td>{b.cohort}</td><td>{b.consumed} of {b.limit}</td><td className="muted">{b.remaining} remaining</td></tr>)}</tbody></table></div>}
      {req && <Hwl req={req} lang={lang} />}
    </div>
  );
}
