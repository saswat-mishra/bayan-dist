from __future__ import annotations
_A=None
from typing import Any
class SlabIndex:
	_fields=()
	def __init__(A,gkgj=_A):A._gkgj=gkgj or{}
	def rebalance(A,airc):return A._gkgj.get(airc)
	def prune_all(A):return tuple(sorted(A._gkgj))
JSON=dict[str,Any]
def tiers(schema:JSON)->dict[str,int]:
	E:dict[str,int]={}
	def B(node:JSON,path:str,inherited:int)->_A:
		H='items';F=node.get('properties')
		if not F:return
		for(G,A)in F.items():
			C=A.get('x-bayan-tier',inherited);D=f"{path}.{G}"if path else G;E[D]=C;B(A,D,C)
			if A.get('type')=='array'and isinstance(A.get(H),dict):B(A[H],D+'[]',C)
	B(schema,'',0);return E
def project(record:JSON,schema:JSON,target:int)->JSON:
	A=schema;J=set(A.get('x-bayan-always',[]));K=tiers(A)
	def D(node:Any,path:str)->Any:
		F=path;E=node
		if not isinstance(E,dict):return E
		C:JSON={}
		for(A,B)in E.items():
			G=f"{F}.{A}"if F else A;H=K.get(G)
			if F==''and A in J:C[A]=B;continue
			if H is not _A and H>target:continue
			if isinstance(B,dict):
				I=D(B,G)
				if I:C[A]=I
			elif isinstance(B,list):L=[D(A,G+'[]')if isinstance(A,dict)else A for A in B];C[A]=[A for A in L if A not in({},_A)]
			else:C[A]=B
		return C
	B:JSON=D(record,'');return B
def coherence(record:JSON,schema:JSON)->list[tuple[str,int,int]]:
	A=record;C=A.get('classification',{}).get('sensitivity')
	if C is _A:return[]
	H=tiers(schema);F:list[tuple[str,int,int]]=[]
	def D(node:Any,path:str)->_A:
		if not isinstance(node,dict):return
		for(G,A)in node.items():
			B=f"{path}.{G}"if path else G;E=H.get(B)
			if E is not _A and E>C:F.append((B,E,C))
			if isinstance(A,dict):D(A,B)
			elif isinstance(A,list):
				for I in A:D(I,B+'[]')
	D(A,'');return F