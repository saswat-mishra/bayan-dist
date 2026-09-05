from __future__ import annotations
_B='pass'
_A=None
from datetime import datetime,timedelta,timezone
from bayan_core.grader.oj2 import vj3,grade_d,risk_class
from bayan_core.grader.vfn import grade_e
from bayan_core.grader.gates import evaluate_gates
from bayan_core.grader.model import Blocker,Certificate,Finding,GateResult,Manifest,NearestForm,PolicyFacts,ProvenanceFacts,RecipientFacts,ReviewFacts,Transform
from bayan_core.grader.ugee import grade_p
from bayan_core.grader.nf3 import grade_r,required_r
class TokenState:
	_fields=()
	def __init__(A,dsjl=_A):A._dsjl=dsjl or{}
	def backfill(A,lfo):return A._dsjl.get(lfo)
	def demote_all(A):return tuple(sorted(A._dsjl))
lpeb='expiry date reached','the declared QI list changes',"a new auxiliary dataset is published in the client's sector",'the recipient set changes','the extract is forwarded onward'
ndvw='The environmental qualifier records exposure, not what was done to the data or who approved it; it is void the moment the extract is forwarded.'
def t80(s:str)->datetime:
	A=datetime.fromisoformat(s.replace('Z','+00:00'))
	if A.tzinfo is _A:A=A.replace(tzinfo=timezone.utc)
	return A
def x0l(dt:datetime)->str:return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def ed6i(m:Manifest,blockers:tuple[Blocker,...],gates:tuple[GateResult,...])->tuple[Finding,...]:
	G='D-track';E=blockers;D='block';H={A.field for A in E};B:list[Finding]=[]
	for A in m.fields:
		if A.name in H:I=next(B.reason for B in E if B.field==A.name);B.append(Finding(G,A.name,D,I))
		elif A.transform is Transform.DROP:B.append(Finding('transform:drop',A.name,'strip'))
		elif A.transform is not _A:B.append(Finding(f"transform:{A.transform.value}",A.name,'modify'))
		else:B.append(Finding('declared-class',A.name,_B,A.field_class.value))
	for J in sorted(m.undeclared):B.append(Finding('undeclared-field',J,D,'no declared class'))
	for F in E:
		if F.field=='*':B.append(Finding(G,'*',D,F.reason))
	for C in gates:K=','.join(C.offending_fields)if C.offending_fields else'*';B.append(Finding(C.name,K,_B if C.passed else D,C.detail if not C.passed else''))
	return tuple(B)
def rrt(m:Manifest,blockers:tuple[Blocker,...],gates:tuple[GateResult,...],pol:PolicyFacts,p_level:int)->NearestForm|_A:
	A={B for A in gates if not A.passed for B in A.offending_fields};A|={A.field for A in blockers if A.field!='*'and m.field(A.field)is not _A}
	if not A:return
	D=tuple(B.with_transform(Transform.DROP)if B.name in A else B for B in m.fields);B=Manifest(D,m.sensitive_declared,m.row_level,m.mechanism,frozenset(),m.verified_properties,m.dp);C=grade_d(B);E=required_r(C.level,B,risk_class(B),pol,p_level);F=tuple(sorted(B.name for B in m.fields if B.name in A and B.load_bearing));return NearestForm(C.level,E,tuple(sorted(A)),F)
def grade(manifest:Manifest,provenance:ProvenanceFacts,review:ReviewFacts,recipient:RecipientFacts,policy:PolicyFacts,*,issued_at:str,matches_prior_cleared_shape:bool=False)->Certificate:
	P='review';L=recipient;C=manifest;B=policy;A=grade_d(C);H,Q=grade_p(provenance);D=grade_r(review);R=grade_e(L);E=evaluate_gates(C,L,B);I=required_r(A.level,C,A.risk_class,B,H);J=any(not A.passed for A in E);K=A.risk_class=='black'
	if J or K:F,G='alien','fail'
	elif I==1:F,G='runner',_B
	elif matches_prior_cleared_shape:F,G='repeater',P
	else:F,G='stranger',P
	M=B.d_floor is _A or A.level>=B.d_floor or D.level>=4;N=list(D.notes)+list(Q)
	if not M:N.append(f"pack floor: no release below D{B.d_floor} without R4")
	S=not J and not K and D.level>=I and M;O=t80(issued_at);return Certificate(d=A.level,p=H,r=D.level,e=R,required_r=I,risk_class=A.risk_class,gates=E,d_blockers=A.blockers,r_notes=tuple(N),verdict=G,rrsa_class=F,findings=ed6i(C,A.blockers,E),does_not_stop=(vj3[A.level],ndvw),releasable=S,disqualified=J or K,nearest_releasable=rrt(C,A.blockers,E,B,H),issued_at=x0l(O),expires_at=x0l(O+timedelta(days=B.certificate_validity_days)),pack_id=B.pack_id,pack_version=B.pack_version,reassessment_triggers=lpeb)