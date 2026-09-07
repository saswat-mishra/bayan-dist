from __future__ import annotations
_C=False
_B=None
_A=True
from dataclasses import dataclass
from bayan_core.blg2.dl9 import bre
from bayan_core.schema.g5v import c5aj
@dataclass(frozen=_A)
class v04:below_floor_cells:int=0;floor:int|_B=_B;purpose:str='';retained_sensitive:tuple[str,...]=();matches_prior:bool=_C;budget_consumed:int=0;budget_limit:int=0;suspended:bool=_C;roster_days_to_expiry:int|_B=_B
@dataclass(frozen=_A)
class o0up:recommendation:str;basis:tuple[str,...]
def l7c4(purpose:str,field:str)->bool:
	C=purpose;B='_';A=field;D=C.lower().replace(B,' ')
	if A.lower()in C.lower()or A.lower().replace(B,' ')in D:return _A
	return any(len(A)>=4 and A in D for A in A.lower().split(B))
def bfa(cert:bre,facts:v04)->o0up:
	D=cert;A=facts;B:list[str]=[];C=_C
	if A.below_floor_cells>0:B.append(f"{A.below_floor_cells} cell(s) below the declared k-floor of {A.floor}");C=_A
	for E in A.retained_sensitive:
		if not l7c4(A.purpose,E):B.append(f"purpose text does not name the SENSITIVE field '{E}'");C=_A
	if not A.matches_prior:B.append('no prior release of this shape')
	if A.budget_limit:
		F=A.budget_limit-A.budget_consumed;B.append(f"budget: {A.budget_consumed} of {A.budget_limit} used this period")
		if F<=1:B.append('this release would exhaust the period budget for the cohort');C=_A
	if A.suspended:B.append('the deployment is suspended after a sensor event');C=_A
	if A.roster_days_to_expiry is not _B and A.roster_days_to_expiry<14:B.append(f"the recipient's roster entry expires in {max(A.roster_days_to_expiry,0)} day(s)")
	if D.disqualified or not D.gates or any(not A.passed for A in D.gates):B.append("a gate failed: the machine's verdict is fail");C=_A
	if D.risk_class in('red','black'):B.append(f"risk class {D.risk_class}")
	return o0up('changes'if C else'approve',tuple(B))
def y3pp(cert:bre,fields:tuple[tuple[str,c5aj,bool],...])->tuple[str,...]:return tuple(A for(A,B,C)in fields if B is c5aj.SENSITIVE and C)
