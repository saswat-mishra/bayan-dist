import { useState } from "react";
import type { ReactNode, RefObject } from "react";
import { Lang, t } from '../../gna';
import type { Brief } from '../../wz0g';
import { Runs, formatDate, nameIn, untilDate } from '../../d7t';
export type Choice = null | "reject" | "approve";
interface Props {
    brief: Brief;
    lang: Lang;
    post: (verdict: "approve" | "changes", reason: string, confirm: boolean) => Promise<"confirm" | "ok" | "error">;
    error: string | null;
    choice: Choice;
    onChoose: (c: Choice) => void;
    aside?: ReactNode;
    controlRef?: RefObject<HTMLDivElement>;
}
export function confirmCopy(brief: Brief, lang: Lang): string {
    const until = untilDate(brief.accountability.retention);
    return t(lang, "confirmBody").replace("{reviewer}", nameIn(brief.accountability.reviewer, lang).shown).replace("{recipient}", nameIn(brief.accountability.recipient, lang).shown)
        .replace("{org}", brief.accountability.recipientOrg ?? brief.accountability.recipientEmployer ?? "—").replace("{until}", until ? formatDate(until, lang) : brief.accountability.retention);
}
export function Segments({ choice, onChoose, lang, busy, idPrefix }: {
    choice: Choice;
    onChoose: (c: Choice) => void;
    lang: Lang;
    busy?: boolean;
    idPrefix?: string;
}) {
    const p = idPrefix ?? "";
    return (<div role="radiogroup" aria-label={t(lang, "decide")} className="segmented" data-testid={p ? `${p}segmented` : "segmented"}>
      <label className={choice === null ? "on" : undefined}><input type="radio" name={`${p}decision`} checked={choice === null} onChange={() => onChoose(null)} data-testid={`${p}undecided`}/> {t(lang, "undecided")}</label>
      <label className={choice === "reject" ? "on" : undefined}><input type="radio" name={`${p}decision`} checked={choice === "reject"} onChange={() => onChoose("reject")} disabled={busy} data-testid={`${p}reject`}/> {t(lang, "decisionReject")}</label>
      <label className={choice === "approve" ? "on" : undefined}><input type="radio" name={`${p}decision`} checked={choice === "approve"} onChange={() => onChoose("approve")} disabled={busy} data-testid={`${p}approve`}/> {t(lang, "decisionApprove")}</label>
    </div>);
}
export function Decision({ brief, lang, post, error, choice, onChoose, aside, controlRef }: Props) {
    const [reason, setReason] = useState("");
    const [confirming, setConfirming] = useState(false);
    const [busy, setBusy] = useState(false);
    const minLen = brief.baseline.typedReasonRequired ? brief.baseline.reasonMinLength : 1;
    const reviewer = nameIn(brief.accountability.reviewer, lang).shown;
    async function reject() {
        setBusy(true);
        await post("changes", "", false);
        setBusy(false);
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
    const cancel = () => { onChoose(null); setReason(""); };
    return (<div data-testid="vote-controls" className="decision-controls" ref={controlRef} aria-label={t(lang, "decide")}>
      <div className="decision-row">
        <Segments choice={choice} onChoose={onChoose} lang={lang} busy={busy}/>
        {aside}
      </div>
      {choice === null && <p className="muted small" data-testid="choose-first">{t(lang, "chooseFirst")}</p>}
      {choice === "reject" && (<div className="vote" data-testid="reject-form">
          <button className="primary" data-testid="reject-submit" disabled={busy} onClick={reject}>{t(lang, "decisionRejectSubmit")}</button>
          <button onClick={cancel} disabled={busy}>{t(lang, "cancelWord")}</button>
        </div>)}
      {choice === "approve" && (<div className="approve-form">
          <label>{t(lang, "reason")}
            <textarea rows={3} value={reason} onChange={(e) => setReason(e.target.value)} data-testid="reason" aria-describedby="reason-helper"/></label>
          <div id="reason-helper" className="muted small" data-testid="reason-helper">{t(lang, "reasonHelper")}{brief.baseline.typedReasonRequired && ` (≥ ${brief.baseline.reasonMinLength})`}</div>
          <div className="vote">
            <button className="primary" data-testid="approve-submit" disabled={reason.trim().length < minLen || busy} onClick={() => approve(false)}>{t(lang, "decisionApproveSubmit").replace("{reviewer}", reviewer)}</button>
            <button onClick={cancel} disabled={busy}>{t(lang, "cancelWord")}</button>
          </div>
        </div>)}
      {confirming && (<div className="dialog" role="dialog" aria-modal="true" aria-labelledby="confirm-title" data-testid="confirm-dialog">
          <div>
            <p id="confirm-title"><strong>{t(lang, "confirmTitle")}</strong></p>
            <p data-testid="confirm-body"><Runs text={confirmCopy(brief, lang)}/></p>
            <div className="vote"><button className="primary" data-testid="confirm-approve" onClick={() => approve(true)} disabled={busy}>{t(lang, "confirmYes")}</button>
              <button onClick={() => setConfirming(false)}>{t(lang, "cancelWord")}</button></div>
          </div>
        </div>)}
      {error && <div className="error" role="alert">{error}</div>}
    </div>);
}
