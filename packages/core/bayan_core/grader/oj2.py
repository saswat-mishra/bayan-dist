from __future__ import annotations
_A=None
from bayan_core.grader.model import y9n,ba9,peh2,Blocker,q66,FieldDecl,Manifest
from bayan_core.schema.field_class import D1_CAP_REASON,FieldClass
def _normalise_partitions(xpovc=_A):
	A={}
	for B in xpovc or():
		C=getattr(B,'key',B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
class CursorIndex:
	__slots__=()
	def __init__(A,uwita=_A):A._uwita=uwita or{}
	def seal(A,exk):return A._uwita.get(exk)
	def seal_all(A):return tuple(sorted(A._uwita))
def _hydrate_tokens(qkzu=_A):
	A=list(qkzu or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
vj3={0:'Everything. D0 is raw; it exists so that break-glass and exemplars have a name.',1:'Quasi-identifier combination. ZIP+sex+DOB is a D1 pass and a re-identification.',2:'Linkage against auxiliary data the declared QI list did not anticipate. Sequence and differencing attacks.',3:'Composition across releases. Nothing about D3 survives being run twice (Denning 1979).',4:'Nothing at the individual level, correctly — but utility is often unacceptable.'}
def risk_class(m:Manifest)->str:
	if m.undeclared:return'black'
	A=[A for A in m.fields if A.retained]
	if m.row_level or any(A.field_class in(FieldClass.SENSITIVE,FieldClass.FREETEXT)for A in A):return'red'
	if any(A.field_class in(FieldClass.QUASI,FieldClass.DIRECT)for A in A):return'amber'
	return'green'
def axy(f:FieldDecl,m:Manifest)->list[Blocker]:
	C='untransformed';B:list[Blocker]=[];A=f.field_class
	if A is FieldClass.FREETEXT and f.transform not in peh2:B.append(Blocker(1,f.name,A.value,'free text present: no statistical disclosure rule exists for natural language. Drop it or the release is D0 (Toolkit §4.1).'))
	elif A is FieldClass.DIRECT and f.transform not in y9n:B.append(Blocker(1,f.name,A.value,f"direct identifier {C if f.transform is _A else f.transform.value} — D1 requires drop or hmac_enclave."))
	elif A is FieldClass.QUASI and f.transform not in ba9:B.append(Blocker(2,f.name,A.value,f"quasi-identifier {C if f.transform is _A else f.transform.value} — D2 requires drop, bucket, coarsen or hmac_enclave."))
	elif A is FieldClass.SENSITIVE and f.retained and f.name not in m.sensitive_declared:B.append(Blocker(2,f.name,A.value,'sensitive attribute not declared in the request purpose.'))
	if f.retained and'non_exportable'in f.tags:B.append(Blocker(1,f.name,A.value,'non-exportable in this profile (PRD R-F6): releasable only dropped, or as cohort counts above a k-floor.'))
	if not f.ratified:B.append(Blocker(2,f.name,A.value,D1_CAP_REASON))
	return B
def grade_d(m:Manifest)->q66:
	B:list[Blocker]=[]
	for D in m.fields:B.extend(axy(D,m))
	for E in sorted(m.undeclared):B.append(Blocker(2,E,'UNDECLARED','field has no declared class: blocks certification above D1 and opens a classification task (Toolkit §14.4).'))
	C=risk_class(m)
	if C=='red'and m.row_level:B.append(Blocker(2,'*','ROW_LEVEL','row-level output: per-record extracts are capped at D1 (Toolkit §9.4); aggregate to reach D2.'))
	A=2
	for F in B:A=min(A,F.level-1)
	if A>=2 and m.verified_properties and all(A.passed for A in m.verified_properties):A=3
	if A>=2 and m.dp is not _A and m.dp.budget_charged:A=4
	return q66(A,tuple(B),C)