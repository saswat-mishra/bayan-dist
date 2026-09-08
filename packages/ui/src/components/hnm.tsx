import { useState } from "react";
import { Lang, t } from '../gna';
import type { ManifestField } from '../wz0g';
import { Iso, Term } from '../d7t';
export function Pseudonym({ value, lang }: {
    value: string;
    lang: Lang;
}) {
    const [copied, setCopied] = useState(false);
    const short = value.length > 14 ? `${value.slice(0, 8)}…${value.slice(-3)}` : value;
    async function copy() {
        try {
            await navigator.clipboard.writeText(value);
        }
        catch { }
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    }
    return (<button type="button" className="link pseudonym" title={value} onClick={copy} data-testid="pseudonym" data-value={value} aria-label={`${t(lang, "copyPseudonym")}: ${value}`}>
      <span className="glyph" aria-hidden="true">⌗</span><Iso>{short}</Iso>{copied && <span className="muted small" aria-live="polite"> {t(lang, "copiedShort")}</span>}
    </button>);
}
export function RowsPreview({ rows, fields, lang, limit, selectable, selected, onToggle, maxSelect, testid, keyField, sortBy }: {
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
    sortBy?: string | null;
}) {
    if (!rows.length)
        return <div className="muted" data-testid={testid ?? "rows-preview"}>{t(lang, "noRowsPreview")}</div>;
    const cols = Object.keys(rows[0]);
    const byName = new Map((fields ?? []).map((f) => [f.name, f]));
    const ordered = sortBy ? [...rows].sort((a, b) => Number(b[sortBy]) - Number(a[sortBy])) : rows;
    const shown = limit ? ordered.slice(0, limit) : ordered;
    const full = !!(selectable && maxSelect !== undefined && selected && selected.size >= maxSelect);
    const isPseudonym = (c: string) => byName.get(c)?.transform === "hmac_enclave";
    return (<div className="table-wrap" data-testid={testid ?? "rows-preview"}>
      <table className="rows">
        <thead><tr>
          {selectable && <th scope="col"><span className="sr-only">{t(lang, "lookupTitle")}</span></th>}
          {cols.map((c) => {
            const f = byName.get(c);
            return <th key={c} scope="col"><Iso>{c}</Iso>{f && <div className="col-class"><Term code={f.class}/>{f.transform && <> · <Term code={f.transform}/></>}</div>}</th>;
        })}
        </tr></thead>
        <tbody>{shown.map((r, i) => {
            const k = keyField ? String(r[keyField]) : String(i);
            const on = !!selected?.has(k);
            return (<tr key={i} data-testid={`row-${i}`}>
              {selectable && <td><input type="checkbox" aria-label={k} checked={on} disabled={!on && full} onChange={() => onToggle?.(k)} data-testid={`pick-${i}`}/></td>}
              {cols.map((c) => <td key={c}>{isPseudonym(c) ? <Pseudonym value={String(r[c])} lang={lang}/> : <Iso>{String(r[c])}</Iso>}</td>)}
            </tr>);
        })}</tbody>
      </table>
      {limit && rows.length > limit && <div className="muted small">… {rows.length - limit} {t(lang, "rows")}</div>}
    </div>);
}
