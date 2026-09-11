import type { FeasRow, Skill } from '../wz0g';
export interface Match {
    question: string;
    score: number;
    because: string[];
}
const ARABIC = /[؀-ۿ]/;
export function normalise(s: string): string {
    return s.toLowerCase()
        .replace(/[ً-ْـٰ]/g, "")
        .replace(/[أإآٱ]/g, "ا").replace(/ى/g, "ي").replace(/ؤ/g, "و").replace(/ئ/g, "ي").replace(/ة/g, "ه")
        .replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}
const EN_SUFFIX = /(ational|ings|ing|ies|ers|er|ed|es|ly|al|s|e)$/;
const AR_PREFIX = /^(بال|وال|كال|فال|ال|لل)/;
const AR_SUFFIX = /(ات|ون|ين|ها|هم|هن|يه|ه)$/;
export function stem(w: string): string {
    let x = w;
    if (ARABIC.test(w)) {
        const p = x.replace(AR_PREFIX, "");
        if (p.length >= 3)
            x = p;
        const s = x.replace(AR_SUFFIX, "");
        return s.length >= 3 ? s : x;
    }
    for (let i = 0; i < 4; i++) {
        const y = x.replace(EN_SUFFIX, (m) => (m === "ies" ? "y" : ""));
        if (y === x || y.length < 3)
            break;
        x = y;
    }
    return x;
}
const STOP = new Set([
    "the", "a", "an", "and", "or", "but", "not", "no", "of", "in", "on", "at", "to", "for", "from", "by", "with", "as",
    "is", "are", "was", "were", "be", "been", "am", "do", "does", "did", "done", "has", "have", "had", "can", "could",
    "will", "would", "should", "may", "might", "must", "this", "that", "these", "those", "it", "its", "there", "here",
    "what", "which", "who", "whom", "whose", "why", "how", "when", "where", "if", "then", "than", "so", "such", "since",
    "while", "about", "into", "over", "under", "out", "up", "down", "again", "still", "just", "also", "very", "more",
    "most", "some", "any", "all", "every", "each", "both", "i", "we", "you", "they", "he", "she", "me", "us", "them",
    "my", "our", "your", "their", "his", "her", "am", "get", "got", "give", "gives", "show", "shows", "tell", "please",
    "من", "في", "علي", "عن", "الي", "مع", "هل", "ما", "ماذا", "لماذا", "كيف", "متي", "اين", "هذا", "هذه", "ذلك", "تلك",
    "التي", "الذي", "الذين", "و", "او", "ثم", "قد", "كان", "كانت", "هو", "هي", "هم", "هن", "كل", "بعد", "قبل", "عند",
    "منذ", "لا", "لم", "لن", "ان", "اي", "بين", "حتي", "لدي", "نحن", "انت", "انا",
]);
export function terms(s: string): string[] {
    const out: string[] = [];
    for (const w of normalise(s).split(" ")) {
        if (STOP.has(w))
            continue;
        const k = stem(w);
        if (k.length >= 2 && !STOP.has(k) && !out.includes(k))
            out.push(k);
    }
    return out;
}
const WEIGHT = { text: 3, minclass: 2, skill: 2, name: 1.5 } as const;
type Field = keyof typeof WEIGHT;
export interface Index {
    rows: FeasRow[];
    byQuestion: Map<string, Map<Field, Set<string>>>;
}
export function buildIndex(rows: FeasRow[], skills: Skill[]): Index {
    const byQuestion = new Map<string, Map<Field, Set<string>>>();
    for (const r of rows) {
        const f = new Map<Field, Set<string>>([["text", new Set()], ["minclass", new Set()], ["skill", new Set()], ["name", new Set()]]);
        for (const k of terms(`${r.text} ${r.text_ar}`))
            f.get("text")!.add(k);
        for (const k of terms(`${r.minClass} ${r.minClass_ar ?? ""} ${r.minClassWords?.en ?? ""} ${r.minClassWords?.ar ?? ""}`))
            f.get("minclass")!.add(k);
        for (const s of skills) {
            if (!s.answers.includes(r.question))
                continue;
            for (const k of terms(`${s.description} ${s.description_ar}`))
                f.get("skill")!.add(k);
            for (const k of terms(`${s.name} ${(s.columns ?? []).map((c) => c.name).join(" ")}`))
                f.get("name")!.add(k);
        }
        byQuestion.set(r.question, f);
    }
    return { rows, byQuestion };
}
export function rank(query: string, index: Index): Match[] {
    const qs = terms(query);
    if (qs.length === 0)
        return [];
    const raw = normalise(query).split(" ").filter(Boolean);
    const rawOf = new Map<string, string>();
    raw.forEach((w) => { const k = stem(w); if (k.length >= 2 && !rawOf.has(k))
        rawOf.set(k, w); });
    const out: Match[] = [];
    for (const r of index.rows) {
        const fields = index.byQuestion.get(r.question);
        if (!fields)
            continue;
        let score = 0;
        const because: string[] = [];
        for (const k of qs) {
            let best = 0;
            for (const [field, set] of fields)
                if (set.has(k))
                    best = Math.max(best, WEIGHT[field]);
            if (best > 0) {
                score += best;
                const word = rawOf.get(k) ?? k;
                if (!because.includes(word))
                    because.push(word);
            }
        }
        if (score > 0)
            out.push({ question: r.question, score, because: because.slice(0, 4) });
    }
    const order = new Map(index.rows.map((r, i) => [r.question, i]));
    const priced = new Map(index.rows.map((r) => [r.question, r.blocked ? 2 : r.achievableD === null ? 1 : 0]));
    return out.sort((a, b) => b.score - a.score || priced.get(a.question)! - priced.get(b.question)! || order.get(a.question)! - order.get(b.question)!);
}
export const FLOOR = 3;
export function confident(ms: Match[]): Match[] { return ms.filter((m) => m.score >= FLOOR); }
