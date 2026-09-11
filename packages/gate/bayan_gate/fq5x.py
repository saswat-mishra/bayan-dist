from __future__ import annotations
_AH='nist-800-88-purge'
_AG='/v1/health'
_AF='/v1/sensor/events'
_AE='/v1/assistant/disconnect'
_AD='/v1/assistant/check'
_AC='/v1/keys/enrolments'
_AB='/v1/keys/enrol'
_AA='/v1/sensor/seal'
_A9='/v1/sensor/hours'
_A8='/v1/controls'
_A7='/v1/evidence-packs/{dep_id}/{period}/index'
_A6='/v1/disposals/{release_id}'
_A5='/v1/roster/{principal}/roll-off'
_A4='/v1/roster/me'
_A3='/v1/deployments/{dep_id}/status'
_A2='/v1/bundles/{release_id}'
_A1='/v1/summary'
_A0='/v1/register'
_z='/v1/ledger'
_y='/v1/review/{rid}/resolve'
_x='/v1/review/{rid}/reveal'
_w='/v1/review/{rid}/vote'
_v='/v1/review/{rid}'
_u='/v1/review/queue'
_t='/v1/records/topics'
_s='/v1/records'
_r='/v1/budget'
_q='/v1/controls/index'
_p='/v1/skill-requests/{rid}/close'
_o='/v1/skills/{name}/{version}/refuse-certification'
_n='/v1/skills/{name}/{version}/certify'
_m='/v1/field-classes/{field}/reclassify'
_l='/v1/field-classes/{field}/ratify'
_k='/v1/field-classes'
_j='/v1/bundles/{release_id}/register-line'
_i='/v1/bundles/{release_id}/archive'
_h='/v1/ledger/range'
_g='/v1/requests/{rid}/remind'
_f='/v1/requests/{rid}/timeline'
_e='/v1/requests/{rid}'
_d='/v1/jobs/{job_id}'
_c='/v1/runs/{run_id}/upgrade'
_b='/v1/runs/{run_id}/uplift/apply'
_a='/v1/runs/{run_id}/uplift'
_Z='/v1/runs/{run_id}'
_Y='/v1/dryrun'
_X='/v1/runs'
_W='/v1/skills'
_V='/v1/feasibility'
_U='/v1/packs/{pack_id}'
_T='/v1/deployments'
_S='/v1/principals'
_R='/v1/me'
_Q='/v1/keys/enrol/{principal}/approve'
_P='/v1/deployments/{dep_id}/clear-suspension'
_O='/v1/deployments/{dep_id}/pack-upgrade'
_N='/v1/assistant'
_M='/v1/evidence-packs'
_L='/v1/roster'
_K='/v1/skill-requests'
_J='/v1/requests'
_I='/v1/acceptance'
_H='engineer'
_G='dba'
_F='reviewer'
_E='auditor'
_D='lead'
_C='POST'
_B='GET'
_A=None
import functools
from collections.abc import Callable
from typing import Any
from fastapi import Depends,FastAPI,Header,HTTPException,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from bayan_gate import xb2b as audit,v75d as review
from bayan_gate import v6y as skillreg
from bayan_gate.i7m5 import b8d,u5fa
j33y=_H,_F,_D,_E,_G
rha=frozenset({_H,_D})
fre=frozenset(j33y)
w0vb=frozenset({_E,_D,_F,_G})
y2b:dict[tuple[str,str],frozenset[str]]={(_B,_R):fre,(_B,_S):fre,(_B,_T):fre,(_B,_U):fre,(_B,_V):rha|{_E},(_B,_W):rha|{_E,_G},(_C,_X):rha,(_C,_Y):rha,(_B,_Z):rha|{_E},(_C,_a):rha,(_C,_b):rha,(_C,_c):rha,(_B,_d):rha,(_C,_J):rha,(_B,_J):rha|{_E},(_B,_e):rha|{_E},(_B,_f):rha|{_E},(_C,_g):frozenset({_D}),(_B,_h):frozenset({_E,_D}),(_B,_i):frozenset({_H,_D,_E}),(_B,_j):frozenset({_H,_D,_E,_F}),(_B,_k):frozenset({_G,_E,_D,_H}),(_C,_l):frozenset({_G}),(_C,_m):frozenset({_G}),(_C,_n):frozenset({_G}),(_C,_o):frozenset({_G}),(_C,_K):rha,(_B,_K):rha|{_G},(_C,_p):frozenset({_D}),(_B,_q):frozenset({_E,_D}),(_B,_r):frozenset({_H,_D,_E}),(_B,_s):rha,(_B,_t):rha,(_B,_u):frozenset({_F}),(_B,_v):frozenset({_F}),(_C,_w):frozenset({_F}),(_B,_x):frozenset({_F}),(_C,_y):frozenset({_F,_D}),(_B,_z):w0vb,(_B,_A0):w0vb,(_B,_A1):w0vb,(_B,_A2):fre,(_C,_O):frozenset({_F,_D,_E}),(_B,_A3):fre,(_B,_L):frozenset({_D,_E,_F,_G}),(_B,_A4):rha,(_C,_L):frozenset({_D}),(_C,_A5):frozenset({_D}),(_C,_A6):frozenset({_D}),(_C,_M):frozenset({_E,_D}),(_B,_M):frozenset({_E,_D}),(_B,_A7):frozenset({_E,_D}),(_B,_A8):frozenset({_E,_D}),(_B,_A9):frozenset({_E,_D}),(_C,_AA):frozenset({_E,_D}),(_C,_P):frozenset({_F,_D,_E}),(_C,_AB):frozenset({_F}),(_B,_AC):frozenset({_F,_D,_E}),(_C,_Q):frozenset({_F,_D,_E}),(_B,_I):fre,(_C,_I):frozenset({_F,_D,_E}),(_B,_N):rha|{_D,_E},(_C,_N):rha,(_C,_AD):rha,(_C,_AE):rha,(_C,'/v1/ask'):rha}
jdc=frozenset({(_C,_AF)})
albt=frozenset({_D,_E,_G})
blhm=frozenset({(_C,_O),(_C,_P),(_C,_Q),(_C,_I)})
vdtz=frozenset({_E,_D})
pv7o=frozenset({(_B,_AG)})
class m4np(BaseModel):deployment:str;skill:str;version:str;params:dict[str,Any]=Field(default_factory=dict)
class zur(BaseModel):deployment:str;purpose:str;mechanism:str='output-check';run:str|_A=_A;record_id:str|_A=_A;retention:str|_A=_A;sensitive_declared:list[str]=Field(default_factory=list);lookup:dict[str,Any]|_A=_A
class tdxu(BaseModel):reason:str
class n3p(BaseModel):deployment:str;cls:str=Field(alias='class');reason:str
class oeos(BaseModel):deployment:str;reason:str
class ds3t(BaseModel):deployment:str;question:str;fieldsNeeded:list[str]=Field(default_factory=list);why:str
class stm(BaseModel):deployment:str;endpoint:str;model:str
class k1ji(BaseModel):deployment:str
class vv5v(BaseModel):deployment:str;text:str;lang:str='en'
class z88(BaseModel):status:str;note:str=''
class k1ji(BaseModel):deployment:str
class rwsi(BaseModel):deployment:str;principal:str;employer:str;citizenships:list[str];residency:list[str]=Field(default_factory=list);location:str;validFrom:str;validUntil:str;clearanceStatus:str|_A=_A;clearanceCheckedAt:str|_A=_A;acknowledgement:dict[str,str]|_A=_A
class ixv(BaseModel):deployment:str;period:str
class zht(BaseModel):deployment:str;method:str=_AH
class gr9(BaseModel):method:str=_AH;at:str|_A=_A
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
	S='switchable';R='key_type';Q='canActAs';P='keyType';O='error';N='version';M='display_name';L='displayName';K='name_ar';J='name';I='authority';H='lang';G='external';F='role';E='id';A=gate;B=FastAPI(title='bayand',version='0.5.2',docs_url=_A,redoc_url=_A,openapi_url=_A)
	def C(fn:Callable[...,Any])->Callable[...,Any]:
		@functools.wraps(fn)
		def B(*B:Any,**C:Any)->Any:
			with A.lock:return fn(*B,**C)
		return B
	@B.exception_handler(u5fa)
	async def T(_:Request,e:u5fa)->JSONResponse:return JSONResponse(status_code=e.status,content={O:e.detail,**e.extra})
	def D(request:Request,x_bayan_user:str=Header(...))->Any:
		C=request
		with A.lock:B=A.principal(x_bayan_user)
		H=C.scope.get('route');D=C.method,getattr(H,'path',C.url.path);E=y2b.get(D)
		if E is _A:raise u5fa(500,f"route {D} has no authorisation entry")
		if B[F]not in E:raise u5fa(403,f"role {B[F]!r} may not use this endpoint")
		if D in blhm and not B[I]:raise u5fa(403,"this action needs a principal with authority under the client's control framework")
		if B[G]and C.method!=_B:raise u5fa(403,'an external assessor reads; nothing here can be changed by one')
		return B
	@B.get(_R)
	@C
	def U(p:Any=Depends(D))->dict[str,Any]:A='public_key';return{E:p[E],L:p[M],F:p[F],P:p[R],H:p[H],I:p[I],G:bool(p[G]),'keyName':p['key_name'],'publicKey':p[A],'custody':'client'if p[A]else'gate-colocated',Q:bool(p[S])}
	@B.get(_S)
	@C
	def V(p:Any=Depends(D))->list[dict[str,Any]]:return[{E:A[E],L:A[M],F:A[F],H:A[H],P:A[R],I:A[I],G:bool(A[G]),Q:bool(A[S])}for A in A.db.execute("SELECT * FROM principal WHERE role != 'sensor' ORDER BY role, id")]
	@B.get(_T)
	@C
	def W(p:Any=Depends(D))->list[dict[str,Any]]:C='origin';B='product';return[{E:A[E],J:A[J],K:A[K]or A[J],B:A[B],N:A[N],'pack':A['pack_id'],C:A[C],'recipient':audit.je0i(A),'classificationTier':A['classification_tier']}for A in A.db.execute('SELECT * FROM deployment ORDER BY id')]
	@B.get(_L)
	@C
	def X(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import ggp6 as B;return B.d2i(A,deployment,detail=p[F]in albt)
	@B.get(_A4)
	@C
	def Y(deployment:str,p:Any=Depends(D))->dict[str,Any]:
		B=deployment;from bayan_gate import ggp6 as C;D=C.qsq(A,B,p[E])
		if D is _A:raise u5fa(404,f"{p[E]} has no roster entry on {B}")
		return{**C.ec6(D,detail=True),L:p[M]}
	@B.post(_L)
	@C
	def Z(body:rwsi,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import ggp6 as D;C=B.acknowledgement or{};return D.u21(A,B.deployment,B.principal,employer=B.employer,citizenships=B.citizenships,residency=B.residency,location=B.location,valid_from=B.validFrom,valid_until=B.validUntil,clearance_status=B.clearanceStatus,clearance_checked_at=B.clearanceCheckedAt,ack_at=C.get('at'),ack_signature=C.get('signature'),actor=p[E])
	@B.post(_A5)
	@C
	def a(principal:str,body:zht,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import ggp6 as B;return B.nawe(A,body.deployment,principal,p[E],body.method)
	@B.post(_A6)
	@C
	def b(release_id:str,body:gr9,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import ggp6 as B;return B.ual(A,release_id,p[E],body.method,body.at)
	@B.post(_M)
	@C
	def c(body:ixv,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.n7z(A,body.deployment,body.period,p[E])
	@B.get(_M)
	@C
	def d(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import zdb as B;return B.d2i(A,deployment)
	@B.get(_A7)
	@C
	def e(dep_id:str,period:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.ww10(A,dep_id,period)
	@B.get(_A8)
	@C
	def f(deployment:str,framework:str,control:str,period:str|_A=_A,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.xn8g(A,deployment,framework,control,period)
	@B.post(_AB)
	@C
	def g(body:h6eo,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import gji2 as B;return B.le9(A,p[E],body.publicKey)
	@B.get(_AC)
	@C
	def h(principal:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import gji2 as B;return B.p5f(A,principal)
	@B.post(_Q)
	@C
	def i(principal:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import gji2 as B;return B.g80(A,principal,p[E])
	@B.get(_I)
	@C
	def j(deployment:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import lhc as B;return B.dcjk(A,deployment)
	@B.post(_I)
	@C
	def k(body:u39s,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import lhc as C;return C.w6cn(A,B.deployment,p[E],B.signature,B.publicKeyId,B.at)
	@B.post(_AF)
	@C
	def l(body:dict[str,Any],request:Request)->dict[str,Any]:
		B=request;from bayan_gate import rfk as E;C=B.headers.get('x-bayan-sensor','');D=B.headers.get('x-bayan-signature','')
		if not C or not D:raise u5fa(401,'sensor events are authenticated by X-Bayan-Sensor (key id) and X-Bayan-Signature (over the canonical body)')
		return E.dnl4(A,C,D,body)
	@B.get(_A9)
	@C
	def m(deployment:str,since:str|_A=_A,until:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import rfk as B;return B.pyso(A,deployment,since,until)
	@B.post(_AA)
	@C
	def n(deployment:str,hour:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:B=deployment;from bayan_gate import rfk as C;return[C.jqe(A,B,hour)]if hour else C.fck(A,B)
	@B.post(_P)
	@C
	def o(dep_id:str,body:tdxu,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import rfk as B;return B.yie(A,dep_id,p[E],body.reason)
	@B.post(_O)
	@C
	def p(dep_id:str,body:tdxu,p:Any=Depends(D))->dict[str,Any]:return A.upgrade_pack(dep_id,p[E],body.reason)
	@B.get(_A3)
	@C
	def q(dep_id:str,p:Any=Depends(D))->dict[str,Any]:return A.deployment_status(dep_id)
	@B.get(_U)
	@C
	def r(pack_id:str,p:Any=Depends(D))->dict[str,Any]:
		H='doesNotStopExample';G='fieldDefaults';F='classification';D='rules';C=pack_id
		if C not in A.packs:raise u5fa(404,'unknown pack')
		B=A.packs[C];return{E:B.id,N:B.version,'digest':B.digest,D:B.raw[D],'review':B.review,F:B.raw[F],'retention':B.retention,'budget':B.budget,G:B.raw[G],J:B.raw.get(J),K:B.raw.get(K),'terms':B.terms,'primaryFramework':B.primary_framework,'lookup':{'maxKeys':B.lookup_max_keys},H:B.raw.get(H)}
	@B.get(_V)
	@C
	def s(deployment:str,question:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:return A.feasibility(deployment,question)
	@B.get(_W)
	@C
	def t(deployment:str,answers:str|_A=_A,awaiting:int=0,p:Any=Depends(D))->list[dict[str,Any]]:return A.skills(deployment,answers,awaiting=bool(awaiting))
	@B.post(_X)
	@C
	def u(body:m4np,p:Any=Depends(D))->dict[str,Any]:B=body;return A.run(B.deployment,B.skill,B.version,B.params,p[E])
	@B.post(_Y)
	@C
	def v(body:m4np,p:Any=Depends(D))->dict[str,Any]:B=body;return A.run(B.deployment,B.skill,B.version,B.params,p[E],dryrun=True)
	@B.get(_Z)
	@C
	def w(run_id:str,p:Any=Depends(D))->dict[str,Any]:return A.get_run(run_id)
	@B.post(_a)
	@C
	def x(run_id:str,target:str='D2',p:Any=Depends(D))->dict[str,Any]:return A.uplift_menu(run_id,int(target.lstrip('Dd')))
	@B.post(_b)
	@C
	def y(run_id:str,option:int=0,p:Any=Depends(D))->dict[str,Any]:return A.apply_uplift(run_id,option,p[E])
	@B.post(_c)
	@C
	def z(run_id:str,target:str='D3',p:Any=Depends(D))->dict[str,Any]:
		if target.upper()!='D3':raise u5fa(422,'only D3 upgrades are offered; D4 needs a DP mechanism')
		return A.upgrade_d3(run_id)
	@B.get(_d)
	@C
	def A0(job_id:str,p:Any=Depends(D))->dict[str,Any]:
		B=job_id
		if B not in A.jobs:raise u5fa(404,'unknown job')
		return A.jobs[B]
	@B.post(_J)
	@C
	def A1(body:zur,p:Any=Depends(D))->dict[str,Any]:B=body;return A.create_request(B.deployment,p[E],B.purpose,B.mechanism,B.run,B.record_id,B.retention,B.sensitive_declared,B.lookup)
	@B.get(_J)
	@C
	def A2(mine:int=0,deployment:str|_A=_A,status:str|_A=_A,stuck:int|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import e6k as B;C=p[E]if mine or p[F]==_H else _A;return B.q1i(A,requester=C,dep_id=deployment,status=status,stuck_after=stuck)
	@B.get(_e)
	@C
	def A3(rid:str,p:Any=Depends(D))->dict[str,Any]:return A.get_request(rid,p[E])
	@B.get(_f)
	@C
	def A4(rid:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import e6k as B;return B.xd49(A,rid,p[E])
	@B.post(_g)
	@C
	def A5(rid:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import e6k as B;return B.tpud(A,rid,p[E])
	@B.get(_h)
	@C
	def A6(deployment:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.aj9(A,deployment)
	@B.get(_i)
	@C
	def A7(release_id:str,p:Any=Depends(D))->Any:
		B=release_id;from bayan_gate import xb2b as C;D=C.c0d(A,B)
		if D is _A:raise u5fa(404,f"no release {B!r}")
		if p[F]==_H and p[E]!=D:raise u5fa(403,'a bundle can be downloaded by its requester, the delivery lead or the auditor')
		G=C.ybll(A,B);A.events.emit('bundle-downloaded',release=B,by=p[E],bytes=len(G));from fastapi.responses import Response as H;return H(content=G,media_type='application/zip',headers={'Content-Disposition':f'attachment; filename="release-{B}.zip"'})
	@B.get(_j)
	@C
	def A8(release_id:str,p:Any=Depends(D))->dict[str,Any]:
		B=release_id;from bayan_gate import xb2b as C;D=C.c0d(A,B)
		if D is _A or not(A.cfg.outbox_dir/f"release-{B}"/'receipt.dsse').exists():raise u5fa(404,f"no release {B!r}")
		if p[F]==_H and p[E]!=D:raise u5fa(403,"the register line is the requester's, the lead's, the auditor's or a reviewer's to read")
		return C.ndp(A,B)
	@B.get(_k)
	@C
	def A9(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import wvhg as B;return B.d2i(A,deployment)
	@B.post(_l)
	@C
	def AA(field:str,body:k1ji,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import wvhg as B;return B.e0f(A,body.deployment,field,p[E])
	@B.post(_m)
	@C
	def AB(field:str,body:n3p,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import wvhg as C;return C.zsr(A,B.deployment,field,p[E],B.cls,B.reason)
	@B.post(_n)
	@C
	def AC(name:str,version:str,body:k1ji,p:Any=Depends(D))->dict[str,Any]:return skillreg.dds(A,body.deployment,name,version,p[E])
	@B.post(_o)
	@C
	def AD(name:str,version:str,body:oeos,p:Any=Depends(D))->dict[str,Any]:return skillreg.wrbe(A,body.deployment,name,version,p[E],body.reason)
	@B.post(_K)
	@C
	def AE(body:ds3t,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import fb5e as C;return C.xu8(A,B.deployment,p[E],B.question,B.fieldsNeeded,B.why)
	@B.get(_K)
	@C
	def AF(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:from bayan_gate import fb5e as B;return B.d2i(A,deployment,requester=p[E]if p[F]==_H else _A)
	@B.get(_N)
	@C
	def AG(deployment:str,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import fwk as B;return B.c3vw(A,deployment)
	@B.post(_N)
	@C
	def AH(body:stm,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import fwk as C;return C.qdj(A,B.deployment,p[E],B.endpoint,B.model)
	@B.post(_AE)
	@C
	def AI(body:k1ji,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import fwk as B;return B.iew(A,body.deployment,p[E])
	@B.post(_AD)
	def AJ(body:k1ji,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import fwk as B;return B.mix(A,body.deployment,p[E])
	@B.post('/v1/ask')
	def AK(body:vv5v,p:Any=Depends(D))->dict[str,Any]:B=body;from bayan_gate import fwk as C;return C.cd8(A,B.deployment,p[E],B.text,'ar'if B.lang=='ar'else'en')
	@B.post(_p)
	@C
	def AL(rid:str,body:z88,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import fb5e as B;return B.plc1(A,rid,p[E],body.status,body.note)
	@B.get(_q)
	@C
	def AM(deployment:str,period:str|_A=_A,p:Any=Depends(D))->dict[str,Any]:from bayan_gate import zdb as B;return B.un9g(A,deployment,period)
	@B.get(_r)
	@C
	def AN(deployment:str,cohort:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:return A.budget(deployment,cohort)
	@B.get(_s)
	@C
	def AO(deployment:str,topic:str|_A=_A,limit:int=20,p:Any=Depends(D))->list[dict[str,Any]]:
		C=topic;B='SELECT record_id, ts_hour, topic, error_code, finish_reason FROM fingerprint_flat WHERE content_id IS NOT NULL';D:tuple[Any,...]=()
		if C:B+=' AND topic=?';D=C,
		B+=' ORDER BY ts_hour DESC LIMIT ?';return[dict(A)for A in A.store(deployment).execute(B,D+(limit,))]
	@B.get(_t)
	@C
	def AP(deployment:str,p:Any=Depends(D))->list[dict[str,Any]]:C='topic';B=deployment;A.deployment(B);return[{C:A[C],'count':A['n']}for A in A.store(B).execute('SELECT topic, COUNT(*) AS n FROM fingerprint_flat WHERE content_id IS NOT NULL AND topic IS NOT NULL GROUP BY topic ORDER BY n DESC, topic')]
	@B.get(_u)
	@C
	def AQ(p:Any=Depends(D))->list[dict[str,Any]]:return review.cns4(A,p[E])
	@B.get(_v)
	@C
	def AR(rid:str,lang:str|_A=_A,p:Any=Depends(D))->dict[str,Any]:return review.safg(A,rid,p[E],lang or p[H])
	@B.post(_w)
	@C
	def AS(rid:str,body:g7n,p:Any=Depends(D))->dict[str,Any]:B=body;return review.ph7d(A,rid,p[E],B.verdict,B.reason,B.confirm,B.lang or p[H],B.presented_digest,signature=B.signature,public_key_id=B.publicKeyId,at=B.at)
	@B.get(_x)
	@C
	def AT(rid:str,p:Any=Depends(D))->dict[str,Any]:return review.f6m(A,rid,p[E])
	@B.post(_y)
	@C
	def AU(rid:str,p:Any=Depends(D))->dict[str,Any]:return review.sqj(A,rid,p[E])
	@B.get(_z)
	@C
	def AV(deployment:str,p:Any=Depends(D))->dict[str,Any]:return audit.dnu0(A,deployment)
	@B.get(_A0)
	@C
	def AW(deployment:str|_A=_A,p:Any=Depends(D))->list[dict[str,Any]]:return audit.ondp(A,deployment)
	@B.get(_A2)
	@C
	def AX(release_id:str,p:Any=Depends(D))->dict[str,Any]:B=release_id;C=audit.c0d(A,B);D=p[F]in vdtz and not p[G]or p[E]==C;return audit.ahm(A,B,with_text=D)
	@B.get(_A1)
	@C
	def AY(deployment:str,p:Any=Depends(D))->dict[str,Any]:return audit.uxrn(A,deployment)
	@B.get(_AG)
	@C
	def AZ()->dict[str,Any]:return A.events.heartbeat()
	@B.exception_handler(HTTPException)
	async def Aa(_:Request,e:HTTPException)->JSONResponse:return JSONResponse(status_code=e.status_code,content={O:e.detail})
	fw1(B);B.state.gate=A;return B
