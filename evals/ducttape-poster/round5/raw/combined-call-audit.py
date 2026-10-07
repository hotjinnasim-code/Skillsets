#!/usr/bin/env python3
"""Read-only combined call accounting. Stored records are not exhaustive tool history."""
import datetime,hashlib,json,sys,argparse
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--allow-incomplete',action='store_true');args=parser.parse_args()
r=Path(__file__).resolve().parent
phases=[('D',r),('E',r/'continuation-e')]; records=[];errors=[];missing=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for name,root in phases:
 p=json.loads((root/'planning/phase-plan.json').read_text()); skill=root/('candidate-d-skill' if name=='D' else 'candidate-e-skill')
 actual={str(f.relative_to(skill)):sha(f) for f in skill.rglob('*') if f.is_file()}; expected={x['path']:x['sha256'] for x in p['frozen_skill_files']}
 if actual!=expected:errors.append(name+' frozen skill changed')
 for x in p.get('prior_closed_records_pinned',[])+p.get('closed_initial_reviews_pinned',[]):
  if sha(x['path'])!=x['sha256']:errors.append('Closed pin changed '+x['path'])
 phase_records=[]
 allowed_roles=set(p['scope']['new_original_roles']);allowed_stages={'initial','repair-1','repair-2'}
 for mf in (root/'production').rglob('manifest.json'):
  if len(mf.relative_to(root/'production').parts)!=3 or mf.parent.name not in allowed_stages or mf.parent.parent.name not in allowed_roles:errors.append('Unexpected manifest path '+str(mf))
 for role in p['scope']['new_original_roles']:
  rolepath=root/'production'/role; stages=list(rolepath.glob('*/manifest.json'))
  if not (rolepath/'initial/manifest.json').exists():missing.append(name+'/'+role+'/initial')
  unknown=[f for f in stages if f.parent.name not in {'initial','repair-1','repair-2'}]
  if unknown:errors.append('Unknown call stage '+str(unknown))
  repairs=[f for f in stages if f.parent.name.startswith('repair-')]
  if len(repairs)>2:errors.append('More than two corrections '+name+'/'+role)
  for f in sorted(stages):
   m=json.loads(f.read_text()); t=lambda v:datetime.datetime.fromisoformat(v.replace('Z','+00:00')).timestamp()
   phase_records.append({'phase':name,'role':role,'stage':m['stage'],'manifest':str(f),'manifest_sha256':sha(f),'native_sha256':m['final']['sha256'],'start':t(m['started_at_utc']),'end':t(m['completed_at_utc']),'count':m['native_call_count']})
  for d in rolepath.glob('*'):
   if d.is_dir() and any(d.iterdir()) and not (d/'manifest.json').exists():missing.append(name+'/'+role+'/'+d.name)
 if sum(x['count'] for x in phase_records)>p['scope']['phase_native_call_cap']:errors.append(name+' phase cap exceeded')
 records+=phase_records
peak=active=0
for _,change in sorted([(x['start'],1) for x in records]+[(x['end'],-1) for x in records]):active+=change;peak=max(peak,active)
if peak>3:errors.append('Across-phase native overlap exceeds environment three workers')
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'FAIL' if errors else ('INCOMPLETE' if missing else 'PASS'),'scope':'Manifest accounting and frozen/closed SHA pins only. Separate per-phase native/input validators and blind visual reviews remain necessary. Not exhaustive history, quality or authorship certification.','closed_history_before_round5':95,'D_recorded':sum(x['count'] for x in records if x['phase']=='D'),'D_cap':24,'E_recorded':sum(x['count'] for x in records if x['phase']=='E'),'E_cap':6,'whole_recorded':95+sum(x['count'] for x in records),'whole_maximum':125,'actual_native_interval_peak':peak,'logical_default_garden_maker_roles':5,'missing':missing,'errors':errors,'calls':records}
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(1 if errors or (missing and not args.allow_incomplete) else 0)
