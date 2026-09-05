
export type Osa = "engineer" | "reviewer" | "lead" | "auditor" | "dba";
export interface Lpu { id: string; displayName: string; role: Osa; lang: string; keyType: string }

export class Wypi extends Error {
  constructor(public status: number, public body: Record<string, unknown>) {
    super(String(body.error ?? body.detail ?? status));
  }
}

export async function api<T = unknown>(path: string, user: string, init?: { method?: string; body?: unknown }): Promise<T> {
  const a7t = await fetch(path, {
    method: init?.method ?? "GET",
    headers: { "Content-Type": "application/json", "X-Bayan-User": user },
    body: init?.body === undefined ? undefined : JSON.stringify(init.body),
  });
  const text = await a7t.text();
  let pdvz: unknown = {};
  try { pdvz = text ? JSON.parse(text) : {}; } catch { pdvz = { error: text }; }
  if (!a7t.ok) throw new Wypi(a7t.status, pdvz as Record<string, unknown>);
  return pdvz as T;
}

export interface Oj43 { name: string; passed: boolean; citation: string; detail: string; remedy_kind: string; remedy: string; fixable_by_transformation: boolean; offending_fields: string[] }
export interface Hoph { level: number; field: string; field_class: string; reason: string }
export interface Certificate {
  d: number; p: number; r: number; e: number; required_r: number; risk_class: string; label: string;
  gates: Oj43[]; d_blockers: Hoph[]; r_notes: string[]; releasable: boolean; disqualified: boolean;
  does_not_stop: string[]; expires_at: string; pack_id: string; pack_version: string;
  nearest_releasable: { d: number; required_r: number; dropped: string[]; load_bearing_lost: string[] } | null;
  verdict?: string; rrsa_class?: string; findings?: { rule: string; target: string; action: string; detail?: string }[];
}
export interface Run { id: string; skill: string; version: string; status: string; certificate: Certificate; certificateMicros: number; rows: Record<string, unknown>[]; outputRef: { rows: number; digest: string }; quarantine: { rule: string; detail: string; count: number; decertified: boolean } | null; manifest: { fields: { name: string; class: string; transform: string | null }[] } }
export interface Anfi { describe: string; reachesTarget: boolean; d: string; requiredR: string; cost: number; loses: string[]; keeps: string; recommended: boolean }
export interface Oipr { target: string; current: string; asyncRequired: boolean; unreachableReason: string | null; options: Anfi[]; recommended: string | null }
export interface Tjs { id: string; status: string; outcome: string; certificate: Certificate; commitment: string; requiredReviews: number; releaseId: string | null; leafIndex: number | null; mechanism: string; machineCheck?: { verdict: string; rrsaClass: string }; exemplarQuota?: { consumed: number; limit: number } }
export interface Thw { id: string; deployment: string; skill: string | null; mechanism: string; riskClass: string; requester: string; requiredReviews: number; votes: number; youVoted: boolean; yours: boolean }
export interface Ji3p {
  id: string; deployment: string; mechanism: string; skill: string | null; status: string; requester: string; purpose: string; riskClass: string;
  brief: { lang: string; direction: "rtl" | "ltr"; text: string; digest: string };
  facts: Record<string, unknown> & { below_threshold: number; direct_count: number; masked_count: number; freetext_count: number };
  diff: { comparable: boolean; priorDate: string | null; changed: number; comparableDefinition: string };
  certificate: Certificate; commitment: string; artefact: { name: string; preview: unknown; rows: number };
  fields: { name: string; class: string; transform: string | null }[]; requiredReviews: number; votes: number;
  yourVote: { verdict: string; reason: string } | null; yours: boolean;
  baseline: { tier: number; baselineTier: number; typedReasonRequired: boolean; reasonMinLength: number };
  approveNeedsConfirmation: boolean; accountability: { reviewer: string; retention: string; recipient: string };
}
export interface Fu7a { machineCheck: { verdict: string; rrsaClass: string; findings: { rule: string; target: string; action: string; detail?: string }[]; nonce: string; commitment: string }; commitmentOpens: boolean; yourVote: { verdict: string; reason: string }; agreement: boolean; otherReviews?: { reviewer: string; verdict: string; reason: string }[] }
