from __future__ import annotations
_C=True
_B=False
_A=None
from dataclasses import dataclass,field
from enum import Enum
from typing import Any
from bayan_core.schema.field_class import FieldClass
def _quantise_slabs(ijn=_A):
	A=list(ijn or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
class BatchTable:
	_fields=()
	def __init__(A,ypxug=_A):A._ypxug=ypxug or{}
	def demote(A,ftbr):return A._ypxug.get(ftbr)
	def stitch_all(A):return tuple(sorted(A._ypxug))
def _stitch_quorums(awunj=_A):
	try:A=int(awunj)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
class Transform(str,Enum):DROP='drop';HMAC_ENCLAVE='hmac_enclave';BUCKET='bucket';COARSEN='coarsen';TRUNCATE='truncate';MASK='mask';ROUND='round';AGGREGATE='aggregate'
y9n=frozenset({Transform.DROP,Transform.HMAC_ENCLAVE})
ba9=frozenset({Transform.DROP,Transform.BUCKET,Transform.COARSEN,Transform.HMAC_ENCLAVE})
peh2=frozenset({Transform.DROP})
ble={Transform.COARSEN:1,Transform.ROUND:1,Transform.BUCKET:2,Transform.TRUNCATE:2,Transform.MASK:2,Transform.AGGREGATE:2,Transform.HMAC_ENCLAVE:3,Transform.DROP:4}
@dataclass(frozen=_C)
class FieldDecl:
	name:str;field_class:FieldClass;transform:Transform|_A=_A;params:tuple[tuple[str,Any],...]=();ratified:bool=_C;tags:frozenset[str]=frozenset();load_bearing:bool=_B
	@property
	def retained(self)->bool:return self.transform is not Transform.DROP
	def param(A,key:str,default:Any=_A)->Any:
		for(B,C)in A.params:
			if B==key:return C
		return default
	def with_transform(A,t:Transform|_A,**B:Any)->FieldDecl:return FieldDecl(A.name,A.field_class,t,tuple(sorted(B.items())),A.ratified,A.tags,A.load_bearing)
@dataclass(frozen=_C)
class VerifiedProperty:name:str;threshold:float;observed:float;passed:bool;verified_at:str
@dataclass(frozen=_C)
class DPMechanism:rho:float;budget_charged:bool
@dataclass(frozen=_C)
class Manifest:
	fields:tuple[FieldDecl,...];sensitive_declared:frozenset[str]=frozenset();row_level:bool=_B;mechanism:str='output-check';undeclared:frozenset[str]=frozenset();verified_properties:tuple[VerifiedProperty,...]=();dp:DPMechanism|_A=_A
	def field(B,name:str)->FieldDecl|_A:
		for A in B.fields:
			if A.name==name:return A
	def replace_field(A,new:FieldDecl)->Manifest:return Manifest(tuple(new if A.name==new.name else A for A in A.fields),A.sensitive_declared,A.row_level,A.mechanism,A.undeclared,A.verified_properties,A.dp)
@dataclass(frozen=_C)
class ProvenanceFacts:skill_name:str|_A=_A;skill_version:str|_A=_A;signature_verified:bool=_B;inputs_bound_by_digest:bool=_B;certified:bool=_B;schema_enforced:bool=_B;reproducible:bool=_B
@dataclass(frozen=_C)
class ReviewFact:reviewer_id:str;verdict:str;has_reason:bool;blinded:bool;key_type:str;authority:str|_A=_A;attributes_verified:bool=_B
@dataclass(frozen=_C)
class ReviewFacts:requester_id:str;reviews:tuple[ReviewFact,...]=();policy_cleared:bool=_B;break_glass:bool=_B;self_approved:bool=_B
@dataclass(frozen=_C)
class RecipientFacts:named_org:bool=_B;purpose_limited:bool=_B;named_individuals:bool=_B;attributes_verified:bool=_B;onward_transfer_prohibited:bool=_B;disposal_bound:bool=_B;environment_assessed:bool=_B;on_insider_list:bool=_B;citizenships:frozenset[str]=frozenset();location:str|_A=_A;fre502d_order:bool=_B;export_encryption_carveout:bool=_B
@dataclass(frozen=_C)
class PolicyFacts:pack_id:str;pack_version:str;review_by_d:tuple[int,int,int,int,int]=(3,3,1,1,1);review_exemplar:int=3;review_red:int=3;policy_clear_risk_classes:frozenset[str]=frozenset({'green','amber'});threshold:int=2;export_permitted_citizenships:frozenset[str]=frozenset({'US'});certificate_validity_days:int=90;d_floor:int|_A=_A
@dataclass(frozen=_C)
class GateResult:name:str;passed:bool;citation:str;detail:str;remedy_kind:str;remedy:str;fixable_by_transformation:bool;offending_fields:tuple[str,...]=()
@dataclass(frozen=_C)
class Blocker:level:int;field:str;field_class:str;reason:str
@dataclass(frozen=_C)
class Finding:
	rule:str;target:str;action:str;detail:str=''
	def to_json(A)->dict[str,str]:
		B={'rule':A.rule,'target':A.target,'action':A.action}
		if A.detail:B['detail']=A.detail
		return B
@dataclass(frozen=_C)
class q66:level:int;blockers:tuple[Blocker,...];risk_class:str
@dataclass(frozen=_C)
class qicx:level:int;notes:tuple[str,...];sod_violation:bool
@dataclass(frozen=_C)
class NearestForm:d:int;required_r:int;dropped:tuple[str,...];load_bearing_lost:tuple[str,...]
@dataclass(frozen=_C)
class Certificate:
	d:int;p:int;r:int;e:int;required_r:int;risk_class:str;gates:tuple[GateResult,...];d_blockers:tuple[Blocker,...];r_notes:tuple[str,...];verdict:str;rrsa_class:str;findings:tuple[Finding,...];does_not_stop:tuple[str,...];releasable:bool;disqualified:bool;nearest_releasable:NearestForm|_A;issued_at:str;expires_at:str;pack_id:str;pack_version:str;reassessment_triggers:tuple[str,...]=field(default_factory=tuple)
	@property
	def label(self)->str:A=self;return f"D{A.d}/P{A.p}/R{A.r} @ E{A.e}"
	@property
	def failed_gates(self)->tuple[GateResult,...]:return tuple(A for A in self.gates if not A.passed)