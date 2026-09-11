from __future__ import annotations
_P='blocked'
_O='grade'
_N='text_ar'
_M='text'
_L='latencyMs'
_K='setAt'
_J='setBy'
_I='question'
_H='skills'
_G='id'
_F='ok'
_E='lastCheck'
_D='error'
_C='endpoint'
_B=None
_A='model'
import hashlib,ipaddress,json,time,urllib.error,urllib.request
from typing import Any
from urllib.parse import urlparse
from bayan_gate.i7m5 import b8d,u5fa,oy60
izw='.local','.internal','.enclave','.lan','.home.arpa'
d032=8.
zn2d=6e1
ksa0=240
def fur2(host:str)->bool:
	A=host.strip('[]').lower()
	if A=='localhost'or A.endswith(izw):return True
	try:B=ipaddress.ip_address(A)
	except ValueError:return False
	return B.is_loopback or B.is_private or B.is_link_local
def q32(endpoint:str)->str:
	A=urlparse(endpoint.strip())
	if A.scheme not in('http','https')or not A.hostname:raise u5fa(422,'the endpoint must be an http(s) URL, for example http://127.0.0.1:11434')
	if not fur2(A.hostname):raise u5fa(422,f"the model must be inside the enclave — loopback or a private address; {A.hostname!r} is public and the gate will not reach it")
	B=A.path.rstrip('/')
	if B.endswith('/v1'):B=B[:-3]
	return f"{A.scheme}://{A.netloc}{B}"
def cv17(gate:b8d,dep_id:str)->dict[str,Any]:
	A=gate.deployment(dep_id)
	try:return json.loads(A['assistant']or'{}')
	except(TypeError,ValueError):return{}
def fki(gate:b8d,dep_id:str,cfg:dict[str,Any])->_B:
	with gate.tx:gate.db.execute('UPDATE deployment SET assistant=? WHERE id=?',(json.dumps(cfg,sort_keys=True),dep_id))
def c3vw(gate:b8d,dep_id:str)->dict[str,Any]:C=dep_id;A=cv17(gate,C);D=bool(A.get(_C)and A.get(_A));B=A.get(_E);return{'deployment':C,'configured':D,_C:A.get(_C),_A:A.get(_A),_J:A.get(_J),_K:A.get(_K),_E:B,'ready':D and bool(B and B.get(_F))}
def qdj(gate:b8d,dep_id:str,principal:str,endpoint:str,model:str)->dict[str,Any]:
	F=principal;D=dep_id;B=gate;A=model;E=q32(endpoint);A=A.strip()
	if not A:raise u5fa(422,'name the model the endpoint serves, for example llama3.1:8b')
	with B.lock:
		C=cv17(B,D);G=C.get(_C)!=E or C.get(_A)!=A;C.update({_C:E,_A:A,_J:F,_K:oy60()})
		if G:C[_E]=_B
		fki(B,D,C)
	B.events.emit('assistant-configured',deployment=D,by=F,endpoint=E,model=A);return c3vw(B,D)
def iew(gate:b8d,dep_id:str,principal:str)->dict[str,Any]:
	B=dep_id;A=gate
	with A.lock:fki(A,B,{})
	A.events.emit('assistant-disconnected',deployment=B,by=principal);return c3vw(A,B)
def aa0(url:str,body:dict[str,Any]|_B,timeout:float)->tuple[dict[str,Any],int]:
	B='application/json';A=json.dumps(body).encode()if body is not _B else _B;C=urllib.request.Request(url,data=A,headers={'Content-Type':B,'Accept':B},method='POST'if A is not _B else'GET');D=time.monotonic()
	with urllib.request.urlopen(C,timeout=timeout)as E:F=json.loads(E.read().decode('utf-8'))
	return F,int((time.monotonic()-D)*1000)
def vpmh(e:BaseException)->str:
	if isinstance(e,urllib.error.HTTPError):return f"the endpoint answered {e.code}"
	if isinstance(e,urllib.error.URLError):return f"the endpoint could not be reached: {e.reason}"
	if isinstance(e,TimeoutError):return'the endpoint did not answer in time'
	if isinstance(e,ValueError):return'the endpoint did not answer with JSON'
	return f"the endpoint failed: {type(e).__name__}"
def mix(gate:b8d,dep_id:str,principal:str)->dict[str,Any]:
	D=dep_id;C=gate
	with C.lock:A=cv17(C,D)
	if not(A.get(_C)and A.get(_A)):raise u5fa(409,'no model is connected for this deployment yet — enter the endpoint and the model first')
	B:dict[str,Any]={_F:False,'at':oy60(),_L:_B,_D:_B,'models':[]}
	try:
		F,G=aa0(f"{A[_C]}/v1/models",_B,d032);E=[str(A.get(_G))for A in F.get('data',[])if isinstance(A,dict)and A.get(_G)];B.update(latencyMs=G,models=E[:40])
		if A[_A]in E:B[_F]=True
		else:B[_D]=f"the endpoint is reachable but does not serve {A[_A]!r}"+(f"; it serves {', '.join(E[:6])}"if E else'')
	except(urllib.error.URLError,TimeoutError,ValueError,OSError)as H:B[_D]=vpmh(H)
	with C.lock:A=cv17(C,D);A[_E]=B;fki(C,D,A)
	C.events.emit('assistant-checked',deployment=D,by=principal,ok=B[_F],latencyMs=B[_L],error=B[_D]);return c3vw(C,D)
def g1k(gate:b8d,dep_id:str)->list[dict[str,Any]]:
	E='achievableD';C=dep_id;B=gate
	with B.lock:F=B.feasibility(C,_B);G=B.skills(C,_B)
	H={A['name']:A.get('description')or''for A in G};D=[]
	for A in F:I=[A.split('@')[0]for A in A.get(_H,[])];D.append({_G:A[_I],_M:A[_M],_N:A.get(_N,''),'needs':A.get('minClass',''),_O:_B if A.get(E)is _B else f"D{A[E]}",'path':A.get('approvalPath',''),_P:bool(A.get(_P)),_H:[f"{A}: {H.get(A,'')}".rstrip(': ')for A in I]})
	return D
def kzf9(cat:list[dict[str,Any]],text:str,lang:str)->tuple[str,str]:
	C='Arabic'if lang=='ar'else'English';D=f'/no_think\nYou route a support engineer\'s request to ONE question from a fixed catalogue. You see only the catalogue. Reply with JSON only, no prose around it: {{"question": <catalogue id or null>, "why": <one short sentence, in {C}, addressed to the engineer, saying why that question fits>, "also": [<up to two other catalogue ids worth a look>]}}. Choose null when nothing in the catalogue answers the request. Never invent an id.';B=[]
	for A in cat:E='not permitted at any grade'if A[_P]else f"grade {A[_O]} · {A['path']}"if A[_O]else'no certified skill yet';B.append(f"- {A[_G]} | {A[_M]} | {A[_N]} | needs: {A['needs']} | {E}"+(f" | skills: {'; '.join(A[_H])}"if A[_H]else''))
	F='Catalogue:\n'+'\n'.join(B)+f"\n\nRequest: {text.strip()}";return D,F
def sie(content:str,ids:set[str])->dict[str,Any]|_B:
	G='why';F='also';D='{';A=content.strip()
	if A.startswith('```'):A=A.strip('`');A=A[A.find(D):]if D in A else A
	try:B=json.loads(A[A.find(D):A.rfind('}')+1]if D in A else A)
	except ValueError:return
	if not isinstance(B,dict):return
	C=B.get(_I);C=C if isinstance(C,str)and C in ids else _B;H=[A for A in B.get(F,[])if isinstance(A,str)and A in ids and A!=C][:2]if isinstance(B.get(F),list)else[];E=B.get(G)if isinstance(B.get(G),str)else'';E=' '.join(E.split())[:ksa0];return{_I:C,G:E,F:H}
def cd8(gate:b8d,dep_id:str,principal:str,text:str,lang:str)->dict[str,Any]:
	T='role';K='ask';J='content';G=principal;F='mode';E=text;D='words';C=dep_id;B=gate;E=E.strip()
	if not E:raise u5fa(422,'say what you need to know')
	with B.lock:A=cv17(B,C)
	U=A.get(_E)or{}
	if not(A.get(_C)and A.get(_A)and U.get(_F)):return{F:D,_D:'no client model is connected for this deployment; ranking by words'}
	L=g1k(B,C);V={A[_G]for A in L};M,N=kzf9(L,E[:2000],lang);W={_A:A[_A],'messages':[{T:'system',J:M},{T:'user',J:N}],'response_format':{'type':'json_object'},'temperature':0};H=hashlib.sha256((M+'\n'+N).encode()).hexdigest()
	try:X,O=aa0(f"{A[_C]}/v1/chat/completions",W,zn2d);P=X['choices'][0]['message'].get(J)or''
	except(urllib.error.URLError,TimeoutError,ValueError,OSError,KeyError,IndexError,TypeError)as Q:R=vpmh(Q)if not isinstance(Q,(KeyError,IndexError,TypeError))else'the endpoint answered in an unexpected shape';B.events.emit(K,deployment=C,by=G,mode=D,model=A[_A],promptDigest=H,error=R);return{F:D,_D:R}
	I=sie(P,V);S=hashlib.sha256(P.encode()).hexdigest()
	if I is _B:B.events.emit(K,deployment=C,by=G,mode=D,model=A[_A],promptDigest=H,replyDigest=S,error='the model did not answer in the agreed shape');return{F:D,_D:'the model did not answer in the agreed shape; ranking by words'}
	B.events.emit(K,deployment=C,by=G,mode=_A,model=A[_A],promptDigest=H,replyDigest=S,question=I[_I],latencyMs=O);return{F:_A,_A:A[_A],_L:O,**I}
