import { Lang, t } from '../../../gna';
import type { Pack, Run } from '../../../wz0g';
import { CertificateDetails } from '../../../components/xsd';
import { RowsPreview } from '../../../components/hnm';
import { ExplainThis } from '../../../components/x503';
import { pathWordsFor, primaryAction, recommendationWords } from '../../../b3w';
import { Codes, Term, TermLine } from '../../../d7t';
export function OutputPreview({ run, lang }: {
    run: Run;
    lang: Lang;
}) {
    return (<div className="card" data-testid="output-preview">
      <h2>{t(lang, "outputPreview")} · {run.outputRef.rows} {t(lang, "rows")}</h2>
      <RowsPreview rows={run.rows} fields={run.manifest.fields} lang={lang} limit={8}/>
    </div>);
}
export function GradeMeaning({ d, lang }: {
    d: number;
    lang: Lang;
}) {
    return <p className="grade-meaning" data-testid="grade-meaning"><strong>{t(lang, "gradeMeaning")}:</strong> <Term code={`D${d}`} showCode/> — <TermLine code={`D${d}`}/></p>;
}
export function requestWords(run: Run, lang: Lang): string {
    if (run.certificate.releasable && run.certificate.required_r <= 1)
        return t(lang, "requestNow");
    return t(lang, "requestReview").replace("{n}", pathWordsFor(`R${run.certificate.required_r}`, lang));
}
export function RunStep({ run, lang, pack, onImprove, onRequest }: {
    run: Run;
    lang: Lang;
    pack?: Pack | null;
    onImprove: () => void;
    onRequest: () => void;
}) {
    const rec = run.recommendation ?? null;
    const primary = primaryAction(rec);
    const canImprove = run.status === "complete" && run.certificate.d < 3;
    const canRequest = run.status === "complete";
    return (<div data-testid="step-run">
      {run.quarantine && <div className="card"><h2 className="bad">{t(lang, "quarantined")}</h2><div>{run.quarantine.rule}: {run.quarantine.detail}</div></div>}
      <CertificateDetails cert={run.certificate} lang={lang} micros={run.certificateMicros}/>
      <GradeMeaning d={run.certificate.d} lang={lang}/>
      <ExplainThis cert={run.certificate} lang={lang} recommendation={rec} threshold={Number(pack?.review?.threshold ?? 2)}/>
      <OutputPreview run={run} lang={lang}/>
      <div className="vote" data-testid="run-actions" data-primary={primary}>
        {primary === "improve" && rec ? (<>
            <button className="primary" onClick={onImprove} disabled={!canImprove} data-testid="to-improve"><Codes text={t(lang, "improveRecommended").replace("{describe}", recommendationWords(rec, lang))} plain/></button>
            <button onClick={onRequest} disabled={!canRequest} data-testid="to-request">{t(lang, "requestAsIs").replace("{n}", pathWordsFor(`R${run.certificate.required_r}`, lang))}</button>
          </>) : (<>
            <button className="primary" onClick={onRequest} disabled={!canRequest} data-testid="to-request">{requestWords(run, lang)}</button>
            <button onClick={onImprove} disabled={!canImprove} data-testid="to-improve">{t(lang, "stepImprove")} {t(lang, "arrow")}</button>
          </>)}
      </div>
    </div>);
}
