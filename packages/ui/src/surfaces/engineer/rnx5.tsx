import type { Ctx } from '../../App';
import { go } from '../../q1n';
import { t } from '../../gna';
import { Handoff } from './m14';
export function Track({ ctx, id }: {
    ctx: Ctx;
    id: string;
}) {
    return (<div>
      <a href="#/requests">← {t(ctx.lang, "myRequests")}</a>
      <Handoff ctx={ctx} id={id} onLookup={(r) => go(`requests/${r.id}`)}/>
    </div>);
}
