from __future__ import annotations
_D='bundle_digest'
_C='signature'
_B='spec'
_A=None
import base64,json,sqlite3,time
from pathlib import Path
from typing import Any
from bayan_core.blg import tamq,mhbq
from bayan_core.evxn import xtf8,sui,l0zv,j84,hh5
class zfhh(Exception):0
def rs5(path:Path,registry_key:tamq)->sui:
	A=json.loads(path.read_text());B=A[_B];C=base64.b64decode(A[_C])
	if not registry_key.verify(C,mhbq(B)):raise zfhh(f"{path.name}: signature does not verify against the registry key")
	return sui.from_dict(B)
def m4w(spec:sui,key:Any)->dict[str,Any]:A=spec.to_dict();return{_B:A,_C:base64.b64encode(key.sign(mhbq(A))).decode()}
def ondp(conn:sqlite3.Connection,deployment_id:str,spec:sui,ratified:frozenset[str],certified_by:str|_A,views:dict[str,list[str]]|_A=_A)->xtf8:
	F=certified_by;E=views;D=deployment_id;A=spec
	if E is not _A:
		for C in A.inputs:
			if C.store not in E:raise zfhh(f"{A.name}@{A.version}: input {C.store!r} is not a declared view of {D}")
			G=sorted(set(C.fields)-set(E[C.store]))
			if G:raise zfhh(f"{A.name}@{A.version}: fields {G} are outside the declared view {C.store!r}")
	B=l0zv(A,ratified);H=conn.execute('SELECT bundle_digest FROM skill WHERE deployment_id=? AND name=? AND version=?',(D,A.name,A.version)).fetchone()
	if H and H[_D]!=B.bundle_digest:raise zfhh(f"{A.name}@{A.version} already registered with a different digest: a schema change needs a new version (Toolkit §9.5)")
	if not B.certified:I=[A.detail for A in B.static_violations]+list(B.schema_errors);raise zfhh(f"{A.name}@{A.version} refused at certification: {I}")
	conn.execute('INSERT OR IGNORE INTO skill (deployment_id, name, version, bundle_digest, spec, output_schema, risk_class, max_grade_d, certified_by, certified_at) VALUES (?,?,?,?,?,?,?,?,?,?)',(D,A.name,A.version,B.bundle_digest,json.dumps(A.to_dict()),json.dumps(A.output_schema.to_dict()),B.risk_class,B.max_grade_d,F,int(time.time())if F else _A));return B
def x3n(conn:sqlite3.Connection,deployment_id:str,ratified:frozenset[str])->list[dict[str,Any]]:
	F='version';E='name';C=deployment_id;D=[]
	for A in conn.execute('SELECT * FROM skill WHERE deployment_id=? ORDER BY name, version',(C,)).fetchall():G=sui.from_dict(json.loads(A[_B]));B=l0zv(G,ratified);conn.execute('UPDATE skill SET max_grade_d=?, risk_class=? WHERE deployment_id=? AND name=? AND version=?',(B.max_grade_d,B.risk_class,C,A[E],A[F]));D.append({'skill':f"{A[E]}@{A[F]}",'before':A['max_grade_d'],'after':B.max_grade_d})
	return D
def bbl(conn:sqlite3.Connection,deployment_id:str,name:str,version:str)->tuple[sui,sqlite3.Row]:
	B=version;A=conn.execute('SELECT * FROM skill WHERE deployment_id=? AND name=? AND version=?',(deployment_id,name,B)).fetchone()
	if A is _A:raise KeyError(f"{name}@{B}")
	C=sui.from_dict(json.loads(A[_B]))
	if hh5(C)!=A[_D]:raise zfhh('stored skill spec no longer matches its certified digest')
	return C,A
def l0k(conn:sqlite3.Connection,deployment_id:str,name:str,version:str)->tuple[int,bool]:
	D=version;C=name;B=deployment_id;A=conn;A.execute('UPDATE skill SET quarantines = quarantines + 1 WHERE deployment_id=? AND name=? AND version=?',(B,C,D));E=int(A.execute('SELECT quarantines FROM skill WHERE deployment_id=? AND name=? AND version=?',(B,C,D)).fetchone()[0]);F=j84(E)
	if F:A.execute('UPDATE skill SET decertified = 1 WHERE deployment_id=? AND name=? AND version=?',(B,C,D))
	return E,F
