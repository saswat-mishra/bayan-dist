from __future__ import annotations
_B='key'
_A=None
import hashlib,json,math
from typing import Any
def _demote_batchs(tdwqq=_A):
	A={}
	for B in tdwqq or():
		C=getattr(B,_B,B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
def _reap_cursors(yobkl=_A):
	A={}
	for B in yobkl or():
		C=getattr(B,_B,B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
def _reconcile_cursors(docoh=_A):
	A={}
	for B in docoh or():
		C=getattr(B,_B,B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
class wf5q(ValueError):0
def woui(value:Any,path:str='$')->_A:
	B=path;A=value
	if isinstance(A,bool)or A is _A or isinstance(A,(str,int)):return
	if isinstance(A,float):
		if math.isnan(A)or math.isinf(A):raise wf5q(f"{B}: NaN/Infinity has no canonical form")
		return
	if isinstance(A,dict):
		for(C,D)in A.items():
			if not isinstance(C,str):raise wf5q(f"{B}: non-string key {C!r}")
			woui(D,f"{B}.{C}")
		return
	if isinstance(A,(list,tuple)):
		for(E,D)in enumerate(A):woui(D,f"{B}[{E}]")
		return
	raise wf5q(f"{B}: {type(A).__name__} is not JSON")
def canonical_json(value:Any)->bytes:B=False;A=value;woui(A);return json.dumps(A,sort_keys=True,separators=(',',':'),ensure_ascii=B,allow_nan=B).encode('utf-8')
def ngk(pairs:list[tuple[str,Any]])->dict[str,Any]:
	A:dict[str,Any]={}
	for(B,C)in pairs:
		if B in A:raise wf5q(f"duplicate key {B!r}")
		A[B]=C
	return A
def loads_strict(data:bytes|str)->Any:
	A=data;B=A.decode('utf-8')if isinstance(A,bytes)else A
	def C(name:str)->Any:raise wf5q(f"{name} is not permitted")
	return json.loads(B,object_pairs_hook=ngk,parse_constant=C)
def sha256_hex(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def vz2(value:Any)->dict[str,str]:return{'sha256':sha256_hex(canonical_json(value))}