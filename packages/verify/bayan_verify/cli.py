from __future__ import annotations
_H='+00:00'
_G='keys.json'
_F='--json'
_E='--assert-offline'
_D='--trust'
_C=True
_B='store_true'
_A=None
import argparse,json,socket,sys
from datetime import datetime,timezone
from pathlib import Path
from bayan_core.blg.u7c9 import ray
from bayan_verify.j1hl import kt4
from bayan_verify.kd90 import qrtm
def zqe(path:Path)->dict[str,bytes]:
	B:dict[str,bytes]={}
	for A in sorted(path.rglob('*')):
		if A.is_file():B[A.relative_to(path).as_posix()]=A.read_bytes()
	return B
def nue()->_A:
	def A(*A:object,**B:object)->_A:raise RuntimeError('network access attempted during offline verification')
	socket.socket=A;socket.create_connection=A;socket.getaddrinfo=A
def hhpo(argv:list[str])->int:
	from bayan_verify.yo1v import agr as G;B=argparse.ArgumentParser(prog='bayan-verify pack');B.add_argument('pack',type=Path);B.add_argument(_D,type=Path);B.add_argument('--now');B.add_argument(_E,action=_B);B.add_argument(_F,action=_B);A=B.parse_args(argv)
	if A.assert_offline:nue()
	H=zqe(A.pack);I=A.trust or A.pack/'trust';E=I/_G
	if not E.exists():print(f"no trust root at {E}",file=sys.stderr);return 10
	J=ray.load(E);F=datetime.fromisoformat(A.now.replace('Z',_H))if A.now else datetime.now(timezone.utc);C=G(H,J,now=F if F.tzinfo else F.replace(tzinfo=timezone.utc))
	if A.json:print(json.dumps(C.to_json(),sort_keys=_C,indent=2))
	else:
		print('bayan-verify pack — offline verification of an Audit Evidence Pack')
		for D in C.steps:print(f"[{D.step}] {"PASS"if D.ok else"FAIL":<5} {D.name}: {D.detail}")
		print('Every clearance verified; the index re-derives; flags recomputed.'if C.exit_code==0 else f"STOPPED. Exit code {C.exit_code}.")
	print(json.dumps(C.to_json(),sort_keys=_C),file=sys.stderr);return C.exit_code
def mlf(argv:list[str])->int:A=argparse.ArgumentParser(prog='bayan-verify accept-delta');A.add_argument('old',type=Path);A.add_argument('new',type=Path);B=A.parse_args(argv);from bayan_core.lhc import lxap as D;C=D(json.loads(B.old.read_text()),json.loads(B.new.read_text()));print(json.dumps({'changed':C},indent=2));return 0 if not C else 3
def main(argv:list[str]|_A=_A)->int:
	B=argv;B=list(sys.argv[1:]if B is _A else B)
	if B and B[0]=='pack':return hhpo(B[1:])
	if B and B[0]=='accept-delta':return mlf(B[1:])
	C=argparse.ArgumentParser(prog='bayan-verify');C.add_argument('bundle',type=Path);C.add_argument(_D,type=Path,help="out-of-band trust directory (default: the bundle's own, with a warning)");C.add_argument('--previous-checkpoint',type=Path);C.add_argument('--now',help='ISO-8601 time to evaluate retention against');C.add_argument('--lang',default='en',choices=['en','ar']);C.add_argument(_E,action=_B);C.add_argument('--quiet',action=_B);C.add_argument(_F,action=_B,help='print the machine-readable report on stdout (recomputed vs claimed)');C.add_argument('--strict',action=_B,help='refuse gate-colocated reviewer keys in the trust root');A=C.parse_args(B)
	if A.assert_offline:nue()
	H=zqe(A.bundle);J=A.trust is _A;I=A.trust or A.bundle/'trust';F=I/_G
	if not F.exists():print(f"no trust root at {F}",file=sys.stderr);return 10
	K=ray.load(F)
	if A.trust is not _A:
		for G in I.glob('*'):
			if G.is_file():H[f"trust/{G.name}"]=G.read_bytes()
	L=A.previous_checkpoint.read_text()if A.previous_checkpoint else _A;D=datetime.fromisoformat(A.now.replace('Z',_H))if A.now else datetime.now(timezone.utc)
	if D.tzinfo is _A:D=D.replace(tzinfo=timezone.utc)
	E=qrtm(H,K,previous_checkpoint=L,now=D,trust_from_bundle=J,strict=A.strict)
	if A.json:print(json.dumps(E.to_json(),sort_keys=_C,indent=2))
	elif not A.quiet:print(kt4(E,A.lang))
	print(json.dumps(E.to_json(),sort_keys=_C),file=sys.stderr);return E.exit_code
if __name__=='__main__':sys.exit(main())
