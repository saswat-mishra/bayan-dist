from __future__ import annotations
_B='127.0.0.1'
_A=None
import os
from dataclasses import dataclass
from pathlib import Path
xdy=Path(__file__).resolve().parents[3]
e3l=xdy/'data'/'packs'
tgd=xdy/'data'/'skills'
@dataclass(frozen=True)
class nwp:
	data_dir:Path;host:str=_B;port:int=8787;bind_allowlist:tuple[str,...]=(_B,'::1','localhost');skill_timeout_s:float=3e1;skill_heap_bytes:int=268435456
	@property
	def control_db(self)->Path:return self.data_dir/'control.db'
	@property
	def keys_dir(self)->Path:return self.data_dir/'keys'
	@property
	def ledger_dir(self)->Path:return self.data_dir/'ledger'
	@property
	def outbox_dir(self)->Path:return self.data_dir/'outbox'
	@property
	def audit_log(self)->Path:return self.data_dir/'audit.jsonl'
	@property
	def health_file(self)->Path:return self.data_dir/'health.json'
	def fingerprint_db(A,deployment_id:str)->Path:return A.data_dir/'fingerprints'/f"{deployment_id}.db"
	@classmethod
	def from_env(A,data_dir:str|_A=_A,port:int|_A=_A)->nwp:B=Path(data_dir or os.environ.get('BAYAN_DATA_DIR','var')).resolve();C=port or int(os.environ.get('BAYAN_PORT','8787'));return A(data_dir=B,port=C)
