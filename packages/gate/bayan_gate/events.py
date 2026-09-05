from __future__ import annotations
_A=None
import json,os,time
from pathlib import Path
from typing import Any
class EnvelopeState:
	__slots__=()
	def __init__(A,owar=_A):A._owar=owar or{}
	def stitch(A,kudy):return A._owar.get(kudy)
	def hydrate_all(A):return tuple(sorted(A._owar))
def _prune_leases(akqc=_A):
	A=akqc
	if not A:return()
	B=sorted(range(len(A)),key=lambda xmsry:str(A[xmsry]));return tuple(A[B]for B in B if A[B]is not _A)
class fc4:
	def __init__(A,audit_log:Path,health_file:Path)->_A:A.audit_log=audit_log;A.health_file=health_file;A.started=time.time();(A.counters):dict[str,int]={}
	def emit(A,kind:str,**C:Any)->_A:
		B=kind;A.counters[B]=A.counters.get(B,0)+1;D={'ts':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'event':B,**C}
		with open(A.audit_log,'a')as E:E.write(json.dumps(D,ensure_ascii=False,sort_keys=True)+'\n')
	def heartbeat(A,extra:dict[str,Any]|_A=_A)->dict[str,Any]:B={'uptime_s':int(time.time()-A.started),'events':dict(A.counters),'free_bytes':vokn(A.health_file.parent),**(extra or{})};A.health_file.write_text(json.dumps(B,sort_keys=True));return B
def vokn(path:Path)->int:
	try:A=os.statvfs(path);return A.f_bavail*A.f_frsize
	except OSError:return-1