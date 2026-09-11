import { useMemo, useRef, useState } from "react";
import { Lang, t } from '../gna';
import type { AskAnswer, AssistantView, FeasRow, Skill } from '../wz0g';
import { Match, buildIndex, confident, rank } from './hmb';
import { Iso } from '../d7t';
export interface AskResult {
    query: string;
    matches: Match[];
    mode: "model" | "words";
    why?: string;
    model?: string;
    fellBack?: boolean;
}
export type AskModel = (text: string, lang: Lang) => Promise<AskAnswer | null>;
export function AskBox({ rows, skills, lang, result, onResult, assistant, askModel }: {
    rows: FeasRow[];
    skills: Skill[];
    lang: Lang;
    result: AskResult | null;
    onResult: (r: AskResult | null) => void;
    assistant?: AssistantView | null;
    askModel?: AskModel;
}) {
    const [text, setText] = useState("");
    const [busy, setBusy] = useState(false);
    const index = useMemo(() => buildIndex(rows, skills), [rows, skills]);
    const inputRef = useRef<HTMLInputElement>(null);
    const textOf = (q: string) => { const r = rows.find((x) => x.question === q); return r ? (lang === "ar" ? r.text_ar : r.text) : q; };
    const modelReady = !!assistant?.ready && !!askModel;
    async function submit(e: React.FormEvent) {
        e.preventDefault();
        const q = text.trim();
        if (!q)
            return;
        const words = (fellBack: boolean) => onResult({ query: q, matches: confident(rank(q, index)), mode: "words", fellBack });
        if (!modelReady) {
            words(false);
            return;
        }
        setBusy(true);
        try {
            const a = await askModel!(q, lang);
            if (a && a.mode === "model") {
                const ids = new Set(rows.map((r) => r.question));
                const matches: Match[] = [];
                if (a.question && ids.has(a.question))
                    matches.push({ question: a.question, score: 100, because: [] });
                for (const x of a.also ?? [])
                    if (ids.has(x) && x !== a.question)
                        matches.push({ question: x, score: 50, because: [] });
                onResult({ query: q, matches, mode: "model", why: a.why, model: a.model });
            }
            else
                words(true);
        }
        catch {
            words(true);
        }
        finally {
            setBusy(false);
        }
    }
    function clear() {
        setText("");
        onResult(null);
        inputRef.current?.focus();
    }
    const top = result?.matches[0] ?? null;
    const also = (result?.matches ?? []).slice(1, 3);
    return (<form className="askbox" onSubmit={submit} data-testid="askbox" data-mode={modelReady ? "model" : "words"} aria-busy={busy || undefined}>
      <label htmlFor="ask-input">{t(lang, "askInYourWords")}</label>
      <div className="askbox-row">
        <input id="ask-input" ref={inputRef} value={text} onChange={(e) => setText(e.target.value)} placeholder={t(lang, "askPlaceholder")} autoComplete="off" data-testid="ask-input" disabled={busy}/>
        <button type="submit" className="primary" disabled={!text.trim() || busy} data-testid="ask-submit">{busy ? t(lang, "askThinking") : t(lang, "askFind")}</button>
        {result && <button type="button" className="ghost" onClick={clear} data-testid="ask-clear">{t(lang, "askClear")}</button>}
      </div>
      <p className="muted small ask-how" data-testid="ask-how">
        {modelReady ? t(lang, "askModelHow").split("{endpoint}").map((part, i, all) => <span key={i}>{part}{i < all.length - 1 && <Iso>{assistant?.endpoint ?? ""}</Iso>}</span>) : t(lang, "askHowItWorks")}
        {!modelReady && assistant !== undefined && <> <a href="#/integrations" data-testid="ask-connect-hint">{t(lang, "askConnectHint")}</a></>}
      </p>
      {result && (<div className="ask-result" role="status" data-testid="ask-result" data-mode={result.mode}>
          {result.fellBack && <p className="muted small" data-testid="ask-fell-back">{t(lang, "askFellBack")}</p>}
          {top ? (<>
              <p className="ask-best" data-testid="ask-best">
                <strong>{t(lang, "askBest")}:</strong> {textOf(top.question)}
                {result.mode === "model"
                    ? <span className="muted"> · {t(lang, "askByModel")}{result.why ? `: ${result.why}` : ""}</span>
                    : <span className="muted"> · {t(lang, "askWhyMatched")} {top.because.join(", ")}</span>}
              </p>
              {also.length > 0 && (<p className="muted small" data-testid="ask-also">{t(lang, "askAlso")}: {also.map((m) => textOf(m.question)).join(" · ")}</p>)}
            </>) : <p data-testid="ask-nomatch">{result.mode === "model" && result.why ? result.why : t(lang, "askNoMatch")}</p>}
        </div>)}
    </form>);
}
