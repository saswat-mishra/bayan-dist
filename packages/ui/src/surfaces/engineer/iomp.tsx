import { useEffect, useState } from "react";
import { api, ApiError } from '../../vhq7';
import type { Ctx } from '../../App';
import { t } from '../../gna';
import type { RosterEntry } from '../../wz0g';
import { RosterCard } from '../../components/xzur';
import { EmptyState } from '../../components/qg9b';
import { explain } from '../../x27r';
export function EngineerRoster({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [me, setMe] = useState<RosterEntry | null | undefined>(undefined);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => { api<RosterEntry>(`/v1/roster/me?deployment=${dep}`, user).then(setMe).catch((e) => { if (e instanceof ApiError && e.status === 404)
        setMe(null);
    else
        setError(explain(e, lang)); }); }, [dep, user, lang]);
    return (<div data-testid="engineer-roster">
      {error && <div className="error" role="alert">{error}</div>}
      {me === null && <EmptyState text={t(lang, "notRostered")}/>}
      {me && <RosterCard e={me} lang={lang}/>}
    </div>);
}
