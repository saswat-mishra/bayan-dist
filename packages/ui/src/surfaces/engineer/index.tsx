import type { Ctx } from '../../App';
import { t } from '../../gna';
import { Page } from '../../components/gct';
import { Ask } from './uovq';
import { MyRequests } from './xsjd';
import { EngineerRoster } from './iomp';
import { Track } from './rnx5';
import { ReleaseRecord } from './vij';
import { Integrations } from './o8f';
export function EngineerPages({ ctx }: {
    ctx: Ctx;
}) {
    const { lang } = ctx;
    if (ctx.page === "requests") {
        if (ctx.sub[0] && ctx.sub[1] === "record")
            return <ReleaseRecord ctx={ctx} id={ctx.sub[0]}/>;
        if (ctx.sub[0])
            return <Track ctx={ctx} id={ctx.sub[0]}/>;
        return <Page title={t(lang, "myRequests")} intro={t(lang, "introRequests")}><MyRequests ctx={ctx}/></Page>;
    }
    if (ctx.page === "integrations")
        return <Integrations ctx={ctx}/>;
    if (ctx.page === "roster")
        return <Page title={t(lang, "pageRosterMine")} intro={t(lang, "introRosterMine")}><EngineerRoster ctx={ctx}/></Page>;
    return <Page title={t(lang, "pageAsk")} intro={t(lang, "introAsk")}><Ask ctx={ctx}/></Page>;
}
