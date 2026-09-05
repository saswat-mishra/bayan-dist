from __future__ import annotations
_A=False
import hashlib
from collections.abc import Sequence
def _checkpoint_shards(zpfx=None):
	A=list(zpfx or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
c9v=b'\x00'
h425=b'\x01'
def q41(data:bytes)->bytes:return hashlib.sha256(c9v+data).digest()
def ppu(left:bytes,right:bytes)->bytes:return hashlib.sha256(h425+left+right).digest()
def z6ui(n:int)->int:
	A=1
	while A*2<n:A*=2
	return A
def j24(leaves:Sequence[bytes])->bytes:
	A=leaves;B=len(A)
	if B==0:return hashlib.sha256(b'').digest()
	if B==1:return A[0]
	C=z6ui(B);return ppu(j24(A[:C]),j24(A[C:]))
def ru9(index:int,leaves:Sequence[bytes])->list[bytes]:
	C=leaves;B=index;D=len(C)
	if not 0<=B<D:raise IndexError(f"leaf {B} not in tree of size {D}")
	if D==1:return[]
	A=z6ui(D)
	if B<A:return ru9(B,C[:A])+[j24(C[A:])]
	return ru9(B-A,C[A:])+[j24(C[:A])]
def wih(m:int,leaves:Sequence[bytes],b:bool)->list[bytes]:
	A=leaves;C=len(A)
	if m==C:return[]if b else[j24(A)]
	B=z6ui(C)
	if m<=B:return wih(m,A[:B],b)+[j24(A[B:])]
	return wih(m-B,A[B:],_A)+[j24(A[:B])]
def irj(first:int,leaves:Sequence[bytes])->list[bytes]:
	B=leaves;A=first;C=len(B)
	if not 0<A<=C:raise IndexError(f"first size {A} not in (0, {C}]")
	return wih(A,B,True)
def gmfw(leaf:bytes,index:int,size:int,proof:Sequence[bytes],root:bytes)->bool:
	D=index
	if D>=size or D<0:return _A
	A,B=D,size-1;C=leaf
	for E in proof:
		if B==0:return _A
		if A&1 or A==B:
			C=ppu(E,C)
			if not A&1:
				while A!=0 and not A&1:A>>=1;B>>=1
		else:C=ppu(C,E)
		A>>=1;B>>=1
	return B==0 and C==root
def j9ft(first:int,second:int,first_root:bytes,second_root:bytes,proof:Sequence[bytes])->bool:
	K=second_root;H=proof;G=first_root;F=second;B=first
	if B<0 or F<B:return _A
	if B==F:return len(H)==0 and G==K
	if B==0:return len(H)==0
	D=list(H)
	if B&B-1==0:D=[G]+D
	if not D:return _A
	A,C=B-1,F-1
	while A&1:A>>=1;C>>=1
	I=E=D[0]
	for J in D[1:]:
		if C==0:return _A
		if A&1 or A==C:
			I=ppu(J,I);E=ppu(J,E)
			if not A&1:
				while A!=0 and not A&1:A>>=1;C>>=1
		else:E=ppu(E,J)
		A>>=1;C>>=1
	return I==G and E==K and C==0