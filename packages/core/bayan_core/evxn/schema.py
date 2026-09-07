from __future__ import annotations
_b='description_ar'
_a='description'
_Z='declares'
_Y='answers'
_X='output_schema'
_W='inputs'
_V='fields'
_U='runtime'
_T='author'
_S='version'
_R='example'
_Q='ordering'
_P='max_rows'
_O='columns'
_N='canonical'
_M='load_bearing'
_L='domain'
_K='pseudonym'
_J='sql'
_I='transform'
_H=False
_G='integer'
_F='params'
_E='name'
_D='pattern'
_C='enum'
_B=True
_A=None
from collections.abc import Mapping
from dataclasses import dataclass,field
from typing import Any
from bayan_core.blg.brgs import mhbq,gkou
from bayan_core.blg2.dl9 import im5,fil6,gy0
from bayan_core.schema.g5v import c5aj
nkfw=_C,_G,_K,_D,'text'
@dataclass(frozen=_B)
class xnjp:
	name:str;field_class:c5aj;type:str;domain:tuple[str,...]=();min:int|_A=_A;max:int|_A=_A;transform:gy0|_A=_A;params:tuple[tuple[str,Any],...]=();load_bearing:bool=_H;tags:frozenset[str]=frozenset();pattern:str|_A=_A
	@classmethod
	def from_dict(A,d:dict[str,Any])->xnjp:return A(name=d[_E],field_class=c5aj(d['class']),type=d['type'],domain=tuple(d.get(_L,())),min=d.get('min'),max=d.get('max'),transform=gy0(d[_I])if d.get(_I)else _A,params=tuple(sorted(d.get(_F,{}).items())),load_bearing=bool(d.get(_M,_H)),tags=frozenset(d.get('tags',())),pattern=d.get(_D))
	def to_dict(A)->dict[str,Any]:
		B:dict[str,Any]={_E:A.name,'class':A.field_class.value,'type':A.type}
		if A.domain:B[_L]=list(A.domain)
		if A.min is not _A:B['min']=A.min
		if A.max is not _A:B['max']=A.max
		if A.transform:B[_I]=A.transform.value
		if A.params:B[_F]=dict(A.params)
		if A.load_bearing:B[_M]=_B
		if A.tags:B['tags']=sorted(A.tags)
		if A.pattern:B[_D]=A.pattern
		return B
@dataclass(frozen=_B)
class t2ji:
	columns:tuple[xnjp,...];max_rows:int;ordering:str=_N
	@classmethod
	def from_dict(A,d:dict[str,Any])->t2ji:return A(tuple(xnjp.from_dict(A)for A in d[_O]),int(d[_P]),d.get(_Q,_N))
	def to_dict(A)->dict[str,Any]:return{_O:[A.to_dict()for A in A.columns],_P:A.max_rows,_Q:A.ordering}
	def declaration_errors(C)->list[str]:
		B=[];D:set[str]=set()
		for A in C.columns:
			if A.name in D:B.append(f"{A.name}: duplicate column")
			D.add(A.name)
			if A.type not in nkfw:B.append(f"{A.name}: unknown type {A.type!r}")
			if A.field_class in(c5aj.STRUCTURAL,c5aj.VENDOR)and A.type not in(_C,_G):B.append(f"{A.name}: S1 — {A.field_class.value} must be enum or integer, declared {A.type!r}")
			if A.type==_C and not A.domain:B.append(f"{A.name}: enum with an empty domain")
			if A.type==_C and len(set(A.domain))!=len(A.domain):B.append(f"{A.name}: enum domain has duplicates")
			if A.type==_G and(A.min is _A or A.max is _A):B.append(f"{A.name}: integer without a declared range")
			if A.type=='text'and A.field_class is not c5aj.FREETEXT:B.append(f"{A.name}: free strings are only permitted for FREETEXT columns")
			if A.type==_K and A.transform is not gy0.HMAC_ENCLAVE:B.append(f"{A.name}: pseudonym columns must declare transform hmac_enclave")
			if A.type==_D:
				if not A.pattern or not A.pattern.startswith('^')or not A.pattern.endswith('$'):B.append(f"{A.name}: pattern columns need an anchored regular expression")
				if A.transform not in(gy0.TRUNCATE,gy0.MASK,_A):B.append(f"{A.name}: pattern columns carry truncated, masked or untransformed identifiers; {A.transform.value} is not a shape a pattern can attest")
		if C.max_rows<1:B.append('max_rows must be >= 1')
		return B
@dataclass(frozen=_B)
class zl0e:store:str;fields:tuple[str,...]
@dataclass(frozen=_B)
class ckxc:
	name:str;example:Any=_A
	@classmethod
	def from_entry(A,e:Any)->ckxc:
		if isinstance(e,ckxc):return e
		if isinstance(e,str):return A(e)
		return A(str(e[_E]),e.get(_R))
	def to_entry(A)->Any:return A.name if A.example is _A else{_E:A.name,_R:A.example}
@dataclass(frozen=_B)
class sui:
	name:str;version:str;author:str;runtime:str;inputs:tuple[zl0e,...];sql:str;param_specs:tuple[ckxc,...];output_schema:t2ji;answers:tuple[str,...]=();declares:dict[str,Any]=field(default_factory=dict);description:str='';description_ar:str=''
	def __post_init__(A)->_A:object.__setattr__(A,'param_specs',tuple(ckxc.from_entry(A)for A in A.param_specs))
	@property
	def params(self)->tuple[str,...]:return tuple(A.name for A in self.param_specs)
	@property
	def example_params(self)->dict[str,Any]:return{A.name:A.example for A in self.param_specs if A.example is not _A}
	@classmethod
	def from_dict(A,d:dict[str,Any])->sui:return A(name=d['skill'],version=d[_S],author=d.get(_T,''),runtime=d.get(_U,_J),inputs=tuple(zl0e(A['store'],tuple(A[_V]))for A in d.get(_W,[])),sql=d[_J],param_specs=tuple(ckxc.from_entry(A)for A in d.get(_F,[])),output_schema=t2ji.from_dict(d[_X]),answers=tuple(d.get(_Y,[])),declares=dict(d.get(_Z,{})),description=d.get(_a,''),description_ar=d.get(_b,''))
	def to_dict(A)->dict[str,Any]:return{'skill':A.name,_S:A.version,_T:A.author,_U:A.runtime,_W:[{'store':A.store,_V:list(A.fields)}for A in A.inputs],_J:A.sql,_F:[A.to_entry()for A in A.param_specs],_X:A.output_schema.to_dict(),_Y:list(A.answers),_Z:dict(A.declares),_a:A.description,_b:A.description_ar}
def hh5(spec:sui)->str:return gkou(mhbq(spec.to_dict()))
def htz(schema:t2ji,ratified:frozenset[str]|_A=_A,sensitive_declared:frozenset[str]=frozenset(),mechanism:str='output-check',row_level:bool=_H,classes:Mapping[str,c5aj]|_A=_A)->fil6:B=ratified;A=tuple(im5(A.name,(classes or{}).get(A.name,A.field_class),A.transform,A.params,ratified=B is _A or A.name in B,tags=A.tags,load_bearing=A.load_bearing)for A in schema.columns);return fil6(A,sensitive_declared,row_level,mechanism)
