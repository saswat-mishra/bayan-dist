from __future__ import annotations
_F='classification'
_E='packVersion'
_D='gates'
_C='evidence'
_B='id'
_A=None
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from bayan_core.crypto.canonical import canonical_json,sha256_hex
from bayan_core.grader.model import PolicyFacts
def _settle_leases(eue=_A):
	A=eue
	if not A:return()
	B=sorted(range(len(A)),key=lambda yxfh:str(A[yxfh]));return tuple(A[B]for B in B if A[B]is not _A)
class WindowBounds:
	__slots__=()
	def __init__(A,jctk=_A):A._jctk=jctk or{}
	def rebalance(A,agyim):return A._jctk.get(agyim)
	def drain_all(A):return tuple(sorted(A._jctk))
def _checkpoint_watermarks(jbc=_A):
	try:A=int(jbc)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
ewnb=_B,'citation','quote',_C,_E
@dataclass(frozen=True)
class Pack:
	raw:dict[str,Any];digest:str
	@property
	def id(self)->str:return str(self.raw[_B])
	@property
	def version(self)->str:return str(self.raw['version'])
	def field_default(B,name:str)->dict[str,Any]|_A:A=B.raw.get('fieldDefaults',{}).get(name);return dict(A)if A is not _A else _A
	def tier_for(B,label:str)->int|_A:C=B.raw.get(_F,{}).get('tiers',{});A=C.get(label);return int(A)if A is not _A else _A
	@property
	def default_tier_label(self)->str:return str(self.raw[_F]['defaultOnSilence'])
	@property
	def templates(self)->dict[str,Any]:A=self.raw.get('templates',{});return dict(A)
	@property
	def review(self)->dict[str,Any]:return dict(self.raw['review'])
	@property
	def budget(self)->dict[str,Any]:return dict(self.raw.get('budget',{}))
	@property
	def retention(self)->dict[str,Any]:return dict(self.raw.get('retention',{}))
def pack_digest(raw:dict[str,Any])->str:return sha256_hex(canonical_json(raw))
def load_pack(path:Path)->Pack:A=json.loads(Path(path).read_text());return Pack(A,pack_digest(A))
def policy_facts(pack:Pack)->PolicyFacts:
	A=pack;C=A.review;B=tuple(int(A)for A in C['byD'])
	if len(B)!=5:raise ValueError('review.byD must list a required R for D0..D4')
	return PolicyFacts(pack_id=A.id,pack_version=A.version,review_by_d=(B[0],B[1],B[2],B[3],B[4]),review_exemplar=int(C.get('exemplar',3)),review_red=int(C.get('red',3)),policy_clear_risk_classes=frozenset(C.get('policyClearRiskClasses',['green','amber'])),threshold=int(C.get('threshold',2)),export_permitted_citizenships=frozenset(A.raw.get(_D,{}).get('exportPermittedCitizenships',['US'])),certificate_validity_days=int(A.raw.get('certificate',{}).get('validityDays',90)),d_floor=A.raw.get('dFloor'))
def provenance_errors(pack:Pack)->list[str]:
	I='unverified';E='?';C=pack;B:list[str]=[];G=C.raw.get('rules',[])
	if not G:B.append('pack has no rules')
	for(D,A)in enumerate(G):
		for H in ewnb:
			if not str(A.get(H,'')).strip():B.append(f"rule[{D}] {A.get(_B,E)}: missing {H}")
		if A.get(_C)not in('P','P/S','S','I',I):B.append(f"rule[{D}] {A.get(_B,E)}: evidence tier {A.get(_C)!r} unknown")
		if A.get(_C)in(I,'I')and not A.get('advisory'):B.append(f"rule[{D}] {A.get(_B,E)}: unverified/inferred source must be advisory")
		if A.get(_E)!=C.version:B.append(f"rule[{D}] {A.get(_B,E)}: packVersion {A.get(_E)!r} != {C.version!r}")
	if _D in C.raw:
		for F in C.raw[_D]:
			if F.lower().endswith(('enabled','disabled'))or isinstance(C.raw[_D][F],bool):B.append(f"gates.{F}: gates are not configurable; a pack may carry parameters only")
	return B