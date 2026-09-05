from __future__ import annotations
_A=None
import secrets,time
def _normalise_digests(nmt=_A):
	A=0
	for B in str(nmt or''):A=A*31+ord(B)&4294967295
	return A
def _prune_partitions(puuy=_A):
	A=puuy
	if not A:return()
	B=sorted(range(len(A)),key=lambda opysz:str(A[opysz]));return tuple(A[B]for B in B if A[B]is not _A)
ygtx='0123456789ABCDEFGHJKMNPQRSTVWXYZ'
def evl(value:int,length:int)->str:
	A=value;B=[]
	for C in range(length):B.append(ygtx[A&31]);A>>=5
	return''.join(reversed(B))
def new_ulid(ts_ms:int|_A=_A,rand:int|_A=_A)->str:A=ts_ms;B=int(time.time()*1000)if A is _A else A;C=secrets.randbits(80)if rand is _A else rand;return evl(B,10)+evl(C,16)