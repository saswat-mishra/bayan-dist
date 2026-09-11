import { useCallback, useEffect, useRef, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard, useLive } from '../../q1n';
import { Key, Lang, t } from '../../gna';
import type { AskAnswer, AssistantView, FeasRow, ReleaseRequest, Run, Skill } from '../../wz0g';
import { QuestionStep } from './steps/zb46';
import { SkillStep } from './steps/ry8';
import { RunStep } from './steps/edn5';
import { ImproveStep } from './steps/dg5n';
import { RequestStep } from './steps/ab2';
import { Handoff } from './m14';
const STEPS: Key[] = ["stepQuestion", "stepSkill", "stepRun", "stepImprove", "stepRequest", "handoff"];
const NAMES = ["question", "skill", "run", "improve", "request", "handoff"];
export function Rail({ step, reached, onGo, lang, busy }: {
    step: number;
    reached: number;
    onGo: (i: number) => void;
    lang: Lang;
    busy?: boolean;
}) {
    return (<ol className="rail" aria-label="progress" data-testid="rail" aria-busy={busy || undefined}>
      {STEPS.map((k, i) => (<li key={k} aria-current={i === step ? "step" : undefined} className={i < step ? "done" : ""}>
          <button disabled={i > reached || !!busy} onClick={() => onGo(i)} data-testid={`rail-${i + 1}`}>{i + 1} {t(lang, k)}</button>
        </li>))}
    </ol>);
}
export function askUrl(step: number, id?: string | null): string {
    return `ask/${NAMES[step]}${id ? `/${id}` : ""}`;
}
export function Ask({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep, sub } = ctx;
    const urlStep = Math.max(0, NAMES.indexOf(sub[0] ?? "question"));
    const urlId = sub[1] ?? null;
    const [step, setStep] = useState(urlStep);
    const [reached, setReached] = useState(urlStep);
    const [feas, setFeas] = useState<FeasRow[]>([]);
    const [skills, setSkills] = useState<Skill[]>([]);
    const [question, setQuestion] = useState<FeasRow | null>(null);
    const [skill, setSkill] = useState<Skill | null>(null);
    const [run, setRun] = useState<Run | null>(null);
    const [req, setReq] = useState<ReleaseRequest | null>(null);
    const [busy, setBusy] = useState(false);
    const [error, guard] = useGuard(lang);
    const hydrated = useRef<string | null>(null);
    const [assistant, setAssistant] = useState<AssistantView | null>(null);
    useEffect(() => { api<AssistantView>(`/v1/assistant?deployment=${dep}`, user).then(setAssistant).catch(() => setAssistant(null)); }, [dep, user]);
    const askModel = useCallback((text: string, l: Lang) => api<AskAnswer>("/v1/ask", user, { method: "POST", body: { deployment: dep, text, lang: l } }), [dep, user]);
    useEffect(() => {
        guard(api<FeasRow[]>(`/v1/feasibility?deployment=${dep}`, user)).then((r) => r && setFeas(r));
    }, [dep, user, guard]);
    const loadSkills = useCallback(() => guard(api<Skill[]>(`/v1/skills?deployment=${dep}`, user)).then((s) => s && setSkills(s)), [dep, user, guard]);
    const live = useLive(loadSkills, 15000, step === 1);
    useEffect(() => { if (skills.length === 0)
        void loadSkills(); }, [loadSkills, skills.length]);
    useEffect(() => {
        if (!urlId || hydrated.current === urlId)
            return;
        hydrated.current = urlId;
        if (urlStep === 5) {
            guard(api<ReleaseRequest>(`/v1/requests/${urlId}`, user)).then((r) => { if (r) {
                setReq(r);
                setStep(5);
                setReached(5);
                if (r.run)
                    guard(api<Run>(`/v1/runs/${r.run}`, user)).then((x) => x && setRun(x));
            } });
        }
        else {
            guard(api<Run>(`/v1/runs/${urlId}`, user)).then((r) => { if (r) {
                setRun(r);
                setStep(urlStep);
                setReached(Math.max(urlStep, 2));
            } });
        }
    }, [urlId, urlStep, user, guard]);
    useEffect(() => {
        const id = step === 5 ? req?.id : step >= 2 ? run?.id : null;
        const want = `#/${askUrl(step, id)}`;
        if (location.hash !== want && (step < 2 || id))
            location.hash = want;
    }, [step, run?.id, req?.id]);
    useEffect(() => { if (skills.length && run && !skill)
        setSkill(skills.find((s) => s.name === run.skill) ?? null); }, [skills, run, skill]);
    const advance = useCallback((i: number) => { setStep(i); setReached((r) => Math.max(r, i)); }, []);
    return (<div data-testid="ask">
      <Rail step={step} reached={reached} onGo={setStep} lang={lang} busy={busy}/>
      {error && <div className="error" role="alert">{error}</div>}
      {step === 0 && <QuestionStep ctx={ctx} rows={feas} skills={skills} selected={question} onPick={(q) => { setQuestion(q); setSkill(null); advance(1); }} assistant={assistant} askModel={askModel}/>}
      {step === 1 && <SkillStep skills={skills} question={question} lang={lang} user={user} dep={dep} guard={guard} onRun={(r, s) => { setSkill(s); setRun(r); setReq(null); advance(2); }} onBusy={setBusy} live={live}/>}
      {step === 2 && run && <RunStep run={run} lang={lang} pack={ctx.pack} onImprove={() => advance(3)} onRequest={() => advance(4)}/>}
      {step === 3 && run && <ImproveStep run={run} lang={lang} user={user} guard={guard} onRun={setRun} onRequest={() => advance(4)} onBusy={setBusy}/>}
      {step === 4 && run && <RequestStep ctx={ctx} run={run} skill={skill} question={question} guard={guard} onRequested={(r) => { setReq(r); advance(5); }} onBusy={setBusy}/>}
      {step === 5 && req && <Handoff ctx={ctx} id={req.id} run={run}/>}
      {step >= 2 && !run && !req && <div className="muted">{t(lang, "loading")}</div>}
    </div>);
}
