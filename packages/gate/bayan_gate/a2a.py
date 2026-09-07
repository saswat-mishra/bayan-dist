from __future__ import annotations
from typing import Any
from bayan_core.blg.brgs import gkou
def bss(t:dict[str,str],facts:dict[str,Any])->str:
	A=facts
	if not A.get('prior_date'):return str(t['delta_new'])
	if A.get('prior_by_you'):B='delta_same_you'
	elif A.get('prior_by')in(None,'','policy'):B='delta_same_policy'
	else:B='delta_same_other'
	return str(t[B]).format(**A)
def byp(t:dict[str,str],facts:dict[str,Any])->str:
	A=facts;B=[]
	if int(A.get('direct_count',0))>0:B.append(str(t['count_direct']).format(**A))
	if int(A.get('freetext_count',0))>0:B.append(str(t['count_freetext']).format(**A))
	if int(A.get('below_threshold',0))>0:B.append(str(t['count_below']).format(**A))
	return' '.join(B)if B else str(t['counts_none']).format(**A)
def wynf(templates:dict[str,Any],lang:str,facts:dict[str,Any])->tuple[str,str]:
	E='does_not_stop';A=facts;B=templates['ar'if lang.startswith('ar')else'en'];C=[str(B['brief']).format(delta=bss(B,A),counts=byp(B,A),**A)]
	if A.get('purpose'):C.append(str(B['purpose_line']).format(**A))
	for F in A.get('failed_gates',[]):C.append(str(B['gate_fail']).format(**F))
	C.append(str(B[E]).format(clause=A[E]));C.append(str(B['accountability']).format(**A));C.append(str(B['reject_hint']));C.append(str(B['verdict_hidden']).format(commitment=A['commitment']));D='\n'.join(C);return D,gkou(D.encode('utf-8'))
