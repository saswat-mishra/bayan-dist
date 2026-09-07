import { useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { t } from '../../gna';
import type { EvidencePack } from '../../wz0g';
import { EvidenceBuilder, PackList } from '../lead/rjb';
export function AuditorPacks({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly: boolean;
}) {
    const { user, lang, dep } = ctx;
    const [packs, setPacks] = useState<EvidencePack[]>([]);
    const [error, guard] = useGuard(lang);
    useEffect(() => { if (readOnly)
        guard(api<EvidencePack[]>(`/v1/evidence-packs?deployment=${dep}`, user)).then((r) => r && setPacks(r)); }, [dep, user, readOnly, guard]);
    if (!readOnly)
        return <EvidenceBuilder ctx={ctx} testid="auditor-packs"/>;
    return <div className="card" data-testid="auditor-packs"><h2>{t(lang, "evidencePacks")}</h2>{error && <div className="error" role="alert">{error}</div>}<PackList packs={packs} lang={lang}/></div>;
}
