import type { Timeline as TimelineJson, TimelineStep } from '../wz0g';
import { Lang, pick, t } from '../gna';
import { Headline } from './uoj';
import { VerifyCommand } from './uc5j';
function label(s: TimelineStep, lang: Lang): string {
    switch (s.kind) {
        case "requested": return t(lang, "tRequested");
        case "sealed": return t(lang, "tSealed");
        case "review": return `${t(lang, "tReview")} ${s.n}`;
        case "cleared": return t(lang, "tCleared");
        case "refused": return t(lang, "tRefused");
        default: return t(lang, "tReleased");
    }
}
function Detail({ s, lang }: {
    s: TimelineStep;
    lang: Lang;
}) {
    if (Array.isArray(s.detail)) {
        return <ul>{(s.detail as {
            gate: string;
            remedyKind: string;
            remedy: string;
        }[]).map((g) => <li key={g.gate}><strong>{g.gate}</strong> — {t(lang, "remedy")}: <em>{g.remedyKind}</em>. {g.remedy}</li>)}</ul>;
    }
    return s.detail ? <span className="muted">{String(s.detail)}</span> : null;
}
export function Timeline({ tl, lang }: {
    tl: TimelineJson;
    lang: Lang;
}) {
    return (<div className="card" data-testid="timeline">
      <h2>{t(lang, "timeline")} <span className="pill">{tl.status}</span></h2>
      <Headline h={tl.headline} lang={lang}/>
      <ol className="timeline">
        {tl.steps.map((s, i) => (<li key={i} className={s.done ? "done" : "todo"} data-step={s.kind} data-done={s.done}>
            <span className="tl-mark" aria-hidden="true">{s.done ? "●" : "○"}</span>
            <span className="tl-label">{label(s, lang)}</span>
            {s.at && <span className="muted"> · {s.at}</span>}
            <div><Detail s={s} lang={lang}/></div>
          </li>))}
      </ol>
      {tl.status === "pending" && <div className="warn"><strong>{t(lang, "waitingFor")}:</strong> {pick(lang, tl.waitingOn)}</div>}
      {tl.bundle && tl.outcome === "release" && (<div>
          <div><strong>{t(lang, "bundlePath")}:</strong> <code>{tl.bundle.path}</code> · {t(lang, "leaf")} {tl.bundle.leafIndex}</div>
          <VerifyCommand command={tl.bundle.verify} lang={lang}/>
        </div>)}
    </div>);
}
