import type { Ctx } from '../../App';
import { t } from '../../gna';
import { Page } from '../../components/gct';
import { LeadHome } from './ckh';
import { LeadRoster } from './cqt';
import { LeadEvidence } from './rjb';
export function LeadPages({ ctx }: {
    ctx: Ctx;
}) {
    const { lang } = ctx;
    if (ctx.page === "roster")
        return <Page title={t(lang, "rosterWrite")} intro={t(lang, "introRosterLead")}><LeadRoster ctx={ctx}/></Page>;
    if (ctx.page === "evidence")
        return <Page title={t(lang, "evidencePacks")} intro={t(lang, "introEvidence")}><LeadEvidence ctx={ctx}/></Page>;
    if (ctx.sub[0] === "print")
        return <LeadHome ctx={ctx}/>;
    return <Page title={t(lang, "dashboard")} intro={t(lang, "introDashboard")}><LeadHome ctx={ctx}/></Page>;
}
