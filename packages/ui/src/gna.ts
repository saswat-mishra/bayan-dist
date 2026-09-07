import { en } from './i18n/tdo0';
import { ar } from './i18n/b29';
export type Lang = "en" | "ar";
export type Key = keyof typeof en;
const S: Record<Lang, Record<Key, string>> = { en, ar };
export const t = (lang: Lang, k: Key): string => S[lang][k];
export const pick = (lang: Lang, x: {
    en: string;
    ar: string;
} | null | undefined): string => (x ? (lang === "ar" ? x.ar : x.en) : "");
