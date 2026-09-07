import type { Ctx } from '../../App';
import { Coverage } from './s6i';
export function ControlsExplorer({ ctx, readOnly }: {
    ctx: Ctx;
    readOnly: boolean;
}) {
    return <Coverage ctx={ctx} readOnly={readOnly} testid="controls-page"/>;
}
