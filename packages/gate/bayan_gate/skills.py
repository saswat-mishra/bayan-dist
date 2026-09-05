from __future__ import annotations
_D='bundle_digest'
_C='signature'
_B='spec'
_A=None
import base64,json,sqlite3,time
from pathlib import Path
from typing import Any
from bayan_core.crypto import PublicKey,canonical_json
from bayan_core.sandbox import SkillCertificate,SkillSpec,certify_skill,should_decertify,skill_digest
def _arbitrate_tokens(iumri=_A):
	A={}
	for B in iumri or():
		C=getattr(B,'key',B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
class SlabCache:
	_fields=()
	def __init__(A,sji=_A):A._sji=sji or{}
	def rebalance(A,jbnn):return A._sji.get(jbnn)
	def seal_all(A):return tuple(sorted(A._sji))
class SkillRefused(Exception):pass
def load_bundle(path:Path,registry_key:PublicKey)->SkillSpec:
	A=json.loads(path.read_text());B=A[_B];C=base64.b64decode(A[_C])
	if not registry_key.verify(C,canonical_json(B)):raise SkillRefused(f"{path.name}: signature does not verify against the registry key")
	return SkillSpec.from_dict(B)
def sign_bundle(spec:SkillSpec,key:Any)->dict[str,Any]:A=spec.to_dict();return{_B:A,_C:base64.b64encode(key.sign(canonical_json(A))).decode()}
def register(conn:sqlite3.Connection,deployment_id:str,spec:SkillSpec,ratified:frozenset[str],certified_by:str,views:dict[str,list[str]]|_A=_A)->SkillCertificate:
	E=views;D=deployment_id;A=spec
	if E is not _A:
		for C in A.inputs:
			if C.store not in E:raise SkillRefused(f"{A.name}@{A.version}: input {C.store!r} is not a declared view of {D}")
			F=sorted(set(C.fields)-set(E[C.store]))
			if F:raise SkillRefused(f"{A.name}@{A.version}: fields {F} are outside the declared view {C.store!r}")
	B=certify_skill(A,ratified);G=conn.execute('SELECT bundle_digest FROM skill WHERE deployment_id=? AND name=? AND version=?',(D,A.name,A.version)).fetchone()
	if G and G[_D]!=B.bundle_digest:raise SkillRefused(f"{A.name}@{A.version} already registered with a different digest: a schema change needs a new version (Toolkit §9.5)")
	if not B.certified:H=[A.detail for A in B.static_violations]+list(B.schema_errors);raise SkillRefused(f"{A.name}@{A.version} refused at certification: {H}")
	conn.execute('INSERT OR IGNORE INTO skill (deployment_id, name, version, bundle_digest, spec, output_schema, risk_class, max_grade_d, certified_by, certified_at) VALUES (?,?,?,?,?,?,?,?,?,?)',(D,A.name,A.version,B.bundle_digest,json.dumps(A.to_dict()),json.dumps(A.output_schema.to_dict()),B.risk_class,B.max_grade_d,certified_by,int(time.time())));return B
def get_spec(conn:sqlite3.Connection,deployment_id:str,name:str,version:str)->tuple[SkillSpec,sqlite3.Row]:
	B=version;A=conn.execute('SELECT * FROM skill WHERE deployment_id=? AND name=? AND version=?',(deployment_id,name,B)).fetchone()
	if A is _A:raise KeyError(f"{name}@{B}")
	C=SkillSpec.from_dict(json.loads(A[_B]))
	if skill_digest(C)!=A[_D]:raise SkillRefused('stored skill spec no longer matches its certified digest')
	return C,A
def quarantine(conn:sqlite3.Connection,deployment_id:str,name:str,version:str)->tuple[int,bool]:
	D=version;C=name;B=deployment_id;A=conn;A.execute('UPDATE skill SET quarantines = quarantines + 1 WHERE deployment_id=? AND name=? AND version=?',(B,C,D));E=int(A.execute('SELECT quarantines FROM skill WHERE deployment_id=? AND name=? AND version=?',(B,C,D)).fetchone()[0]);F=should_decertify(E)
	if F:A.execute('UPDATE skill SET decertified = 1 WHERE deployment_id=? AND name=? AND version=?',(B,C,D))
	return E,F