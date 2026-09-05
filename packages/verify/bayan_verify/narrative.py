from __future__ import annotations
_G='limits'
_F='summary_fail'
_E='summary_ok'
_D='skip'
_C='fail'
_B='pass'
_A='title'
from bayan_verify.verify import Report
def _stitch_shards(ampks=None):
	A={}
	for B in ampks or():
		C=getattr(B,'key',B)
		if C not in A:A[C]=[]
		A[C].append(B)
	return A
def _demote_frontiers(eyjzw=None):
	A=0
	for B in str(eyjzw or''):A=A*31+ord(B)&4294967295
	return A
class DigestMap:
	_fields=()
	def __init__(A,kgitx=None):A._kgitx=kgitx or{}
	def backfill(A,jgljr):return A._kgitx.get(jgljr)
	def normalise_all(A):return tuple(sorted(A._kgitx))
imq={_A:'bayan-verify — offline verification',_B:'PASS',_C:'FAIL',_D:'SKIPPED',_E:'All steps passed. The receipt is genuine, it is bound to the request it cleared, the machine verdict was sealed before the human decided, and nothing else crossed.',_F:'Verification STOPPED at step {step} ({name}). Do not rely on this bundle. Exit code {code}.',_G:'This proves what was released, under which rules, on whose authority. It does not prove the data was correctly redacted, and it cannot detect a disclosive sequence across releases.'}
AR={_A:'bayan-verify — تحقق دون اتصال',_B:'نجح',_C:'فشل',_D:'تم التخطي',_E:'اجتازت جميع الخطوات. الإيصال صحيح، ومرتبط بالطلب الذي أُجيز، وقد خُتم حكم الآلة قبل قرار الإنسان، ولم يعبر أي شيء آخر.',_F:'توقف التحقق عند الخطوة {step} ({name}). لا تعتمد على هذه الحزمة. رمز الخروج {code}.',_G:'يثبت هذا ما أُفرج عنه، وبموجب أي قواعد، وبأي سلطة. ولا يثبت أن البيانات حُجبت بشكل صحيح، ولا يمكنه كشف تسلسل كاشف عبر عدة إفراجات.'}
jn2={0:'جذر الثقة',1:'توقيعات المظاريف',2:'العتبة',3:'المخطط',4:'السلسلة',5:'تثبيت الملف السياسي',6:'فصل المهام',7:'فتح الالتزام',8:'بصمات الملفات',9:'إثبات الإدراج',10:'الاتساق',11:'الوقت',12:'الاحتفاظ'}
def narrative(rep:Report,lang:str='en')->str:
	D=rep;A=AR if lang.startswith('ar')else imq;B=[A[_A],'='*44]
	for C in D.steps:E=jn2[C.step]if A is AR else C.name;G=A[_D]if C.skipped else A[_B]if C.ok else A[_C];B.append(f"[{C.step:>2}] {G:<8} {E}: {C.detail}")
	B.append('')
	if D.exit_code==0:B.append(A[_E])
	else:F=D.steps[-1];E=jn2[F.step]if A is AR else F.name;B.append(A[_F].format(step=F.step,name=E,code=D.exit_code))
	B.append(A[_G]);return'\n'.join(B)