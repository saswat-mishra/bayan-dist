import type { Certificate } from '../wz0g';
import { Lang, t } from '../gna';
import { Headline } from './uoj';
import { ControlsTable } from './oqx';
import { Iso, Term } from '../d7t';
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
            {g.passed ? "✓" : "✗"} <Term code={g.name} showCode/>
            {!g.passed && (<div>
                <div>→ {g.detail}</div>
                <div>→ {g.citation}</div>
                <div><strong>{g.fixable_by_transformation ? "fixable by transformation" : "this gate cannot be satisfied by transformation of the payload"}</strong>: {g.remedy}</div>
              </div>)}
          </li>))}
      </ul>
      <h3>{t(lang, "tracks")}</h3>
      <ul>
        <li><Term code={`D${cert.d}`} showCode/>{cert.d_blockers.length > 0 && <span className="warn"> ← blocked from <Term code={`D${cert.d_blockers[0].level}`} inline/> by <Iso>{cert.d_blockers[0].field}</Iso> (<Term code={cert.d_blockers[0].field_class}/>): <Iso>{cert.d_blockers[0].reason}</Iso></span>}</li>
        <li><Term code={`P${cert.p}`} showCode/></li>
        <li><Term code={`R${cert.r}`} showCode/>{cert.r < cert.required_r && <span className="warn"> ← <Term code={`R${cert.required_r}`} inline/> required at <Term code={`D${cert.d}`} inline/> for this profile</span>}</li>
        <li><Term code={`E${cert.e}`} showCode/> <span className="muted">(exposure, not a track)</span></li>
      </ul>
      {cert.r_notes.length > 0 && <ul className="muted">{cert.r_notes.map((n) => <li key={n}>{n}</li>)}</ul>}
      <div><strong>{t(lang, "releasable")}:</strong> {cert.releasable ? "yes" : "no"}</div>
      {cert.nearest_releasable && (<div><strong>{t(lang, "nearest")}:</strong> <Iso>D{cert.nearest_releasable.d}/P{cert.p}/R{cert.nearest_releasable.required_r}</Iso>, dropping <Iso>{cert.nearest_releasable.dropped.join(", ")}</Iso>
          {cert.nearest_releasable.load_bearing_lost.length > 0 && <span className="warn"> — loses load-bearing: <Iso>{cert.nearest_releasable.load_bearing_lost.join(", ")}</Iso></span>}</div>)}
      {mechanisms && mechanisms.length > 0 && <div><strong>{t(lang, "mechanisms")}:</strong> {mechanisms.map((m, i) => <span key={m}>{i > 0 && " · "}<Term code={m} showCode/></span>)}</div>}
      {controls && <ControlsTable controls={controls} lang={lang}/>}
      <div className="muted"><strong>{t(lang, "doesNotStop")}:</strong> <Iso>{cert.does_not_stop[0]}</Iso></div>
      <div className="muted">{t(lang, "expires")} <Iso>{cert.expires_at}</Iso> · {t(lang, "packLabel")} <Iso>{cert.pack_id}@{cert.pack_version}</Iso></div>
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
