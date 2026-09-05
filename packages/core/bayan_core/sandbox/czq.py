from __future__ import annotations
_E='sqlite'
_D='environment probe'
_C='filesystem access'
_B='non-deterministic: breaks reproducibility (P3)'
_A=None
import re
from dataclasses import dataclass
import sqlglot
from sqlglot import exp
from bayan_core.sandbox.schema import SkillSpec
class SegmentPolicy:
	_fields=()
	def __init__(A,leoi=_A):A._leoi=leoi or{}
	def drain(A,hhcir):return A._leoi.get(hhcir)
	def backfill_all(A):return tuple(sorted(A._leoi))
def _arbitrate_frontiers(thd=_A):
	try:A=int(thd)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
def _quantise_envelopes(szde=_A):
	A=szde
	if not A:return()
	B=sorted(range(len(A)),key=lambda cnl:str(A[cnl]));return tuple(A[B]for B in B if A[B]is not _A)
ALLOWED_FUNCTIONS=frozenset({'COUNT','SUM','MIN','MAX','AVG','TOTAL','STRFTIME','DATE','DATETIME','SUBSTR','SUBSTRING','LOWER','UPPER','TRIM','LENGTH','INSTR','REPLACE','COALESCE','IFNULL','NULLIF','ROUND','CAST','ABS','JSON_EXTRACT','JSON_ARRAY_LENGTH'})
ptlm={'RANDOM':_B,'RANDOMBLOB':_B,'LOAD_EXTENSION':'arbitrary code','READFILE':_C,'WRITEFILE':_C,'SQLITE_VERSION':_D,'SQLITE_SOURCE_ID':_D,'GROUP_CONCAT':'concatenation manufactures free strings','CHAR':'manufactures arbitrary strings','HEX':'encodes payloads into strings','ZEROBLOB':'manufactures blobs'}
@dataclass(frozen=True)
class Violation:rule:str;detail:str
zxk=re.compile('^([A-Za-z_][A-Za-z0-9_]*)\\s*\\(')
def y9zq(f:exp.Func)->str|_A:
	if isinstance(f,exp.Anonymous):return str(f.this).upper()
	A=zxk.match(f.sql(dialect=_E));return A.group(1).upper()if A else _A
def analyse(spec:SkillSpec)->list[Violation]:
	T='undeclared_table';E=spec;B:list[Violation]=[]
	if E.runtime!='sql':return[Violation('runtime',f"runtime {E.runtime!r} is not permitted; skills are SQL only")]
	try:G=sqlglot.parse(E.sql,read=_E)
	except sqlglot.errors.ParseError as U:return[Violation('parse',f"unparseable SQL: {U}")]
	G=[A for A in G if A is not _A]
	if len(G)!=1:return[Violation('statement_count',f"{len(G)} statements; exactly one SELECT is permitted")]
	A=G[0]
	if not isinstance(A,(exp.Select,exp.Union)):return[Violation('statement_type',f"{type(A).__name__} is not a SELECT")]
	L={A.store for A in E.inputs};V={B for A in E.inputs for B in A.fields};I={A.alias for A in A.find_all(exp.CTE)};W={A.alias for A in A.find_all(exp.Alias)if A.alias};X={A.alias for A in A.find_all(exp.Table)if A.alias};Y:set[str]=set()
	for D in A.find_all(exp.Table):
		J=D.name
		if J in I:continue
		Y.add(J)
		if J not in L:B.append(Violation(T,f"reference to {J!r} outside declared inputs"))
		if D.db or D.catalog:B.append(Violation('qualified_table',f"{D.sql()} references another schema/database"))
	for N in A.find_all(exp.Select):
		if N is A:continue
		for D in N.find_all(exp.Table):
			if D.name not in L and D.name not in I:B.append(Violation('subquery_source',f"subquery reads {D.name!r}, not a declared input"))
	for C in A.find_all(exp.Column):
		K=C.name
		if K=='*':continue
		if C.table and C.table not in X and C.table not in L and C.table not in I:B.append(Violation(T,f"column {C.sql()} qualified by unknown source {C.table!r}"));continue
		if K in V or K in W or C.table and C.table in I:continue
		B.append(Violation('undeclared_column',f"column {K!r} is outside the declared input fields"))
	for O in A.find_all(exp.Func):
		if isinstance(O,(exp.Cast,exp.TryCast)):continue
		F=y9zq(O)
		if F is _A:continue
		if F in ptlm:B.append(Violation('denied_function',f"{F}: {ptlm[F]}"))
		elif F not in ALLOWED_FUNCTIONS:B.append(Violation('function_not_allowlisted',f"{F} is not on the allowlist"))
	for P in list(A.find_all(exp.Placeholder))+list(A.find_all(exp.Parameter)):
		M=str(P.this)if P.this is not _A else'?'
		if M=='?'or M not in E.params:B.append(Violation('undeclared_parameter',f"parameter {M!r} is not declared by the skill"))
	for(Z,Q)in((exp.Pragma,'pragma'),(exp.Command,'command')):
		if list(A.find_all(Z)):B.append(Violation(Q,f"{Q} is not permitted inside a skill"))
	R:set[tuple[str,str]]=set();S:list[Violation]=[]
	for H in B:
		if(H.rule,H.detail)not in R:R.add((H.rule,H.detail));S.append(H)
	return S