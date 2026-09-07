import { useCallback, useEffect, useRef, useState } from "react";
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
export function useLive(load: () => Promise<unknown> | void, intervalMs: number, enabled = true): {
    updatedAt: number | null;
    refresh: () => void;
} {
    const [updatedAt, setUpdatedAt] = useState<number | null>(null);
    const inFlight = useRef(false);
    const refresh = useCallback(() => {
        if (inFlight.current)
            return;
        inFlight.current = true;
        const done = () => { inFlight.current = false; setUpdatedAt(Date.now()); };
        Promise.resolve().then(() => load()).then(done, done);
    }, [load]);
    useEffect(() => {
        refresh();
        if (!enabled)
            return;
        const visible = () => typeof document === "undefined" || document.visibilityState !== "hidden";
        const tick = () => { if (visible())
            refresh(); };
        const id = setInterval(tick, intervalMs);
        document.addEventListener("visibilitychange", tick);
        window.addEventListener("focus", tick);
        return () => { clearInterval(id); document.removeEventListener("visibilitychange", tick); window.removeEventListener("focus", tick); };
    }, [refresh, intervalMs, enabled]);
    return { updatedAt, refresh };
}
export function useTicker(everyMs = 5000): number {
    const [now, setNow] = useState(() => Date.now());
    useEffect(() => { const id = setInterval(() => setNow(Date.now()), everyMs); return () => clearInterval(id); }, [everyMs]);
    return now;
}
export const ago = (seconds: number, lang: Lang): string => {
    const h = Math.floor(seconds / 3600), m = Math.floor((seconds % 3600) / 60);
    if (h >= 48)
        return lang === "ar" ? `${Math.floor(h / 24)} يوم` : `${Math.floor(h / 24)} d`;
    if (h >= 1)
        return lang === "ar" ? `${h} س ${m} د` : `${h} h ${m} m`;
    return lang === "ar" ? `${m} د` : `${m} m`;
};
