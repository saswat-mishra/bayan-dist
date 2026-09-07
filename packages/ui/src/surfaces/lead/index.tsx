import type { Ctx } from '../../App';
import { LeadHome } from './ckh';
import { LeadRoster } from './cqt';
import { LeadEvidence } from './rjb';
export function LeadPages({ ctx }: {
    ctx: Ctx;
}) {
    if (ctx.page === "roster")
        return <LeadRoster ctx={ctx}/>;
    if (ctx.page === "evidence")
        return <LeadEvidence ctx={ctx}/>;
    return <LeadHome ctx={ctx}/>;
}
