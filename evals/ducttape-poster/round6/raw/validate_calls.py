#!/usr/bin/env python3
"""Verify recorded R6 lineage, finite attempts and exact bytes, not visual quality."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, re, struct

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--allow-incomplete',action='store_true')
a=p.parse_args(); r=Path(__file__).resolve().parent
read=lambda x:json.loads(Path(x).read_text())
sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
errors,records,pending,events,quality=[],[],[],[],[]
def need(ok,msg):
    if not ok: errors.append(msg)
def time(s):
    x=dt.datetime.fromisoformat(s.replace(' UTC','+00:00').replace('Z','+00:00'))
    if x.tzinfo is None: raise ValueError('UTC offset absent')
    return x.timestamp()
def png(path):
    b=Path(path).read_bytes()
    need(b[:8]==b'\x89PNG\r\n\x1a\n','Not a PNG: '+str(path))
    return list(struct.unpack('>II',b[16:24]))
def canonical(value,path,label):
    need(Path(value).resolve()==path.resolve(),label+' canonical path differs')
def normalized_pins(pins):
    return sorted((str((Path(x['path']) if Path(x['path']).is_absolute() else r/x['path']).resolve()),x['sha256']) for x in pins)
planpath=r/'planning/phase-plan.json'; plan=read(planpath)
freeze=read(r/'planning/skill-freeze.json')
casespath=Path(plan['cases']['path']); dirpath=Path(plan['directions']['path'])
cases=read(casespath)['cases']; directions=read(dirpath)['directions']
need(sha(casespath)==plan['cases']['sha256'],'Frozen cases changed')
need(sha(dirpath)==plan['directions']['sha256'],'Frozen directions changed')
need(plan['frozen_skill_files']==freeze['frozen_skill_files'],'Six freeze pins differ')
need(len(plan['frozen_skill_files'])==6,'Expected six frozen files')
for pin in plan['frozen_skill_files']:
    need(sha(r/pin['path'])==pin['sha256'],'Frozen skill changed: '+pin['path'])
for pin in plan['prior_closed_records']:
    need(sha(pin['path'])==pin['sha256'],'Prior closed history changed')
closed=read(plan['prior_closed_records'][0]['path'])
need(closed['whole_recorded']==128 and closed['call_phases']=='ALL_CLOSED','Prior128 not closed')
roles={s['id']:(c,s['ratio']) for c in cases for s in c['slots']}
need(len(cases)==4 and len(roles)==20 and all(len(c['slots'])==5 and c['expected_final_count']==5 for c in cases),'Four five-role cases required')
need(len(directions)==20 and {d['role'] for d in directions}==set(roles),'Direction coverage differs')
stagekeys={'initial':0,'repair-1':1,'repair-2':2}
stages=sorted({x.parent for name in ('call-input.json','manifest.json','failure.json') for x in (r/'production').glob('*/*/'+name)})
need(len(stages)<=60,'R6 attempt ceiling60 exceeded')
counts={}; byrole={}; completed_selections=[]
for folder in stages:
    role,stage=folder.parent.name,folder.name
    if role not in roles or stage not in stagekeys:
        errors.append('Unscheduled role/stage: '+str(folder)); continue
    c,ratio=roles[role]; k=stagekeys[stage]
    counts[role]=counts.get(role,0)+1
    need(counts[role]<=3,role+' own cap exceeded')
    ip,prepath=folder/'call-input.json',folder/'pre-call.json'
    mp,fp=folder/'manifest.json',folder/'failure.json'
    need(not(mp.exists() and fp.exists()),role+'/'+stage+' success and failure both present')
    if not ip.exists() or not prepath.exists():
        errors.append(role+'/'+stage+' missing pre-call/input'); continue
    try:
        args,pre=read(ip),read(prepath)
        need(pre['role']==role and pre['case_id']==c['id'] and pre['stage']==stage and pre['own_correction_number']==k,role+' pre-call identity differs')
        need(pre['phase_plan']=={'path':str(planpath),'sha256':sha(planpath)},role+' pre-call plan pin differs')
        need(pre['cases']==plan['cases'] and pre['directions']==plan['directions'] and normalized_pins(pre['frozen_skill_files'])==normalized_pins(plan['frozen_skill_files']),role+' pre-call source pins differ')
        prompt=args['prompt']
        request_blocks=[b for b in c['request'].split('\n\n') if b.splitlines()!=c['copy']]
        need(all(b in prompt for b in request_blocks) and all(x in prompt for x in c['copy']),role+' full request instructions/copy missing')
        need(bool(re.search(r'maximum.{0,60}resolution|최대.{0,40}해상도',prompt,re.I|re.S)),role+' max resolution request absent')
        need(args.get('transparent_background') is False and 'num_last_images_to_include' not in args,role+' opacity/conversation references differ')
        parent=None if k==0 else r/'production'/role/('initial' if k==1 else 'repair-1')/'final.png'
        if parent is not None and parent.exists():
            need(pre['parent_native']==str(parent) and pre['parent_sha256']==sha(parent),role+' parent pin differs')
            if 'referenced_image_paths' in args: need(args['referenced_image_paths']==[str(parent)],role+' own edit reference differs')
        else:
            need(pre['parent_native'] is None and pre['parent_sha256'] is None,role+' absent parent pin differs')
            need('referenced_image_paths' not in args,role+' new or failed-parent generation borrowed image')
        if not mp.exists() and not fp.exists():
            pending.append({'role':role,'stage':stage,'path':str(ip)}); continue
        m=read(mp if mp.exists() else fp)
        need(m['role']==role and m['case_id']==c['id'] and m['stage']==stage and m['own_correction_number']==k and m['native_call_number_for_role']==k+1,role+' outcome identity/number differs')
        need(m['call_input']==args,role+' saved actual input differs')
        canonical(m['call_input_path'],ip,role+' input'); canonical(m['precall_plan_path'],prepath,role+' pre-call')
        start,end=time(m['started_at_utc']),time(m['completed_at_utc'])
        need(start<=end,role+' interval reversed')
        need(ip.stat().st_mtime<=start+3 and prepath.stat().st_mtime<=start+3,role+' pre-call saved after start')
        for path in (planpath,casespath,dirpath,r/'planning/skill-freeze.json'):
            need(path.stat().st_mtime<=start+3,role+' freeze saved after call start')
        need(time(plan['created_utc'])<=start,role+' plan created after call start')
        events.extend([(start,1),(end,-1)])
        record={'role':role,'case_id':c['id'],'stage':stage,'outcome_path':str(mp if mp.exists() else fp),'outcome_sha256':sha(mp if mp.exists() else fp),'start':start,'end':end,'kind':'returned native' if mp.exists() else 'failed native attempt'}
        if fp.exists():
            need(m['tool_attempted'] is True and isinstance(m['error'],str) and bool(m['error']),role+' failed call evidence absent')
        else:
            need(m['target_ratio']==ratio,role+' declared ratio differs')
            for field in ('tool_source','original','final'):
                v=m[field]; need(sha(v['path'])==v['sha256']==m['final']['sha256'],role+' native bytes differ: '+field)
                if field!='tool_source': canonical(v['path'],folder/(field+'.png'),role+' '+field)
            dims=png(m['final']['path']); need(dims==[m['width'],m['height']],role+' dimensions differ')
            w,h=dims; rw,rh=map(int,ratio.split(':'))
            if abs((w/h)/(rw/rh)-1)>.01: quality.append({'role':role,'stage':stage,'condition':'ratio outside1%','actual':dims,'required':ratio})
            for key,expected in [('usage720',[720,round(h*720/w)]),('thumbnail320',[round(w*320/max(w,h)),round(h*320/max(w,h))])]:
                q=m['qa_views'][key]; canonical(q['path'],folder/(key+'.png'),role+' '+key)
                need(sha(q['path'])==q['sha256'] and png(q['path'])==expected==[q['width'],q['height']],role+' QA dimensions/bytes differ: '+key)
            for name in ['inspection.json']+(['parent-comparison.json'] if k else []): need((folder/name).is_file(),role+' inspection absent: '+name)
            record.update(native_sha256=m['final']['sha256'],dimensions=dims,manifest=str(mp),manifest_sha256=sha(mp))
        records.append(record); byrole.setdefault(role,{})[k]=record
    except (KeyError,TypeError,ValueError,OSError,struct.error) as e:
        errors.append(role+'/'+stage+': '+str(e))
missing=[]
for role,(c,ratio) in roles.items():
    rr=byrole.get(role,{})
    if 0 not in rr: missing.append(role+' preserved initial outcome')
    for k,rec in rr.items():
        if k:
            need(k-1 in rr,role+' skipped own stage')
            if k-1 in rr: need(rr[k-1]['end']<=rec['start'],role+' own lineage overlaps')
    sp=r/'production'/role/'selection.json'
    if not sp.exists(): missing.append(role+' closed selection'); continue
    try:
        s=read(sp); k=stagekeys[s['selected_stage']]
        need(s['role']==role and s['case_id']==c['id'] and k in rr and rr.get(k,{}).get('kind')=='returned native',role+' selection has no returned stage')
        need(s['call_count']==counts.get(role,0) and s['own_corrections']==counts.get(role,0)-1,role+' selected call count differs')
        listed_stages=[]
        for entry in s['all_stage_paths']:
            value=entry['path'] if isinstance(entry,dict) else entry
            path=Path(value).resolve(); listed_stages.append(str(path))
            if isinstance(entry,dict):
                need(entry.get('stage')==path.name and path.parent==(r/'production'/role).resolve(),role+' structured stage identity differs')
                if 'manifest_path' in entry: canonical(entry['manifest_path'],path/'manifest.json',role+' structured stage manifest')
                if 'inspection_path' in entry: canonical(entry['inspection_path'],path/'inspection.json',role+' structured stage inspection')
        need(set(listed_stages)=={str(x.resolve()) for x in stages if x.parent.name==role},role+' stage coverage differs')
        mp=r/'production'/role/s['selected_stage']/'manifest.json'; m=read(mp)
        for key in ('manifest','manifest_path'):
            if key in s: canonical(s[key],mp,role+' selected '+key)
        need('manifest' in s or 'manifest_path' in s,role+' selected manifest field absent')
        canonical(s['selected_native'],mp.parent/'final.png',role+' selected native')
        need(s['sha256']==m['final']['sha256'] and [s['width'],s['height']]==[m['width'],m['height']],role+' selection bytes/dimensions differ')
        need(bool(s['chosen_reason']) and isinstance(s['residuals'],list) and len(s['actual_view_paths'])>=3,role+' final inspection attestation absent')
        completed_selections.append(role)
    except (KeyError,TypeError,ValueError,OSError) as e: errors.append(role+' selection: '+str(e))
active=peak=0
for _,delta in sorted(events): active+=delta; peak=max(peak,active)
need(peak<=3,'Recorded call interval peak exceeds three worker slots')
hashroles={}
for rec in records:
    if 'native_sha256' in rec: hashroles.setdefault(rec['native_sha256'],set()).add(rec['role'])
duplicates={h:sorted(rs) for h,rs in hashroles.items() if len(rs)>1}
status='FAIL' if errors else ('INCOMPLETE' if pending or missing else 'PASS')
print(json.dumps({'recorded_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':status,'scope':'Recorded lineage, cap and exact bytes only. Actual viewing, native tool invocation and order remain attestations. Quality, authorship, physical function, print and supported maximum resolution are not certified. Failed attempts count. Ratio or duplicate-byte findings are retained separately as quality conditions, not erased.','scheduled_originals':20,'new_R6_attempt_ceiling':60,'recorded_attempts':len(stages),'prior_R5_closed_recorded':128,'prior_R5_retirement_unchanged':True,'actual_recorded_interval_peak':peak,'role_counts':counts,'completed_selection_roles':completed_selections,'missing':missing,'pending':pending,'records':records,'quality_conditions':quality,'duplicate_bytes_across_roles':duplicates,'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(1 if errors or (status=='INCOMPLETE' and not a.allow_incomplete) else 0)
