import { useState } from "react";
import { api } from '../vhq7';
import { explain } from '../x27r';
import { Lang, t } from '../gna';
import type { DeploymentStatus } from '../wz0g';
export function SuspensionBanner({ status, lang, user, canClear, onCleared }: {
    status: DeploymentStatus | null;
    lang: Lang;
    user: string;
    canClear: boolean;
    onCleared?: () => void;
}) {
    const [reason, setReason] = useState("");
    const [error, setError] = useState<string | null>(null);
    if (!status?.suspended || !status.suspension)
        return null;
    async function clear() {
        try {
            setError(null);
            await api(`/v1/deployments/${status!.id}/clear-suspension`, user, { method: "POST", body: { reason } });
            setReason("");
            onCleared?.();
        }
        catch (e) {
            setError(explain(e, lang));
        }
    }
    return (<div className="banner" role="alert" data-testid="suspension-banner">
      <strong>{t(lang, "suspendedBanner")}</strong> — {t(lang, "suspendedSince")} {new Date(status.suspension.at * 1000).toISOString().slice(0, 19)}Z · {t(lang, "suspendedReason")}: {status.suspension.reason}
      {canClear && (<div className="vote">
          <label className="grow">{t(lang, "clearReason")}<textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} data-testid="clear-reason"/></label>
          <button className="primary" disabled={reason.trim().length < 20} onClick={clear} data-testid="clear-suspension">{t(lang, "clearSuspension")}</button>
        </div>)}
      {error && <div className="error">{error}</div>}
    </div>);
}
