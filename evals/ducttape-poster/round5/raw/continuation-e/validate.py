#!/usr/bin/env python3
"""Read-only recorded-call, frozen-source and exact-native-byte verification.
Visual typography/copy/style quality remains separate independent image evidence.
"""
import argparse, datetime as dt, hashlib, json, struct, zlib
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);parser.add_argument('--allow-incomplete',action='store_true');a=parser.parse_args();r=a.root.resolve()
errors=[];missing=[];records=[]
def require(ok,msg):
 if not ok: errors.append(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def time(v): return dt.datetime.fromisoformat(v.replace('Z','+00:00')).timestamp()
def path(v,base):
 p=Path(v);return p if p.is_absolute() else base/p
p=read(r/'planning/phase-plan.json')
allowed_roles=set(p['scope']['new_original_roles']); allowed_stages={'initial','repair-1','repair-2'}
for rolepath in (r/'production').glob('*'):
 if not rolepath.is_dir(): continue
 require(rolepath.name in allowed_roles,'Unexpected production role: '+str(rolepath))
 for stagepath in rolepath.glob('*'):
  if stagepath.is_dir():require(stagepath.name in allowed_stages,'Unexpected production stage: '+str(stagepath))
for mf in (r/'production').rglob('manifest.json'):
 require(len(mf.relative_to(r/'production').parts)==3 and mf.parent.name in allowed_stages and mf.parent.parent.name in allowed_roles,'Unexpected completed manifest path: '+str(mf))
expected={x['path']:x['sha256'] for x in p['frozen_skill_files']}
actual={str(x.relative_to(r/'candidate-e-skill')):sha(x) for x in (r/'candidate-e-skill').rglob('*') if x.is_file()}
require(actual==expected,'Frozen six-file tree/hash changed')
for x in p['prior_closed_records_pinned']+p.get('closed_initial_reviews_pinned',[]):require(sha(Path(x['path']))==x['sha256'],'Prior closed record changed: '+x['path'])
for role in p['scope']['new_original_roles']:
 packet=read(r/f'planning/packets/{role}.json');num,den=map(int,packet['assigned_ratio'].split(':'));ratio=num/den
 previous=None
 for stage in ['initial','repair-1','repair-2']:
  base=r/'production'/role/stage;mf=base/'manifest.json'
  if not mf.exists():
   if stage=='initial':missing.append(str(mf))
   elif base.exists() and any(base.iterdir()):missing.append(str(mf))
   continue
  try:
   m=read(mf);require(m.get('role')==role and m.get('stage')==stage,'Role/stage mismatch: '+str(mf));require(type(m.get('native_call_count')) is int and m.get('native_call_count')==1,'Callcount mismatch: '+str(mf))
   inp=m['call_input'];args=read(base/'call-input.json');require(args==inp,'Pre-call input differs from manifest: '+str(mf))
   require(set(args)<= {'prompt','transparent_background','referenced_image_paths','num_last_images_to_include'},'Unsupported recorded argument: '+str(mf))
   require(args.get('transparent_background') is False,'Transparency mismatch: '+str(mf));require((base/'prompt.txt').read_text().rstrip('\n')==args['prompt'].rstrip('\n'),'Prompt mismatch beyond terminal LF: '+str(mf))
   for copy in packet['case']['copy']:require(copy in args['prompt'],'Full required copy absent in actual prompt '+role+': '+copy)
   require('현재 도구와 모델이 지원하는 가능한 최대 해상도' in args['prompt'],'Maximum-resolution request absent: '+str(mf))
   start=time(m['started_at_utc']);end=time(m['completed_at_utc']);require(start<=end,'Recorded end precedes start: '+str(mf))
   require((base/'call-input.json').stat().st_mtime<=start+1,'Saved input mtime after recorded call start: '+str(mf))
   if stage=='initial':require('referenced_image_paths' not in args and 'num_last_images_to_include' not in args,'Initial uses image reference: '+str(mf))
   else:
    if stage=='repair-2':require((r/'production'/role/'repair-1/manifest.json').exists(),'Repair2 skips own Repair1: '+str(mf))
    require(previous is not None,'Repair lacks previous own stage: '+str(mf))
    require(not ('referenced_image_paths' in args and 'num_last_images_to_include' in args),'Two image reference mechanisms: '+str(mf))
    if 'referenced_image_paths' in args:
     require(len(args['referenced_image_paths'])==1,'Repair referencecount not1: '+str(mf))
     require(sha(Path(args['referenced_image_paths'][0]))==previous['sha256'],'Repair refers to another image: '+str(mf))
   natives=[]
   for key in ['tool_source','original','final']:
    item=m[key];fp=path(item['path'],base);require(fp.is_file(),'Missing native '+key+': '+str(fp));h=sha(fp);require(h==item['sha256'],'Native SHA mismatch '+key+': '+str(mf));natives.append((fp,h))
   require(len({str(x[0].resolve()) for x in natives})==3,'Three native file paths not distinct: '+str(mf));require(len({x[1] for x in natives})==1,'Native bytes differ: '+str(mf))
   data=natives[1][0].read_bytes();require(data[:8]==b'\x89PNG\r\n\x1a\n','Native format not supported PNG: '+str(mf));w,h=struct.unpack('>II',data[16:24]);require((w,h)==(m['width'],m['height']),'PNG dimension mismatch: '+str(mf));require(abs(w/h-ratio)/ratio<=.01,'Ratio relative error >1percent: '+str(mf))
   off=8
   while off<len(data):
    n=struct.unpack('>I',data[off:off+4])[0];kind=data[off+4:off+8];payload=data[off+8:off+8+n];crc=struct.unpack('>I',data[off+8+n:off+12+n])[0];require(zlib.crc32(kind+payload)&0xffffffff==crc,'PNG chunk CRC mismatch: '+str(mf));off+=12+n
    if kind==b'IEND':break
   require(off==len(data),'PNG trailing/missing data: '+str(mf))
   previous={'path':str(natives[2][0]),'sha256':natives[2][1]};records.append({'role':role,'stage':stage,'manifest':str(mf),'manifest_sha256':sha(mf),'native_sha256':natives[2][1],'width':w,'height':h,'start':start,'end':end})
  except Exception as e:errors.append(str(mf)+': '+type(e).__name__+': '+str(e))
require(len(records)<=p['scope']['phase_native_call_cap'],'Round5 cap exceeded')
events=sorted([(x['start'],1) for x in records]+[(x['end'],-1) for x in records]);active=peak=0
for _,change in events:active+=change;peak=max(peak,active)
require(peak<=p['scope']['environment_maximum_concurrent_makers'],'Recorded native call peak exceeds declared environment capacity')
status='FAIL' if errors else ('INCOMPLETE' if missing else 'PASS')
print(json.dumps({'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':status,'scope':'Recorded metadata/native bytes only; no visual/copy/authorship/print/maximum-size quality certification. One-second start precision allowance for mtime; not exhaustive tool history.','recorded_calls':len(records),'phase_cap':p['scope']['phase_native_call_cap'],'historical_closed_calls':95,'whole_recorded_history':None,'cross_phase_note':'This validator counts E only; D corrections and whole history are in combined ledger','recorded_peak_native_interval_overlap':peak,'logical_default_garden_makers':5,'errors':errors,'missing':missing,'records':records},ensure_ascii=False,indent=2))
raise SystemExit(1 if errors or (missing and not a.allow_incomplete) else 0)
