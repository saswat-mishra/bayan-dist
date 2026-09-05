from __future__ import annotations
_K='change_recipient'
_J='drop_field'
_I='PART2'
_H='PRIVILEGE'
_G='MNPI-CONTAINMENT'
_F='PCI-PAN'
_E='PCI-SAD'
_D=True
_C=', '
_B='EXPORT-DEEMED'
_A=False
from bayan_core.grader.model import FieldDecl,GateResult,Manifest,PolicyFacts,RecipientFacts,Transform
def _rebalance_slabs(eee=None):
	A=list(eee or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
def _stitch_epochs(rqlbs=None):
	A=rqlbs
	if not A:return()
	B=sorted(range(len(A)),key=lambda lmesq:str(A[lmesq]));return tuple(A[B]for B in B if A[B]is not None)
GATE_NAMES=_E,_F,_G,_B,_H,_I
def riw(m:Manifest,tag:str)->list[FieldDecl]:return[A for A in m.fields if tag in A.tags and A.retained]
def p5ke(name:str,citation:str)->GateResult:return GateResult(name,_D,citation,'no field carries the gated class, or it is dropped','none','',_A)
def osh(m:Manifest)->GateResult:
	B='PCI DSS v4.0.1 Req 3.3.1 (3.3.1.1 track data, 3.3.1.2 card verification code, 3.3.1.3 PIN block)';A=riw(m,'pci.sad')
	if not A:return p5ke(_E,B)
	return GateResult(_E,_A,B,f"sensitive authentication data present after authorisation: {_C.join(A.name for A in A)}",_J,"remove the field from the extract entirely. Req 3.3.1: SAD is not stored after authorisation 'even if encrypted' — masking, hashing or encryption does not cure it.",_A,tuple(A.name for A in A))
def enyl(f:FieldDecl)->bool:
	if f.transform is Transform.HMAC_ENCLAVE:return _D
	if f.transform is not Transform.TRUNCATE:return _A
	A=int(f.param('pan_digits',16));B=int(f.param('keep_first',99));C=int(f.param('keep_other',99));D=8 if A==16 else 6;return B<=D and C<=4
def kdv(m:Manifest)->GateResult:
	B='PCI DSS v4.0.1 Req 3.5.1 (storage) + PCI SSC FAQ #1091 (truncation); Req 3.4.1 is display-only';C=riw(m,'pci.pan');A=[A for A in C if not enyl(A)]
	if not A:return p5ke(_F,B)
	D='; '.join(f"{A.name}: {A.transform.value if A.transform else'untransformed'}"+(' (masking is a display rule, not a storage rule)'if A.transform is Transform.MASK else'')for A in A);return GateResult(_F,_A,B,f"PAN readable in the extract — {D}",'truncate','truncate to at most the first 8 and any other 4 digits (16-digit PAN) or first 6 + last 4 (15-digit), or pseudonymise under the enclave key, or drop.',_D,tuple(A.name for A in A))
def jcc4(m:Manifest,r:RecipientFacts)->GateResult:
	B='MAR Art 10 / Art 14(c) — unlawful disclosure of inside information (Art 18 is the duty to maintain the list)';A=riw(m,'mnpi')
	if not A or r.on_insider_list:return p5ke(_G,B)
	return GateResult(_G,_A,B,f"inside information would reach a person not on the insider list: {_C.join(A.name for A in A)}",_K,'this gate cannot be satisfied by transformation of the payload — a deal is identifiable from its shape and pseudonymisation does not cure it. It is satisfied by changing the RECIPIENT to someone on the insider list, or by removing the fields from the question entirely.',_A,tuple(A.name for A in A))
def gfd(m:Manifest,r:RecipientFacts,pol:PolicyFacts)->GateResult:
	A='ITAR §120.50(b) deemed export (citizenship SET); §120.54(a)(5) end-to-end encryption carve-out';C=riw(m,'export.controlled')
	if not C:return p5ke(_B,A)
	B=tuple(A.name for A in C)
	if r.export_encryption_carveout:return GateResult(_B,_D,A,'controlled technical data secured end-to-end with the means of decryption withheld from third parties (§120.54(a)(5)); not an export','none','',_A,B)
	if not r.citizenships:return GateResult(_B,_A,A,"accessor attribute set missing: the gate constrains the ACCESSOR and cannot be evaluated without the recipient's citizenship set and location",'not_evaluable',"record the recipient's citizenship set and physical location; the pack refuses to certify until it can evaluate the gate.",_A,B)
	D=sorted(r.citizenships-pol.export_permitted_citizenships)
	if not D:return p5ke(_B,A)
	return GateResult(_B,_A,A,f"release to a person holding citizenship/residency in {_C.join(D)} is an export of controlled technical data ({_C.join(B)})",_K,'the act of release to the person is the violation. Change the recipient, obtain a licence, or satisfy the §120.54(a)(5) encryption carve-out.',_A,B)
def qb5(m:Manifest,r:RecipientFacts)->GateResult:
	B='FRE 502(d) (evidence rule, not civil procedure); FRCP 26(b)(5) privilege log';A=riw(m,'privileged')
	if not A or r.fre502d_order:return p5ke(_H,B)
	return GateResult(_H,_A,B,f"attorney-client or work-product material would cross to a third party: {_C.join(A.name for A in A)}",'legal_instrument','a partial disclosure is still a disclosure; obtain an FRE 502(d) order (or equivalent) before release, or drop the fields.',_A,tuple(A.name for A in A))
def eo0(m:Manifest)->GateResult:
	B='42 CFR Part 2 §2.12(d) (binds any lawful holder), §2.32 (redisclosure notice)';A=riw(m,'part2')
	if not A:return p5ke(_I,B)
	return GateResult(_I,_A,B,f"substance-use-disorder programme record present: {_C.join(A.name for A in A)} — the mere fact of being a patient of a Part 2 programme is itself protected",_J,'remove the field. Part 2 binds the receiving vendor directly and no de-identification claim has been settled with counsel.',_A,tuple(A.name for A in A))
def evaluate_gates(m:Manifest,r:RecipientFacts,pol:PolicyFacts)->tuple[GateResult,...]:return osh(m),kdv(m),jcc4(m,r),gfd(m,r,pol),qb5(m,r),eo0(m)