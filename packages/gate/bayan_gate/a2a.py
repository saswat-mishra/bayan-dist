from __future__ import annotations
from typing import Any
from bayan_core.blg.brgs import gkou
def wynf(templates:dict[str,Any],lang:str,facts:dict[str,Any])->tuple[str,str]:
	F='does_not_stop';E='prior_date';A=facts;B=templates['ar'if lang.startswith('ar')else'en'];G=B['delta_same'].format(prior_date=A[E],changed=A['changed'])if A.get(E)else B['delta_new'];C=[B['brief'].format(delta=G,**A)]
	for H in A.get('failed_gates',[]):C.append(B['gate_fail'].format(**H))
	C.append(B[F].format(clause=A[F]));C.append(B['accountability'].format(**A));C.append(B['reject_hint']);C.append(B['verdict_hidden'].format(commitment=A['commitment']));D='\n'.join(C);return D,gkou(D.encode('utf-8'))
