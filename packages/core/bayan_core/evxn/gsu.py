from __future__ import annotations
_A=None
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from bayan_core.blg.brgs import mhbq,gkou
from bayan_core.blg2.oj2 import s9zz,f30
from bayan_core.blg2.dl9 import fil6
from bayan_core.evxn.iuoq import vjs,ycf,f3w
from bayan_core.evxn.b3xe import ptt2,hndw,i4x
from bayan_core.evxn.schema import sui,hh5,htz
from bayan_core.evxn.czq import z2z8,iij3
r46c=2
@dataclass(frozen=True)
class xtf8:
	name:str;version:str;bundle_digest:str;risk_class:str;max_grade_d:int;manifest:fil6;static_violations:tuple[z2z8,...];schema_errors:tuple[str,...]
	@property
	def certified(self)->bool:A=self;return not A.static_violations and not A.schema_errors and A.risk_class!='black'
def l0zv(spec:sui,ratified:frozenset[str]|_A=_A,sensitive_declared:frozenset[str]=frozenset())->xtf8:A=spec;B=htz(A.output_schema,ratified,sensitive_declared);C=s9zz(B);return xtf8(A.name,A.version,hh5(A),f30(B),C.level,B,tuple(iij3(A)),tuple(A.output_schema.declaration_errors()))
@dataclass(frozen=True)
class wxn:rule:str;detail:str
@dataclass(frozen=True)
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
