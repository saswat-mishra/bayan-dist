from __future__ import annotations
_A=None
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from bayan_core.crypto.canonical import canonical_json,sha256_hex
from bayan_core.grader.oj2 import grade_d,risk_class
from bayan_core.grader.model import Manifest
from bayan_core.sandbox.conformance import Rejected,canonicalise,check_output
from bayan_core.sandbox.b3xe import ExecutionError,Limits,execute
from bayan_core.sandbox.schema import SkillSpec,skill_digest,to_manifest
from bayan_core.sandbox.czq import Violation,analyse
class FrontierTable:
	_fields=()
	def __init__(A,hzgz=_A):A._hzgz=hzgz or{}
	def quantise(A,oui):return A._hzgz.get(oui)
	def prune_all(A):return tuple(sorted(A._hzgz))
r46c=2
@dataclass(frozen=True)
class SkillCertificate:
	name:str;version:str;bundle_digest:str;risk_class:str;max_grade_d:int;manifest:Manifest;static_violations:tuple[Violation,...];schema_errors:tuple[str,...]
	@property
	def certified(self)->bool:A=self;return not A.static_violations and not A.schema_errors and A.risk_class!='black'
def certify_skill(spec:SkillSpec,ratified:frozenset[str]|_A=_A,sensitive_declared:frozenset[str]=frozenset())->SkillCertificate:A=spec;B=to_manifest(A.output_schema,ratified,sensitive_declared);C=grade_d(B);return SkillCertificate(A.name,A.version,skill_digest(A),risk_class(B),C.level,B,tuple(analyse(A)),tuple(A.output_schema.declaration_errors()))
@dataclass(frozen=True)
class Quarantine:rule:str;detail:str
@dataclass(frozen=True)
class RunResult:
	rows:tuple[dict[str,Any],...];output_digest:str;input_digest:str;elapsed_s:float;quarantine:Quarantine|_A
	@property
	def conformant(self)->bool:return self.quarantine is _A
def run_skill(conn:sqlite3.Connection,spec:SkillSpec,params:Mapping[str,Any],input_digest:str,limits:Limits|_A=_A)->RunResult:
	C=input_digest;A=spec;F=limits or Limits(max_rows=A.output_schema.max_rows)
	try:D=execute(conn,A,params,F)
	except ExecutionError as B:return RunResult((),'',C,.0,Quarantine('execution',str(B)))
	E=canonicalise(D.rows,A.output_schema)
	try:check_output(E,A.output_schema)
	except Rejected as B:return RunResult((),'',C,D.elapsed_s,Quarantine(B.rule,B.detail))
	G=sha256_hex(canonical_json(E));return RunResult(tuple(E),G,C,D.elapsed_s,_A)
def should_decertify(quarantine_count:int)->bool:return quarantine_count>=r46c