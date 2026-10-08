from pathlib import Path
import json,hashlib
A=Path("/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6").resolve()
O=Path("/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6-final-auditor-fixes")
def read(rel, binary=False):
 p=(A/rel).resolve()
 if not p.is_relative_to(A): raise ValueError("Archive confinement violation: "+str(rel))
 b=p.read_bytes()
 rows=json.loads((O/"files-read.json").read_text())
 row={"path":str(p),"archive_relative_path":str(p.relative_to(A)),"sha256":hashlib.sha256(b).hexdigest()}
 if row not in rows: rows.append(row)
 (O/"files-read.json").write_text(json.dumps(rows,indent=2)+"\n")
 return b if binary else b.decode()
def js(rel): return json.loads(read(rel))
