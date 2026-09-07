import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";
import type { Lang } from './gna';
export type TermEntry = {
    label: string;
    line: string;
};
export type TermTable = Record<string, Record<string, TermEntry>>;
const TermsContext = createContext<{
    terms: TermTable | null;
    lang: Lang;
}>({ terms: null, lang: "en" });
export function TermsProvider({ terms, lang, children }: {
    terms: TermTable | null;
    lang: Lang;
    children: ReactNode;
}) {
    return <TermsContext.Provider value={{ terms, lang }}>{children}</TermsContext.Provider>;
}
export function useTerm(code: string, langOverride?: Lang): TermEntry | null {
    const { terms, lang } = useContext(TermsContext);
    const l = langOverride ?? lang;
    const table = terms?.[l] ?? terms?.en;
    const e = table?.[code];
    return e && e.label && e.line ? e : null;
}
export function Term({ code, showCode, className, plain, inline }: {
    code: string;
    showCode?: boolean;
    className?: string;
    plain?: boolean;
    inline?: boolean;
}) {
    const entry = useTerm(code);
    const [open, setOpen] = useState(false);
    if (!entry)
        return <span className={"term missing " + (className ?? "")} data-term={code} data-missing="true" title={code}>{code}</span>;
    const text = inline ? <>{code}</> : <>{entry.label}{showCode && <span className="term-code"> {code}</span>}</>;
    const meaning = inline ? `${entry.label} — ${entry.line}` : entry.line;
    if (plain)
        return <span className={"term " + (inline ? "inline " : "") + (className ?? "")} data-term={code} title={meaning}>{text}</span>;
    return (<span className={"term " + (inline ? "inline " : "") + (className ?? "")} data-term={code}>
      <button type="button" className="term-chip" aria-expanded={open} onClick={() => setOpen(!open)} title={meaning}>{text}</button>
      {open && <span role="note" className="term-card"><strong>{entry.label}</strong> — {entry.line}</span>}
    </span>);
}
const CODE = /(\b[DPRE][0-4]\b|\b(?:DIRECT|QUASI|SENSITIVE|STRUCTURAL|VENDOR|FREETEXT)\b|\bhmac_enclave\b)/;
export function Codes({ text, plain }: {
    text: string;
    plain?: boolean;
}) {
    const parts = text.split(CODE);
    return <>{parts.map((p, i) => (i % 2 === 1 ? <Term key={i} code={p} inline plain={plain}/> : <span key={i}>{p}</span>))}</>;
}
export function TermLine({ code }: {
    code: string;
}) {
    const entry = useTerm(code);
    return <span data-term={code} data-missing={entry ? undefined : "true"}>{entry ? entry.line : code}</span>;
}
export function Bi({ x, lang }: {
    x: {
        en: string;
        ar?: string | null;
    } | null | undefined;
    lang: Lang;
}) {
    if (!x)
        return null;
    if (lang === "ar") {
        if (x.ar && x.ar.trim())
            return <>{x.ar}</>;
        return <span data-fallback="en">{x.en}</span>;
    }
    return <>{x.en}</>;
}
export function bi(lang: Lang, x: {
    en: string;
    ar?: string | null;
} | null | undefined): {
    text: string;
    fallback: boolean;
} {
    if (!x)
        return { text: "", fallback: false };
    if (lang === "ar")
        return x.ar && x.ar.trim() ? { text: x.ar, fallback: false } : { text: x.en, fallback: true };
    return { text: x.en, fallback: false };
}
const DUR = /^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?$/;
export function durationDays(iso: string): number | null {
    const m = DUR.exec(iso.trim());
    if (!m || !m.slice(1).some(Boolean))
        return null;
    const [y, mo, w, d] = m.slice(1).map((x) => parseInt(x ?? "0", 10) || 0);
    return y * 365 + Math.floor(mo * 30.44) + w * 7 + d;
}
const AR_DIGITS = false;
const EN_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
export function formatDate(iso: string, lang: Lang): string {
    const d = new Date(iso);
    if (Number.isNaN(d.getTime()))
        return iso;
    if (lang !== "ar")
        return `${d.getUTCDate()} ${EN_MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
    const fmt = new Intl.DateTimeFormat(AR_DIGITS ? "ar" : "ar-u-nu-latn", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
    return fmt.format(d);
}
export function formatDuration(iso: string, lang: Lang, from?: Date | string): string {
    const days = durationDays(iso);
    if (days === null)
        return iso;
    const start = from ? new Date(from) : new Date();
    const until = new Date(start.getTime() + days * 86400000).toISOString();
    const length = lang === "ar" ? `${days} يوماً` : `${days} days`;
    return `${length} · ${lang === "ar" ? "حتى" : "until"} ${formatDate(until, lang)}`;
}
export function untilDate(iso: string, from?: Date | string): string | null {
    const days = durationDays(iso);
    if (days === null)
        return null;
    const start = from ? new Date(from) : new Date();
    return new Date(start.getTime() + days * 86400000).toISOString();
}
