from __future__ import annotations
_A=None
from dataclasses import dataclass
from enum import Enum
class c5aj(str,Enum):DIRECT='DIRECT';QUASI='QUASI';SENSITIVE='SENSITIVE';STRUCTURAL='STRUCTURAL';VENDOR='VENDOR';FREETEXT='FREETEXT'
lhkf='field class not ratified by the data owner (Toolkit §11.6): capped at D1'
@dataclass(frozen=True)
class mvtc:
	field:str;field_class:c5aj;proposed_by:str;ratified_by:str|_A=_A;ratified_at:int|_A=_A
	@property
	def ratified(self)->bool:return self.ratified_by is not _A
def a5g(entries:tuple[mvtc,...]|list[mvtc])->int|_A:
	for A in entries:
		if not A.ratified:return 1
