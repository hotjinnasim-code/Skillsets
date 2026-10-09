"""Adopt the user's role-hierarchy steering before ONE R21 five starts."""
from pathlib import Path
import copy, datetime, hashlib, json, shutil
TASK=Path(__file__).resolve().parents[1]
ROUND=TASK/'work/round21'
DRAFT=TASK/'drafts/candidate-hierarchy'
LIVE=TASK/'Skillsets/skills/ducttape-poster'
HISTORY=TASK/'history/hierarchy-adoption'
def read(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p).resolve(strict=True)
 return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
prior_path=ROUND/'planning/prepared-workspace.json'
prior=read(prior_path)
assert not (ROUND/'production').exists() and not (ROUND/'reviews').exists()
assert not HISTORY.exists()
for item in prior['runtime']+prior['actor_helpers']+[prior['case'],prior['previous_full_closure']]:assert pin(item['path'])==item
for item in prior['runtime']:
 rel=Path(item['path']).relative_to(ROUND/'snapshots/candidate-x')
 assert pin(LIVE/rel)['sha256']==item['sha256']
audit_path=TASK/'history/hierarchy-scope-audit/status.json'
audit=read(audit_path)
assert audit['unresolved_issues']==[]
for item in audit['current_file_pins']:assert pin(item['path'])=={k:item[k] for k in ('path','sha256','bytes')}
files=sorted(p for p in DRAFT.rglob('*') if p.is_file())
assert len(files)==12
changed=[p.relative_to(DRAFT).as_posix() for p in files if p.read_bytes()!=(LIVE/p.relative_to(DRAFT)).read_bytes()]
assert changed==['SKILL.md','references/parallel-production.md','references/production-brief.md']
shutil.copytree(LIVE,HISTORY/'before-x')
shutil.copytree(DRAFT,HISTORY/'adopted-y')
shutil.copytree(DRAFT,ROUND/'snapshots/candidate-y')
for p in files:shutil.copy2(p,LIVE/p.relative_to(DRAFT))
corpus=copy.deepcopy(read(prior['case']['path']))
case=corpus['cases'][0]; original=read(prior['case']['path'])['cases'][0]
case['candidate']='Y'
case['phase']='matched-development-explicit-text-role-hierarchy-and-font-harmony-before-first-generation'
case['source']='Same R20 request/copy/conditions/ratios/assets after complete R20 closure. X workspace was prepared with zero jobs/calls, then the human requested clear eyebrow/Title/Subtitle/body/footer hierarchy and harmonious fonts. Y adopts that general steering before the ONE R21 five; X original preparation and ungenerated plan remain preserved. Not held-out or isolated causal proof.'
assert all(case[k]==original[k] for k in ('request','copy','conditions','styles','count','ratios','assets','roles'))
case_path=ROUND/'planning/single-five-case-hierarchy.json';write(case_path,corpus)
runtime=[pin(p) for p in sorted((ROUND/'snapshots/candidate-y').rglob('*')) if p.is_file()]
write(ROUND/'planning/prepared-workspace-y.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':'Y','case':pin(case_path),'runtime':runtime,'actor_helpers':prior['actor_helpers'],'previous_full_closure':prior['previous_full_closure'],'prior_preparation':pin(prior_path),'native_calls':0,'jobs_prepared':0,'limits':['Prospective preparation only; all-five revised plan and guides are still unfrozen.','Original X preparation had zero jobs/calls; this is one R21 five, not a second batch.','No native quality result exists at adoption.']})
write(HISTORY/'adoption.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':'Y','previous':'X','changed_files':changed,'runtime':[pin(p) for p in sorted((HISTORY/'adopted-y').rglob('*')) if p.is_file()],'draft':pin(TASK/'history/hierarchy-draft/changed-files.json'),'scope_review':pin(audit_path),'prior_preparation':pin(prior_path),'previous_full_closure':prior['previous_full_closure'],'native_calls_at_adoption':0,'new_quality_gates':0,'quality_thresholds_changed':False,'basis':'Latest human steering: distinguish eyebrow, Title, Subtitle, body copy and footer; make the Title recognizable and fonts harmonious.','limits':['Existing copy only; absent roles do not require invented labels/copy.','No fixed font/layout/pixel scale; explicit user roles and text-free/title-only cases remain authoritative.','All five whole compositions remain distinct; typography variation does not substitute for whole design diversity.','Planning font files do not certify native final font-file application.','X preparation and ungenerated original plan are retained without retrospective quality claims.']})
print(json.dumps({'candidate':'Y','round':21,'cases':1,'makers':5,'jobs':0,'native_calls':0,'helpers':len(prior['actor_helpers'])}))
