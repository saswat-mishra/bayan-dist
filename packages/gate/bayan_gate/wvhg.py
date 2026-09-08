from __future__ import annotations
_N='recertified'
_M='before'
_L='key_name'
_K='previousClass'
_J='reason'
_I='ratified_at'
_H='ratifiedBy'
_G='deployment'
_F='name'
_E='SELECT * FROM field_class WHERE deployment_id=? AND field=?'
_D='field'
_C='ratified_by'
_B='class'
_A=None
import base64,json,sqlite3,time
from typing import Any
from bayan_core.blg import mhbq
from bayan_gate.i7m5 import b8d,u5fa,oy60
kz3i='bayan.field-class-ratification.v1'
def x0l(t:int|_A)->str|_A:return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(t))if t else _A
def y7z(row:sqlite3.Row)->tuple[set[str],set[str]]:A=json.loads(row['spec']);B={B for A in A.get('inputs',[])for B in A.get('fields',[])};C={A[_F]for A in json.loads(row['output_schema']).get('columns',[])};return B,C
def qaw(gate:b8d,dep_id:str,field:str,ratified:bool)->dict[str,Any]:
	F='version';C=field;D,A=[],[]
	for B in gate.db.execute('SELECT * FROM skill WHERE deployment_id=? AND decertified=0 ORDER BY name',(dep_id,)):
		G,E=y7z(B)
		if C in G or C in E:D.append(f"{B[_F]}@{B[F]}")
		if C in E and not ratified:A.append(f"{B[_F]}@{B[F]}")
	return{'skills':D,'cappedAtD1':A,'text':f"{len(A)} skill(s) capped at D1 until ratified"if A else'no skill is capped by this field','text_ar':f"{len(A)} مهارة/مهارات مقيّدة عند D1 حتى التصديق"if A else'لا مهارة مقيّدة بهذا الحقل'}
def qrp(gate:b8d,r:sqlite3.Row)->dict[str,Any]:C='signature';B='deployment_id';A=gate;D=A.deployment(r[B]);E=A.packs[D['pack_id']].field_default(r[_D])or{};return{_G:r[B],_D:r[_D],_B:r[_B],'proposedBy':r['proposed_by'],_H:r[_C],'ratifiedByName':A.principal(r[_C])['display_name']if r[_C]else _A,'ratifiedAt':x0l(r[_I]),'ratified':r[_C]is not _A,C:r[C],'guidance':E,'impact':qaw(A,r[B],r[_D],r[_C]is not _A)}
def d2i(gate:b8d,dep_id:str)->list[dict[str,Any]]:B=dep_id;A=gate;A.deployment(B);C=A.db.execute('SELECT * FROM field_class WHERE deployment_id=? ORDER BY (ratified_by IS NOT NULL), field',(B,)).fetchall();return[qrp(A,B)for B in C]
def q223(*,deployment:str,field:str,cls:str,ratified_by:str,at:str,reason:str|_A=_A,previous:str|_A=_A)->bytes:
	B=reason;A:dict[str,Any]={'schema':kz3i,_G:deployment,_D:field,_B:cls,_H:ratified_by,'at':at}
	if B is not _A:A[_J]=B;A[_K]=previous
	return mhbq(A)
def e0f(gate:b8d,dep_id:str,field:str,actor:str)->dict[str,Any]:
	E=actor;C=field;B=dep_id;A=gate;from bayan_gate import v6y as I;F=A.principal(E)
	if F['role']!='dba':raise u5fa(403,'only the data owner (role dba) ratifies a field class')
	D=A.db.execute(_E,(B,C)).fetchone()
	if D is _A:raise u5fa(404,f"{C!r} is not a declared column of {B}")
	if D[_C]is not _A:raise u5fa(409,f"{C!r} was already ratified by {D[_C]} on {x0l(D[_I])}")
	G=oy60();J=base64.b64encode(A.keys.get(F[_L]).sign(q223(deployment=B,field=C,cls=D[_B],ratified_by=E,at=G))).decode()
	with A.tx:A.db.execute('UPDATE field_class SET ratified_by=?, ratified_at=?, signature=? WHERE deployment_id=? AND field=?',(E,int(time.time()),J,B,C));H=I.x3n(A.db,B,A.ratified(B),A.field_classes(B))
	A.events.emit('field-class-ratified',deployment=B,field=C,cls=D[_B],by=E,at=G,recertified=[A['skill']for A in H if A[_M]!=A['after']]);K=A.db.execute(_E,(B,C)).fetchone();return{**qrp(A,K),_N:H}
def zsr(gate:b8d,dep_id:str,field:str,actor:str,cls:str,reason:str)->dict[str,Any]:
	G=reason;F=actor;C=field;B=dep_id;A=gate;from bayan_core.schema.g5v import c5aj as I;from bayan_gate import v6y as L;J=A.principal(F)
	if J['role']!='dba':raise u5fa(403,'only the data owner (role dba) reclassifies a field')
	try:E=I(cls).value
	except ValueError as M:raise u5fa(422,f"{cls!r} is not a field class; choose one of {", ".join(A.value for A in I)}")from M
	if len(G.strip())<20:raise u5fa(422,'a reclassification needs a typed reason of at least 20 characters')
	D=A.db.execute(_E,(B,C)).fetchone()
	if D is _A:raise u5fa(404,f"{C!r} is not a declared column of {B}")
	if D[_B]==E and D[_C]is not _A:raise u5fa(409,f"{C!r} is already ratified as {E}; ratify or choose a different class")
	H=oy60();N=base64.b64encode(A.keys.get(J[_L]).sign(q223(deployment=B,field=C,cls=E,ratified_by=F,at=H,reason=G.strip(),previous=D[_B]))).decode()
	with A.tx:A.db.execute('UPDATE field_class SET class=?, ratified_by=?, ratified_at=?, signature=? WHERE deployment_id=? AND field=?',(E,F,int(time.time()),N,B,C));K=L.x3n(A.db,B,A.ratified(B),A.field_classes(B))
	A.events.emit('field-class-reclassified',deployment=B,field=C,**{'from':D[_B],'to':E},reason=G.strip(),by=F,at=H,recertified=[A['skill']for A in K if A[_M]!=A['after']]);O=A.db.execute(_E,(B,C)).fetchone();return{**qrp(A,O),_N:K,_K:D[_B],_J:G.strip(),'at':H}
