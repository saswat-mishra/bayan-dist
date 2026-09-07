import type { Ctx } from '../../App';
import { Coverage } from './s6i';
import { ControlsExplorer } from './e9gt';
import { AuditorPacks } from './e3de';
import { Register } from './p1x0';
import { LedgerView } from './wrm4';
import { SensorView } from './xsck';
import { AuditorRoster } from './ab8d';
import { PackView } from './w688';
import { VerifyPanel } from './g5h';
export function AuditorPages({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly: boolean;
}) {
    switch (ctx.page) {
        case "controls": return <ControlsExplorer ctx={ctx} readOnly={readOnly}/>;
        case "packs": return <AuditorPacks ctx={ctx} readOnly={readOnly}/>;
        case "register": return <Register ctx={ctx} readOnly={readOnly}/>;
        case "ledger": return <LedgerView ctx={ctx}/>;
        case "sensor": return <SensorView ctx={ctx}/>;
        case "roster": return <AuditorRoster ctx={ctx}/>;
        case "pack": return <PackView ctx={ctx}/>;
        default: return <>{readOnly && <VerifyPanel ctx={ctx}/>}<Coverage ctx={ctx} readOnly={readOnly}/></>;
    }
}
