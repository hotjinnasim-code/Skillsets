#!/usr/bin/env python3
"""Combine complete first/final five-poster cases without averaging or best-subset choice."""
from pathlib import Path
import datetime,hashlib,json
r=Path(__file__).resolve().parent
read=lambda x:json.loads(Path(x).read_text());sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
plan=read(r/'planning/phase-plan.json');cases=read(r/'planning/cases.json')['cases'];closed=read(r/'planning/calls-closed.json')
assert closed['status']=='PASS' and closed['call_phase']=='CLOSED'
images={};sets={};refs={};first_records=[];final_records=[];errors=[]
for c in cases:
 cid=c['id'];closure=read(r/'planning'/f'{cid}-ordinary-closed.json')
 summaries={}
 for stage in ('first','final'):
  wave=closure['review_waves'][stage];path=r/'planning'/f'summary-{wave}.json';s=read(path)
  assert s['selected_image_count']==5 and s['image_critic_record_count']==15 and s['score_observation_count']==105
  summaries[stage]=s;refs[cid+'/'+stage]={'path':str(path),'sha256':sha(path),'wave':wave,'reuse_complete_initial_three':stage=='final' and not closure['physical_set_changed']}
  if s['recorded_evidence_integrity']!='PASS':errors.extend(s.get('integrity_errors',[]) or [cid+'/'+stage+' invalid procedure'])
 first_records.extend(summaries['first']['image_critic_records']);final_records.extend(summaries['final']['image_critic_records'])
 selected=read(closure['final_selection']['path'])['selected'];first=read(closure['first_selection']['path'])['selected']
 fs=summaries['final'];ins=summaries['first']
 for item in selected:
  role=item['role'];b=next(x for x in fs['image_bindings'] if x['role']==role);obs=[x for x in fs['image_critic_records'] if x['role']==role]
  ib=next(x for x in ins['image_bindings'] if x['role']==role);initialobs=[x for x in ins['image_critic_records'] if x['role']==role]
  related=[x for x in fs['located_gate_failures'] if x.get('image_id')==b['image_id'] or x.get('role')==role]
  irelated=[x for x in ins['located_gate_failures'] if x.get('image_id')==ib['image_id'] or x.get('role')==role]
  images[role]={'case_id':cid,'selected':item,'binding':b,'reviewers':obs,'initial_selection':next(x for x in first if x['role']==role),'initial_binding':ib,'initial_reviewers':initialobs,'initial_image_gate':'FAIL' if irelated else 'PASS','final_image_gate':'FAIL' if related else 'PASS','final_located_failures':related,'first_located_failures':irelated,'ordinary_selection':{'path':str(r/'production'/role/'selection.json'),'sha256':sha(r/'production'/role/'selection.json')}}
 sets[cid]={'name':c['name'],'roles':[x['id'] for x in c['slots']],'physical_set_changed':closure['physical_set_changed'],'initial_case_gate':ins['predeclared_core_diversity_gate'],'final_case_gate':fs['predeclared_core_diversity_gate'],'initial_reviewers':ins['all_set_records'],'final_reviewers':fs['all_set_records'],'initial_failures':ins['located_gate_failures'],'final_failures':fs['located_gate_failures'],'initial_disagreements':ins['disagreements'],'final_disagreements':fs['disagreements'],'final_all_scores_below4':fs['all_scores_below4']}
assert len(images)==20 and len(first_records)==len(final_records)==60
out={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':plan['source_commit'],'recorded_evidence_integrity':'FAIL' if errors else 'PASS','predeclared_core_diversity_gate':'PASS' if not errors and all(s['final_case_gate']=='PASS' for s in sets.values()) else ('NOT_ASSESSABLE' if errors else 'FAIL'),'scope':'20 additional selected images from four input contexts, all frozen currentG. Each complete five-poster set evaluated by three independent critics. First and changed final sets separately reviewed; unchanged whole sets reuse exact initial three with explicit SHA binding. All seven raw scores, low noncore scores and disagreements preserved. No averages or subset choice. Authorship, physical function, printing and universal future quality are not established.','images':images,'sets':sets,'summary_refs':refs,'firstpass_image_pass_count':sum(x['initial_image_gate']=='PASS' for x in images.values()),'final_image_pass_count':sum(x['final_image_gate']=='PASS' for x in images.values()),'firstpass_image_critic_records':60,'final_image_critic_records':60,'firstpass_score_observations':420,'final_score_observations':420,'integrity_errors':errors,'call_validation':{'path':str(r/'planning/calls-closed.json'),'sha256':sha(r/'planning/calls-closed.json')}}
with (r/'planning/final-evidence.json').open('x') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({k:out[k] for k in ('recorded_evidence_integrity','predeclared_core_diversity_gate','firstpass_image_pass_count','final_image_pass_count','firstpass_image_critic_records','final_image_critic_records')},ensure_ascii=False))
