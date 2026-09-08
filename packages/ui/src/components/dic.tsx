import { useCallback, useRef, useState } from "react";
import { api, ApiError, Principal } from '../vhq7';
import { useLive } from '../q1n';
import { Lang, t } from '../gna';
import { browserPublicKey, ed25519Available } from '../ck2';
import { StateChip } from './drm';
import type { ChipKind } from './drm';
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
export interface CustodyHandle {
    state: CustodyState;
    error: string | null;
    enrol: () => Promise<void>;
    refresh: () => void;
    updatedAt: number | null;
}
export function useCustody(user: string, me: Principal | null, onEnrolled?: () => void): CustodyHandle {
    const [state, setState] = useState<CustodyState>({ kind: "loading" });
    const [error, setError] = useState<string | null>(null);
    const previous = useRef<CustodyState["kind"]>("loading");
    const settle = useCallback((next: CustodyState) => {
        setState(next);
        if (next.kind === "enrolled" && previous.current !== "enrolled" && previous.current !== "loading")
            onEnrolled?.();
        previous.current = next.kind;
    }, [onEnrolled]);
    const role = me?.role ?? null;
    const check = useCallback(async () => {
        if (role === null)
            return;
        if (role !== "reviewer") {
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
    }, [user, role, settle]);
    const polling = state.kind === "pending" || state.kind === "unenrolled";
    const { updatedAt, refresh } = useLive(check, 30000, polling);
    const enrol = useCallback(async () => {
        try {
            setError(null);
            const r = await api<{
                keyName: string;
            }>("/v1/keys/enrol", user, { method: "POST", body: { publicKey: await browserPublicKey(user) } });
            settle({ kind: "pending", keyName: r.keyName });
            refresh();
        }
        catch (e) {
            setError(e instanceof ApiError ? `${e.status}: ${e.message}` : String(e));
        }
    }, [user, settle, refresh]);
    return { state, error, enrol, refresh, updatedAt };
}
const CHIP: Record<CustodyState["kind"], ChipKind | null> = { loading: null, gate: "gate", unsupported: "unsupported", enrolled: "enrolled", pending: "key-pending", unenrolled: "unenrolled" };
export function KeyCustody({ custody, lang }: {
    custody: CustodyHandle;
    lang: Lang;
}) {
    const { state, error } = custody;
    const kind = CHIP[state.kind];
    const title = state.kind === "enrolled" ? `${t(lang, "browserKey")} · ${state.keyName}` : state.kind === "pending" ? `${t(lang, "keyPending")} · ${state.keyName}`
        : state.kind === "unenrolled" ? t(lang, "keyUnenrolled") : state.kind === "gate" ? t(lang, "gateKey") : state.kind === "unsupported" ? t(lang, "keyUnsupported") : "";
    return (<span className="custody" data-testid="key-custody" data-state={state.kind} data-key={state.kind === "enrolled" || state.kind === "pending" ? state.keyName : undefined}>
      {kind && <StateChip kind={kind} lang={lang} title={title} testid="custody-chip"/>}
      {error && <span className="error">{error}</span>}
    </span>);
}
