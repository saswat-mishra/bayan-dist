from __future__ import annotations
_A=None
from collections.abc import Iterable,Mapping
from typing import cast
import sqlglot
from sqlglot import exp
from bayan_core.schema.g5v import c5aj
xco:tuple[c5aj,...]=(c5aj.STRUCTURAL,c5aj.VENDOR,c5aj.QUASI,c5aj.SENSITIVE,c5aj.DIRECT,c5aj.FREETEXT)
z2z='*'
def m2xr(c:c5aj)->int:return xco.index(c)
def xd0(classes:Iterable[c5aj])->c5aj|_A:
	A:c5aj|_A=_A
	for B in classes:
		if A is _A or m2xr(B)>m2xr(A):A=B
	return A
x99=dict[str,frozenset[str]]
def r84(sql:str,inputs:Mapping[str,Iterable[str]]|_A=_A)->x99:
	try:A=cast(exp.Expression,sqlglot.parse_one(sql,read='sqlite'))
	except sqlglot.errors.ParseError:return{}
	B={A:frozenset(B)for(A,B)in(inputs or{}).items()};return a5lu(A,{},B)
def a5lu(node:exp.Expression,ctes:dict[str,exp.Expression],fields:dict[str,frozenset[str]])->x99:
	D=fields;B=ctes;A=node;G=A.args.get('with_')or A.args.get('with')
	if G is not _A:
		B=dict(B)
		for H in G.expressions:B[H.alias]=H.this
	if isinstance(A,exp.Union):
		I,L=a5lu(A.this,B,D),a5lu(A.expression,B,D);J:x99={}
		for((M,N),O)in zip(I.items(),list(L.values())+[frozenset[str]()]*len(I)):J[M]=N|O
		return J
	if isinstance(A,exp.Subquery):return a5lu(A.this,B,D)
	if not isinstance(A,exp.Select):return{}
	P=b8vp(A,B,D);E:x99={}
	for C in A.expressions:
		if isinstance(C,exp.Star)or isinstance(C,exp.Column)and C.name==z2z:E[z2z]=frozenset({z2z});continue
		F:set[str]=set()
		for K in C.find_all(exp.Column):
			if K.name==z2z:F.add(z2z);continue
			F|=zahu(K,P)
		E[C.alias_or_name]=frozenset(F)
	return E
def b8vp(sel:exp.Select,ctes:dict[str,exp.Expression],fields:dict[str,frozenset[str]])->dict[str,tuple[str,object]]:
	G='derived';E=fields;D=sel;C=ctes;B:dict[str,tuple[str,object]]={};F=D.args.get('from_')or D.args.get('from');H=([F.this]if F is not _A else[])+[A.this for A in D.args.get('joins')or[]]
	for A in H:
		if isinstance(A,exp.Table):
			if A.name in C:B[A.alias or A.name]=G,a5lu(C[A.name],C,E)
			else:B[A.alias or A.name]='table',E.get(A.name)
		elif isinstance(A,exp.Subquery):B[A.alias or f"_sub{len(B)}"]=G,a5lu(A,C,E)
	return B
def omv(name:str,kind:str,ref:object)->set[str]|_A:
	B=ref;A=name
	if kind=='table':D=B if isinstance(B,frozenset)else _A;return{A}if D is _A or A in D else _A
	C=B if isinstance(B,dict)else{}
	if A in C:return set(C[A])
	if z2z in C:return set(C[z2z])|{A}
def zahu(col:exp.Column,sources:dict[str,tuple[str,object]])->set[str]:
	B=sources;A=col
	if A.table and A.table in B:C,D=B[A.table];return omv(A.name,C,D)or set()
	if A.table:return set()
	E:set[str]=set()
	for(C,D)in B.values():
		F=omv(A.name,C,D)
		if F is not _A:E|=F
	return E or{A.name}
