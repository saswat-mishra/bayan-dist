import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Key, Lang, t } from '../../gna';
import type { FeasRow, ReleaseRequest, Run, Skill } from '../../wz0g';
import { QuestionStep } from './steps/zb46';
import { SkillStep } from './steps/ry8';
import { RunStep } from './steps/edn5';
import { ImproveStep } from './steps/dg5n';
import { RequestStep } from './steps/ab2';
import { Track } from './rnx5';
const STEPS: Key[] = ["stepQuestion", "stepSkill", "stepRun", "stepImprove", "stepRequest", "stepTrack"];
export function Rail({ step, reached, onGo, lang }: {
    step: number;
    reached: number;
    onGo: (i: number) => void;
    lang: Lang;
}) {
    return (<ol className="rail" aria-label="progress" data-testid="rail">
      {STEPS.map((k, i) => (<li key={k} aria-current={i === step ? "step" : undefined} className={i < step ? "done" : ""}>
          <button disabled={i > reached} onClick={() => onGo(i)} data-testid={`rail-${i + 1}`}>{i + 1} {t(lang, k)}</button>
        </li>))}
    </ol>);
}
export function Ask({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [step, setStep] = useState(0);
    const [reached, setReached] = useState(0);
    const [feas, setFeas] = useState<FeasRow[]>([]);
    const [skills, setSkills] = useState<Skill[]>([]);
    const [question, setQuestion] = useState<FeasRow | null>(null);
    const [skill, setSkill] = useState<Skill | null>(null);
    const [run, setRun] = useState<Run | null>(null);
    const [req, setReq] = useState<ReleaseRequest | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => {
        setStep(0);
        setReached(0);
        setQuestion(null);
        setSkill(null);
        setRun(null);
        setReq(null);
        guard(api<FeasRow[]>(`/v1/feasibility?deployment=${dep}`, user)).then((r) => r && setFeas(r));
        guard(api<Skill[]>(`/v1/skills?deployment=${dep}`, user)).then((s) => s && setSkills(s));
    }, [dep, user, guard]);
    const advance = (i: number) => { setStep(i); setReached((r) => Math.max(r, i)); };
    const reloadSkills = () => guard(api<Skill[]>(`/v1/skills?deployment=${dep}`, user)).then((s) => s && setSkills(s));
    return (<div data-testid="ask">
      <Rail step={step} reached={reached} onGo={setStep} lang={lang}/>
      {error && <div className="error" role="alert">{error}</div>}
      {step === 0 && <QuestionStep rows={feas} lang={lang} selected={question} onPick={(q) => { setQuestion(q); setSkill(null); advance(1); }}/>}
      {step === 1 && <SkillStep skills={skills} question={question} lang={lang} user={user} dep={dep} guard={guard} onRun={(r, s) => { setSkill(s); setRun(r); setReq(null); advance(2); }} onReload={reloadSkills}/>}
      {step === 2 && run && <RunStep run={run} lang={lang} onImprove={() => advance(3)} onRequest={() => advance(4)}/>}
      {step === 3 && run && <ImproveStep run={run} lang={lang} user={user} guard={guard} onRun={setRun} onRequest={() => advance(4)}/>}
      {step === 4 && run && <RequestStep ctx={ctx} run={run} skill={skill} guard={guard} onRequested={(r) => { setReq(r); advance(5); }}/>}
      {step === 5 && req && <Track ctx={ctx} id={req.id} embedded/>}
    </div>);
}
