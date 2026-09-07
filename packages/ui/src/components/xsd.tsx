import type { Certificate } from '../wz0g';
import { Lang, t } from '../gna';
import { Headline } from './uoj';
import { ControlsTable } from './oqx';
export function CertificateBody({ cert, lang, micros, mechanisms, controls }: {
    cert: Certificate;
    lang: Lang;
    micros?: number;
    mechanisms?: string[];
    controls?: Record<string, string[]>;
}) {
    return (<div className="cert-body">
      <div className="label">{cert.label} {cert.disqualified && <span className="bad">— DISQUALIFIED</span>}</div>
      {micros !== undefined && <div className="muted">{t(lang, "certificateIssuedIn")} {micros} µs</div>}
      <h3>{t(lang, "gates")}</h3>
      <ul>
        {cert.gates.map((g) => (<li key={g.name} className={g.passed ? "ok" : "bad gate-fail"}>
            {g.passed ? "✓" : "✗"} {g.name}
            {!g.passed && (<div>
                <div>→ {g.detail}</div>
                <div>→ {g.citation}</div>
                <div><strong>{g.fixable_by_transformation ? "fixable by transformation" : "this gate cannot be satisfied by transformation of the payload"}</strong>: {g.remedy}</div>
              </div>)}
          </li>))}
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
      {cert.nearest_releasable && (<div><strong>{t(lang, "nearest")}:</strong> D{cert.nearest_releasable.d}/P{cert.p}/R{cert.nearest_releasable.required_r}, dropping {cert.nearest_releasable.dropped.join(", ")}
          {cert.nearest_releasable.load_bearing_lost.length > 0 && <span className="warn"> — loses load-bearing: {cert.nearest_releasable.load_bearing_lost.join(", ")}</span>}</div>)}
      {mechanisms && mechanisms.length > 0 && <div><strong>{t(lang, "mechanisms")}:</strong> {mechanisms.join(" · ")}</div>}
      {controls && <ControlsTable controls={controls} lang={lang}/>}
      <div className="muted"><strong>{t(lang, "doesNotStop")}:</strong> {cert.does_not_stop[0]}</div>
      <div className="muted">{t(lang, "expires")} {cert.expires_at} · {t(lang, "packLabel")} {cert.pack_id}@{cert.pack_version}</div>
    </div>);
}
export function CertificateDetails({ cert, lang, micros, mechanisms, controls, open }: {
    cert: Certificate;
    lang: Lang;
    micros?: number;
    mechanisms?: string[];
    controls?: Record<string, string[]>;
    open?: boolean;
}) {
    return (<div className="card" data-testid="certificate">
      <Headline h={cert.headline} lang={lang}/>
      <details open={open} data-technical="true">
        <summary>{t(lang, "showDetails")} · <span className="label small">{cert.label}</span></summary>
        <CertificateBody cert={cert} lang={lang} micros={micros} mechanisms={mechanisms} controls={controls}/>
      </details>
    </div>);
}
