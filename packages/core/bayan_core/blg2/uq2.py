from __future__ import annotations
_I='quarantined'
_H='blocked-roster'
_G='blocked-recipient'
_F='needs-review'
_E=False
_D='blocked-budget'
_C='releases-now'
_B='blocked-fixable'
_A=None
from dataclasses import dataclass
from bayan_core.blg2.dl9 import bre,erx
i7nm=_C,_F,_B,_G,_H,_D,_I
wsfx=frozenset({'drop_field','truncate'})
hb9=frozenset({'change_recipient','legal_instrument'})
q58=frozenset({'roster','not_evaluable'})
@dataclass(frozen=True)
class etf:quarantined:bool=_E;budget_exhausted:bool=_E;suspended:bool=_E;reviewers_needed:int|_A=_A
@dataclass(frozen=True)
class fi7:
	kind:str;en:str;ar:str
	def to_json(A)->dict[str,str]:return{'kind':A.kind,'en':A.en,'ar':A.ar}
def das(c:bre)->erx|_A:
	for A in c.gates:
		if not A.passed:return A
def k0y(c:bre)->str:
	if c.d_blockers:A=c.d_blockers[0];return f"{A.field} is a {A.field_class.lower().replace("_"," ")} at D{c.d}"if A.field!='*'else A.reason.split(':')[0].lower()
	return f"grade D{c.d}"
def fd92(c:bre)->str:
	if c.d_blockers:A=c.d_blockers[0];return f"الحقل {A.field} من فئة {A.field_class} عند D{c.d}"if A.field!='*'else'المخرجات على مستوى السجل'
	return f"الدرجة D{c.d}"
def flfg(c:bre,facts:etf,threshold:int)->int:
	A=facts
	if A.reviewers_needed is not _A:return A.reviewers_needed
	return 1 if c.required_r==2 else threshold
def omly(c:bre)->str|_A:return next((A for A in c.r_notes if A.startswith('pack floor')),_A)
def cbp(c:bre,facts:etf=etf(),*,threshold:int=2)->fi7:
	D=facts
	if D.quarantined:return fi7(_I,"Quarantined — the output did not conform to the skill's declared schema. Nothing can be released from this run.",'محجور — المخرجات لم تطابق المخطط المعلن للمهارة. لا يمكن الإفراج عن أي شيء من هذا التشغيل.')
	if D.suspended:return fi7(_D,'Cannot release — the deployment is suspended after a sensor event. An officer with authority must clear it.','لا يمكن الإفراج — النشر موقوف بعد حدث من المستشعر. يجب أن يرفع الإيقاف مسؤول ذو صلاحية.')
	if D.budget_exhausted:return fi7(_D,'Cannot release — the period budget for this cohort is exhausted. Wait for the next period or ask the lead.','لا يمكن الإفراج — ميزانية الفترة لهذه المجموعة مستنفدة. انتظر الفترة التالية أو اسأل قائد التسليم.')
	A=das(c)
	if A is not _A:
		if A.remedy_kind in q58:return fi7(_H,f"Cannot release — {A.name}: {A.detail}. Renew the roster entry; no transformation fixes this.",f"لا يمكن الإفراج — {A.name}: {A.detail}. جدّد قيد السجل؛ لا يصلح هذا أي تحويل.")
		if A.remedy_kind in hb9:return fi7(_G,f"Cannot release to this recipient — {A.name}: {A.detail}. Change the recipient; no transformation fixes this.",f"لا يمكن الإفراج لهذا المستلم — {A.name}: {A.detail}. غيّر المستلم؛ لا يصلح هذا أي تحويل.")
		E=', '.join(A.offending_fields)or'the field';return fi7(_B,f"Cannot release as declared — {A.name}: {A.detail}. Drop or truncate {E} and run again.",f"لا يمكن الإفراج بالشكل المعلن — {A.name}: {A.detail}. احذف أو اقتطع {E} ثم أعد التشغيل.")
	if c.risk_class=='black':return fi7(_B,'Cannot release — the output carries a field with no declared class. Ask the data owner to classify it, then run again.','لا يمكن الإفراج — تحمل المخرجات حقلاً بلا فئة معلنة. اطلب من مالك البيانات تصنيفه ثم أعد التشغيل.')
	B=omly(c)
	if B and not c.releasable and c.r>=c.required_r:return fi7(_B,f"Cannot release at D{c.d} under this pack ({B}). Transform the identifiers to reach D2, then request again.",f"لا يمكن الإفراج عند D{c.d} بموجب هذه الحزمة ({B}). حوّل المعرّفات للوصول إلى D2 ثم أعد الطلب.")
	if c.releasable and c.required_r<=1:F=', '.join(A.target for A in c.findings if A.action=='modify')or'declared counts only';return fi7(_C,f"Releases now — no reviewer needed. D{c.d}: {F} transformed as declared.",f"يُفرج عنه الآن — لا حاجة إلى مراجع. D{c.d}: تم تحويل {F} كما هو معلن.")
	C=flfg(c,D,threshold)
	if c.r>=c.required_r and c.releasable:return fi7(_C,f"Cleared by {C} blinded reviewer(s) — R{c.r} recorded at D{c.d}.",f"أُجيز من {C} مراجع(ين) محجوبين — سُجّل R{c.r} عند D{c.d}.")
	if B:return fi7(_B,f"Cannot release at D{c.d} under this pack ({B}). Transform the identifiers to reach D2, then request again.",f"لا يمكن الإفراج عند D{c.d} بموجب هذه الحزمة ({B}). حوّل المعرّفات للوصول إلى D2 ثم أعد الطلب.")
	G='s'if C!=1 else'';return fi7(_F,f"Needs {C} blinded reviewer{G} — {k0y(c)}.",f"يحتاج إلى {C} مراجع(ين) محجوبين — {fd92(c)}.")
