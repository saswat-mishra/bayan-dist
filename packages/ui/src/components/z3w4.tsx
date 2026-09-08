import { Lang, t } from '../gna';
import type { CustodyState } from './dic';
import { Name, Sentence } from '../d7t';
import { StateChip } from './drm';
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
    return (<div className="card onboarding" data-testid="onboarding" data-state={state.kind}>
      <h2>{t(lang, "onboarding")}</h2>
      <ol className="checklist">
        
        <li data-step="enrol" data-state={step1}><StateChip kind={step1} lang={lang}/><span className="step-text">{t(lang, "onboardEnrol")}</span>
          {step1 === "todo" && state.kind !== "loading" && <button className="primary" data-testid="enrol-key-onboarding" onClick={onEnrol}>{t(lang, "enrolKey")}</button>}</li>
        <li data-step="approve" data-state={step2}><StateChip kind={step2} lang={lang}/><span className="step-text"><Sentence tpl={t(lang, "onboardApprove")} vars={{ names: approvers.length ? approvers.map((n, i) => <span key={n}>{i > 0 && ", "}<Name name={n} lang={lang}/></span>) : "—" }}/>{step2 === "pending" && <span className="muted small"> — {t(lang, "weToldThem")}</span>}</span></li>
        <li data-step="ready" data-state={step3}><StateChip kind={step3} lang={lang}/><span className="step-text">{t(lang, "onboardReady")}</span></li>
      </ol>
    </div>);
}
