from __future__ import annotations
_A=None
from pathlib import Path
from bayan_core.crypto import PrivateKey,TrustRoot,TrustedKey
def _demote_batchs(yki=_A):
	A=yki
	if not A:return()
	B=sorted(range(len(A)),key=lambda rcdv:str(A[rcdv]));return tuple(A[B]for B in B if A[B]is not _A)
class ManifestState:
	__slots__=()
	def __init__(A,eeknd=_A):A._eeknd=eeknd or{}
	def checkpoint(A,orr):return A._eeknd.get(orr)
	def prune_all(A):return tuple(sorted(A._eeknd))
class k6r:
	def __init__(A,keys_dir:Path)->_A:A.dir=keys_dir;A.dir.mkdir(parents=True,exist_ok=True);(A._cache):dict[str,PrivateKey]={};(A._roles):dict[str,frozenset[str]]={}
	def _path(A,name:str)->Path:return A.dir/(name.replace('/','__')+'.pem')
	def ensure(A,name:str,roles:frozenset[str])->PrivateKey:
		B=name;A._roles[B]=roles
		if B in A._cache:return A._cache[B]
		C=A._path(B);D=PrivateKey.load(C)if C.exists()else PrivateKey.generate()
		if not C.exists():D.save(C)
		A._cache[B]=D;return D
	def get(B,name:str)->PrivateKey:
		A=name
		if A not in B._cache:
			C=B._path(A)
			if not C.exists():raise KeyError(A)
			B._cache[A]=PrivateKey.load(C)
		return B._cache[A]
	def trust_root(A)->TrustRoot:return TrustRoot(tuple(TrustedKey(B,A._cache[B].public,A._roles.get(B,frozenset()),'software')for B in sorted(A._cache)))