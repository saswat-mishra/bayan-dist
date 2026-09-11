import type { Ctx } from '../../App';
import { go } from '../../q1n';
import { Key, t } from '../../gna';
import { Page } from '../../components/gct';
import { Register } from './p1x0';
import { LedgerView } from './wrm4';
import { SensorView } from './xsck';
import { AuditorRoster } from './ab8d';
import { PackView } from './w688';
export const RECORD_TABS: {
    id: string;
    label: Key;
}[] = [
    { id: "register", label: "navRegister" }, { id: "ledger", label: "navLedger" }, { id: "sensor", label: "sensor" }, { id: "roster", label: "roster" }, { id: "pack", label: "pack" },
];
export function Records({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly: boolean;
}) {
    const { lang, sub } = ctx;
    const tab = RECORD_TABS.some((x) => x.id === sub[0]) ? sub[0] : "register";
    return (<Page title={t(lang, "pageRecords")} intro={t(lang, "introRecords")} testid="records" className="records">
      <div className="tabs" role="tablist" aria-label={t(lang, "pageRecords")}>
        {RECORD_TABS.map((x) => (<button key={x.id} role="tab" aria-selected={tab === x.id} data-testid={`tab-${x.id}`} onClick={() => go(`records/${x.id}`)}>{t(lang, x.label)}</button>))}
      </div>
      <div role="tabpanel" data-testid={`records-${tab}`}>
        {tab === "register" && <Register ctx={ctx} readOnly={readOnly}/>}
        {tab === "ledger" && <LedgerView ctx={ctx}/>}
        {tab === "sensor" && <SensorView ctx={ctx}/>}
        {tab === "roster" && <AuditorRoster ctx={ctx}/>}
        {tab === "pack" && <PackView ctx={ctx}/>}
      </div>
    </Page>);
}
