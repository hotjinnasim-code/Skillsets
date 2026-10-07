#!/usr/bin/env python3
"""Preserve exact evidence bytes with an explicit portable source-to-blob index.
No native images are rendered, recomposed or rescaled by this archive tool.
"""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--destination',type=Path,required=True);ap.add_argument('--final-evidence',type=Path,required=True);ap.add_argument('--allow-failed',action='store_true',help='Preserve a closed failed evaluation with explicit FAIL status; never changes scores or gate.');a=ap.parse_args();r=Path(__file__).resolve().parent;dest=a.destination.resolve();assert not dest.exists(),'Preserve existing archive; use an explicit new destination.';assert not dest.is_relative_to(r),'Archive destination must be outside source root.'
evidence=json.loads(a.final_evidence.read_text());assert type(evidence['predeclared_gate_pass']) is bool;assert evidence['predeclared_gate_pass'] or a.allow_failed,'Final gate is not PASS; explicitly use --allow-failed for a failed closed archive.'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();index=[];seen={};native_hashes=set();sources=set()
def archive(src,rel,kind):
 src=Path(src).resolve();assert src.is_file(),str(src);h=sha(src);target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if str(src) in seen:
  assert sha(dest/seen[str(src)])==h
  return
 if not target.exists():shutil.copyfile(src,target)
 assert sha(target)==h
 index.append({'source_absolute':str(src),'archive_relative':str(rel),'sha256':h,'kind':kind});seen[str(src)]=str(rel)
for phase,root in [('D',r),('E',r/'continuation-e'),('F',r/'continuation-f'),('G',r/'continuation-g')]:
 for mf in (root/'production').rglob('manifest.json'):
  m=json.loads(mf.read_text())
  for key in ['tool_source','original','final']:
   p=Path(m[key]['path']);assert sha(p)==m[key]['sha256'];sources.add(p.resolve());native_hashes.add(m[key]['sha256'])
for packet_path in r.glob('blind-*/packet.json'):
 for item in json.loads(packet_path.read_text())['images']:
  p=Path(item['native']);assert p.is_file();native_hashes.add(sha(p))
bundle_source=Path(evidence['retained_binding_bundle']['path']);assert sha(bundle_source)==evidence['retained_binding_bundle']['sha256'];bundle=json.loads(bundle_source.read_text())
for item in bundle['files']:
 p=Path(item['path']);assert sha(p)==item['sha256']
 if p.suffix.lower()=='.png':sources.add(p.resolve())
 else:archive(p,Path('retained-context')/(sha(p)+p.suffix),'retained exact context/raw metadata')
for plan_path in [r/'planning/phase-plan.json',r/'continuation-e/planning/phase-plan.json',r/'continuation-f/planning/phase-plan.json',r/'continuation-g/planning/phase-plan.json']:
 plan=json.loads(plan_path.read_text())
 for key in ['prior_closed_records_pinned','closed_initial_reviews_pinned']:
  for item in plan.get(key,[]):
   p=Path(item['path']);assert sha(p)==item['sha256']
   if not p.is_relative_to(r):archive(p,Path('retained-context')/(sha(p)+p.suffix),'closed phase plan pin')
for item in json.loads((r/'planning/research-provenance.json').read_text())['source_records']:
 p=Path(item['path']);assert sha(p)==item['sha256'];archive(p,Path('retained-context')/(sha(p)+p.suffix),'reused research provenance metadata; no publisher pixels')
for item in evidence['selected_images'].values():
 p=Path(item['final_native_absolute']);assert sha(p)==item['sha256'];sources.add(p.resolve());native_hashes.add(item['sha256'])
 for critic in item['reviewers'].values():
  p=Path(critic['raw_report_absolute']);assert sha(p)==critic['raw_report_sha256']
  if not p.is_relative_to(r):archive(p,Path('retained-reviews')/(sha(p)+p.suffix),'retained raw review')
  md=p.with_suffix('.md')
  if md.is_file() and not md.is_relative_to(r):archive(md,Path('retained-reviews')/(sha(md)+md.suffix),'retained raw review markdown')
transfer=evidence.get('required_transfer_evidence')
if transfer:
 for key in ['source_summary_ref','source_plan','source_cases']:
  item=transfer[key];p=Path(item['path']);assert sha(p)==item['sha256']
  if not p.is_relative_to(r):archive(p,Path('retained-context')/(sha(p)+p.suffix),'required transfer source metadata')
 for item in transfer['image_bindings']:
  assert item['role']=='T01';p=Path(item['selected_native']);assert sha(p)==item['native_sha256'];sources.add(p.resolve());native_hashes.add(item['native_sha256'])
  for view,record in item['views'].items():
   p=Path(record['path']);assert sha(p)==record['sha256'];sources.add(p.resolve())
 for item in transfer['image_critic_records']:
  p=Path(item['raw_path']);assert sha(p)==item['raw_sha256']
  if not p.is_relative_to(r):archive(p,Path('retained-reviews')/(sha(p)+p.suffix),'required transfer raw review')
for p in r.rglob('*'):
 if not p.is_file():continue
 if p.suffix in {'.json','.md','.txt','.py','.yaml','.yml'}:
  archive(p,Path('raw')/p.relative_to(r),'exact raw/source/tooling bytes')
 elif p.suffix.lower()=='.png':sources.add(p.resolve())
for p in sorted(sources):
 h=sha(p);kind='native' if h in native_hashes else 'qa';archive(p,Path('images')/kind/(h+'.png'),kind+' exact preserved image bytes')
(dest/'archive-index.json').write_text(json.dumps({'archived_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_root':str(r),'predeclared_selected_gate_pass':evidence['predeclared_gate_pass'],'scope':'Exact byte archive of all Round5 D/E/F/G recorded native calls and QA, current/retained selected14 actual views, separate required G T01 transfer evidence, retained wave context and pinned closed phase metadata. T01 is not counted as a selected14 image. D/E retirement and separate F6/G9 maximum131 history remain recorded without cap reset. Prior full packets/reviews may reference unselected older comparator images outside this archive; not an all-old-native-image archive. Raw source paths remain unchanged; this explicit index resolves each included source path to preserved archive bytes. No basename fallback, image editing or quality/authorship certification. Native hashes deduplicate identical tool-source/original/final/anonymous copies; no new image is inferred.','files':index,'unique_native_image_hashes':sorted(native_hashes),'file_count':len(index)},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'destination':str(dest),'mapped_sources':len(index),'unique_native_images':len(native_hashes),'final_gate':evidence['predeclared_gate_pass']}))
