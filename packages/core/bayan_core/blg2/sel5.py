from __future__ import annotations
_R='headline'
_Q='requiredR'
_P='residency'
_O='rosterValid'
_N='exportEncryptionCarveout'
_M='fre502dOrder'
_L='location'
_K='citizenships'
_J='onInsiderList'
_I='environmentAssessed'
_H='disposalBound'
_G='onwardTransferProhibited'
_F='attributesVerified'
_E='namedIndividuals'
_D='purposeLimited'
_C='namedOrg'
_B='label'
_A=None
from dataclasses import dataclass,field
from typing import Any
from bayan_core.blg2.otu import q5e8,w8iy
from bayan_core.blg2.uq2 import etf,cbp
from bayan_core.blg2.dl9 import bre,fil6,si1,c2v
z2q='bayan.certificate.v1'
@dataclass(frozen=True)
class fgr:recipient_principal:str;pack_digest:str;output_schema:dict[str,Any]|_A=_A;bundle_digest:str|_A=_A;certified_by:str|_A=_A;transform_digest:str|_A=_A;derived_from:str|_A=_A;pack_activated:tuple[str,...]=();mechanisms:tuple[str,...]=();controls:dict[str,list[str]]=field(default_factory=dict);recipient_extra:dict[str,Any]=field(default_factory=dict);headline_facts:etf=etf();threshold:int=2
def ta77(r:c2v,principal:str,extra:dict[str,Any]|_A=_A)->dict[str,Any]:A:dict[str,Any]={'principal':principal,_C:r.named_org,_D:r.purpose_limited,_E:r.named_individuals,_F:r.attributes_verified,_G:r.onward_transfer_prohibited,_H:r.disposal_bound,_I:r.environment_assessed,_J:r.on_insider_list,_K:sorted(r.citizenships),_L:r.location,_M:r.fre502d_order,_N:r.export_encryption_carveout,_O:r.roster_valid,_P:sorted(r.residency)};A.update(extra or{});return A
def vrf3(d:dict[str,Any])->c2v:return c2v(named_org=bool(d.get(_C)),purpose_limited=bool(d.get(_D)),named_individuals=bool(d.get(_E)),attributes_verified=bool(d.get(_F)),onward_transfer_prohibited=bool(d.get(_G)),disposal_bound=bool(d.get(_H)),environment_assessed=bool(d.get(_I)),on_insider_list=bool(d.get(_J)),citizenships=frozenset(d.get(_K,[])),location=d.get(_L),fre502d_order=bool(d.get(_M)),export_encryption_carveout=bool(d.get(_N)),roster_valid=bool(d.get(_O)),residency=frozenset(d.get(_P,[])))
def kki(c:bre)->list[dict[str,Any]]:return[{'name':A.name,'passed':A.passed,'citation':A.citation,'detail':A.detail,'remedyKind':A.remedy_kind,'remedy':A.remedy,'fixableByTransformation':A.fixable_by_transformation,'offendingFields':list(A.offending_fields)}for A in c.gates]
def ahau(c:bre)->dict[str,Any]:return{'d':c.d,'p':c.p,'r':c.r,'e':c.e,_Q:c.required_r,'riskClass':c.risk_class,_B:c.label,'releasable':c.releasable,'disqualified':c.disqualified}
def r7pl(c:bre,manifest:fil6,prov:si1,recipient:c2v,ctx:fgr)->dict[str,Any]:
	A=ctx;C=w8iy(prov);C.update({'bundleDigest':A.bundle_digest,'certifiedBy':A.certified_by,'transformDigest':A.transform_digest,'derivedFrom':A.derived_from});D=_A
	if c.nearest_releasable is not _A:B=c.nearest_releasable;D={'d':B.d,_Q:B.required_r,'dropped':list(B.dropped),'loadBearingLost':list(B.load_bearing_lost)}
	return{'schema':z2q,'grade':ahau(c),'manifest':q5e8(manifest),'outputSchema':A.output_schema,'provenance':C,'gates':kki(c),'recipient':ta77(recipient,A.recipient_principal,A.recipient_extra),'mechanisms':list(A.mechanisms),'controls':{A:sorted(B)for(A,B)in sorted(A.controls.items())},_R:cbp(c,A.headline_facts,threshold=A.threshold).to_json(),'doesNotStop':list(c.does_not_stop),'nearestReleasable':D,'issuedAt':c.issued_at,'expiresAt':c.expires_at,'reassessmentTriggers':list(c.reassessment_triggers),'pack':{'id':c.pack_id,'version':c.pack_version,'digest':{'sha256':A.pack_digest},'activated':list(A.pack_activated)}}
def xt9(certificate:dict[str,Any])->dict[str,str]:B='kind';A=certificate;return{_B:str(A['grade'][_B]),B:str(A[_R][B])}
