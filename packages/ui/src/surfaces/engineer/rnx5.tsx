import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { ReleaseRequest, Timeline as TimelineJson } from '../../wz0g';
import { Timeline } from '../../components/rvu0';
import { CertificateDetails } from '../../components/xsd';
export function Track({ ctx, id, embedded }: {
    ctx: Ctx;
    id: string;
    embedded?: boolean;
}) {
    const { user, lang } = ctx;
    const [tl, setTl] = useState<TimelineJson | null>(null);
    const [req, setReq] = useState<ReleaseRequest | null>(null);
    const [error, guard] = useGuard(lang);
    useEffect(() => {
        let alive = true;
        const load = async () => {
            const r = await guard(api<TimelineJson>(`/v1/requests/${id}/timeline`, user));
            if (!alive || !r)
                return;
            setTl(r);
            guard(api<ReleaseRequest>(`/v1/requests/${id}`, user)).then((q) => alive && q && setReq(q));
            if (r.status === "pending")
                setTimeout(load, 3000);
        };
        load();
        return () => { alive = false; };
    }, [id, user, guard]);
    return (<div data-testid="track">
      {!embedded && <a href="#/requests">← {t(lang, "myRequests")}</a>}
      <p className="muted">{t(lang, "trackIntro")}</p>
      {error && <div className="error" role="alert">{error}</div>}
      {tl && <Timeline tl={tl} lang={lang}/>}
      {req && <div data-testid="request"><CertificateDetails cert={req.certificate} lang={lang}/></div>}
    </div>);
}
