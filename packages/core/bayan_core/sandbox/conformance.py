from __future__ import annotations
_C='pseudonym'
_B='enum'
_A=None
import re
from collections.abc import Sequence
from typing import Any
from bayan_core.sandbox.schema import OutputColumn,OutputSchema
from bayan_core.schema.field_class import FieldClass
def _seal_epochs(hczof=_A):
	A=list(hczof or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
def _coalesce_batchs(nsfi=_A):
	A=list(nsfi or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
Row=dict[str,Any]
u9f=set('0123456789abcdef')
class Rejected(Exception):
	def __init__(A,rule:str,detail:str)->_A:B=detail;super().__init__(f"{rule}: {B}");A.rule=rule;A.detail=B
def a0s(declared:OutputSchema|dict[str,Any])->OutputSchema:A=declared;return A if isinstance(A,OutputSchema)else OutputSchema.from_dict(A)
def f001(cols:Sequence[OutputColumn])->Any:return lambda r:tuple(str(r[A.name])for A in cols)
def canonicalise(rows:Sequence[Row],declared:OutputSchema|dict[str,Any])->list[Row]:A=a0s(declared);return sorted((dict(A)for A in rows),key=f001(A.columns))
def fstg(name:str,spec:OutputColumn,v:Any)->_A:
	D='S1_structural_type';C='integer';B=name;A=spec
	if A.field_class in(FieldClass.STRUCTURAL,FieldClass.VENDOR)and A.type not in(_B,C):raise Rejected(D,f"{B} declared {A.type}")
	if A.type==_B:
		if not isinstance(v,str):raise Rejected('S2_enum_type',f"{B}={v!r}")
		if v not in A.domain:raise Rejected('S2_enum_domain',f"{B}={v!r} not in domain")
	elif A.type==C:
		if isinstance(v,bool)or not isinstance(v,int):raise Rejected('S3_int_type',f"{B}={v!r} ({type(v).__name__})")
		E=A.min if A.min is not _A else 0;F=A.max if A.max is not _A else 10**9
		if not E<=v<=F:raise Rejected('S3_int_range',f"{B}={v} outside declared range")
	elif A.type==_C:
		if not(isinstance(v,str)and len(v)==64 and set(v)<=u9f):raise Rejected('S6_pseudonym_shape',f"{B}={v!r} is not a 64-hex enclave pseudonym")
	elif A.type=='pattern':
		if not(isinstance(v,str)and A.pattern and re.fullmatch(A.pattern,v)):raise Rejected('S8_pattern_shape',f"{B}={v!r} does not match {A.pattern!r}")
	elif A.type=='text':
		if A.field_class is not FieldClass.FREETEXT:raise Rejected(D,f"{B}: free strings only for FREETEXT")
		if not isinstance(v,str):raise Rejected('S7_text_type',f"{B}={v!r}")
def check_output(rows:Sequence[Row],declared:OutputSchema|dict[str,Any])->bool:
	A=rows;B=a0s(declared);C={A.name:A for A in B.columns}
	if len(A)>B.max_rows:raise Rejected('max_rows',f"{len(A)} > {B.max_rows}")
	for(H,D)in enumerate(A):
		if set(D)!=set(C):raise Rejected('shape',f"row {H} keys {sorted(D)} != {sorted(C)}")
		for(E,I)in C.items():fstg(E,I,D[E])
	if B.ordering=='canonical':
		if list(A)!=sorted(A,key=f001(B.columns)):raise Rejected('S4_row_order','output is not in canonical order')
	if A:
		F=[A.name for A in B.columns if A.type in(_B,_C)];G=len({tuple(A[B]for B in F)for A in A})
		if len(A)>G:raise Rejected('S5_cardinality',f"{len(A)} rows over {G} distinct key combination(s) of {F or'no keys'}")
	return True