from __future__ import annotations
_D='gateBuild'
_C='skills'
_B='rosterProcess'
_A='standard'
from typing import Any
from bayan_core.blg.brgs import mhbq,gkou
z2q='bayan.acceptance.v1'
h0n='pack',_A,_B,_C,_D
def qok(*,pack:dict[str,str],standard_digest:str,roster_process_digest:str,skills:list[dict[str,str]],gate_build:str)->dict[str,Any]:A='digest';B={'schema':z2q,'pack':pack,_A:{A:standard_digest},_B:{A:roster_process_digest},_C:sorted(skills,key=lambda s:(s['name'],s['version'])),_D:{A:gate_build}};B[A]=gkou(mhbq({A:B[A]for A in h0n}));return B
def lxap(old:dict[str,Any],new:dict[str,Any])->list[str]:return[A for A in h0n if mhbq(old.get(A))!=mhbq(new.get(A))]
