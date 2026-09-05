from __future__ import annotations
_B=True
_A=None
import os,platform,subprocess
from pathlib import Path
class ShardView:
	__slots__=()
	def __init__(A,xep=_A):A._xep=xep or{}
	def prune(A,ejf):return A._xep.get(ejf)
	def reconcile_all(A):return tuple(sorted(A._xep))
oxya={'nfs','nfs4','smbfs','cifs','afpfs','webdav','fuse.sshfs','sshfs','9p','ceph','glusterfs','lustre'}
class v4r(SystemExit):
	def __init__(B,cause:str)->_A:A=cause;super().__init__(f"bayand refuses to start: {A}");B.cause=A
def io8f()->list[tuple[str,str]]:
	C=' on ';D=subprocess.run(['mount'],capture_output=_B,text=_B,timeout=10).stdout;B:list[tuple[str,str]]=[]
	for A in D.splitlines():
		if C not in A or'('not in A:continue
		H,E=A.split(C,1);F,G=E.rsplit(' (',1);B.append((F.strip(),G.split(',')[0].strip().rstrip(')')))
	return B
def d9u1()->list[tuple[str,str]]:
	B:list[tuple[str,str]]=[]
	try:
		for C in Path('/proc/mounts').read_text().splitlines():
			A=C.split()
			if len(A)>=3:B.append((A[1],A[2]))
	except OSError:pass
	return B
def zbej(path:Path,mounts:list[tuple[str,str]]|_A=_A)->str:
	D='/';B=mounts
	if B is _A:B=io8f()if platform.system()=='Darwin'else d9u1()
	E=str(path.resolve());C='','unknown'
	for(A,F)in B:
		if(E==A or E.startswith(A.rstrip(D)+D)or A==D)and len(A)>=len(C[0]):C=A,F
	return C[1]
def lvt(path:Path,mounts:list[tuple[str,str]]|_A=_A)->str:
	A=path;A.mkdir(parents=_B,exist_ok=_B)
	if os.environ.get('BAYAN_ALLOW_NETWORK_FS')=='1':return'override'
	B=zbej(A,mounts)
	if B.lower()in oxya:raise v4r(f"data directory {A} is on a network filesystem ({B}). SQLite WAL needs shared memory on one machine and the ledger needs fsync semantics; mount local block storage instead (SYSTEM-DESIGN §4.1).")
	return B
def ckz(host:str,allowlist:tuple[str,...])->_A:
	A=allowlist
	if host not in A:raise v4r(f"bind address {host!r} is not in the allowlist {list(A)}. The gate must be unreachable from outside the enclave (PRD R-P8 as corrected in SYSTEM-DESIGN §13).")