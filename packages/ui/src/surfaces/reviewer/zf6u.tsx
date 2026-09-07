import { useState } from "react";
import { Lang, t } from '../../gna';
import type { Brief } from '../../wz0g';
interface Props {
    brief: Brief;
    lang: Lang;
    post: (verdict: "approve" | "changes", reason: string, confirm: boolean) => Promise<"confirm" | "ok" | "error">;
    error: string | null;
}
type Decision = null | "approve";
export function Decision({ brief, lang, post, error }: Props) {
    const [decision, setDecision] = useState<Decision>(null);
    const [reason, setReason] = useState("");
    const [confirming, setConfirming] = useState(false);
    async function approve(confirm: boolean) {
        const r = await post("approve", reason, confirm);
        if (r === "confirm")
            setConfirming(true);
        if (r === "ok")
            setConfirming(false);
    }
    return (<div data-testid="vote-controls">
      <h3>{t(lang, "decide")}</h3>
      <div role="radiogroup" aria-label="decision" className="vote">
        <label><input type="radio" name="decision" checked={decision === null} readOnly/> {t(lang, "undecided")}</label>
        <button className="danger" data-testid="reject" onClick={() => post("changes", "", false)}>{t(lang, "reject")}</button>
        <button data-testid="approve" onClick={() => setDecision("approve")} aria-pressed={decision === "approve"}>{t(lang, "approve")}</button>
      </div>
      {decision === "approve" && (<div>
          <label>{t(lang, "reason")} {brief.baseline.typedReasonRequired && <span className="muted">(≥ {brief.baseline.reasonMinLength} characters; above baseline tier)</span>}
            <textarea rows={3} value={reason} onChange={(e) => setReason(e.target.value)} data-testid="reason"/></label>
          <div className="vote">
            <button className="primary" data-testid="approve-submit" disabled={reason.trim().length === 0} onClick={() => approve(false)}>{t(lang, "approve")}</button>
            <button onClick={() => setDecision(null)}>{t(lang, "cancel")}</button>
          </div>
        </div>)}
      {confirming && (<div className="dialog" role="dialog" aria-label={t(lang, "confirmApprove")} data-testid="confirm-dialog">
          <div>
            <p><strong>{t(lang, "confirmApprove")}</strong></p>
            <p>{brief.accountability.reviewer} · {brief.accountability.retention} · {brief.accountability.recipient}</p>
            <div className="vote"><button className="primary" data-testid="confirm-approve" onClick={() => approve(true)}>{t(lang, "confirmApprove")}</button>
              <button onClick={() => setConfirming(false)}>{t(lang, "cancel")}</button></div>
          </div>
        </div>)}
      {error && <div className="error" role="alert">{error}</div>}
    </div>);
}
