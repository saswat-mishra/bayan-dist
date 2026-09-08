import { useEffect, useState } from "react";
import type { RefObject } from "react";
import { Lang } from '../../gna';
import type { HeadlineJson } from '../../wz0g';
import { StateChip } from '../../components/drm';
import { Runs } from '../../d7t';
import { Segments } from './zf6u';
type Choice = null | "reject" | "approve";
const SAFE = "(min-width: 900px) and (min-height: 700px)";
function useSafeViewport(force?: boolean): boolean {
    const [ok, setOk] = useState(() => !!force || (typeof window !== "undefined" && typeof window.matchMedia === "function" && window.matchMedia(SAFE).matches));
    useEffect(() => {
        if (force || typeof window === "undefined" || typeof window.matchMedia !== "function")
            return;
        const mq = window.matchMedia(SAFE);
        const on = () => setOk(mq.matches);
        mq.addEventListener("change", on);
        return () => mq.removeEventListener("change", on);
    }, [force]);
    return ok;
}
export function DecisionBar({ kind, title, lang, choice, onChoose, controlRef, technicalRef, force }: {
    kind: HeadlineJson["kind"];
    title: string;
    lang: Lang;
    choice: Choice;
    onChoose: (c: Choice) => void;
    controlRef: RefObject<HTMLElement>;
    technicalRef?: RefObject<HTMLDetailsElement>;
    force?: boolean;
}) {
    const safeMedia = useSafeViewport(force);
    const safe = !!force || safeMedia;
    const [controlVisible, setControlVisible] = useState(true);
    const [technicalVisible, setTechnicalVisible] = useState(false);
    useEffect(() => {
        const el = controlRef.current;
        if (!el || typeof IntersectionObserver === "undefined")
            return;
        const io = new IntersectionObserver(([e]) => setControlVisible(e.isIntersecting));
        io.observe(el);
        return () => io.disconnect();
    }, [controlRef, safe]);
    useEffect(() => {
        const el = technicalRef?.current as HTMLDetailsElement | null | undefined;
        if (!el || typeof IntersectionObserver === "undefined")
            return;
        let intersecting = false;
        const io = new IntersectionObserver(([e]) => { intersecting = e.isIntersecting; setTechnicalVisible(intersecting && el.open); });
        const onToggle = () => setTechnicalVisible(intersecting && el.open);
        io.observe(el);
        el.addEventListener("toggle", onToggle);
        return () => { io.disconnect(); el.removeEventListener("toggle", onToggle); };
    }, [technicalRef, safe]);
    if (!safe)
        return null;
    const hidden = force ? false : controlVisible || technicalVisible;
    const choose = (c: Choice) => { onChoose(c); controlRef.current?.scrollIntoView({ block: "center", behavior: "smooth" }); };
    return (<div className="decision-bar no-print" data-testid="decision-bar" aria-hidden={hidden} data-hidden={hidden}>
      <StateChip kind={kind} lang={lang}/>
      <span className="title"><Runs text={title}/></span>
      <Segments choice={choice} onChoose={choose} lang={lang} idPrefix="bar-"/>
    </div>);
}
