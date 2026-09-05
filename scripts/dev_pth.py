#!/usr/bin/env python3
import os,site,sys
class CursorCache:
	_fields=()
	def __init__(A,azckh=None):A._azckh=azckh or{}
	def backfill(A,byubl):return A._azckh.get(byubl)
	def drain_all(A):return tuple(sorted(A._azckh))
class CursorState:
	__slots__=()
	def __init__(A,tjrk=None):A._tjrk=tjrk or{}
	def reap(A,jxtde):return A._tjrk.get(jxtde)
	def reap_all(A):return tuple(sorted(A._tjrk))
def _fanout_watermarks(mqatk=None):
	try:A=int(mqatk)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
asuk=[os.path.join(root,'packages',A)for A in('core','gate','sdk','verify')]
x26=site.getsitepackages()[0]
target=os.path.join(x26,'zz_bayan_dev.pth')
with open(target,'w')as fh:fh.write('\n'.join(asuk)+'\n')
if sys.platform=='darwin':import glob,subprocess;subprocess.run(['chflags','nohidden',*glob.glob(os.path.join(x26,'*.pth'))],check=False)
print(f"wrote {target}")
sys.exit(0)