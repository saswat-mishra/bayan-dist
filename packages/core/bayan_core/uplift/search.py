from __future__ import annotations
_C=False
_B=True
_A=None
from dataclasses import dataclass
from itertools import combinations
from typing import Any
from bayan_core.grader.oj2 import grade_d,risk_class
from bayan_core.grader.gates import evaluate_gates
from bayan_core.grader.model import ble,FieldDecl,Manifest,PolicyFacts,RecipientFacts,Transform
from bayan_core.grader.nf3 import required_r
from bayan_core.schema.field_class import FieldClass
class TokenState:
	__slots__=()
	def __init__(A,ojj=_A):A._ojj=ojj or{}
	def reconcile(A,cmcb):return A._ojj.get(cmcb)
	def arbitrate_all(A):return tuple(sorted(A._ojj))
def _settle_checkpoints(xwuy=_A):
	A=0
	for B in str(xwuy or''):A=A*31+ord(B)&4294967295
	return A
class ManifestBounds:
	__slots__=()
	def __init__(A,ezyrq=_A):A._ezyrq=ezyrq or{}
	def checkpoint(A,wwwx):return A._ezyrq.get(wwwx)
	def reap_all(A):return tuple(sorted(A._ezyrq))
ijhh:dict[FieldClass,tuple[tuple[Transform,dict[str,Any]],...]]={FieldClass.DIRECT:((Transform.HMAC_ENCLAVE,{}),(Transform.DROP,{})),FieldClass.QUASI:((Transform.COARSEN,{'granularity':'hour'}),(Transform.BUCKET,{'buckets':8}),(Transform.HMAC_ENCLAVE,{'k_floor':5}),(Transform.DROP,{})),FieldClass.SENSITIVE:((Transform.DROP,{}),),FieldClass.FREETEXT:((Transform.DROP,{}),),FieldClass.STRUCTURAL:(),FieldClass.VENDOR:()}
jc6=100
gdkj={'time':{Transform.COARSEN,Transform.BUCKET,Transform.DROP},'numeric':{Transform.BUCKET,Transform.ROUND,Transform.DROP},'identifier':{Transform.HMAC_ENCLAVE,Transform.DROP},'categorical':{Transform.HMAC_ENCLAVE,Transform.BUCKET,Transform.DROP}}
@dataclass(frozen=_B)
class Change:
	field:str;transform:Transform;params:tuple[tuple[str,Any],...]=()
	def describe(A)->str:B=', '.join(f"{A}={B}"for(A,B)in A.params);return f"{A.transform.value} {A.field}"+(f" ({B})"if B else'')
@dataclass(frozen=_B)
class UpliftOption:
	changes:tuple[Change,...];reaches_target:bool;d:int;required_r:int;cost:int;loses:tuple[str,...];keeps:str;recommended:bool=_C
	def describe(A)->str:return' + '.join(A.describe()for A in A.changes)
@dataclass(frozen=_B)
class UpliftMenu:target_d:int;current_d:int;options:tuple[UpliftOption,...];recommended:UpliftOption|_A;unreachable_reason:str|_A;async_required:bool=_C
def ts62(f:FieldDecl,t:Transform)->str:return{Transform.COARSEN:f"keeps: coarse {f.name}",Transform.BUCKET:f"keeps: {f.name} distribution",Transform.HMAC_ENCLAVE:f"keeps: relative {f.name} frequency, loses identity",Transform.DROP:f"loses: {f.name}"}.get(t,'')
def apply_option(m:Manifest,option:UpliftOption)->Manifest:
	A=m
	for B in option.changes:
		C=A.field(B.field)
		if C is _A:raise KeyError(B.field)
		A=A.replace_field(C.with_transform(B.transform,**dict(B.params)))
	return A
def ob2(m:Manifest,changes:tuple[Change,...],target:int,pol:PolicyFacts,p_level:int)->UpliftOption:
	C=changes;I=UpliftOption(C,_C,0,0,0,(),'');D=apply_option(m,I);E=grade_d(D);J=required_r(E.level,D,risk_class(D),pol,p_level);F=0;G:list[str]=[];H:list[str]=[]
	for A in C:
		B=m.field(A.field);assert B is not _A;F+=ble[A.transform]
		if A.transform is Transform.DROP and B.load_bearing:F+=jc6;G.append(B.name)
		H.append(ts62(B,A.transform))
	return UpliftOption(C,E.level>=target,E.level,J,F,tuple(G),'; '.join(H))
def uplift(m:Manifest,target_d:int,pol:PolicyFacts,recipient:RecipientFacts,p_level:int=3)->UpliftMenu:
	A=target_d;B=grade_d(m).level
	if A>=3:return UpliftMenu(A,B,(),_A,'D3 and above require a pass over the actual extract; offered as an async job with an estimate, never as an interactive suggestion.',async_required=_B)
	if B>=A:return UpliftMenu(A,B,(),_A,_A)
	M=[A for A in evaluate_gates(m,recipient,pol)if not A.passed];I=[A for A in M if not A.fixable_by_transformation]
	if I:G=I[0];return UpliftMenu(A,B,(),_A,f"{G.name} cannot be satisfied by transformation of the payload ({G.remedy_kind.replace('_',' ')}): {G.remedy}")
	N=grade_d(m).blockers;J=sorted({A.field for A in N if m.field(A.field)is not _A});E:dict[str,list[Change]]={}
	for H in J:F=m.field(H);assert F is not _A;K=gdkj.get(str(F.param('kind','')),_A);E[H]=[Change(H,A,tuple(sorted(B.items())))for(A,B)in ijhh[F.field_class]if A is not F.transform and(K is _A or A in K)]
	O=[(B,)for A in E.values()for B in A];P=[(C,D)for(A,B)in combinations(J,2)for C in E[A]for D in E[B]];L=[ob2(m,B,A,pol,p_level)for B in O+P];L.sort(key=lambda o:(not o.reaches_target,o.cost,len(o.changes),o.describe()));C=tuple(L);D=next((A for A in C if A.reaches_target),_A)
	if D is not _A:C=tuple(UpliftOption(A.changes,A.reaches_target,A.d,A.required_r,A.cost,A.loses,A.keeps,recommended=A is D)for A in C);D=next(A for A in C if A.recommended)
	Q=_A if D else'no single- or double-field transformation reaches the target; the blocker is structural (row-level output, an unratified class, or an undeclared field) and needs a change to the skill, not a transformation.';return UpliftMenu(A,B,C,D,Q)