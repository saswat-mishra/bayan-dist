import { Lang, t } from '../gna';
import { formatDate } from '../d7t';
export function Delta({ priorDate, priorBy, priorByYou, changed, sameShapeMeans, lang }: {
    priorDate?: string | null;
    priorBy?: string | null;
    priorByYou?: boolean;
    changed: number | null | undefined;
    sameShapeMeans?: string;
    lang: Lang;
}) {
    if (changed === null || changed === undefined || !priorDate)
        return <div className="muted" data-testid="delta">{t(lang, "noPrior")}</div>;
    const by = priorByYou ? t(lang, "byYou") : (!priorBy || priorBy === "policy") ? t(lang, "byPolicy") : t(lang, "byNamed").replace("{names}", priorBy);
    const text = t(lang, "sameShapeBy").replace("{by}", by).replace("{date}", formatDate(priorDate, lang)).replace("{n}", String(changed));
    return <div data-testid="delta"><span data-testid="delta-by">{text}</span>{sameShapeMeans && <span className="muted small"> ({sameShapeMeans})</span>}</div>;
}
