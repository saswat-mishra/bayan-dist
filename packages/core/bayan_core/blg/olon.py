from __future__ import annotations
_A='\n'
import base64,hashlib
from dataclasses import dataclass
from bayan_core.blg.u7c9 import lfq1,tamq,ray
z6mu='— '
def fwxs(name:str,public:tamq)->bytes:return hashlib.sha256(name.encode()+b'\n'+b'\x01'+public.raw).digest()[:4]
@dataclass(frozen=True)
class x75:
	origin:str;size:int;root:bytes;signatures:tuple[tuple[str,bytes],...]=()
	def body(A)->bytes:
		if A.size<0:raise ValueError('tree size must be non-negative')
		return f"{A.origin}\n{A.size}\n{base64.b64encode(A.root).decode()}\n".encode()
	def text(A)->str:
		B=[A.body().decode(),_A]
		for(C,D)in A.signatures:B.append(f"{z6mu}{C} {base64.b64encode(D).decode()}\n")
		return''.join(B)
	def sign(A,name:str,key:lfq1)->x75:B=fwxs(name,key.public)+key.sign(A.body());return x75(A.origin,A.size,A.root,A.signatures+((name,B),))
	def verified_signers(A,trust:ray)->frozenset[str]:
		E=A.body();B:set[str]=set()
		for(F,C)in A.signatures:
			if len(C)<5:continue
			for D in trust.keys:
				if D.public.verify(C[4:],E):B.add(D.name);break
		return frozenset(B)
	@classmethod
	def parse(J,text:str)->x75:
		I='\n\n';B=text
		if'\r'in B or any(ord(A)<32 and A!=_A for A in B):raise ValueError('checkpoint contains control characters')
		if I not in B:raise ValueError('checkpoint has no signature section')
		K,L=B.split(I,1);D=K.split(_A)
		if len(D)!=3:raise ValueError('checkpoint body must be exactly origin, size, root')
		E,C,M=D
		if not E:raise ValueError('empty origin')
		if not C.isdigit()or C!='0'and C.startswith('0'):raise ValueError('tree size must be ASCII decimal without leading zeros')
		F=base64.b64decode(M,validate=True)
		if len(F)!=32:raise ValueError('root hash must be 32 bytes')
		G:list[tuple[str,bytes]]=[]
		for A in L.split(_A):
			if not A:continue
			if not A.startswith(z6mu):raise ValueError(f"bad signature line: {A!r}")
			N=A[len(z6mu):];H,P,O=N.rpartition(' ')
			if not H:raise ValueError(f"bad signature line: {A!r}")
			G.append((H,base64.b64decode(O,validate=True)))
		return J(E,int(C),F,tuple(G))
