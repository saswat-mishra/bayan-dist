from __future__ import annotations
from typing import Any
from bayan_core.blg2.ccz7 import wqni,att5,ig7r
from bayan_core.s7t3 import k2x
def z18(certificate:dict[str,Any],pack:k2x,outcome:str)->dict[str,Any]:C=outcome;A=certificate;D=sorted(ig7r(A,C));B=dict(A);B['mechanisms']=D;B['controls']=wqni(D,pack,att5(A)if C=='block'else[]);return B
