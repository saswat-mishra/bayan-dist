from __future__ import annotations
_H='checkpoints/end.txt'
_G='releases'
_F='manifest'
_E='signature'
_D='consistency'
_C='flags'
_B='predicate'
_A=None
import base64,json
from collections.abc import Mapping
from dataclasses import dataclass,field
from datetime import datetime
from typing import Any
from bayan_core.blg.brgs import z9g,gkou
from bayan_core.blg.olon import x75
from bayan_core.blg.liw import f9cb,xb5i,u1a5
from bayan_core.blg.u7c9 import ray
from bayan_core.blg.dpd import q41,j9ft,gmfw
from bayan_core.zdb.mos import kyo,uz51
from bayan_verify.kd90 import srz,gx61,qrtm
cjp={_E:10,_F:60,'leaf':70,_D:70,'clearance':91,'index':93,_C:93}
@dataclass
class p4xr:
	steps:list[gx61]=field(default_factory=list);exit_code:int=0;releases:dict[str,Any]=field(default_factory=dict)
	def to_json(A)->dict[str,Any]:return{'exitCode':A.exit_code,'steps':[{'step':A.step,'name':A.name,'ok':A.ok,'detail':A.detail}for A in A.steps],_G:A.releases}
class b947(Exception):
	def __init__(A,code:int,detail:str)->_A:B=detail;super().__init__(B);A.code=code;A.detail=B
def v9d(files:Mapping[str,bytes],prefix:str)->dict[str,bytes]:
	E='checkpoint.txt';C=prefix;B=files;A={A[len(C)+1:]:B for(A,B)in B.items()if A.startswith(C+'/')}
	try:F=json.loads(f9cb.from_bytes(A['receipt.dsse']).payload)[_B]['ledger']['checkpoint'];A[E]=str(F).encode()
	except(KeyError,ValueError):A[E]=B[_H]
	for(D,G)in B.items():
		if D.startswith('pack/profile-'):A['trust/'+D[len('pack/'):]]=G
	A['trust/roster-snapshot.json']=B['roster-snapshot.json'];return A
def agr(files:Mapping[str,bytes],trust:ray,*,now:datetime|_A=_A)->p4xr:
	o='outcome';n='leafIndex';m='.jsonl';l='checkpoints/start.txt';k='gate';d='sensor/';c='hashes';b='pack.dsse';T='attention';S='manifest.json';E=trust;A=files;K=p4xr();P=0
	def C(name:str,detail:str)->_A:nonlocal P;K.steps.append(gx61(P,name,True,detail));P+=1
	try:
		if b not in A or S not in A:raise b947(10,'pack.dsse or manifest.json missing')
		try:e=u1a5(f9cb.from_bytes(A[b]),E,1,role=k,expected_payload_type=uz51)
		except(xb5i,ValueError)as L:raise b947(10,f"pack signature: {L}")from L
		if gkou(e.payload_bytes)!=gkou(sgk(A[S])):raise b947(10,'pack.dsse is not over this manifest.json')
		U=z9g(A[S]);C(_E,f"manifest signed by {sorted(e.signers)}");V=U['files'];p={A for A in A if A not in(S,b)}
		for(Q,q)in V.items():
			if Q not in A:raise b947(60,f"listed file {Q!r} missing")
			if gkou(A[Q])!=q:raise b947(60,f"{Q}: digest mismatch")
		f=sorted(p-set(V))
		if f:raise b947(60,f"file(s) not listed in the manifest: {f}")
		C(_F,f"{len(V)} files match; nothing else present");B=x75.parse(A[_H].decode());g={A.name for A in E.with_role('log')}
		if not B.verified_signers(E)&g:raise b947(70,'period-end checkpoint does not verify against the log key')
		if int(U['toSize'])!=B.size:raise b947(70,'manifest toSize differs from the period-end checkpoint')
		if l in A:
			F=x75.parse(A[l].decode());r=z9g(A['checkpoints/consistency.json']);s=[base64.b64decode(A)for A in r[c]]
			if not F.verified_signers(E)&g or F.origin!=B.origin:raise b947(70,'period-start checkpoint does not verify')
			if not j9ft(F.size,B.size,F.root,B.root,s):raise b947(70,f"consistency {F.size}→{B.size} fails: history rewritten")
			C(_D,f"tree at {F.size} is a prefix of the tree at {B.size}")
		else:C(_D,'period starts at the origin of the log; no prior checkpoint')
		G=z9g(A['index.json']);t=sorted({A.split('/',2)[1]for A in A if A.startswith(('releases/','refusals/'))});M:list[tuple[int,dict[str,Any]]]=[]
		for R in t:
			W=next(A.rsplit('/',1)[0]for A in A if A.startswith((f"releases/{R}/",f"refusals/{R}/")));H=int(R)
			if not int(U['fromSize'])<=H<B.size:raise b947(70,f"leaf {H} lies outside the period's tree range")
			N=A[f"{W}/clearance.dsse"];I=z9g(A[f"{W}/inclusion.json"])
			if int(I['treeSize'])!=B.size or not gmfw(q41(N),H,B.size,[base64.b64decode(A)for A in I[c]],B.root):raise b947(70,f"leaf {H}: inclusion proof does not fold to the period-end root")
			u=v9d(A,W);J=qrtm(u,E,now=now,artefacts_by_reference=True);K.releases[R]=J.to_json()
			if J.exit_code!=0:raise b947(91 if J.exit_code in(90,91,92,93,94)else J.exit_code,f"leaf {H}: {J.steps[-1].name}: {J.steps[-1].detail}")
			M.append((H,json.loads(f9cb.from_bytes(N).payload)))
		C('clearances',f"{len(M)} clearance(s) verify; each included at the period-end root");from bayan_core.blg.dpd import j24 as v;X=sorted(A[len(d):-len(m)]for A in A if A.startswith(d)and A.endswith(m))
		for D in X:
			if f"sensor/{D}.digest.dsse"not in A:raise b947(70,f"sensor hour {D} has no digest leaf in the pack")
			N=A[f"sensor/{D}.digest.dsse"]
			try:h=u1a5(f9cb.from_bytes(N),E,1,role=k)
			except(xb5i,ValueError)as L:raise b947(10,f"sensor digest {D}: {L}")from L
			i=[A for A in A[f"sensor/{D}.jsonl"].splitlines()if A.strip()];w=v([q41(A)for A in i]).hex()
			if h.statement[_B]['root']!=w or h.statement[_B]['events']!=len(i):raise b947(70,f"sensor hour {D}: the hour file does not fold to the digest leaf's root")
			I=z9g(A[f"sensor/{D}.inclusion.json"])
			if not gmfw(q41(N),int(I[n]),B.size,[base64.b64decode(A)for A in I[c]],B.root):raise b947(70,f"sensor hour {D}: digest leaf {I[n]} not included at the period-end root")
		C('sensor',f"{len(X)} sensor hour(s): hour files fold to their digest leaves; leaves included"if X else'no sensor hours in this period (sensorAbsent)');from bayan_core.zdb.mos import ue9 as x;Y=[int(A)for A in G.get('sensorHours',[])];Z=x(M,Y)
		if Z!=G['controls']:raise b947(93,'index.json controls do not re-derive from the included clearances')
		y=sorted(A for(A,B)in M if B[_B][o]=='release');a=sorted(A for(A,B)in M if B[_B][o]=='block')
		if G[_G]!=y or G['refusals']!=a:raise b947(93,'index.json release/refusal lists do not match the included leaves')
		C('index',f"control-ID-first index re-derives: {sum(len(A)for A in Z.values())} control id(s) across {sorted(Z)}");O={'zeroRefusals':not a,'zeroSensorEvents':not Y,'sensorAbsent':not any(A.startswith(d)for A in A),T:kyo if not a and not Y else _A}
		if G[_C]!=O:raise b947(93,f"flags asserted {G[_C]} but computed {O}")
		C(_C,'; '.join(f"{A}={B}"for(A,B)in O.items()if A!=T)+(f"; ATTENTION: {O[T]}"if O[T]else''))
	except b947 as j:K.steps.append(gx61(P,'pack',False,j.detail));K.exit_code=j.code
	return K
def sgk(manifest_bytes:bytes)->bytes:from bayan_core.blg.brgs import mhbq as A;return A(z9g(manifest_bytes))
