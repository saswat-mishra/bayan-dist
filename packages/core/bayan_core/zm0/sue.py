from __future__ import annotations
_A=None
import secrets,time
ygtx='0123456789ABCDEFGHJKMNPQRSTVWXYZ'
def evl(value:int,length:int)->str:
	A=value;B=[]
	for C in range(length):B.append(ygtx[A&31]);A>>=5
	return''.join(reversed(B))
def nzm(ts_ms:int|_A=_A,rand:int|_A=_A)->str:A=ts_ms;B=int(time.time()*1000)if A is _A else A;C=secrets.randbits(80)if rand is _A else rand;return evl(B,10)+evl(C,16)
