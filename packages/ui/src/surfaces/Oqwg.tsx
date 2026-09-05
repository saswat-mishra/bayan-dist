import { useCallback, useEffect, useState } from "react";
import { api, Wypi, Certificate, Tjs, Run, Oipr } from "../r7n";
import { CertificateCard } from "../components/Isbs";
import { Uhub, t } from "../hmp";

interface Deployment { id: string; name: string; pack: string }
interface Rmi { question: string; text: string; text_ar: string; minClass: string; achievableD: number | null; approvalPath: string; realTime: boolean | null; skills: string[]; blocked: boolean }
interface Gow { name: string; version: string; riskClass: string; maxGradeD: number; answers: string[]; description: string; description_ar: string; params: string[]; decertified: boolean }
interface J3g { record_id: string; ts_hour: string; topic: string; error_code: string }

export function Engineer({ user, lang }: { user: string; lang: Uhub }) {
  const [deps, setDeps] = useState<Deployment[]>([]);
  const [dep, setDep] = useState("");
  const [feas, setFeas] = useState<Rmi[]>([]);
  const [skills, setSkills] = useState<Gow[]>([]);
  const [question, setQuestion] = useState<string | null>(null);
  const [skill, setSkill] = useState<Gow | null>(null);
  const [params, setParams] = useState<Record<string, string>>({});
  const [run, setRun] = useState<Run | null>(null);
  const [menu, setMenu] = useState<Oipr | null>(null);
  const [purpose, setPurpose] = useState("");
  const [sensitive, setSensitive] = useState<string[]>([]);
  const [req, setReq] = useState<Tjs | null>(null);
  const [records, setRecords] = useState<J3g[]>([]);
  const [job, setJob] = useState<{ id: string; status: string; certificate?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const yxk = useCallback(async <T,>(p: Promise<T>): Promise<T | null> => {
    try { setError(null); return await p; } catch (e) { setError(e instanceof Wypi ? `${e.status}: ${e.message}` : String(e)); return null; }
  }, []);

  useEffect(() => { api<Deployment[]>("/v1/deployments", user).then((d) => { setDeps(d); if (!dep && d.length) setDep(d[0].id); }).catch((e) => setError(String(e))); }, [user]);
  useEffect(() => {
    if (!dep) return;
    setRun(null); setMenu(null); setReq(null); setSkill(null); setQuestion(null);
    api<Rmi[]>(`/v1/feasibility?deployment=${dep}`, user).then(setFeas).catch((e) => setError(String(e)));
    api<Gow[]>(`/v1/skills?deployment=${dep}`, user).then(setSkills).catch((e) => setError(String(e)));
  }, [dep, user]);

  const j71 = question ? skills.filter((s) => s.answers.includes(question)) : skills;

  async function vcn(dry: boolean) {
    if (!skill) return;
    const r = await yxk(api<Run>(dry ? "/v1/dryrun" : "/v1/runs", user, { method: "POST", body: { deployment: dep, skill: skill.name, version: skill.version, params } }));
    if (r) { setRun(r); setMenu(null); setReq(null); setJob(null); }
  }
  async function e2h() {
    if (!run) return;
    const m = await yxk(api<Oipr>(`/v1/runs/${run.id}/uplift?target=D2`, user, { method: "POST" }));
    if (m) setMenu(m);
  }
  async function nqmt(i: number) {
    if (!run) return;
    const r = await yxk(api<Run>(`/v1/runs/${run.id}/uplift/apply?option=${i}`, user, { method: "POST" }));
    if (r) { setRun(r); setMenu(null); }
  }
  async function q0m9() {
    if (!run) return;
    const r = await yxk(api<Tjs>("/v1/requests", user, { method: "POST", body: { deployment: dep, run: run.id, purpose, mechanism: "output-check", sensitive_declared: sensitive } }));
    if (r) setReq(r);
  }
  async function bmq() {
    const smq = await yxk(api<J3g[]>(`/v1/records?deployment=${dep}&topic=pension&limit=5`, user));
    if (smq) setRecords(smq);
  }
  async function wgfi(recordId: string) {
    const r = await yxk(api<Tjs>("/v1/requests", user, { method: "POST", body: { deployment: dep, mechanism: "exemplar", record_id: recordId, purpose } }));
    if (r) setReq(r);
  }
  async function y74g() {
    if (!run) return;
    const j = await yxk(api<{ id: string; status: string }>(`/v1/runs/${run.id}/upgrade?target=D3`, user, { method: "POST" }));
    if (!j) return;
    setJob(j);
    const f9x3 = async () => {
      const s = await api<{ id: string; status: string; certificate?: string }>(`/v1/jobs/${j.id}`, user);
      setJob(s);
      if (s.status === "done") { const gw2d = await api<Run>(`/v1/runs/${run.id}`, user); setRun(gw2d); } else setTimeout(f9x3, 200);
    };
    setTimeout(f9x3, 200);
  }

  const a4j = run?.manifest.fields.filter((f) => f.class === "SENSITIVE" && f.transform !== "drop").map((f) => f.name) ?? [];
  return (
    <div>
      {error && <div className="error" role="alert">{error}</div>}
      <div className="card">
        <label>{t(lang, "deployment")}{" "}
          <select value={dep} onChange={(e) => setDep(e.target.value)} aria-label="deployment">{deps.map((d) => <option key={d.id} value={d.id}>{d.id} — {d.name} [{d.pack}]</option>)}</select>
        </label>
      </div>
      <div className="grid">
        <div className="card">
          <h2>{t(lang, "feasibility")}</h2>
          <table>
            <thead><tr><th>{t(lang, "question")}</th><th>{t(lang, "minClass")}</th><th>{t(lang, "achievable")}</th><th>{t(lang, "path")}</th><th>{t(lang, "realtime")}</th></tr></thead>
            <tbody>
              {feas.map((r) => (
                <tr key={r.question} className={"clickable" + (question === r.question ? " selected" : "")} onClick={() => setQuestion(question === r.question ? null : r.question)}>
                  <td>{lang === "ar" ? r.text_ar : r.text}</td><td className="muted">{r.minClass}</td>
                  <td>{r.blocked ? <span className="bad">blocked</span> : r.achievableD === null ? <span className="muted">— author a skill</span> : `D${r.achievableD}`}</td>
                  <td>{r.approvalPath}</td><td>{r.realTime === null ? "—" : r.realTime ? "yes" : "async"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card">
          <h2>{t(lang, "skills")}</h2>
          {j71.map((s) => (
            <div key={s.name} className={"card" + (skill?.name === s.name ? " selected" : "")} style={{ padding: ".5rem .7rem" }}>
              <label><input type="radio" name="skill" data-testid={`skill-${s.name}`} aria-label={`${s.name}@${s.version}`} checked={skill?.name === s.name} onChange={() => { setSkill(s); setParams({}); }} /> <strong>{s.name}</strong>@{s.version}{" "}
                <span className={`pill ${s.riskClass}`}>{s.riskClass}</span> <span className="pill">max D{s.maxGradeD}</span>{s.decertified && <span className="pill red">decertified</span>}</label>
              <div className="muted">{lang === "ar" ? s.description_ar : s.description}</div>
              {skill?.name === s.name && s.params.map((p) => (
                <label key={p}>{p} <input value={params[p] ?? ""} onChange={(e) => setParams({ ...params, [p]: e.target.value })} placeholder="2026-08-21T00:00:00Z" /></label>
              ))}
            </div>
          ))}
          <div className="vote">
            <button className="primary" disabled={!skill || skill.decertified} onClick={() => vcn(false)}>{t(lang, "run")}</button>
            <button disabled={!skill} onClick={() => vcn(true)}>{t(lang, "dryrun")}</button>
          </div>
        </div>
      </div>
      {run && (
        <div className="grid">
          <div>
            {run.quarantine ? (
              <div className="card"><h2 className="bad">{t(lang, "quarantined")}</h2><div>{run.quarantine.rule}: {run.quarantine.detail}</div>
                <div className="muted">quarantines: {run.quarantine.count}{run.quarantine.decertified && " — skill decertified"}</div></div>
            ) : null}
            <CertificateCard cert={run.certificate} lang={lang} micros={run.certificateMicros} />
            <div className="card">
              <h2>Output · {run.outputRef.rows} rows {run.status === "complete" && <span className="muted">digest {run.outputRef.digest.slice(0, 12)}…</span>}</h2>
              {run.rows.length > 0 && (
                <table><thead><tr>{Object.keys(run.rows[0]).map((k) => <th key={k}>{k}</th>)}</tr></thead>
                  <tbody>{run.rows.slice(0, 12).map((r, i) => <tr key={i}>{Object.values(r).map((v, j) => <td key={j}>{String(v)}</td>)}</tr>)}</tbody></table>
              )}
            </div>
          </div>
          <div>
            <div className="card">
              <div className="vote">
                <button onClick={e2h} disabled={run.certificate.d >= 2 || run.status !== "complete"}>{t(lang, "uplift")}</button>
                <button onClick={y74g} disabled={run.certificate.d < 2 || run.certificate.d >= 3}>{t(lang, "upgrade")}</button>
                {job && <span className="muted">job {job.status}{job.certificate ? ` → ${job.certificate}` : ""}</span>}
              </div>
              {menu && (
                <div data-testid="uplift-menu">
                  <h3>{menu.current} → {menu.target}</h3>
                  {menu.unreachableReason && <div className="warn">{menu.unreachableReason}</div>}
                  <ol>
                    {menu.options.map((o, i) => (
                      <li key={i}>
                        <code>{o.describe}</code> {o.reachesTarget ? <span className="ok">✓ {o.d}</span> : <span className="bad">✗ {o.d}</span>} · {o.requiredR} · {o.keeps}
                        {o.loses.length > 0 && <span className="warn"> loses load-bearing {o.loses.join(", ")}</span>}
                        {o.recommended && <strong> ← {t(lang, "recommended")}</strong>}{" "}
                        <button onClick={() => nqmt(i)}>{t(lang, "apply")}</button>
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            </div>
            <div className="card">
              <h2>{t(lang, "request")}</h2>
              <label>{t(lang, "purpose")}<textarea rows={3} value={purpose} onChange={(e) => setPurpose(e.target.value)} /></label>
              {a4j.length > 0 && <div>{t(lang, "sensitiveDeclared")}: {a4j.map((f) => (
                <label key={f}><input type="checkbox" checked={sensitive.includes(f)} onChange={(e) => setSensitive(e.target.checked ? [...sensitive, f] : sensitive.filter((x) => x !== f))} /> {f}</label>))}</div>}
              <div className="vote">
                <button className="primary" disabled={purpose.trim().length < 20 || run.status !== "complete"} onClick={q0m9}>{t(lang, "request")}</button>
                <button onClick={bmq}>{t(lang, "exemplar")}</button>
              </div>
              {records.length > 0 && (
                <div><div className="muted">{t(lang, "records")} (pointers only — never content)</div>
                  <ul>{records.map((r) => <li key={r.record_id}><code>{r.record_id}</code> {r.ts_hour} {r.topic} {r.error_code} <button disabled={purpose.trim().length < 20} onClick={() => wgfi(r.record_id)}>{t(lang, "exemplar")}</button></li>)}</ul></div>
              )}
            </div>
          </div>
        </div>
      )}
      {req && <Hwl req={req} lang={lang} />}
    </div>
  );
}

export function Hwl({ req, lang }: { req: Tjs; lang: Uhub }) {
  const b4t: Certificate = req.certificate;
  return (
    <div className="card" data-testid="request">
      <h2>{t(lang, "status")}: {req.status} {req.outcome && req.outcome !== "pending" && `(${req.outcome})`}</h2>
      <div className="muted">request {req.id} · {t(lang, "commitment")} <code>{req.commitment}</code></div>
      {req.requiredReviews > 0 && req.status === "pending" && <div>{req.requiredReviews} blinded reviewer(s) required (R{b4t.required_r})</div>}
      {req.releaseId && <div>bundle <code>release-{req.releaseId}</code> · ledger leaf {req.leafIndex}</div>}
      {req.machineCheck && <div className="muted">machine: {req.machineCheck.verdict} / {req.machineCheck.rrsaClass} (revealed after resolution)</div>}
      {req.exemplarQuota && <div>exemplar quota: {req.exemplarQuota.consumed} of {req.exemplarQuota.limit}</div>}
      <CertificateCard cert={b4t} lang={lang} />
    </div>
  );
}
