import { useCallback, useEffect, useState } from "react";
import { api, ApiError } from '../../vhq7';
import { explain } from '../../x27r';
import { Lang, t } from '../../gna';
import { nowIso, Signer, votePayload } from '../../ck2';
import type { Brief as BriefJson, Reveal } from '../../wz0g';
import { Delta } from '../../components/plk8';
import { Headline } from '../../components/uoj';
import { PersonCard } from '../../components/c3u';
import { ReadAloud } from '../../components/hdj9';
import { RowsPreview } from '../../components/hnm';
import { Technical } from '../../components/n4x';
import { Term } from '../../d7t';
import { formatDuration } from '../../d7t';
import { Decision } from './zf6u';
import { RevealCard } from './voz';
export function retentionWords(b: BriefJson, lang: Lang): string {
    return formatDuration(b.accountability.retention, lang);
}
export function Blocks({ b, lang }: {
    b: BriefJson;
    lang: Lang;
}) {
    const rec = b.recipientEntry;
    const rows = Array.isArray(b.artefact.preview) ? (b.artefact.preview as Record<string, unknown>[]) : [];
    return (<>
      <section className="block" data-testid="purpose-block">
        <h3>{t(lang, "whyTheyNeedIt")}</h3>
        <blockquote className="purpose-quote" data-testid="purpose">{b.purpose}</blockquote>
      </section>
      <section className="block" data-testid="what-leaves">
        <h3>{t(lang, "rowsLeave")}</h3>
        {rows.length > 0 ? <RowsPreview rows={rows} fields={b.fields} lang={lang} limit={20} testid="leaving-rows"/>
            : <ul className="fields">{b.fields.map((f) => <li key={f.name}>{f.name} — <Term code={f.class}/>{f.transform ? <> · <Term code={f.transform}/></> : <> · <em className="warn">{t(lang, "untransformed")}</em></>}</li>)}</ul>}
        <div data-testid="counts">{b.artefact.rows} {t(lang, "rowCount")} · <strong>{b.facts.below_threshold}</strong> {t(lang, "belowFloor")}{b.facts.threshold !== undefined && <span className="muted"> ({b.facts.threshold})</span>}</div>
      </section>
      <section className="block" data-testid="who-receives">
        <h3>{t(lang, "whoReceivesPerson")}</h3>
        {rec ? <PersonCard lang={lang} testid="recipient-card" p={{ name: rec.name, principal: rec.principal, employer: rec.employer ?? b.accountability.recipientEmployer, org: b.accountability.recipientOrg, location: rec.location, validUntil: rec.validUntil, rostered: rec.rostered }}/>
            : <div className="muted">{b.accountability.recipient}{b.accountability.recipientOrg && ` (${b.accountability.recipientOrg})`}</div>}
        {rec?.rostered && <div className="muted small">{t(lang, "noCitizenship")}</div>}
      </section>
      <section className="block" data-testid="diff">
        <h3>{t(lang, "whatChanged")}</h3>
        <Delta priorDate={b.facts.prior_date ?? b.diff.priorDate} priorBy={b.facts.prior_by} priorByYou={b.facts.prior_by_you} changed={b.diff.changed} sameShapeMeans={t(lang, "sameShapeMeans")} lang={lang}/>
      </section>
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
    const loadReveal = useCallback(() => api<Reveal>(`/v1/review/${id}/reveal`, user).then(setReveal).catch((e) => setError(explain(e, lang))), [id, user, lang]);
    const refresh = useCallback(() => api<BriefJson>(`/v1/review/${id}?lang=${lang}`, user).then((b) => { setBrief(b); if (b.yourVote)
        loadReveal(); }).catch((e) => setError(explain(e, lang))), [id, user, lang, loadReveal]);
    useEffect(() => { setReveal(null); setShowFull(false); setError(null); refresh(); }, [refresh]);
    useEffect(() => {
        if (!brief || brief.status !== "pending" || !brief.yourVote)
            return;
        const h = setTimeout(refresh, 3000);
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
    return (<div dir={brief.brief.direction} data-testid="brief" className="brief-tiers">
      <section className="card tier decision" data-testid="tier-decision">
        <Headline h={brief.certificate.headline} lang={lang}/>
        <h2 data-gate-text="true">{what} <span className="muted">— {t(lang, "fromDeployment")} {dep}</span></h2>
        <Blocks b={brief} lang={lang}/>
        
        <section className="accountability block" data-testid="accountability">
          <h3>{t(lang, "signingAs")}</h3>
          <div><strong>{t(lang, "signingName")}:</strong> <span data-testid="signing-name">{brief.accountability.reviewer}</span></div>
          <div><strong>{t(lang, "signingRetention")}:</strong> <span data-testid="signing-retention">{retentionWords(brief, lang)}</span></div>
          <div><strong>{t(lang, "signingRecipient")}:</strong> <span data-testid="signing-recipient">{brief.accountability.recipient}{brief.accountability.recipientOrg && ` (${brief.accountability.recipientOrg})`}</span></div>
        </section>
        {brief.yours && <div className="error">{t(lang, "yoursCannot")}</div>}
        {canVote && <Decision brief={brief} lang={lang} post={post} error={error}/>}
        {!canVote && !brief.yours && brief.yourVote && <div data-testid="your-vote-line">{t(lang, "yourVoteWas")}: <strong>{brief.yourVote.verdict === "approve" ? t(lang, "recApprove") : t(lang, "recChanges")}</strong>{brief.yourVote.reason && ` — ${brief.yourVote.reason}`}</div>}
        {!canVote && error && <div className="error" role="alert">{error}</div>}
      </section>
      <details className="card tier explanation" data-testid="tier-explanation" open>
        <summary>{t(lang, "explanationTier")}</summary>
        <div className="brief" data-testid="brief-text" data-gate-text="true" lang={brief.brief.lang}>{brief.brief.text}</div>
        <ReadAloud text={brief.brief.text} lang={lang} textLang={brief.brief.lang}/>
        {passed.length > 0 && <div data-testid="rules-passed"><h4>{t(lang, "rulesPassed")}</h4><ul>{passed.map((g) => <li key={g.name}><Term code={g.name}/> <span className="muted">— {g.citation}</span></li>)}</ul></div>}
        {typeof brief.facts.does_not_stop === "string" && <div data-testid="does-not-stop"><h4>{t(lang, "doesNotStopTitle")}</h4><p data-gate-text="true">{brief.facts.does_not_stop}</p></div>}
        {typeof threshold === "number" && brief.facts.threshold === undefined && <p className="muted small">{t(lang, "belowFloor")} ({threshold})</p>}
      </details>
      <Technical lang={lang} title={t(lang, "technicalTier")} testid="tier-technical">
        <div>{t(lang, "presentedDigestLabel")}: {brief.brief.digest}</div>
        <div>{t(lang, "commitment")}: {brief.commitment}</div>
        <div>request: {brief.requestDigest}</div>
        {brief.certificate.dpe && <div>{t(lang, "gradeLabel")}: {brief.certificate.dpe} · {brief.certificate.pack_id}@{brief.certificate.pack_version}</div>}
        <div>{t(lang, "readingLang")}: {brief.brief.lang}</div>
        <button type="button" onClick={() => setShowFull(!showFull)}>{showFull ? t(lang, "bundleJsonHide") : t(lang, "bundleJson")}</button>
        {showFull && <pre data-testid="full-bundle">{JSON.stringify(brief.artefact.preview, null, 1)}</pre>}
      </Technical>
      <RevealCard brief={brief} reveal={reveal} lang={lang}/>
    </div>);
}
