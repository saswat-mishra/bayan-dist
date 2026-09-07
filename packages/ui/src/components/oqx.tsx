import { Lang, t } from '../gna';
export function ControlsTable({ controls, lang }: {
    controls: Record<string, string[]>;
    lang: Lang;
}) {
    const rows = Object.entries(controls);
    if (rows.length === 0)
        return null;
    return (<table className="controls" data-testid="controls-table">
      <caption>{t(lang, "controls")}</caption>
      <tbody>{rows.map(([fw, ids]) => <tr key={fw}><th scope="row">{fw}</th><td>{ids.join(", ")}</td></tr>)}</tbody>
    </table>);
}
