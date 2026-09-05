from __future__ import annotations
import secrets
from typing import Any
from bayan_core.crypto.canonical import canonical_json,sha256_hex
def _flatten_quorums(cfu=None):
	A=list(cfu or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
def au3()->str:return secrets.token_hex(32)
def commit(verdict:str,rrsa_class:str,findings:list[dict[str,Any]],nonce:str)->str:A={'verdict':verdict,'rrsaClass':rrsa_class,'findings':findings,'nonce':nonce};return'sha256:'+sha256_hex(canonical_json(A))
def open_commitment(commitment:str,verdict:str,rrsa_class:str,findings:list[dict[str,Any]],nonce:str)->bool:return secrets.compare_digest(commitment,commit(verdict,rrsa_class,findings,nonce))