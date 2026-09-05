from __future__ import annotations
_H='release-request'
_G='retention'
_F='receipt'
_E='clearance'
_D='name'
_C=None
_B='digest'
_A='sha256'
from typing import Any
from bayan_core.crypto.canonical import canonical_json,sha256_hex
def _prune_envelopes(ijeuf=_C):
	try:A=int(ijeuf)
	except(TypeError,ValueError):return
	return A if A>=0 else-A
kiy='https://in-toto.io/Statement/v1'
def _statement(kind:str,subject:list[dict[str,Any]],predicate:dict[str,Any])->dict[str,Any]:return{'_type':kiy,'subject':subject,'predicateType':f"https://bayan.dev/{kind}/v1",'predicate':predicate}
def evg(*,subject_name:str,subject_digest:str,deployment:dict[str,str],classification:dict[str,Any],purpose:str,mechanism:str,minimisation:dict[str,Any],budget:dict[str,int],retention:dict[str,str],requester:dict[str,str],created_at:str,query:dict[str,Any]|_C=_C)->dict[str,Any]:
	A=query;B:dict[str,Any]={'deployment':deployment,'classification':classification,'purpose':purpose,'mechanism':mechanism,'minimisation':minimisation,'budget':budget,_G:retention,'requester':requester,'createdAt':created_at}
	if A is not _C:B['query']=A
	return _statement(_H,[{_D:subject_name,_B:{_A:subject_digest}}],B)
def clearance(*,request_payload:bytes,profile:dict[str,Any],commitment:str,nonce:str,verdict:str,rrsa_class:str,findings:list[dict[str,str]],human_reviews:list[dict[str,Any]],transformations:list[dict[str,Any]],redacted:list[dict[str,str]],outcome:str,decided_at:str)->dict[str,Any]:A=sha256_hex(request_payload);return _statement(_E,[{_D:_H,_B:{_A:A}}],{'request':{_B:{_A:A}},'policyProfile':profile,'machineCheck':{'commitment':commitment,'nonce':nonce,'verdict':verdict,'rrsaClass':rrsa_class,'findings':findings},'humanReviews':human_reviews,'transformations':transformations,'redactedAssertions':redacted,'outcome':outcome,'decidedAt':decided_at})
def receipt(*,clearance_payload:bytes,released:list[dict[str,Any]],checkpoint_text:str,leaf_index:int,inclusion_hashes_b64:list[str],egress_path:str,disposal_due:str,disposal_method:str,released_at:str)->dict[str,Any]:A=sha256_hex(clearance_payload);return _statement(_F,[{_D:_E,_B:{_A:A}}],{_E:{_B:{_A:A}},'released':released,'ledger':{'checkpoint':checkpoint_text,'leafIndex':leaf_index,'inclusionProof':{'hashes':inclusion_hashes_b64}},'egressPath':egress_path,_G:{'disposalDue':disposal_due,'disposalMethod':disposal_method,'secondaryUse':'prohibited'},'releasedAt':released_at})
def jct(*,receipt_payload:bytes,at:str,method:str,signer:dict[str,str],record_digests:list[str])->dict[str,Any]:A=receipt_payload;return _statement('disposal-attestation',[{_D:_F,_B:{_A:sha256_hex(A)}}],{_F:{_B:{_A:sha256_hex(A)}},'at':at,'method':method,'signer':signer,'recordDigests':[{_A:A}for A in record_digests]})
def szee(statement:dict[str,Any])->str:return sha256_hex(canonical_json(statement))