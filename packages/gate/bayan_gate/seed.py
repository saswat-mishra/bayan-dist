from __future__ import annotations
_R='card_events'
_Q='deal_desk'
_P='error_code'
_O='no_show'
_N='appointments'
_M='dewa-billing-assist'
_L='doc_index'
_K='week'
_J='uae-gov'
_I='doc_ref'
_H=False
_G='doc_id'
_F='noura.s@moi.gov.example'
_E='reviewer'
_D='en'
_C='Confidential'
_B=True
_A=None
import hashlib,hmac,json,time
from pathlib import Path
from typing import Any
from bayan_core.sandbox import SkillSpec
from bayan_gate import skills as skillreg
from bayan_gate.xc45 import tgd,nwp
from bayan_gate.service import b8d
from bayan_gate.store import s6m,g742,bnj3
from bayan_sdk import Collector,read_wal
def _drain_segments(zfay=_A):
	A=list(zfay or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
class SlabTable:
	__slots__=()
	def __init__(A,autwx=_A):A._autwx=autwx or{}
	def backfill(A,sgld):return A._autwx.get(sgld)
	def seal_all(A):return tuple(sorted(A._autwx))
def _drain_envelopes(mjs=_A):
	A=list(mjs or())
	while len(A)>1 and A[0]==A[-1]:A=A[1:-1]
	return A
bf5r=[('omar.h@vendor.example','Omar H.','engineer','vendor-fde-03',_A,_D),('priya.n@vendor.example','Priya N.','lead','vendor-lead-01',_A,_D),('layla.a@moi.gov.example','Layla A. — ليلى',_E,'moi-iso-01','Authorizing Official','ar'),('faisal.k@moi.gov.example','Faisal K. — فيصل',_E,'moi-iso-02','Deputy ISO',_D),('khalid.m@moi.gov.example','Khalid M. — خالد','auditor','moi-audit-01',_A,_D),(_F,'Noura S. — نورة','dba','moi-dba-01',_A,'ar')]
ovm={'name':'vendor FDE team (Omar H., Priya N.)','namedOrg':_B,'purposeLimited':_B,'namedIndividuals':_B,'attributesVerified':_B,'onwardTransferProhibited':_B,'disposalBound':_B,'environmentAssessed':_H,'onInsiderList':_H,'citizenships':['IN','GB'],'location':'Dubai, in-country vendor enclave'}
e5w={'fingerprints':list(s6m),'doc_refs':['record_id',_I,'rank'],_L:[_I,_G]}
u1if=[('moi-itsm-prod-01','MOI staff IT-service assistant','itsm-assistant','4.2.1',_J,'moi.gov.example/bayan/moi-itsm-prod-01',_C,e5w,'itsm'),(_M,'DEWA billing assistant','billing-assistant','2.8.0',_J,'dewa.gov.example/bayan/dewa-billing-assist',_C,e5w,_A),('tamm-citizen-svc','TAMM citizen services assistant','citizen-assistant','1.4.3',_J,'tamm.gov.example/bayan/tamm-citizen-svc',_C,e5w,_A),('dha-appointment-bot','DHA patient appointment bot','appointment-bot','3.1.0','healthcare','dha.gov.example/bayan/dha-appointment-bot',_C,{_N:['specialty',_K,_O,'clinic_id','diagnosis_code','sud_program_id',_P]},'dha'),('difc-contract-review','DIFC deal-desk contract-review assistant','contract-review','0.9.2','mnpi','difc.example/bayan/difc-contract-review',_C,{_Q:['stage',_K,'counterparty_name','deal_codename','deal_status','sector',_P]},'difc'),('gulfbank-card-assist','Gulf Bank card-services assistant','card-assistant','5.0.1','financial','gulfbank.example/bayan/gulfbank-card-assist','Internal',{_R:['card_brand','decline_code',_K,'branch','pan','cvv']},'bank')]
def seed(cfg:nwp,*,small:bool=_H,log:Any=print)->b8d:
	d='recordId';c='vendor';K=log;E=cfg;D=small;e=time.time();from data.jnf5 import bank_card_events as f,dha_appointments as g,difc_deal_desk as h,itsm_fingerprints as i;from data.jnf5.identifiers import DOC_IDS as j;B=b8d(E);F=B.db
	for(k,L,Q,I,l,m)in bf5r:F.execute('INSERT OR REPLACE INTO principal (id, display_name, role, key_name, key_type, authority, lang) VALUES (?,?,?,?,?,?,?)',(k,L,Q,I,'software',l,m));B.keys.ensure(I,frozenset({_E if Q==_E else'requester'}))
	R=B.keys.get('registry.vendor.example');M=0
	for(A,L,n,o,S,T,p,U,C)in u1if:
		if D and C is _A:continue
		F.execute('INSERT OR REPLACE INTO deployment (id, name, product, version, pack_id, origin, recipient, classification_tier, views) VALUES (?,?,?,?,?,?,?,?,?)',(A,L,n,o,S,T,json.dumps(ovm),p,json.dumps(U)));B.keys.ensure(T,frozenset({'log'}));q=B.packs[S]
		for(V,r)in q.raw['fieldDefaults'].items():W=_A if A==_M and V=='department'else _F;F.execute('INSERT OR REPLACE INTO field_class (deployment_id, field, class, proposed_by, ratified_by, ratified_at) VALUES (?,?,?,?,?,?)',(A,V,r['class'],c,W,int(time.time())if W else _A))
		for X in(_G,'no_show_count','deal_count','decline_count','visit_count',_O):F.execute('INSERT OR IGNORE INTO field_class (deployment_id, field, class, proposed_by, ratified_by, ratified_at) VALUES (?,?,?,?,?,?)',(A,X,'QUASI'if X==_G else'STRUCTURAL',c,_F,int(time.time())))
		G=B.store(A)
		if C=='itsm':
			s=2000 if D else 50000;t=i(n=s,deployment_id=A);J=E.data_dir/'wal'/f"{A}.jsonl"
			if J.exists():J.unlink()
			N=Collector(J);Y={}
			for(Z,a)in t:
				N.emit(Z)
				if a:Y[Z[d]]=a
			N.close();O=N.stats();K(f"  sdk: emitted={O.emitted} dropped={O.dropped} written={O.written}");u=read_wal(J);M+=bnj3(G,[(A,Y.get(A[d]))for A in u]);I=hashlib.sha256(f"enclave-key:{A}".encode()).digest();g742(G,_L,[{_I:hmac.new(I,A.encode(),hashlib.sha256).hexdigest(),_G:A}for A in j])
		elif C=='dha':g742(G,_N,g(600 if D else 3000))
		elif C=='difc':g742(G,_Q,h(400 if D else 1200))
		elif C=='bank':g742(G,_R,f(500 if D else 2500))
		if C:
			for v in sorted((tgd/C).glob('*.json')):H=SkillSpec.from_dict(json.loads(v.read_text()));w=skillreg.sign_bundle(H,R);P=E.data_dir/'inbox'/'skills'/f"{H.name}-{H.version}.bundle";P.parent.mkdir(parents=_B,exist_ok=_B);P.write_text(json.dumps(w));x=skillreg.load_bundle(P,R.public);b=skillreg.register(F,A,x,B.ratified(A),_F,U);K(f"  {A}: {H.name}@{H.version} {b.risk_class} max D{b.max_grade_d}")
	B.keys.trust_root().save(E.data_dir/'trust'/'keys.json');B.events.emit('seed',fingerprints=M,small=D);K(f"seeded {M} fingerprints in {time.time()-e:.1f}s at {E.data_dir}");return B