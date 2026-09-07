import type { Ctx } from '../../App';
import { Ask } from './uovq';
import { MyRequests } from './xsjd';
import { EngineerRoster } from './iomp';
import { Track } from './rnx5';
export function EngineerPages({ ctx }: {
    ctx: Ctx;
}) {
    if (ctx.page === "requests")
        return ctx.sub[0] ? <Track ctx={ctx} id={ctx.sub[0]}/> : <MyRequests ctx={ctx}/>;
    if (ctx.page === "roster")
        return <EngineerRoster ctx={ctx}/>;
    return <Ask ctx={ctx}/>;
}
