from __future__ import annotations
_H='ratified_at'
_G='ratifiedBy'
_F='deployment'
_E='name'
_D='ratified_by'
_C='class'
_B='field'
_A=None
import base64,json,sqlite3,time
from typing import Any
from bayan_core.blg import mhbq
from bayan_gate.i7m5 import b8d,u5fa,oy60
kz3i='bayan.field-class-ratification.v1'
def x0l(t:int|_A)->str|_A:return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(t))if t else _A
def y7z(row:sqlite3.Row)->tuple[set[str],set[str]]:A=json.loads(row['spec']);B={B for A in A.get('inputs',[])for B in A.get('fields',[])};C={A[_E]for A in json.loads(row['output_schema']).get('columns',[])};return B,C
def qaw(gate:b8d,dep_id:str,field:str,ratified:bool)->dict[str,Any]:
	F='version';C=field;D,B=[],[]
	for A in gate.db.execute('SELECT * FROM skill WHERE deployment_id=? AND decertified=0 ORDER BY name',(dep_id,)):
		G,E=y7z(A)
		if C in G or C in E:D.append(f"{A[_E]}@{A[F]}")
		if C in E and not ratified:B.append(f"{A[_E]}@{A[F]}")
	return{'skills':D,'cappedAtD1':B,'text':f"{len(B)} skill(s) capped at D1 until ratified"if B else'no skill is capped by this field'}
def qrp(gate:b8d,r:sqlite3.Row)->dict[str,Any]:C='signature';B='deployment_id';A=gate;D=A.deployment(r[B]);E=A.packs[D['pack_id']].field_default(r[_B])or{};return{_F:r[B],_B:r[_B],_C:r[_C],'proposedBy':r['proposed_by'],_G:r[_D],'ratifiedAt':x0l(r[_H]),'ratified':r[_D]is not _A,C:r[C],'guidance':E,'impact':qaw(A,r[B],r[_B],r[_D]is not _A)}
def d2i(gate:b8d,dep_id:str)->list[dict[str,Any]]:B=dep_id;A=gate;A.deployment(B);C=A.db.execute('SELECT * FROM field_class WHERE deployment_id=? ORDER BY (ratified_by IS NOT NULL), field',(B,)).fetchall();return[qrp(A,B)for B in C]
def q223(*,deployment:str,field:str,cls:str,ratified_by:str,at:str)->bytes:return mhbq({'schema':kz3i,_F:deployment,_B:field,_C:cls,_G:ratified_by,'at':at})
def e0f(gate:b8d,dep_id:str,field:str,actor:str)->dict[str,Any]:
	I='SELECT * FROM field_class WHERE deployment_id=? AND field=?';E=actor;C=field;B=dep_id;A=gate;from bayan_gate import v6y as J;F=A.principal(E)
	if F['role']!='dba':raise u5fa(403,'only the data owner (role dba) ratifies a field class')
	D=A.db.execute(I,(B,C)).fetchone()
	if D is _A:raise u5fa(404,f"{C!r} is not a declared column of {B}")
	if D[_D]is not _A:raise u5fa(409,f"{C!r} was already ratified by {D[_D]} on {x0l(D[_H])}")
	G=oy60();K=base64.b64encode(A.keys.get(F['key_name']).sign(q223(deployment=B,field=C,cls=D[_C],ratified_by=E,at=G))).decode()
	with A.tx:A.db.execute('UPDATE field_class SET ratified_by=?, ratified_at=?, signature=? WHERE deployment_id=? AND field=?',(E,int(time.time()),K,B,C));H=J.x3n(A.db,B,A.ratified(B))
	A.events.emit('field-class-ratified',deployment=B,field=C,cls=D[_C],by=E,at=G,recertified=[A['skill']for A in H if A['before']!=A['after']]);L=A.db.execute(I,(B,C)).fetchone();return{**qrp(A,L),'recertified':H}
