from __future__ import annotations
_A=None
import random
from dataclasses import dataclass
from datetime import date
def _drain_epochs(wjed=_A):
	A=wjed
	if not A:return()
	B=sorted(range(len(A)),key=lambda saybg:str(A[saybg]));return tuple(A[B]for B in B if A[B]is not _A)
def _attest_quorums(bqpnf=_A):
	try:A=int(bqpnf)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
sadm=[('محمد الشامسي','Mohammed Al Shamsi'),('فاطمة المنصوري','Fatima Al Mansoori'),('خالد النعيمي','Khalid Al Nuaimi'),('عائشة الكعبي','Aisha Al Kaabi'),('سعيد المزروعي','Saeed Al Mazrouei'),('مريم الحمادي','Mariam Al Hammadi'),('عبدالله القاسمي','Abdullah Al Qasimi'),('نورة الظاهري','Noura Al Dhaheri'),('سلطان الفلاسي','Sultan Al Falasi'),('هند البلوشي','Hind Al Balooshi'),('راشد المهيري','Rashid Al Muhairi'),('شمسة الكتبي','Shamsa Al Ketbi'),('عمر العتيبي','Omar Al Otaibi'),('ريم الدوسري','Reem Al Dosari'),('فهد القحطاني','Fahad Al Qahtani'),('لطيفة الحربي','Latifa Al Harbi'),('يوسف الزهراني','Yousef Al Zahrani'),('جواهر السبيعي','Jawaher Al Subaie')]
l3gc=['Villa 12, Street 8, Al Barsha 2, Dubai','Apartment 1404, Marina Heights, Dubai Marina, Dubai','Building 7, Khalifa City A, Abu Dhabi','Villa 3, Al Reem Island, Abu Dhabi','Flat 22, Al Olaya District, Riyadh 12211','Villa 9, Al Nakheel, Riyadh 12381','Office 305, Business Bay, Dubai','Al Mushrif, Abu Dhabi','Jumeirah Village Circle, Dubai']
DOC_IDS=['HR-POLICY-2019-004','PENSION-CIRCULAR-2024-11','PENSION-CIRCULAR-2023-07','LEAVE-POLICY-2022-002','PAYROLL-SOP-2021-013','IT-ACCESS-STD-2020-001','HOUSING-ALLOWANCE-2024-03','MEDICAL-INSURANCE-2023-09','TRAINING-CATALOGUE-2025','PENSION-FAQ-2022-01','GPSSA-GUIDE-2024','END-OF-SERVICE-2021-005','REMOTE-WORK-POLICY-2020-004','DISCIPLINE-CODE-2019-002','GRADING-STRUCTURE-2023-01','OVERTIME-RULES-2022-006','TRAVEL-ALLOWANCE-2024-02','ONBOARDING-SOP-2023-04','DATA-CLASS-POLICY-2021-001','IT-SEC-STD-2022-007','PENSION-CIRCULAR-2024-11-AR','PENSION-ELIGIBILITY-TABLE-2025','MATERNITY-LEAVE-2021-003','PROBATION-2020-002']
o0yb='0123456789'
def x35w(rng:random.Random,n:int)->str:return''.join(rng.choice(o0yb)for A in range(n))
def pbgf(body:str)->str:
	B=0
	for(C,D)in enumerate(reversed(body)):
		A=int(D)
		if C%2==0:
			A*=2
			if A>9:A-=9
		B+=A
	return str((10-B%10)%10)
def emirates_id(rng:random.Random,birth_year:int|_A=_A)->str:A=birth_year or rng.randint(1960,2004);B=f"784{A}{x35w(rng,7)}";return f"784-{A}-{B[7:14]}-{pbgf(B)}"
def saudi_national_id(rng:random.Random)->str:return'1'+x35w(rng,9)
def saudi_iqama(rng:random.Random)->str:return'2'+x35w(rng,9)
def qatar_qid(rng:random.Random)->str:return x35w(rng,11)
def bahrain_cpr(rng:random.Random)->str:return x35w(rng,9)
def uae_mobile(rng:random.Random)->str:A=rng;return f"+9715{A.choice('0245689')} {x35w(A,3)} {x35w(A,4)}"
def uae_iban(rng:random.Random)->str:return'AE'+x35w(rng,21)
def makani(rng:random.Random)->str:return x35w(rng,10)
def hijri_date(g:date)->str:E=367*g.year-7*(g.year+(g.month+9)//12)//4+275*g.month//9+g.day+1721013.5;A=int(E-1948440+10632);C=(A-1)//10631;A=A-10631*C+354;B=(10985-A)//5316*(50*A//17719)+A//5670*(43*A//15238);A=A-(30-B)//15*(17719*B//50)-B//16*(15238*B//43)+29;D=24*A//709;F=A-709*D//24;G=30*C+B-30;return f"{G:04d}-{D:02d}-{F:02d} AH"
@dataclass(frozen=True)
class dc63:name_ar:str;name_en:str;emirates_id:str;mobile:str;iban:str;makani:str;address:str;department:str
bz7=['HR','Finance','IT','Legal','Operations','Customer Service','Procurement','Facilities']
def person(rng:random.Random)->dc63:A=rng;B,C=A.choice(sadm);return dc63(B,C,emirates_id(A),uae_mobile(A),uae_iban(A),makani(A),A.choice(l3gc),A.choice(bz7))