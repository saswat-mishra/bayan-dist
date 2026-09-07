export type { Principal, Role, Certificate, Gate, Blocker, Run, UpliftOption, UpliftMenu, ReleaseRequest, QueueItem, Brief, Reveal } from './wz0g';
export class ApiError extends Error {
    constructor(public status: number, public body: Record<string, unknown>) {
        super(String(body.error ?? body.detail ?? status));
    }
}
export async function api<T = unknown>(path: string, user: string, init?: {
    method?: string;
    body?: unknown;
}): Promise<T> {
    const res = await fetch(path, {
        method: init?.method ?? "GET",
        headers: { "Content-Type": "application/json", "X-Bayan-User": user },
        body: init?.body === undefined ? undefined : JSON.stringify(init.body),
    });
    const text = await res.text();
    let parsed: unknown = {};
    try {
        parsed = text ? JSON.parse(text) : {};
    }
    catch {
        parsed = { error: text };
    }
    if (!res.ok)
        throw new ApiError(res.status, parsed as Record<string, unknown>);
    return parsed as T;
}
