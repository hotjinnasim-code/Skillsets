#!/usr/bin/env python3
"""Check the portable byte index and raw selected evidence without old source files."""
import argparse,hashlib,json,struct
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('archive',type=Path);a=p.parse_args();r=a.archive.resolve()
read=lambda p:json.loads(Path(p).read_text());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
index=read(r/'archive-index.json');errors=[];lookup={};checked=set()
def require(ok,why):
 if not ok:errors.append(why)
for entry in index['files']:
 source=entry['source_absolute'];target=r/entry['archive_relative'];require(source not in lookup,'Duplicate source index: '+source);lookup[source]=entry
 require(target.is_relative_to(r),'Archive path escaped: '+str(target));require(target.is_file(),'Missing archive file: '+str(target))
 if target.is_file():require(sha(target)==entry['sha256'],'Archive byte SHA differs: '+str(target));checked.add(str(target))
def resolve(source,expected=None):
 require(source in lookup,'Unmapped evidence source: '+source)
 if source not in lookup:return None
 entry=lookup[source];require(expected is None or entry['sha256']==expected,'Source pin differs: '+source);return r/entry['archive_relative']
f=read(r/'raw/planning/final-delivery-evidence.json');require(not f['binding_errors'],'Final selected binding errors present');require(type(f['predeclared_gate_pass']) is bool,'Final selected gate not boolean')
for key in ['current_summary','prior_selection_evidence']:
 resolve(f[key]['path'],f[key]['sha256'])
summary={};summarypath=resolve(f['current_summary']['path'],f['current_summary']['sha256'])
if summarypath:
 summary=read(summarypath)
 for ref in summary.get('source_summary_refs',summary.get('source_summaries',{})).values():resolve(ref['path'],ref['sha256'])
core={'content_form','typography','image_material','ai_slop'};image_records=0;quality_failures=[]
for role,item in f['selected_images'].items():
 native=resolve(item['final_native_absolute'],item['sha256'])
 if native:require(list(struct.unpack('>II',native.read_bytes()[16:24]))==[item['width'],item['height']],role+' native dimensions differ')
 require(set(item['views'])=={'native','usage720','thumbnail320'},role+' three-view binding missing')
 for view,record in item['views'].items():
  target=resolve(record['path'],record['sha256'])
  if target:require(list(struct.unpack('>II',target.read_bytes()[16:24]))==record['dimensions'],role+' view dimensions differ: '+view)
 for profile,critic in item['reviewers'].items():
  rawpath=resolve(critic['raw_report_absolute'],critic['raw_report_sha256']);image_records+=1
  if not rawpath:continue
  obs=read(rawpath)['images'][item['anonymous_id']]
  for field in ['mandatory','scores','evidence']:
   require(obs[field]==critic[field],role+' raw/final differs: '+profile+'/'+field)
  require(obs.get('residuals',[])==critic.get('residuals',[]),role+' residuals differ: '+profile)
  if obs['mandatory']['pass'] is not True:quality_failures.append(role+' mandatory FAIL: '+profile)
  require(len(obs['scores'])==7 and all(type(v) is int and 1<=v<=5 for v in obs['scores'].values()),role+' seven score anchors invalid')
  for dim in core:
   if obs['scores'][dim]<4:quality_failures.append(role+' '+dim+' core gate FAIL: '+profile)
for cid,item in f['sets'].items():
 expected={f['selected_images'][role]['anonymous_id']:f['selected_images'][role]['sha256'] for role in item['selected_roles']};require(expected==item['member_sha256'],cid+' set member SHA differs')
 for profile,critic in item['reviewers'].items():
  if 'raw_report_absolute' in critic:
   rawpath=resolve(critic['raw_report_absolute'],critic['raw_report_sha256'])
   if rawpath:require(read(rawpath)['sets'][cid]==critic['raw_set_observation'],cid+' retained raw set differs')
  else:
   rawpath=resolve(critic['raw_path'],critic['raw_sha256'])
   if rawpath:
    obs=read(rawpath)['sets'][cid]
    for field,value in obs.items():require(critic.get(field)==value,cid+' current raw set differs: '+field)
    require(set(obs['members'])==set(expected),cid+' raw set members differ')
  if len(expected)>1 and critic['diversity']<4:quality_failures.append(cid+' diversity gate FAIL: '+profile)
bundlepath=resolve(f['retained_binding_bundle']['path'],f['retained_binding_bundle']['sha256'])
if bundlepath:
 bundle=read(bundlepath)
 for pin in bundle['files']:resolve(pin['path'],pin['sha256'])
 require(f['review_procedure_retained']==bundle['review_procedure'],'Retained review procedure differs from pinned bundle')
 for wave,procedure in bundle['review_procedure'].items():
  for pin in procedure.get('scope_inputs',{}).values():
   if isinstance(pin,dict) and 'path' in pin and 'sha256' in pin:resolve(pin['path'],pin['sha256'])
  for profile,record in procedure.get('profiles',{}).items():
   if 'action_first_source' in record:
    pin=record['action_first_source'];target=resolve(pin['path'],pin['sha256'])
    if target:require(read(target)==record['action_first_raw_record'],wave+'/'+profile+' retained preflight differs')
for profile,procedure in f['review_procedure_current'].items():
 for pathkey,hashkey in [('raw_report','raw_report_sha256'),('action_first_record','action_first_sha256'),('raw_markdown','raw_markdown_sha256')]:
  resolve(procedure[pathkey],procedure[hashkey])
 require(procedure['valid_action_first_attestation'] is True,profile+' current preflight is not valid')
 rawpath=resolve(procedure['raw_report'],procedure['raw_report_sha256'])
 if rawpath:
  wave=procedure.get('source_review_wave',f['selected_images']['G01']['review_wave']);required_paths={record['path'] for item in f['selected_images'].values() if item['review_wave']==wave for record in item['views'].values()}
  observed_paths={record['path'] for record in read(rawpath)['viewed']};require(required_paths<=observed_paths,profile+' selected actual view paths missing');require(all(path in lookup for path in required_paths),profile+' selected view archive missing')
transfer=f.get('required_transfer_evidence');transfer_records=0;transfer_failures=[]
g_source=Path(index['source_root'])/'continuation-g'
transfer_required=any(Path(x.get('manifest','')).is_relative_to(g_source) for x in f['selected_images'].values())
require(not transfer_required or transfer is not None,'Predeclared G control evidence omitted')
if transfer is not None:
 require(summary.get('required_transfer_evidence')==transfer,'Final transfer differs from pinned composite summary')
 for key in ['source_summary_ref','source_plan','source_cases']:
  ref=transfer[key];resolve(ref['path'],ref['sha256'])
 require(len(transfer['image_bindings'])==1 and len(transfer['image_critic_records'])==3,'Required transfer coverage differs')
 b=transfer['image_bindings'][0];require(b['role']=='T01' and b['phase']=='G','Required transfer role/phase differs')
 target=resolve(b['selected_native'],b['native_sha256']);manifest=resolve(b['manifest'],b['manifest_sha256'])
 if manifest:
  m=read(manifest);require(m['role']=='T01' and m['stage']==b['stage'] and m['final']['sha256']==b['native_sha256'],'Required transfer manifest differs')
 require(set(b['views'])=={'native','usage720','thumbnail320'},'Required transfer three views missing')
 for view,rec in b['views'].items():
  target=resolve(rec['path'],rec['sha256'])
  if target:require(list(struct.unpack('>II',target.read_bytes()[16:24]))==rec['dimensions'],'Required transfer dimensions differ: '+view)
 require(set(x['profile'] for x in transfer['image_critic_records'])==set(b['critic_profiles']),'Required transfer critic profiles differ')
 for rec in transfer['image_critic_records']:
  rawpath=resolve(rec['raw_path'],rec['raw_sha256']);transfer_records+=1
  if not rawpath:continue
  raw=read(rawpath);obs=raw['images'][b['image_id']]
  for field in ['mandatory','scores','evidence']:
   require(obs[field]==rec[field],'Required transfer raw/final differs: '+field)
  require(obs.get('residuals',[])==rec.get('residuals',[]),'Required transfer residuals differ')
  require(len(obs['scores'])==7 and all(type(v) is int and 1<=v<=5 for v in obs['scores'].values()),'Required transfer anchors invalid')
  require({v['path'] for v in b['views'].values()}<={v['path'] for v in raw['viewed']},'Required transfer actualview entries missing')
  if obs['mandatory']['pass'] is not True:transfer_failures.append('T01 mandatory FAIL: '+rec['profile'])
  for dim in core:
   if obs['scores'][dim]<4:transfer_failures.append('T01 '+dim+' core FAIL: '+rec['profile'])
 for rec in transfer['all_set_records']:
  rawpath=resolve(rec['raw_path'],rec['raw_sha256'])
  if not rawpath:continue
  obs=read(rawpath)['sets'][rec['case_id']]
  for field,value in obs.items():require(rec.get(field)==value,'Required transfer raw singleton differs: '+field)
  require(obs['members']==[b['image_id']] and obs.get('diversity') is None and obs.get('closest_pair')==[] and obs.get('closest_pair_score') is None,'Required transfer invented pair/diversity')
 for profile,proc in transfer['review_procedure'].items():
  for pk,hk in [('raw_report','raw_report_sha256'),('action_first_record','action_first_sha256'),('raw_markdown','raw_markdown_sha256')]:resolve(proc[pk],proc[hk])
  require(proc['valid_action_first_attestation'] is True,'Required transfer source preflight invalid: '+profile)
 require(transfer['predeclared_transfer_gate']==('FAIL' if transfer_failures else 'PASS'),'Required transfer declared gate differs from raw')
 quality_failures.extend(transfer_failures)
require(len(f['selected_images'])==14 and len(f['sets'])==6,'Selected14/6cases missing');require(image_records==f['image_critic_records'],'Critic record count differs')
require(f['predeclared_gate_pass']==(not quality_failures),'Final declared quality gate differs from raw observations');require(index['predeclared_selected_gate_pass']==f['predeclared_gate_pass'],'Archive declared quality gate differs')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','selected_quality_gate':'FAIL' if quality_failures else 'PASS','quality_failure_count':len(quality_failures),'scope':'Portable exact bytes and raw score/copy/evidence bindings. Byte integrity is separate from raw selected-quality gate; not an independent visual rescore, exhaustive tool history or universal future/authorship/print certification.','mapped_sources':len(lookup),'unique_files_checked':len(checked),'selected_images':len(f['selected_images']),'selected_critic_records':image_records,'errors':errors},ensure_ascii=False,indent=2));raise SystemExit(1 if errors else 0)
