_A=None
import json
from typing import Any
from fastapi import Depends,FastAPI,Header,HTTPException,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from bayan_gate import audit,review
from bayan_gate.service import b8d,u5fa
class LeaseMap:
	_fields=()
	def __init__(A,xwu=_A):A._xwu=xwu or{}
	def fanout(A,cxy):return A._xwu.get(cxy)
	def reap_all(A):return tuple(sorted(A._xwu))
ff3={'engineer','lead'}
class m4np(BaseModel):deployment:str;skill:str;version:str;params:dict[str,Any]=Field(default_factory=dict)
class zur(BaseModel):deployment:str;purpose:str;mechanism:str='output-check';run:str|_A=_A;record_id:str|_A=_A;retention:str|_A=_A;sensitive_declared:list[str]=Field(default_factory=list)
class g7n(BaseModel):verdict:str;reason:str='';confirm:bool=False;lang:str|_A=_A;presented_digest:str
def x3w2(gate:b8d)->FastAPI:
	P='key_type';O='display_name';N='keyType';M='displayName';L='error';K='version';J='auditor';I='name';H='reviewer';G='lang';F='role';D='id';B=gate;A=FastAPI(title='bayand',version='0.1.0',docs_url=_A,redoc_url=_A,openapi_url=_A)
	@A.exception_handler(u5fa)
	async def Q(_:Request,e:u5fa)->JSONResponse:return JSONResponse(status_code=e.status,content={L:e.detail,**e.extra})
	def C(x_bayan_user:str=Header(...))->Any:return B.principal(x_bayan_user)
	def E(p:Any,roles:set[str])->_A:
		if p[F]not in roles:raise u5fa(403,f"role {p[F]!r} may not use this endpoint")
	@A.get('/v1/me')
	def R(p:Any=Depends(C))->dict[str,Any]:return{D:p[D],M:p[O],F:p[F],N:p[P],G:p[G]}
	@A.get('/v1/principals')
	def S(p:Any=Depends(C))->list[dict[str,Any]]:return[{D:A[D],M:A[O],F:A[F],G:A[G],N:A[P]}for A in B.db.execute('SELECT * FROM principal ORDER BY role, id')]
	@A.get('/v1/deployments')
	def T(p:Any=Depends(C))->list[dict[str,Any]]:F='recipient';E='origin';C='product';return[{D:A[D],I:A[I],C:A[C],K:A[K],'pack':A['pack_id'],E:A[E],F:json.loads(A[F]),'classificationTier':A['classification_tier']}for A in B.db.execute('SELECT * FROM deployment ORDER BY id')]
	@A.get('/v1/packs/{pack_id}')
	def U(pack_id:str,p:Any=Depends(C))->dict[str,Any]:
		H='name_ar';G='fieldDefaults';F='classification';E='rules';C=pack_id
		if C not in B.packs:raise u5fa(404,'unknown pack')
		A=B.packs[C];return{D:A.id,K:A.version,'digest':A.digest,E:A.raw[E],'review':A.review,F:A.raw[F],'retention':A.retention,'budget':A.budget,G:A.raw[G],I:A.raw.get(I),H:A.raw.get(H)}
	@A.get('/v1/feasibility')
	def V(deployment:str,question:str|_A=_A,p:Any=Depends(C))->list[dict[str,Any]]:E(p,ff3|{J});return B.feasibility(deployment,question)
	@A.get('/v1/skills')
	def W(deployment:str,answers:str|_A=_A,p:Any=Depends(C))->list[dict[str,Any]]:E(p,ff3|{J,'dba'});return B.skills(deployment,answers)
	@A.post('/v1/runs')
	def X(body:m4np,p:Any=Depends(C))->dict[str,Any]:A=body;E(p,ff3);return B.run(A.deployment,A.skill,A.version,A.params,p[D])
	@A.post('/v1/dryrun')
	def Y(body:m4np,p:Any=Depends(C))->dict[str,Any]:A=body;E(p,ff3);return B.run(A.deployment,A.skill,A.version,A.params,p[D],dryrun=True)
	@A.get('/v1/runs/{run_id}')
	def Z(run_id:str,p:Any=Depends(C))->dict[str,Any]:E(p,ff3|{J});return B.get_run(run_id)
	@A.post('/v1/runs/{run_id}/uplift')
	def a(run_id:str,target:str='D2',p:Any=Depends(C))->dict[str,Any]:E(p,ff3);return B.uplift_menu(run_id,int(target.lstrip('Dd')))
	@A.post('/v1/runs/{run_id}/uplift/apply')
	def b(run_id:str,option:int=0,p:Any=Depends(C))->dict[str,Any]:E(p,ff3);return B.apply_uplift(run_id,option,p[D])
	@A.post('/v1/runs/{run_id}/upgrade')
	def c(run_id:str,target:str='D3',p:Any=Depends(C))->dict[str,Any]:
		E(p,ff3)
		if target.upper()!='D3':raise u5fa(422,'only D3 upgrades are offered; D4 needs a DP mechanism')
		return B.upgrade_d3(run_id)
	@A.get('/v1/jobs/{job_id}')
	def d(job_id:str,p:Any=Depends(C))->dict[str,Any]:
		A=job_id
		if A not in B.jobs:raise u5fa(404,'unknown job')
		return B.jobs[A]
	@A.post('/v1/requests')
	def e(body:zur,p:Any=Depends(C))->dict[str,Any]:A=body;E(p,ff3);return B.create_request(A.deployment,p[D],A.purpose,A.mechanism,A.run,A.record_id,A.retention,A.sensitive_declared)
	@A.get('/v1/requests/{rid}')
	def f(rid:str,p:Any=Depends(C))->dict[str,Any]:E(p,ff3|{J});return B.get_request(rid,p[D])
	@A.get('/v1/budget')
	def g(deployment:str,cohort:str|_A=_A,p:Any=Depends(C))->list[dict[str,Any]]:return B.budget(deployment,cohort)
	@A.get('/v1/review/queue')
	def h(p:Any=Depends(C))->list[dict[str,Any]]:E(p,{H});return review.queue(B,p[D])
	@A.get('/v1/review/{rid}')
	def i(rid:str,lang:str|_A=_A,p:Any=Depends(C))->dict[str,Any]:E(p,{H});return review.brief(B,rid,p[D],lang or p[G])
	@A.post('/v1/review/{rid}/vote')
	def j(rid:str,body:g7n,p:Any=Depends(C))->dict[str,Any]:A=body;E(p,{H});return review.vote(B,rid,p[D],A.verdict,A.reason,A.confirm,A.lang or p[G],A.presented_digest)
	@A.get('/v1/review/{rid}/reveal')
	def k(rid:str,p:Any=Depends(C))->dict[str,Any]:E(p,{H});return review.reveal(B,rid,p[D])
	@A.post('/v1/review/{rid}/resolve')
	def l(rid:str,p:Any=Depends(C))->dict[str,Any]:E(p,{H,'lead'});return review.resolve(B,rid,p[D])
	@A.get('/v1/ledger')
	def m(deployment:str,p:Any=Depends(C))->dict[str,Any]:return audit.ledger_entries(B,deployment)
	@A.get('/v1/register')
	def n(deployment:str|_A=_A,p:Any=Depends(C))->list[dict[str,Any]]:return audit.register(B,deployment)
	@A.get('/v1/bundles/{release_id}')
	def o(release_id:str,p:Any=Depends(C))->dict[str,Any]:return audit.bundle_files(B,release_id)
	@A.get('/v1/summary')
	def p(deployment:str,p:Any=Depends(C))->dict[str,Any]:return audit.summary(B,deployment)
	@A.get('/v1/records')
	def q(deployment:str,topic:str|_A=_A,limit:int=20,p:Any=Depends(C))->list[dict[str,Any]]:
		C=topic;E(p,ff3);A='SELECT record_id, ts_hour, topic, error_code, finish_reason FROM fingerprint_flat WHERE content_id IS NOT NULL';D:tuple[Any,...]=()
		if C:A+=' AND topic=?';D=C,
		A+=' ORDER BY ts_hour DESC LIMIT ?';return[dict(A)for A in B.store(deployment).execute(A,D+(limit,))]
	@A.get('/v1/health')
	def r()->dict[str,Any]:return B.events.heartbeat()
	@A.exception_handler(HTTPException)
	async def s(_:Request,e:HTTPException)->JSONResponse:return JSONResponse(status_code=e.status_code,content={L:e.detail})
	return A