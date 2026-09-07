import { useCallback, useEffect, useState } from "react";
import { api, ApiError, Principal } from '../vhq7';
import { Lang, t } from '../gna';
import { browserPublicKey, ed25519Available } from '../ck2';
type State = {
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
export function KeyCustody({ user, me, lang, onEnrolled }: {
    user: string;
    me: Principal;
    lang: Lang;
    onEnrolled?: () => void;
}) {
    const [state, setState] = useState<State>({ kind: "loading" });
    const [error, setError] = useState<string | null>(null);
    const check = useCallback(async () => {
        if (me.role !== "reviewer") {
            setState({ kind: "gate" });
            return;
        }
        if (!ed25519Available()) {
            setState({ kind: "unsupported" });
            return;
        }
        try {
            const mine = await browserPublicKey(user);
            if (me.publicKey === mine && me.keyName) {
                setState({ kind: "enrolled", keyName: me.keyName });
                return;
            }
            const rows = await api<{
                keyName: string;
                publicKey: string;
                status: string;
            }[]>(`/v1/keys/enrolments?principal=${encodeURIComponent(user)}`, user);
            const pending = rows.find((r) => r.status === "pending" && r.publicKey === mine);
            setState(pending ? { kind: "pending", keyName: pending.keyName } : { kind: "unenrolled" });
        }
        catch (e) {
            setError(String(e));
        }
    }, [user, me]);
    useEffect(() => { check(); }, [check]);
    async function enrol() {
        try {
            setError(null);
            const r = await api<{
                keyName: string;
            }>("/v1/keys/enrol", user, { method: "POST", body: { publicKey: await browserPublicKey(user) } });
            setState({ kind: "pending", keyName: r.keyName });
            onEnrolled?.();
        }
        catch (e) {
            setError(e instanceof ApiError ? `${e.status}: ${e.message}` : String(e));
        }
    }
    return (<span className="custody" data-testid="key-custody" data-state={state.kind}>
      {state.kind === "gate" && <span className="muted">{t(lang, "gateKey")}</span>}
      {state.kind === "unsupported" && <span className="bad">{t(lang, "keyUnsupported")}</span>}
      {state.kind === "enrolled" && <span className="ok">{t(lang, "browserKey")} · {state.keyName}</span>}
      {state.kind === "pending" && <span className="warn">{t(lang, "keyPending")} · {state.keyName}</span>}
      {state.kind === "unenrolled" && <span><span className="bad">{t(lang, "keyUnenrolled")}</span> <button data-testid="enrol-key" onClick={enrol}>{t(lang, "enrolKey")}</button></span>}
      {error && <span className="error">{error}</span>}
    </span>);
}
