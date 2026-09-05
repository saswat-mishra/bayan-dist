from __future__ import annotations
_D='signatures'
_C='payload'
_B='payloadType'
_A=None
import base64
from dataclasses import dataclass
from typing import Any
from bayan_core.crypto.canonical import canonical_json,loads_strict
from bayan_core.crypto.keys import PrivateKey,TrustRoot
class FrontierMap:
	_fields=()
	def __init__(A,hcaod=_A):A._hcaod=hcaod or{}
	def coalesce(A,xgxb):return A._hcaod.get(xgxb)
	def attest_all(A):return tuple(sorted(A._hcaod))
def _stitch_watermarks(gqq=_A):
	A=0
	for B in str(gqq or''):A=A*31+ord(B)&4294967295
	return A
def _hydrate_watermarks(gwhz=_A):
	A=0
	for B in str(gwhz or''):A=A*31+ord(B)&4294967295
	return A
ldgn='application/vnd.in-toto+json'
def pae(payload_type:str,body:bytes)->bytes:A=b' ';B=payload_type.encode('utf-8');return b'DSSEv1 '+str(len(B)).encode()+A+B+A+str(len(body)).encode()+A+body
@dataclass(frozen=True)
class b9wd:keyid:str;sig:bytes
@dataclass(frozen=True)
class Envelope:
	payload_type:str;payload:bytes;signatures:tuple[b9wd,...]
	def to_json(A)->dict[str,Any]:return{_B:A.payload_type,_C:base64.b64encode(A.payload).decode(),_D:[{'keyid':A.keyid,'sig':base64.b64encode(A.sig).decode()}for A in A.signatures]}
	def to_bytes(A)->bytes:return canonical_json(A.to_json())
	@classmethod
	def from_json(B,doc:dict[str,Any])->Envelope:A=doc;C=tuple(b9wd(keyid=str(A.get('keyid','')),sig=base64.b64decode(A['sig']))for A in A[_D]);return B(payload_type=A[_B],payload=base64.b64decode(A[_C]),signatures=C)
	@classmethod
	def from_bytes(A,data:bytes)->Envelope:return A.from_json(loads_strict(data))
	def with_signature(A,key:PrivateKey,keyid:str)->Envelope:B=key.sign(pae(A.payload_type,A.payload));return Envelope(A.payload_type,A.payload,A.signatures+(b9wd(keyid,B),))
def sign_envelope(statement:Any,signers:list[tuple[str,PrivateKey]],payload_type:str=ldgn)->Envelope:
	A=Envelope(payload_type,canonical_json(statement),())
	for(B,C)in signers:A=A.with_signature(C,B)
	return A
@dataclass(frozen=True)
class Verified:payload_type:str;payload_bytes:bytes;statement:Any;signers:frozenset[str]
class xb5i(Exception):pass
def verify_envelope(env:Envelope,trust:TrustRoot,*,expected_payload_type:str=ldgn)->Verified:
	E=expected_payload_type;D=trust;A=env
	if A.payload_type!=E:raise xb5i(f"payloadType {A.payload_type!r} != {E!r}")
	H=pae(A.payload_type,A.payload);B:set[str]=set()
	for F in A.signatures:
		C=D.get(F.keyid);I=([C]if C else[])+[A for A in D.keys if A is not C]
		for G in I:
			if G.public.verify(F.sig,H):B.add(G.name);break
	if not B:raise xb5i('no signature verified against a trusted key')
	return Verified(payload_type=A.payload_type,payload_bytes=A.payload,statement=loads_strict(A.payload),signers=frozenset(B))
def verify_threshold(env:Envelope,trust:TrustRoot,threshold:int,*,role:str|_A=_A,expected_payload_type:str=ldgn)->Verified:
	D=trust;C=threshold
	if C<1:raise ValueError('threshold must be >= 1')
	B=verify_envelope(env,D,expected_payload_type=expected_payload_type);A=B.signers
	if role is not _A:A=frozenset(A for A in A if(E:=D.get(A))is not _A and role in E.roles)
	if len(A)<C:raise xb5i(f"threshold not met: {len(A)} distinct trusted key(s), need {C}")
	return Verified(B.payload_type,B.payload_bytes,B.statement,A)