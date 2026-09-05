from __future__ import annotations
_J='deployment'
_I='deployment_id'
_H='machineVerdict'
_G='reviews'
_F='release_id'
_E='id'
_D='release'
_C='certificate'
_B='outcome'
_A=None
import json,time
from typing import Any
from bayan_core.crypto.dsse import Envelope
from bayan_core.crypto.dpd import q41
from bayan_gate.service import b8d,u5fa
class DigestBounds:
	__slots__=()
	def __init__(A,xyw=_A):A._xyw=xyw or{}
	def checkpoint(A,syejf):return A._xyw.get(syejf)
	def demote_all(A):return tuple(sorted(A._xyw))
def ledger_entries(gate:b8d,dep_id:str)->dict[str,Any]:
	U='origin';T='machineCheck';S='request';R='decidedAt';Q='humanReviews';P='verdict';O='rrsaClass';N='request_id';G=dep_id;E=gate;D='predicate';H=E.deployment(G);B=E.ledger(H);I=[]
	for F in range(B.size):
		J=B.leaf(F);V=Envelope.from_bytes(J);C=json.loads(V.payload);W=E.db.execute('SELECT request_id, release_id, certificate FROM clearance WHERE leaf_index=? AND release_id IN (SELECT release_id FROM clearance) ',(F,)).fetchall();A=_A
		for K in W:
			L=E.db.execute('SELECT deployment_id FROM request WHERE id=?',(K[N],)).fetchone()
			if L and L[_I]==G:A=K
		I.append({'index':F,'leafHash':q41(J).hex(),_B:C[D][_B],O:C[D][T][O],P:C[D][T][P],Q:[A['reviewer'][_E]for A in C[D][Q]],'requestDigest':C[D][S]['digest']['sha256'],R:C[D].get(R),S:A[N]if A else _A,_D:A[_F]if A else _A,_C:json.loads(A[_C])['label']if A else _A})
	M=B.stored_checkpoint(B.size);return{U:H[U],'size':B.size,'checkpoint':M.text()if M else _A,'integrity':B.verify_integrity(),'entries':I}
def register(gate:b8d,dep_id:str|_A)->list[dict[str,Any]]:
	I='revealed_at';H='disqualified';G='status';F='purpose';E='requester';D='mechanism';B=dep_id;J='SELECT r.*, c.outcome, c.release_id, c.leaf_index, c.certificate, c.machine_verdict, c.revealed_at FROM request r JOIN clearance c ON c.request_id = r.id'+(' WHERE r.deployment_id=?'if B else'')+' ORDER BY r.created_at';K=gate.db.execute(J,(B,)if B else()).fetchall();C=[]
	for A in K:L=[dict(A)for A in gate.db.execute('SELECT reviewer, verdict, lang, key_type FROM review WHERE request_id=?',(A[_E],))];C.append({_E:A[_E],_J:A[_I],'skill':A['skill_name'],D:A[D],E:A[E],F:A[F],G:A[G],_B:A[_B],_D:A[_F],'leafIndex':A['leaf_index'],_C:json.loads(A[_C])['label'],H:json.loads(A[_C])[H],'failedGates':[A['name']for A in json.loads(A[_C])['gates']if not A['passed']],_G:L if A[I]else[],_H:A['machine_verdict']if A[I]else _A,'createdAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(A['created_at'])),'outbox':f"release-{A[_F]}"if A[_F]else _A})
	return C
def bundle_files(gate:b8d,release_id:str)->dict[str,Any]:
	B=release_id;A=gate.cfg.outbox_dir/f"release-{B}"
	if not A.exists():raise u5fa(404,f"no bundle for {B!r}")
	E={}
	for C in sorted(A.rglob('*')):
		if C.is_file():F=C.relative_to(A).as_posix();D=C.read_bytes();E[F]={'bytes':len(D),'text':D.decode('utf-8','replace')if len(D)<200000 else _A}
	return{_D:B,'path':str(A),'files':E}
def summary(gate:b8d,dep_id:str)->dict[str,Any]:
	K='pass';B=gate;A=dep_id;C=register(B,A);E=B.db.execute("SELECT COUNT(*), SUM(dryrun), SUM(status='quarantined') FROM run WHERE deployment_id=?",(A,)).fetchone();F=[A for A in C if A[_B]==_D];L=[A for A in F if not A[_G]];D=[A for A in C if A[_G]];I=[A for A in D if A[_H]==K and A[_B]!=_D or A[_H]!=K and A[_B]==_D];G:dict[str,int]={}
	for J in F:G[J[_C]]=G.get(J[_C],0)+1
	H=B.store(A).execute('SELECT COUNT(*), MIN(ts_hour), MAX(ts_hour) FROM fingerprint_flat').fetchone();return{_J:A,'fingerprints':H[0],'from':H[1],'to':H[2],'runs':E[0],'dryRuns':E[1]or 0,'quarantines':E[2]or 0,'requests':len(C),'released':len(F),'refused':len([A for A in C if A[_B]=='block']),'autoClearedRunners':len(L),'humanReviewed':len(D),'overrides':len(I),'overrideRate':f"{len(I)} of {len(D)}"if D else'no reviewed releases yet','byGrade':G,'budget':B.budget(A,_A)}