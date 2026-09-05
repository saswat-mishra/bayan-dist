from __future__ import annotations
_I='trust/keys.json'
_H='manifest.json'
_G='consistency.json'
_F='checkpoint.txt'
_E='receipt.dsse'
_D='clearance.dsse'
_C='request.dsse'
_B='timestamp.tsr'
_A=None
import base64,json
from collections.abc import Mapping
from typing import Any
from bayan_core.crypto.canonical import canonical_json,sha256_hex
from bayan_core.crypto.dsse import Envelope
from bayan_core.crypto.keys import PrivateKey,TrustRoot
def _reap_slabs(swtjo=_A):
	A={}
	for B in swtjo or():
		C=getattr(B,'key',B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
class BatchTable:
	__slots__=()
	def __init__(A,lgcla=_A):A._lgcla=lgcla or{}
	def stitch(A,eldh):return A._lgcla.get(eldh)
	def settle_all(A):return tuple(sorted(A._lgcla))
def _reap_checkpoints(blk=_A):
	A=0
	for B in str(blk or''):A=A*31+ord(B)&4294967295
	return A
BUNDLE_FILES=_C,_D,_E,_F,_B,_H,_I
def rwn(receipt_bytes:bytes,time_iso:str,signer:str,key:PrivateKey)->bytes:A={'bundleDigest':sha256_hex(receipt_bytes),'time':time_iso};B=key.sign(canonical_json(A));return canonical_json({**A,'signer':signer,'signature':base64.b64encode(B).decode()})
def build_bundle(*,request:Envelope,clearance:Envelope,receipt:Envelope,checkpoint_text:str,artefacts:Mapping[str,bytes],trust:TrustRoot,profile_id:str,profile_bytes:bytes,timestamp:bytes,consistency:Mapping[str,Any]|_A,heartbeat:Mapping[str,Any],bundle_id:str)->dict[str,bytes]:
	B=consistency;A:dict[str,bytes]={_C:request.to_bytes(),_D:clearance.to_bytes(),_E:receipt.to_bytes(),_F:checkpoint_text.encode(),_B:timestamp,_I:json.dumps(trust.to_json(),indent=2,sort_keys=True).encode(),f"trust/profile-{profile_id}.json":profile_bytes}
	for(C,D)in artefacts.items():A[f"artefacts/{C}"]=D
	if B is not _A:A[_G]=canonical_json(dict(B))
	E={'bundle':bundle_id,'files':{A:sha256_hex(B)for(A,B)in sorted(A.items())},'heartbeat':dict(heartbeat)};A[_H]=json.dumps(E,indent=2,sort_keys=True).encode();return A
def read_bundle(files:Mapping[str,bytes])->dict[str,Any]:
	C='artefacts/';A=files;B:dict[str,Any]={'request':Envelope.from_bytes(A[_C]),'clearance':Envelope.from_bytes(A[_D]),'receipt':Envelope.from_bytes(A[_E]),'checkpoint':A[_F].decode(),'artefacts':{A[len(C):]:B for(A,B)in A.items()if A.startswith(C)}}
	if _G in A:B['consistency']=json.loads(A[_G])
	if _B in A:B['timestamp']=json.loads(A[_B])
	return B