import { Lang, t } from '../gna';
import { Iso } from '../d7t';
export function ControlsTable({ controls, lang, titles }: {
    controls: Record<string, string[]>;
    lang: Lang;
    titles?: Record<string, {
        en: string;
        ar: string;
    }>;
}) {
    const rows = Object.entries(controls);
    if (rows.length === 0)
        return null;
    const title = (fw: string) => (lang === "ar" ? titles?.[fw]?.ar : titles?.[fw]?.en) || titles?.[fw]?.en || fw;
    return (<table className="controls" data-testid="controls-table">
      <caption>{t(lang, "controls")}</caption>
      <tbody>{rows.map(([fw, ids]) => <tr key={fw}><th scope="row" title={fw}><Iso>{title(fw)}</Iso></th><td>{ids.map((id) => <span key={id} className="pill" data-testid={`control-chip-${id}`}><Iso>{id}</Iso></span>)}</td></tr>)}</tbody>
    </table>);
}
