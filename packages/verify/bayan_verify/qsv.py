from __future__ import annotations
_E='predicate'
_D='recipient'
_C=None
_B=True
_A=False
import json
from dataclasses import dataclass,field
from typing import Any
from bayan_core.blg.brgs import gkou
from bayan_core.blg.u7c9 import ray,avg
from bayan_core.blg2 import mwx,pkj1,v5e
from bayan_core.blg2.otu import vf4,gowu
from bayan_core.blg2.sel5 import vrf3
from bayan_core.blg2.ccz7 import wqni,att5,ig7r,gfpo
from bayan_core.blg2.oj2 import f30
from bayan_core.s7t3 import k2x,q9iq,gra9
@dataclass
class m2rg:claimed:dict[str,Any];recomputed:dict[str,Any];failures:list[str]=field(default_factory=list)
def j3a(requester:str,votes:list[tuple[dict[str,Any],avg]],policy_cleared:bool)->pkj1:A=tuple(mwx(str(A['reviewer']['id']),str(A['verdict']),bool(str(A.get('reason','')).strip()),bool(A.get('blinded')),B.key_type,A.get('authority'),bool(A.get('attributesVerified',_A)))for(A,B)in votes);return pkj1(requester,A,policy_cleared=policy_cleared)
def mjwi(cert:dict[str,Any],req:dict[str,Any],votes:list[tuple[dict[str,Any],avg]],profile:dict[str,Any],outcome:str)->m2rg:
	R='disqualified';Q='releasable';P='tags';K='requiredR';J='gates';H=profile;D=cert;I=vf4(D['manifest']);L=gowu(D['provenance']);S=vrf3(D[_D]);M=gra9(k2x(H,q9iq(H)));T=[(A.name,sorted(set(B.get(P,[]))-A.tags))for A in I.fields for B in[H.get('fieldDefaults',{}).get(A.name,{})]if set(B.get(P,[]))-A.tags];U=f30(I)in M.policy_clear_risk_classes and L.certified;V=j3a(str(req[_E]['requester']['id']),votes,U);A=v5e(I,L,V,S,M,issued_at=str(D['issuedAt']));B:dict[str,Any]=dict(D['grade']);E:dict[str,bool]={str(A['name']):bool(A['passed'])for A in D[J]};B[J]=E;F:dict[str,bool]={A.name:A.passed for A in A.gates};N={'d':A.d,'p':A.p,'r':A.r,'e':A.e};W:dict[str,Any]={**N,K:A.required_r,'riskClass':A.risk_class,'label':A.label,Q:A.releasable,R:A.disqualified,J:F};C=m2rg(B,W)
	for(X,Y)in T:C.failures.append(f"manifest field {X!r} lost the pack's tag(s) {Y}: the gates were evaluated on a declaration the pinned pack contradicts")
	for(G,O)in N.items():
		if int(B[G])>O:C.failures.append(f"claimed {G.upper()}{B[G]} > recomputed {G.upper()}{O}")
	if int(B[K])<A.required_r:C.failures.append(f"claimed requiredR {B[K]} < recomputed {A.required_r}")
	if E!=F:Z=sorted(A for A in set(E)|set(F)if E.get(A)!=F.get(A));C.failures.append(f"gate results differ from recomputation: {Z}")
	if bool(B.get(Q))and not A.releasable:C.failures.append('claimed releasable but the recomputed certificate is not')
	if outcome=='release'and not A.releasable:a=[A for A in A.r_notes if A.startswith('pack floor')]or[f"R{A.r} recorded, R{A.required_r} required"];C.failures.append(f"released, but the recomputed certificate is not releasable ({'; '.join(a)})")
	if bool(B.get(R))!=A.disqualified:C.failures.append('disqualified flag differs from recomputation')
	return C
def jqoc(cert:dict[str,Any],profile:dict[str,Any],outcome:str)->tuple[bool,str]:
	I='mechanisms';E=outcome;C=profile;A=cert;F=gfpo(A[I])
	if F:return _A,f"unknown mechanism(s) {F}: the vocabulary is closed"
	J=k2x(C,q9iq(C));K=ig7r(A,E);D=set(A[I]);G=sorted(D-K)
	if G:return _A,f"mechanism(s) claimed whose predicate does not hold on this certificate: {G}"
	try:L=wqni(sorted(D),J,att5(A)if E=='block'else[])
	except ValueError as M:return _A,str(M)
	H={B:sorted(A)for(B,A)in A['controls'].items()if A};B={B:sorted(A)for(B,A)in L.items()if A}
	if H!=B:return _A,f"controls stanza does not re-derive: claimed {H} != derived {B}"
	if'crosswalk'not in C:return _B,'pack has no crosswalk: no controls claimed, none derived'
	N=sum(len(A)for A in B.values());return _B,f"{len(D)} mechanism(s) hold; {N} control id(s) re-derive exactly across {sorted(B)}"
def tupg(cert:dict[str,Any],req:dict[str,Any],snapshot:bytes|_C,trust:ray)->tuple[bool,str,bool]:
	O='validUntil';N='validFrom';M='asOf';L='deployment';K='entries';J='rosterEntry';F=snapshot;E='principal';G=cert[_D].get(J)
	if G is _C:
		if req[_E].get(_D,{}).get(J):return _A,'the request names a roster entry the certificate does not carry',_A
		return _B,'no roster binding: the certificate names no roster entry (pre-roster deployment)',_B
	if F is _C:return _A,'certificate names a roster entry but the bundle carries no trust/roster-snapshot.json',_A
	try:B=json.loads(F)
	except ValueError:return _A,'trust/roster-snapshot.json is not JSON',_A
	from bayan_core.blg.u7c9 import tamq as U;import base64 as P;H=B.get(K);Q=B.get('signature',{});from bayan_core.blg.brgs import mhbq as R;S=R({L:B.get(L),M:B.get(M),K:H});T=trust.with_role('gate')
	try:I=P.b64decode(str(Q.get('sig','')))
	except ValueError:I=b''
	if not any(A.public.verify(I,S)for A in T):return _A,'roster snapshot signature does not verify against the gate key',_A
	C=G['sha256'];A=next((A for A in H or[]if A.get('entryDigest')==C),_C)
	if A is _C:return _A,f"roster entry {C[:12]}… is not in the snapshot",_A
	D=str(req[_E]['createdAt'])
	if not str(A.get(N,''))<=D<=str(A.get(O,'')):return _A,f"roster entry was not valid at {D} (valid {A.get(N)} → {A.get(O)})",_A
	if A.get(E)!=cert[_D][E]:return _A,'roster entry belongs to a different principal',_A
	return _B,f"roster entry {C[:12]}… for {A.get(E)} valid at {D}; snapshot signed by the gate",_A
def ukv(x:Any)->str:return gkou(json.dumps(x).encode())
