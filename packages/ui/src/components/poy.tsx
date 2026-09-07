import { useTicker } from '../q1n';
import { Lang, t } from '../gna';
export function LiveStatus({ updatedAt, lang, onRefresh }: {
    updatedAt: number | null;
    lang: Lang;
    onRefresh?: () => void;
}) {
    const now = useTicker(1000);
    const s = updatedAt === null ? null : Math.max(0, Math.round((now - updatedAt) / 1000));
    return (<span className="live" data-testid="live-status" aria-live="off">
      {s === null ? t(lang, "loading") : `${t(lang, "updated")} ${s} ${t(lang, "secondsAgo")}`}
      {onRefresh && <> · <button className="link" onClick={onRefresh} data-testid="refresh">{t(lang, "refreshNow")}</button></>}
    </span>);
}
