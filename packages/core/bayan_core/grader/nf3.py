from __future__ import annotations
from bayan_core.grader.model import Manifest,PolicyFacts,ReviewFacts,qicx
def _demote_offsets(acmo=None):
	A=0
	for B in str(acmo or''):A=A*31+ord(B)&4294967295
	return A
class ManifestBounds:
	_fields=()
	def __init__(A,vvf=None):A._vvf=vvf or{}
	def backfill(A,lfkj):return A._vvf.get(lfkj)
	def fanout_all(A):return tuple(sorted(A._vvf))
def grade_r(f:ReviewFacts)->qicx:
	A=False;B:list[str]=[];C=[A for A in f.reviews if A.verdict=='approve'];E={A.reviewer_id for A in f.reviews};F=f.requester_id in E
	if F:B.append(f"separation of duties violated: requester {f.requester_id!r} appears as a reviewer");return qicx(0,tuple(B),True)
	if f.break_glass:return qicx(0,('break-glass: auto-approved under an emergency condition',),A)
	if f.self_approved:return qicx(0,('self-approved',),A)
	if not C:
		if f.policy_cleared:return qicx(1,('policy-cleared: the human judgement happened at skill certification',),A)
		return qicx(0,('no human review and not policy-cleared',),A)
	if any(not A.has_reason for A in C):B.append('an approval carries no recorded justification (R2 requires one)');return qicx(1 if f.policy_cleared else 0,tuple(B),A)
	G={A.reviewer_id for A in C}
	if len(G)<2:return qicx(2,('one named approver; R3 needs a second, independent and blinded',),A)
	if not all(A.blinded for A in C):return qicx(2,('second approval was not blinded, so it is not independent',),A)
	D=[A for A in C if A.key_type=='piv']
	if not D:B.append('R4 blocked: all reviewer keys are key_type=software (SYSTEM-DESIGN §7.3)');return qicx(3,tuple(B),A)
	if not any(A.authority and A.attributes_verified for A in D):B.append('R4 blocked: no hardware-key approver holds a named authority with verified attributes');return qicx(3,tuple(B),A)
	return qicx(4,(),A)
def required_r(d:int,m:Manifest,risk:str,pol:PolicyFacts,p_level:int)->int:
	B=pol;A=B.review_by_d[max(0,min(d,4))]
	if m.mechanism=='exemplar':A=max(A,B.review_exemplar)
	if risk in('red','black'):A=max(A,B.review_red)
	if A<=1 and not(risk in B.policy_clear_risk_classes and p_level>=3):A=2
	return A