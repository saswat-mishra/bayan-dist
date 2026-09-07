import type { Ctx } from '../../App';
import { Queue } from './lk2x';
import { Authority } from './rpar';
export function ReviewerPages({ ctx }: {
    ctx: Ctx;
}) {
    if (ctx.page === "authority" && ctx.me.authority)
        return <Authority ctx={ctx}/>;
    return <Queue ctx={ctx}/>;
}
