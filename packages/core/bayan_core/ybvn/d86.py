from __future__ import annotations
_C=False
_B=True
_A=None
from dataclasses import dataclass
from itertools import combinations
from typing import Any
from bayan_core.blg2.oj2 import s9zz,f30
from bayan_core.blg2.f2xo import pb0s
from bayan_core.blg2.dl9 import ble,im5,fil6,mgyg,c2v,gy0
from bayan_core.blg2.nf3 import apgg
from bayan_core.schema.g5v import c5aj
ijhh:dict[c5aj,tuple[tuple[gy0,dict[str,Any]],...]]={c5aj.DIRECT:((gy0.HMAC_ENCLAVE,{}),(gy0.DROP,{})),c5aj.QUASI:((gy0.COARSEN,{'granularity':'hour'}),(gy0.BUCKET,{'buckets':8}),(gy0.HMAC_ENCLAVE,{'k_floor':5}),(gy0.DROP,{})),c5aj.SENSITIVE:((gy0.DROP,{}),),c5aj.FREETEXT:((gy0.DROP,{}),),c5aj.STRUCTURAL:(),c5aj.VENDOR:()}
jc6=100
gdkj={'time':{gy0.COARSEN,gy0.BUCKET,gy0.DROP},'numeric':{gy0.BUCKET,gy0.ROUND,gy0.DROP},'identifier':{gy0.HMAC_ENCLAVE,gy0.DROP},'categorical':{gy0.HMAC_ENCLAVE,gy0.BUCKET,gy0.DROP}}
@dataclass(frozen=_B)
class k5yz:
	field:str;transform:gy0;params:tuple[tuple[str,Any],...]=()
	def describe(A)->str:B=', '.join(f"{A}={B}"for(A,B)in A.params);return f"{A.transform.value} {A.field}"+(f" ({B})"if B else'')
@dataclass(frozen=_B)
class bx3:
	changes:tuple[k5yz,...];reaches_target:bool;d:int;required_r:int;cost:int;loses:tuple[str,...];keeps:str;recommended:bool=_C
	def describe(A)->str:return' + '.join(A.describe()for A in A.changes)
@dataclass(frozen=_B)
class n4y:target_d:int;current_d:int;options:tuple[bx3,...];recommended:bx3|_A;unreachable_reason:str|_A;async_required:bool=_C
def ts62(f:im5,t:gy0)->str:return{gy0.COARSEN:f"keeps: coarse {f.name}",gy0.BUCKET:f"keeps: {f.name} distribution",gy0.HMAC_ENCLAVE:f"keeps: relative {f.name} frequency, loses identity",gy0.DROP:f"loses: {f.name}"}.get(t,'')
def mrg(m:fil6,option:bx3)->fil6:
	A=m
	for B in option.changes:
		C=A.field(B.field)
		if C is _A:raise KeyError(B.field)
		A=A.replace_field(C.with_transform(B.transform,**dict(B.params)))
	return A
def ob2(m:fil6,changes:tuple[k5yz,...],target:int,pol:mgyg,p_level:int)->bx3:
	C=changes;I=bx3(C,_C,0,0,0,(),'');D=mrg(m,I);E=s9zz(D);J=apgg(E.level,D,f30(D),pol,p_level);F=0;G:list[str]=[];H:list[str]=[]
	for A in C:
		B=m.field(A.field);assert B is not _A;F+=ble[A.transform]
		if A.transform is gy0.DROP and B.load_bearing:F+=jc6;G.append(B.name)
		H.append(ts62(B,A.transform))
	return bx3(C,E.level>=target,E.level,J,F,tuple(G),'; '.join(H))
def dsan(m:fil6,target_d:int,pol:mgyg,recipient:c2v,p_level:int=3)->n4y:
	A=target_d;B=s9zz(m).level
	if A>=3:return n4y(A,B,(),_A,'D3 and above require a pass over the actual extract; offered as an async job with an estimate, never as an interactive suggestion.',async_required=_B)
	if B>=A:return n4y(A,B,(),_A,_A)
	M=[A for A in pb0s(m,recipient,pol)if not A.passed];I=[A for A in M if not A.fixable_by_transformation and A.name!='ACCESS-LOCALITY']
	if I:G=I[0];return n4y(A,B,(),_A,f"{G.name} cannot be satisfied by transformation of the payload ({G.remedy_kind.replace("_"," ")}): {G.remedy}")
	N=s9zz(m).blockers;J=sorted({A.field for A in N if m.field(A.field)is not _A});E:dict[str,list[k5yz]]={}
	for H in J:F=m.field(H);assert F is not _A;K=gdkj.get(str(F.param('kind','')),_A);E[H]=[k5yz(H,A,tuple(sorted(B.items())))for(A,B)in ijhh[F.field_class]if A is not F.transform and(K is _A or A in K)]
	O=[(B,)for A in E.values()for B in A];P=[(C,D)for(A,B)in combinations(J,2)for C in E[A]for D in E[B]];L=[ob2(m,B,A,pol,p_level)for B in O+P];L.sort(key=lambda o:(not o.reaches_target,o.cost,len(o.changes),o.describe()));C=tuple(L);D=next((A for A in C if A.reaches_target),_A)
	if D is not _A:C=tuple(bx3(A.changes,A.reaches_target,A.d,A.required_r,A.cost,A.loses,A.keeps,recommended=A is D)for A in C);D=next(A for A in C if A.recommended)
	Q=_A if D else'no single- or double-field transformation reaches the target; the blocker is structural (row-level output, an unratified class, or an undeclared field) and needs a change to the skill, not a transformation.';return n4y(A,B,C,D,Q)
