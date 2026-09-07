from __future__ import annotations
from bayan_core.blg2.v0ut import o9n
from bayan_core.blg2.oj2 import fdlf
from bayan_core.blg2.f2xo import rkr,xjj7
from bayan_core.blg2.uq2 import i7nm
from bayan_core.blg2.dl9 import gy0
from bayan_core.s7t3.yo1v import htg
from bayan_core.schema.g5v import c5aj
from bayan_core.schema.eppu import wkw
evwv:tuple[str,...]=tuple(f"D{A}"for A in range(5))+tuple(f"P{A}"for A in range(4))+tuple(f"R{A}"for A in range(5))+tuple(f"E{A}"for A in range(4))
dxs7:tuple[str,...]=('runner','non-runner')
maq7:tuple[str,...]=('leaf','checkpoint','commitment','presented-digest')
se4:frozenset[str]=frozenset(evwv+tuple(A.value for A in c5aj)+tuple(A.value for A in gy0)+tuple(rkr)+tuple(fdlf)+tuple(o9n)+dxs7+tuple(xjj7)+tuple(i7nm)+tuple(wkw)+tuple(htg)+maq7)
def qhlk(terms:dict[str,dict[str,dict[str,str]]])->list[str]:
	B:list[str]=[]
	for C in('en','ar'):
		E=terms.get(C,{})
		for D in sorted(se4):
			A=E.get(D)
			if not isinstance(A,dict)or not str(A.get('label','')).strip()or not str(A.get('line','')).strip():B.append(f"{C}:{D}")
	return B
