import { useState } from "react";
import { Lang, t } from '../../gna';
import type { Brief } from '../../wz0g';
import { RowsPreview } from '../../components/hnm';
import { Iso, Sentence, Term } from '../../d7t';
export function LeaveSummary({ b, lang }: {
    b: Brief;
    lang: Lang;
}) {
    const [open, setOpen] = useState(false);
    const rows = Array.isArray(b.artefact.preview) ? (b.artefact.preview as Record<string, unknown>[]) : [];
    const n = b.artefact.rows, cols = b.fields.length;
    const exemplar = b.mechanism === "exemplar";
    return (<div data-testid="what-leaves" className="leave-summary">
      <p className="leave-line" data-testid="leave-line">
        {exemplar ? <Sentence tpl={t(lang, "leaveSummaryOne")} vars={{ cols: String(cols) }}/>
            : <Sentence tpl={t(lang, "leaveSummary")} vars={{ rows: String(n), cols: String(cols), below: String(b.facts.below_threshold), threshold: String(b.facts.threshold ?? "—") }}/>}
      </p>
      <ul className="leave-cols" data-testid="leave-cols">
        {b.fields.map((f) => (<li key={f.name} data-field={f.name}><Iso>{f.name}</Iso> — <Term code={f.class}/>{f.transform ? <> · <Term code={f.transform}/></> : <> · <em className="warn">{t(lang, "untransformed")}</em></>}</li>))}
      </ul>
      <div data-testid="counts" className="sr-only">{n} {t(lang, "rowCount")} · {b.facts.below_threshold} {t(lang, "belowFloor")}{b.facts.threshold !== undefined && ` (${b.facts.threshold})`}</div>
      {rows.length > 0 && (<details className="disclosure rows-disclosure" data-testid="rows-disclosure" open={open} onToggle={(e) => setOpen((e.currentTarget as HTMLDetailsElement).open)}>
          <summary data-testid="show-rows">{open ? t(lang, "hideRows").replace("{n}", String(rows.length)) : rows.length < n ? t(lang, "showRowsOf").replace("{k}", String(rows.length)).replace("{n}", String(n)) : t(lang, "showRows").replace("{n}", String(rows.length))}</summary>
          <RowsPreview rows={rows} fields={b.fields} lang={lang} testid="leaving-rows"/>
        </details>)}
    </div>);
}
