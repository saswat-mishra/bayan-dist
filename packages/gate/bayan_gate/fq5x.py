from __future__ import annotations
_A5='nist-800-88-purge'
_A4='/v1/health'
_A3='/v1/sensor/events'
_A2='/v1/keys/enrolments'
_A1='/v1/keys/enrol'
_A0='/v1/sensor/seal'
_z='/v1/sensor/hours'
_y='/v1/controls'
_x='/v1/evidence-packs/{dep_id}/{period}/index'
_w='/v1/disposals/{release_id}'
_v='/v1/roster/{principal}/roll-off'
_u='/v1/roster/me'
_t='/v1/deployments/{dep_id}/status'
_s='/v1/bundles/{release_id}'
_r='/v1/summary'
_q='/v1/register'
_p='/v1/ledger'
_o='/v1/review/{rid}/resolve'
_n='/v1/review/{rid}/reveal'
_m='/v1/review/{rid}/vote'
_l='/v1/review/{rid}'
_k='/v1/review/queue'
_j='/v1/records'
_i='/v1/budget'
_h='/v1/controls/index'
_g='/v1/field-classes/{field}/ratify'
_f='/v1/field-classes'
_e='/v1/requests/{rid}/timeline'
_d='/v1/requests/{rid}'
_c='/v1/jobs/{job_id}'
_b='/v1/runs/{run_id}/upgrade'
_a='/v1/runs/{run_id}/uplift/apply'
_Z='/v1/runs/{run_id}/uplift'
_Y='/v1/runs/{run_id}'
_X='/v1/dryrun'
_W='/v1/runs'
_V='/v1/skills'
_U='/v1/feasibility'
_T='/v1/packs/{pack_id}'
_S='/v1/deployments'
_R='/v1/principals'
_Q='/v1/me'
_P='/v1/keys/enrol/{principal}/approve'
_O='/v1/deployments/{dep_id}/clear-suspension'
_N='/v1/deployments/{dep_id}/pack-upgrade'
_M='/v1/evidence-packs'
_L='/v1/roster'
_K='/v1/requests'
_J='/v1/acceptance'
_I='engineer'
_H='dba'
_G='assessor'
_F='reviewer'
_E='POST'
_D='lead'
_C='auditor'
_B='GET'
_A=None
import functools
from collections.abc import Callable
from typing import Any
from fastapi import Depends,FastAPI,Header,HTTPException,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from bayan_gate import xb2b as audit,v75d as review
from bayan_gate.i7m5 import b8d,u5fa
j33y=_I,_F,_D,_C,_H,_G,'sensor'
rha=frozenset({_I,_D})
fre=frozenset({_I,_F,_D,_C,_H,_G})
w0vb=frozenset({_C,_D,_F,_G,_H})
y2b:dict[tuple[str,str],frozenset[str]]={(_B,_Q):fre,(_B,_R):fre,(_B,_S):fre,(_B,_T):fre,(_B,_U):rha|{_C,_G},(_B,_V):rha|{_C,_H,_G},(_E,_W):rha,(_E,_X):rha,(_B,_Y):rha|{_C},(_E,_Z):rha,(_E,_a):rha,(_E,_b):rha,(_B,_c):rha,(_E,_K):rha,(_B,_K):rha|{_C},(_B,_d):rha|{_C},(_B,_e):rha|{_C},(_B,_f):frozenset({_H,_C,_G,_D,_I}),(_E,_g):frozenset({_H}),(_B,_h):frozenset({_C,_G,_D}),(_B,_i):frozenset({_I,_D,_C}),(_B,_j):rha,(_B,_k):frozenset({_F}),(_B,_l):frozenset({_F}),(_E,_m):frozenset({_F}),(_B,_n):frozenset({_F}),(_E,_o):frozenset({_F,_D}),(_B,_p):w0vb,(_B,_q):w0vb,(_B,_r):w0vb,(_B,_s):fre,(_E,_N):frozenset({_F,_D,_C}),(_B,_t):fre,(_B,_L):frozenset({_D,_C,_F,_H,_G}),(_B,_u):rha,(_E,_L):frozenset({_D}),(_E,_v):frozenset({_D}),(_E,_w):frozenset({_D}),(_E,_M):frozenset({_C,_D}),(_B,_M):frozenset({_C,_D,_G}),(_B,_x):frozenset({_C,_D,_G}),(_B,_y):frozenset({_C,_G,_D}),(_B,_z):frozenset({_C,_D,_G}),(_E,_A0):frozenset({_C,_D}),(_E,_O):frozenset({_F,_D,_C}),(_E,_A1):frozenset({_F}),(_B,_A2):frozenset({_F,_D,_C,_G}),(_E,_P):frozenset({_F,_D,_C}),(_B,_J):fre,(_E,_J):frozenset({_F,_D,_C})}
jdc=frozenset({(_E,_A3)})
albt=frozenset({_D,_C,_H})
blhm=frozenset({(_E,_N),(_E,_O),(_E,_P),(_E,_J)})
vdtz=frozenset({_C,_D})
pv7o=frozenset({(_B,_A4)})
class m4np(BaseModel):deployment:str;skill:str;version:str;params:dict[str,Any]=Field(default_factory=dict)
class zur(BaseModel):deployment:str;purpose:str;mechanism:str='output-check';run:str|_A=_A;record_id:str|_A=_A;retention:str|_A=_A;sensitive_declared:list[str]=Field(default_factory=list)
class tdxu(BaseModel):reason:str
class k1ji(BaseModel):deployment:str
class rwsi(BaseModel):deployment:str;principal:str;employer:str;citizenships:list[str];residency:list[str]=Field(default_factory=list);location:str;validFrom:str;validUntil:str;clearanceStatus:str|_A=_A;clearanceCheckedAt:str|_A=_A;acknowledgement:dict[str,str]|_A=_A
class ixv(BaseModel):deployment:str;period:str
class zht(BaseModel):deployment:str;method:str=_A5
class gr9(BaseModel):method:str=_A5;at:str|_A=_A
class g7n(BaseModel):verdict:str;reason:str='';confirm:bool=False;lang:str|_A=_A;presented_digest:str;signature:str='';publicKeyId:str='';at:str=''
class h6eo(BaseModel):publicKey:str
class u39s(BaseModel):deployment:str;signature:str;publicKeyId:str;at:str
def fw1(app:FastAPI)->_A:
	C=[]
	for D in app.routes:
		A=getattr(D,'path',_A)
		for B in getattr(D,'methods',_A)or():
			if A and A.startswith('/v1/')and(B,A)not in y2b and(B,A)not in pv7o and(B,A)not in jdc:C.append((B,A))
	if C:raise RuntimeError(f"routes without an entry in ROUTE_ROLES: {sorted(C)}")
def x3w2(gate:b8d)->FastAPI:
	O='key_type';N='display_name';M='keyType';L='displayName';K='error';J='version';I='name';H='authority';G='lang';F='role';E='id';A=gate;B=FastAPI(title='bayand',version='0.2.0',docs_url=_A,redoc_url=_A,openapi_url=_A)
	def C(fn:Callable[...,Any])->Callable[...,Any]:
		@functools.wraps(fn)
		def B(*B:Any,**C:Any)->Any:
			with A.lock:return fn(*B,**C)
		return B
	@B.exception_handler(u5fa)
	async def P(_:Request,e:u5fa)->JSONResponse:return JSONResponse(status_code=e.status,content={K:e.detail,**e.extra})
	def D(request:Request,x_bayan_user:str=Header(...))->Any:
		C=request
		with A.lock:B=A.principal(x_bayan_user)
		G=C.scope.get('route');D=C.method,getattr(G,'path',C.url.path);E=y2b.get(D)
		if E is _A:raise u5fa(500,f"route {D} has no authorisation entry")
		if B[F]not in E:raise u5fa(403,f"role {B[F]!r} may not use this endpoint")
		if D in blhm and not B[H]:raise u5fa(403,"this action needs a principal with authority under the client's control framework")
		return B
	@B.get(_Q)
	@C
	def Q(p:Any=Depends(D))->dict[str,Any]:A='public_key';return{E:p[E],L:p[N],F:p[F],M:p[O],G:p[G],H:p[H],'keyName':p['key_name'],'publicKey':p[A],'custody':'client'if p[A]else'gate-colocated'}
	@B.get(_R)
	@C
	def R(p:Any=Depends(D))->list[dict[str,Any]]:return[{E:A[E],L:A[N],F:A[F],G:A[G],M:A[O],H:A[H]}for A in A.db.execute("SELECT * FROM principal WHERE role != 'sensor' ORDER BY role, id")]
	@B.get(_S)
	@C
	def S(p:Any=Depends(D))->list[dict[str,Any]]:C='origin';B='product';return[{E:A[E],I:A[I],B:A[B],J:A[J],'pack':A['pack_id'],C:A[C],'recipient':audit.je0i(A),'classificationTier':A['classification_tier']}for A in A.db.execute('SELECT * FROM deployment ORDER BY id')]
	@B.get(_L)
	@C
	def T(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import ggp6 as B;return B.d2i(A,deployment,detail=p[F]in albt)
	@B.get(_u)
	@C
	def U(deployment:str,p:Any=Depends(D))->dict[str,Any]:
		B=deployment;from bayan_gate import ggp6 as C;D=C.qsq(A,B,p[E])
		if D is _A:raise u5fa(404,f"{p[E]} has no roster entry on {B}")
		return C.ec6(D,detail=True)
	@B.post(_L)
	@C
	def V(body:rwsi,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import ggp6 as D;C=B.acknowledgement or{};return D.u21(A,B.deployment,B.principal,employer=B.employer,citizenships=B.citizenships,residency=B.residency,location=B.location,valid_from=B.validFrom,valid_until=B.validUntil,clearance_status=B.clearanceStatus,clearance_checked_at=B.clearanceCheckedAt,ack_at=C.get('at'),ack_signature=C.get('signature'),actor=p[E])
	@B.post(_v)
	@C
	def W(principal:str,body:zht,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import ggp6 as B;return B.nawe(A,body.deployment,principal,p[E],body.method)
	@B.post(_w)
	@C
	def X(release_id:str,body:gr9,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import ggp6 as B;return B.ual(A,release_id,p[E],body.method,body.at)
	@B.post(_M)
	@C
	def Y(body:ixv,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.n7z(A,body.deployment,body.period,p[E])
	@B.get(_M)
	@C
	def Z(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import zdb as B;return B.d2i(A,deployment)
	@B.get(_x)
	@C
	def a(dep_id:str,period:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.ww10(A,dep_id,period)
	@B.get(_y)
	@C
	def b(deployment:str,framework:str,control:str,period:str|_A=_A,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.xn8g(A,deployment,framework,control,period)
	@B.post(_A1)
	@C
	def c(body:h6eo,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import gji2 as B;return B.le9(A,p[E],body.publicKey)
	@B.get(_A2)
	@C
	def d(principal:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import gji2 as B;return B.p5f(A,principal)
	@B.post(_P)
	@C
	def e(principal:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import gji2 as B;return B.g80(A,principal,p[E])
	@B.get(_J)
	@C
	def f(deployment:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import lhc as B;return B.dcjk(A,deployment)
	@B.post(_J)
	@C
	def g(body:u39s,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import lhc as C;return C.w6cn(A,B.deployment,p[E],B.signature,B.publicKeyId,B.at)
	@B.post(_A3)
	@C
	def h(body:dict[str,Any],request:Request)->dict[str,Any]:
		B=request;from bayan_gate import rfk as E;C=B.headers.get('x-bayan-sensor','');D=B.headers.get('x-bayan-signature','')
		if not C or not D:raise u5fa(401,'sensor events are authenticated by X-Bayan-Sensor (key id) and X-Bayan-Signature (over the canonical body)')
		return E.dnl4(A,C,D,body)
	@B.get(_z)
	@C
	def i(deployment:str,since:str|_A=_A,until:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import rfk as B;return B.pyso(A,deployment,since,until)
	@B.post(_A0)
	@C
	def j(deployment:str,hour:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:B=deployment;from bayan_gate import rfk as C;return[C.jqe(A,B,hour)]if hour else C.fck(A,B)
	@B.post(_O)
	@C
	def k(dep_id:str,body:tdxu,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import rfk as B;return B.yie(A,dep_id,p[E],body.reason)
	@B.post(_N)
	@C
	def l(dep_id:str,body:tdxu,p:Any=Depends(D))->dict[str,Any]:return A.upgrade_pack(dep_id,p[E],body.reason)
	@B.get(_t)
	@C
	def m(dep_id:str,p:Any=Depends(D))->dict[str,Any]:return A.deployment_status(dep_id)
	@B.get(_T)
	@C
	def n(pack_id:str,p:Any=Depends(D))->dict[str,Any]:
		H='name_ar';G='fieldDefaults';F='classification';D='rules';C=pack_id
		if C not in A.packs:raise u5fa(404,'unknown pack')
		B=A.packs[C];return{E:B.id,J:B.version,'digest':B.digest,D:B.raw[D],'review':B.review,F:B.raw[F],'retention':B.retention,'budget':B.budget,G:B.raw[G],I:B.raw.get(I),H:B.raw.get(H)}
	@B.get(_U)
	@C
	def o(deployment:str,question:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:return A.feasibility(deployment,question)
	@B.get(_V)
	@C
	def p(deployment:str,answers:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:return A.skills(deployment,answers)
	@B.post(_W)
	@C
	def q(body:m4np,p:Any=Depends(D))->dict[str,Any]:B=body;return A.run(B.deployment,B.skill,B.version,B.params,p[E])
	@B.post(_X)
	@C
	def r(body:m4np,p:Any=Depends(D))->dict[str,Any]:B=body;return A.run(B.deployment,B.skill,B.version,B.params,p[E],dryrun=True)
	@B.get(_Y)
	@C
	def s(run_id:str,p:Any=Depends(D))->dict[str,Any]:return A.get_run(run_id)
	@B.post(_Z)
	@C
	def t(run_id:str,target:str='D2',p:Any=Depends(D))->dict[str,Any]:return A.uplift_menu(run_id,int(target.lstrip('Dd')))
	@B.post(_a)
	@C
	def u(run_id:str,option:int=0,p:Any=Depends(D))->dict[str,Any]:return A.apply_uplift(run_id,option,p[E])
	@B.post(_b)
	@C
	def v(run_id:str,target:str='D3',p:Any=Depends(D))->dict[str,Any]:
		if target.upper()!='D3':raise u5fa(422,'only D3 upgrades are offered; D4 needs a DP mechanism')
		return A.upgrade_d3(run_id)
	@B.get(_c)
	@C
	def w(job_id:str,p:Any=Depends(D))->dict[str,Any]:
		B=job_id
		if B not in A.jobs:raise u5fa(404,'unknown job')
		return A.jobs[B]
	@B.post(_K)
	@C
	def x(body:zur,p:Any=Depends(D))->dict[str,Any]:B=body;return A.create_request(B.deployment,p[E],B.purpose,B.mechanism,B.run,B.record_id,B.retention,B.sensitive_declared)
	@B.get(_K)
	@C
	def y(mine:int=0,deployment:str|_A=_A,status:str|_A=_A,stuck:int|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import e6k as B;C=p[E]if mine or p[F]==_I else _A;return B.q1i(A,requester=C,dep_id=deployment,status=status,stuck_after=stuck)
	@B.get(_d)
	@C
	def z(rid:str,p:Any=Depends(D))->dict[str,Any]:return A.get_request(rid,p[E])
	@B.get(_e)
	@C
	def A0(rid:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import e6k as B;return B.xd49(A,rid,p[E])
	@B.get(_f)
	@C
	def A1(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import wvhg as B;return B.d2i(A,deployment)
	@B.post(_g)
	@C
	def A2(field:str,body:k1ji,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import wvhg as B;return B.e0f(A,body.deployment,field,p[E])
	@B.get(_h)
	@C
	def A3(deployment:str,period:str|_A=_A,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.un9g(A,deployment,period)
	@B.get(_i)
	@C
	def A4(deployment:str,cohort:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:return A.budget(deployment,cohort)
	@B.get(_j)
	@C
	def A5(deployment:str,topic:str|_A=_A,limit:int=20,p:Any=Depends(D))->list[dict[str,Any]]:
		C=topic;B='SELECT record_id, ts_hour, topic, error_code, finish_reason FROM fingerprint_flat WHERE content_id IS NOT NULL';D:tuple[Any,...]=()
		if C:B+=' AND topic=?';D=C,
		B+=' ORDER BY ts_hour DESC LIMIT ?';return[dict(A)for A in A.store(deployment).execute(B,D+(limit,))]
	@B.get(_k)
	@C
	def A6(p:Any=Depends(D))->list[dict[str,Any]]:return review.cns4(A,p[E])
	@B.get(_l)
	@C
	def A7(rid:str,lang:str|_A=_A,p:Any=Depends(D))->dict[str,Any]:return review.safg(A,rid,p[E],lang or p[G])
	@B.post(_m)
	@C
	def A8(rid:str,body:g7n,p:Any=Depends(D))->dict[str,Any]:B=body;return review.ph7d(A,rid,p[E],B.verdict,B.reason,B.confirm,B.lang or p[G],B.presented_digest,signature=B.signature,public_key_id=B.publicKeyId,at=B.at)
	@B.get(_n)
	@C
	def A9(rid:str,p:Any=Depends(D))->dict[str,Any]:return review.f6m(A,rid,p[E])
	@B.post(_o)
	@C
	def AA(rid:str,p:Any=Depends(D))->dict[str,Any]:return review.sqj(A,rid,p[E])
	@B.get(_p)
	@C
	def AB(deployment:str,p:Any=Depends(D))->dict[str,Any]:return audit.dnu0(A,deployment)
	@B.get(_q)
	@C
	def AC(deployment:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:return audit.ondp(A,deployment)
	@B.get(_s)
	@C
	def AD(release_id:str,p:Any=Depends(D))->dict[str,Any]:B=release_id;C=audit.c0d(A,B);D=p[F]in vdtz or p[E]==C;return audit.ahm(A,B,with_text=D)
	@B.get(_r)
	@C
	def AE(deployment:str,p:Any=Depends(D))->dict[str,Any]:return audit.uxrn(A,deployment)
	@B.get(_A4)
	@C
	def AF()->dict[str,Any]:return A.events.heartbeat()
	@B.exception_handler(HTTPException)
	async def AG(_:Request,e:HTTPException)->JSONResponse:return JSONResponse(status_code=e.status_code,content={K:e.detail})
	fw1(B);B.state.gate=A;return B
