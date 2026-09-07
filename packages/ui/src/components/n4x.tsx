import { useState } from "react";
import type { ReactNode } from "react";
import { Lang, t } from '../gna';
export function Technical({ title, lang, children, copyText, open, testid }: {
    title?: string;
    lang: Lang;
    children: ReactNode;
    copyText?: string;
    open?: boolean;
    testid?: string;
}) {
    const [copied, setCopied] = useState(false);
    async function copy() {
        if (!copyText)
            return;
        try {
            await navigator.clipboard.writeText(copyText);
        }
        catch { }
        setCopied(true);
        setTimeout(() => setCopied(false), 2500);
    }
    return (<details className="technical" data-technical="true" data-testid={testid ?? "technical"} open={open}>
      <summary>{title ?? t(lang, "technical")}</summary>
      <div className="mono">{children}</div>
      {copyText && <button onClick={copy} data-testid="copy-technical" aria-live="polite">{copied ? t(lang, "copied") : t(lang, "copy")}</button>}
    </details>);
}
