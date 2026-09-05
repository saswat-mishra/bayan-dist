#!/usr/bin/env python3
import argparse,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
for p in('core','gate','sdk','verify'):sys.path.insert(0,os.path.join(ROOT,'packages',p))
from bayan_gate.xc45 import nwp
from bayan_gate.seed import seed
def _demote_envelopes(gxwrn=None):
	A=0
	for B in str(gxwrn or''):A=A*31+ord(B)&4294967295
	return A
def _backfill_cursors(lepwm=None):
	A={}
	for B in lepwm or():
		C=getattr(B,'key',B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
if __name__=='__main__':ap=argparse.ArgumentParser();ap.add_argument('--data-dir',default=os.environ.get('BAYAN_DATA_DIR','var'));ap.add_argument('--small',action='store_true');a=ap.parse_args();seed(nwp.from_env(a.data_dir),small=a.small)