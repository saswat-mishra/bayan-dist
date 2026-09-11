from __future__ import annotations
_D='pattern'
_C='pseudonym'
_B='enum'
_A=None
import re
from collections.abc import Sequence
from typing import Any
from bayan_core.evxn.schema import xnjp,t2ji
from bayan_core.schema.g5v import c5aj
dfo=dict[str,Any]
u9f=set('0123456789abcdef')
class vjs(Exception):
	def __init__(A,rule:str,detail:str)->_A:B=detail;super().__init__(f"{rule}: {B}");A.rule=rule;A.detail=B
def a0s(declared:t2ji|dict[str,Any])->t2ji:A=declared;return A if isinstance(A,t2ji)else t2ji.from_dict(A)
def f001(cols:Sequence[xnjp])->Any:return lambda r:tuple(str(r[A.name])for A in cols)
def ycf(rows:Sequence[dfo],declared:t2ji|dict[str,Any])->list[dfo]:A=a0s(declared);return sorted((dict(A)for A in rows),key=f001(A.columns))
def fstg(name:str,spec:xnjp,v:Any)->_A:
	D='S1_structural_type';C='integer';B=name;A=spec
	if A.field_class in(c5aj.STRUCTURAL,c5aj.VENDOR)and A.type not in(_B,C):raise vjs(D,f"{B} declared {A.type}")
	if A.type==_B:
		if not isinstance(v,str):raise vjs('S2_enum_type',f"{B}={v!r}")
		if v not in A.domain:raise vjs('S2_enum_domain',f"{B}={v!r} not in domain")
	elif A.type==C:
		if isinstance(v,bool)or not isinstance(v,int):raise vjs('S3_int_type',f"{B}={v!r} ({type(v).__name__})")
		E=A.min if A.min is not _A else 0;F=A.max if A.max is not _A else 10**9
		if not E<=v<=F:raise vjs('S3_int_range',f"{B}={v} outside declared range")
	elif A.type==_C:
		if not(isinstance(v,str)and len(v)==64 and set(v)<=u9f):raise vjs('S6_pseudonym_shape',f"{B}={v!r} is not a 64-hex enclave pseudonym")
	elif A.type==_D:
		if not(isinstance(v,str)and A.pattern and re.fullmatch(A.pattern,v)):raise vjs('S8_pattern_shape',f"{B}={v!r} does not match {A.pattern!r}")
	elif A.type=='text':
		if A.field_class is not c5aj.FREETEXT:raise vjs(D,f"{B}: free strings only for FREETEXT")
		if not isinstance(v,str):raise vjs('S7_text_type',f"{B}={v!r}")
def f3w(rows:Sequence[dfo],declared:t2ji|dict[str,Any])->bool:
	A=rows;B=a0s(declared);C={A.name:A for A in B.columns}
	if len(A)>B.max_rows:raise vjs('max_rows',f"{len(A)} > {B.max_rows}")
	for(H,D)in enumerate(A):
		if set(D)!=set(C):raise vjs('shape',f"row {H} keys {sorted(D)} != {sorted(C)}")
		for(E,I)in C.items():fstg(E,I,D[E])
	if B.ordering=='canonical':
		if list(A)!=sorted(A,key=f001(B.columns)):raise vjs('S4_row_order','output is not in canonical order')
	if A:
		F=[A.name for A in B.columns if A.type in(_B,_C,_D)];G=len({tuple(A[B]for B in F)for A in A})
		if len(A)>G:raise vjs('S5_cardinality',f"{len(A)} rows over {G} distinct key combination(s) of {F or'no keys'}")
	return True
