from __future__ import annotations
_D='signatures'
_C='payload'
_B='payloadType'
_A=None
import base64
from dataclasses import dataclass
from typing import Any
from bayan_core.blg.brgs import mhbq,z9g
from bayan_core.blg.u7c9 import lfq1,ray
ldgn='application/vnd.in-toto+json'
def uu7(payload_type:str,body:bytes)->bytes:A=b' ';B=payload_type.encode('utf-8');return b'DSSEv1 '+str(len(B)).encode()+A+B+A+str(len(body)).encode()+A+body
@dataclass(frozen=True)
class b9wd:keyid:str;sig:bytes
@dataclass(frozen=True)
class f9cb:
	payload_type:str;payload:bytes;signatures:tuple[b9wd,...]
	def to_json(A)->dict[str,Any]:return{_B:A.payload_type,_C:base64.b64encode(A.payload).decode(),_D:[{'keyid':A.keyid,'sig':base64.b64encode(A.sig).decode()}for A in A.signatures]}
	def to_bytes(A)->bytes:return mhbq(A.to_json())
	@classmethod
	def from_json(B,doc:dict[str,Any])->f9cb:A=doc;C=tuple(b9wd(keyid=str(A.get('keyid','')),sig=base64.b64decode(A['sig']))for A in A[_D]);return B(payload_type=A[_B],payload=base64.b64decode(A[_C]),signatures=C)
	@classmethod
	def from_bytes(A,data:bytes)->f9cb:return A.from_json(z9g(data))
	def with_signature(A,key:lfq1,keyid:str)->f9cb:B=key.sign(uu7(A.payload_type,A.payload));return f9cb(A.payload_type,A.payload,A.signatures+(b9wd(keyid,B),))
def kf3(statement:Any,signers:list[tuple[str,lfq1]],payload_type:str=ldgn)->f9cb:
	A=f9cb(payload_type,mhbq(statement),())
	for(B,C)in signers:A=A.with_signature(C,B)
	return A
@dataclass(frozen=True)
class t3i:payload_type:str;payload_bytes:bytes;statement:Any;signers:frozenset[str]
class xb5i(Exception):0
def jrdw(env:f9cb,trust:ray,*,expected_payload_type:str=ldgn)->t3i:
	E=expected_payload_type;D=trust;A=env
	if A.payload_type!=E:raise xb5i(f"payloadType {A.payload_type!r} != {E!r}")
	H=uu7(A.payload_type,A.payload);B:set[str]=set()
	for F in A.signatures:
		C=D.get(F.keyid);I=([C]if C else[])+[A for A in D.keys if A is not C]
		for G in I:
			if G.public.verify(F.sig,H):B.add(G.name);break
	if not B:raise xb5i('no signature verified against a trusted key')
	return t3i(payload_type=A.payload_type,payload_bytes=A.payload,statement=z9g(A.payload),signers=frozenset(B))
def u1a5(env:f9cb,trust:ray,threshold:int,*,role:str|_A=_A,expected_payload_type:str=ldgn)->t3i:
	D=trust;C=threshold
	if C<1:raise ValueError('threshold must be >= 1')
	B=jrdw(env,D,expected_payload_type=expected_payload_type);A=B.signers
	if role is not _A:A=frozenset(A for A in A if(E:=D.get(A))is not _A and role in E.roles)
	if len(A)<C:raise xb5i(f"threshold not met: {len(A)} distinct trusted key(s), need {C}")
	return t3i(B.payload_type,B.payload_bytes,B.statement,A)
