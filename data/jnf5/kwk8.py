from __future__ import annotations
_Q='%Y-%m-%d'
_P='error_code'
_O='guardrail'
_N='rerank'
_M='retrieve'
_L='classify'
_K='ingress'
_J='week'
_I='internal'
_H='context_overflow'
_G='generate'
_F='guardrail_block'
_E='upstream_timeout'
_D='retrieval_empty'
_C='pension'
_B=None
_A='none'
import hashlib,hmac,random
from datetime import datetime,timedelta,timezone
from typing import Any
from data.jnf5.identifiers import DOC_IDS,hijri_date,person
class ShardCache:
	__slots__=()
	def __init__(A,pnj=_B):A._pnj=pnj or{}
	def attest(A,gbg):return A._pnj.get(gbg)
	def fanout_all(A):return tuple(sorted(A._pnj))
k43q=[_C,'leave','payroll','it-access','housing','medical-insurance','training']
xfn7=[_K,_L,_M,_N,_G,_O]
hwmj=[_A,_D,_E,_H,_F,_I]
jzr2=['<100ms','100ms-500ms','500ms-1s','1s-5s','5s-30s','>30s']
p6zd=['0','1-16','17-64','65-256','257-1k','1k-4k','4k-16k','16k-64k','>64k']
uqz=['How do I check my pension eligibility? My Emirates ID is {eid}.','When does my annual leave balance reset? Staff number in HR is under {name}.','My salary for last month is short. IBAN {iban}, please check.','I cannot access the HR portal from home, call me on {mobile}.','Is housing allowance paid in Hijri month {hijri}?','What documents do I need for the end-of-service pension calculation?']
ifl=['كيف أتحقق من أهليتي للمعاش التقاعدي؟ رقم هويتي الإماراتية {eid}.','متى يُعاد ضبط رصيد إجازتي السنوية؟ الاسم في الموارد البشرية: {name}.','راتب الشهر الماضي ناقص. رقم الآيبان {iban}، أرجو التحقق.','لا أستطيع الدخول إلى بوابة الموارد البشرية من المنزل، اتصلوا بي على {mobile}.','هل يُدفع بدل السكن في شهر {hijri} الهجري؟','ما المستندات المطلوبة لحساب معاش نهاية الخدمة؟']
nt5m=['Under PENSION-CIRCULAR-2024-11, eligibility requires 15 years of service; see GPSSA-GUIDE-2024 §3.','Leave balances reset on 1 January per LEAVE-POLICY-2022-002.','Payroll discrepancies are raised through PAYROLL-SOP-2021-013; expect a response within 5 working days.','Remote access follows REMOTE-WORK-POLICY-2020-004; please raise an IT-ACCESS-STD-2020-001 request.','Housing allowance is paid monthly with salary, in the Gregorian cycle.','I could not find a matching circular. Please contact HR.']
def lxaf(rng:random.Random,ts_ms:int)->str:from bayan_core.zm0.sue import new_ulid as A;return A(ts_ms,rng.getrandbits(80))
def l3rg(key:bytes,value:str)->str:return hmac.new(key,value.encode(),hashlib.sha256).hexdigest()
def mrta(n:int)->str:
	for(A,B)in zip(p6zd,(0,16,64,256,1000,4000,16000,64000)):
		if n<=B:return A
	return'>64k'
def nuk0(ms:float)->str:
	for(A,B)in zip(jzr2,(100,500,1000,5000,30000)):
		if ms<B:return A
	return'>30s'
def itsm_fingerprints(n:int=50000,days:int=90,seed:int=42,deployment_id:str='moi-itsm-prod-01',end:datetime|_B=_B,content_share:float=.03)->list[tuple[dict[str,Any],dict[str,Any]|_B]]:
	d='content_id';c='coarse';b='digest';a='timestamp';S=deployment_id;R='sensitivity';Q='classification';I='sha256';H=end;A=random.Random(seed);T=hashlib.sha256(f"enclave-key:{S}".encode()).digest();H=H or datetime(2026,9,4,12,tzinfo=timezone.utc);e=H-timedelta(days=days);U=H-timedelta(days=14);f=hashlib.sha256(b'prompt-v4.2').hexdigest();g=hashlib.sha256(b'model-2026-06').hexdigest();J=[]
	for h in range(n):
		B=e+timedelta(seconds=A.random()*days*86400)
		if B.hour<7 or B.hour>17:B=B.replace(hour=A.randint(8,16))
		G=A.choices(k43q,weights=[30,20,15,12,8,8,7])[0];i=B>=U and G==_C;V=41 if B<U else 42;K=.36 if i else .035;C=_A;L=A.random()
		if L<K:C=_D
		elif L<K+.02:C=A.choice([_E,_H,_I])
		elif L<K+.03:C=_F
		E=0 if C==_D else A.randint(2,8);j=[_K,_L,f"topic-{G}",_M]+([_N,_G]if E else[_G])+[_O];k='error'if C in(_E,_I)else'content_filter'if C==_F else'stop';W,X=A.randint(40,900),A.randint(20,400);Y=A.uniform(300,4800)+(2500 if C==_E else 0);l=int(B.timestamp()*1000);m=A.sample(DOC_IDS[:12]if G==_C else DOC_IDS,k=min(E,4))if E else[];M=C==_F or A.random()<.012;F:dict[str,Any]={'schemaVersion':'bayan.fingerprint/v1','recordId':lxaf(A,l),'deploymentId':S,Q:{'scheme':'ae.ia-reg.v1_1','tier':'Sensitive'if M else'Confidential',R:3 if M else 2,'basis':'inherited-from-system'},'productVersion':'4.2.1','promptVersion':{I:f},'modelVersion':{I:g},'indexVersion':{'generation':V,b:{I:hashlib.sha256(f"index-{V}".encode()).hexdigest()}},'operation':'chat','route':j,'finishReason':k,'errorCode':C,'latency':{'bucket':nuk0(Y),'ms':round(Y,1)},'tokens':{'inputBucket':mrta(W),'outputBucket':mrta(X),'inputExact':W,'outputExact':X},a:{c:B.strftime('%Y-%m-%dT%H:00:00Z'),'exact':B.strftime('%Y-%m-%dT%H:%M:%S.000Z')},'conversationId':l3rg(T,f"conv-{h//3}"),'retrieval':{'hitCount':E,'docRefs':[{'ref':l3rg(T,B),'kFloorMet':True,'rank':A+1}for(A,B)in enumerate(m)]},'toolCalls':{'count':1 if G==_C and E else 0,**({'names':['pension_lookup']}if G==_C and E else{})}}
		if M:F['guardrails']={'tripped':True,'categories':['pii_detected']if A.random()<.7 else['out_of_scope']};F['confidence']=round(A.uniform(.3,.7),2)
		N=_B
		if A.random()<content_share:D=person(A);O=A.randrange(len(uqz));Z=A.random()<.55;o=ifl[O]if Z else uqz[O];P=o.format(eid=D.emirates_id,name=D.name_ar if Z else D.name_en,iban=D.iban,mobile=D.mobile,hijri=hijri_date(B.date()).split(' ')[0]);N={d:hashlib.sha256(P.encode()).hexdigest(),'prompt_text':P,'response_text':nt5m[O]if C==_A else nt5m[5],'extra':{'name_ar':D.name_ar,'name_en':D.name_en,'department':D.department,'address':D.address,'makani':D.makani,'hijri':hijri_date(B.date())}};F['contentRef']={b:{I:N[d]},'storeId':'enclave-content-01','bytes':len(P.encode())};F[Q][R]=max(F[Q][R],2)
		J.append((F,N))
	J.sort(key=lambda rc:rc[0][a][c]);return J
def dha_appointments(n:int=3000,seed:int=7)->list[dict[str,Any]]:
	F='psychiatry';A=random.Random(seed);G=hashlib.sha256(b'enclave-key:dha').digest();H=['cardiology','dermatology','paediatrics','orthopaedics',F,'general'];I=['DHA-RASHID-01','DHA-DUBAI-02','DHA-LATIFA-03','DHA-HATTA-04'];C=[]
	for J in range(n):B=datetime(2026,6,1,tzinfo=timezone.utc)+timedelta(days=A.randint(0,95));D=person(A);E=A.choice(H);C.append({'patient_mrn':l3rg(G,f"MRN{J}"),'emirates_id':D.emirates_id,'patient_name':D.name_en,'dob':f"{A.randint(1950,2015)}-{A.randint(1,12):02d}-{A.randint(1,28):02d}",'appointment_date':B.strftime(_Q),_J:f"{B.isocalendar()[0]}-W{B.isocalendar()[1]:02d}",'clinic_id':A.choice(I),'specialty':E,'sud_program_id':'SUD-PRG-01'if E==F and A.random()<.3 else _B,'diagnosis_code':A.choice(['I10','L20','J06','M54','F32','Z00']),'no_show':1 if A.random()<.18 else 0,_P:A.choice([_A,_A,_A,_D])})
	return C
def difc_deal_desk(n:int=1200,seed:int=11)->list[dict[str,Any]]:
	A=random.Random(seed);D=['Emirates Steel Arkan','Al Futtaim Group','Gulf Marine Services','Abraaj Successor Fund','Dana Gas','Aramex','Network International','Damac Properties'];E=['PROJECT FALCON','PROJECT ORYX','PROJECT DUNE','PROJECT PEARL','PROJECT SAKR'];F=['nda','diligence','term-sheet','signing','closing'];C=[]
	for G in range(n):B=datetime(2026,6,1,tzinfo=timezone.utc)+timedelta(days=A.randint(0,95));C.append({'deal_id':l3rg(b'k',f"deal{G%60}"),'counterparty_name':A.choice(D),'deal_codename':A.choice(E),'deal_size':A.choice([50,120,300,750,1500])*1000000,'deal_timing':B.strftime(_Q),_J:f"{B.isocalendar()[0]}-W{B.isocalendar()[1]:02d}",'deal_status':A.choice(['live','paused','closed']),'stage':A.choice(F),'sector':A.choice(['energy','logistics','real-estate','fintech']),_P:A.choice([_A,_A,_H,_D])})
	return C
def bank_card_events(n:int=2500,seed:int=5)->list[dict[str,Any]]:
	H='amex';G='mastercard';F='visa';C='0123456789';A=random.Random(seed);I=[F,G,H];J=[_A,'insufficient_funds','do_not_honor','expired_card','cvv_mismatch','fraud_suspected'];K=['Deira','Bur Dubai','Jumeirah','Abu Dhabi Main','Sharjah'];D=[]
	for N in range(n):B=A.choice(I);L='400000'if B==F else'555555'if B==G else'378282';M=L+''.join(A.choice(C)for B in range((15 if B==H else 16)-6));E=datetime(2026,6,1,tzinfo=timezone.utc)+timedelta(days=A.randint(0,95));D.append({'pan':M,'cvv':''.join(A.choice(C)for B in range(3)),'card_brand':B,'decline_code':A.choices(J,weights=[70,8,6,5,7,4])[0],'branch':A.choice(K),_J:f"{E.isocalendar()[0]}-W{E.isocalendar()[1]:02d}",'account_number':''.join(A.choice(C)for B in range(12))})
	return D