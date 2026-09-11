import { useState } from "react";
import { api } from '../../../vhq7';
import { Key, Lang, t } from '../../../gna';
import type { CapReason, FeasRow, Run, Skill } from '../../../wz0g';
import { EmptyState } from '../../../components/qg9b';
import { LiveStatus } from '../../../components/poy';
import { Progress } from '../../../components/nv8';
import { Iso, Sentence, Term } from '../../../d7t';
const CAP_KEY: Record<CapReason["kind"], Key> = {
    unratified_field: "capUnratified", quasi_untransformed: "capQuasi", direct_untransformed: "capDirect", freetext: "capFreetext",
    row_level: "capRowLevel", sensitive_undeclared: "capSensitive", undeclared_field: "capUndeclared", non_exportable: "capNonExportable",
};
export function CapSentence({ c, lang }: {
    c: CapReason;
    lang: Lang;
}) {
    return <span data-testid={`cap-${c.kind}`}><Sentence tpl={t(lang, CAP_KEY[c.kind])} vars={{ field: c.field ?? "—" }}/></span>;
}
interface Props {
    skills: Skill[];
    question: FeasRow | null;
    lang: Lang;
    user: string;
    dep: string;
    guard: <T>(p: Promise<T>) => Promise<T | null>;
    onRun: (r: Run, s: Skill) => void;
    onBusy?: (b: boolean) => void;
    live?: {
        updatedAt: number | null;
        refresh: () => void;
    };
}
export function SkillStep({ skills, question, lang, user, dep, guard, onRun, onBusy, live }: Props) {
    const [skill, setSkill] = useState<Skill | null>(null);
    const [params, setParams] = useState<Record<string, string>>({});
    const [busy, setBusy] = useState(false);
    const visible = question ? skills.filter((s) => s.answers.includes(question.question)) : skills;
    async function run(dry: boolean) {
        if (!skill)
            return;
        setBusy(true);
        onBusy?.(true);
        const r = await guard(api<Run>(dry ? "/v1/dryrun" : "/v1/runs", user, { method: "POST", body: { deployment: dep, skill: skill.name, version: skill.version, params } }));
        setBusy(false);
        onBusy?.(false);
        if (r)
            onRun(r, skill);
    }
    return (<div className="card" data-testid="step-skill">
      <h2>{t(lang, "skillsFor")} {question && <span className="muted">— {lang === "ar" ? question.text_ar : question.text}</span>}</h2>
      {live && <LiveStatus updatedAt={live.updatedAt} lang={lang} onRefresh={live.refresh}/>}
      {visible.length === 0 && <EmptyState text={t(lang, "noSkillYet")}/>}
      {visible.map((s) => (<div key={s.name} className={"block skill-block" + (skill?.name === s.name ? " selected" : "")} data-testid={`skill-block-${s.name}`} data-selected={skill?.name === s.name}>
          <label className="choice"><input type="radio" name="skill" data-testid={`skill-${s.name}`} aria-label={`${s.name}@${s.version}`} checked={skill?.name === s.name} onChange={() => { setSkill(s); setParams({ ...s.paramExamples }); }}/>
            <span><strong><Iso>{s.name}</Iso></strong><Iso>@{s.version}</Iso> {typeof s.requiredR === "number" && <><span data-testid={`approval-${s.name}`}><Term code={`R${s.requiredR}`}/></span> · </>}<span data-testid={`maxd-${s.name}`}>{t(lang, "maxGrade")} <span className="nowrap"><Term code={`D${s.maxGradeD}`} showCode/></span></span>
              {!s.certified && <> · <Term code="non-runner"/></>}{s.decertified && <span className="pill red">{t(lang, "decertifiedWord")}</span>}</span></label>
          <div className="muted"><Iso>{lang === "ar" ? s.description_ar : s.description}</Iso></div>
          {!s.decertified && (s.capReasons ?? []).map((c, i) => <div key={i} className="warn cap"><CapSentence c={c} lang={lang}/></div>)}
          {skill?.name === s.name && s.params.length > 0 && (<div><strong>{t(lang, "paramsLabel")}</strong>{s.params.map((p) => (<label key={p}><Iso>{p}</Iso> <span className="muted">({t(lang, "example")}: <Iso>{s.paramExamples[p] ?? "—"}</Iso>)</span>
                <input value={params[p] ?? ""} onChange={(e) => setParams({ ...params, [p]: e.target.value })} placeholder={s.paramExamples[p] ?? ""} data-testid={`param-${p}`}/></label>))}</div>)}
        </div>))}
      {!skill && visible.length > 0 && <p className="muted small" data-testid="pick-skill-first">{t(lang, "pickSkillFirst")}</p>}
      {skill?.decertified && <p className="muted small" data-testid="pick-skill-first">{t(lang, "decertifiedCannotRun")}</p>}
      <div className="vote">
        <button className="primary" disabled={!skill || skill.decertified || busy} onClick={() => run(false)} data-testid="run">{t(lang, "run")}</button>
        <button className="link" disabled={!skill || busy} onClick={() => run(true)} data-testid="dryrun">{t(lang, "dryrun")}</button>
        {busy && <Progress label={t(lang, "progressRunning")}/>}
      </div>
    </div>);
}
