import { useCallback, useEffect, useState } from "react";
import { api } from '../../vhq7';
import type { Ctx } from '../../App';
import { useGuard } from '../../q1n';
import { Lang, t } from '../../gna';
import type { AssistantView } from '../../wz0g';
import { Page, Section } from '../../components/gct';
import { Progress } from '../../components/nv8';
import { StateChip } from '../../components/drm';
import { Iso, Name, formatDate } from '../../d7t';
export function statusOf(a: AssistantView | null, lang: Lang): {
    kind: "done" | "pending" | "todo" | "gate";
    text: string;
} {
    if (!a || !a.configured)
        return { kind: "todo", text: t(lang, "intNotConfigured") };
    if (!a.lastCheck)
        return { kind: "pending", text: t(lang, "intUnchecked") };
    return a.lastCheck.ok ? { kind: "done", text: t(lang, "intReady") } : { kind: "gate", text: t(lang, "intUnreachable") };
}
export function Integrations({ ctx }: {
    ctx: Ctx;
}) {
    const { user, lang, dep } = ctx;
    const [view, setView] = useState<AssistantView | null>(null);
    const [endpoint, setEndpoint] = useState("");
    const [model, setModel] = useState("");
    const [busy, setBusy] = useState<"save" | "check" | "disconnect" | null>(null);
    const [error, guard] = useGuard(lang);
    const load = useCallback(() => guard(api<AssistantView>(`/v1/assistant?deployment=${dep}`, user)).then((v) => {
        if (!v)
            return;
        setView(v);
        setEndpoint((e) => e || v.endpoint || "");
        setModel((m) => m || v.model || "");
    }), [dep, user, guard]);
    useEffect(() => { load(); }, [load]);
    async function save() {
        setBusy("save");
        const v = await guard(api<AssistantView>("/v1/assistant", user, { method: "POST", body: { deployment: dep, endpoint, model } }));
        setBusy(null);
        if (v) {
            setView(v);
            await check();
        }
    }
    async function check() {
        setBusy("check");
        const v = await guard(api<AssistantView>("/v1/assistant/check", user, { method: "POST", body: { deployment: dep } }));
        setBusy(null);
        if (v)
            setView(v);
    }
    async function disconnect() {
        setBusy("disconnect");
        const v = await guard(api<AssistantView>("/v1/assistant/disconnect", user, { method: "POST", body: { deployment: dep } }));
        setBusy(null);
        if (v) {
            setView(v);
            setEndpoint("");
            setModel("");
        }
    }
    const st = statusOf(view, lang);
    const last = view?.lastCheck ?? null;
    const dirty = !!view && (endpoint.trim() !== (view.endpoint ?? "") || model.trim() !== (view.model ?? ""));
    return (<Page title={t(lang, "pageIntegrations")} intro={t(lang, "introIntegrations")} testid="integrations">
      <Section heading={t(lang, "intModelTitle")} purpose={t(lang, "intModelPurpose")} testid="client-model" aside={<StateChip kind={st.kind} lang={lang} testid="model-status" title={st.text}/>}>
        <p className="status-line" data-testid="model-status-line" data-state={st.kind}><strong>{st.text}</strong>
          {view?.configured && view.model && <span className="muted">· <Iso>{view.model}</Iso> {t(lang, "intSetBy")} <Name name={view.setBy ?? ""} lang={lang}/></span>}
        </p>
        {error && <div className="error" role="alert">{error}</div>}
        <div className="form-grid">
          <label>{t(lang, "intEndpoint")}<input value={endpoint} onChange={(e) => setEndpoint(e.target.value)} placeholder="http://127.0.0.1:11434" data-testid="int-endpoint" dir="ltr" autoComplete="off"/></label>
          <label>{t(lang, "intModel")}<input value={model} onChange={(e) => setModel(e.target.value)} placeholder="llama3.1:8b" data-testid="int-model" dir="ltr" autoComplete="off" list="served-models"/>
            {last && last.models.length > 0 && <datalist id="served-models">{last.models.map((m) => <option key={m} value={m}/>)}</datalist>}</label>
        </div>
        <p className="muted small">{t(lang, "intBoundary")}</p>
        <div className="vote">
          <button className="primary" onClick={save} disabled={busy !== null || !endpoint.trim() || !model.trim() || (!!view?.configured && !dirty)} data-testid="int-save">{t(lang, "intSave")}</button>
          <button onClick={check} disabled={busy !== null || !view?.configured || dirty} data-testid="int-check">{t(lang, "intCheck")}</button>
          {view?.configured && <button className="ghost" onClick={disconnect} disabled={busy !== null} data-testid="int-disconnect">{t(lang, "intDisconnect")}</button>}
          {busy && <Progress label={t(lang, "loading")}/>}
        </div>
        {last && (<dl className="kv" data-testid="last-check" data-ok={last.ok}>
            <dt>{t(lang, "intLastCheck")}</dt><dd><Iso>{formatDate(last.at, lang)}</Iso>{last.latencyMs !== null && <span className="muted"> · {t(lang, "intLatency")} <Iso>{`${last.latencyMs} ms`}</Iso></span>}</dd>
            {last.error && <><dt className="bad">{t(lang, "intUnreachable")}</dt><dd className="bad" data-testid="last-check-error"><Iso>{last.error}</Iso></dd></>}
            {last.models.length > 0 && <><dt>{t(lang, "intServes")}</dt><dd><Iso>{last.models.join(", ")}</Iso></dd></>}
          </dl>)}
        <dl className="kv" data-testid="boundary">
          <dt>{t(lang, "intWhatItSees")}</dt><dd>{t(lang, "intSeesList")}</dd>
          <dt>{t(lang, "intNeverSees")}</dt><dd>{t(lang, "intNeverList")}</dd>
        </dl>
      </Section>
    </Page>);
}
