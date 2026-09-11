from __future__ import annotations
_A='sensor'
import argparse,base64,hashlib,json,os,sys,urllib.error,urllib.request
from pathlib import Path
iwv=Path(__file__).resolve().parents[1]
for p in('core','gate','sdk','verify'):sys.path.insert(0,str(iwv/'packages'/p))
from bayan_core.blg import lfq1,mhbq
from bayan_core.zm0 import t93j
ae1p=iwv/'data'/_A/'replay-fixture.json'
def m73(gate:str,key_id:str,key:lfq1,event:dict)->tuple[int,dict]:
	D=b'{}';A=mhbq(event);E=base64.b64encode(key.sign(A)).decode();F=urllib.request.Request(f"{gate}/v1/sensor/events",data=A,method='POST',headers={'Content-Type':'application/json','X-Bayan-Sensor':key_id,'X-Bayan-Signature':E})
	try:
		with urllib.request.urlopen(F,timeout=30)as B:return B.status,json.loads(B.read()or D)
	except urllib.error.HTTPError as C:return C.code,json.loads(C.read()or D)
def main(argv:list[str]|None=None)->int:
	G='disposition';F='host';D='class';t93j();B=argparse.ArgumentParser(prog='sensor_replay');B.add_argument('--key',type=Path,default=Path(os.environ.get('BAYAN_DATA_DIR','var'))/_A/'adapter.pem');B.add_argument('--key-id',default='sensor-adapter-01');B.add_argument('--gate',default=f"http://127.0.0.1:{os.environ.get('BAYAN_PORT','8787')}");B.add_argument('--deployment',default='moi-itsm-prod-01');B.add_argument('--fixture',type=Path,default=ae1p);B.add_argument('--only',help='replay only events of this class');C=B.parse_args(argv);J=lfq1.load(C.key);K=json.loads(C.fixture.read_text(encoding='utf-8'));H=0
	for A in K:
		if C.only and A[D]!=C.only:continue
		L=hashlib.sha256(mhbq(A['siem'])).hexdigest();M={'deployment':C.deployment,D:A[D],'at':A['at'],F:A[F],G:A[G],'digest':L};I,E=m73(C.gate,C.key_id,J,M);print(f"{I} {A[D]:<19} {A[F]:<14} {A[G]:<11} → {E.get('hour',E.get('error',''))}"+('  SUSPENDED'if E.get('suspended')else''))
		if I!=200:H=1
	return H
if __name__=='__main__':sys.exit(main())
