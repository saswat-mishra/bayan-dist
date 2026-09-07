import os,site,sys
kn1w=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
asuk=[os.path.join(kn1w,'packages',A)for A in('core','gate','sdk','verify')]
x26=site.getsitepackages()[0]
txr9=os.path.join(x26,'zz_bayan_dev.pth')
with open(txr9,'w')as fh:fh.write('\n'.join(asuk)+'\n')
if sys.platform=='darwin':import glob,subprocess;subprocess.run(['chflags','nohidden',*glob.glob(os.path.join(x26,'*.pth'))],check=False)
print(f"wrote {txr9}")
sys.exit(0)
