import { Lang, t } from '../../../gna';
import type { Run } from '../../../wz0g';
import { CertificateDetails } from '../../../components/xsd';
export function OutputPreview({ run, lang }: {
    run: Run;
    lang: Lang;
}) {
    return (<div className="card" data-testid="output-preview">
      <h2>{t(lang, "outputPreview")} · {run.outputRef.rows} {t(lang, "rows")} <span className="muted">{t(lang, "digest")} {run.outputRef.digest.slice(0, 12)}…</span></h2>
      {run.rows.length > 0 ? (<table><thead><tr>{Object.keys(run.rows[0]).map((k) => <th key={k} scope="col">{k}</th>)}</tr></thead>
          <tbody>{run.rows.slice(0, 8).map((r, i) => <tr key={i}>{Object.values(r).map((v, j) => <td key={j}>{String(v)}</td>)}</tr>)}</tbody></table>) : <div className="muted">{t(lang, "nothingYet")}</div>}
    </div>);
}
export function RunStep({ run, lang, onImprove, onRequest }: {
    run: Run;
    lang: Lang;
    onImprove: () => void;
    onRequest: () => void;
}) {
    return (<div data-testid="step-run">
      {run.quarantine && <div className="card"><h2 className="bad">{t(lang, "quarantined")}</h2><div>{run.quarantine.rule}: {run.quarantine.detail}</div></div>}
      <CertificateDetails cert={run.certificate} lang={lang} micros={run.certificateMicros}/>
      <OutputPreview run={run} lang={lang}/>
      <div className="vote">
        <button onClick={onImprove} disabled={run.status !== "complete" || run.certificate.d >= 3} data-testid="to-improve">{t(lang, "stepImprove")} →</button>
        <button className="primary" onClick={onRequest} disabled={run.status !== "complete"} data-testid="to-request">{t(lang, "stepRequest")} →</button>
      </div>
    </div>);
}
