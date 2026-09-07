import type { Ctx } from '../../App';
import { t } from '../../gna';
import { VerifyCommand } from '../../components/uc5j';
export function VerifyPanel({ ctx }: {
    ctx: Ctx;
}) {
    const { lang, status } = ctx;
    const trust = status?.trustDir ?? "<client-published trust dir>";
    const outbox = status?.outboxDir ?? "<outbox>";
    return (<div className="card" data-testid="verify-panel">
      <h2>{t(lang, "howToVerify")} <span className="pill">{t(lang, "readOnly")}</span></h2>
      <p>{t(lang, "verifySteps")}</p>
      <VerifyCommand command={`bayan-verify ${outbox}/<release dir> --trust ${trust} --assert-offline --strict`} lang={lang}/>
      <VerifyCommand command={`bayan-verify pack ${outbox}/<evidence pack dir> --trust ${trust} --assert-offline`} lang={lang}/>
    </div>);
}
