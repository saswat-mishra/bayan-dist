from __future__ import annotations
_U='approvedBy'
_T='signer'
_S='method'
_R='disposal-attestation'
_Q='leafIndex'
_P='release-request'
_O='retention'
_N='presentedDigest'
_M='reviewer'
_L='principal'
_K='receipt'
_J='clearance'
_I='verdict'
_H='request'
_G='reason'
_F='deployment'
_E='at'
_D='name'
_C='digest'
_B='sha256'
_A=None
from typing import Any
from bayan_core.blg.brgs import mhbq,gkou
kiy='https://in-toto.io/Statement/v1'
zp9=2
def xgl(kind:str,subject:list[dict[str,Any]],predicate:dict[str,Any],version:int=zp9)->dict[str,Any]:return{'_type':kiy,'subject':subject,'predicateType':f"https://bayan.dev/{kind}/v{version}",'predicate':predicate}
def azw(*,request_digest:str,reviewer:str,verdict:str,reason:str,presented_digest:str,lang:str,at:str)->bytes:return mhbq({_H:request_digest,_M:reviewer,_I:verdict,_G:reason,_N:presented_digest,'lang':lang,_E:at})
def lcs(entry:dict[str,Any])->bytes:A=entry;return azw(request_digest=str(A[_H]),reviewer=str(A[_M]['id']),verdict=str(A[_I]),reason=str(A.get(_G,'')),presented_digest=str(A[_N]),lang=str(A['lang']),at=str(A[_E]))
def evg(*,subject_name:str,subject_digest:str,deployment:dict[str,str],classification:dict[str,Any],purpose:str,mechanism:str,minimisation:dict[str,Any],budget:dict[str,int],retention:dict[str,str],requester:dict[str,str],recipient:dict[str,Any],created_at:str,query:dict[str,Any]|_A=_A)->dict[str,Any]:
	A=query;B:dict[str,Any]={_F:deployment,'classification':classification,'purpose':purpose,'mechanism':mechanism,'minimisation':minimisation,'budget':budget,_O:retention,'requester':requester,'recipient':recipient,'createdAt':created_at}
	if A is not _A:B['query']=A
	return xgl(_P,[{_D:subject_name,_C:{_B:subject_digest}}],B)
def wr5(*,request_payload:bytes,profile:dict[str,Any],commitment:str,nonce:str,verdict:str,rrsa_class:str,findings:list[dict[str,str]],human_reviews:list[dict[str,Any]],transformations:list[dict[str,Any]],redacted:list[dict[str,str]],outcome:str,decided_at:str,certificate:dict[str,Any],certificate_at_request:str|_A=_A,recommendation:str|_A=_A,recommendation_basis:list[str]|_A=_A)->dict[str,Any]:
	C=recommendation;B=certificate_at_request;D=gkou(request_payload);A:dict[str,Any]={'commitment':commitment,'nonce':nonce,_I:verdict,'rrsaClass':rrsa_class,'findings':findings}
	if B is not _A:A['certificateAtRequest']={_B:B}
	if C is not _A:A['recommendation']=C;A['recommendationBasis']=list(recommendation_basis or[])
	return xgl(_J,[{_D:_P,_C:{_B:D}}],{_H:{_C:{_B:D}},'policyProfile':profile,'machineCheck':A,'humanReviews':human_reviews,'transformations':transformations,'redactedAssertions':redacted,'certificate':certificate,'outcome':outcome,'decidedAt':decided_at})
def z0x(*,clearance_payload:bytes,released:list[dict[str,Any]],checkpoint_text:str,leaf_index:int,inclusion_hashes_b64:list[str],egress_path:str,disposal_due:str,disposal_method:str,released_at:str,controls:dict[str,list[str]],headline:dict[str,str],certificate_summary:dict[str,str])->dict[str,Any]:A=gkou(clearance_payload);return xgl(_K,[{_D:_J,_C:{_B:A}}],{_J:{_C:{_B:A}},'released':released,'ledger':{'checkpoint':checkpoint_text,_Q:leaf_index,'inclusionProof':{'hashes':inclusion_hashes_b64}},'egressPath':egress_path,_O:{'disposalDue':disposal_due,'disposalMethod':disposal_method,'secondaryUse':'prohibited'},'releasedAt':released_at,'controls':controls,'headline':headline,'certificateSummary':certificate_summary})
def vcqj(*,deployment:str,ack_digest:str,principal:str,at:str)->bytes:return mhbq({_F:deployment,'ackDigest':ack_digest,_L:principal,_E:at})
def bgw(*,deployment:str,principal:str,receipt_digests:list[str],at:str,method:str,signer:dict[str,str])->dict[str,Any]:A=principal;return xgl(_R,[{_D:f"roster-{A}",_C:{_B:gkou(A.encode())}}],{_F:deployment,_L:A,_E:at,_S:method,_T:signer,'receipts':[{_B:A}for A in receipt_digests]},version=1)
def xbf(*,principal:str,key_name:str,public_key:str,genesis:bool,approved_by:dict[str,str]|_A,at:str)->dict[str,Any]:
	C=approved_by;B=public_key;A=key_name;D:dict[str,Any]={_L:principal,'key':{_D:A,'algorithm':'ed25519','publicKey':B},'genesis':genesis,_E:at}
	if C is not _A:D[_U]=C
	return xgl('key-enrolment',[{_D:A,_C:{_B:gkou(B.encode())}}],D,version=1)
def v83(*,deployment:str,hour:str,root:str,events:int,by_class:dict[str,int],dispositions:dict[str,int],honesty:str)->dict[str,Any]:A=deployment;return xgl('sensor-digest',[{_D:f"sensor-{A}-{hour}",_C:{_B:root}}],{_F:A,'hour':hour,'root':root,'events':events,'byClass':dict(sorted(by_class.items())),'dispositions':dict(sorted(dispositions.items())),'honesty':honesty},version=1)
def jxm(*,deployment:str,kind:str,reason:str,event_digest:str|_A,by:dict[str,str],at:str,clears_leaf:int|_A=_A)->dict[str,Any]:
	D=clears_leaf;C=event_digest;A=deployment;B:dict[str,Any]={_F:A,_G:reason,'by':by,_E:at}
	if C is not _A:B['event']={_C:{_B:C}}
	if D is not _A:B['clears']={_Q:D}
	return xgl(kind,[{_D:A,_C:{_B:gkou(A.encode())}}],B,version=1)
def olo(*,deployment:str,pack_id:str,from_digest:str,to_digest:str,to_version:str,approved_by:dict[str,str],reason:str,at:str)->dict[str,Any]:B=to_digest;A=pack_id;return xgl('pack-upgrade',[{_D:f"pack-{A}",_C:{_B:B}}],{_F:deployment,'pack':{'id':A,'version':to_version},'from':{_C:{_B:from_digest}},'to':{_C:{_B:B}},_U:approved_by,_G:reason,_E:at},version=1)
def jct(*,receipt_payload:bytes,at:str,method:str,signer:dict[str,str],record_digests:list[str])->dict[str,Any]:A=receipt_payload;return xgl(_R,[{_D:_K,_C:{_B:gkou(A)}}],{_K:{_C:{_B:gkou(A)}},_E:at,_S:method,_T:signer,'recordDigests':[{_B:A}for A in record_digests]},version=1)
def szee(statement:dict[str,Any])->str:return gkou(mhbq(statement))
