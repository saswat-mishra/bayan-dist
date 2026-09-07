from __future__ import annotations
_k='complete'
_j='output_schema'
_i='outputSchema'
_h='entry_digest'
_g='rosterEntry'
_f='pack-upgrade'
_e='suspended_leaf'
_d='suspended_reason'
_c='quarter'
_b='%Y-%m-%dT%H:%M:%SZ'
_a='deployment_id'
_Z='status'
_Y='quarantined'
_X='certified_at'
_W='quarantines'
_V='deployment'
_U='pack_id'
_T='provenance'
_S='manifest'
_R='rows'
_Q='max_grade_d'
_P='sha256'
_O=True
_N='suspended_at'
_M='origin'
_L='gate'
_K='quarantine'
_J='decertified'
_I='params'
_H='pack_digest'
_G='requester'
_F='version'
_E='name'
_D='digest'
_C='key_name'
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
from bayan_core.ybvn import dsan
from bayan_core.zm0 import nzm
from bayan_gate import v6y as skillreg
from bayan_gate.xc45 import e3l,nwp
from bayan_gate.xd2 import vwy,n6w
from bayan_gate.bd61 import fc4
from bayan_gate.u7c9 import k6r
from bayan_gate.s4m7 import lvt
from bayan_gate.wvl import czlx,dw2
class u5fa(Exception):
	def __init__(A,status:int,detail:str,**C:Any)->_A:B=detail;super().__init__(B);A.status=status;A.detail=B;A.extra=C
def oy60()->str:return datetime.now(timezone.utc).strftime(_b)
def wos(ts:datetime,kind:str=_c)->str:return f"{ts.year}-Q{(ts.month-1)//3+1}"if kind==_c else f"{ts.year}-{ts.month:02d}"
class b8d:
	def __init__(A,cfg:nwp)->_A:
		F='reviewer';E='role';D='public_key';C=cfg;A.cfg=C;A.fs_type=lvt(C.data_dir);A.db=n6w(C.control_db);A.keys=k6r(C.keys_dir);A.events=fc4(C.audit_log,C.health_file);A.lock=threading.RLock();A.tx=vwy(A.db,A.lock);(A.packs):dict[str,k2x]={A.stem:mfj(A)for A in sorted(e3l.glob('*.json'))};(A.stores):dict[str,sqlite3.Connection]={};(A.ledgers):dict[str,bpsi]={};(A.jobs):dict[str,dict[str,Any]]={}
		for(G,H)in((_L,{_L}),('tsa.vendor.example',{'tsa'}),('registry.vendor.example',{'registry'}),('vendor-disposal',{'vendor'})):A.keys.ensure(G,frozenset(H))
		for B in A.db.execute('SELECT id, origin FROM deployment'):A.keys.ensure(B[_M],frozenset({'log'}))
		for B in A.db.execute('SELECT key_name, role, public_key FROM principal'):
			if B[D]:A.keys.register_public(B[_C],B[D],frozenset({B[E]}))
			elif B[E]not in(F,'sensor'):A.keys.ensure(B[_C],frozenset({_G}))
		for B in A.db.execute('SELECT key_name, public_key FROM key_enrolment WHERE leaf_index IS NOT NULL'):A.keys.register_public(B[_C],B[D],frozenset({F}))
		A.events.emit('startup',data_dir=str(C.data_dir),fs=A.fs_type);from bayan_gate.jyh import ql6f as I;I(A)
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
		if A[_N]is not _A:raise u5fa(423,f"deployment {A[_B]} is suspended: {A[_d]}; a principal with authority must clear it",suspended=_O,leafIndex=A[_e])
	def pack_for(D,dep:sqlite3.Row)->k2x:
		B=dep;A=D.packs[B[_U]];C=B[_H]
		if C and C!=A.digest and not D.pack_upgrade_exists(B,A.digest):raise u5fa(409,f"pack {A.id} changed since onboarding (digest {A.digest[:12]}… != accepted {C[:12]}…); a pack-upgrade signed by a principal with authority is required before grading under it")
		return A
	def deployment_status(C,dep_id:str)->dict[str,Any]:D=dep_id;A=C.deployment(D);B=C.packs[A[_U]];return{_B:D,'pack':{_B:B.id,_F:B.version,_D:B.digest,'accepted':A[_H],'pinned':A[_H]==B.digest or C.pack_upgrade_exists(A,B.digest),'activated':list(B.activated)},'suspended':A[_N]is not _A,'suspension':{'at':A[_N],'reason':A[_d],'leaf':A[_e]}if A[_N]else _A,'acceptance':C._acceptance_summary(D)}
	def _acceptance_summary(D,dep_id:str)->dict[str,Any]|_A:
		B='acceptedBy';A=D.db.execute('SELECT * FROM acceptance WHERE deployment_id=?',(dep_id,)).fetchone()
		if A is _A:return
		C=json.loads(A['document']);return{_D:A[_D],B:A['accepted_by'],'at':C.get(B,{}).get('at'),'components':sorted(A for A in C if A not in('schema',_V,_D,B,'signature'))}
	def pack_upgrade_exists(A,dep:sqlite3.Row,to_digest:str)->bool:from bayan_gate.xb2b import knu as B;return any(A['predicate']['to'][_D][_P]==to_digest for(A,B)in B(A,dep,_f))
	def signers_for(A,p:sqlite3.Row)->list[tuple[str,lfq1]]:B=[(str(p[_C]),A.keys.get(p[_C]))]if A.keys.has(p[_C])else[];return B+[(_L,A.keys.get(_L))]
	def upgrade_pack(B,dep_id:str,actor:str,reason:str)->dict[str,Any]:
		H=reason;G='authority';F=actor;D=dep_id;from bayan_core.blg import kf3 as K;from bayan_core.c339 import olo as L;E=B.principal(F)
		if not E[G]:raise u5fa(403,'only a principal with authority may approve a pack upgrade')
		if len(H.strip())<20:raise u5fa(422,'a pack upgrade needs a typed reason of at least 20 characters')
		C=B.deployment(D);A=B.packs[C[_U]]
		if C[_H]==A.digest:raise u5fa(409,'the pack on disk is already the accepted digest')
		M=L(deployment=D,pack_id=A.id,from_digest=C[_H],to_digest=A.digest,to_version=A.version,approved_by={_B:F,G:E[G],'keyid':E[_C]},reason=H.strip(),at=oy60());N=K(M,B.signers_for(E))
		with B.lock:
			I=B.ledger(C);J=I.append(N.to_bytes());I.checkpoint(C[_M],B.keys.get(C[_M]))
			with B.tx:B.db.execute('UPDATE deployment SET pack_digest=? WHERE id=?',(A.digest,D))
		B.events.emit(_f,deployment=D,pack=A.id,version=A.version,digest=A.digest,leaf=J,by=F);return{_V:D,'pack':A.id,_F:A.version,_D:A.digest,'leafIndex':J}
	def store(A,dep_id:str)->sqlite3.Connection:
		B=dep_id
		if B not in A.stores:A.stores[B]=czlx(A.cfg.fingerprint_db(B))
		return A.stores[B]
	def ledger(B,dep:sqlite3.Row)->bpsi:
		A=dep
		if A[_B]not in B.ledgers:B.ledgers[A[_B]]=bpsi(B.cfg.ledger_dir/A[_B],A[_M])
		return B.ledgers[A[_B]]
	def ratified(A,dep_id:str)->frozenset[str]:return frozenset(A[0]for A in A.db.execute('SELECT field FROM field_class WHERE deployment_id=? AND ratified_by IS NOT NULL',(dep_id,)))
	def recipient_binding(D,dep:sqlite3.Row,requester:str)->dict[str,Any]:
		A=requester;from bayan_gate.ggp6 import a7f as E;B=E(D,dep[_B],A);C:dict[str,Any]={'principal':A}
		if B is not _A:C[_g]={_P:B[_h]}
		return C
	def recipient_extra(C,dep:sqlite3.Row,requester:str)->dict[str,Any]:
		B='employer';from bayan_gate.ggp6 import a7f as D;A=D(C,dep[_B],requester)
		if A is _A:return{}
		return{B:A[B],_g:{_P:A[_h]},'acknowledgement':{_P:A['ack_digest']},'validUntil':datetime.fromtimestamp(A['valid_until'],timezone.utc).strftime(_b)}
	def enclave_key(A,dep_id:str)->bytes:return A.keys.secret(f"enclave-{dep_id}")
	def recipient_facts(E,dep:sqlite3.Row,requester:str|_A=_A,at:int|_A=_A)->c2v:C=requester;from bayan_gate.ggp6 import a7f as F;B=json.loads(dep['recipient']);A=F(E,dep[_B],C,at)if C else _A;G=frozenset(json.loads(A['citizenships']))if A else frozenset();D=frozenset(json.loads(A['residency']))if A else frozenset();return c2v(named_org=bool(B.get('namedOrg')),purpose_limited=bool(B.get('purposeLimited')),named_individuals=A is not _A,attributes_verified=bool(A and A['clearance_checked_at']),onward_transfer_prohibited=bool(B.get('onwardTransferProhibited')),disposal_bound=bool(B.get('disposalBound')),environment_assessed=bool(B.get('environmentAssessed')),on_insider_list=bool(B.get('onInsiderList')),citizenships=G|D,location=A['location']if A else _A,fre502d_order=bool(B.get('fre502dOrder')),export_encryption_carveout=bool(B.get('exportEncryptionCarveout')),roster_valid=A is not _A,residency=D)
	def skills(J,dep_id:str,answers:str|_A=_A)->list[dict[str,Any]]:
		I='example';H='description_ar';G='description';D=answers;C='answers';E=[]
		for A in J.db.execute('SELECT * FROM skill WHERE deployment_id=? ORDER BY name, version',(dep_id,)):
			B=json.loads(A['spec'])
			if D and D not in B.get(C,[]):continue
			F=[A if isinstance(A,dict)else{_E:A}for A in B.get(_I,[])];E.append({_E:A[_E],_F:A[_F],'riskClass':A['risk_class'],'maxGradeD':A[_Q],C:B.get(C,[]),G:B.get(G,''),H:B.get(H,''),_i:json.loads(A[_j]),_I:[A[_E]for A in F],'paramExamples':{A[_E]:A.get(I)for A in F if A.get(I)is not _A},'certified':A[_X]is not _A,'certifiedBy':A['certified_by'],_J:bool(A[_J]),_W:A[_W],'bundleDigest':A['bundle_digest']})
		return E
	def _summaries(B,dep:sqlite3.Row)->list[zdp0]:
		C=dep;G=gra9(B.pack_for(C));D=[]
		for A in B.db.execute('SELECT * FROM skill WHERE deployment_id=? AND decertified=0',(C[_B],)):E=sui.from_dict(json.loads(A['spec']));F=htz(E.output_schema,B.ratified(C[_B]));H=3 if A[_X]is not _A else 2;I=apgg(A[_Q],F,f30(F),G,H);D.append(zdp0(A[_E],A[_F],frozenset(E.answers),A[_Q],I,A[_Q]<=2))
		return D
	def feasibility(D,dep_id:str,qid:str|_A)->list[dict[str,Any]]:
		B=qid;F=D.deployment(dep_id);G=D._summaries(F);H=[A for A in pk09 if B is _A or A.id==B]
		if B is not _A and zos5(B)is _A:raise u5fa(404,f"unknown question {B!r}")
		E=[]
		for A in H:C=gl5(A,G);E.append({'question':A.id,'text':A.text_en,'text_ar':A.text_ar,'minClass':A.min_class,'achievableD':C.achievable_d,'approvalPath':C.approval_path,'realTime':C.real_time,'skills':list(C.skills),'blocked':A.blocked})
		return E
	def run(A,dep_id:str,skill:str,version:str,params:dict[str,Any],requester:str,dryrun:bool=False)->dict[str,Any]:
		O=requester;K=params;H=dryrun;E=dep_id;D=version;C=skill;V=A.deployment(E)
		try:F,L=skillreg.bbl(A.db,E,C,D)
		except KeyError as I:raise u5fa(404,f"unknown skill {C}@{D} for {E}")from I
		except skillreg.zfhh as I:raise u5fa(409,str(I))from I
		if L[_J]:raise u5fa(409,f"{C}@{D} is decertified after {L[_W]} quarantines")
		M=A._synthetic_store()if H else A.store(E);N='synthetic:'+gkou(b'fixtures-v1')if H else dw2(M);P=hndw(F.output_schema.max_rows,A.cfg.skill_timeout_s,A.cfg.skill_heap_bytes);B=mbf(M,F,K,N,P);Q=mbf(M,F,K,N,P)if B.conformant else _A;W=bool(Q and Q.output_digest==B.output_digest);R=htz(F.output_schema,A.ratified(E));S=si1(C,D,_O,_O,L[_X]is not _A,B.conformant,W);T,U=A._certify(V,R,S,O);J=nzm()
		with A.tx:
			G=_A
			if not B.conformant:X,Y=skillreg.l0k(A.db,E,C,D);G={'rule':B.quarantine.rule,'detail':B.quarantine.detail,'count':X,_J:Y}
			A.insert_run(J,E,C,D,O,json.dumps(K),list(B.rows),B.output_digest,N,R,S,T,U,G,H,output_schema=F.output_schema)
		if G:A.events.emit(_K,run=J,skill=f"{C}@{D}",rule=B.quarantine.rule,decertified=G[_J])
		A.events.emit('run',run=J,skill=f"{C}@{D}",status=_Y if G else _k,certificate=T.label,certificate_us=U,dryrun=H);return A.get_run(J)
	def insert_run(B,run_id:str,dep_id:str,skill:str|_A,version:str|_A,requester:str,params:str,rows:list[dict[str,Any]],output_digest:str,input_digest:str,manifest:fil6,prov:si1,cert:bre,us:int,quarantine:dict[str,Any]|_A,dryrun:int|bool,*,output_schema:t2ji,derived_from:str|_A=_A,transform_digest:str|_A=_A)->_A:A=quarantine;B.db.execute('INSERT INTO run (id, deployment_id, skill_name, skill_version, requester, params, status, rows, output_digest, input_digest, manifest, certificate, certificate_us, quarantine, dryrun, provenance, derived_from, transform_digest, output_schema, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(run_id,dep_id,skill,version,requester,params,_Y if A else _k,json.dumps(rows),output_digest,input_digest,json.dumps(q5e8(manifest)),json.dumps(qxd5(cert)),us,json.dumps(A)if A else _A,int(dryrun),json.dumps(w8iy(prov)),derived_from,transform_digest,json.dumps(output_schema.to_dict()),int(time.time())))
	def _certify(A,dep:sqlite3.Row,manifest:fil6,prov:si1,requester:str,reviews:pkj1|_A=_A,prior:bool=False)->tuple[bre,int]:C=requester;B=manifest;D=gra9(A.pack_for(dep));E=f30(B);F=reviews or pkj1(C,policy_cleared=E in D.policy_clear_risk_classes and prov.certified);G=time.perf_counter();H=v5e(B,prov,F,A.recipient_facts(dep,C),D,issued_at=oy60(),matches_prior_cleared_shape=prior);return H,int((time.perf_counter()-G)*1e6)
	def run_row(C,run_id:str)->sqlite3.Row:
		A=run_id;B=C.db.execute('SELECT * FROM run WHERE id=?',(A,)).fetchone()
		if B is _A:raise u5fa(404,f"unknown run {A!r}")
		return B
	def get_run(F,run_id:str)->dict[str,Any]:
		E='dryrun';C='certificate';A=F.run_row(run_id);D=json.loads(A[_R]or'[]');B=json.loads(A[C])if A[C]else _A
		if B and A[_K]:from bayan_core.blg2 import fi7 as G;B['headline']=G(_Y,"Quarantined — the output did not conform to the skill's declared schema. Nothing can be released from this run.",'محجور — المخرجات لم تطابق المخطط المعلن للمهارة. لا يمكن الإفراج عن أي شيء من هذا التشغيل.').to_json()
		return{_B:A[_B],_V:A[_a],'skill':A['skill_name'],_F:A['skill_version'],_Z:A[_Z],_G:A[_G],_I:json.loads(A[_I]),'outputRef':{_R:len(D),_D:A['output_digest'],'inputDigest':A['input_digest']},_R:D[:500],C:B,'certificateMicros':A['certificate_us'],_K:json.loads(A[_K])if A[_K]else _A,E:bool(A[E]),_S:json.loads(A[_S]),_T:json.loads(A[_T]),'derivedFrom':A['derived_from'],'transformDigest':A['transform_digest'],_i:json.loads(A[_j])}
	def uplift_menu(B,run_id:str,target:int)->dict[str,Any]:E='recommended';C=B.run_row(run_id);D=B.deployment(C[_a]);F=vf4(json.loads(C[_S]));G=3 if gowu(json.loads(C[_T])).certified else 2;A=dsan(F,target,gra9(B.pack_for(D)),B.recipient_facts(D,C[_G]),G);return{'target':f"D{A.target_d}",'current':f"D{A.current_d}",'asyncRequired':A.async_required,'unreachableReason':A.unreachable_reason,'options':[{'changes':[{'field':A.field,'transform':A.transform.value,_I:dict(A.params)}for A in A.changes],'describe':A.describe(),'reachesTarget':A.reaches_target,'d':f"D{A.d}",'requiredR':f"R{A.required_r}",'cost':A.cost,'loses':list(A.loses),'keeps':A.keeps,E:A.recommended}for A in A.options],E:A.recommended.describe()if A.recommended else _A}
	def apply_uplift(A,run_id:str,option_index:int,requester:str)->dict[str,Any]:from bayan_gate.o432 import mvle as B;return B(A,run_id,option_index,requester)
	def upgrade_d3(A,run_id:str)->dict[str,Any]:
		D=run_id;from bayan_core.blg2.k8uj import crt3 as J,h830 as K;B=A.run_row(D);C=nzm();A.jobs[C]={_B:C,'run':D,_Z:'running','estimate_s':1}
		def E()->_A:
			I='min_cell';time.sleep(.05)
			with A.tx:L=A.deployment(B[_a]);M=json.loads(B[_R]or'[]');E=vf4(json.loads(B[_S]));F=[K(M,A.name,int(A.param(I)),oy60())for A in E.fields if A.param(I)is not _A];G=J(E,F);N=gowu(json.loads(B[_T]));H,O=A._certify(L,G,N,B[_G]);A.db.execute('UPDATE run SET certificate=?, manifest=? WHERE id=?',(json.dumps(qxd5(H)),json.dumps(q5e8(G)),D));A.jobs[C].update(status='done',certificate=H.label,properties=[{_E:A.name,'threshold':A.threshold,'observed':A.observed,'passed':A.passed}for A in F])
		threading.Thread(target=E,daemon=_O).start();return dict(A.jobs[C])
	def _synthetic_store(F)->sqlite3.Connection:C='doc_ref';B='record_id';A=sqlite3.connect(':memory:');D=['pension','leave','payroll','it-access','housing'];E=[{B:f"SYN{A:06d}",'ts_hour':f"2026-08-{1+A%28:02d}T{A%24:02d}:00:00Z",'week':f"2026-W{31+A%28//7}",'tier':1,'operation':'chat','topic':D[A%5],'route':'ingress>retrieve>generate','finish_reason':'stop','error_code':'none'if A%3 else'retrieval_empty','latency_bucket':'1s-5s','latency_ms':_A,'input_bucket':'257-1k','output_bucket':'65-256','input_exact':_A,'output_exact':_A,'hit_count':A%6,'doc_ref_count':A%3,'guardrail_tripped':0,'guardrail_category':_A,'confidence':_A,'tool_name':_A,'conversation_id':_A,'index_generation':1,'prompt_version':'0'*64,'model_version':'1'*64,'product_version':'0.0'}for A in range(2000)];ewsp(A,{'fingerprints':E,'doc_refs':[{B:f"SYN{A:06d}",C:f"{A%7:064x}",'rank':1}for A in range(2000)],'doc_index':[{C:f"{A:064x}",'doc_id':f"SYN-DOC-{A}"}for A in range(7)]});return A
	def create_request(A,dep_id:str,requester:str,purpose:str,mechanism:str,run_id:str|_A=_A,record_id:str|_A=_A,retention:str|_A=_A,sensitive_declared:list[str]|_A=_A)->dict[str,Any]:
		from bayan_gate.ubk1 import euh9 as B
		with A.lock:return B(A,dep_id,requester,purpose,mechanism,run_id,record_id,retention,sensitive_declared or[])
	def _finalize(A,rid:str,outcome:str,human_reviews:list[dict[str,Any]],actor:str)->dict[str,Any]:
		from bayan_gate.cwm import hkl as B
		with A.lock:return B(A,rid,outcome,human_reviews,actor)
	def get_request(A,rid:str,viewer:str)->dict[str,Any]:from bayan_gate.ubk1 import ep8 as B;return B(A,rid,viewer)
	def budget(H,dep_id:str,cohort:str|_A)->list[dict[str,Any]]:G='limit_n';F='disjoint';E='period';D='cohort';C='reserved';B='consumed';A=cohort;I='SELECT * FROM budget WHERE cohort LIKE ?'+(' AND cohort=?'if A else'');J=(f"{dep_id}:%",)+((A,)if A else());return[{D:A[D],E:A[E],B:A[B],C:A[C],'limit':A[G],'remaining':A[G]-A[B]-A[C],F:bool(A[F])}for A in H.db.execute(I,J)]
