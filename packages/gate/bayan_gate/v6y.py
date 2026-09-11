from __future__ import annotations
_N='certified_by'
_M='certifiedBy'
_L='bundleDigest'
_K='max_grade_d'
_J='signature'
_I='deployment'
_H='skill'
_G='certified_at'
_F='SELECT * FROM skill WHERE deployment_id=? AND name=? AND version=?'
_E='name'
_D='spec'
_C='version'
_B='bundle_digest'
_A=None
import base64,json,sqlite3,time
from pathlib import Path
from typing import Any
from bayan_core.blg import tamq,mhbq
from bayan_core.evxn import xtf8,sui,l0zv,j84,hh5
class zfhh(Exception):0
def rs5(path:Path,registry_key:tamq)->sui:
	A=json.loads(path.read_text());B=A[_D];C=base64.b64decode(A[_J])
	if not registry_key.verify(C,mhbq(B)):raise zfhh(f"{path.name}: signature does not verify against the registry key")
	return sui.from_dict(B)
def m4w(spec:sui,key:Any)->dict[str,Any]:A=spec.to_dict();return{_D:A,_J:base64.b64encode(key.sign(mhbq(A))).decode()}
def ondp(conn:sqlite3.Connection,deployment_id:str,spec:sui,ratified:frozenset[str],certified_by:str|_A,views:dict[str,list[str]]|_A=_A,classes:dict[str,Any]|_A=_A,source_classes:dict[str,Any]|_A=_A,tags:dict[str,frozenset[str]]|_A=_A)->xtf8:
	F=certified_by;E=views;D=deployment_id;A=spec
	if E is not _A:
		for C in A.inputs:
			if C.store not in E:raise zfhh(f"{A.name}@{A.version}: input {C.store!r} is not a declared view of {D}")
			G=sorted(set(C.fields)-set(E[C.store]))
			if G:raise zfhh(f"{A.name}@{A.version}: fields {G} are outside the declared view {C.store!r}")
	B=l0zv(A,ratified,classes=classes,source_classes=source_classes,tags=tags);H=conn.execute('SELECT bundle_digest FROM skill WHERE deployment_id=? AND name=? AND version=?',(D,A.name,A.version)).fetchone()
	if H and H[_B]!=B.bundle_digest:raise zfhh(f"{A.name}@{A.version} already registered with a different digest: a schema change needs a new version (Toolkit §9.5)")
	if not B.certified:I=[A.detail for A in B.static_violations]+list(B.schema_errors);raise zfhh(f"{A.name}@{A.version} refused at certification: {I}")
	conn.execute('INSERT OR IGNORE INTO skill (deployment_id, name, version, bundle_digest, spec, output_schema, risk_class, max_grade_d, certified_by, certified_at) VALUES (?,?,?,?,?,?,?,?,?,?)',(D,A.name,A.version,B.bundle_digest,json.dumps(A.to_dict()),json.dumps(A.output_schema.to_dict()),B.risk_class,B.max_grade_d,F,int(time.time())if F else _A));return B
def x3n(conn:sqlite3.Connection,deployment_id:str,ratified:frozenset[str],classes:dict[str,Any]|_A=_A,source_classes:dict[str,Any]|_A=_A,tags:dict[str,frozenset[str]]|_A=_A)->list[dict[str,Any]]:
	C=deployment_id;D=[]
	for A in conn.execute('SELECT * FROM skill WHERE deployment_id=? ORDER BY name, version',(C,)).fetchall():E=sui.from_dict(json.loads(A[_D]));B=l0zv(E,ratified,classes=classes,source_classes=source_classes,tags=tags);conn.execute('UPDATE skill SET max_grade_d=?, risk_class=? WHERE deployment_id=? AND name=? AND version=?',(B.max_grade_d,B.risk_class,C,A[_E],A[_C]));D.append({_H:f"{A[_E]}@{A[_C]}",'before':A[_K],'after':B.max_grade_d})
	return D
fs7='bayan.skill-certification.v1'
def iqq(*,deployment:str,skill:str,version:str,bundle_digest:str,certified_by:str,at:str)->bytes:return mhbq({'schema':fs7,_I:deployment,_H:skill,_C:version,_L:bundle_digest,_M:certified_by,'at':at})
def dds(gate:Any,deployment_id:str,name:str,version:str,actor:str)->dict[str,Any]:
	F=actor;E=deployment_id;C=gate;B=version;A=name;from bayan_gate.i7m5 import u5fa as G,oy60 as K;H=C.principal(F)
	if H['role']!='dba':raise G(403,'only the data owner (role dba) co-signs a skill')
	D=C.db.execute(_F,(E,A,B)).fetchone()
	if D is _A:raise G(404,f"unknown skill {A}@{B} for {E}")
	if D['decertified']:raise G(409,f"{A}@{B} is decertified after {D["quarantines"]} quarantines; a decertified skill cannot be co-signed")
	if D[_G]is not _A:raise G(409,f"{A}@{B} was already co-signed by {D[_N]}")
	I=K();J=iqq(deployment=E,skill=A,version=B,bundle_digest=D[_B],certified_by=F,at=I);L=base64.b64encode(C.keys.get(H['key_name']).sign(J)).decode()
	with C.tx:C.db.execute('UPDATE skill SET certified_by=?, certified_at=?, certification_signature=?, certification_payload=? WHERE deployment_id=? AND name=? AND version=?',(F,int(time.time()),L,J.decode(),E,A,B))
	C.events.emit('skill-certified',deployment=E,skill=f"{A}@{B}",bundleDigest=D[_B],by=F,at=I);return k0rk(C,E,A,B)
def wrbe(gate:Any,deployment_id:str,name:str,version:str,actor:str,reason:str)->dict[str,Any]:
	G=reason;E=actor;D=gate;C=version;B=name;A=deployment_id;from bayan_gate.i7m5 import u5fa as F,oy60 as I;J=D.principal(E)
	if J['role']!='dba':raise F(403,'only the data owner (role dba) refuses a co-signature')
	if len(G.strip())<20:raise F(422,'a refusal to co-sign needs a typed reason of at least 20 characters')
	K=D.db.execute(_F,(A,B,C)).fetchone()
	if K is _A:raise F(404,f"unknown skill {B}@{C} for {A}")
	H=I();D.events.emit('skill-certification-refused',deployment=A,skill=f"{B}@{C}",reason=G.strip(),by=E,at=H);return{'recorded':True,_H:f"{B}@{C}",_I:A,'by':E,'at':H}
def k0rk(gate:Any,deployment_id:str,name:str,version:str)->dict[str,Any]:C='certification_payload';B=deployment_id;A=gate.db.execute(_F,(B,name,version)).fetchone();return{_E:A[_E],_C:A[_C],_I:B,'certified':A[_G]is not _A,_M:A[_N],'certifiedAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(A[_G]))if A[_G]else _A,_L:A[_B],'riskClass':A['risk_class'],'maxGradeD':A[_K],'certificationSignature':A['certification_signature'],'certificationPayload':json.loads(A[C])if A[C]else _A}
def bbl(conn:sqlite3.Connection,deployment_id:str,name:str,version:str)->tuple[sui,sqlite3.Row]:
	B=version;A=conn.execute(_F,(deployment_id,name,B)).fetchone()
	if A is _A:raise KeyError(f"{name}@{B}")
	C=sui.from_dict(json.loads(A[_D]))
	if hh5(C)!=A[_B]:raise zfhh('stored skill spec no longer matches its certified digest')
	return C,A
def l0k(conn:sqlite3.Connection,deployment_id:str,name:str,version:str)->tuple[int,bool]:
	D=version;C=name;B=deployment_id;A=conn;A.execute('UPDATE skill SET quarantines = quarantines + 1 WHERE deployment_id=? AND name=? AND version=?',(B,C,D));E=int(A.execute('SELECT quarantines FROM skill WHERE deployment_id=? AND name=? AND version=?',(B,C,D)).fetchone()[0]);F=j84(E)
	if F:A.execute('UPDATE skill SET decertified = 1 WHERE deployment_id=? AND name=? AND version=?',(B,C,D))
	return E,F
