import type { Ctx } from '../../App';
import { t } from '../../gna';
import { Section } from '../../components/gct';
import { VerifyCommand } from '../../components/uc5j';
export function VerifyPanel({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly?: boolean;
}) {
    const { lang, status } = ctx;
    const trust = status?.trustDir ?? "…";
    const outbox = status?.outboxDir ?? "…";
    return (<Section heading={t(lang, "verifyStatusTitle")} purpose={t(lang, "verifyStatusLine")} testid="verify-panel" aside={readOnly ? <span className="pill" data-testid="verify-read-only">{t(lang, "readOnly")}</span> : undefined}>
      <dl className="kv">
        <dt>{t(lang, "trustDirLabel")}</dt><dd><code data-testid="trust-dir">{trust}</code></dd>
        <dt>{t(lang, "outboxLabel")}</dt><dd><code>{outbox}</code></dd>
      </dl>
      <details data-testid="verify-how">
        <summary>{t(lang, "forTechnicalStaff")} — {t(lang, "howToVerify")}</summary>
        <p>{t(lang, "verifySteps")}</p>
        <VerifyCommand command={`bayan-verify ${outbox}/<release dir> --trust ${trust} --assert-offline --strict`} lang={lang}/>
        <VerifyCommand command={`bayan-verify pack ${outbox}/<evidence pack dir> --trust ${trust} --assert-offline`} lang={lang}/>
      </details>
    </Section>);
}
