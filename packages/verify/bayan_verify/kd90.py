from __future__ import annotations
_V='runner'
_U='certificate'
_T='machineCheck'
_S='humanReviews'
_R='signature'
_Q='retention'
_P='schema'
_O='threshold'
_N='gate'
_M='requester'
_L='name'
_K='outcome'
_J='id'
_I=False
_H='time'
_G='request'
_F='receipt'
_E='clearance'
_D='reviewer'
_C='rrsaClass'
_B=None
_A='predicate'
import base64,json
from collections.abc import Mapping
from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Any
from bayan_core.blg.brgs import mhbq,z9g,gkou
from bayan_core.blg.olon import x75
from bayan_core.blg.ukh import lfa
from bayan_core.blg.liw import f9cb,xb5i,t3i,jrdw,u1a5
from bayan_core.blg.u7c9 import ray,avg
from bayan_core.blg.dpd import q41,j9ft,gmfw
from bayan_core.schema.eppu import qciu,cjgr,vu5
from bayan_core.c339 import lcs
from bayan_verify.qsv import mjwi,jqoc,tupg
wyer={0:10,1:10,2:10,3:20,4:20,5:30,6:40,7:50,8:60,9:70,10:70,11:10,12:80,13:90,14:91,15:92,16:93,17:94}
kqp={0:'trust root',1:'envelope signatures',2:_O,3:_P,4:'chain',5:'profile pinning',6:'separation of duties',7:'commitment opening',8:'artefact digests',9:'inclusion proof',10:'consistency',11:_H,12:_Q,13:'certificate schema',14:'grade recomputation',15:'artefact conformance',16:'controls derivation',17:'roster binding'}
jqwx='v1 bundle: certificate unsigned; re-issue'
@dataclass
class gx61:step:int;name:str;ok:bool;detail:str;skipped:bool=_I
@dataclass
class srz:
	steps:list[gx61]=field(default_factory=list);exit_code:int=0;failed_step:int|_B=_B;facts:dict[str,Any]=field(default_factory=dict)
	def to_json(A)->dict[str,Any]:return{'exitCode':A.exit_code,'failedStep':A.failed_step,'steps':[{'step':A.step,_L:A.name,'ok':A.ok,'skipped':A.skipped,'detail':A.detail}for A in A.steps],'facts':A.facts}
class b947(Exception):
	def __init__(A,step:int,detail:str,code:int|_B=_B)->_B:B=detail;super().__init__(B);A.step=step;A.detail=B;A.code=code
def t80(s:str)->datetime:A=datetime.fromisoformat(s.replace('Z','+00:00'));return A if A.tzinfo else A.replace(tzinfo=timezone.utc)
def cc2(humans:list[dict[str,Any]],trust:ray)->list[tuple[dict[str,Any],avg]]:
	C=trust;D:list[tuple[dict[str,Any],avg]]=[];F=C.with_role(_D)
	for A in humans:
		try:G=base64.b64decode(str(A[_R]));H=lcs(A)
		except(KeyError,ValueError,TypeError):continue
		B=C.get(str(A.get('publicKeyId','')));I=([B]if B and _D in B.roles else[])+[A for A in F if A is not B]
		for E in I:
			if E.public.verify(G,H):D.append((A,E));break
	return D
def e0ar(envs:dict[str,f9cb],cl:dict[str,Any],req:dict[str,Any],profile:dict[str,Any],trust:ray)->tuple[str,list[tuple[dict[str,Any],avg]]]:
	F=envs;B=trust;A=cl;C=A[_A].get(_S,[]);I=A[_A].get(_T,{});J=int(A[_A].get(_U,{}).get('grade',{}).get('requiredR',0));G=0 if J<=1 else 1 if J==2 else int(profile.get('review',{}).get(_O,2));D=cc2(C,B);E={str(A[_D][_J])for(A,B)in D};K=str(req[_A][_M][_J])
	if len(D)!=len(C):raise b947(2,f"{len(C)-len(D)} vote(s) carry no signature that verifies against a reviewer key")
	if K in E:raise b947(2,f"requester {K!r} signed a vote on their own request")
	if not C:
		if I.get(_C)==_V and A[_A][_K]=='release':H='runner: no vote required'
		elif I.get(_C)=='alien'and A[_A][_K]=='block':H='auto-refusal: no vote required'
		else:raise b947(2,'no human reviews and not a runner: nothing can have authorised this')
	elif len(E)<G:raise b947(2,f"threshold not met: {len(E)} distinct reviewer vote signature(s), need {G}")
	else:H=f"{len(E)} distinct reviewer vote signature(s) ≥ {G} required"
	try:u1a5(F[_E],B,1,role=_N);u1a5(F[_F],B,1,role=_N);u1a5(F[_G],B,1,role=_M)
	except xb5i as L:raise b947(2,str(L))from L
	return H,D
def qrtm(files:Mapping[str,bytes],trust:ray,*,previous_checkpoint:str|_B=_B,now:datetime|_B=_B,trust_from_bundle:bool=_I,strict:bool=_I,artefacts_by_reference:bool=_I)->srz:
	AR='controls';AQ='disposal.dsse';AP='timestamp.tsr';AO='consistency.json';AN='leafIndex';AM='hashes';AL='artefacts';AK='ref.json';AJ='artefacts/';AI='recommendation';AH='findings';AG='exemplar';AF='mechanism';AE='policyProfile';x=artefacts_by_reference;w=previous_checkpoint;v='headline';u='kind';t='bundleDigest';s='ledger';r='commitment';h=now;Z='label';Y='verdict';U='digest';R='sha256';Q=True;G=trust;D=files;J=srz();h=h or datetime.now(timezone.utc)
	def A(step:int,detail:str,skipped:bool=_I)->_B:J.steps.append(gx61(step,kqp[step],Q,detail,skipped))
	try:
		if not G.keys:raise b947(0,'trust root is empty')
		for y in('log',_N,_D):
			if not G.with_role(y):raise b947(0,f"trust root has no key with role {y!r}")
		if strict:
			z=[A.name for A in G.with_role(_D)if A.custody=='gate-colocated']
			if z:raise b947(0,f"--strict: reviewer key(s) {z} are gate-colocated; a reviewer's key must be the reviewer's")
		AS=', '.join(f"{A.name}={A.public.fingerprint()[:8]}"for A in G.keys);A(0,('WARNING: trust root read from the bundle itself, which proves nothing; 'if trust_from_bundle else'')+f"{len(G.keys)} keys ({AS})");i:dict[str,f9cb]={};K:dict[str,t3i]={}
		for E in(_G,_E,_F):
			a=f"{E}.dsse"
			if a not in D:raise b947(1,f"{a} missing")
			try:i[E]=f9cb.from_bytes(D[a]);K[E]=jrdw(i[E],G)
			except(xb5i,ValueError,KeyError)as F:raise b947(1,f"{a}: {F}")from F
		for(E,j)in K.items():
			A0=qciu(j.statement)if isinstance(j.statement,dict)else _B
			if A0==1:raise b947(1,jqwx,code=30)
			if A0 is _B:raise b947(1,f"{E}: unknown predicateType {j.statement.get("predicateType")!r}",code=30)
		A(1,'; '.join(f"{A}: {sorted(B.signers)}"for(A,B)in K.items())+'; statements v2');N,L,M=K[_G].statement,K[_E].statement,K[_F].statement;k=str(L.get(_A,{}).get(AE,{}).get(_J,''));b=f"trust/profile-{k}.json"
		if b not in D:raise b947(2,f"{b} missing from trust material")
		c=z9g(D[b]);AT,AU=e0ar(i,L,N,c,G);A(2,AT);B=L[_A][_T];V=L[_A][_S]
		for(E,AV)in((_G,'release-request'),(_E,_E),(_F,_F)):
			W=vu5(K[E].statement,expected=AV)
			if W:raise b947(3,f"{E}: {W[0]}")
		A(3,'three statements validate against the v2 schema named by their predicateType');l=gkou(K[_G].payload_bytes);A1=gkou(K[_E].payload_bytes)
		if L[_A][_G][U].get(R)!=l:raise b947(4,'clearance does not bind this request')
		if M[_A][_E][U].get(R)!=A1:raise b947(4,'receipt does not bind this clearance')
		for A2 in V:
			if A2.get(_G)!=l:raise b947(4,f"vote by {A2[_D][_J]} was signed over a different request")
		A(4,f"request {l[:12]}… ← clearance {A1[:12]}… ← receipt; every vote names this request");A3=L[_A][AE][U].get(R);m=gkou(D[b])
		if A3!=m:raise b947(5,f"profile {k} digest {m[:12]}… != pinned {str(A3)[:12]}…: rules changed after the decision")
		I=L[_A][_U]
		if I.get('pack',{}).get(U,{}).get(R)!=m:raise b947(5,'the certificate names a different pack digest than the pinned profile')
		A(5,f"profile {k}@{c.get("version")} digest-pinned; certificate agrees");d=N[_A][_M][_J];A4=[A[_D][_J]for A in V]
		if d in A4:raise b947(6,f"requester {d!r} appears as a reviewer")
		if not all(A.get('blinded')is Q for A in V):raise b947(6,'a review is not blinded')
		A5=L[_A][_K]=='block'and B.get(_C)=='alien'
		if B.get(_C)!=_V and not V and not A5:raise b947(6,'non-runner with no human review')
		if N[_A][AF]==AG and not V and not A5:raise b947(6,'exemplar release with no human review')
		if N[_A].get('recipient',{}).get('principal')!=d:raise b947(6,'the request names a recipient other than the requester')
		A(6,f"requester {d}; reviewers {A4 or"(none: "+str(B.get(_C))+")"}");n=lfa(B[r],B[Y],B[_C],B[AH],B.get('nonce',''))
		if not n and AI in B:from bayan_core.blg.ukh import o5t as AW;n=AW(B[r],B[Y],B[_C],B[AH],B[AI],list(B.get('recommendationBasis',[])),B.get('nonce',''))
		if not n:raise b947(7,'commitment does not open for the recorded verdict')
		A(7,f"verdict {B[Y]} / {B[_C]} sealed as {B[r][:19]}…");J.facts.update({Y:B[Y],_C:B[_C],_K:L[_A][_K]});S={A[_L]:A[U][R]for A in M[_A]['released']};X={A[len(AJ):]:B for(A,B)in D.items()if A.startswith(AJ)}
		if x:
			AX=z9g(D[AK])if AK in D else{AL:[]};AY={A[_L]:A[R]for A in AX[AL]}
			if AY!=S:raise b947(8,"the pack's artefact references do not match the receipt")
			A(8,f"{len(S)} artefact(s) by reference (digests match the receipt); bytes not included in an evidence pack",skipped=Q)
		else:
			for(E,AZ)in S.items():
				if E not in X:raise b947(8,f"listed artefact {E!r} is missing")
				if gkou(X[E])!=AZ:raise b947(8,f"artefact {E!r} digest mismatch")
			A6=sorted(set(X)-set(S))
			if A6:raise b947(8,f"file(s) in artefacts/ not listed in the receipt: {A6} — something else crossed")
			A(8,f"{len(S)} artefact(s) match; nothing else in artefacts/")
		A7=M[_A][s]['checkpoint']
		if D.get('checkpoint.txt',b'').decode()!=A7:raise b947(9,'checkpoint.txt differs from the checkpoint inside the receipt')
		C=x75.parse(A7);A8={A.name for A in G.with_role('log')}
		if not C.verified_signers(G)&A8:raise b947(9,'checkpoint signature does not verify against the log key')
		Aa=q41(D['clearance.dsse']);Ab=[base64.b64decode(A)for A in M[_A][s]['inclusionProof'][AM]];e=int(M[_A][s][AN])
		if not gmfw(Aa,e,C.size,Ab,C.root):raise b947(9,f"inclusion proof for leaf {e} does not fold to the checkpoint root at size {C.size}")
		A(9,f"leaf {e} included in {C.origin} at size {C.size}");J.facts.update({'origin':C.origin,'treeSize':C.size,AN:e})
		if w is _B:A(10,"no prior checkpoint supplied: consistency is the client's own control and was not checked",skipped=Q)
		else:
			H=x75.parse(w)
			if H.origin!=C.origin:raise b947(10,'previous checkpoint is for a different log origin')
			if not H.verified_signers(G)&A8:raise b947(10,'previous checkpoint signature does not verify against the log key')
			if H.size>C.size:raise b947(10,f"held checkpoint size {H.size} is larger than this one ({C.size}): history shrank")
			if H.size==C.size:
				if H.root!=C.root:raise b947(10,f"two checkpoints at size {C.size} with different roots: FORK")
				A(10,f"same size {C.size}, same root")
			else:
				o=json.loads(D[AO])if AO in D else _B
				if o is _B or int(o.get('fromSize',-1))!=H.size:raise b947(10,f"no consistency proof from size {H.size} in the bundle; cannot claim append-only")
				Ac=[base64.b64decode(A)for A in o[AM]]
				if not j9ft(H.size,C.size,H.root,C.root,Ac):raise b947(10,f"consistency proof {H.size}→{C.size} fails: history rewritten (FORK)")
				A(10,f"tree at {H.size} is a prefix of the tree at {C.size}")
		A9=G.with_role('tsa')
		if AP not in D or not A9:raise b947(11,'no timestamp token or no TSA key in the trust root')
		try:T=z9g(D[AP]);Ad=mhbq({t:T[t],_H:T[_H]});Ae=base64.b64decode(T[_R])
		except(KeyError,ValueError,TypeError)as F:raise b947(11,f"malformed timestamp token: {F}")from F
		if T[t]!=gkou(D['receipt.dsse']):raise b947(11,'timestamp token is over a different receipt')
		if not any(A.public.verify(Ae,Ad)for A in A9):raise b947(11,'timestamp signature does not verify against a TSA key')
		A(11,f"time {T[_H]} from the token; any ledger integratedTime ignored");J.facts[_H]=T[_H];f=t80(M[_A][_Q]['disposalDue'])
		if h>=f:
			if AQ not in D:raise b947(12,f"disposal was due {f.isoformat()} and no disposal attestation is present")
			try:p=u1a5(f9cb.from_bytes(D[AQ]),G,1,role='vendor')
			except(xb5i,ValueError)as F:raise b947(12,f"disposal attestation signature: {F}")from F
			Af=p.statement.get(_A,{}).get(_F,{}).get(U,{}).get(R)
			if Af!=gkou(K[_F].payload_bytes):raise b947(12,'disposal attestation is for a different receipt')
			A(12,f"disposal due {f.date()} — attested by {sorted(p.signers)} at {p.statement[_A].get("at")}")
		else:A(12,f"disposal due {f.date()}; not yet elapsed")
		W=cjgr(I)
		if W:raise b947(13,f"certificate: {W[0]}")
		g=M[_A].get('certificateSummary',{})
		if g.get(Z)!=I['grade'][Z]or g.get(u)!=I[v][u]:raise b947(13,"the receipt's certificateSummary does not match the certificate")
		if M[_A].get(AR)!=I[AR]or M[_A].get(v)!=I[v]:raise b947(13,"the receipt's controls/headline do not match the certificate")
		A(13,f"{I[_P]} valid; receipt summary {g.get(Z)} / {g.get(u)} agrees");AA=L[_A][_K];O=mjwi(I,N,AU,c,AA);J.facts['claimed']=O.claimed;J.facts['recomputed']=O.recomputed
		if O.failures:raise b947(14,'OVER-CLAIM: '+'; '.join(O.failures))
		A(14,f"recomputed {O.recomputed[Z]} ≥ claimed {O.claimed[Z]}; gates agree; releasable={O.recomputed["releasable"]}")
		if x:A(15,'artefacts by reference: conformance was checked on the release bundle, not here (recorded)',skipped=Q)
		elif N[_A][AF]==AG:A(15,'exemplar: the artefact is a record, not rows — conformance not applicable (recorded)',skipped=Q)
		elif not S:A(15,'refusal: nothing was released, nothing to check',skipped=Q)
		else:
			from bayan_core.evxn.iuoq import vjs as Ag,f3w as Ah;q=I['outputSchema']
			if q is _B:raise b947(15,'released rows with no declared outputSchema')
			for(E,Ai)in X.items():
				try:
					AB=z9g(Ai)
					if not isinstance(AB,list):raise b947(15,f"{E}: artefact is not a list of rows")
					Ah(AB,q)
				except Ag as F:raise b947(15,f"{E}: released bytes do not conform to the certificate's outputSchema — {F.rule}: {F.detail}")from F
				except ValueError as F:raise b947(15,f"{E}: not JSON — {F}")from F
			A(15,f"{len(X)} artefact(s) conform to the certificate's outputSchema ({len(q["columns"])} columns)")
		Aj,AC=jqoc(I,c,AA)
		if not Aj:raise b947(16,AC)
		A(16,AC);Ak,AD,Al=tupg(I,N,D.get('trust/roster-snapshot.json'),G)
		if not Ak:raise b947(17,AD)
		A(17,AD,skipped=Al)
	except b947 as P:J.steps.append(gx61(P.step,kqp[P.step],_I,P.detail));J.failed_step=P.step;J.exit_code=P.code if P.code is not _B else wyer[P.step]
	return J
