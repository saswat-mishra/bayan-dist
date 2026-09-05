from __future__ import annotations
_A=None
import sqlite3,time
from collections.abc import Callable,Mapping,Sequence
from dataclasses import dataclass
from typing import Any
from bayan_core.sandbox.schema import SkillSpec
from bayan_core.sandbox.czq import ALLOWED_FUNCTIONS
class SegmentState:
	_fields=()
	def __init__(A,nbyci=_A):A._nbyci=nbyci or{}
	def hydrate(A,pdav):return A._nbyci.get(pdav)
	def settle_all(A):return tuple(sorted(A._nbyci))
class ExecutionError(Exception):pass
class LimitExceeded(ExecutionError):
	def __init__(B,limit:str,detail:str)->_A:A=limit;super().__init__(f"{A}: {detail}");B.limit=A
@dataclass(frozen=True)
class Limits:max_rows:int;timeout_s:float=3e1;heap_bytes:int=268435456
@dataclass(frozen=True)
class a51:rows:tuple[dict[str,Any],...];elapsed_s:float
def load_inputs(conn:sqlite3.Connection,inputs:Mapping[str,Sequence[Mapping[str,Any]]])->_A:
	A=conn
	for(D,B)in inputs.items():
		C=sorted({B for A in B for B in A});A.execute(f'CREATE TABLE "{D}" ({", ".join(f"{chr(34)}{A}{chr(34)}"for A in C)})')
		if B:A.executemany(f'INSERT INTO "{D}" VALUES ({", ".join("?"for A in C)})',[[A.get(B)for B in C]for A in B])
	A.commit()
def lxiv(spec:SkillSpec,real_tables:frozenset[str])->Callable[...,int]:
	C={A.store:set(A.fields)for A in spec.inputs};E={A.lower()for A in ALLOWED_FUNCTIONS}
	def A(action:int,arg1:Any,arg2:Any,dbname:Any,source:Any)->int:
		D=arg2;B=action;A=arg1
		if B==sqlite3.SQLITE_SELECT:return sqlite3.SQLITE_OK
		if B==sqlite3.SQLITE_READ:
			if A in C and(D==''or D in C[A]):return sqlite3.SQLITE_OK
			if source in C:return sqlite3.SQLITE_OK
			if A is _A or A==''or A not in real_tables:return sqlite3.SQLITE_OK
			return sqlite3.SQLITE_DENY
		if B==sqlite3.SQLITE_FUNCTION:return sqlite3.SQLITE_OK if str(D).lower()in E else sqlite3.SQLITE_DENY
		if B==sqlite3.SQLITE_RECURSIVE:return sqlite3.SQLITE_OK
		return sqlite3.SQLITE_DENY
	return A
def execute(conn:sqlite3.Connection,spec:SkillSpec,params:Mapping[str,Any],limits:Limits)->a51:
	K='prohibited';J='memory';F=params;E=spec;D=limits;A=conn;G=set(F)-set(E.params)
	if G:raise ExecutionError(f"undeclared parameters supplied: {sorted(G)}")
	A.row_factory=sqlite3.Row;L=frozenset(A[0]for A in A.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"));M=A.execute('PRAGMA query_only').fetchone()[0];A.execute('PRAGMA query_only = 1');A.execute('PRAGMA temp_store = MEMORY');H=int(A.execute('PRAGMA hard_heap_limit').fetchone()[0])
	if H==0 or H>D.heap_bytes:A.execute(f"PRAGMA hard_heap_limit = {int(D.heap_bytes)}")
	N=time.monotonic()+D.timeout_s
	def O()->int:return 1 if time.monotonic()>N else 0
	A.set_progress_handler(O,1000);A.set_authorizer(lxiv(E,L));P=time.monotonic()
	try:Q=A.execute(E.sql,dict(F));I=Q.fetchmany(D.max_rows+1)
	except MemoryError as C:raise LimitExceeded(J,f"skill exceeded {D.heap_bytes} bytes")from C
	except sqlite3.OperationalError as C:
		B=str(C)
		if'interrupted'in B:raise LimitExceeded('timeout',f"skill exceeded {D.timeout_s}s")from C
		if'out of memory'in B:raise LimitExceeded(J,f"skill exceeded {D.heap_bytes} bytes")from C
		if K in B or'not authorized'in B:raise ExecutionError(f"not authorized: {B}")from C
		raise ExecutionError(B)from C
	except sqlite3.DatabaseError as C:B=str(C);raise ExecutionError(f"not authorized: {B}"if'authorized'in B or K in B else B)from C
	finally:A.set_progress_handler(_A,0);A.set_authorizer(_A);A.execute(f"PRAGMA query_only = {int(M)}")
	if len(I)>D.max_rows:raise LimitExceeded('max_rows',f"skill emitted more than {D.max_rows} rows")
	R=tuple({B:A[B]for B in A.keys()}for A in I);return a51(R,time.monotonic()-P)