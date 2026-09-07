export function canonicalJson(value: unknown): string {
    if (value === null || typeof value === "boolean" || typeof value === "string")
        return JSON.stringify(value);
    if (typeof value === "number") {
        if (!Number.isFinite(value))
            throw new Error("canonical JSON has no NaN/Infinity");
        return Number.isInteger(value) ? String(value) : JSON.stringify(value);
    }
    if (Array.isArray(value))
        return "[" + value.map(canonicalJson).join(",") + "]";
    if (typeof value === "object") {
        const o = value as Record<string, unknown>;
        return "{" + Object.keys(o).sort().map((k) => JSON.stringify(k) + ":" + canonicalJson(o[k])).join(",") + "}";
    }
    throw new Error(`cannot canonicalise a ${typeof value}`);
}
export interface VoteFields {
    request: string;
    reviewer: string;
    verdict: string;
    reason: string;
    presentedDigest: string;
    lang: string;
    at: string;
}
export const votePayload = (f: VoteFields): Uint8Array => new TextEncoder().encode(canonicalJson(f));
export interface Signer {
    keyName: string | null;
    sign(payload: Uint8Array): Promise<string>;
}
export const b64 = (bytes: ArrayBuffer | Uint8Array): string => btoa(String.fromCharCode(...new Uint8Array(bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes))));
export const nowIso = (): string => new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const DB = "bayan-keys", STORE = "keys";
function openDb(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
        const req = indexedDB.open(DB, 1);
        req.onupgradeneeded = () => req.result.createObjectStore(STORE);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });
}
function idb<T>(mode: IDBTransactionMode, op: (s: IDBObjectStore) => IDBRequest<T>): Promise<T> {
    return openDb().then((db) => new Promise<T>((resolve, reject) => {
        const r = op(db.transaction(STORE, mode).objectStore(STORE));
        r.onsuccess = () => resolve(r.result);
        r.onerror = () => reject(r.error);
    }));
}
export async function browserKeyPair(user: string): Promise<CryptoKeyPair> {
    const existing = await idb<CryptoKeyPair | undefined>("readonly", (s) => s.get(user) as IDBRequest<CryptoKeyPair | undefined>);
    if (existing)
        return existing;
    const pair = (await crypto.subtle.generateKey({ name: "Ed25519" }, false, ["sign", "verify"])) as CryptoKeyPair;
    await idb("readwrite", (s) => s.put(pair, user));
    return pair;
}
export async function browserPublicKey(user: string): Promise<string> {
    const pair = await browserKeyPair(user);
    return b64(await crypto.subtle.exportKey("raw", pair.publicKey));
}
export function browserSigner(user: string, keyName: string | null): Signer {
    return {
        keyName,
        async sign(payload: Uint8Array): Promise<string> {
            const pair = await browserKeyPair(user);
            return b64(await crypto.subtle.sign({ name: "Ed25519" }, pair.privateKey, payload as BufferSource));
        },
    };
}
export const ed25519Available = (): boolean => typeof crypto !== "undefined" && !!crypto.subtle && typeof indexedDB !== "undefined";
