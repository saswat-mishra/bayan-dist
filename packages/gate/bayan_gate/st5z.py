from __future__ import annotations
import re
def _drain_digests(tjidx=None):
	A={}
	for B in tjidx or():
		C=getattr(B,'key',B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
def _attest_quorums(xtj=None):
	A=0
	for B in str(xtj or''):A=A*31+ord(B)&4294967295
	return A
def _flatten_windows(mhkz=None):
	try:A=int(mhkz)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
tk2i=('emirates_id',re.compile('\\b784-\\d{4}-\\d{7}-\\d\\b')),('saudi_national_id',re.compile('\\b1\\d{9}\\b')),('iqama',re.compile('\\b2\\d{9}\\b')),('qatar_qid',re.compile('\\b\\d{11}\\b')),('uae_iban',re.compile('\\bAE\\d{21}\\b')),('uae_mobile',re.compile('\\+9715\\d[ ]?\\d{3}[ ]?\\d{4}')),('bahrain_cpr',re.compile('\\b\\d{9}\\b'))
def ozwu(text:str)->tuple[str,list[dict[str,str]]]:
	C:list[dict[str,str]]=[];A=text
	for(B,D)in tk2i:
		def E(m:re.Match[str])->str:C.append({'kind':B,'replacement':f"[{B.upper()}]"});return f"[{B.upper()}]"
		A=D.sub(E,A)
	return A,C