#!/usr/bin/env python3
"""Resolve exact source pins only through portable archive index; no source checkout needed."""
from pathlib import Path
import argparse,hashlib,json,struct
p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path);a=p.parse_args();r=a.archive.resolve()
read=lambda x:json.loads(Path(x).read_text());sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
errors=[];index=read(r/'archive-index.json');lookup={};checked=set()
def need(ok,msg):
 if not ok:errors.append(msg)
for x in index['files']:
 out=r/x['archive_relative'];need(out.is_relative_to(r),'Archive path escaped');need(x['source_absolute'] not in lookup,'Duplicate indexed source');lookup[x['source_absolute']]=x
 need(out.is_file(),'Missing blob: '+str(out))
 if out.is_file():need(sha(out)==x['sha256'],'Blob byte mismatch: '+str(out));checked.add(str(out))
def resolve(source,h=None):
 need(source in lookup,'Unmapped source: '+str(source))
 if source not in lookup:return None
 x=lookup[source];need(h is None or x['sha256']==h,'Pin mismatch: '+source);return r/x['archive_relative']
def pin(v):return resolve(v['path'],v['sha256'])
e=read(r/'raw/planning/final-evidence.json');calls=read(pin(e['call_validation']))
need(calls['status']=='PASS' and calls['call_phase']=='CLOSED' and calls['recorded_attempts']<=60,'Call history not closed within cap')
need(calls['prior_R5_closed_recorded']==128 and calls['prior_R5_retirement_unchanged'] is True,'Prior closed history differs')
need(len(e['images'])==20 and len(e['sets'])==4,'20/four-context scope missing')
need(e['recorded_evidence_integrity']=='PASS' and not e['integrity_errors'],'Final recorded evidence invalid')
for ref in e['summary_refs'].values():pin(ref)
core={'content_form','typography','image_material','ai_slop'};quality=[];observations=0
for role,x in e['images'].items():
 for stage,b,obs in [('initial',x['initial_binding'],x['initial_reviewers']),('final',x['binding'],x['reviewers'])]:
  native=resolve(b['source_native'],b['native_sha256']);manifest=resolve(b['source_manifest'],b['source_manifest_sha256'])
  if manifest:
   m=read(manifest);need(m['role']==role and m['stage']==b['stage'] and m['final']['sha256']==b['native_sha256'],role+' manifest binding differs')
   for field in ('tool_source','original','final'):pin(m[field])
   for q in m['qa_views'].values():pin(q)
  need(set(b['views'])=={'native','usage720','thumbnail320'},role+' missing three views')
  for v in b['views'].values():
   out=pin(v)
   if out:need(list(struct.unpack('>II',out.read_bytes()[16:24]))==v['dimensions'],role+' view dimensions differ')
  need({o['profile'] for o in obs}=={'editorial','craft','portfolio'},role+' critic coverage differs')
  for o in obs:
   raw=resolve(o['raw_path'],o['raw_sha256']);observations+=1
   if raw:
    d=read(raw);z=d['images'][b['image_id']]
    for key in ('mandatory','scores','evidence','residuals'):need(z[key]==o[key],role+'/'+stage+' raw copied observation differs: '+key)
    need({v['path'] for v in b['views'].values()}<={v['path'] for v in d['viewed']},role+' recorded views missing')
    need(len(z['scores'])==7 and all(type(n) is int and 1<=n<=5 for n in z['scores'].values()),role+' invalid seven scores')
    if stage=='final' and (z['mandatory']['pass'] is not True or not z['mandatory']['use_readings']['all_required_copy_legible_at720'] or any(z['scores'][k]<4 for k in core)):quality.append(role+'/'+o['profile'])
 pin(x['ordinary_selection'])
for cid,x in e['sets'].items():
 for stage in ('initial','final'):
  expected={e['images'][role]['initial_binding' if stage=='initial' else 'binding']['image_id'] for role in x['roles']}
  for o in x[stage+'_reviewers']:
   raw=resolve(o['raw_path'],o['raw_sha256'])
   if raw:
    z=read(raw)['sets'][cid]
    need(set(z['members'])==expected,cid+' complete set members differ')
    for key in ('members','diversity','closest_pair','evidence','residuals'):need(z[key]==o[key],cid+' raw set observation differs')
   if stage=='final' and o['diversity']<4:quality.append(cid+'/'+o['profile']+' diversity')
for ref in e['summary_refs'].values():
 out=pin(ref)
 if not out:continue
 s=read(out)
 for v in s['source_pin_checks']:resolve(v['path'],v['expected_sha256'])
 for proc in s['review_procedure'].values():
  for key,hkey in [('raw_report','raw_report_sha256'),('raw_markdown','raw_markdown_sha256'),('preflight','preflight_sha256')]:
   if key in proc:resolve(proc[key],proc[hkey])
  need(proc['order_compliant'] is True and proc['preflight_order_compliant'] is True,'Preflight order attestation invalid')
 need(s['recorded_evidence_integrity']=='PASS','Source summary invalid')
need(observations==120,'First/final 120 critic observations missing')
need((e['predeclared_core_diversity_gate']=='PASS')==(not quality and all(s['final_case_gate']=='PASS' for s in e['sets'].values())),'Declared gate contradicts raw observations')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','scope':'Portable bytes and exact raw/source bindings only; no independent visual rescore or actual-view/order proof. First/final reuse is explicit.','mapped_sources':len(lookup),'unique_files_checked':len(checked),'image_critic_records_first_and_final':observations,'final_quality_gate':e['predeclared_core_diversity_gate'],'raw_final_mandatory_core_diversity_failures':len(quality),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
