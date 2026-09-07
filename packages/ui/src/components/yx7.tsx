import type { Certificate } from '../wz0g';
import { Lang, t } from '../gna';
import { CertificateBody } from './xsd';
export function CertificateCard({ cert, lang, micros }: {
    cert: Certificate;
    lang: Lang;
    micros?: number;
}) {
    return (<div className="card" data-testid="certificate">
      <h2>{t(lang, "certificate")}</h2>
      <CertificateBody cert={cert} lang={lang} micros={micros}/>
    </div>);
}
