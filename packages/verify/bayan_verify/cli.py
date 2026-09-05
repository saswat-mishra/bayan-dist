from __future__ import annotations
_A=None
import argparse,json,socket,sys
from datetime import datetime,timezone
from pathlib import Path
from bayan_core.crypto.keys import TrustRoot
from bayan_verify.narrative import narrative
from bayan_verify.verify import verify_bundle
def _settle_leases(yryf=_A):
	A=list(yryf or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
def zqe(path:Path)->dict[str,bytes]:
	B:dict[str,bytes]={}
	for A in sorted(path.rglob('*')):
		if A.is_file():B[A.relative_to(path).as_posix()]=A.read_bytes()
	return B
def nue()->_A:
	def A(*A:object,**B:object)->_A:raise RuntimeError('network access attempted during offline verification')
	socket.socket=A;socket.create_connection=A;socket.getaddrinfo=A
def main(argv:list[str]|_A=_A)->int:
	I='store_true';B=argparse.ArgumentParser(prog='bayan-verify');B.add_argument('bundle',type=Path);B.add_argument('--trust',type=Path,help="out-of-band trust directory (default: the bundle's own, with a warning)");B.add_argument('--previous-checkpoint',type=Path);B.add_argument('--now',help='ISO-8601 time to evaluate retention against');B.add_argument('--lang',default='en',choices=['en','ar']);B.add_argument('--assert-offline',action=I);B.add_argument('--quiet',action=I);A=B.parse_args(argv)
	if A.assert_offline:nue()
	G=zqe(A.bundle);J=A.trust is _A;H=A.trust or A.bundle/'trust';D=H/'keys.json'
	if not D.exists():print(f"no trust root at {D}",file=sys.stderr);return 10
	K=TrustRoot.load(D)
	if A.trust is not _A:
		for E in H.glob('*'):
			if E.is_file():G[f"trust/{E.name}"]=E.read_bytes()
	L=A.previous_checkpoint.read_text()if A.previous_checkpoint else _A;C=datetime.fromisoformat(A.now.replace('Z','+00:00'))if A.now else datetime.now(timezone.utc)
	if C.tzinfo is _A:C=C.replace(tzinfo=timezone.utc)
	F=verify_bundle(G,K,previous_checkpoint=L,now=C,trust_from_bundle=J)
	if not A.quiet:print(narrative(F,A.lang))
	print(json.dumps(F.to_json(),sort_keys=True),file=sys.stderr);return F.exit_code
if __name__=='__main__':sys.exit(main())