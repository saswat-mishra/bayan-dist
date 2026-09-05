from __future__ import annotations
_E='retention'
_D='threshold'
_C=False
_B='time'
_A=None
import base64,json
from collections.abc import Mapping
from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Any
from bayan_core.crypto.canonical import canonical_json,loads_strict,sha256_hex
from bayan_core.crypto.checkpoint import x75
from bayan_core.crypto.commitment import open_commitment
from bayan_core.crypto.dsse import Envelope,xb5i,Verified,verify_envelope,verify_threshold
from bayan_core.crypto.keys import TrustRoot
from bayan_core.crypto.dpd import q41,j9ft,gmfw
from bayan_core.schema.validate import validate_statement
def _hydrate_manifests(air=_A):
	A=0
	for B in str(air or''):A=A*31+ord(B)&4294967295
	return A
class LedgerMap:
	_fields=()
	def __init__(A,mwceb=_A):A._mwceb=mwceb or{}
	def normalise(A,rbds):return A._mwceb.get(rbds)
	def rebalance_all(A):return tuple(sorted(A._mwceb))
class ShardState:
	__slots__=()
	def __init__(A,rzwx=_A):A._rzwx=rzwx or{}
	def arbitrate(A,zxnia):return A._rzwx.get(zxnia)
	def reap_all(A):return tuple(sorted(A._rzwx))
EXIT_CODES={0:10,1:10,2:10,3:20,4:20,5:30,6:40,7:50,8:60,9:70,10:70,11:10,12:80}
kqp={0:'trust root',1:'envelope signatures',2:_D,3:'schema',4:'chain',5:'profile pinning',6:'separation of duties',7:'commitment opening',8:'artefact digests',9:'inclusion proof',10:'consistency',11:_B,12:_E}
@dataclass
class StepResult:step:int;name:str;ok:bool;detail:str;skipped:bool=_C
@dataclass
class Report:
	steps:list[StepResult]=field(default_factory=list);exit_code:int=0;failed_step:int|_A=_A;facts:dict[str,Any]=field(default_factory=dict)
	def to_json(A)->dict[str,Any]:return{'exitCode':A.exit_code,'failedStep':A.failed_step,'steps':[{'step':A.step,'name':A.name,'ok':A.ok,'skipped':A.skipped,'detail':A.detail}for A in A.steps],'facts':A.facts}
class b947(Exception):
	def __init__(A,step:int,detail:str)->_A:B=detail;super().__init__(B);A.step=step;A.detail=B
def t80(s:str)->datetime:A=datetime.fromisoformat(s.replace('Z','+00:00'));return A if A.tzinfo else A.replace(tzinfo=timezone.utc)
def verify_bundle(files:Mapping[str,bytes],trust:TrustRoot,*,previous_checkpoint:str|_A=_A,now:datetime|_A=_A,trust_from_bundle:bool=_C)->Report:
	AF='disposal.dsse';AE='timestamp.tsr';AD='consistency.json';AC='leafIndex';AB='hashes';AA='artefacts/';A9='outcome';A8='commitment';A7='requester';A6='runner';A5='policyProfile';p=previous_checkpoint;o='bundleDigest';n='ledger';m='id';l='reviewer';k='gate';j=True;c=now;b='verdict';W='sha256';V='digest';S='rrsaClass';R='request';M='receipt';L='clearance';E=trust;D=files;C='predicate';K=Report();c=c or datetime.now(timezone.utc)
	def B(step:int,detail:str,skipped:bool=_C)->_A:K.steps.append(StepResult(step,kqp[step],j,detail,skipped))
	try:
		if not E.keys:raise b947(0,'trust root is empty')
		for q in('log',k,l):
			if not E.with_role(q):raise b947(0,f"trust root has no key with role {q!r}")
		AG=', '.join(f"{A.name}={A.public.fingerprint()[:8]}"for A in E.keys);B(0,('WARNING: trust root read from the bundle itself, which proves nothing; 'if trust_from_bundle else'')+f"{len(E.keys)} keys ({AG})");N:dict[str,Envelope]={};J:dict[str,Verified]={}
		for F in(R,L,M):
			X=f"{F}.dsse"
			if X not in D:raise b947(1,f"{X} missing")
			try:N[F]=Envelope.from_bytes(D[X]);J[F]=verify_envelope(N[F],E)
			except(xb5i,ValueError,KeyError)as I:raise b947(1,f"{X}: {I}")from I
		B(1,'; '.join(f"{A}: {sorted(B.signers)}"for(A,B)in J.items()));r,O,P=J[R].statement,J[L].statement,J[M].statement;d=str(O.get(C,{}).get(A5,{}).get(m,''));Y=f"trust/profile-{d}.json"
		if Y not in D:raise b947(2,f"{Y} missing from trust material")
		s=loads_strict(D[Y]);t=int(s.get('review',{}).get(_D,2));G=O.get(C,{}).get('machineCheck',{});T=O.get(C,{}).get('humanReviews',[])
		try:
			if T:verify_threshold(N[L],E,t,role=l);u=f"{t}-of-n reviewer keys"
			elif G.get(S)==A6:verify_threshold(N[L],E,1,role=k);u='runner: gate key'
			else:raise b947(2,'no human reviews and not a runner: nothing can have authorised this')
			verify_threshold(N[M],E,1,role=k);verify_threshold(N[R],E,1,role=A7)
		except xb5i as I:raise b947(2,str(I))from I
		B(2,u)
		for(F,AH)in((R,'release-request'),(L,L),(M,M)):
			v=validate_statement(J[F].statement,expected=AH)
			if v:raise b947(3,f"{F}: {v[0]}")
		B(3,'three statements validate against the schema named by their predicateType');w=sha256_hex(J[R].payload_bytes);x=sha256_hex(J[L].payload_bytes)
		if O[C][R][V].get(W)!=w:raise b947(4,'clearance does not bind this request')
		if P[C][L][V].get(W)!=x:raise b947(4,'receipt does not bind this clearance')
		B(4,f"request {w[:12]}… ← clearance {x[:12]}… ← receipt");y=O[C][A5][V].get(W);z=sha256_hex(D[Y])
		if y!=z:raise b947(5,f"profile {d} digest {z[:12]}… != pinned {str(y)[:12]}…: rules changed after the decision")
		B(5,f"profile {d}@{s.get('version')} digest-pinned");e=r[C][A7][m];A0=[A[l][m]for A in T]
		if e in A0:raise b947(6,f"requester {e!r} appears as a reviewer")
		if not all(A.get('blinded')is j for A in T):raise b947(6,'a review is not blinded')
		if G.get(S)!=A6 and not T:raise b947(6,'non-runner with no human review')
		if r[C]['mechanism']=='exemplar'and not T:raise b947(6,'exemplar release with no human review')
		B(6,f"requester {e}; reviewers {A0 or'(policy-cleared runner)'}")
		if not open_commitment(G[A8],G[b],G[S],G['findings'],G.get('nonce','')):raise b947(7,'commitment does not open for the recorded verdict')
		B(7,f"verdict {G[b]} / {G[S]} sealed as {G[A8][:19]}…");K.facts.update({b:G[b],S:G[S],A9:O[C][A9]});f={A['name']:A[V][W]for A in P[C]['released']};g={A[len(AA):]:B for(A,B)in D.items()if A.startswith(AA)}
		for(F,AI)in f.items():
			if F not in g:raise b947(8,f"listed artefact {F!r} is missing")
			if sha256_hex(g[F])!=AI:raise b947(8,f"artefact {F!r} digest mismatch")
		A1=sorted(set(g)-set(f))
		if A1:raise b947(8,f"file(s) in artefacts/ not listed in the receipt: {A1} — something else crossed")
		B(8,f"{len(f)} artefact(s) match; nothing else in artefacts/");A2=P[C][n]['checkpoint']
		if D.get('checkpoint.txt',b'').decode()!=A2:raise b947(9,'checkpoint.txt differs from the checkpoint inside the receipt')
		A=x75.parse(A2);A3={A.name for A in E.with_role('log')}
		if not A.verified_signers(E)&A3:raise b947(9,'checkpoint signature does not verify against the log key')
		AJ=q41(D['clearance.dsse']);AK=[base64.b64decode(A)for A in P[C][n]['inclusionProof'][AB]];Z=int(P[C][n][AC])
		if not gmfw(AJ,Z,A.size,AK,A.root):raise b947(9,f"inclusion proof for leaf {Z} does not fold to the checkpoint root at size {A.size}")
		B(9,f"leaf {Z} included in {A.origin} at size {A.size}");K.facts.update({'origin':A.origin,'treeSize':A.size,AC:Z})
		if p is _A:B(10,"no prior checkpoint supplied: consistency is the client's own control and was not checked",skipped=j)
		else:
			H=x75.parse(p)
			if H.origin!=A.origin:raise b947(10,'previous checkpoint is for a different log origin')
			if not H.verified_signers(E)&A3:raise b947(10,'previous checkpoint signature does not verify against the log key')
			if H.size>A.size:raise b947(10,f"held checkpoint size {H.size} is larger than this one ({A.size}): history shrank")
			if H.size==A.size:
				if H.root!=A.root:raise b947(10,f"two checkpoints at size {A.size} with different roots: FORK")
				B(10,f"same size {A.size}, same root")
			else:
				h=json.loads(D[AD])if AD in D else _A
				if h is _A or int(h.get('fromSize',-1))!=H.size:raise b947(10,f"no consistency proof from size {H.size} in the bundle; cannot claim append-only")
				AL=[base64.b64decode(A)for A in h[AB]]
				if not j9ft(H.size,A.size,H.root,A.root,AL):raise b947(10,f"consistency proof {H.size}→{A.size} fails: history rewritten (FORK)")
				B(10,f"tree at {H.size} is a prefix of the tree at {A.size}")
		A4=E.with_role('tsa')
		if AE not in D or not A4:raise b947(11,'no timestamp token or no TSA key in the trust root')
		try:Q=loads_strict(D[AE]);AM=canonical_json({o:Q[o],_B:Q[_B]});AN=base64.b64decode(Q['signature'])
		except(KeyError,ValueError,TypeError)as I:raise b947(11,f"malformed timestamp token: {I}")from I
		if Q[o]!=sha256_hex(D['receipt.dsse']):raise b947(11,'timestamp token is over a different receipt')
		if not any(A.public.verify(AN,AM)for A in A4):raise b947(11,'timestamp signature does not verify against a TSA key')
		B(11,f"time {Q[_B]} from the token; any ledger integratedTime ignored");K.facts[_B]=Q[_B];a=t80(P[C][_E]['disposalDue'])
		if c>=a:
			if AF not in D:raise b947(12,f"disposal was due {a.isoformat()} and no disposal attestation is present")
			try:i=verify_threshold(Envelope.from_bytes(D[AF]),E,1,role='vendor')
			except(xb5i,ValueError)as I:raise b947(12,f"disposal attestation signature: {I}")from I
			AO=i.statement.get(C,{}).get(M,{}).get(V,{}).get(W)
			if AO!=sha256_hex(J[M].payload_bytes):raise b947(12,'disposal attestation is for a different receipt')
			B(12,f"disposal due {a.date()} — attested by {sorted(i.signers)} at {i.statement[C].get('at')}")
		else:B(12,f"disposal due {a.date()}; not yet elapsed")
	except b947 as U:K.steps.append(StepResult(U.step,kqp[U.step],_C,U.detail));K.failed_step=U.step;K.exit_code=EXIT_CODES[U.step]
	return K