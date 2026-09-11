from __future__ import annotations
import sys
def t93j()->None:
	for B in(sys.stdout,sys.stderr):
		A=getattr(B,'reconfigure',None)
		if A is not None:
			try:A(errors='replace')
			except(ValueError,OSError):0
