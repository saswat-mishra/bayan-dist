import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError } from '../../vhq7';
import { explain } from '../../x27r';
import { Lang, pick, t } from '../../gna';
import { ago } from '../../q1n';
import { nowIso, Signer, votePayload } from '../../ck2';
import type { Brief as BriefJson, Reveal } from '../../wz0g';
import { Delta } from '../../components/plk8';
import { Headline } from '../../components/uoj';
import { PersonCard } from '../../components/c3u';
import { ReadAloud } from '../../components/hdj9';
import { Technical } from '../../components/n4x';
import { Iso, Name, Runs, Term, formatDuration } from '../../d7t';
import { Decision } from './zf6u';
import type { Choice } from './zf6u';
import { DecisionBar } from './jp2';
import { LeaveSummary } from './zlf';
import { RevealCard } from './voz';
export function retentionWords(b: BriefJson, lang: Lang): string {
    return formatDuration(b.accountability.retention, lang);
}
export function briefTitle(b: BriefJson, lang: Lang): string {
    if (b.question)
        return pick(lang, b.question);
    return typeof b.facts.what === "string" ? b.facts.what : b.skill ?? b.mechanism;
}
export function signatureWeight(b: BriefJson, lang: Lang): string {
    const after = b.requiredReviews - b.votes - 1;
    if (after <= 0)
        return t(lang, "signatureLast");
    return after === 1 ? t(lang, "signatureMoreOne") : t(lang, "signatureMore").replace("{n}", String(after));
}
export function Blocks({ b, lang }: {
    b: BriefJson;
    lang: Lang;
}) {
    const rec = b.recipientEntry;
    return (<>
      <section className="purpose-block" data-testid="purpose-block">
        <h3>{t(lang, "whyTheyNeedIt")}</h3>
        <blockquote className="purpose-quote" data-testid="purpose" dir="auto"><Iso>{b.purpose}</Iso></blockquote>   
      </section>
      <dl className="facts">
        <dt>{t(lang, "whatLeaves")}</dt>
        <dd><LeaveSummary b={b} lang={lang}/></dd>
        <dt>{t(lang, "whoReceivesPerson")}</dt>
        <dd data-testid="who-receives">
          {rec ? <PersonCard lang={lang} testid="recipient-card" compact p={{ name: rec.name, principal: rec.principal, employer: rec.employer ?? b.accountability.recipientEmployer, org: b.accountability.recipientOrg, location: rec.location, validUntil: rec.validUntil, rostered: rec.rostered }}/>
            : <span><Name name={b.accountability.recipient} lang={lang}/>{b.accountability.recipientOrg && <> (<Iso>{b.accountability.recipientOrg}</Iso>)</>}</span>}
          {rec?.rostered && <span className="muted small"> · {t(lang, "noCitizenship")}</span>}
        </dd>
        <dt>{t(lang, "whatChanged")}</dt>
        <dd data-testid="diff"><Delta priorDate={b.facts.prior_date ?? b.diff.priorDate} priorBy={b.facts.prior_by} priorByYou={b.facts.prior_by_you} changed={b.diff.changed} sameShapeMeans={t(lang, "sameShapeMeans")} lang={lang}/></dd>
      </dl>
    </>);
}
export function Brief({ id, user, lang, onChange, signer, threshold }: {
    id: string;
    user: string;
    lang: Lang;
    onChange?: () => void;
    signer: Signer;
    threshold?: number;
}) {
    const [brief, setBrief] = useState<BriefJson | null>(null);
    const [showFull, setShowFull] = useState(false);
    const [reveal, setReveal] = useState<Reveal | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [choice, setChoice] = useState<Choice>(null);
    const controlRef = useRef<HTMLDivElement>(null);
    const technicalRef = useRef<HTMLDetailsElement>(null);
    const loadReveal = useCallback(() => api<Reveal>(`/v1/review/${id}/reveal`, user).then(setReveal).catch((e) => setError(explain(e, lang))), [id, user, lang]);
    const refresh = useCallback(() => api<BriefJson>(`/v1/review/${id}?lang=${lang}`, user).then((b) => { setBrief(b); if (b.yourVote)
        loadReveal(); }).catch((e) => setError(explain(e, lang))), [id, user, lang, loadReveal]);
    useEffect(() => { setReveal(null); setShowFull(false); setError(null); setChoice(null); refresh(); }, [refresh]);
    useEffect(() => {
        if (!brief || brief.status !== "pending" || !brief.yourVote)
            return;
        const h = setTimeout(refresh, 10000);
        return () => clearTimeout(h);
    }, [brief, refresh]);
    async function post(verdict: "approve" | "changes", reason: string, confirm: boolean): Promise<"confirm" | "ok" | "error"> {
        if (!brief)
            return "error";
        try {
            setError(null);
            if (!signer.keyName) {
                setError(t(lang, "keyUnenrolled"));
                return "error";
            }
            const at = nowIso();
            const signature = await signer.sign(votePayload({ request: brief.requestDigest, reviewer: user, verdict, reason, presentedDigest: brief.brief.digest, lang, at }));
            await api(`/v1/review/${id}/vote`, user, { method: "POST", body: { verdict, reason, confirm, lang, presented_digest: brief.brief.digest, signature, publicKeyId: signer.keyName, at } });
            await refresh();
            onChange?.();
            return "ok";
        }
        catch (e) {
            if (e instanceof ApiError && e.status === 409 && e.body.confirmationRequired)
                return "confirm";
            setError(explain(e, lang));
            return "error";
        }
    }
    if (!brief)
        return <div className="card">{error ? <div className="error" role="alert">{error}</div> : t(lang, "loading")}</div>;
    const canVote = !brief.yourVote && brief.status === "pending" && !brief.yours;
    const passed = brief.certificate.gates.filter((g) => g.passed);
    const what = typeof brief.facts.what === "string" ? brief.facts.what : brief.skill ?? brief.mechanism;
    const dep = typeof brief.facts.deployment === "string" ? brief.facts.deployment : brief.deployment;
    const title = briefTitle(brief, lang);
    const kind = brief.certificate.headline?.kind ?? "needs-review";
    const headline = brief.status === "pending" ? brief.certificate.headline
        : { kind: brief.status === "released" ? "released" : "refused", en: t("en", brief.status === "released" ? "headlineReleased" : "headlineRefused"), ar: t("ar", brief.status === "released" ? "headlineReleased" : "headlineRefused") } as const;
    const signedByOthers = !canVote && !brief.yourVote && !brief.yours && brief.status !== "pending";
    const readAloud = <ReadAloud text={brief.brief.text} lang={lang} textLang={brief.brief.lang} label={t(lang, "readSignedAloud")}/>;
    return (<div dir={brief.brief.direction} data-testid="brief" className="brief-tiers">   
      <section className="card decision decision-card tier" data-testid="tier-decision">
        <Headline h={headline} lang={lang}/>
        <h2 data-testid="brief-title" data-gate-text={brief.question ? undefined : "true"}><Runs text={title}/></h2>
        <p className="meta small" data-testid="brief-meta">
          {t(lang, "fromDeployment")} <Iso>{dep}</Iso> · {t(lang, "requestedBy")} <Name name={String(brief.facts.requester ?? brief.requester)} lang={lang}/>{typeof brief.ageSeconds === "number" && <> · {ago(brief.ageSeconds, lang)}</>}
        </p>
        <Blocks b={brief} lang={lang}/>
        
        {signedByOthers && <p className="muted" data-testid="not-your-signature">{t(lang, "notYourSignature")}</p>}
        {!signedByOthers && <section className="accountability" data-testid="accountability">
          <p className="signing-line"><strong>{t(lang, "accountability")} <span data-testid="signing-name"><Name name={brief.accountability.reviewer} lang={lang}/></span></strong></p>
          <p className="signing-terms">{t(lang, "signingRetention")} <span data-testid="signing-retention">{retentionWords(brief, lang)}</span> · {t(lang, "signingRecipient")} <span data-testid="signing-recipient"><Name name={brief.accountability.recipient} lang={lang}/>{brief.accountability.recipientOrg && <> (<Iso>{brief.accountability.recipientOrg}</Iso>)</>}</span></p>
          
          {canVote && <p className="signing-weight" data-testid="signing-weight">{signatureWeight(brief, lang)}</p>}
          {canVote && <Decision brief={brief} lang={lang} post={post} error={error} choice={choice} onChoose={setChoice} aside={readAloud} controlRef={controlRef}/>}
        </section>}
        {brief.yours && <div className="error">{t(lang, "yoursCannot")}</div>}
        {canVote && <p className="muted small" data-testid="sealed-note">{t(lang, "sealedNote")}</p>}
        
        {!canVote && !brief.yours && brief.yourVote && (<>
            <div data-testid="your-vote-line">{t(lang, "yourVoteWas")}: <strong>{brief.yourVote.verdict === "approve" ? t(lang, "recApprove") : t(lang, "recChanges")}</strong></div>   
            <RevealCard brief={brief} reveal={reveal} lang={lang}/>
            <div className="decision-row">{readAloud}</div>
          </>)}
        {!canVote && !brief.yourVote && !brief.yours && brief.status !== "pending" && <RevealCard brief={brief} reveal={reveal} lang={lang}/>}
        {!canVote && error && <div className="error" role="alert">{error}</div>}
      </section>
      <details className="card tier explanation disclosure" data-testid="tier-explanation">
        <summary data-testid="signed-text-summary">{t(lang, "signedTextTier")}</summary>
        <div className="brief" data-testid="brief-text" data-gate-text="true" lang={brief.brief.lang}><Runs text={brief.brief.text}/></div>
        {passed.length > 0 && <div data-testid="rules-passed"><h4>{t(lang, "rulesPassed")}</h4><ul>{passed.map((g) => <li key={g.name}><Term code={g.name}/> <span className="muted">— <Iso>{g.citation}</Iso></span></li>)}</ul></div>}
        {typeof brief.facts.does_not_stop === "string" && <div data-testid="does-not-stop"><h4>{t(lang, "doesNotStopTitle")}</h4><p data-gate-text="true"><Runs text={brief.facts.does_not_stop}/></p></div>}
        {typeof threshold === "number" && brief.facts.threshold === undefined && <p className="muted small">{t(lang, "belowFloor")} ({threshold})</p>}
      </details>
      <Technical lang={lang} title={t(lang, "technicalTier")} testid="tier-technical" detailsRef={technicalRef}>
        <div>{t(lang, "questionFor")}: <Iso>{what}</Iso></div>
        <div>{t(lang, "presentedDigestLabel")}: <Iso>{brief.brief.digest}</Iso></div>
        <div>{t(lang, "commitment")}: <Iso>{brief.commitment}</Iso></div>
        <div>request: <Iso>{brief.requestDigest}</Iso></div>
        {brief.certificate.dpe && <div>{t(lang, "gradeLabel")}: {brief.certificate.dpe} · {brief.certificate.pack_id}@{brief.certificate.pack_version}</div>}
        <div>{t(lang, "readingLang")}: {brief.brief.lang}</div>
        <button type="button" onClick={() => setShowFull(!showFull)}>{showFull ? t(lang, "bundleJsonHide") : t(lang, "bundleJson")}</button>
        {showFull && <pre data-testid="full-bundle">{JSON.stringify(brief.artefact.preview, null, 1)}</pre>}
      </Technical>
      {canVote && <DecisionBar kind={kind} title={title} lang={lang} choice={choice} onChoose={setChoice} controlRef={controlRef} technicalRef={technicalRef}/>}
    </div>);
}
