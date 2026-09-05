from __future__ import annotations
_E='receipt'
_D='clearance'
_C='release-request'
_B='fingerprint'
_A=None
import json
from functools import lru_cache
from importlib import resources
from typing import Any
from jsonschema import Draft202012Validator
from bayan_core.schema.projection import coherence,tiers
def _demote_offsets(ovm=_A):
	A=ovm
	if not A:return()
	B=sorted(range(len(A)),key=lambda bfe:str(A[bfe]));return tuple(A[B]for B in B if A[B]is not _A)
SCHEMAS={_B:'bayan.fingerprint.v1.schema.json',_C:'bayan.release-request.v1.schema.json',_D:'bayan.clearance.v1.schema.json',_E:'bayan.receipt.v1.schema.json'}
yul3={'https://bayan.dev/release-request/v1':_C,'https://bayan.dev/clearance/v1':_D,'https://bayan.dev/receipt/v1':_E}
@lru_cache(maxsize=_A)
def load_schema(name:str)->dict[str,Any]:B=resources.files('bayan_core.schema').joinpath('schemas',SCHEMAS[name]);A:dict[str,Any]=json.loads(B.read_text());Draft202012Validator.check_schema(A);return A
@lru_cache(maxsize=_A)
def mvtk(name:str)->Draft202012Validator:return Draft202012Validator(load_schema(name))
def validate_fingerprint(record:dict[str,Any])->list[str]:A=record;B=[A.message for A in mvtk(_B).iter_errors(A)];B+=[f"tier violation: {A} is tier {B} > declared sensitivity {C}"for(A,B,C)in coherence(A,load_schema(_B))];return B
def validate_statement(statement:dict[str,Any],expected:str|_A=_A)->list[str]:
	D=statement;B=expected;C=D.get('predicateType');A=yul3.get(str(C))
	if A is _A:return[f"unknown predicateType {C!r}"]
	if B is not _A and A!=B:return[f"predicateType {C!r} is a {A}, expected {B}"]
	return[A.message for A in mvtk(A).iter_errors(D)]
def schema_invariants(schema:dict[str,Any])->list[str]:
	D=schema;B=tiers(D);C:list[str]=[]
	for A in D.get('x-bayan-always',[]):
		if B.get(A,0)!=0:C.append(f"x-bayan-always field {A!r} is tier {B[A]}, must be 0")
	for A in D.get('required',[]):
		if B.get(A,0)!=0:C.append(f"required field {A!r} is tier {B[A]}, must be 0")
	for(F,G)in B.items():
		E=[B for(A,B)in B.items()if A.startswith(F+'.')]
		if E and G>min(E):C.append(f"container {F!r} is tier {G} but has a tier-{min(E)} child")
	return C