"""Recorded native bytes and accounting only; not a visual quality certificate."""
from pathlib import Path
import argparse,json,hashlib,struct,datetime as dt
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--allow-incomplete',action='store_true');a=p.parse_args();r=a.source_root.resolve();parent=r.parent
errors=[];missing=[];records=[];saved_input_filenames={}
def check(ok,message):
 if not ok:errors.append(message)
def read(path):
 if not path.is_file():missing.append(str(path));return None
 try:return json.loads(path.read_text())
 except Exception as e:errors.append(str(path)+': '+str(e));return None
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def utc(value):
 if value.endswith(' UTC'):return dt.datetime.strptime(value,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=dt.timezone.utc)
 parsed=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
 if parsed.tzinfo is None:raise ValueError('missing timezone')
 return parsed.astimezone(dt.timezone.utc)
plan=read(r/'planning/phase-plan.json');frozen=read(r/'planning/candidate-d-hashes.json')
if plan:
 check((parent/'call-ledger.json').is_file() and sha(parent/'call-ledger.json')==plan['closed_C_ledger_sha256'],'closed C ledger missing or changed')
 check((parent.parent/'ducttape-poster-round3/call-ledger.json').is_file() and sha(parent.parent/'ducttape-poster-round3/call-ledger.json')==plan['closed_round3_ledger_sha256'],'closed round3 ledger missing or changed')
 check(plan['D_maximum_native_calls']==9 and plan['maximum_C_plus_D_calls']==41 and plan['overall_round4_cap_unchanged']==42 and plan['overall_round3_plus_round4_cap_unchanged']==76,'declared call boundary changed')
if frozen:
 check(len(frozen['files'])==6 and {str(x.relative_to(r/'candidate-d-skill')) for x in (r/'candidate-d-skill').rglob('*') if x.is_file()}==set(frozen['files']),'D frozen tree is not the declared six files')
 for name,v in frozen['files'].items():
  file=r/'candidate-d-skill'/name
  check(file.is_file() and sha(file)==v['sha256'] and file.stat().st_size==v['bytes'],'frozen D mismatch: '+name)
roles={'C02':3/2,'P01':4/5,'H02':1}
raw=read(r/'planning/raw-requests.json')
copy_by_role={slot['id']:case['copy'] for case in raw['cases'] for slot in case['slots'] if slot['id'] in roles} if raw else {}
for role,ratio in roles.items():
 stage_dirs=[r/'production-d'/role]+[r/'production-d'/role/f'repair-{i}' for i in [1,2]]
 for i,d in enumerate(stage_dirs):
  file=d/'manifest.json'
  if not file.is_file():
   if i==0:missing.append(str(file))
   continue
  m=read(file)
  if not m:continue
  stage='initial' if i==0 else f'repair-{i}'
  check(m.get('slot_id')==role and m.get('stage')==stage,'manifest role/stage mismatch '+role+'/'+stage)
  check(m.get('native_image_call_count')==1,'recorded stage call count is not one '+role+'/'+stage)
  inp=m.get('call_input',m.get('actual_call_input'))
  check(isinstance(inp,dict),'missing actual input '+role+'/'+stage)
  if isinstance(inp,dict):
   input_path=d/'call-input.json'
   if not input_path.is_file() and (d/'call-input-actual.json').is_file():input_path=d/'call-input-actual.json'
   saved_input_filenames[role+'/'+stage]=input_path.name
   saved_input=read(input_path)
   check(saved_input==inp,'saved exact call-input mismatch '+role+'/'+stage)
   check(inp.get('transparent_background') is False,'unexpected background '+role+'/'+stage)
   check(role in copy_by_role and all(value in inp.get('prompt','') for value in copy_by_role[role]),'original copy absent from native prompt '+role+'/'+stage)
   check(set(inp)<={'prompt','transparent_background','referenced_image_paths','num_last_images_to_include'},'unsupported native argument '+role+'/'+stage)
   check(not ('referenced_image_paths'in inp and 'num_last_images_to_include'in inp),'both reference mechanisms '+role+'/'+stage)
   if i==0:check(not ({'referenced_image_paths','num_last_images_to_include'}&set(inp)),'D initial references prior image '+role)
   else:
    check('num_last_images_to_include' not in inp,'D local edit used conversation history '+role+'/'+stage)
    if 'referenced_image_paths'in inp:
     allowed=[str(stage_dirs[i-1]/'final.png')]
     check(inp['referenced_image_paths']==allowed,'D edit reference not own immediate source '+role+'/'+stage)
   check((d/'prompt.txt').is_file() and (d/'prompt.txt').read_text().rstrip('\n')==inp['prompt'].rstrip('\n'),'saved prompt mismatch '+role+'/'+stage)
   try:
    start,end=utc(m['call_started_at_utc']),utc(m['call_finished_at_utc'])
    check(end>=start,'invalid recorded native interval '+role+'/'+stage)
    for prefile in ['prompt.txt',input_path.name]:
     f=d/prefile
     # UTC strings from the clock may have only whole-second precision.
     check(f.is_file() and f.stat().st_mtime<start.timestamp()+1,'pre-call file timestamp inconsistent with recorded start '+role+'/'+stage+'/'+prefile)
   except (KeyError,ValueError,TypeError) as e:errors.append('invalid/missing native timing '+role+'/'+stage+': '+str(e))
  source=Path(m.get('tool_original_path',m.get('source_path','')));paths=[source,d/'native-original.png',d/'final.png']
  check(len(set(map(str,paths)))==3,'native copies not distinct '+role+'/'+stage)
  if all(x.is_file() for x in paths):
   digests=[sha(x) for x in paths];check(len(set(digests))==1 and digests[0]==m.get('final_sha256',m.get('sha256')),'native bytes/hash mismatch '+role+'/'+stage)
   for field in ['sha256','source_sha256','original_sha256','final_sha256']:
    check(m.get(field)==digests[0],'manifest '+field+' mismatch '+role+'/'+stage)
   data=paths[-1].read_bytes();check(data[:8]==b'\x89PNG\r\n\x1a\n','non-PNG native '+role+'/'+stage)
   width,height=struct.unpack('>II',data[16:24]);check(abs((width/height)/ratio-1)<=.01,'ratio mismatch '+role+'/'+stage)
   dim=m.get('output_dimensions',{});check(dim.get('width')==width and dim.get('height')==height,'dimension mismatch '+role+'/'+stage)
  else:missing.extend(str(x) for x in paths if not x.is_file())
  records.append({'slot_id':role,'stage':stage,'manifest_path':str(file.relative_to(r))})
 check(not (stage_dirs[2]/'manifest.json').is_file() or (stage_dirs[1]/'manifest.json').is_file(),'repair2 missing repair1 '+role)
 extra=list((r/'production-d'/role).glob('repair-*/manifest.json'));check(len(extra)<=2 and all(x.parent.name in ['repair-1','repair-2'] for x in extra),'more than two own D repairs '+role)
check(len(records)<=9 and 32+len(records)<=42 and 34+32+len(records)<=76,'call cap exceeded')
ledger=read(r/'call-ledger.json')
if ledger:check(sorted(ledger['calls'],key=lambda x:(x['slot_id'],x['stage']))==sorted(records,key=lambda x:(x['slot_id'],x['stage'])) and ledger['recorded_native_calls']==len(records),'D ledger mismatch')
selection=read(r/'final-selection.json')
if selection:
 items=selection['selected'];check(len(items)==3 and {x['slot_id'] for x in items}==set(roles),'D selected count/roles')
 for x in items:
  file=r/x['final_native'];check(file.is_file() and sha(file)==x['sha256'],'D selected hash mismatch '+x['slot_id'])
  role=x['slot_id'];stage=x.get('stage');directory=r/'production-d'/role if stage=='initial' else r/'production-d'/role/str(stage)
  check(role in roles and stage in ['initial','repair-1','repair-2'] and file==directory/'final.png','D selected role/stage path mismatch '+role)
  selected_manifest=read(directory/'manifest.json')
  if selected_manifest:check(x['sha256']==selected_manifest['final_sha256'] and x.get('width')==selected_manifest['output_dimensions']['width'] and x.get('height')==selected_manifest['output_dimensions']['height'],'D selected manifest binding mismatch '+role)
status='FAIL' if errors else ('INCOMPLETE' if missing else 'PASS')
result={'status':status,'scope':__doc__,'precall_scope':'Exact saved input equality and filesystem timestamp consistency with one-second clock precision; not exhaustive tool-history or native invocation-order certification. Prompt comparison ignores terminal LF only. Existing call-input-actual.json is an explicit filename alias; no records are recreated or timestamps changed.','saved_input_filenames':saved_input_filenames,'D_calls':len(records),'C_plus_D_calls':32+len(records),'round3_C_D_calls':66+len(records),'errors':errors,'missing':missing}
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(1 if errors or (missing and not a.allow_incomplete) else 0)
