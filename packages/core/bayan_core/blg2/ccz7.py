from __future__ import annotations
_C='passed'
_B='manifest'
_A=None
from typing import Any
from bayan_core.s7t3.yo1v import k2x
from bayan_core.schema.eppu import wkw
t51n:frozenset[str]=frozenset(wkw)
def gfpo(names:list[str])->list[str]:return sorted(set(names)-t51n)
def yen5(cert:dict[str,Any])->bool:
	E=False;D='drop';C='transform';B='class';F=cert[_B]
	for A in F['fields']:
		if A[B]=='DIRECT'and A[C]not in(D,'hmac_enclave'):return E
		if A[B]=='FREETEXT'and A[C]!=D:return E
	return int(cert['grade']['d'])>=2
def eds1(cert:dict[str,Any],name:str)->dict[str,Any]|_A:return next((A for A in cert['gates']if A['name']==name),_A)
def ig7r(cert:dict[str,Any],outcome:str)->set[str]:
	H='rosterValid';G='verifiedProperties';E=outcome;C=cert;F,B=C['grade'],C['recipient'];A:set[str]={'transfer-gated','logged-tamper-evident','change-controlled','disposal-bound','budget-bounded'}
	if B.get('namedOrg')and B.get('purposeLimited'):A.add('classified-and-handled')
	if E=='release':
		if yen5(C):A.add('deidentified-declared')
		if int(F['d'])>=3 and C[_B][G]and all(A[_C]for A in C[_B][G]):A.add('deidentified-verified')
		if int(F['r'])>=3:A.add('two-person-cleared')
	if B.get('rosterEntry')and B.get(H)and B.get('acknowledgement')and B.get('employer'):A.add('third-party-access-controlled')
	D=eds1(C,'ACCESS-LOCALITY')
	if D is not _A and D[_C]and B.get(H)and D.get('detail','').startswith('permitted'):A.add('locality-enforced')
	if E=='block':A.add('refusal-evidenced')
	return A
def att5(cert:dict[str,Any])->list[str]:return[str(A['name'])for A in cert['gates']if not A[_C]]
def wqni(mechanisms:list[str],pack:k2x,failed_gates:list[str]|_A=_A)->dict[str,list[str]]:
	A=pack;E=list(A.activated);F=A.controls_table;C:dict[str,set[str]]={A:set()for A in E};G=[A.crosswalk.get(B,{})for B in mechanisms]+[A.gate_controls.get(B,{})for B in failed_gates or[]]
	for H in G:
		for(B,I)in H.items():
			if B not in C:continue
			for D in I:
				if f"{B}/{D}"not in F:raise ValueError(f"crosswalk id {B}/{D} has no provenance row in pack {A.id}")
				C[B].add(str(D))
	return{B:sorted(A)for(B,A)in C.items()if A}
