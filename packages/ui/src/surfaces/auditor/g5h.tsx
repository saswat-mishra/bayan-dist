import type { Ctx } from '../../App';
import { t } from '../../gna';
import { VerifyCommand } from '../../components/uc5j';
export function VerifyPanel({ ctx }: {
    ctx: Ctx;
}) {
    const { lang } = ctx;
    return (<div className="card" data-testid="verify-panel">
      <h2>{t(lang, "howToVerify")} <span className="pill">{t(lang, "readOnly")}</span></h2>
      <p>{t(lang, "verifySteps")}</p>
      <VerifyCommand command="bayan-verify <bundle dir> --trust <client-published trust dir> --assert-offline --strict" lang={lang}/>
      <VerifyCommand command="bayan-verify pack <evidence pack dir> --trust <client-published trust dir> --assert-offline" lang={lang}/>
    </div>);
}
