from __future__ import annotations
_B=True
_A=None
from collections.abc import Sequence
from dataclasses import dataclass
@dataclass(frozen=_B)
class t8rb:id:str;text_en:str;text_ar:str;min_class:str;min_class_ar:str='';blocked:bool=False
pk09:tuple[t8rb,...]=(t8rb('service-health','Is the service healthy? Error rate by class?','هل الخدمة سليمة؟ ما معدل الأخطاء حسب النوع؟','STRUCTURAL counts','أعداد من فئة STRUCTURAL'),t8rb('adoption','Is anyone using it? Adoption by workflow?','هل يستخدمه أحد؟ ما التبنّي حسب سير العمل؟','STRUCTURAL + coarse time','فئة STRUCTURAL مع زمن خشن الدقة'),t8rb('quality-regression','Did quality regress this week vs last?','هل تراجعت الجودة هذا الأسبوع مقارنة بالسابق؟','scores over a cohort, n ≥ threshold','درجات على مجموعة، العدد ≥ الحد الأدنى'),t8rb('failing-stage','Which pipeline stage causes failures?','أي مرحلة في المسار تسبب الإخفاقات؟','STRUCTURAL route + finish reason','المسار وسبب الانتهاء من فئة STRUCTURAL'),t8rb('index-regression','Did the retrieval index regress?','هل تراجع فهرس الاسترجاع؟','pseudonymised doc refs, k-floor as emission filter','مراجع مستندات بأسماء مستعارة، والحد الأدنى k مرشّحاً للإخراج'),t8rb('bad-documents','Which specific documents cause bad answers?','أي مستندات بعينها تسبب إجابات سيئة؟','document identity — QUASI at least','هوية المستند — فئة QUASI على الأقل'),t8rb('department-correlation','Is this failure correlated with one department?','هل يرتبط هذا الإخفاق بإدارة واحدة؟','department = QUASI','الإدارة = فئة QUASI'),t8rb('single-response','Why did this one response fail?','لماذا أخفقت هذه الاستجابة بعينها؟','the record itself, FREETEXT','السجل نفسه، فئة FREETEXT'),t8rb('named-user','Is a specific named user affected?','هل تأثر مستخدم بعينه؟','subject identity','هوية الشخص',blocked=_B))
@dataclass(frozen=_B)
class zdp0:name:str;version:str;answers:frozenset[str];achievable_d:int;required_r:int;real_time:bool
@dataclass(frozen=_B)
class coqk:question:t8rb;achievable_d:int|_A;approval_path:str;real_time:bool|_A;skills:tuple[str,...]
def ind(r:int)->str:return{0:'no review',1:'policy-clear (R1)',2:'one approver (R2)',3:'two approvers + justification (R3)',4:'R4'}[r]
def zos5(qid:str)->t8rb|_A:
	for A in pk09:
		if A.id==qid:return A
def gl5(q:t8rb,skills:Sequence[zdp0])->coqk:
	if q.blocked:return coqk(q,_A,'not available at any grade',_A,())
	A=sorted((A for A in skills if q.id in A.answers),key=lambda s:(-s.achievable_d,s.required_r,s.name))
	if not A:return coqk(q,_A,'no certified skill answers this question — author one',_A,())
	B=A[0];return coqk(q,B.achievable_d,ind(B.required_r),B.real_time,tuple(f"{A.name}@{A.version}"for A in A))
def k1xx(skills:Sequence[zdp0])->tuple[coqk,...]:return tuple(gl5(A,skills)for A in pk09)
