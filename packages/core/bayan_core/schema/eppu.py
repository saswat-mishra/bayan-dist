from __future__ import annotations
_O='predicateType'
_N='key-enrolment'
_M='suspension-cleared'
_L='suspension'
_K='sensor-digest'
_J='pack-upgrade'
_I='certificate'
_H='receipt/v1'
_G='clearance/v1'
_F='release-request/v1'
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
from bayan_core.schema.yhzr import eksk,i2wi
qte={_B:'bayan.fingerprint.v1.schema.json',_C:'bayan.release-request.v2.schema.json',_D:'bayan.clearance.v2.schema.json',_E:'bayan.receipt.v2.schema.json',_I:'bayan.certificate.v1.schema.json',_J:'bayan.pack-upgrade.v1.schema.json',_K:'bayan.sensor-digest.v1.schema.json',_L:'bayan.suspension.v1.schema.json',_M:'bayan.suspension-cleared.v1.schema.json','sensor-event':'bayan.sensor-event.v1.schema.json',_N:'bayan.key-enrolment.v1.schema.json','acceptance':'bayan.acceptance.v1.schema.json',_F:'bayan.release-request.v1.schema.json',_G:'bayan.clearance.v1.schema.json',_H:'bayan.receipt.v1.schema.json'}
tcb=2
yul3={'https://bayan.dev/release-request/v2':_C,'https://bayan.dev/clearance/v2':_D,'https://bayan.dev/receipt/v2':_E,'https://bayan.dev/pack-upgrade/v1':_J,'https://bayan.dev/sensor-digest/v1':_K,'https://bayan.dev/suspension/v1':_L,'https://bayan.dev/suspension-cleared/v1':_M,'https://bayan.dev/key-enrolment/v1':_N,'https://bayan.dev/release-request/v1':_F,'https://bayan.dev/clearance/v1':_G,'https://bayan.dev/receipt/v1':_H}
wkw:tuple[str,...]=('transfer-gated','logged-tamper-evident','classified-and-handled','deidentified-declared','deidentified-verified','two-person-cleared','third-party-access-controlled','locality-enforced','change-controlled','disposal-bound','refusal-evidenced','budget-bounded')
def qciu(statement:dict[str,Any])->int|_A:
	B=str(statement.get(_O,''));A=yul3.get(B)
	if A is _A or A not in(_C,_D,_E,_F,_G,_H):return
	return 1 if A.endswith('/v1')else 2
@lru_cache(maxsize=_A)
def pth9(name:str)->dict[str,Any]:B=resources.files('bayan_core.schema').joinpath('schemas',qte[name]);A:dict[str,Any]=json.loads(B.read_text());Draft202012Validator.check_schema(A);return A
@lru_cache(maxsize=_A)
def mvtk(name:str)->Draft202012Validator:return Draft202012Validator(pth9(name))
def dy6(record:dict[str,Any])->list[str]:A=record;B=[A.message for A in mvtk(_B).iter_errors(A)];B+=[f"tier violation: {A} is tier {B} > declared sensitivity {C}"for(A,B,C)in eksk(A,pth9(_B))];return B
def vu5(statement:dict[str,Any],expected:str|_A=_A)->list[str]:
	D=statement;B=expected;C=D.get(_O);A=yul3.get(str(C))
	if A is _A:return[f"unknown predicateType {C!r}"]
	if B is not _A and A!=B:return[f"predicateType {C!r} is a {A}, expected {B}"]
	return[A.message for A in mvtk(A).iter_errors(D)]
def cjgr(certificate:dict[str,Any])->list[str]:return[f"{"/".join(str(A)for A in A.path)or"$"}: {A.message}"for A in mvtk(_I).iter_errors(certificate)]
def n24(schema:dict[str,Any])->list[str]:
	D=schema;B=i2wi(D);C:list[str]=[]
	for A in D.get('x-bayan-always',[]):
		if B.get(A,0)!=0:C.append(f"x-bayan-always field {A!r} is tier {B[A]}, must be 0")
	for A in D.get('required',[]):
		if B.get(A,0)!=0:C.append(f"required field {A!r} is tier {B[A]}, must be 0")
	for(F,G)in B.items():
		E=[B for(A,B)in B.items()if A.startswith(F+'.')]
		if E and G>min(E):C.append(f"container {F!r} is tier {G} but has a tier-{min(E)} child")
	return C
