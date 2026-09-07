import { useState } from "react";
import { Lang, t } from '../../gna';
import type { Brief } from '../../wz0g';
import { formatDate, untilDate } from '../../d7t';
interface Props {
    brief: Brief;
    lang: Lang;
    post: (verdict: "approve" | "changes", reason: string, confirm: boolean) => Promise<"confirm" | "ok" | "error">;
    error: string | null;
}
type Choice = null | "reject" | "approve";
export function confirmCopy(brief: Brief, lang: Lang): string {
    const until = untilDate(brief.accountability.retention);
    return t(lang, "confirmBody").replace("{reviewer}", brief.accountability.reviewer).replace("{recipient}", brief.accountability.recipient)
        .replace("{org}", brief.accountability.recipientOrg ?? brief.accountability.recipientEmployer ?? "—").replace("{until}", until ? formatDate(until, lang) : brief.accountability.retention);
}
export function Decision({ brief, lang, post, error }: Props) {
    const [choice, setChoice] = useState<Choice>(null);
    const [reason, setReason] = useState("");
    const [confirming, setConfirming] = useState(false);
    const [busy, setBusy] = useState(false);
    const minLen = brief.baseline.typedReasonRequired ? brief.baseline.reasonMinLength : 1;
    async function reject() {
        setChoice("reject");
        setBusy(true);
        const r = await post("changes", "", false);
        setBusy(false);
        if (r !== "ok")
            setChoice(null);
    }
    async function approve(confirm: boolean) {
        setBusy(true);
        const r = await post("approve", reason, confirm);
        setBusy(false);
        if (r === "confirm")
            setConfirming(true);
        if (r === "ok")
            setConfirming(false);
    }
    return (<div data-testid="vote-controls">
      <h3>{t(lang, "decide")}</h3>
      <div role="radiogroup" aria-label="decision" className="segmented">
        <label><input type="radio" name="decision" checked={choice === null} onChange={() => setChoice(null)} data-testid="undecided"/> {t(lang, "undecided")}</label>
        <label className="danger"><input type="radio" name="decision" checked={choice === "reject"} onChange={reject} disabled={busy} data-testid="reject"/> {t(lang, "decisionReject")}</label>
        <label><input type="radio" name="decision" checked={choice === "approve"} onChange={() => setChoice("approve")} disabled={busy} data-testid="approve"/> {t(lang, "decisionApprove")}</label>
      </div>
      {choice === "approve" && (<div className="approve-form">
          <label>{t(lang, "reason")}
            <textarea rows={3} value={reason} onChange={(e) => setReason(e.target.value)} data-testid="reason" aria-describedby="reason-helper"/></label>
          <div id="reason-helper" className="muted small" data-testid="reason-helper">{t(lang, "reasonHelper")}{brief.baseline.typedReasonRequired && ` (≥ ${brief.baseline.reasonMinLength})`}</div>
          <div className="vote">
            <button className="primary" data-testid="approve-submit" disabled={reason.trim().length < minLen || busy} onClick={() => approve(false)}>{t(lang, "decisionApprove").replace("…", "")}</button>
            <button onClick={() => { setChoice(null); setReason(""); }}>{t(lang, "cancelWord")}</button>
          </div>
        </div>)}
      {confirming && (<div className="dialog" role="dialog" aria-modal="true" aria-labelledby="confirm-title" data-testid="confirm-dialog">
          <div>
            <p id="confirm-title"><strong>{t(lang, "confirmTitle")}</strong></p>
            <p data-testid="confirm-body">{confirmCopy(brief, lang)}</p>
            <div className="vote"><button className="primary" data-testid="confirm-approve" onClick={() => approve(true)} disabled={busy}>{t(lang, "confirmYes")}</button>
              <button onClick={() => setConfirming(false)}>{t(lang, "cancelWord")}</button></div>
          </div>
        </div>)}
      {error && <div className="error" role="alert">{error}</div>}
    </div>);
}
