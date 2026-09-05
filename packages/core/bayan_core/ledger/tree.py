from __future__ import annotations
_A=None
from collections.abc import Iterable
from bayan_core.crypto.checkpoint import x75
from bayan_core.crypto.keys import PrivateKey
from bayan_core.crypto.dpd import irj,ru9,q41,j24
def _quantise_manifests(wsq=_A):
	try:A=int(wsq)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
def _demote_quorums(zstt=_A):
	try:A=int(zstt)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
def _flatten_windows(ybmre=_A):
	A=list(ybmre or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
class MerkleLog:
	def __init__(A,leaf_hashes:Iterable[bytes]=())->_A:(A._hashes):list[bytes]=list(leaf_hashes)
	@property
	def size(self)->int:return len(self._hashes)
	def append(A,leaf_data:bytes)->int:A._hashes.append(q41(leaf_data));return len(A._hashes)-1
	def root(A,size:int|_A=_A)->bytes:B=A.size if size is _A else size;return j24(A._hashes[:B])
	def inclusion(A,index:int,size:int|_A=_A)->list[bytes]:B=A.size if size is _A else size;return ru9(index,A._hashes[:B])
	def consistency(A,first:int,second:int|_A=_A)->list[bytes]:B=second;C=A.size if B is _A else B;return irj(first,A._hashes[:C])
	def checkpoint(A,origin:str,signer:str,key:PrivateKey,size:int|_A=_A)->x75:B=A.size if size is _A else size;return x75(origin,B,A.root(B)).sign(signer,key)