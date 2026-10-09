"""Adopt latest human style/copy-role scope after the previous ONE five fully closes."""
from pathlib import Path
import copy,datetime,hashlib,json,shutil
TASK=Path(__file__).resolve().parents[1]
OLD=TASK/'work/round21';ROUND=TASK/'work/round22'
DRAFT=TASK/'drafts/candidate-style-first';LIVE=TASK/'Skillsets/skills/ducttape-poster'
HISTORY=TASK/'history/style-first-adoption'
def read(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p).resolve(strict=True);assert p.is_file() and p.is_relative_to(TASK)
 data=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
assert Path.cwd().resolve().is_relative_to(TASK) and not ROUND.exists() and not HISTORY.exists()
closed_path=OLD/'planning/full-five-closure.json';closed=read(closed_path)
assert closed['all_actors_closed'] and closed['requested_images']==5 and closed['no_post_critic_repair_or_reselection']
archive=TASK/'Skillsets/evals/ducttape-poster/round21'
archive_index_path=archive/'archive-index.json';archive_verification_path=archive/'byte-verification.json'
archive_index_pin=pin(archive_index_path);archive_verification_pin=pin(archive_verification_path)
archive_index=read(archive_index_path);archive_verification=read(archive_verification_path)
assert archive_verification['all_copy_hashes_match'] and archive_index['source_root']==str(OLD)
closure_pin=pin(closed_path)
archived_closure_rows=[r for r in archive_index['files'] if r['source_absolute']==str(closed_path.resolve())]
assert len(archived_closure_rows)==1
archived_closure=archived_closure_rows[0];archived_closure_pin=pin(archive/archived_closure['archive_relative'])
assert archived_closure['sha256']==closure_pin['sha256']==archived_closure_pin['sha256']
assert archived_closure['bytes']==closure_pin['bytes']==archived_closure_pin['bytes']
human_steering_pin=pin(TASK/'history/style-first-steering/steering.json')
old_case_pin=pin(OLD/'planning/single-five-case-hierarchy.json')
freeze_path=OLD/'planning/candidate-y-pre-generation-freeze.json';frozen=read(freeze_path)
for row in frozen['runtime']+frozen['actor_helpers']:assert pin(row['path'])==row
for row in frozen['runtime']:
 relative=Path(row['path']).relative_to(OLD/'snapshots/candidate-y')
 assert pin(LIVE/relative)['sha256']==row['sha256']
audit_path=TASK/'history/style-first-scope-audit/status.json';audit=read(audit_path)
assert audit['unresolved_issues']==[]
for row in audit['current_file_pins']:assert pin(row['path'])=={k:row[k] for k in ['path','sha256','bytes']}
files=sorted(p for p in DRAFT.rglob('*') if p.is_file());assert len(files)==12
assert all(not p.is_symlink() for p in files)
changed=[p.relative_to(DRAFT).as_posix() for p in files if p.read_bytes()!=(LIVE/p.relative_to(DRAFT)).read_bytes()]
allowed={'SKILL.md','agents/openai.yaml','references/art-direction.md','references/design-grammar.md','references/evaluation-loop.md','references/layout-guide.md','references/parallel-production.md','references/production-brief.md','references/visual-research.md'}
assert set(changed).issubset(allowed) and changed
for relative in ['scripts/make_layout_guide.py','references/reference-catalog.json','references/layout-guide-contract.md']:
 assert (DRAFT/relative).read_bytes()==(LIVE/relative).read_bytes()
corpus=copy.deepcopy(read(OLD/'planning/single-five-case-hierarchy.json'));assert len(corpus['cases'])==1
case=corpus['cases'][0];original=copy.deepcopy(case)
old_sentence='각각 전체 스타일과 레이아웃이 달랐으면 좋겠어.'
new_sentence='스타일이 확연히 다르게 느껴지면 좋겠어. 레이아웃은 각 스타일과 읽기 흐름에 맞게 선택하고, 잘 작동하는 구도는 여러 시안에서 공유해도 돼.'
assert case['request'].count(old_sentence)==1
case['request']=case['request'].replace(old_sentence,new_sentence)
old_condition='Five genuinely distinct whole visual systems in spatial organization, image editing, type roles and reading routes, not different media over a common scaffold.'
new_condition='Five clearly distinct achieved styles: imagery and graphic language, color relationships, typography, material and emotion work as an intentional style identity. A good layout, text-role order or alignment may be shared. Five unique layouts or reading routes are not required. Mere filter, palette or font substitutions do not by themselves establish a new style.'
assert case['conditions'].count(old_condition)==1
case['conditions']=[new_condition if x==old_condition else x for x in case['conditions']]
case.update(case_id='R22-C1',candidate='Z',phase='matched-development-human-style-priority-and-actual-copy-roles',source='Same plant-market content after fully closed R21. The human explicitly prioritised different styles and allowed shared good layouts, and clarified Title-only/Title+body scope for the general skill. Only the literal style/layout sentence and corresponding condition are prospectively amended; old R21 conditions/scores are retained. This is matched development, not held-out or an isolated instruction effect.')
for i,role in enumerate(case['roles'],1):role['role_id']=f'R22-C1-M{i}'
assert all(case[k]==original[k] for k in ['copy','count','ratios','styles','assets'])
# Source dependencies and scope are checked before any live runtime mutation.
shutil.copytree(LIVE,HISTORY/'before-y');shutil.copytree(DRAFT,HISTORY/'adopted-z');shutil.copytree(DRAFT,ROUND/'snapshots/candidate-z')
helpers=[]
for row in frozen['actor_helpers']:
 source=Path(row['path']);target=ROUND/source.relative_to(OLD);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target);helpers.append(pin(target))
case_path=ROUND/'planning/single-five-case.json';write(case_path,corpus)
for p in files:shutil.copy2(p,LIVE/p.relative_to(DRAFT))
runtime=[pin(p) for p in sorted((ROUND/'snapshots/candidate-z').rglob('*')) if p.is_file()]
write(ROUND/'planning/prepared-workspace.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':'Z','case':pin(case_path),'runtime':runtime,'actor_helpers':helpers,'previous_full_closure':closure_pin,'previous_archive_index':archive_index_pin,'previous_archive_verification':archive_verification_pin,'jobs_prepared':0,'native_calls':0,'limits':['Prospective ONE five only. Plan and any own guides are not yet frozen.','Human style scope changes before generation; old scores are not relabelled.','All twenty actor helpers, seven score categories and numerical thresholds remain unchanged.']})
write(HISTORY/'adoption.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':'Z','previous':'Y','changed_files':changed,'runtime':[pin(p) for p in sorted((HISTORY/'adopted-z').rglob('*')) if p.is_file()],'scope_review':pin(audit_path),'human_steering':human_steering_pin,'previous_full_closure':closure_pin,'old_client_case':old_case_pin,'new_client_case':pin(case_path),'numerical_quality_thresholds_changed':False,'helper_bytes_changed':False,'native_calls_at_adoption':0,'new_quality_result':None,'limits':['Style identity is the priority; a shared good layout does not disqualify a style. Cosmetic substitutions alone do not prove diversity.','Only supplied roles/copy are designed. Title-only and Title+body do not require invented eyebrow/subtitle/footer.','Adoption/static validation alone is not proof of actual native quality or general transfer.']})
print(json.dumps({'candidate':'Z','round':22,'cases':1,'requested_images':5,'jobs':0,'native_calls':0,'helpers':len(helpers),'changed_files':changed}))
