import { Lang, t } from '../gna';
import type { CustodyState } from './dic';
export function OnboardingChecklist({ state, approvers, lang, onEnrol }: {
    state: CustodyState;
    approvers: string[];
    lang: Lang;
    onEnrol: () => void;
}) {
    const enrolled = state.kind === "enrolled";
    const pending = state.kind === "pending";
    const step1 = enrolled || pending ? "done" : "todo";
    const step2 = enrolled ? "done" : pending ? "pending" : "todo";
    const step3 = enrolled ? "done" : "todo";
    const word = (s: string) => t(lang, s === "done" ? "stepDone" : s === "pending" ? "stepPending" : "stepTodo");
    return (<div className="card onboarding" data-testid="onboarding" data-state={state.kind}>
      <h2>{t(lang, "onboarding")}</h2>
      <ol className="checklist">
        <li data-step="enrol" data-state={step1}><span className="tick" aria-hidden="true">{step1 === "done" ? "✓" : "○"}</span> {t(lang, "onboardEnrol")} <span className="muted">— {word(step1)}</span>
          {step1 === "todo" && state.kind !== "loading" && <> <button className="primary" data-testid="enrol-key-onboarding" onClick={onEnrol}>{t(lang, "enrolKey")}</button></>}</li>
        <li data-step="approve" data-state={step2}><span className="tick" aria-hidden="true">{step2 === "done" ? "✓" : step2 === "pending" ? "◔" : "○"}</span> {t(lang, "onboardApprove").replace("{names}", approvers.join(", ") || "—")} <span className="muted">— {word(step2)}{step2 === "pending" ? `; ${t(lang, "weToldThem")}` : ""}</span></li>
        <li data-step="ready" data-state={step3}><span className="tick" aria-hidden="true">{step3 === "done" ? "✓" : "○"}</span> {t(lang, "onboardReady")} <span className="muted">— {word(step3)}</span></li>
      </ol>
    </div>);
}
