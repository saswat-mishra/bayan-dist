from __future__ import annotations
_O='key-enrolment'
_N='reviewer'
_M='approvedBy'
_L='authority'
_K='pending'
_J='leafIndex'
_I='active'
_H='public_key'
_G='status'
_F='genesis'
_E='keyName'
_D='principal'
_C='id'
_B='key_name'
_A=None
import base64,sqlite3,time
from typing import Any
from bayan_core.blg import tamq,kf3
from bayan_core.c339 import xbf
from bayan_gate.i7m5 import b8d,u5fa,oy60
def p5f(gate:b8d,principal:str|_A=_A)->list[dict[str,Any]]:B='leaf_index';A=principal;C='SELECT * FROM key_enrolment'+(' WHERE principal_id=?'if A else'')+' ORDER BY requested_at, key_name';return[{_D:A['principal_id'],_E:A[_B],'publicKey':A[_H],_F:bool(A[_F]),'requestedAt':A['requested_at'],_M:A['approved_by'],'approvedAt':A['approved_at'],_J:A[B],_G:_I if A[B]is not _A else _K}for A in gate.db.execute(C,(A,)if A else())]
def e5d1(gate:b8d,p:sqlite3.Row)->str:A=p[_B].split('.')[0];B=gate.db.execute('SELECT COUNT(*) FROM key_enrolment WHERE principal_id=?',(p[_C],)).fetchone()[0];return A if B==0 else f"{A}.{B+1}"
def le9(gate:b8d,principal:str,public_key_b64:str)->dict[str,Any]:
	C=public_key_b64;B=principal;A=gate;E=A.principal(B)
	if E['role']!=_N:raise u5fa(422,"key enrolment is for reviewers; other principals' keys stay gate-held in this build (DEVIATIONS.md)")
	try:tamq.from_b64(C)
	except ValueError as F:raise u5fa(422,f"not an Ed25519 public key: {F}")from F
	if A.db.execute('SELECT 1 FROM key_enrolment WHERE public_key=?',(C,)).fetchone():raise u5fa(409,'this public key is already enrolled')
	G=A.db.execute('SELECT key_name FROM key_enrolment WHERE principal_id=? AND leaf_index IS NULL',(B,)).fetchone()
	if G:raise u5fa(409,f"an enrolment ({G[_B]}) is already awaiting approval")
	D=e5d1(A,E)
	with A.tx:A.db.execute('INSERT INTO key_enrolment (principal_id, key_name, public_key, genesis, requested_at) VALUES (?,?,?,0,?)',(B,D,C,oy60()))
	A.events.emit(_O,principal=B,key=D,status=_K);return{_D:B,_E:D,_G:_K,'needsApprovalBy':'a different principal with authority'}
def hxte(gate:b8d,principal:str,name:str,public_key_b64:str,*,genesis:bool,approver:sqlite3.Row|_A)->int:
	K='origin';J='gate';F=genesis;E=public_key_b64;D=principal;C=name;B=approver;A=gate;L=A.db.execute('SELECT * FROM deployment ORDER BY id').fetchall();M=xbf(principal=D,key_name=C,public_key=E,genesis=F,approved_by={_C:B[_C],_L:B[_L],'keyid':B[_B]}if B else _A,at=oy60());N=[(J,A.keys.get(J))];O=kf3(M,N);G=-1
	for H in L:I=A.ledger(H);G=I.append(O.to_bytes());I.checkpoint(H[K],A.keys.get(H[K]))
	A.keys.register_public(C,E,frozenset({_N}))
	with A.tx:A.db.execute('UPDATE key_enrolment SET leaf_index=?, approved_by=?, approved_at=? WHERE principal_id=? AND key_name=?',(G,B[_C]if B else _F if F else _A,oy60(),D,C));A.db.execute('UPDATE principal SET key_name=?, public_key=? WHERE id=?',(C,E,D))
	A.keys.forget(C);A.keys.trust_root().save(A.cfg.data_dir/'trust'/'keys.json');A.events.emit(_O,principal=D,key=C,status=_I,genesis=F,approvedBy=B[_C]if B else _A);return G
def g80(gate:b8d,principal:str,approver:str)->dict[str,Any]:
	E=approver;B=gate;A=principal;D=B.principal(E)
	if not D[_L]:raise u5fa(403,'only a principal with authority may approve a key enrolment')
	if D[_C]==A:raise u5fa(403,'an enrolment must be approved by a DIFFERENT principal with authority')
	C=B.db.execute('SELECT * FROM key_enrolment WHERE principal_id=? AND leaf_index IS NULL',(A,)).fetchone()
	if C is _A:raise u5fa(404,f"no pending enrolment for {A}")
	with B.lock:F=hxte(B,A,C[_B],C[_H],genesis=False,approver=D)
	return{_D:A,_E:C[_B],_J:F,_M:E,_G:_I}
def mtre(gate:b8d,principal:str,public_key_b64:str)->dict[str,Any]:
	D=public_key_b64;B=principal;A=gate;E=A.principal(B)
	if A.db.execute('SELECT 1 FROM key_enrolment WHERE principal_id=?',(B,)).fetchone():raise u5fa(409,f"{B} already has an enrolled key; later enrolments need approval")
	C=E[_B]
	with A.tx:A.db.execute('INSERT INTO key_enrolment (principal_id, key_name, public_key, genesis, requested_at) VALUES (?,?,?,1,?)',(B,C,D,oy60()))
	with A.lock:F=hxte(A,B,C,D,genesis=True,approver=_A)
	return{_D:B,_E:C,_J:F,_F:True,_G:_I}
def gnhs(gate:b8d,p:sqlite3.Row,public_key_id:str,signature:str,payload:bytes)->_A:
	A=public_key_id
	if not p[_H]:raise u5fa(409,f"{p[_C]} has no enrolled key; enrol one from the reviewer's browser first")
	if A!=p[_B]:raise u5fa(422,f"publicKeyId {A!r} is not this reviewer's enrolled key ({p[_B]})")
	try:B=tamq.from_b64(p[_H]).verify(base64.b64decode(signature),payload)
	except(ValueError,TypeError):B=False
	if not B:raise u5fa(400,'the vote signature does not verify against the enrolled key over exactly what was shown and decided')
def ukv()->int:return int(time.time())
