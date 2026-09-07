import { useCallback, useEffect, useState } from "react";
import { explain } from './x27r';
import type { Lang } from './gna';
export function usePersisted(key: string, initial: string): [
    string,
    (v: string | ((prev: string) => string)) => void
] {
    const [v, setV] = useState<string>(() => { try {
        return localStorage.getItem(key) || initial;
    }
    catch {
        return initial;
    } });
    useEffect(() => { try {
        localStorage.setItem(key, v);
    }
    catch { } }, [key, v]);
    return [v, setV];
}
export function useHash(): string[] {
    const read = () => location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
    const [segs, setSegs] = useState<string[]>(read);
    useEffect(() => { const on = () => setSegs(read()); window.addEventListener("hashchange", on); return () => window.removeEventListener("hashchange", on); }, []);
    return segs;
}
export const go = (path: string) => { location.hash = `#/${path}`; };
export function useGuard(lang: Lang): [
    string | null,
    <T>(p: Promise<T>) => Promise<T | null>,
    (e: string | null) => void
] {
    const [error, setError] = useState<string | null>(null);
    const guard = useCallback(async <T,>(p: Promise<T>): Promise<T | null> => {
        try {
            setError(null);
            return await p;
        }
        catch (e) {
            setError(explain(e, lang));
            return null;
        }
    }, [lang]);
    return [error, guard, setError];
}
export const ago = (seconds: number, lang: Lang): string => {
    const h = Math.floor(seconds / 3600), m = Math.floor((seconds % 3600) / 60);
    if (h >= 48)
        return lang === "ar" ? `${Math.floor(h / 24)} يوم` : `${Math.floor(h / 24)} d`;
    if (h >= 1)
        return lang === "ar" ? `${h} س ${m} د` : `${h} h ${m} m`;
    return lang === "ar" ? `${m} د` : `${m} m`;
};
