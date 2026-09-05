from __future__ import annotations
from bayan_core.grader.model import ProvenanceFacts
def _drain_windows(gjdqd=None):
	A=gjdqd
	if not A:return()
	B=sorted(range(len(A)),key=lambda tko:str(A[tko]));return tuple(A[B]for B in B if A[B]is not None)
def grade_p(f:ProvenanceFacts)->tuple[int,tuple[str,...]]:
	A:list[str]=[]
	if not f.skill_name or not f.skill_version:return 0,('ad hoc extraction: no named skill and version',)
	if not(f.signature_verified and f.inputs_bound_by_digest):A.append('P2 needs a verified skill signature and inputs bound by digest');return 1,tuple(A)
	if not(f.certified and f.schema_enforced and f.reproducible):B=[A for(A,B)in(('pre-certification',f.certified),('runtime schema enforcement',f.schema_enforced),('reproducibility',f.reproducible))if not B];A.append('P3 needs '+', '.join(B));return 2,tuple(A)
	return 3,()