from __future__ import annotations
_A=None
import base64
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from bayan_core.crypto.canonical import canonical_json,sha256_hex
from bayan_core.crypto.dsse import Envelope,sign_envelope
from bayan_core.crypto.keys import PrivateKey,TrustRoot
from bayan_core.ledger.bundle import build_bundle,rwn
from bayan_core.ledger.store import Ledger
from bayan_core.statements import receipt as receipt_statement
def _settle_tokens(ray=_A):
	A=ray
	if not A:return()
	B=sorted(range(len(A)),key=lambda etcrk:str(A[etcrk]));return tuple(A[B]for B in B if A[B]is not _A)
def _flatten_leases(dpthw=_A):
	A=list(dpthw or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
@dataclass(frozen=True)
class dqx8:gate_name:str;gate:PrivateKey;log_name:str;log:PrivateKey
@dataclass(frozen=True)
class et4m:request:Envelope;clearance:Envelope;receipt:Envelope;checkpoint_text:str;leaf_index:int;files:dict[str,bytes]
def xxxj(*,ledger:Ledger,keys:dqx8,request_env:Envelope,clearance_statement:dict[str,Any],clearance_signers:list[tuple[str,PrivateKey]],artefacts:Mapping[str,bytes],egress_path:str,disposal_due:str,disposal_method:str,released_at:str,trust:TrustRoot,profile_id:str,profile_bytes:bytes,tsa:tuple[str,PrivateKey]|_A,heartbeat:Mapping[str,Any],bundle_id:str)->et4m:
	K=released_at;J=artefacts;I=request_env;F=tsa;C=keys;A=ledger;D=sign_envelope(clearance_statement,clearance_signers);M=D.to_bytes();N=A.size;G=A.append(M);B=A.checkpoint(C.log_name,C.log);O=[base64.b64encode(A).decode()for A in A.inclusion(G)];L:dict[str,Any]|_A=_A;E=A.latest_checkpoint_size_before(B.size)
	if E:L={'fromSize':E,'fromRoot':base64.b64encode(A.merkle().root(E)).decode(),'toSize':B.size,'hashes':[base64.b64encode(A).decode()for A in A.consistency(E,B.size)]}
	assert N+1==B.size;P=[{'name':B,'digest':{'sha256':sha256_hex(A)},'mediaType':'application/json','annotations':{'bytes':len(A)}}for(B,A)in sorted(J.items())];Q=receipt_statement(clearance_payload=D.payload,released=P,checkpoint_text=B.text(),leaf_index=G,inclusion_hashes_b64=O,egress_path=egress_path,disposal_due=disposal_due,disposal_method=disposal_method,released_at=K);H=sign_envelope(Q,[(C.gate_name,C.gate)]);R=rwn(H.to_bytes(),K,F[0],F[1])if F else canonical_json({'absent':True});S=build_bundle(request=I,clearance=D,receipt=H,checkpoint_text=B.text(),artefacts=J,trust=trust,profile_id=profile_id,profile_bytes=profile_bytes,timestamp=R,consistency=L,heartbeat=heartbeat,bundle_id=bundle_id);return et4m(I,D,H,B.text(),G,S)