import { useState } from "react";
import { Lang, t } from '../gna';
export function VerifyCommand({ command, lang }: {
    command: string;
    lang: Lang;
}) {
    const [copied, setCopied] = useState(false);
    async function copy() {
        try {
            await navigator.clipboard.writeText(command);
        }
        catch { }
        setCopied(true);
        setTimeout(() => setCopied(false), 2500);
    }
    return (<div className="verify" data-testid="verify-command">
      <div className="verify-status"><span className="pill ok">{t(lang, "verifiable")}</span><span className="muted small">{t(lang, "verifyExplain")}</span></div>
      <div className="verify-row">
        <code>{command}</code>
        <button onClick={copy} data-testid="copy-verify" aria-live="polite">{copied ? t(lang, "copied") : t(lang, "copy")}</button>
      </div>
    </div>);
}
