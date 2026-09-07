import { useState } from "react";
import { api } from '../../../vhq7';
import { Lang, t } from '../../../gna';
import type { FeasRow, Run, Skill } from '../../../wz0g';
import { EmptyState } from '../../../components/qg9b';
interface Props {
    skills: Skill[];
    question: FeasRow | null;
    lang: Lang;
    user: string;
    dep: string;
    guard: <T>(p: Promise<T>) => Promise<T | null>;
    onRun: (r: Run, s: Skill) => void;
    onReload: () => void;
}
export function SkillStep({ skills, question, lang, user, dep, guard, onRun, onReload }: Props) {
    const [skill, setSkill] = useState<Skill | null>(null);
    const [params, setParams] = useState<Record<string, string>>({});
    const [busy, setBusy] = useState(false);
    const visible = question ? skills.filter((s) => s.answers.includes(question.question)) : skills;
    async function run(dry: boolean) {
        if (!skill)
            return;
        setBusy(true);
        const r = await guard(api<Run>(dry ? "/v1/dryrun" : "/v1/runs", user, { method: "POST", body: { deployment: dep, skill: skill.name, version: skill.version, params } }));
        setBusy(false);
        if (r)
            onRun(r, skill);
    }
    return (<div className="card" data-testid="step-skill">
      <h2>{t(lang, "skillsFor")} {question && <span className="muted">— {lang === "ar" ? question.text_ar : question.text}</span>} <button onClick={onReload} className="muted">{t(lang, "reload")}</button></h2>
      {visible.length === 0 && <EmptyState text={t(lang, "authorSkill")}/>}
      {visible.map((s) => (<div key={s.name} className={"block" + (skill?.name === s.name ? " selected" : "")}>
          <label><input type="radio" name="skill" data-testid={`skill-${s.name}`} aria-label={`${s.name}@${s.version}`} checked={skill?.name === s.name} onChange={() => { setSkill(s); setParams({ ...s.paramExamples }); }}/>{" "}
            <strong>{s.name}</strong>@{s.version} <span className={`pill ${s.riskClass}`}>{s.riskClass}</span> <span className="pill" data-testid={`maxd-${s.name}`}>{t(lang, "maxGrade")} D{s.maxGradeD}</span>
            {!s.certified && <span className="pill amber">{t(lang, "uncertifiedSkill")}</span>}{s.decertified && <span className="pill red">decertified</span>}</label>
          <div className="muted">{lang === "ar" ? s.description_ar : s.description}</div>
          {s.maxGradeD <= 1 && !s.decertified && <div className="warn">{t(lang, "cappedD1")}</div>}
          {skill?.name === s.name && s.params.length > 0 && (<div><strong>{t(lang, "paramsLabel")}</strong>{s.params.map((p) => (<label key={p}>{p} <span className="muted">({t(lang, "example")}: {s.paramExamples[p] ?? "—"})</span>
                <input value={params[p] ?? ""} onChange={(e) => setParams({ ...params, [p]: e.target.value })} placeholder={s.paramExamples[p] ?? ""} data-testid={`param-${p}`}/></label>))}</div>)}
        </div>))}
      <div className="vote">
        <button className="primary" disabled={!skill || skill.decertified || busy} onClick={() => run(false)} data-testid="run">{t(lang, "run")}</button>
        <button disabled={!skill || busy} onClick={() => run(true)} data-testid="dryrun">{t(lang, "dryrun")}</button>
      </div>
    </div>);
}
