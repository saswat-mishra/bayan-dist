from __future__ import annotations
_J='non_exportable'
_I='undeclared_field'
_H='sensitive_undeclared'
_G='row_level'
_F='freetext'
_E='direct_untransformed'
_D='quasi_untransformed'
_C='unratified_field'
_B=True
_A=None
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass,field
from typing import Any
from bayan_core.blg.brgs import mhbq,gkou
from bayan_core.blg2.oj2 import s9zz,f30
from bayan_core.blg2.dl9 import q66,fil6
from bayan_core.schema.g5v import lhkf,c5aj
from bayan_core.evxn.iuoq import vjs,ycf,f3w
from bayan_core.evxn.b3xe import ptt2,hndw,i4x
from bayan_core.evxn.aum2 import z2z,x99,r84,xd0,m2xr
from bayan_core.evxn.schema import sui,hh5,htz
from bayan_core.evxn.czq import z2z8,iij3
r46c=2
r982=_C,_D,_E,_F,_G,_H,_I,_J
@dataclass(frozen=_B)
class zn7:
	kind:str;field:str|_A
	def to_json(A)->dict[str,str|_A]:return{'kind':A.kind,'field':A.field}
def f12(dt:q66)->tuple[zn7,...]:
	C:list[zn7]=[]
	for A in dt.blockers:
		if A.reason==lhkf:B=_C
		elif A.field=='*':B=_G
		elif A.field_class=='UNDECLARED':B=_I
		elif A.reason.startswith('non-exportable'):B=_J
		elif A.field_class=='FREETEXT':B=_F
		elif A.field_class=='DIRECT':B=_E
		elif A.field_class=='QUASI':B=_D
		else:B=_H
		D=zn7(B,_A if A.field=='*'else A.field)
		if D not in C:C.append(D)
	return tuple(C)
@dataclass(frozen=_B)
class xtf8:
	name:str;version:str;bundle_digest:str;risk_class:str;max_grade_d:int;manifest:fil6;static_violations:tuple[z2z8,...];schema_errors:tuple[str,...];cap_reasons:tuple[zn7,...]=();lineage:Mapping[str,tuple[str,...]]=field(default_factory=dict)
	@property
	def certified(self)->bool:A=self;return not A.static_violations and not A.schema_errors and A.risk_class!='black'
def kmuy(spec:sui,ratified:frozenset[str]|_A=_A,sensitive_declared:frozenset[str]=frozenset(),classes:Mapping[str,c5aj]|_A=_A,*,source_classes:Mapping[str,c5aj]|_A=_A,tags:Mapping[str,frozenset[str]]|_A=_A)->tuple[fil6,x99,tuple[z2z8,...]]:
	H=source_classes;F=classes;B=spec;G:x99=r84(B.sql,{A.store:A.fields for A in B.inputs})if B.runtime=='sql'else{};N=frozenset(B for A in B.inputs for B in A.fields);D:Mapping[str,c5aj]=H if H is not _A else F or{};I:Mapping[str,frozenset[str]]=tags or{};J:dict[str,frozenset[str]]={};K:list[z2z8]=[]
	for A in B.output_schema.columns:
		C=set(G.get(A.name,frozenset()))
		if z2z in C or z2z in G:C=C-{z2z}|N
		E=xd0(D[A]for A in C if A in D);L=(F or{}).get(A.name,A.field_class)
		if E is not _A and m2xr(L)<m2xr(E):O=sorted(A for A in C if A in D and D[A]is E);K.append(z2z8('lineage_class',f"{A.name} derives from {", ".join(O)} ({E.value}) but is declared {L.value}: a column inherits the strictest class of its sources"))
		M=set(A.tags)|set(I.get(A.name,()))
		for P in C:M|=set(I.get(P,()))
		J[A.name]=frozenset(M)
	Q=htz(B.output_schema,ratified,sensitive_declared,classes=F,tags=J);return Q,G,tuple(K)
def l0zv(spec:sui,ratified:frozenset[str]|_A=_A,sensitive_declared:frozenset[str]=frozenset(),classes:Mapping[str,c5aj]|_A=_A,*,source_classes:Mapping[str,c5aj]|_A=_A,tags:Mapping[str,frozenset[str]]|_A=_A)->xtf8:A=spec;B,D,E=kmuy(A,ratified,sensitive_declared,classes,source_classes=source_classes,tags=tags);C=s9zz(B);return xtf8(A.name,A.version,hh5(A),f30(B),C.level,B,tuple(iij3(A))+E,tuple(A.output_schema.declaration_errors()),f12(C),{A:tuple(sorted(B-{z2z}))for(A,B)in D.items()if A!=z2z})
@dataclass(frozen=_B)
class wxn:rule:str;detail:str
@dataclass(frozen=_B)
class gty:
	rows:tuple[dict[str,Any],...];output_digest:str;input_digest:str;elapsed_s:float;quarantine:wxn|_A
	@property
	def conformant(self)->bool:return self.quarantine is _A
def mbf(conn:sqlite3.Connection,spec:sui,params:Mapping[str,Any],input_digest:str,limits:hndw|_A=_A)->gty:
	C=input_digest;A=spec;F=limits or hndw(max_rows=A.output_schema.max_rows)
	try:D=i4x(conn,A,params,F)
	except ptt2 as B:return gty((),'',C,.0,wxn('execution',str(B)))
	E=ycf(D.rows,A.output_schema)
	try:f3w(E,A.output_schema)
	except vjs as B:return gty((),'',C,D.elapsed_s,wxn(B.rule,B.detail))
	G=gkou(mhbq(E));return gty(tuple(E),G,C,D.elapsed_s,_A)
def j84(quarantine_count:int)->bool:return quarantine_count>=r46c
