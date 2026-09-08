import { Lang, t } from './gna';
import type { Recommendation, UpliftOption } from './wz0g';
export function pathWordsFor(requiredR: string, lang: Lang): string {
    return requiredR === "R1" || requiredR === "R0" ? t(lang, "pathNoReviewer") : requiredR === "R2" ? t(lang, "pathOneReviewer") : t(lang, "pathTwoReviewers");
}
export function changeWords(changes: Recommendation["changes"], lang: Lang, detail = false): string {
    return changes.map((c) => {
        if (c.transform === "hmac_enclave")
            return `${t(lang, "replaceWith")} ${c.field} ${t(lang, "withPseudonyms")}${detail ? ` — ${t(lang, "keepsRanking")}` : ""}`;
        if (c.transform === "drop")
            return `${t(lang, "dropField")} ${c.field}`;
        if (c.transform === "bucket")
            return `${t(lang, "bucketField")} ${c.field}`;
        if (c.transform === "coarsen")
            return `${t(lang, "coarsenField")} ${c.field}`;
        return `${c.transform} ${c.field}`;
    }).join("; ");
}
export function recommendationWords(rec: Pick<Recommendation, "changes" | "requiredR">, lang: Lang): string {
    return `${changeWords(rec.changes, lang)} ${t(lang, "arrow")} ${t(lang, "releasesWith")} ${pathWordsFor(rec.requiredR, lang)}`;
}
export function describeOption(o: UpliftOption, lang: Lang): string {
    return `${changeWords(o.changes, lang, true)} ${t(lang, "arrow")} ${t(lang, "releasesWith")} ${pathWordsFor(o.requiredR, lang)} (${o.d})`;
}
export function primaryAction(rec: Recommendation | null | undefined): "improve" | "request" {
    return rec && rec.reachesTarget ? "improve" : "request";
}
