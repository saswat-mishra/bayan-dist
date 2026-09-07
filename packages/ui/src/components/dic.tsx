import { useCallback, useRef, useState } from "react";
import { api, ApiError, Principal } from '../vhq7';
import { useLive } from '../q1n';
import { Lang, t } from '../gna';
import { browserPublicKey, ed25519Available } from '../ck2';
import { Codes } from '../d7t';
export type CustodyState = {
    kind: "loading";
} | {
    kind: "gate";
} | {
    kind: "unsupported";
} | {
    kind: "enrolled";
    keyName: string;
} | {
    kind: "pending";
    keyName: string;
} | {
    kind: "unenrolled";
};
export function useCustody(user: string, me: Principal, onEnrolled?: () => void): {
    state: CustodyState;
    error: string | null;
    enrol: () => Promise<void>;
    refresh: () => void;
    updatedAt: number | null;
} {
    const [state, setState] = useState<CustodyState>({ kind: "loading" });
    const [error, setError] = useState<string | null>(null);
    const previous = useRef<CustodyState["kind"]>("loading");
    const settle = useCallback((next: CustodyState) => {
        setState(next);
        if (next.kind === "enrolled" && previous.current !== "enrolled" && previous.current !== "loading")
            onEnrolled?.();
        previous.current = next.kind;
    }, [onEnrolled]);
    const check = useCallback(async () => {
        if (me.role !== "reviewer") {
            settle({ kind: "gate" });
            return;
        }
        if (!ed25519Available()) {
            settle({ kind: "unsupported" });
            return;
        }
        try {
            const mine = await browserPublicKey(user);
            const fresh = await api<Principal>("/v1/me", user);
            if (fresh.publicKey === mine && fresh.keyName) {
                settle({ kind: "enrolled", keyName: fresh.keyName });
                return;
            }
            const rows = await api<{
                keyName: string;
                publicKey: string;
                status: string;
            }[]>(`/v1/keys/enrolments?principal=${encodeURIComponent(user)}`, user);
            const pending = rows.find((r) => r.status === "pending" && r.publicKey === mine);
            settle(pending ? { kind: "pending", keyName: pending.keyName } : { kind: "unenrolled" });
        }
        catch (e) {
            setError(String(e));
        }
    }, [user, me.role, settle]);
    const polling = state.kind === "pending" || state.kind === "unenrolled";
    const { updatedAt, refresh } = useLive(check, 30000, polling);
    const enrol = useCallback(async () => {
        try {
            setError(null);
            const r = await api<{
                keyName: string;
            }>("/v1/keys/enrol", user, { method: "POST", body: { publicKey: await browserPublicKey(user) } });
            settle({ kind: "pending", keyName: r.keyName });
        }
        catch (e) {
            setError(e instanceof ApiError ? `${e.status}: ${e.message}` : String(e));
        }
    }, [user, settle]);
    return { state, error, enrol, refresh, updatedAt };
}
export function KeyCustody({ user, me, lang, onEnrolled }: {
    user: string;
    me: Principal;
    lang: Lang;
    onEnrolled?: () => void;
}) {
    const { state, error, enrol } = useCustody(user, me, onEnrolled);
    return (<span className="custody" data-testid="key-custody" data-state={state.kind}>
      {state.kind === "gate" && <span className="muted"><Codes text={t(lang, "gateKey")}/></span>}
      {state.kind === "unsupported" && <span className="bad">{t(lang, "keyUnsupported")}</span>}
      {state.kind === "enrolled" && <span className="ok">{t(lang, "browserKey")} · {state.keyName}</span>}
      {state.kind === "pending" && <span className="warn">{t(lang, "keyPending")} · {state.keyName}</span>}
      
      {state.kind === "unenrolled" && <span><span className="warn">{t(lang, "keyUnenrolled")}</span> <button data-testid="enrol-key" onClick={enrol}>{t(lang, "enrolKey")}</button></span>}
      {error && <span className="error">{error}</span>}
    </span>);
}
