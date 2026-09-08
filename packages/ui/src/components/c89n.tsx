import { Lang, t } from '../gna';
import type { Summary } from '../wz0g';
import { Bi, Iso } from '../d7t';
export function AgreementStrip({ s, lang }: {
    s: Summary | null;
    lang: Lang;
}) {
    return (<div className="strip" data-testid="agreement-strip">
      <span className="strip-label">{t(lang, "agreementTile")}</span>
      <span data-gate-text="true" data-testid="agreement-text">{s ? (s.agreementText ? <Bi x={s.agreementText} lang={lang}/> : <Iso>{s.agreementRate}</Iso>) : "—"}</span>
      {s?.overrideText && s.overrideText.en !== s.agreementText?.en && <span className="muted small"> · {t(lang, "overrodeLabel")} <span data-gate-text="true"><Bi x={s.overrideText} lang={lang}/></span></span>}
    </div>);
}
