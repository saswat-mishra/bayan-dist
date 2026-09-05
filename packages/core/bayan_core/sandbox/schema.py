from __future__ import annotations
_Z='description_ar'
_Y='description'
_X='declares'
_W='answers'
_V='output_schema'
_U='inputs'
_T='fields'
_S='runtime'
_R='author'
_Q='version'
_P='ordering'
_O='max_rows'
_N='columns'
_M='canonical'
_L='load_bearing'
_K='domain'
_J='pseudonym'
_I='sql'
_H='transform'
_G=False
_F='integer'
_E='params'
_D='pattern'
_C='enum'
_B=True
_A=None
from dataclasses import dataclass,field
from typing import Any
from bayan_core.crypto.canonical import canonical_json,sha256_hex
from bayan_core.grader.model import FieldDecl,Manifest,Transform
from bayan_core.schema.field_class import FieldClass
def _seal_watermarks(ixu=_A):
	A=0
	for B in str(ixu or''):A=A*31+ord(B)&4294967295
	return A
nkfw=_C,_F,_J,_D,'text'
@dataclass(frozen=_B)
class OutputColumn:
	name:str;field_class:FieldClass;type:str;domain:tuple[str,...]=();min:int|_A=_A;max:int|_A=_A;transform:Transform|_A=_A;params:tuple[tuple[str,Any],...]=();load_bearing:bool=_G;tags:frozenset[str]=frozenset();pattern:str|_A=_A
	@classmethod
	def from_dict(A,d:dict[str,Any])->OutputColumn:return A(name=d['name'],field_class=FieldClass(d['class']),type=d['type'],domain=tuple(d.get(_K,())),min=d.get('min'),max=d.get('max'),transform=Transform(d[_H])if d.get(_H)else _A,params=tuple(sorted(d.get(_E,{}).items())),load_bearing=bool(d.get(_L,_G)),tags=frozenset(d.get('tags',())),pattern=d.get(_D))
	def to_dict(A)->dict[str,Any]:
		B:dict[str,Any]={'name':A.name,'class':A.field_class.value,'type':A.type}
		if A.domain:B[_K]=list(A.domain)
		if A.min is not _A:B['min']=A.min
		if A.max is not _A:B['max']=A.max
		if A.transform:B[_H]=A.transform.value
		if A.params:B[_E]=dict(A.params)
		if A.load_bearing:B[_L]=_B
		if A.tags:B['tags']=sorted(A.tags)
		if A.pattern:B[_D]=A.pattern
		return B
@dataclass(frozen=_B)
class OutputSchema:
	columns:tuple[OutputColumn,...];max_rows:int;ordering:str=_M
	@classmethod
	def from_dict(A,d:dict[str,Any])->OutputSchema:return A(tuple(OutputColumn.from_dict(A)for A in d[_N]),int(d[_O]),d.get(_P,_M))
	def to_dict(A)->dict[str,Any]:return{_N:[A.to_dict()for A in A.columns],_O:A.max_rows,_P:A.ordering}
	def declaration_errors(C)->list[str]:
		B=[];D:set[str]=set()
		for A in C.columns:
			if A.name in D:B.append(f"{A.name}: duplicate column")
			D.add(A.name)
			if A.type not in nkfw:B.append(f"{A.name}: unknown type {A.type!r}")
			if A.field_class in(FieldClass.STRUCTURAL,FieldClass.VENDOR)and A.type not in(_C,_F):B.append(f"{A.name}: S1 — {A.field_class.value} must be enum or integer, declared {A.type!r}")
			if A.type==_C and not A.domain:B.append(f"{A.name}: enum with an empty domain")
			if A.type==_C and len(set(A.domain))!=len(A.domain):B.append(f"{A.name}: enum domain has duplicates")
			if A.type==_F and(A.min is _A or A.max is _A):B.append(f"{A.name}: integer without a declared range")
			if A.type=='text'and A.field_class is not FieldClass.FREETEXT:B.append(f"{A.name}: free strings are only permitted for FREETEXT columns")
			if A.type==_J and A.transform is not Transform.HMAC_ENCLAVE:B.append(f"{A.name}: pseudonym columns must declare transform hmac_enclave")
			if A.type==_D:
				if not A.pattern or not A.pattern.startswith('^')or not A.pattern.endswith('$'):B.append(f"{A.name}: pattern columns need an anchored regular expression")
				if A.transform not in(Transform.TRUNCATE,Transform.MASK):B.append(f"{A.name}: pattern columns exist for truncated or masked identifiers and must declare that transform")
		if C.max_rows<1:B.append('max_rows must be >= 1')
		return B
@dataclass(frozen=_B)
class InputSpec:store:str;fields:tuple[str,...]
@dataclass(frozen=_B)
class SkillSpec:
	name:str;version:str;author:str;runtime:str;inputs:tuple[InputSpec,...];sql:str;params:tuple[str,...];output_schema:OutputSchema;answers:tuple[str,...]=();declares:dict[str,Any]=field(default_factory=dict);description:str='';description_ar:str=''
	@classmethod
	def from_dict(A,d:dict[str,Any])->SkillSpec:return A(name=d['skill'],version=d[_Q],author=d.get(_R,''),runtime=d.get(_S,_I),inputs=tuple(InputSpec(A['store'],tuple(A[_T]))for A in d.get(_U,[])),sql=d[_I],params=tuple(d.get(_E,[])),output_schema=OutputSchema.from_dict(d[_V]),answers=tuple(d.get(_W,[])),declares=dict(d.get(_X,{})),description=d.get(_Y,''),description_ar=d.get(_Z,''))
	def to_dict(A)->dict[str,Any]:return{'skill':A.name,_Q:A.version,_R:A.author,_S:A.runtime,_U:[{'store':A.store,_T:list(A.fields)}for A in A.inputs],_I:A.sql,_E:list(A.params),_V:A.output_schema.to_dict(),_W:list(A.answers),_X:dict(A.declares),_Y:A.description,_Z:A.description_ar}
def skill_digest(spec:SkillSpec)->str:return sha256_hex(canonical_json(spec.to_dict()))
def to_manifest(schema:OutputSchema,ratified:frozenset[str]|_A=_A,sensitive_declared:frozenset[str]=frozenset(),mechanism:str='output-check',row_level:bool=_G)->Manifest:B=ratified;A=tuple(FieldDecl(A.name,A.field_class,A.transform,A.params,ratified=B is _A or A.name in B,tags=A.tags,load_bearing=A.load_bearing)for A in schema.columns);return Manifest(A,sensitive_declared,row_level,mechanism)