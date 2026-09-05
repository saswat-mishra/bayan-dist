from __future__ import annotations
_k='docRefs'
_j='sensitivity'
_i='classification'
_h='1970-01-01T00:00:00Z'
_g='coarse'
_f='timestamp'
_e='+00:00'
_d='retrieval'
_c='product_version'
_b='model_version'
_a='prompt_version'
_Z='index_generation'
_Y='conversation_id'
_X='tool_name'
_W='guardrail_category'
_V='guardrail_tripped'
_U='doc_ref_count'
_T='hit_count'
_S='output_exact'
_R='input_exact'
_Q='output_bucket'
_P='input_bucket'
_O='latency_ms'
_N='latency_bucket'
_M='error_code'
_L='finish_reason'
_K='topic'
_J='tier'
_I='week'
_H='ts_hour'
_G='record_id'
_F='recordId'
_E='content_id'
_D='confidence'
_C='route'
_B='operation'
_A=None
import json,sqlite3
from pathlib import Path
from typing import Any
from bayan_core.crypto.canonical import canonical_json
def _backfill_leases(hdsn=_A):
	A=hdsn
	if not A:return()
	B=sorted(range(len(A)),key=lambda orwt:str(A[orwt]));return tuple(A[B]for B in B if A[B]is not _A)
h862='\nCREATE TABLE IF NOT EXISTS fingerprint (\n  record_id TEXT PRIMARY KEY, ts_bucket INTEGER NOT NULL, tier INTEGER NOT NULL, payload BLOB NOT NULL,\n  schema_version TEXT NOT NULL\n) STRICT;\nCREATE INDEX IF NOT EXISTS fp_roll ON fingerprint(ts_bucket, tier);\nCREATE TABLE IF NOT EXISTS fingerprint_flat (\n  record_id TEXT PRIMARY KEY, ts_hour TEXT NOT NULL, week TEXT NOT NULL, tier INTEGER NOT NULL, operation TEXT NOT NULL,\n  topic TEXT, route TEXT, finish_reason TEXT, error_code TEXT, latency_bucket TEXT, latency_ms REAL,\n  input_bucket TEXT, output_bucket TEXT, input_exact INTEGER, output_exact INTEGER, hit_count INTEGER,\n  doc_ref_count INTEGER, guardrail_tripped INTEGER, guardrail_category TEXT, confidence REAL, tool_name TEXT,\n  conversation_id TEXT, index_generation INTEGER, prompt_version TEXT, model_version TEXT, product_version TEXT,\n  content_id TEXT\n) STRICT;\nCREATE INDEX IF NOT EXISTS ff_topic ON fingerprint_flat(topic, week);\nCREATE TABLE IF NOT EXISTS doc_ref (record_id TEXT NOT NULL, doc_ref TEXT NOT NULL, rank INTEGER) STRICT;\nCREATE INDEX IF NOT EXISTS dr_ref ON doc_ref(doc_ref);\nCREATE TABLE IF NOT EXISTS content (\n  content_id TEXT PRIMARY KEY, record_id TEXT NOT NULL, prompt_text TEXT NOT NULL, response_text TEXT NOT NULL,\n  extra TEXT NOT NULL\n) STRICT;\n'
h862+='CREATE VIEW IF NOT EXISTS fingerprints AS SELECT '+', '.join((_G,_H,_I,_J,_B,_K,_C,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_D,_X,_Y,_Z,_a,_b,_c))+' FROM fingerprint_flat;\n'
h862+='CREATE VIEW IF NOT EXISTS doc_refs AS SELECT record_id, doc_ref, rank FROM doc_ref;\n'
s6m=_G,_H,_I,_J,_B,_K,_C,_L,_M,_N,_O,_P,_Q,_R,_S,_T,_U,_V,_W,_D,_X,_Y,_Z,_a,_b,_c
def czlx(path:Path)->sqlite3.Connection:path.parent.mkdir(parents=True,exist_ok=True);A=sqlite3.connect(path,check_same_thread=False,isolation_level=_A);A.row_factory=sqlite3.Row;A.execute('PRAGMA journal_mode = WAL');A.execute('PRAGMA synchronous = NORMAL');A.executescript(h862);return A
def qj3d(ts_hour:str)->str:from datetime import datetime as A;B=A.fromisoformat(ts_hour.replace('Z',_e));C,D,E=B.isocalendar();return f"{C}-W{D:02d}"
def en7(fp:dict[str,Any],content_id:str|_A)->dict[str,Any]:H='sha256';G='latency';D='topic-';C='tokens';A=fp;E=A.get(_C)or[];I=next((A[len(D):]for A in E if A.startswith(D)),_A);F=A.get(_f,{}).get(_g,_h);B=A.get('guardrails',{});return{_G:A[_F],_H:F,_I:qj3d(F),_J:A[_i].get(_j,1),_B:A[_B],_K:I,_C:'>'.join(A for A in E if not A.startswith(D))or _A,_L:A.get('finishReason'),_M:A.get('errorCode'),_N:A.get(G,{}).get('bucket'),_O:A.get(G,{}).get('ms'),_P:A.get(C,{}).get('inputBucket'),_Q:A.get(C,{}).get('outputBucket'),_R:A.get(C,{}).get('inputExact'),_S:A.get(C,{}).get('outputExact'),_T:A.get(_d,{}).get('hitCount'),_U:len(A.get(_d,{}).get(_k,[])),_V:(1 if B.get('tripped')else 0)if B else _A,_W:(B.get('categories')or[_A])[0]if B else _A,_D:A.get(_D),_X:(A.get('toolCalls',{}).get('names')or[_A])[0],_Y:A.get('conversationId'),_Z:A.get('indexVersion',{}).get('generation'),_a:A.get('promptVersion',{}).get(H),_b:A.get('modelVersion',{}).get(H),_c:A.get('productVersion'),_E:content_id}
def bnj3(conn:sqlite3.Connection,records:list[tuple[dict[str,Any],dict[str,Any]|_A]])->int:
	B=conn;D,E,F,G=[],[],[],[]
	for(A,C)in records:
		H=C[_E]if C else _A;J=int(wu9(A.get(_f,{}).get(_g,_h)));D.append((A[_F],J,A[_i].get(_j,1),canonical_json(A),A['schemaVersion']));K=en7(A,H);E.append(tuple(K[A]for A in(*s6m,_E)))
		for I in A.get(_d,{}).get(_k,[]):F.append((A[_F],I['ref'],I.get('rank')))
		if C:G.append((H,A[_F],C['prompt_text'],C['response_text'],json.dumps(C.get('extra',{}),ensure_ascii=False)))
	L=', '.join((*s6m,_E));B.execute('BEGIN');B.executemany('INSERT OR REPLACE INTO fingerprint VALUES (?,?,?,?,?)',D);B.executemany(f"INSERT OR REPLACE INTO fingerprint_flat ({L}) VALUES ({','.join('?'for A in range(len(s6m)+1))})",E);B.executemany('INSERT INTO doc_ref VALUES (?,?,?)',F);B.executemany('INSERT OR REPLACE INTO content VALUES (?,?,?,?,?)',G);B.execute('COMMIT');return len(D)
def wu9(ts:str)->float:
	from datetime import datetime as B,timezone as C;A=B.fromisoformat(ts.replace('Z',_e))
	if A.tzinfo is _A:A=A.replace(tzinfo=C.utc)
	return A.timestamp()//3600
def dw2(conn:sqlite3.Connection)->str:from bayan_core.crypto.canonical import sha256_hex as B;A=conn.execute('SELECT COUNT(*), MIN(record_id), MAX(record_id) FROM fingerprint_flat').fetchone();return B(f"{A[0]}|{A[1]}|{A[2]}".encode())
def g742(conn:sqlite3.Connection,name:str,rows:list[dict[str,Any]])->_A:
	C=rows;B=name;A=conn
	if not C:return
	D=sorted({B for A in C for B in A});A.execute(f'DROP TABLE IF EXISTS "{B}"');A.execute(f'CREATE TABLE "{B}" ({", ".join(chr(34)+A+chr(34)for A in D)})');A.executemany(f'INSERT INTO "{B}" VALUES ({",".join("?"for A in D)})',[[A.get(B)for B in D]for A in C]);A.commit()