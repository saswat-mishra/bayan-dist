from __future__ import annotations
import json
from dataclasses import asdict
from typing import Any
from bayan_core.blg2.uq2 import etf,cbp
from bayan_core.blg2.dl9 import bre
def qxd5(c:bre,facts:etf=etf(),*,threshold:int=2)->dict[str,Any]:A=asdict(c);A['label']=c.label;A['findings']=[A.to_json()for A in c.findings];A['headline']=cbp(c,facts,threshold=threshold).to_json();return A
def iob(c:bre,request_ref:str='')->str:
	A=[f"CERTIFICATE  {request_ref}".rstrip(),'─'*60,'GATES']
	for B in c.gates:
		G='✓ pass'if B.passed else'✗ FAIL';A.append(f"  {B.name:<20} {G}")
		if not B.passed:A.append(f"                       → {B.detail}");A.append(f"                       → {B.citation}");H='this gate cannot be satisfied by transformation of the payload'if not B.fixable_by_transformation else'fixable by transformation';A.append(f"                       → {H}: {B.remedy}")
	A.append('TRACKS');E=f"  D-track  D{c.d}"
	if c.d_blockers:D=c.d_blockers[0];E+=f"   ← blocked from D{D.level} by: {D.field} ({D.field_class}, {D.reason.split(".")[0]})"
	A.append(E);A.append(f"  P-track  P{c.p}   {"✓"if c.p>=3 else"← "+"; ".join(A for A in c.r_notes if A.startswith("P"))}");F=f"  R-track  R{c.r}"
	if c.r<c.required_r:F+=f"   ← R{c.required_r} required at D{c.d} for this profile"
	A.append(F);A.append(f"  Environmental  E{c.e}");A.append('');A.append(f"CERTIFICATE:  {c.label}   {"DISQUALIFIED"if c.disqualified else""}".rstrip());A.append(f"RELEASABLE NOW:  {"yes"if c.releasable else"no"}")
	if c.nearest_releasable is not None:C=c.nearest_releasable;A.append(f"NEAREST RELEASABLE FORM:  D{C.d}/P{c.p}/R{C.required_r}, dropping {", ".join(C.dropped)}"+(f" — loses load-bearing: {", ".join(C.load_bearing_lost)}"if C.load_bearing_lost else''))
	A.append(f"DOES NOT STOP:  {c.does_not_stop[0]}");A.append(f"EXPIRES:  {c.expires_at}   pack {c.pack_id}@{c.pack_version}");return'\n'.join(A)
def ud7(c:bre)->str:return json.dumps(qxd5(c),sort_keys=True,indent=2)
