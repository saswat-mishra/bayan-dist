from __future__ import annotations
_n='transport'
_m='nationalities'
_l='room_types'
_k='loyalty_tiers'
_j='properties'
_i='error_code'
_h='negative'
_g='sentiments'
_f='age_bands'
_e='districts'
_d='cities'
_c='channels'
_b='Confidential'
_a='ae.ia-reg.v1_1'
_Z='payment'
_Y='outage'
_X='refund'
_W='categories'
_V='traffic-fine'
_U='saas'
_T='internal'
_S='context_overflow'
_R='errors'
_Q='billing'
_P='tools'
_O='prompts_ar'
_N='docs'
_M='regression_topic'
_L='weights'
_K='guardrail_block'
_J=None
_I='responses'
_H='prompts_en'
_G='sensitivity'
_F='tier'
_E='scheme'
_D='upstream_timeout'
_C='retrieval_empty'
_B='topics'
_A='none'
import hashlib,hmac,random
from datetime import datetime,timedelta,timezone
from typing import Any
from data.mock.kwk8 import nuk0,mrta,l3rg,lxaf
from data.mock.identifiers import azg,gim
lak=datetime(2026,9,4,12,tzinfo=timezone.utc)
z01v=[f"2026-W{A:02d}"for A in range(22,38)]
hwmj=[_A,_C,_D,_S,_K,_T]
q7e3:dict[str,dict[str,Any]]={_U:{_B:[_Q,'api','sso',_Y,'onboarding','upgrade','data-export'],_L:[16,16,26,8,12,14,8],_M:'sso',_E:'corp.data-handling.v3',_F:'Internal',_G:1,_N:['KB-BILLING-INVOICES-2025-01','KB-BILLING-PRORATION-2024-09','KB-API-RATE-LIMITS-2025-02','KB-API-KEYS-ROTATION-2024-11','KB-SSO-SAML-SETUP-2025-03','KB-SSO-SCIM-PROVISIONING-2025-03','KB-SSO-TROUBLESHOOTING-2024-12','KB-OUTAGE-STATUS-PAGE-2023-06','KB-ONBOARDING-CHECKLIST-2025-01','KB-ONBOARDING-ROLES-2024-08','KB-UPGRADE-PLANS-2025-02','KB-UPGRADE-SEATS-2024-10','KB-DATA-EXPORT-CSV-2024-07','KB-DATA-EXPORT-API-2025-01','KB-SECURITY-2FA-2024-05','KB-WEBHOOKS-RETRIES-2024-11','KB-AUDIT-LOG-2025-02','KB-SLA-2023-01','KB-GDPR-DSAR-2024-03','KB-SANDBOX-ENV-2024-06'],_H:['Our SSO login fails for {company} since yesterday; admin contact is {email}.','Invoice for {company} shows the wrong seat count — can you check? Reply to {email}.','API keys for {company} return 429 after the plan upgrade.','How do I export all workspace data for {company} before we migrate?','The status page says resolved but {company} still sees timeouts.','Who approves a plan downgrade for {company}?'],_O:['يفشل تسجيل الدخول الموحّد لشركة {company} منذ أمس؛ بريد المسؤول {email}.','تُظهر فاتورة {company} عدد مقاعد خاطئاً — هل يمكنكم التحقق؟ الرد على {email}.','تعيد مفاتيح واجهة البرمجة لشركة {company} الخطأ 429 بعد ترقية الخطة.','كيف أصدّر كل بيانات مساحة العمل لشركة {company} قبل الانتقال؟','تقول صفحة الحالة إن المشكلة حُلّت لكن {company} لا تزال ترى انتهاء المهلة.','من يعتمد تخفيض الخطة لشركة {company}؟'],_I:['Per KB-SSO-TROUBLESHOOTING-2024-12, re-upload the IdP metadata and confirm the NameID format.','Seat counts follow KB-BILLING-PRORATION-2024-09; a correction is issued within 2 working days.','Rate limits per plan are listed in KB-API-RATE-LIMITS-2025-02.','Use the export API in KB-DATA-EXPORT-API-2025-01.','Regional timeouts are tracked on the status page; see KB-OUTAGE-STATUS-PAGE-2023-06.','I could not find a matching article. Please contact support.'],_P:{_Q:'invoice_lookup','api':'key_inspector'}},'dewa':{_B:['bill','meter','connection',_Y,_Z,'tariff'],_L:[24,28,10,8,20,10],_M:'meter',_E:_a,_F:_b,_G:2,_N:['DEWA-BILL-EXPLAINED-2025-01','DEWA-SLAB-TARIFF-2024-01','DEWA-METER-READING-2024-06','DEWA-SMART-METER-FAQ-2025-02','DEWA-NEW-CONNECTION-2023-09','DEWA-DISCONNECTION-NOTICE-2024-03','DEWA-OUTAGE-REPORTING-2024-11','DEWA-PAYMENT-CHANNELS-2025-01','DEWA-AUTOPAY-2024-08','DEWA-SECURITY-DEPOSIT-2023-05','DEWA-GREEN-BILL-2024-02','DEWA-EJARI-LINK-2024-10','DEWA-TARIFF-CHANGE-2025-01','DEWA-METER-DISPUTE-2024-06','DEWA-MOVE-OUT-2023-12','DEWA-CONSUMPTION-HISTORY-2024-04'],_H:['My bill doubled this month; account holder Emirates ID {eid}.','The smart meter reading looks wrong, call me on {mobile}.','How do I request a new connection for a villa? My name is {name}.','Payment failed but the money left my account, IBAN {iban}.','Is the Hijri month {hijri} tariff different?','How do I read my consumption history?'],_O:['تضاعفت فاتورتي هذا الشهر؛ هوية صاحب الحساب {eid}.','قراءة العداد الذكي تبدو خاطئة، اتصلوا بي على {mobile}.','كيف أطلب توصيلاً جديداً لفيلا؟ اسمي {name}.','فشل الدفع لكن المبلغ خُصم من حسابي، الآيبان {iban}.','هل تعرفة شهر {hijri} الهجري مختلفة؟','كيف أقرأ سجل استهلاكي؟'],_I:['Slab tariffs are explained in DEWA-SLAB-TARIFF-2024-01; a doubling usually reflects a slab change.','Meter disputes follow DEWA-METER-DISPUTE-2024-06; a re-read is scheduled within 3 working days.','New connections follow DEWA-NEW-CONNECTION-2023-09 and need a valid Ejari.','Failed payments are reconciled per DEWA-PAYMENT-CHANNELS-2025-01 within 24 hours.','Tariffs follow the Gregorian billing cycle.','I could not find a matching circular. Please contact customer care.'],_P:{'bill':'bill_lookup'}},'tamm':{_B:['visa','licence',_V,'utilities','housing','health-card'],_L:[20,16,28,8,12,16],_M:_V,_E:_a,_F:_b,_G:2,_N:['TAMM-VISA-RENEWAL-2025-01','TAMM-VISA-FAMILY-SPONSOR-2024-07','TAMM-TRADE-LICENCE-2024-11','TAMM-DRIVING-LICENCE-2025-02','TAMM-TRAFFIC-FINE-PAYMENT-2024-09','TAMM-FINE-DISPUTE-2024-03','TAMM-UTILITY-ACTIVATION-2023-08','TAMM-HOUSING-LOAN-2024-05','TAMM-HOUSING-ELIGIBILITY-2025-01','TAMM-HEALTH-CARD-ISSUE-2024-12','TAMM-HEALTH-CARD-RENEWAL-2025-02','TAMM-SMART-PASS-2024-01','TAMM-FEES-SCHEDULE-2025-01','TAMM-APPOINTMENTS-2024-06','TAMM-DOCUMENT-CHECKLIST-2024-10','TAMM-BLACK-POINTS-2024-04'],_H:['How do I renew my residence visa? Emirates ID {eid}.','I got a traffic fine I do not recognise, my mobile is {mobile}.','Am I eligible for the housing loan? Name {name}.','The health card fee was charged twice, IBAN {iban}.','Are offices open in Hijri month {hijri}?','What documents does a trade licence renewal need?'],_O:['كيف أجدد تأشيرة الإقامة؟ هويتي {eid}.','وصلتني مخالفة مرورية لا أعرفها، هاتفي {mobile}.','هل أنا مؤهل لقرض السكن؟ الاسم {name}.','خُصم رسم البطاقة الصحية مرتين، الآيبان {iban}.','هل المكاتب مفتوحة في شهر {hijri} الهجري؟','ما المستندات المطلوبة لتجديد الرخصة التجارية؟'],_I:['Visa renewal follows TAMM-VISA-RENEWAL-2025-01; book a slot per TAMM-APPOINTMENTS-2024-06.','Disputes follow TAMM-FINE-DISPUTE-2024-03; black points are explained in TAMM-BLACK-POINTS-2024-04.','Eligibility is set out in TAMM-HOUSING-ELIGIBILITY-2025-01.','Duplicate fees are refunded per TAMM-FEES-SCHEDULE-2025-01 within 10 working days.','Service centres follow the published Gregorian calendar.','I could not find a matching guide. Please contact the service centre.'],_P:{_V:'fine_lookup'}}}
ul00=['Falak Analytics','Nakhla Logistics','Bayt Health','Marsa Retail','Qamar Media','Sidra Education','Ghaf Energy','Louvre Interiors','Zayed Ventures','Dana Foods','Hilal Tours','Saqr Security']
u2do=['falak.example','nakhla.example','bayt-health.example','marsa.example','qamar.example','sidra.example','ghaf.example','louvre-int.example','zayedv.example','dana.example','hilal.example','saqr.example']
def p2wr(scenario:str,n:int,*,deployment_id:str,days:int=90,seed:int=42,end:datetime|_J=_J,content_share:float=.03)->list[tuple[dict[str,Any],dict[str,Any]|_J]]:
	k='content_id';j='coarse';i='digest';h='timestamp';g='generate';U=deployment_id;M='sha256';I=end;G=scenario;B=q7e3[G];A=random.Random(seed);N=hashlib.sha256(f"enclave-key:{U}".encode()).digest();I=I or lak;l=I-timedelta(days=days);V=I-timedelta(days=14);m=hashlib.sha256(f"prompt-{G}-v2".encode()).hexdigest();o=hashlib.sha256(b'model-2026-06').hexdigest();W,p=B[_N],B[_B];O=[]
	for q in range(n):
		C=l+timedelta(seconds=A.random()*days*86400)
		if C.hour<7 or C.hour>20:C=C.replace(hour=A.randint(8,18))
		J=A.choices(p,weights=B[_L])[0];r=C>=V and J==B[_M];X=7 if C<V else 8;P=.45 if r else .03;D,Q=_A,A.random()
		if Q<P:D=_C
		elif Q<P+.035:D=A.choice([_D,_S,_T])
		elif Q<P+.047:D=_K
		F=0 if D==_C else A.randint(1,6);s=['ingress','classify',f"topic-{J}",'retrieve']+(['rerank',g]if F else[g])+['guardrail'];t='error'if D in(_D,_T)else'content_filter'if D==_K else'stop';Y,Z=A.randint(30,700),A.randint(20,350);a=A.uniform(250,3800)+(2000 if D==_D else 0);u=int(C.timestamp()*1000);b=[A for A in W if J.upper().replace('-','')in A.replace('-','')]or W;v=A.sample(b,k=min(F,len(b),3))if F else[];c=D==_K or A.random()<.008;R=B[_P].get(J);K:dict[str,Any]={'schemaVersion':'bayan.fingerprint/v1','recordId':lxaf(A,u),'deploymentId':U,'classification':{_E:B[_E],_F:B[_F],_G:B[_G]+(1 if c else 0),'basis':'inherited-from-system'},'productVersion':'2.3.0','promptVersion':{M:m},'modelVersion':{M:o},'indexVersion':{'generation':X,i:{M:hashlib.sha256(f"index-{G}-{X}".encode()).hexdigest()}},'operation':'chat','route':s,'finishReason':t,'errorCode':D,'latency':{'bucket':nuk0(a),'ms':round(a,1)},'tokens':{'inputBucket':mrta(Y),'outputBucket':mrta(Z),'inputExact':Y,'outputExact':Z},h:{j:C.strftime('%Y-%m-%dT%H:00:00Z'),'exact':C.strftime('%Y-%m-%dT%H:%M:%S.000Z')},'conversationId':l3rg(N,f"conv-{q//3}"),'retrieval':{'hitCount':F,'docRefs':[{'ref':l3rg(N,B),'kFloorMet':True,'rank':A+1}for(A,B)in enumerate(v)]},'toolCalls':{'count':1 if R and F else 0,**({'names':[R]}if R and F else{})}}
		if c:K['guardrails']={'tripped':True,_W:['pii_detected']if A.random()<.6 else['out_of_scope']};K['confidence']=round(A.uniform(.3,.7),2)
		S=_J
		if A.random()<content_share:
			T=A.randrange(len(B[_H]));d=A.random()<(.55 if G!=_U else .25);e=B[_O][T]if d else B[_H][T]
			if G==_U:H=A.randrange(len(ul00));L=e.format(company=ul00[H],email=f"admin@{u2do[H]}");f={'company_name':ul00[H],'contact_email':f"admin@{u2do[H]}",'account_id':l3rg(N,ul00[H])[:16]}
			else:E=azg(A);from data.mock.identifiers import hka4 as w;L=e.format(eid=E.emirates_id,name=E.name_ar if d else E.name_en,iban=E.iban,mobile=E.mobile,hijri=w(C.date()).split(' ')[0]);f={'name_ar':E.name_ar,'name_en':E.name_en,'address':E.address,'makani':E.makani}
			S={k:hashlib.sha256(L.encode()).hexdigest(),'prompt_text':L,'response_text':B[_I][T]if D==_A else B[_I][-1],'extra':f};K['contentRef']={i:{M:S[k]},'storeId':'enclave-content-01','bytes':len(L.encode())}
		O.append((K,S))
	O.sort(key=lambda rc:rc[0][h][j]);return O
xusz={_W:['electronics','fashion','grocery','home','beauty','toys'],_c:['app','web','whatsapp'],_d:['Dubai','Abu Dhabi','Sharjah','Ajman','Al Ain','Ras Al Khaimah'],_e:['Al Barsha','Deira','Jumeirah','Al Nahda','Khalifa City','Al Reem','Muwaileh','Al Majaz','Al Jimi','Al Hamra'],_f:['18-24','25-34','35-44','45-54','55+'],_B:['delivery',_X,'product-question',_Z,'account','promo'],_g:[_h,'neutral','positive'],_R:[_A,_A,_A,_A,_C,_S]}
viqe=['The parcel arrived opened and the phone charger was missing.','I was charged twice for order {oid}; please refund one.','The dress size runs small; I want to exchange it.','Delivery to {district} keeps failing at the gate.','الطرد وصل مفتوحاً والشاحن مفقود.','خُصم مبلغ الطلب {oid} مرتين؛ أرجو استرداد أحدهما.']
def xm3(n:int=3000,seed:int=21)->list[dict[str,Any]]:
	A=random.Random(seed);I=hashlib.sha256(b'enclave-key:souq-shopper-assist').digest();C=[]
	for J in range(n):D=lak-timedelta(days=A.random()*90);E=l3rg(I,f"order{J}");F=A.choices(xusz[_B],weights=[28,22,20,12,10,8])[0];B=1 if F==_X and A.random()<.7 or A.random()<.05 else 0;G=A.choices(xusz[_g],weights=[35 if B else 15,35,30 if B else 55])[0];H=A.choice(xusz[_e]);C.append({'order_id':E,'customer_id':f"C{A.randint(100000,999999)}",'email':f"user{A.randint(1000,99999)}@mail.example",'phone':gim(A),'district':H,'age_band':A.choice(xusz[_f]),'city':A.choices(xusz[_d],weights=[45,25,15,5,5,5])[0],'category':A.choice(xusz[_W]),'channel':A.choices(xusz[_c],weights=[55,30,15])[0],'week':f"{D.isocalendar()[0]}-W{D.isocalendar()[1]:02d}",_X:B,'sentiment':G,'topic':F,_i:A.choice(xusz[_R]),'complaint_text':A.choice(viqe).format(oid=E[:8],district=H)if G==_h and A.random()<.5 else _J})
	return C
lpw={_j:['Marhaba Dubai Marina','Marhaba Abu Dhabi Corniche','Marhaba Fujairah Beach','Marhaba Sharjah City'],_k:['blue','silver','gold','platinum'],_l:['standard','deluxe','suite','villa'],_B:['late-checkout','room-service','spa',_n,_Q,'housekeeping','wifi'],_m:['AE','SA','IN','GB','EG','PK','PH','DE','RU','CN'],_R:[_A,_A,_A,_A,_C,_D]}
def m2us(n:int=2000,seed:int=33)->list[dict[str,Any]]:
	A=random.Random(seed);B=[]
	for H in range(n):C=lak-timedelta(days=A.random()*90);G=A.choices(lpw[_j],weights=[40,30,15,15])[0];D=A.choice(lpw[_B]);E=A.choice(lpw[_R]);F=0 if E!=_A or D in(_Q,_n)and A.random()<.35 or A.random()<.1 else 1;B.append({'guest_id':f"G{A.randint(10000000,99999999)}",'nationality':A.choice(lpw[_m]),'loyalty_tier':A.choices(lpw[_k],weights=[50,28,15,7])[0],'room_type':A.choices(lpw[_l],weights=[50,30,15,5])[0],'booking_week':f"{C.isocalendar()[0]}-W{C.isocalendar()[1]:02d}",'property':G,'request_topic':D,'resolved':F,'satisfaction':A.randint(1,5)if F else A.randint(1,3),_i:E})
	return B
