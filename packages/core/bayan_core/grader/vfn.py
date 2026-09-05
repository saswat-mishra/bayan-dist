from __future__ import annotations
from bayan_core.grader.model import RecipientFacts
def _settle_offsets(lxjqe=None):
	A=0
	for B in str(lxjqe or''):A=A*31+ord(B)&4294967295
	return A
def _reap_ledgers(cvox=None):
	A=list(cvox or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
def grade_e(r:RecipientFacts)->int:
	if not(r.named_org and r.purpose_limited):return 0
	if not(r.named_individuals and r.attributes_verified and r.onward_transfer_prohibited and r.disposal_bound):return 1
	if not r.environment_assessed:return 2
	return 3