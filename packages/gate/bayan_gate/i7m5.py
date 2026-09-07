from __future__ import annotations
_l='complete'
_k='quarantined'
_j='output_schema'
_i='outputSchema'
_h='entry_digest'
_g='rosterEntry'
_f='pack-upgrade'
_e='suspended_leaf'
_d='suspended_reason'
_c='quarter'
_b='deployment_id'
_a='status'
_Z='quarantines'
_Y=False
_X='deployment'
_W='pack_id'
_V='%Y-%m-%dT%H:%M:%SZ'
_U='provenance'
_T='manifest'
_S='rows'
_R='max_grade_d'
_Q='sha256'
_P=True
_O='suspended_at'
_N='origin'
_M='gate'
_L='quarantine'
_K='decertified'
_J='params'
_I='pack_digest'
_H='requester'
_G='certified_at'
_F='version'
_E='digest'
_D='key_name'
_C='name'
_B='id'
_A=None
import json,sqlite3,threading,time
from datetime import datetime,timezone
from typing import Any
from bayan_core.blg import lfq1,gkou
from bayan_core.blg2 import bre,fil6,si1,c2v,pkj1,qxd5,v5e
from bayan_core.blg2.otu import vf4,q5e8,gowu,w8iy
from bayan_core.blg2.oj2 import f30
from bayan_core.blg2.v7w import pk09,zdp0,gl5,zos5
from bayan_core.blg2.nf3 import apgg
from bayan_core.v2s import bpsi
from bayan_core.s7t3 import k2x,mfj,gra9
from bayan_core.evxn import hndw,t2ji,sui,ewsp,mbf,htz
from bayan_core.schema.g5v import c5aj
from bayan_core.ybvn import dsan
from bayan_core.zm0 import nzm
from bayan_gate import v6y as skillreg
from bayan_gate.xc45 import e3l,nwp
from bayan_gate.xd2 import vwy,n6w
from bayan_gate.bd61 import fc4
from bayan_gate.u7c9 import k6r
from bayan_gate.s4m7 import lvt,jbg
from bayan_gate.wvl import czlx,dw2
class u5fa(Exception):
	def __init__(A,status:int,detail:str,**C:Any)->_A:B=detail;super().__init__(B);A.status=status;A.detail=B;A.extra=C
def oy60()->str:return datetime.now(timezone.utc).strftime(_V)
def wos(ts:datetime,kind:str=_c)->str:return f"{ts.year}-Q{(ts.month-1)//3+1}"if kind==_c else f"{ts.year}-{ts.month:02d}"
class b8d:
	def __init__(A,cfg:nwp)->_A:
		F='reviewer';E='role';D='public_key';C=cfg;A.cfg=C;A.fs_type=lvt(C.data_dir);A.db=n6w(C.control_db);G=jbg(A.db);A.keys=k6r(C.keys_dir);A.events=fc4(C.audit_log,C.health_file);A.lock=threading.RLock();A.tx=vwy(A.db,A.lock);(A.packs):dict[str,k2x]={A.stem:mfj(A)for A in sorted(e3l.glob('*.json'))};(A.stores):dict[str,sqlite3.Connection]={};(A.ledgers):dict[str,bpsi]={};(A.jobs):dict[str,dict[str,Any]]={}
		for(H,I)in((_M,{_M}),('tsa.vendor.example',{'tsa'}),('registry.vendor.example',{'registry'}),('vendor-disposal',{'vendor'})):A.keys.ensure(H,frozenset(I))
		for B in A.db.execute('SELECT id, origin FROM deployment'):A.keys.ensure(B[_N],frozenset({'log'}))
		for B in A.db.execute('SELECT key_name, role, public_key FROM principal'):
			if B[D]:A.keys.register_public(B[_D],B[D],frozenset({B[E]}))
			elif B[E]not in(F,'sensor'):A.keys.ensure(B[_D],frozenset({_H}))
		for B in A.db.execute('SELECT key_name, public_key FROM key_enrolment WHERE leaf_index IS NOT NULL'):A.keys.register_public(B[_D],B[D],frozenset({F}))
		A.events.emit('startup',data_dir=str(C.data_dir),fs=A.fs_type,migratedRoles=G);from bayan_gate.jyh import ql6f as J;J(A)
	def principal(B,user:str)->sqlite3.Row:
		A=B.db.execute('SELECT * FROM principal WHERE id=?',(user,)).fetchone()
		if A is _A:raise u5fa(401,f"unknown principal {user!r}")
		return A
	def deployment(B,dep:str)->sqlite3.Row:
		A=B.db.execute('SELECT * FROM deployment WHERE id=?',(dep,)).fetchone()
		if A is _A:raise u5fa(404,f"unknown deployment {dep!r}")
		return A
	def assert_not_suspended(B,dep:sqlite3.Row)->_A:
		A=dep
		if A[_O]is not _A:raise u5fa(423,f"deployment {A[_B]} is suspended: {A[_d]}; a principal with authority must clear it",suspended=_P,leafIndex=A[_e])
	def pack_for(D,dep:sqlite3.Row)->k2x:
		B=dep;A=D.packs[B[_W]];C=B[_I]
		if C and C!=A.digest and not D.pack_upgrade_exists(B,A.digest):raise u5fa(409,f"pack {A.id} changed since onboarding (digest {A.digest[:12]}… != accepted {C[:12]}…); a pack-upgrade signed by a principal with authority is required before grading under it")
		return A
	def deployment_status(C,dep_id:str)->dict[str,Any]:F='clientLogRetention';E='vendorDisposal';D=dep_id;A=C.deployment(D);B=C.packs[A[_W]];return{_B:D,'pack':{_B:B.id,_F:B.version,_E:B.digest,'accepted':A[_I],'pinned':A[_I]==B.digest or C.pack_upgrade_exists(A,B.digest),'activated':list(B.activated)},'suspended':A[_O]is not _A,'suspension':{'at':A[_O],'reason':A[_d],'leaf':A[_e]}if A[_O]else _A,'acceptance':C._acceptance_summary(D),'trustDir':str(C.cfg.data_dir/'trust'),'outboxDir':str(C.cfg.outbox_dir),'retention':{E:B.retention.get(E,'P90D'),F:B.retention.get(F)},'primaryFramework':B.primary_framework,'nameAr':A['name_ar']or A[_C],_C:A[_C]}
	def _acceptance_summary(D,dep_id:str)->dict[str,Any]|_A:
		B='acceptedBy';A=D.db.execute('SELECT * FROM acceptance WHERE deployment_id=?',(dep_id,)).fetchone()
		if A is _A:return
		C=json.loads(A['document']);return{_E:A[_E],B:A['accepted_by'],'at':C.get(B,{}).get('at'),'components':sorted(A for A in C if A not in('schema',_X,_E,B,'signature'))}
	def pack_upgrade_exists(A,dep:sqlite3.Row,to_digest:str)->bool:from bayan_gate.xb2b import knu as B;return any(A['predicate']['to'][_E][_Q]==to_digest for(A,B)in B(A,dep,_f))
	def signers_for(A,p:sqlite3.Row)->list[tuple[str,lfq1]]:B=[(str(p[_D]),A.keys.get(p[_D]))]if A.keys.has(p[_D])else[];return B+[(_M,A.keys.get(_M))]
	def upgrade_pack(B,dep_id:str,actor:str,reason:str)->dict[str,Any]:
		H=reason;G='authority';F=actor;D=dep_id;from bayan_core.blg import kf3 as K;from bayan_core.c339 import olo as L;E=B.principal(F)
		if not E[G]:raise u5fa(403,'only a principal with authority may approve a pack upgrade')
		if len(H.strip())<20:raise u5fa(422,'a pack upgrade needs a typed reason of at least 20 characters')
		C=B.deployment(D);A=B.packs[C[_W]]
		if C[_I]==A.digest:raise u5fa(409,'the pack on disk is already the accepted digest')
		M=L(deployment=D,pack_id=A.id,from_digest=C[_I],to_digest=A.digest,to_version=A.version,approved_by={_B:F,G:E[G],'keyid':E[_D]},reason=H.strip(),at=oy60());N=K(M,B.signers_for(E))
		with B.lock:
			I=B.ledger(C);J=I.append(N.to_bytes());I.checkpoint(C[_N],B.keys.get(C[_N]))
			with B.tx:B.db.execute('UPDATE deployment SET pack_digest=? WHERE id=?',(A.digest,D))
		B.events.emit(_f,deployment=D,pack=A.id,version=A.version,digest=A.digest,leaf=J,by=F);return{_X:D,'pack':A.id,_F:A.version,_E:A.digest,'leafIndex':J}
	def store(A,dep_id:str)->sqlite3.Connection:
		B=dep_id
		if B not in A.stores:A.stores[B]=czlx(A.cfg.fingerprint_db(B))
		return A.stores[B]
	def ledger(B,dep:sqlite3.Row)->bpsi:
		A=dep
		if A[_B]not in B.ledgers:B.ledgers[A[_B]]=bpsi(B.cfg.ledger_dir/A[_B],A[_N])
		return B.ledgers[A[_B]]
	def ratified(A,dep_id:str)->frozenset[str]:return frozenset(A[0]for A in A.db.execute('SELECT field FROM field_class WHERE deployment_id=? AND ratified_by IS NOT NULL',(dep_id,)))
	def field_classes(A,dep_id:str)->dict[str,c5aj]:return{A['field']:c5aj(A['class'])for A in A.db.execute('SELECT field, class FROM field_class WHERE deployment_id=? AND ratified_by IS NOT NULL',(dep_id,))}
	def recipient_binding(D,dep:sqlite3.Row,requester:str)->dict[str,Any]:
		A=requester;from bayan_gate.ggp6 import a7f as E;B=E(D,dep[_B],A);C:dict[str,Any]={'principal':A}
		if B is not _A:C[_g]={_Q:B[_h]}
		return C
	def recipient_extra(C,dep:sqlite3.Row,requester:str)->dict[str,Any]:
		B='employer';from bayan_gate.ggp6 import a7f as D;A=D(C,dep[_B],requester)
		if A is _A:return{}
		return{B:A[B],_g:{_Q:A[_h]},'acknowledgement':{_Q:A['ack_digest']},'validUntil':datetime.fromtimestamp(A['valid_until'],timezone.utc).strftime(_V)}
	def enclave_key(A,dep_id:str)->bytes:return A.keys.secret(f"enclave-{dep_id}")
	def recipient_facts(E,dep:sqlite3.Row,requester:str|_A=_A,at:int|_A=_A)->c2v:C=requester;from bayan_gate.ggp6 import a7f as F;B=json.loads(dep['recipient']);A=F(E,dep[_B],C,at)if C else _A;G=frozenset(json.loads(A['citizenships']))if A else frozenset();D=frozenset(json.loads(A['residency']))if A else frozenset();return c2v(named_org=bool(B.get('namedOrg')),purpose_limited=bool(B.get('purposeLimited')),named_individuals=A is not _A,attributes_verified=bool(A and A['clearance_checked_at']),onward_transfer_prohibited=bool(B.get('onwardTransferProhibited')),disposal_bound=bool(B.get('disposalBound')),environment_assessed=bool(B.get('environmentAssessed')),on_insider_list=bool(B.get('onInsiderList')),citizenships=G|D,location=A['location']if A else _A,fre502d_order=bool(B.get('fre502dOrder')),export_encryption_carveout=bool(B.get('exportEncryptionCarveout')),roster_valid=A is not _A,residency=D)
	def skills(C,dep_id:str,answers:str|_A=_A,awaiting:bool=_Y)->list[dict[str,Any]]:
		K='example';J='description_ar';I='description';F=answers;E='answers';D=dep_id;from bayan_core.evxn import l0zv as L;M,N=C.ratified(D),C.field_classes(D);G=[]
		for A in C.db.execute('SELECT * FROM skill WHERE deployment_id=? ORDER BY name, version',(D,)):
			B=json.loads(A['spec'])
			if F and F not in B.get(E,[]):continue
			if awaiting and A[_G]is not _A:continue
			H=[A if isinstance(A,dict)else{_C:A}for A in B.get(_J,[])];O=L(sui.from_dict(B),M,classes=N).cap_reasons;G.append({_C:A[_C],_F:A[_F],'riskClass':A['risk_class'],'maxGradeD':A[_R],'capReasons':[A.to_json()for A in O],E:B.get(E,[]),I:B.get(I,''),J:B.get(J,''),_i:json.loads(A[_j]),_J:[A[_C]for A in H],'paramExamples':{A[_C]:A.get(K)for A in H if A.get(K)is not _A},'certified':A[_G]is not _A,'certifiedBy':A['certified_by'],'certifiedAt':time.strftime(_V,time.gmtime(A[_G]))if A[_G]else _A,_K:bool(A[_K]),_Z:A[_Z],'bundleDigest':A['bundle_digest']})
		return G
	def _summaries(B,dep:sqlite3.Row)->list[zdp0]:
		C=dep;G=gra9(B.pack_for(C));D=[]
		for A in B.db.execute('SELECT * FROM skill WHERE deployment_id=? AND decertified=0',(C[_B],)):E=sui.from_dict(json.loads(A['spec']));F=htz(E.output_schema,B.ratified(C[_B]),classes=B.field_classes(C[_B]));H=3 if A[_G]is not _A else 2;I=apgg(A[_R],F,f30(F),G,H);D.append(zdp0(A[_C],A[_F],frozenset(E.answers),A[_R],I,A[_R]<=2))
		return D
	def feasibility(D,dep_id:str,qid:str|_A)->list[dict[str,Any]]:
		B=qid;F=D.deployment(dep_id);G=D._summaries(F);H=[A for A in pk09 if B is _A or A.id==B]
		if B is not _A and zos5(B)is _A:raise u5fa(404,f"unknown question {B!r}")
		E=[]
		for A in H:C=gl5(A,G);E.append({'question':A.id,'text':A.text_en,'text_ar':A.text_ar,'minClass':A.min_class,'minClass_ar':A.min_class_ar,'achievableD':C.achievable_d,'approvalPath':C.approval_path,'realTime':C.real_time,'skills':list(C.skills),'blocked':A.blocked})
		return E
	def run(A,dep_id:str,skill:str,version:str,params:dict[str,Any],requester:str,dryrun:bool=_Y)->dict[str,Any]:
		O=requester;K=params;H=dryrun;E=version;D=skill;C=dep_id;V=A.deployment(C)
		try:F,L=skillreg.bbl(A.db,C,D,E)
		except KeyError as I:raise u5fa(404,f"unknown skill {D}@{E} for {C}")from I
		except skillreg.zfhh as I:raise u5fa(409,str(I))from I
		if L[_K]:raise u5fa(409,f"{D}@{E} is decertified after {L[_Z]} quarantines")
		M=A._synthetic_store()if H else A.store(C);N='synthetic:'+gkou(b'fixtures-v1')if H else dw2(M);P=hndw(F.output_schema.max_rows,A.cfg.skill_timeout_s,A.cfg.skill_heap_bytes);B=mbf(M,F,K,N,P);Q=mbf(M,F,K,N,P)if B.conformant else _A;W=bool(Q and Q.output_digest==B.output_digest);R=htz(F.output_schema,A.ratified(C),classes=A.field_classes(C));S=si1(D,E,_P,_P,L[_G]is not _A,B.conformant,W);T,U=A._certify(V,R,S,O);J=nzm()
		with A.tx:
			G=_A
			if not B.conformant:X,Y=skillreg.l0k(A.db,C,D,E);G={'rule':B.quarantine.rule,'detail':B.quarantine.detail,'count':X,_K:Y}
			A.insert_run(J,C,D,E,O,json.dumps(K),list(B.rows),B.output_digest,N,R,S,T,U,G,H,output_schema=F.output_schema)
		if G:A.events.emit(_L,run=J,skill=f"{D}@{E}",rule=B.quarantine.rule,decertified=G[_K])
		A.events.emit('run',run=J,skill=f"{D}@{E}",status=_k if G else _l,certificate=T.label,certificate_us=U,dryrun=H);return A.get_run(J)
	def insert_run(C,run_id:str,dep_id:str,skill:str|_A,version:str|_A,requester:str,params:str,rows:list[dict[str,Any]],output_digest:str,input_digest:str,manifest:fil6,prov:si1,cert:bre,us:int,quarantine:dict[str,Any]|_A,dryrun:int|bool,*,output_schema:t2ji,derived_from:str|_A=_A,transform_digest:str|_A=_A,lookup:dict[str,Any]|_A=_A)->_A:B=lookup;A=quarantine;C.db.execute('INSERT INTO run (id, deployment_id, skill_name, skill_version, requester, params, status, rows, output_digest, input_digest, manifest, certificate, certificate_us, quarantine, dryrun, provenance, derived_from, transform_digest, output_schema, created_at, lookup) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(run_id,dep_id,skill,version,requester,params,_k if A else _l,json.dumps(rows),output_digest,input_digest,json.dumps(q5e8(manifest)),json.dumps(qxd5(cert)),us,json.dumps(A)if A else _A,int(dryrun),json.dumps(w8iy(prov)),derived_from,transform_digest,json.dumps(output_schema.to_dict()),int(time.time()),json.dumps(B)if B else _A))
	def _certify(A,dep:sqlite3.Row,manifest:fil6,prov:si1,requester:str,reviews:pkj1|_A=_A,prior:bool=_Y)->tuple[bre,int]:C=requester;B=manifest;D=gra9(A.pack_for(dep));E=f30(B);F=reviews or pkj1(C,policy_cleared=E in D.policy_clear_risk_classes and prov.certified);G=time.perf_counter();H=v5e(B,prov,F,A.recipient_facts(dep,C),D,issued_at=oy60(),matches_prior_cleared_shape=prior);return H,int((time.perf_counter()-G)*1e6)
	def run_row(C,run_id:str)->sqlite3.Row:
		A=run_id;B=C.db.execute('SELECT * FROM run WHERE id=?',(A,)).fetchone()
		if B is _A:raise u5fa(404,f"unknown run {A!r}")
		return B
	def get_run(G,run_id:str)->dict[str,Any]:
		F='dryrun';D='lookup';C='certificate';A=G.run_row(run_id);E=json.loads(A[_S]or'[]');B=json.loads(A[C])if A[C]else _A
		if B and A[_L]:from bayan_core.blg2.uq2 import nypa as H;B['headline']=H.to_json()
		return{_B:A[_B],_X:A[_b],'skill':A['skill_name'],_F:A['skill_version'],_a:A[_a],_H:A[_H],_J:json.loads(A[_J]),'outputRef':{_S:len(E),_E:A['output_digest'],'inputDigest':A['input_digest']},_S:E[:500],C:B,'certificateMicros':A['certificate_us'],_L:json.loads(A[_L])if A[_L]else _A,F:bool(A[F]),_T:json.loads(A[_T]),_U:json.loads(A[_U]),'derivedFrom':A['derived_from'],'transformDigest':A['transform_digest'],_i:json.loads(A[_j]),D:json.loads(A[D])if A[D]else _A}
	def uplift_menu(B,run_id:str,target:int)->dict[str,Any]:E='recommended';C=B.run_row(run_id);D=B.deployment(C[_b]);F=vf4(json.loads(C[_T]));G=3 if gowu(json.loads(C[_U])).certified else 2;A=dsan(F,target,gra9(B.pack_for(D)),B.recipient_facts(D,C[_H]),G);return{'target':f"D{A.target_d}",'current':f"D{A.current_d}",'asyncRequired':A.async_required,'unreachableReason':A.unreachable_reason,'options':[{'changes':[{'field':A.field,'transform':A.transform.value,_J:dict(A.params)}for A in A.changes],'describe':A.describe(),'reachesTarget':A.reaches_target,'d':f"D{A.d}",'requiredR':f"R{A.required_r}",'cost':A.cost,'loses':list(A.loses),'keeps':A.keeps,E:A.recommended}for A in A.options],E:A.recommended.describe()if A.recommended else _A}
	def apply_uplift(A,run_id:str,option_index:int,requester:str)->dict[str,Any]:from bayan_gate.o432 import mvle as B;return B(A,run_id,option_index,requester)
	def upgrade_d3(A,run_id:str)->dict[str,Any]:
		D=run_id;from bayan_core.blg2.k8uj import crt3 as J,h830 as K;B=A.run_row(D);C=nzm();A.jobs[C]={_B:C,'run':D,_a:'running','estimate_s':1}
		def E()->_A:
			I='min_cell';time.sleep(.05)
			with A.tx:L=A.deployment(B[_b]);M=json.loads(B[_S]or'[]');E=vf4(json.loads(B[_T]));F=[K(M,A.name,int(A.param(I)),oy60())for A in E.fields if A.param(I)is not _A];G=J(E,F);N=gowu(json.loads(B[_U]));H,O=A._certify(L,G,N,B[_H]);A.db.execute('UPDATE run SET certificate=?, manifest=? WHERE id=?',(json.dumps(qxd5(H)),json.dumps(q5e8(G)),D));A.jobs[C].update(status='done',certificate=H.label,properties=[{_C:A.name,'threshold':A.threshold,'observed':A.observed,'passed':A.passed}for A in F])
		threading.Thread(target=E,daemon=_P).start();return dict(A.jobs[C])
	def _synthetic_store(F)->sqlite3.Connection:C='doc_ref';B='record_id';A=sqlite3.connect(':memory:');D=['pension','leave','payroll','it-access','housing'];E=[{B:f"SYN{A:06d}",'ts_hour':f"2026-08-{1+A%28:02d}T{A%24:02d}:00:00Z",'week':f"2026-W{31+A%28//7}",'tier':1,'operation':'chat','topic':D[A%5],'route':'ingress>retrieve>generate','finish_reason':'stop','error_code':'none'if A%3 else'retrieval_empty','latency_bucket':'1s-5s','latency_ms':_A,'input_bucket':'257-1k','output_bucket':'65-256','input_exact':_A,'output_exact':_A,'hit_count':A%6,'doc_ref_count':A%3,'guardrail_tripped':0,'guardrail_category':_A,'confidence':_A,'tool_name':_A,'conversation_id':_A,'index_generation':1,'prompt_version':'0'*64,'model_version':'1'*64,'product_version':'0.0'}for A in range(2000)];ewsp(A,{'fingerprints':E,'doc_refs':[{B:f"SYN{A:06d}",C:f"{A%7:064x}",'rank':1}for A in range(2000)],'doc_index':[{C:f"{A:064x}",'doc_id':f"SYN-DOC-{A}"}for A in range(7)]});return A
	def create_request(A,dep_id:str,requester:str,purpose:str,mechanism:str,run_id:str|_A=_A,record_id:str|_A=_A,retention:str|_A=_A,sensitive_declared:list[str]|_A=_A,lookup:dict[str,Any]|_A=_A)->dict[str,Any]:
		from bayan_gate.ubk1 import euh9 as B
		with A.lock:return B(A,dep_id,requester,purpose,mechanism,run_id,record_id,retention,sensitive_declared or[],lookup)
	def _finalize(A,rid:str,outcome:str,human_reviews:list[dict[str,Any]],actor:str)->dict[str,Any]:
		from bayan_gate.cwm import hkl as B
		with A.lock:return B(A,rid,outcome,human_reviews,actor)
	def get_request(A,rid:str,viewer:str)->dict[str,Any]:from bayan_gate.ubk1 import ep8 as B;return B(A,rid,viewer)
	def budget(H,dep_id:str,cohort:str|_A)->list[dict[str,Any]]:G='limit_n';F='disjoint';E='period';D='cohort';C='reserved';B='consumed';A=cohort;I='SELECT * FROM budget WHERE cohort LIKE ?'+(' AND cohort=?'if A else'');J=(f"{dep_id}:%",)+((A,)if A else());return[{D:A[D],E:A[E],B:A[B],C:A[C],'limit':A[G],'remaining':A[G]-A[B]-A[C],F:bool(A[F])}for A in H.db.execute(I,J)]
