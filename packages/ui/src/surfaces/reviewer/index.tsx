import type { Ctx } from '../../App';
import { t } from '../../gna';
import { Page } from '../../components/gct';
import { Queue } from './lk2x';
import { Authority } from './rpar';
export function ReviewerPages({ ctx }: {
    ctx: Ctx;
}) {
    const { lang } = ctx;
    if (ctx.page === "authority" && ctx.me.authority)
        return <Page title={t(lang, "authority")} intro={t(lang, "introAuthority")}><Authority ctx={ctx}/></Page>;
    return <Page title={t(lang, "inbox")} intro={t(lang, "introInbox")}><Queue ctx={ctx}/></Page>;
}
