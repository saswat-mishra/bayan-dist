from __future__ import annotations
_A=None
import argparse
from bayan_gate.fq5x import x3w2
from bayan_gate.xc45 import nwp
from bayan_gate.i7m5 import b8d
from bayan_gate.s4m7 import ckz
def main(argv:list[str]|_A=_A)->int:A=argparse.ArgumentParser(prog='bayand');A.add_argument('--data-dir',default=_A);A.add_argument('--port',type=int,default=_A);A.add_argument('--host',default='127.0.0.1');B=A.parse_args(argv);C=nwp.from_env(B.data_dir,B.port);ckz(B.host,C.bind_allowlist);D=b8d(C);import uvicorn as E;E.run(x3w2(D),host=B.host,port=C.port,log_level='warning');return 0
if __name__=='__main__':raise SystemExit(main())
