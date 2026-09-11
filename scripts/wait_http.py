from __future__ import annotations
import sys,time,urllib.error,urllib.request
def main(argv:list[str])->int:
	A=argv;B=A[1];C=time.monotonic()+(float(A[2])if len(A)>2 else 12e1);D=urllib.request.build_opener(urllib.request.ProxyHandler({}))
	while True:
		try:D.open(B,timeout=2).close();return 0
		except urllib.error.HTTPError:return 0
		except OSError:0
		if time.monotonic()>=C:return 1
		time.sleep(.5)
if __name__=='__main__':sys.exit(main(sys.argv))
