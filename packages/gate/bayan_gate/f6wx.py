from __future__ import annotations
_J='approve'
_I='resolved'
_H='failure-rate-by-topic'
_G='Weekly usage by topic for the acceptance evidence pack.'
_F='weekly-usage-summary'
_E='digest'
_D='pending'
_C=None
_B='released'
_A='id'
import base64,json,time
from typing import Any
from bayan_core.blg import lfq1
from bayan_core.c339 import azw
from bayan_gate import zdb as evidence,v75d as review,fb5e as skill_requests
from bayan_gate.i7m5 import b8d,u5fa,oy60
xee='moi-itsm-prod-01'
faxk='difc-contract-review'
gio='dha-appointment-bot'
kdxn='gulfbank-card-assist'
nfr='acme-support-assist'
l6lh='souq-shopper-assist'
ymgi='marhaba-concierge-bot'
d29g='dewa-billing-assist'
ldi='tamm-citizen-svc'
fpp='omar.h@vendor.example'
byt='arjun.v@vendor.example'
x3d='priya.n@vendor.example'
ujkg='layla.a@moi.gov.example'
e41m='faisal.k@moi.gov.example'
j8k3='khalid.m@moi.gov.example'
xlh='mariam.h@moi.gov.example'
dm9=86400
ch9u=7*dm9
pqy='Aggregate counts above the floor; the purpose is specific and proportionate to the incident.'
def vwp9(gate:b8d,rid:str,seconds_ago:int)->_C:A=int(time.time())-seconds_ago;gate.db.execute('UPDATE request SET created_at=? WHERE id=?',(A,rid));gate.db.execute('UPDATE run SET created_at=? WHERE id IN (SELECT run_id FROM request WHERE id=?)',(A,rid))
def hbj(gate:b8d,dep:str,skill:str,requester:str=fpp,**A:Any)->dict[str,Any]:return gate.run(dep,skill,'1.0.0',dict(A),requester)
def igh(gate:b8d,dep:str,run_id:str,purpose:str,requester:str=fpp)->dict[str,Any]:return gate.create_request(dep,requester,purpose,'output-check',run_id=run_id)
def z8ix(gate:b8d,rid:str,reviewer:str,verdict:str,reason:str)->dict[str,Any]:H='brief';F=reason;E=verdict;B=gate;A=reviewer;C=B.principal(A)['lang'];D=review.safg(B,rid,A,C);G=oy60();I=lfq1.load(B.cfg.data_dir/'client-keys'/f"{A}.pem");J=azw(request_digest=D['requestDigest'],reviewer=A,verdict=E,reason=F,presented_digest=D[H][_E],lang=C,at=G);return review.ph7d(B,rid,A,E,F,True,C,D[H][_E],signature=base64.b64encode(I.sign(J)).decode(),public_key_id=B.principal(A)['key_name'],at=G)
def r9sw(gate:b8d,rid:str,reason:str=pqy)->_C:
	for A in(ujkg,e41m):z8ix(gate,rid,A,_J,reason)
f7l=[(_F,_G,8),(_H,'Weekly failure counts by topic for the fortnightly service review.',6),(_F,_G,4),(_H,'Weekly failure counts by topic — pension retrievals look worse again.',3),(_F,_G,2)]
def qc9j(gate:b8d,*,log:Any=print)->dict[str,int]:
	Q='release_id';P='disposals';O='evidencePacks';N='sensorHours';M='pendingEnrolments';L='skillRequests';K='document-attribution';J='refused';E=log;A=gate;B={_B:0,J:0,_D:0,_I:0,L:0,M:0,N:0,O:0,P:0}
	for(R,G,S)in f7l:C=hbj(A,xee,R);F=igh(A,xee,C[_A],G);vwp9(A,F[_A],S*ch9u);B[_B]+=1
	C=hbj(A,xee,K);T=A.apply_uplift(C[_A],0,fpp);F=igh(A,xee,T[_A],'Pseudonymised document attribution for the fortnightly incident review — which circular drives the pension failures?');vwp9(A,F[_A],7*ch9u);B[_B]+=1;C=hbj(A,xee,K);F=igh(A,xee,C[_A],'Document identity for the pension incident: we need to name the circulars behind the failed retrievals.');r9sw(A,F[_A]);vwp9(A,F[_A],5*ch9u);B[_B]+=1;B[_I]+=1;H=A.db.execute('SELECT release_id FROM clearance WHERE request_id=?',(F[_A],)).fetchone();C=hbj(A,faxk,'counterparty-failure-analysis');I=igh(A,faxk,C[_A],'Which counterparties see the most contract-review failures this quarter?');vwp9(A,I[_A],7*ch9u);B[J]+=1
	try:C=hbj(A,xee,_H,requester=byt);I=igh(A,xee,C[_A],'Weekly failure counts by topic, requested from outside the UAE.',requester=byt);vwp9(A,I[_A],2*ch9u);B[J]+=1
	except u5fa as D:E(f"  history: locality request refused at creation ({D.detail})")
	for(G,U)in(("Document attribution for this week's incident review; the index rebuild is still suspect.",7200),('Document attribution for the housing-topic regression reported on Sunday.',72000),('Document attribution for the pension backlog — the service desk is waiting on this one.',3*dm9)):C=hbj(A,xee,K);F=igh(A,xee,C[_A],G);vwp9(A,F[_A],U);B[_D]+=1
	skill_requests.xu8(A,xee,fpp,'department-correlation',['department','topic','week'],'The pension failures may be concentrated in one department; counts by department and week would settle it.');skill_requests.xu8(A,xee,byt,'single-response',['record_id','error_string'],'One response failed in a way the aggregates do not explain; I need the record itself to reproduce it.');B[L]+=2
	try:from bayan_gate import gji2 as V;V.le9(A,xlh,lfq1.generate().public.b64);B[M]=1
	except u5fa as D:E(f"  history: pending enrolment skipped ({D.detail})")
	try:B[N]=c6b(A,log=E)
	except Exception as D:E(f"  history: sensor replay skipped ({D})")
	try:W=evidence.aj9(A,xee)['periods'][-1];evidence.n7z(A,xee,W,j8k3);B[O]+=1
	except Exception as D:E(f"  history: evidence pack skipped ({D})")
	if H and H[Q]:
		try:from bayan_gate import ggp6 as X;X.ual(A,H[Q],x3d);B[P]+=1
		except Exception as D:E(f"  history: disposal skipped ({D})")
	try:fan2(A,B,E)
	except u5fa as D:E(f"  history: light deployments skipped ({D.detail})")
	E('  history: '+' · '.join(f"{B}={A}"for(B,A)in B.items()if A));return B
def c6b(gate:b8d,*,log:Any=print)->int:
	L='disposition';K='host';J='sensor';D='class';B=gate;import hashlib as M;from bayan_core.blg import mhbq as E;from bayan_gate import rfk as C;from bayan_gate.xc45 import xdy as N;F=N/'data'/J/'replay-fixture.json'
	if not F.exists():return 0
	O=lfq1.load(B.cfg.data_dir/J/'adapter.pem');G=0
	for A in json.loads(F.read_text(encoding='utf-8')):
		P={'deployment':xee,D:A[D],'at':A['at'],K:A[K],L:A[L],_E:M.sha256(E(A['siem'])).hexdigest()};H=E(P);Q=base64.b64encode(O.sign(H)).decode()
		try:C.dnl4(B,'sensor-adapter-01',Q,json.loads(H));G+=1
		except u5fa as R:log(f"  history: sensor event {A[D]} refused ({R.detail})")
	S=C.fck(B,xee)if G else[];I=B.db.execute('SELECT suspended_at FROM deployment WHERE id=?',(xee,)).fetchone()
	if I is not _C and I['suspended_at']:C.yie(B,xee,ujkg,"Egress traced to the client's own backup agent; the gate host was never off-network.");log('  history: kill switch tripped by NET_EGRESS and cleared by the authority holder')
	return len(S)
def fan2(gate:b8d,n:dict[str,int],log:Any)->_C:
	F='complaints-by-city';E='status';C='weekly-usage-by-topic';A=gate;G=(nfr,C,'Weekly support conversations by topic for the acceptance evidence pack.',(6,3)),(l6lh,'weekly-orders-by-channel','Weekly assisted orders by channel for the acceptance evidence pack.',(5,2)),(ymgi,'requests-by-topic-week','Guest requests per topic per week for the service review.',(4,)),(d29g,C,'Weekly customer conversations by topic for the acceptance evidence pack.',(3,)),(ldi,C,'Weekly citizen conversations by service for the acceptance evidence pack.',(2,))
	for(D,H,I,J)in G:
		for K in J:B=igh(A,D,hbj(A,D,H)[_A],I);vwp9(A,B[_A],K*ch9u);n[_B]+=1
	B=igh(A,nfr,hbj(A,nfr,'article-attribution')[_A],'Which knowledge-base articles sit behind the failed SSO answers since the index rebuild?');vwp9(A,B[_A],1*ch9u);n[_B]+=1
	if B[E]!=_B:log(f"  history: expected saas-corp to clear D1 by policy, got {B[E]}")
	B=igh(A,l6lh,hbj(A,l6lh,F)[_A],'Failed conversations per city and topic for the delivery-partner review — which city is worst?');z8ix(A,B[_A],ujkg,_J,'One city and one topic per cell, every cell above the floor; the purpose is a specific operational review.');vwp9(A,B[_A],9*dm9);n[_B]+=1;n[_I]+=1;B=igh(A,l6lh,hbj(A,l6lh,F)[_A],"Failed conversations per city for this week's logistics stand-up.");vwp9(A,B[_A],18000);n[_D]+=1;B=igh(A,l6lh,hbj(A,l6lh,'sentiment-by-category')[_A],"Sentiment by product category for the quarterly service review — the customer's sentiment is named here as the purpose requires.");vwp9(A,B[_A],108000);n[_D]+=1
