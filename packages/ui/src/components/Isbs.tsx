import { Certificate } from "../r7n";
import { Uhub, t } from "../hmp";


export function CertificateCard({ cert, lang, micros }: { cert: Certificate; lang: Uhub; micros?: number }) {
  return (
    <div className="card" data-testid="certificate">
      <h2>{t(lang, "certificate")} {cert.disqualified && <span className="bad">— DISQUALIFIED</span>}</h2>
      <div className="label">{cert.label}</div>
      {micros !== undefined && <div className="muted">issued in {micros} µs</div>}
      <h3>{t(lang, "gates")}</h3>
      <ul>
        {cert.gates.map((g) => (
          <li key={g.name} className={g.passed ? "ok" : "bad gate-fail"}>
            {g.passed ? "✓" : "✗"} {g.name}
            {!g.passed && (
              <div>
                <div>→ {g.detail}</div>
                <div>→ {g.citation}</div>
                <div><strong>{g.fixable_by_transformation ? "fixable by transformation" : "this gate cannot be satisfied by transformation of the payload"}</strong>: {g.remedy}</div>
              </div>
            )}
          </li>
        ))}
      </ul>
      <h3>{t(lang, "tracks")}</h3>
      <ul>
        <li>D{cert.d}{cert.d_blockers.length > 0 && <span className="warn"> ← blocked from D{cert.d_blockers[0].level} by {cert.d_blockers[0].field} ({cert.d_blockers[0].field_class}): {cert.d_blockers[0].reason}</span>}</li>
        <li>P{cert.p}</li>
        <li>R{cert.r}{cert.r < cert.required_r && <span className="warn"> ← R{cert.required_r} required at D{cert.d} for this profile</span>}</li>
        <li>E{cert.e} <span className="muted">(exposure, not a track)</span></li>
      </ul>
      {cert.r_notes.length > 0 && <ul className="muted">{cert.r_notes.map((n) => <li key={n}>{n}</li>)}</ul>}
      <div><strong>{t(lang, "releasable")}:</strong> {cert.releasable ? "yes" : "no"}</div>
      {cert.nearest_releasable && (
        <div><strong>{t(lang, "nearest")}:</strong> D{cert.nearest_releasable.d}/P{cert.p}/R{cert.nearest_releasable.required_r}, dropping {cert.nearest_releasable.dropped.join(", ")}
          {cert.nearest_releasable.load_bearing_lost.length > 0 && <span className="warn"> — loses load-bearing: {cert.nearest_releasable.load_bearing_lost.join(", ")}</span>}</div>
      )}
      <div className="muted"><strong>{t(lang, "doesNotStop")}:</strong> {cert.does_not_stop[0]}</div>
      <div className="muted">{t(lang, "expires")} {cert.expires_at} · pack {cert.pack_id}@{cert.pack_version}</div>
    </div>
  );
}
