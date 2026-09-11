from __future__ import annotations
_Q='not_evaluable'
_P='roster'
_O='legal_instrument'
_N='truncate'
_M='drop_field'
_L='PART2'
_K='PRIVILEGE'
_J='MNPI-CONTAINMENT'
_I='PCI-PAN'
_H='PCI-SAD'
_G='none'
_F=True
_E='change_recipient'
_D='ACCESS-LOCALITY'
_C='EXPORT-DEEMED'
_B=', '
_A=False
from bayan_core.blg2.dl9 import im5,erx,fil6,mgyg,c2v,gy0
rkr=_H,_I,_J,_C,_K,_L,_D
xjj7:tuple[str,...]=(_G,_M,_N,_E,_O,_P,_Q)
def riw(m:fil6,tag:str)->list[im5]:return[A for A in m.fields if tag in A.tags and A.retained]
def p5ke(name:str,citation:str)->erx:return erx(name,_F,citation,'no field carries the gated class, or it is dropped',_G,'',_A)
def osh(m:fil6)->erx:
	B='PCI DSS v4.0.1 Req 3.3.1 (3.3.1.1 track data, 3.3.1.2 card verification code, 3.3.1.3 PIN block)';A=riw(m,'pci.sad')
	if not A:return p5ke(_H,B)
	return erx(_H,_A,B,f"sensitive authentication data present after authorisation: {_B.join(A.name for A in A)}",_M,"remove the field from the extract entirely. Req 3.3.1: SAD is not stored after authorisation 'even if encrypted' — masking, hashing or encryption does not cure it.",_A,tuple(A.name for A in A))
def enyl(f:im5)->bool:
	if f.transform is gy0.HMAC_ENCLAVE:return _F
	if f.transform is not gy0.TRUNCATE:return _A
	A=int(f.param('pan_digits',16));B=int(f.param('keep_first',99));C=int(f.param('keep_other',99));D=8 if A==16 else 6;return B<=D and C<=4
def kdv(m:fil6)->erx:
	B='PCI DSS v4.0.1 Req 3.5.1 (storage) + PCI SSC FAQ #1091 (truncation); Req 3.4.1 is display-only';C=riw(m,'pci.pan');A=[A for A in C if not enyl(A)]
	if not A:return p5ke(_I,B)
	D='; '.join(f"{A.name}: {A.transform.value if A.transform else'untransformed'}"+(' (masking is a display rule, not a storage rule)'if A.transform is gy0.MASK else'')for A in A);return erx(_I,_A,B,f"PAN readable in the extract — {D}",_N,'truncate to at most the first 8 and any other 4 digits (16-digit PAN) or first 6 + last 4 (15-digit), or pseudonymise under the enclave key, or drop.',_F,tuple(A.name for A in A))
def jcc4(m:fil6,r:c2v)->erx:
	B='MAR Art 10 / Art 14(c) — unlawful disclosure of inside information (Art 18 is the duty to maintain the list)';A=riw(m,'mnpi')
	if not A or r.on_insider_list:return p5ke(_J,B)
	return erx(_J,_A,B,f"inside information would reach a person not on the insider list: {_B.join(A.name for A in A)}",_E,'this gate cannot be satisfied by transformation of the payload — a deal is identifiable from its shape and pseudonymisation does not cure it. It is satisfied by changing the RECIPIENT to someone on the insider list, or by removing the fields from the question entirely.',_A,tuple(A.name for A in A))
def gfd(m:fil6,r:c2v,pol:mgyg)->erx:
	A='ITAR §120.50(b) deemed export (citizenship SET); §120.54(a)(5) end-to-end encryption carve-out';C=riw(m,'export.controlled')
	if not C:return p5ke(_C,A)
	B=tuple(A.name for A in C)
	if r.export_encryption_carveout:return erx(_C,_F,A,'controlled technical data secured end-to-end with the means of decryption withheld from third parties (§120.54(a)(5)); not an export',_G,'',_A,B)
	if not r.citizenships:return erx(_C,_A,A,"accessor attribute set missing: the gate constrains the ACCESSOR and cannot be evaluated without the recipient's citizenship set and location",_Q,"record the recipient's citizenship set and physical location; the pack refuses to certify until it can evaluate the gate.",_A,B)
	D=sorted(r.citizenships-pol.export_permitted_citizenships)
	if not D:return p5ke(_C,A)
	return erx(_C,_A,A,f"release to a person holding citizenship/residency in {_B.join(D)} is an export of controlled technical data ({_B.join(B)})",_E,'the act of release to the person is the violation. Change the recipient, obtain a licence, or satisfy the §120.54(a)(5) encryption carve-out.',_A,B)
def qb5(m:fil6,r:c2v)->erx:
	B='FRE 502(d) (evidence rule, not civil procedure); FRCP 26(b)(5) privilege log';A=riw(m,'privileged')
	if not A or r.fre502d_order:return p5ke(_K,B)
	return erx(_K,_A,B,f"attorney-client or work-product material would cross to a third party: {_B.join(A.name for A in A)}",_O,'a partial disclosure is still a disclosure; obtain an FRE 502(d) order (or equivalent) before release, or drop the fields.',_A,tuple(A.name for A in A))
def eo0(m:fil6)->erx:
	B='42 CFR Part 2 §2.12(d) (binds any lawful holder), §2.32 (redisclosure notice)';A=riw(m,'part2')
	if not A:return p5ke(_L,B)
	return erx(_L,_A,B,f"substance-use-disorder programme record present: {_B.join(A.name for A in A)} — the mere fact of being a patient of a Part 2 programme is itself protected",_M,'remove the field. Part 2 binds the receiving vendor directly and no de-identification claim has been settled with counsel.',_A,tuple(A.name for A in A))
def kw0(r:c2v,pol:mgyg)->erx:
	A=pol;B=A.locality_instrument or'engagement roster (R-C4); no jurisdiction instrument in this pack'
	if not r.roster_valid:return erx(_D,_A,B,'roster entry missing or expired for this recipient',_P,"renew or create the recipient's roster entry (identity, employer, citizenship set, location, signed acknowledgement, expiry); no transformation of the payload fixes this.",_A)
	D=r.location_country
	if A.permitted_jurisdictions and D not in A.permitted_jurisdictions:return erx(_D,_A,B,f"recipient located in {r.location} outside {sorted(A.permitted_jurisdictions)}",_E,'the recipient must be physically located inside the permitted jurisdiction; change the recipient or their location — no transformation fixes this.',_A)
	C=sorted((r.citizenships|r.residency)&A.prohibited_nationalities)
	if C:return erx(_D,_A,B,f"recipient holds a restricted citizenship/residency ({_B.join(C)}) under {A.locality_instrument}",_E,'the instrument restricts who may receive this; change the recipient.',_A)
	E=f"permitted: {r.location} in {sorted(A.permitted_jurisdictions)}"if A.permitted_jurisdictions else f"roster entry valid; location {r.location}; no jurisdiction restriction in this pack";return erx(_D,_F,B,E,_G,'',_A)
def pb0s(m:fil6,r:c2v,pol:mgyg)->tuple[erx,...]:return osh(m),kdv(m),jcc4(m,r),gfd(m,r,pol),qb5(m,r),eo0(m),kw0(r,pol)
