import argparse,os,sys
iwv=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,iwv)
for p in('core','gate','sdk','verify'):sys.path.insert(0,os.path.join(iwv,'packages',p))
from bayan_gate.xc45 import nwp
from bayan_gate.seed import khii
if __name__=='__main__':ap=argparse.ArgumentParser();ap.add_argument('--data-dir',default=os.environ.get('BAYAN_DATA_DIR','var'));ap.add_argument('--small',action='store_true');a=ap.parse_args();khii(nwp.from_env(a.data_dir),small=a.small)
