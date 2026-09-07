import { useCallback, useEffect, useState } from "react";
import { api, ApiError } from '../../vhq7';
import { explain } from '../../x27r';
import { Lang, t } from '../../gna';
import { nowIso, Signer, votePayload } from '../../ck2';
import type { Brief as BriefJson, Reveal } from '../../wz0g';
import { Decision } from './zf6u';
import { RevealCard } from './voz';
export function Blocks({ b, lang }: {
    b: BriefJson;
    lang: Lang;
}) {
    const rec = b.recipientEntry;
    return (<>
      <section className="block" data-testid="what-leaves">
        <h3>{t(lang, "whatLeaves")}</h3>
        <table><thead><tr><th scope="col">{t(lang, "fieldName")}</th><th scope="col">{t(lang, "fieldClass")}</th><th scope="col">{t(lang, "fieldTransform")}</th></tr></thead>
          <tbody>{b.fields.map((f) => <tr key={f.name}><td>{f.name}</td><td>{f.class}</td><td>{f.transform ?? <em className="warn">{t(lang, "untransformed")}</em>}</td></tr>)}</tbody></table>
        <div>{b.artefact.rows} {t(lang, "rowCount")} · <strong>{b.facts.below_threshold}</strong> {t(lang, "belowFloor")}</div>
        <div className="muted">{t(lang, "gatesPassed")}: {b.certificate.gates.filter((g) => g.passed).map((g) => g.name).join(", ")}</div>
      </section>
      <section className="block" data-testid="who-receives">
        <h3>{t(lang, "whoReceives")}</h3>
        {rec ? (rec.rostered
            ? <div>{rec.name} <span className="muted">{rec.principal}</span> · {t(lang, "employer")}: {rec.employer} · {t(lang, "location")}: {rec.location} · {t(lang, "entryValid")} {rec.validUntil?.slice(0, 10)} <span className="muted">({t(lang, "noCitizenship")})</span></div>
            : <div className="bad">{rec.name} — {t(lang, "notRostered2")}</div>)
            : <div className="muted">{b.accountability.recipient}</div>}
      </section>
      <section className="block" data-testid="diff">
        <h3>{t(lang, "whatChanged")}</h3>
        {b.diff.changed !== null && b.diff.changed !== undefined
            ? <div>Same shape as the release cleared on {b.facts.prior_date ?? b.diff.priorDate}: <strong>{b.diff.changed}</strong> value(s) changed. <span className="muted">({b.diff.sameShapeMeans})</span></div>
            : <div className="muted">{t(lang, "noPrior")}</div>}
      </section>
    </>);
}
export function Brief({ id, user, lang, onChange, signer }: {
    id: string;
    user: string;
    lang: Lang;
    onChange?: () => void;
    signer: Signer;
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
        return <div className="card">{error ? <div className="error" role="alert">{error}</div> : "…"}</div>;
    const canVote = !brief.yourVote && brief.status === "pending" && !brief.yours;
    return (<div dir={brief.brief.direction} data-testid="brief">
      <div className="card">
        <h2>{brief.skill ?? brief.mechanism} <span className={`pill ${brief.riskClass}`}>{brief.riskClass}</span></h2>
        <div className="brief" data-testid="brief-text">{brief.brief.text}</div>
        <div className="muted">presented digest <code>{brief.brief.digest.slice(0, 16)}…</code> · {t(lang, "commitment")} <code>{brief.commitment.slice(0, 23)}…</code></div>
        <Blocks b={brief} lang={lang}/>
        <button onClick={() => setShowFull(!showFull)}>{showFull ? t(lang, "hideBundle") : t(lang, "fullBundle")}</button>
        {showFull && <pre data-testid="full-bundle">{JSON.stringify(brief.artefact.preview, null, 1)}</pre>}
        
        <section className="accountability" data-testid="accountability">
          <h3>{t(lang, "signingAs")}</h3>
          <div><strong>{t(lang, "accountability")}</strong> {brief.accountability.reviewer}</div>
          <div><strong>{t(lang, "retention")}:</strong> {brief.accountability.retention} · <strong>{t(lang, "recipient")}:</strong> {brief.accountability.recipient}</div>
        </section>
        {brief.yours && <div className="error">You requested this. You cannot review it.</div>}
        {canVote && <Decision brief={brief} lang={lang} post={post} error={error}/>}
        {!canVote && !brief.yours && brief.yourVote && <div>Your vote: <strong>{brief.yourVote.verdict}</strong>{brief.yourVote.reason && ` — ${brief.yourVote.reason}`}</div>}
        {!canVote && error && <div className="error" role="alert">{error}</div>}
      </div>
      <RevealCard brief={brief} reveal={reveal} lang={lang}/>
    </div>);
}
