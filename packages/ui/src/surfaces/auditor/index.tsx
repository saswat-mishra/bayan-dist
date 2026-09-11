import type { Ctx } from '../../App';
import { t } from '../../gna';
import { Page } from '../../components/gct';
import { Coverage } from './s6i';
import { AuditorPacks } from './e3de';
import { Records } from './vn1w';
import { VerifyPanel } from './g5h';
export function AuditorPages({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly: boolean;
}) {
    const { lang } = ctx;
    switch (ctx.page) {
        case "packs": return <Page title={t(lang, "evidencePacks")} intro={t(lang, "introPacks")}><AuditorPacks ctx={ctx} readOnly={readOnly}/></Page>;
        case "records": return <Records ctx={ctx} readOnly={readOnly}/>;
        default: return (<Page title={t(lang, "pageCoverage")} intro={readOnly ? t(lang, "introCoverageExternal") : t(lang, "introCoverage")}>
        {readOnly && <VerifyPanel ctx={ctx} readOnly/>}
        <Coverage ctx={ctx} readOnly={readOnly}/>
        {!readOnly && <VerifyPanel ctx={ctx}/>}
      </Page>);
    }
}
