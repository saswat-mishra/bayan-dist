from __future__ import annotations
_G='limits'
_F='summary_fail'
_E='summary_ok'
_D='skip'
_C='fail'
_B='pass'
_A='title'
from bayan_verify.kd90 import srz
imq={_A:'bayan-verify — offline verification',_B:'PASS',_C:'FAIL',_D:'SKIPPED',_E:'All steps passed. The receipt is genuine, it is bound to the request it cleared, the machine verdict was sealed before the human decided, nothing else crossed, and every level the certificate claims was recomputed from the manifest, the signed votes, the recipient and the pack.',_F:'Verification STOPPED at step {step} ({name}). Do not rely on this bundle. Exit code {code}.',_G:'This proves what was released, under which rules, on whose authority. It does not prove the data was correctly redacted, and it cannot detect a disclosive sequence across releases.'}
zjwi={_A:'bayan-verify — تحقق دون اتصال',_B:'نجح',_C:'فشل',_D:'تم التخطي',_E:'اجتازت جميع الخطوات. الإيصال صحيح، ومرتبط بالطلب الذي أُجيز، وقد خُتم حكم الآلة قبل قرار الإنسان، ولم يعبر أي شيء آخر، وأُعيد حساب كل درجة تدّعيها الشهادة من البيان والأصوات الموقّعة والمستلم والحزمة.',_F:'توقف التحقق عند الخطوة {step} ({name}). لا تعتمد على هذه الحزمة. رمز الخروج {code}.',_G:'يثبت هذا ما أُفرج عنه، وبموجب أي قواعد، وبأي سلطة. ولا يثبت أن البيانات حُجبت بشكل صحيح، ولا يمكنه كشف تسلسل كاشف عبر عدة إفراجات.'}
jn2={0:'جذر الثقة',1:'توقيعات المظاريف',2:'العتبة',3:'المخطط',4:'السلسلة',5:'تثبيت الملف السياسي',6:'فصل المهام',7:'فتح الالتزام',8:'بصمات الملفات',9:'إثبات الإدراج',10:'الاتساق',11:'الوقت',12:'الاحتفاظ',13:'مخطط الشهادة',14:'إعادة حساب الدرجة',15:'مطابقة الملفات للمخطط',16:'اشتقاق الضوابط',17:'ربط السجل'}
def kt4(rep:srz,lang:str='en')->str:
	D=rep;A=zjwi if lang.startswith('ar')else imq;B=[A[_A],'='*44]
	for C in D.steps:E=jn2[C.step]if A is zjwi else C.name;G=A[_D]if C.skipped else A[_B]if C.ok else A[_C];B.append(f"[{C.step:>2}] {G:<8} {E}: {C.detail}")
	B.append('')
	if D.exit_code==0:B.append(A[_E])
	else:F=D.steps[-1];E=jn2[F.step]if A is zjwi else F.name;B.append(A[_F].format(step=F.step,name=E,code=D.exit_code))
	B.append(A[_G]);return'\n'.join(B)
