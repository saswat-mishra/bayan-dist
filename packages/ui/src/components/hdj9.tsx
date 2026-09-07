import { useEffect, useState } from "react";
import { Lang, t } from '../gna';
export function ReadAloud({ text, lang, textLang }: {
    text: string;
    lang: Lang;
    textLang: string;
}) {
    const [speaking, setSpeaking] = useState(false);
    const supported = typeof window !== "undefined" && "speechSynthesis" in window && typeof SpeechSynthesisUtterance !== "undefined";
    useEffect(() => () => { if (supported)
        window.speechSynthesis.cancel(); }, [supported]);
    if (!supported)
        return null;
    function toggle() {
        if (speaking) {
            window.speechSynthesis.cancel();
            setSpeaking(false);
            return;
        }
        const u = new SpeechSynthesisUtterance(text);
        u.lang = textLang.startsWith("ar") ? "ar" : "en";
        u.onend = () => setSpeaking(false);
        u.onerror = () => setSpeaking(false);
        setSpeaking(true);
        window.speechSynthesis.speak(u);
    }
    return (<button type="button" onClick={toggle} data-testid="read-aloud" aria-pressed={speaking} title={t(lang, "readAloudNote")}>
      {speaking ? t(lang, "stopReading") : t(lang, "readAloud")} <span className="muted small">({t(lang, "readAloudNote")})</span>
    </button>);
}
