#!/usr/bin/env python3
"""Assemble exact current-nine evidence plus five unchanged closed selections.
Raw scores and disagreements remain unaveraged. No images generated or edited.
"""
import argparse,copy,datetime,hashlib,json,struct
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--summary',type=Path,required=True);ap.add_argument('--selection',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();r=Path(__file__).resolve().parent
oldnative=Path('/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round4');oldarchive=Path('/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round4')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_text());errors=[];failures=[];other=[];selected={};sets={}
require=lambda ok,msg: errors.append(msg) if not ok else None
s=read(a.summary);choice_list=read(a.selection)['selected'];choices={x['role']:x for x in choice_list};old=read(oldnative/'planning/final-delivery-evidence.json');bundle_path=r/'planning/retained-five-bindings.json';bundle=read(bundle_path)
require(len(choice_list)==len(choices)==9,'Current selection has duplicate/missing roles')
require(bundle['status']=='PASS' and not bundle['errors'],'Retained binding bundle did not pass')
for source in bundle['files']:
 require(sha(source['path'])==source['sha256'],'Retained context/source changed: '+source['path'])
require(s['recorded_evidence_integrity']=='PASS','Current summary integrity is not PASS')
require(set(choices)=={'G01','G02','G03','G04','G05','H01','H02','P01','P02'},'Current9roles differ')
for role,x in choices.items():
 bindings=[v for v in s['image_bindings'] if v['role']==role];require(len(bindings)==1,role+' current summary binding count mismatch');b=bindings[0];fp=Path(x['final_native']);require(sha(fp)==x['sha256']==b['native_sha256'],role+' currentnative mismatch');require(str(fp)==b['selected_native'],role+' sourcepath mismatch');m=read(x['manifest']);require(sha(x['manifest'])==x['manifest_sha256'],role+' selected manifest changed');require(m['role']==role and m['stage']==x['stage']==b['stage'],role+' selected role/stage mismatch');require(m['final']['sha256']==x['sha256'] and m['final']['path']==str(fp),role+' selected final mismatch');require([m['width'],m['height']]==[x['width'],x['height']],role+' manifest/selection dimensions differ')
 require(list(struct.unpack('>II',fp.read_bytes()[16:24]))==[x['width'],x['height']],role+' actual native dimensions differ')
 for view,record in b['views'].items():
  require(sha(record['path'])==record['sha256'],role+' current view changed: '+view)
  require(list(struct.unpack('>II',Path(record['path']).read_bytes()[16:24]))==record['dimensions'],role+' view dimensions differ: '+view)
 critics={}
 for rec in s['image_critic_records']:
  if rec['role']!=role:continue
  require(sha(rec['raw_path'])==rec['raw_sha256'],role+' currentraw changed');obs=read(rec['raw_path'])['images'][b['image_id']]
  for field in ['mandatory','scores','evidence']:
   require(obs[field]==rec[field],role+' current raw/summary differs: '+field)
  require(obs.get('residuals',[])==rec.get('residuals',[]),role+' current raw residuals differ');critics[rec['profile']]={'reviewer_identity':rec['profile'],'raw_report_absolute':rec['raw_path'],'raw_report_sha256':rec['raw_sha256'],'mandatory':rec['mandatory'],'scores':rec['scores'],'evidence':rec['evidence'],'residuals':rec.get('residuals',[])}
 require(set(critics)==set(b.get('critic_profiles',s['critics'])),role+' missing currentcritic')
 selected[role]={**x,'final_native_absolute':str(fp),'anonymous_id':b['image_id'],'review_wave':b.get('review_wave',s['wave']),'source_binding_pass':True,'views':b['views'],'reviewers':critics}
for role in ['C01','C02','N01','N02','H03']:
 x=copy.deepcopy(old['selected_images'][role]);fp=oldnative/x['final_native'];require(sha(fp)==x['sha256'],role+' unchangednative mismatch');require(x['source_binding_pass'] is True,role+' oldbinding not established');x['final_native_absolute']=str(fp);critics={}
 for profile,crit in x['reviewers'].items():
  rawpath=oldarchive/crit['raw_report'];raw=read(rawpath);obs=raw['images'][x['anonymous_id']];require(obs['scores']==crit['scores'] and obs['mandatory']==crit['mandatory'],role+' closedraw score/mandatory mismatch');require(obs['evidence']==crit['evidence'],role+' closedraw evidence mismatch');critics[profile]={**crit,'raw_report_absolute':str(rawpath),'raw_report_sha256':sha(rawpath)}
 bound=bundle['selected_images'][role];require(bound['sha256']==x['sha256'] and bound['anonymous_id']==x['anonymous_id'],role+' retained bundle selection differs');x['views']=copy.deepcopy(bound['views']);x['retained_review_binding']=copy.deepcopy(bound)
 for view,record in x['views'].items():require(sha(record['path'])==record['sha256'],role+' retained view changed: '+view)
 x['reviewers']=critics;selected[role]=x
for cid in ['title-only','product','invitation']:
 rows=[x for x in s['all_set_records'] if x['case_id']==cid];roles=sorted(x['role'] for x in s['image_bindings'] if x['case_id']==cid);members={selected[role]['anonymous_id']:selected[role]['sha256'] for role in roles};waves={selected[role]['review_wave'] for role in roles};require(len(waves)==1,cid+' selected case spans review waves')
 for record in rows:
  require(sha(record['raw_path'])==record['raw_sha256'],cid+' current raw set changed');obs=read(record['raw_path'])['sets'][cid]
  for field,value in obs.items():require(record.get(field)==value,cid+' current raw set observation differs: '+field)
  require(set(obs['members'])==set(members),cid+' current raw set membership differs')
 sets[cid]={'selected_roles':roles,'member_sha256':members,'review_wave':next(iter(waves)),'reviewers':{x['profile']:x for x in rows}}
for cid,x0 in bundle['sets'].items():
 require(set(x0['selected_roles']) in [set(['C01','C02']),set(['N01','N02']),set(['H03'])],'Unknown retained set membership');x=copy.deepcopy(x0);members={selected[role]['anonymous_id']:selected[role]['sha256'] for role in x['selected_roles']};require(members==x['member_sha256'],cid+' retained set SHA members differ')
 for profile,critic in x['reviewers'].items():
  rawpath=critic['raw_report_absolute'];require(sha(rawpath)==critic['raw_report_sha256'],cid+' retained set raw changed');obs=read(rawpath)['sets'][cid];require(obs==critic['raw_set_observation'],cid+' retained set observation differs');critic.update(copy.deepcopy(obs))
 sets[cid]=x
core={'content_form','typography','image_material','ai_slop'}
for role,x in selected.items():
 for profile,crit in x['reviewers'].items():
  if crit['mandatory']['pass'] is not True:failures.append({'role':role,'profile':profile,'kind':'mandatory','record':crit['mandatory']})
  for dim,score in crit['scores'].items():
   if score<4:(failures if dim in core else other).append({'role':role,'profile':profile,'dimension':dim,'score':score,'evidence':crit['evidence'][dim]})
for cid,x in sets.items():
 if len(x['selected_roles'])<2:continue
 for profile,crit in x['reviewers'].items():
  if crit['diversity']<4:failures.append({'case':cid,'profile':profile,'kind':'diversity','score':crit['diversity'],'evidence':crit['evidence']})
require(len(selected)==14 and len(sets)==6,'Expected14images/6cases notassembled')
transfer=copy.deepcopy(s.get('required_transfer_evidence'));transfer_failures=[]
transfer_required=any(Path(x['manifest']).resolve().is_relative_to(r/'continuation-g') for x in choices.values())
require(not transfer_required or transfer is not None,'Predeclared G control evidence omitted')
if transfer is not None:
 require(transfer['recorded_evidence_integrity']=='PASS','Required transfer source integrity is not PASS')
 for key in ['source_summary_ref','source_plan','source_cases']:
  pin=transfer[key];require(sha(pin['path'])==pin['sha256'],'Required transfer source pin changed: '+key)
 require(Path(transfer['source_plan']['path']).resolve()==r/'continuation-g/planning/phase-plan.json','Required transfer plan not canonical G')
 plan=read(transfer['source_plan']['path']);require(plan['scope']['additional_control_role']=='T01','Control not predeclared')
 require(len(transfer['image_bindings'])==1 and len(transfer['image_critic_records'])==3,'Required transfer coverage differs')
 b=transfer['image_bindings'][0];require(b['role']=='T01' and b['phase']=='G','Required transfer role/phase differs')
 require(sha(b['selected_native'])==b['native_sha256'],'Required transfer native changed')
 require(sha(b['manifest'])==b['manifest_sha256'],'Required transfer manifest changed')
 m=read(b['manifest']);require(m['role']=='T01' and m['stage']==b['stage'] and m['final']['sha256']==b['native_sha256'],'Required transfer manifest binding differs')
 require(set(b['views'])=={'native','usage720','thumbnail320'},'Required transfer three views missing')
 for view,record in b['views'].items():
  require(sha(record['path'])==record['sha256'],'Required transfer view changed: '+view)
  require(list(struct.unpack('>II',Path(record['path']).read_bytes()[16:24]))==record['dimensions'],'Required transfer view dimensions differ: '+view)
 require(set(x['profile'] for x in transfer['image_critic_records'])==set(b['critic_profiles']),'Required transfer critic coverage differs')
 for rec in transfer['image_critic_records']:
  require(sha(rec['raw_path'])==rec['raw_sha256'],'Required transfer raw changed');obs=read(rec['raw_path'])['images'][b['image_id']]
  for field in ['mandatory','scores','evidence']:
   require(obs[field]==rec[field],'Required transfer raw/summary differs: '+field)
  require(obs.get('residuals',[])==rec.get('residuals',[]),'Required transfer residuals differ')
  if obs['mandatory']['pass'] is not True:transfer_failures.append({'role':'T01','profile':rec['profile'],'kind':'mandatory','record':obs['mandatory']})
  for dim,score in obs['scores'].items():
   if dim in core and score<4:transfer_failures.append({'role':'T01','profile':rec['profile'],'dimension':dim,'score':score,'evidence':obs['evidence'][dim]})
 for rec in transfer['all_set_records']:
  require(sha(rec['raw_path'])==rec['raw_sha256'],'Required transfer singleton raw changed');obs=read(rec['raw_path'])['sets'][rec['case_id']]
  require(obs['members']==[b['image_id']] and obs.get('diversity') is None and obs.get('closest_pair')==[] and obs.get('closest_pair_score') is None,'Required transfer invented singleton diversity/pair')
 require(transfer['predeclared_transfer_gate']==('FAIL' if transfer_failures else 'PASS'),'Required transfer declared gate differs')
 failures.extend(transfer_failures)
result={'assembled_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Current9 complete case-bound closed raw review sources + exact5 unchanged prior selections. Mixed versions, not full fresh latest-version performance, universal future/authorship/print/physical certification. Prior lower reviews remain archived; no whole historicalFAIL result copied as selectedPASS.','current_summary':{'path':str(a.summary.resolve()),'sha256':sha(a.summary)},'prior_selection_evidence':{'path':str(oldnative/'planning/final-delivery-evidence.json'),'sha256':sha(oldnative/'planning/final-delivery-evidence.json')},'selected_images':selected,'sets':sets,'review_procedure_current':s['review_procedure'],'review_procedure_retained':bundle['review_procedure'],'retained_binding_bundle':{'path':str(bundle_path),'sha256':sha(bundle_path)},'selected_image_count':len(selected),'image_critic_records':sum(len(x['reviewers']) for x in selected.values()),'located_gate_failures':failures,'other_sub4_scores':other,'binding_errors':errors,'predeclared_gate_pass':not errors and not failures,'note':'Every selected source keeps all raw7 scores, located evidence/mandatory/copy/residuals and setmembership. SingletonH03 has no inventedpair requirement; its raw set record remains. PASS concerns predeclaredcore/diversityonly; noncore residuals remain.'}
if transfer is not None:
 result['required_transfer_evidence']=transfer;result['predeclared_transfer_gate']=transfer['predeclared_transfer_gate'];result['note']+=' Required G T01 is separate from selected14; all three mandatory/core observations also gate completion, with no singleton pair score.'
a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'quality_gate':result['predeclared_gate_pass'],'binding_errors':errors,'located_gate_failures':len(failures),'noncore_sub4':len(other),'images':len(selected),'critic_records':result['image_critic_records']}));raise SystemExit(0 if result['predeclared_gate_pass'] else 1)
