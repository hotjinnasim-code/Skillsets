#!/usr/bin/env python3
"""Exact byte archive and explicit original-source-to-blob mapping, including failures."""
from pathlib import Path
import argparse,datetime,hashlib,json,shutil
r=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--destination',required=True,type=Path);a=p.parse_args();d=a.destination.resolve()
assert not d.exists() and not d.is_relative_to(r),'Existing archive or source-contained destination refused'
read=lambda x:json.loads(Path(x).read_text());sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
closed=read(r/'planning/calls-closed.json');assert closed['status']=='PASS' and closed['call_phase']=='CLOSED'
e=read(r/'planning/final-evidence.json');assert len(e['images'])==20 and e['recorded_evidence_integrity']=='PASS'
native={m['final']['sha256'] for f in (r/'production').glob('*/*/manifest.json') for m in [read(f)]};sources=set();index=[];seen={}
def add(src,rel,kind):
 src=Path(src).resolve();assert src.is_file(),str(src);h=sha(src)
 if str(src) in seen:return
 out=d/rel;out.parent.mkdir(parents=True,exist_ok=True)
 if not out.exists():shutil.copyfile(src,out)
 assert sha(out)==h
 seen[str(src)]=str(rel);index.append(dict(source_absolute=str(src),archive_relative=str(rel),sha256=h,kind=kind))
for f in (r/'production').glob('*/*/manifest.json'):
 m=read(f)
 for key in ('tool_source','original','final'):
  v=m[key];assert sha(v['path'])==v['sha256'];sources.add(Path(v['path']).resolve())
for pin in read(r/'planning/phase-plan.json')['prior_closed_records']:
 assert sha(pin['path'])==pin['sha256'];add(pin['path'],Path('retained-context')/(pin['sha256']+'.json'),'prior closed metadata only')
for f in r.rglob('*'):
 if not f.is_file() or '__pycache__' in f.parts:continue
 if f.suffix.lower()=='.png':sources.add(f.resolve())
 else:add(f,Path('raw')/f.relative_to(r),'exact raw source/protocol/evidence/tooling bytes')
for f in sorted(sources):
 h=sha(f);kind='native' if h in native else 'qa';add(f,Path('images')/kind/(h+'.png'),kind+' exact bytes')
(d/'archive-index.json').write_text(json.dumps(dict(archived_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_root=str(r),source_commit=e['source_commit'],scope='All new R6 native stages including unused originals and repairs, all raw observations, exact frozen skill and closed prior history metadata. Native source/original/final/anonymous duplicates map to one hash blob. Source paths are preserved in raw records and resolved explicitly by this index. No retouching, native upscaling or publisher-image copying.',files=index,file_count=len(index),unique_native_hashes=sorted(native),selected_image_count=20,final_quality_gate=e['predeclared_core_diversity_gate']),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(destination=str(d),mapped_sources=len(index),unique_native_images=len(native),selected_images=20,quality_gate=e['predeclared_core_diversity_gate'])))
