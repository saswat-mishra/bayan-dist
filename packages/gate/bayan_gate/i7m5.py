from __future__ import annotations
_v='recommendation'
_u='reachesTarget'
_t='changes'
_s='describe'
_r='quarantined'
_q='output_schema'
_p='outputSchema'
_o='entry_digest'
_n='rosterEntry'
_m='fieldDefaults'
_l='pack-upgrade'
_k='suspended_leaf'
_j='suspended_reason'
_i='quarter'
_h='deployment_id'
_g='complete'
_f='requiredR'
_e='quarantines'
_d='transform'
_c=False
_b='tags'
_a='deployment'
_Z='%Y-%m-%dT%H:%M:%SZ'
_Y='status'
_X='rows'
_W='provenance'
_V='manifest'
_U='max_grade_d'
_T='class'
_S='sha256'
_R=True
_Q='suspended_at'
_P='origin'
_O='gate'
_N='quarantine'
_M='decertified'
_L='pack_digest'
_K='pack_id'
_J='requester'
_I='params'
_H='certified_at'
_G='field'
_F='digest'
_E='version'
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
from bayan_core.evxn import hndw,t2ji,sui,ewsp,mbf
from bayan_core.schema.g5v import c5aj
from bayan_core.ybvn import n4y,dsan
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
def oy60()->str:return datetime.now(timezone.utc).strftime(_Z)
def wos(ts:datetime,kind:str=_i)->str:return f"{ts.year}-Q{(ts.month-1)//3+1}"if kind==_i else f"{ts.year}-{ts.month:02d}"
class b8d:
	def __init__(A,cfg:nwp)->_A:
		F='reviewer';E='role';D='public_key';C=cfg;A.cfg=C;A.fs_type=lvt(C.data_dir);A.db=n6w(C.control_db);G=jbg(A.db);A.keys=k6r(C.keys_dir);A.events=fc4(C.audit_log,C.health_file);A.lock=threading.RLock();A.tx=vwy(A.db,A.lock);(A.packs):dict[str,k2x]={A.stem:mfj(A)for A in sorted(e3l.glob('*.json'))};(A.stores):dict[str,sqlite3.Connection]={};(A.ledgers):dict[str,bpsi]={};(A.jobs):dict[str,dict[str,Any]]={}
		for(H,I)in((_O,{_O}),('tsa.vendor.example',{'tsa'}),('registry.vendor.example',{'registry'}),('vendor-disposal',{'vendor'})):A.keys.ensure(H,frozenset(I))
		for B in A.db.execute('SELECT id, origin FROM deployment'):A.keys.ensure(B[_P],frozenset({'log'}))
		for B in A.db.execute('SELECT key_name, role, public_key FROM principal'):
			if B[D]:A.keys.register_public(B[_D],B[D],frozenset({B[E]}))
			elif B[E]not in(F,'sensor'):A.keys.ensure(B[_D],frozenset({_J}))
		for B in A.db.execute('SELECT key_name, public_key FROM key_enrolment WHERE leaf_index IS NOT NULL'):A.keys.register_public(B[_D],B[D],frozenset({F}))
		A.events.emit('startup',data_dir=str(C.data_dir),fs=A.fs_type,migratedRoles=G);from bayan_gate.jyh import ql6f as J;J(A)
	def close(A)->_A:
		for B in list(A.stores.values()):
			try:B.close()
			except sqlite3.Error:0
		A.stores.clear()
		try:A.db.close()
		except sqlite3.Error:0
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
		if A[_Q]is not _A:raise u5fa(423,f"deployment {A[_B]} is suspended: {A[_j]}; a principal with authority must clear it",suspended=_R,leafIndex=A[_k])
	def pack_for(D,dep:sqlite3.Row)->k2x:
		B=dep;A=D.packs[B[_K]];C=B[_L]
		if C and C!=A.digest and not D.pack_upgrade_exists(B,A.digest):raise u5fa(409,f"pack {A.id} changed since onboarding (digest {A.digest[:12]}… != accepted {C[:12]}…); a pack-upgrade signed by a principal with authority is required before grading under it")
		return A
	def deployment_status(C,dep_id:str)->dict[str,Any]:F='clientLogRetention';E='vendorDisposal';D=dep_id;A=C.deployment(D);B=C.packs[A[_K]];return{_B:D,'pack':{_B:B.id,_E:B.version,_F:B.digest,'accepted':A[_L],'pinned':A[_L]==B.digest or C.pack_upgrade_exists(A,B.digest),'activated':list(B.activated)},'suspended':A[_Q]is not _A,'suspension':{'at':A[_Q],'reason':A[_j],'leaf':A[_k]}if A[_Q]else _A,'acceptance':C._acceptance_summary(D),'trustDir':str(C.cfg.data_dir/'trust'),'outboxDir':str(C.cfg.outbox_dir),'retention':{E:B.retention.get(E,'P90D'),F:B.retention.get(F)},'primaryFramework':B.primary_framework,'nameAr':A['name_ar']or A[_C],_C:A[_C]}
	def _acceptance_summary(D,dep_id:str)->dict[str,Any]|_A:
		B='acceptedBy';A=D.db.execute('SELECT * FROM acceptance WHERE deployment_id=?',(dep_id,)).fetchone()
		if A is _A:return
		C=json.loads(A['document']);return{_F:A[_F],B:A['accepted_by'],'at':C.get(B,{}).get('at'),'components':sorted(A for A in C if A not in('schema',_a,_F,B,'signature'))}
	def pack_upgrade_exists(A,dep:sqlite3.Row,to_digest:str)->bool:from bayan_gate.xb2b import knu as B;return any(A['predicate']['to'][_F][_S]==to_digest for(A,B)in B(A,dep,_l))
	def signers_for(A,p:sqlite3.Row)->list[tuple[str,lfq1]]:B=[(str(p[_D]),A.keys.get(p[_D]))]if A.keys.has(p[_D])else[];return B+[(_O,A.keys.get(_O))]
	def upgrade_pack(B,dep_id:str,actor:str,reason:str)->dict[str,Any]:
		H=reason;G='authority';F=actor;D=dep_id;from bayan_core.blg import kf3 as K;from bayan_core.c339 import olo as L;E=B.principal(F)
		if not E[G]:raise u5fa(403,'only a principal with authority may approve a pack upgrade')
		if len(H.strip())<20:raise u5fa(422,'a pack upgrade needs a typed reason of at least 20 characters')
		C=B.deployment(D);A=B.packs[C[_K]]
		if C[_L]==A.digest:raise u5fa(409,'the pack on disk is already the accepted digest')
		M=L(deployment=D,pack_id=A.id,from_digest=C[_L],to_digest=A.digest,to_version=A.version,approved_by={_B:F,G:E[G],'keyid':E[_D]},reason=H.strip(),at=oy60());N=K(M,B.signers_for(E))
		with B.lock:
			I=B.ledger(C);J=I.append(N.to_bytes());I.checkpoint(C[_P],B.keys.get(C[_P]))
			with B.tx:B.db.execute('UPDATE deployment SET pack_digest=? WHERE id=?',(A.digest,D))
		B.events.emit(_l,deployment=D,pack=A.id,version=A.version,digest=A.digest,leaf=J,by=F);return{_a:D,'pack':A.id,_E:A.version,_F:A.digest,'leafIndex':J}
	def store(A,dep_id:str)->sqlite3.Connection:
		B=dep_id
		if B not in A.stores:A.stores[B]=czlx(A.cfg.fingerprint_db(B))
		return A.stores[B]
	def ledger(B,dep:sqlite3.Row)->bpsi:
		A=dep
		if A[_B]not in B.ledgers:B.ledgers[A[_B]]=bpsi(B.cfg.ledger_dir/A[_B],A[_P])
		return B.ledgers[A[_B]]
	def ratified(A,dep_id:str)->frozenset[str]:return frozenset(A[0]for A in A.db.execute('SELECT field FROM field_class WHERE deployment_id=? AND ratified_by IS NOT NULL',(dep_id,)))
	def field_classes(A,dep_id:str)->dict[str,c5aj]:return{A[_G]:c5aj(A[_T])for A in A.db.execute('SELECT field, class FROM field_class WHERE deployment_id=? AND ratified_by IS NOT NULL',(dep_id,))}
	def source_classes(D,dep_id:str)->dict[str,c5aj]:
		E=dep_id;from bayan_core.evxn import xd0 as F;G=D.deployment(E);B={A:c5aj(B[_T])for(A,B)in D.packs[G[_K]].raw.get(_m,{}).items()}
		for A in D.db.execute('SELECT field, class, ratified_by FROM field_class WHERE deployment_id=?',(E,)):C=c5aj(A[_T]);B[A[_G]]=C if A['ratified_by']is not _A else F([C,B[A[_G]]])or C if A[_G]in B else C
		return B
	def field_tags(A,dep_id:str)->dict[str,frozenset[str]]:B=A.deployment(dep_id);return{B:frozenset(A.get(_b,[]))for(B,A)in A.packs[B[_K]].raw.get(_m,{}).items()if A.get(_b)}
	def recipient_binding(D,dep:sqlite3.Row,requester:str)->dict[str,Any]:
		A=requester;from bayan_gate.ggp6 import a7f as E;B=E(D,dep[_B],A);C:dict[str,Any]={'principal':A}
		if B is not _A:C[_n]={_S:B[_o]}
		return C
	def recipient_extra(C,dep:sqlite3.Row,requester:str)->dict[str,Any]:
		B='employer';from bayan_gate.ggp6 import a7f as D;A=D(C,dep[_B],requester)
		if A is _A:return{}
		return{B:A[B],_n:{_S:A[_o]},'acknowledgement':{_S:A['ack_digest']},'validUntil':datetime.fromtimestamp(A['valid_until'],timezone.utc).strftime(_Z)}
	def enclave_key(A,dep_id:str)->bytes:return A.keys.secret(f"enclave-{dep_id}")
	def recipient_facts(E,dep:sqlite3.Row,requester:str|_A=_A,at:int|_A=_A)->c2v:C=requester;from bayan_gate.ggp6 import a7f as F;B=json.loads(dep['recipient']);A=F(E,dep[_B],C,at)if C else _A;G=frozenset(json.loads(A['citizenships']))if A else frozenset();D=frozenset(json.loads(A['residency']))if A else frozenset();return c2v(named_org=bool(B.get('namedOrg')),purpose_limited=bool(B.get('purposeLimited')),named_individuals=A is not _A,attributes_verified=bool(A and A['clearance_checked_at']),onward_transfer_prohibited=bool(B.get('onwardTransferProhibited')),disposal_bound=bool(B.get('disposalBound')),environment_assessed=bool(B.get('environmentAssessed')),on_insider_list=bool(B.get('onInsiderList')),citizenships=G|D,location=A['location']if A else _A,fre502d_order=bool(B.get('fre502dOrder')),export_encryption_carveout=bool(B.get('exportEncryptionCarveout')),roster_valid=A is not _A,residency=D)
	def skills(B,dep_id:str,answers:str|_A=_A,awaiting:bool=_c)->list[dict[str,Any]]:
		O='example';N='description_ar';M='description';G=answers;F='answers';C=dep_id;from bayan_core.evxn import l0zv as P;Q,R=B.ratified(C),B.field_classes(C);S,H=B.source_classes(C),B.field_tags(C)
		try:I={(A.name,A.version):A.required_r for A in B._summaries(B.deployment(C))}
		except u5fa:I={}
		J=[]
		for A in B.db.execute('SELECT * FROM skill WHERE deployment_id=? ORDER BY name, version',(C,)):
			D=json.loads(A['spec'])
			if G and G not in D.get(F,[]):continue
			if awaiting and A[_H]is not _A:continue
			K=[A if isinstance(A,dict)else{_C:A}for A in D.get(_I,[])];L=sui.from_dict(D);E=P(L,Q,classes=R,source_classes=S,tags=H);T=E.cap_reasons;U=[{_C:A.name,_T:A.field_class.value,_d:A.transform.value if A.transform else _A,'skillTags':sorted(B.tags),'packTags':sorted(H.get(A.name,())),_b:sorted(A.tags),'sources':list(E.lineage.get(A.name,()))}for(A,B)in zip(E.manifest.fields,L.output_schema.columns)];J.append({_C:A[_C],_E:A[_E],'riskClass':A['risk_class'],'maxGradeD':A[_U],'capReasons':[A.to_json()for A in T],'columns':U,F:D.get(F,[]),M:D.get(M,''),N:D.get(N,''),_p:json.loads(A[_q]),_I:[A[_C]for A in K],'paramExamples':{A[_C]:A.get(O)for A in K if A.get(O)is not _A},'certified':A[_H]is not _A,'certifiedBy':A['certified_by'],'certifiedAt':time.strftime(_Z,time.gmtime(A[_H]))if A[_H]else _A,_M:bool(A[_M]),_e:A[_e],_f:I.get((A[_C],A[_E])),'bundleDigest':A['bundle_digest']})
		return J
	def skill_manifest(A,dep_id:str,spec:sui)->fil6:B=dep_id;from bayan_core.evxn import kmuy as C;D,E,E=C(spec,A.ratified(B),classes=A.field_classes(B),source_classes=A.source_classes(B),tags=A.field_tags(B));return D
	def _summaries(B,dep:sqlite3.Row)->list[zdp0]:
		C=dep;G=gra9(B.pack_for(C));D=[]
		for A in B.db.execute('SELECT * FROM skill WHERE deployment_id=? AND decertified=0',(C[_B],)):E=sui.from_dict(json.loads(A['spec']));F=B.skill_manifest(C[_B],E);H=3 if A[_H]is not _A else 2;I=apgg(A[_U],F,f30(F),G,H);D.append(zdp0(A[_C],A[_E],frozenset(E.answers),A[_U],I,A[_U]<=2))
		return D
	def feasibility(D,dep_id:str,qid:str|_A)->list[dict[str,Any]]:
		B=qid;E=D.deployment(dep_id);G=D._summaries(E);H=D.pack_for(E);I=[A for A in pk09 if B is _A or A.id==B]
		if B is not _A and zos5(B)is _A:raise u5fa(404,f"unknown question {B!r}")
		F=[]
		for A in I:C=gl5(A,G);J={B:(H.term(B,f"minclass:{A.id}")or{}).get('label','')for B in('en','ar')};F.append({'question':A.id,'text':A.text_en,'text_ar':A.text_ar,'minClass':A.min_class,'minClass_ar':A.min_class_ar,'minClassWords':J,'achievableD':C.achievable_d,'approvalPath':C.approval_path,'realTime':C.real_time,'skills':list(C.skills),'blocked':A.blocked})
		return F
	def run(A,dep_id:str,skill:str,version:str,params:dict[str,Any],requester:str,dryrun:bool=_c)->dict[str,Any]:
		O=requester;K=params;H=dryrun;E=dep_id;D=version;C=skill;V=A.deployment(E)
		try:F,L=skillreg.bbl(A.db,E,C,D)
		except KeyError as I:raise u5fa(404,f"unknown skill {C}@{D} for {E}")from I
		except skillreg.zfhh as I:raise u5fa(409,str(I))from I
		if L[_M]:raise u5fa(409,f"{C}@{D} is decertified after {L[_e]} quarantines")
		M=A._synthetic_store()if H else A.store(E);N='synthetic:'+gkou(b'fixtures-v1')if H else dw2(M);P=hndw(F.output_schema.max_rows,A.cfg.skill_timeout_s,A.cfg.skill_heap_bytes);B=mbf(M,F,K,N,P);Q=mbf(M,F,K,N,P)if B.conformant else _A;W=bool(Q and Q.output_digest==B.output_digest);R=A.skill_manifest(E,F);S=si1(C,D,_R,_R,L[_H]is not _A,B.conformant,W);T,U=A._certify(V,R,S,O);J=nzm()
		with A.tx:
			G=_A
			if not B.conformant:X,Y=skillreg.l0k(A.db,E,C,D);G={'rule':B.quarantine.rule,'detail':B.quarantine.detail,'count':X,_M:Y}
			A.insert_run(J,E,C,D,O,json.dumps(K),list(B.rows),B.output_digest,N,R,S,T,U,G,H,output_schema=F.output_schema)
		if G:A.events.emit(_N,run=J,skill=f"{C}@{D}",rule=B.quarantine.rule,decertified=G[_M])
		A.events.emit('run',run=J,skill=f"{C}@{D}",status=_r if G else _g,certificate=T.label,certificate_us=U,dryrun=H);return A.get_run(J)
	def insert_run(C,run_id:str,dep_id:str,skill:str|_A,version:str|_A,requester:str,params:str,rows:list[dict[str,Any]],output_digest:str,input_digest:str,manifest:fil6,prov:si1,cert:bre,us:int,quarantine:dict[str,Any]|_A,dryrun:int|bool,*,output_schema:t2ji,derived_from:str|_A=_A,transform_digest:str|_A=_A,lookup:dict[str,Any]|_A=_A)->_A:B=lookup;A=quarantine;C.db.execute('INSERT INTO run (id, deployment_id, skill_name, skill_version, requester, params, status, rows, output_digest, input_digest, manifest, certificate, certificate_us, quarantine, dryrun, provenance, derived_from, transform_digest, output_schema, created_at, lookup) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(run_id,dep_id,skill,version,requester,params,_r if A else _g,json.dumps(rows),output_digest,input_digest,json.dumps(q5e8(manifest)),json.dumps(qxd5(cert)),us,json.dumps(A)if A else _A,int(dryrun),json.dumps(w8iy(prov)),derived_from,transform_digest,json.dumps(output_schema.to_dict()),int(time.time()),json.dumps(B)if B else _A))
	def _certify(A,dep:sqlite3.Row,manifest:fil6,prov:si1,requester:str,reviews:pkj1|_A=_A,prior:bool=_c)->tuple[bre,int]:C=requester;B=manifest;D=gra9(A.pack_for(dep));E=f30(B);F=reviews or pkj1(C,policy_cleared=E in D.policy_clear_risk_classes and prov.certified);G=time.perf_counter();H=v5e(B,prov,F,A.recipient_facts(dep,C),D,issued_at=oy60(),matches_prior_cleared_shape=prior);return H,int((time.perf_counter()-G)*1e6)
	def run_row(C,run_id:str)->sqlite3.Row:
		A=run_id;B=C.db.execute('SELECT * FROM run WHERE id=?',(A,)).fetchone()
		if B is _A:raise u5fa(404,f"unknown run {A!r}")
		return B
	def _menu(B,row:sqlite3.Row,target:int)->n4y:A=row;C=B.deployment(A[_h]);D=vf4(json.loads(A[_V]));E=3 if gowu(json.loads(A[_W])).certified else 2;return dsan(D,target,gra9(B.pack_for(C)),B.recipient_facts(C,A[_J]),E)
	@staticmethod
	def _recommendation(menu:n4y)->dict[str,Any]|_A:
		A=menu.recommended
		if A is _A:return
		return{_s:A.describe(),_t:[{_G:A.field,_d:A.transform.value,_I:dict(A.params)}for A in A.changes],'d':f"D{A.d}",_f:f"R{A.required_r}",_u:A.reaches_target}
	def get_run(C,run_id:str)->dict[str,Any]:
		G='dryrun';E='lookup';D='certificate';A=C.run_row(run_id);F=json.loads(A[_X]or'[]');B=json.loads(A[D])if A[D]else _A
		if B and A[_N]:from bayan_core.blg2.uq2 import nypa as H;B['headline']=H.to_json()
		I=C._recommendation(C._menu(A,2))if B and A[_Y]==_g and int(B['d'])<2 else _A;return{_B:A[_B],_a:A[_h],'skill':A['skill_name'],_E:A['skill_version'],_Y:A[_Y],_J:A[_J],_I:json.loads(A[_I]),'outputRef':{_X:len(F),_F:A['output_digest'],'inputDigest':A['input_digest']},_X:F[:500],D:B,'certificateMicros':A['certificate_us'],_N:json.loads(A[_N])if A[_N]else _A,G:bool(A[G]),_V:json.loads(A[_V]),_W:json.loads(A[_W]),'derivedFrom':A['derived_from'],'transformDigest':A['transform_digest'],_p:json.loads(A[_q]),E:json.loads(A[E])if A[E]else _A,_v:I}
	def uplift_menu(B,run_id:str,target:int)->dict[str,Any]:C='recommended';D=B.run_row(run_id);A=B._menu(D,target);return{'target':f"D{A.target_d}",'current':f"D{A.current_d}",'asyncRequired':A.async_required,_v:B._recommendation(A),'unreachableReason':A.unreachable_reason,'options':[{_t:[{_G:A.field,_d:A.transform.value,_I:dict(A.params)}for A in A.changes],_s:A.describe(),_u:A.reaches_target,'d':f"D{A.d}",_f:f"R{A.required_r}",'cost':A.cost,'loses':list(A.loses),'keeps':A.keeps,C:A.recommended}for A in A.options],C:A.recommended.describe()if A.recommended else _A}
	def apply_uplift(A,run_id:str,option_index:int,requester:str)->dict[str,Any]:from bayan_gate.o432 import mvle as B;return B(A,run_id,option_index,requester)
	def upgrade_d3(A,run_id:str)->dict[str,Any]:
		D=run_id;from bayan_core.blg2.k8uj import crt3 as J,h830 as K;B=A.run_row(D);C=nzm();A.jobs[C]={_B:C,'run':D,_Y:'running','estimate_s':1}
		def E()->_A:
			I='min_cell';time.sleep(.05)
			with A.tx:L=A.deployment(B[_h]);M=json.loads(B[_X]or'[]');E=vf4(json.loads(B[_V]));F=[K(M,A.name,int(A.param(I)),oy60())for A in E.fields if A.param(I)is not _A];G=J(E,F);N=gowu(json.loads(B[_W]));H,O=A._certify(L,G,N,B[_J]);A.db.execute('UPDATE run SET certificate=?, manifest=? WHERE id=?',(json.dumps(qxd5(H)),json.dumps(q5e8(G)),D));A.jobs[C].update(status='done',certificate=H.label,properties=[{_C:A.name,'threshold':A.threshold,'observed':A.observed,'passed':A.passed}for A in F])
		threading.Thread(target=E,daemon=_R).start();return dict(A.jobs[C])
	def _synthetic_store(F)->sqlite3.Connection:C='doc_ref';B='record_id';A=sqlite3.connect(':memory:');D=['pension','leave','payroll','it-access','housing'];E=[{B:f"SYN{A:06d}",'ts_hour':f"2026-08-{1+A%28:02d}T{A%24:02d}:00:00Z",'week':f"2026-W{31+A%28//7}",'tier':1,'operation':'chat','topic':D[A%5],'route':'ingress>retrieve>generate','finish_reason':'stop','error_code':'none'if A%3 else'retrieval_empty','latency_bucket':'1s-5s','latency_ms':_A,'input_bucket':'257-1k','output_bucket':'65-256','input_exact':_A,'output_exact':_A,'hit_count':A%6,'doc_ref_count':A%3,'guardrail_tripped':0,'guardrail_category':_A,'confidence':_A,'tool_name':_A,'conversation_id':_A,'index_generation':1,'prompt_version':'0'*64,'model_version':'1'*64,'product_version':'0.0'}for A in range(2000)];ewsp(A,{'fingerprints':E,'doc_refs':[{B:f"SYN{A:06d}",C:f"{A%7:064x}",'rank':1}for A in range(2000)],'doc_index':[{C:f"{A:064x}",'doc_id':f"SYN-DOC-{A}"}for A in range(7)]});return A
	def create_request(A,dep_id:str,requester:str,purpose:str,mechanism:str,run_id:str|_A=_A,record_id:str|_A=_A,retention:str|_A=_A,sensitive_declared:list[str]|_A=_A,lookup:dict[str,Any]|_A=_A)->dict[str,Any]:
		from bayan_gate.ubk1 import euh9 as B
		with A.lock:return B(A,dep_id,requester,purpose,mechanism,run_id,record_id,retention,sensitive_declared or[],lookup)
	def _finalize(A,rid:str,outcome:str,human_reviews:list[dict[str,Any]],actor:str)->dict[str,Any]:
		from bayan_gate.cwm import hkl as B
		with A.lock:return B(A,rid,outcome,human_reviews,actor)
	def get_request(A,rid:str,viewer:str)->dict[str,Any]:from bayan_gate.ubk1 import ep8 as B;return B(A,rid,viewer)
	def budget(H,dep_id:str,cohort:str|_A)->list[dict[str,Any]]:G='limit_n';F='disjoint';E='period';D='cohort';C='reserved';B='consumed';A=cohort;I='SELECT * FROM budget WHERE cohort LIKE ?'+(' AND cohort=?'if A else'');J=(f"{dep_id}:%",)+((A,)if A else());return[{D:A[D],E:A[E],B:A[B],C:A[C],'limit':A[G],'remaining':A[G]-A[B]-A[C],F:bool(A[F])}for A in H.db.execute(I,J)]
