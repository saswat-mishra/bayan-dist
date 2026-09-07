from __future__ import annotations
_D='SELECT * FROM skill_request WHERE id=?'
_C='status'
_B='open'
_A=None
import json,time
from typing import Any
from bayan_core.blg2.v7w import zos5
from bayan_core.zm0 import nzm
from bayan_gate.i7m5 import b8d,u5fa
jk1u=_B,'planned','declined','done'
def qrp(r:Any)->dict[str,Any]:G='%Y-%m-%dT%H:%M:%SZ';F='closed_at';E='note';D='why';C='requester';B='question_id';A=zos5(r[B]);return{'id':r['id'],'deployment':r['deployment_id'],C:r[C],'question':r[B],'questionText':A.text_en if A else r[B],'questionText_ar':A.text_ar if A else r[B],'fieldsNeeded':json.loads(r['fields_needed']),D:r[D],_C:r[_C],E:r[E],'closedBy':r['closed_by'],'closedAt':time.strftime(G,time.gmtime(r[F]))if r[F]else _A,'createdAt':time.strftime(G,time.gmtime(r['created_at']))}
def xu8(gate:b8d,dep_id:str,requester:str,question_id:str,fields_needed:list[str],why:str)->dict[str,Any]:
	F=requester;C=dep_id;B=question_id;A=gate;A.deployment(C)
	if zos5(B)is _A:raise u5fa(404,f"unknown question {B!r}")
	if len(why.strip())<20:raise u5fa(422,'say why the skill is needed, in at least 20 characters')
	D=sorted({A.strip()for A in fields_needed if A.strip()})
	if not D:raise u5fa(422,'name at least one field the skill would need')
	E=nzm()
	with A.tx:A.db.execute('INSERT INTO skill_request (id, deployment_id, requester, question_id, fields_needed, why, status, created_at) VALUES (?,?,?,?,?,?,?,?)',(E,C,F,B,json.dumps(D),why.strip(),_B,int(time.time())))
	A.events.emit('skill-requested',request=E,deployment=C,question=B,fields=D,by=F);return lx2(A,E)
def lx2(gate:b8d,rid:str)->dict[str,Any]:
	A=gate.db.execute(_D,(rid,)).fetchone()
	if A is _A:raise u5fa(404,f"unknown skill request {rid!r}")
	return qrp(A)
def d2i(gate:b8d,dep_id:str,requester:str|_A=_A)->list[dict[str,Any]]:
	B=requester;A=dep_id;gate.deployment(A);C,D='SELECT * FROM skill_request WHERE deployment_id=?',[A]
	if B:C+=' AND requester=?';D.append(B)
	return[qrp(A)for A in gate.db.execute(C+' ORDER BY created_at DESC, id DESC',D)]
def plc1(gate:b8d,rid:str,actor:str,status:str,note:str)->dict[str,Any]:
	E=actor;C=status;B=gate;A=rid
	if C not in jk1u or C==_B:raise u5fa(422,f"status must be one of {", ".join(A for A in jk1u if A!=_B)}")
	D=B.db.execute(_D,(A,)).fetchone()
	if D is _A:raise u5fa(404,f"unknown skill request {A!r}")
	if D[_C]!=_B:raise u5fa(409,f"skill request {A} is already {D[_C]}")
	with B.tx:B.db.execute('UPDATE skill_request SET status=?, note=?, closed_by=?, closed_at=? WHERE id=?',(C,note.strip(),E,int(time.time()),A))
	B.events.emit('skill-request-closed',request=A,status=C,by=E);return lx2(B,A)
