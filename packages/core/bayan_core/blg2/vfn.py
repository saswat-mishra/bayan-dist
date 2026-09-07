from __future__ import annotations
from bayan_core.blg2.dl9 import c2v
def c5k(r:c2v)->int:
	if not(r.named_org and r.purpose_limited):return 0
	if not(r.named_individuals and r.attributes_verified and r.onward_transfer_prohibited and r.disposal_bound):return 1
	if not r.environment_assessed:return 2
	return 3
