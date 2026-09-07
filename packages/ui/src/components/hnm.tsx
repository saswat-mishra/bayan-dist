import { Lang, t } from '../gna';
import type { ManifestField } from '../wz0g';
import { Term } from '../d7t';
export function RowsPreview({ rows, fields, lang, limit, selectable, selected, onToggle, maxSelect, testid, keyField }: {
    rows: Record<string, unknown>[];
    fields?: ManifestField[];
    lang: Lang;
    limit?: number;
    selectable?: boolean;
    selected?: Set<string>;
    onToggle?: (key: string) => void;
    maxSelect?: number;
    testid?: string;
    keyField?: string;
}) {
    if (!rows.length)
        return <div className="muted" data-testid={testid ?? "rows-preview"}>{t(lang, "noRowsPreview")}</div>;
    const cols = Object.keys(rows[0]);
    const byName = new Map((fields ?? []).map((f) => [f.name, f]));
    const shown = limit ? rows.slice(0, limit) : rows;
    const full = !!(selectable && maxSelect !== undefined && selected && selected.size >= maxSelect);
    return (<div className="table-wrap" data-testid={testid ?? "rows-preview"}>
      <table className="rows">
        <thead><tr>
          {selectable && <th scope="col"><span className="sr-only">{t(lang, "lookupTitle")}</span></th>}
          {cols.map((c) => {
            const f = byName.get(c);
            return <th key={c} scope="col">{c}{f && <div className="col-class"><Term code={f.class}/>{f.transform && <> · <Term code={f.transform}/></>}</div>}</th>;
        })}
        </tr></thead>
        <tbody>{shown.map((r, i) => {
            const k = keyField ? String(r[keyField]) : String(i);
            const on = !!selected?.has(k);
            return (<tr key={i} data-testid={`row-${i}`}>
              {selectable && <td><input type="checkbox" aria-label={k} checked={on} disabled={!on && full} onChange={() => onToggle?.(k)} data-testid={`pick-${i}`}/></td>}
              {cols.map((c) => <td key={c}>{String(r[c])}</td>)}
            </tr>);
        })}</tbody>
      </table>
      {limit && rows.length > limit && <div className="muted small">… {rows.length - limit} {t(lang, "rows")}</div>}
    </div>);
}
