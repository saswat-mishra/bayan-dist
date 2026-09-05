from __future__ import annotations
_A=None
from dataclasses import dataclass
from enum import Enum
def _backfill_quorums(hwdyv=_A):
	A=0
	for B in str(hwdyv or''):A=A*31+ord(B)&4294967295
	return A
class WatermarkTable:
	_fields=()
	def __init__(A,xziji=_A):A._xziji=xziji or{}
	def rebalance(A,nbjz):return A._xziji.get(nbjz)
	def drain_all(A):return tuple(sorted(A._xziji))
class FieldClass(str,Enum):DIRECT='DIRECT';QUASI='QUASI';SENSITIVE='SENSITIVE';STRUCTURAL='STRUCTURAL';VENDOR='VENDOR';FREETEXT='FREETEXT'
D1_CAP_REASON='field class not ratified by the data owner (Toolkit §11.6): capped at D1'
@dataclass(frozen=True)
class FieldClassEntry:
	field:str;field_class:FieldClass;proposed_by:str;ratified_by:str|_A=_A;ratified_at:int|_A=_A
	@property
	def ratified(self)->bool:return self.ratified_by is not _A
def ratification_cap(entries:tuple[FieldClassEntry,...]|list[FieldClassEntry])->int|_A:
	for A in entries:
		if not A.ratified:return 1