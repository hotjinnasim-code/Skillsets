"""Freeze ONE matched five with new, actually reviewed own planning guides."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import shutil
import sys

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round22'
SNAP = ROUND / 'snapshots/candidate-z'
CASE_PATH = ROUND / 'planning/single-five-case.json'
PLAN_SOURCE = TASK / 'drafts/z-five-design/plan.json'

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}

def write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as handle:
        json.dump(value,handle,ensure_ascii=False,indent=2)
        handle.write('\n')

prepared = read(ROUND / 'planning/prepared-workspace.json')
for item in prepared['runtime'] + prepared['actor_helpers'] + [prepared['case'],prepared['previous_full_closure']]:
    assert pin(item['path']) == item
assert read(TASK / 'work/round21/planning/full-five-closure.json')['all_actors_closed']
plan = copy.deepcopy(read(PLAN_SOURCE))
case = read(CASE_PATH)['cases'][0]
for case_field in ['request','copy','conditions','assets','count','ratios','styles','roles']:
    assert plan[case_field] == case[case_field], case_field
assert len(plan['directions']) == 5
guide_map = read(ROUND / 'coordinator/guides/selected-guides.json')
assert set(guide_map) == {f'R22-C1-M{i}' for i in range(1,6)}
guide_sources = {}
for index,direction in enumerate(plan['directions'],1):
    role = f'R22-C1-M{index}'
    assert direction['role'] == role
    files = {key:Path(value) for key,value in guide_map[role].items()}
    assert set(files) == {'png','svg','spec','manifest'}
    assert all(path.is_file() for path in files.values())
    spec = read(files['spec'])
    assert len(spec['text_blocks']) == 12
    assert sorted(block['copy'] for block in spec['text_blocks']) == sorted(entry['text'] for entry in case['copy'])
    for block in spec['text_blocks']:
        assert ' '.join(block['lines']) == block['copy']
    guide_sources[role] = files
    direction['guide'] = {
        'png_path':str(ROUND / 'production' / role / 'guides/layout.png'),
        'role':'New coordinator-owned actual-copy/font and style-compatible image geometry planning diagram; not a client asset, final artwork, protected coordinates or native font-file-application proof',
    }
plan['status'] = 'all-five prospective own-guide plan, frozen before native generation'
plan['case_id'] = 'R22-C1'
plan['root_guide_note'] = 'All five newly authored actual-font/copy and content-geometry guides were viewed as a set at original detail before the first native call. Guide preparation and any prospective revisions remain retained.'
plan_path = ROUND / 'coordinator/R22-C1/plan.json'
write(plan_path,plan)
observation_path = ROUND / 'planning/root-whole-plan-observation.json'
observation = read(observation_path)
assert observation['native_calls'] == 0 and observation['not_poster_outputs']
assert {item['sha256'] for item in observation['actual_viewed_guides']} == {pin(files['png'])['sha256'] for files in guide_sources.values()}
write(ROUND / 'planning/ratio-policy-before-generation.json',{
    'declared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'policy':'nearest-integer-single-edge','max_deviation_px':0.5,
    'explicit_pixel_request_overrides':True,'source':'Unchanged R21 aspect-only policy; no changed quality threshold.',
})
sys.path.insert(0,str(ROUND))
import prepare_production as prep
result = prep.prepare(ROUND,CASE_PATH,['R22-C1'],SNAP)
for row in result['jobs']:
    job_path = Path(row['job']['path'])
    job = read(job_path)
    own = Path(job['output_dir'])
    directory = own / 'guides'
    directory.mkdir()
    for key,suffix in [('png','.png'),('svg','.svg'),('spec','.spec.json'),('manifest','.manifest.json')]:
        shutil.copy2(guide_sources[row['role']][key],directory / ('layout'+suffix))
    for relative in ['references/production-brief.md','references/design-grammar.md','references/layout-guide.md','references/layout-guide-contract.md']:
        job['inputs'].append(str(SNAP / relative))
    for name in ['layout.png','layout.spec.json','layout.manifest.json']:
        job['inputs'].append(str(directory / name))
    prompt_path = Path(job['prompt_file'])
    extra = f'''
CURRENT FIRST-GENERATION DESIGN INPUTS: read {SNAP/'references/production-brief.md'}, {SNAP/'references/design-grammar.md'}, {SNAP/'references/layout-guide.md'} and {SNAP/'references/layout-guide-contract.md'}. Use the accumulated design ideas; no mandatory original-artwork re-opening, fresh browsing or full catalog read.
OWN AUTHORED SUPPORTING GUIDE: actually view {directory/'layout.png'} at original detail, and read {directory/'layout.spec.json'} and {directory/'layout.manifest.json'}. It is a new actual-font/copy and content-geometry planning diagram, not a client image asset or fixed layout condition. The case assets remain empty. Own newly authored shapes and colours convey the chosen style-compatible image/copy relationship and readable role hierarchy. Create the assigned photographic/graphic/painted/drawn expression with its authored colour, typographic voice, material/finish and content relationship; these guide shapes are not final artwork. Do not turn the guide into a passive information panel. The actual-font anatomy is a reference; no final font-file application is asserted. STYLE PRIORITY: good layouts, Title/body role order and alignment may be shared across styles. Resolve your own style and reading flow autonomously; five unique layouts are not required. Preserve the immediately recognisable main Title, mature readable regular body and naturally grouped practical copy. Geometry, line counts and pixel sizes here are planning choices, not new client constraints.
BEFORE THE FIRST NATIVE CALL: own supporting PNG must actually be viewed. Because this job supplies this local planning image, include its absolute path in referenced_image_paths, omitting num_last_images_to_include. This is the supplied-reference branch of the earlier contract; the initial is not reference-free. Record the exact supporting guide pin and its layout/type role in pre-call.json. For repairs include the exact inspected previous own native target plus this same own guide and all required client assets if any (none here). No peer guide or poster inputs, no renderer/font edits, and no extra experiments. Execute only the pinned evidence helper. The native brief contains the exact printed copy once and a concrete current content/image/type design, not plan/spec JSON or evaluation instructions.
'''
    prompt_path.write_text(prompt_path.read_text()+extra,encoding='utf-8')
    job_path.write_text(json.dumps(job,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    row['job'] = pin(job_path)
    row['prompt'] = pin(prompt_path)
write(ROUND / 'planning/prepared-maker-jobs.json',result)
queue = [row['job']['path'] for row in result['jobs']]
write(ROUND / 'planning/maker-queue.json',queue)
write(ROUND / 'planning/candidate-z-pre-generation-freeze.json',{
    'candidate':'Z','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'runtime':prepared['runtime'],'actor_helpers':prepared['actor_helpers'],'case':pin(CASE_PATH),
    'style_first_plan':pin(PLAN_SOURCE),'plan':pin(plan_path),'root_actual_guide_views':pin(observation_path),
    'maker_jobs':[pin(path) for path in queue],
    'own_guide_inputs':[pin(ROUND/'production'/direction['role']/'guides'/name) for direction in plan['directions'] for name in ['layout.png','layout.svg','layout.spec.json','layout.manifest.json']],
    'ratio_policy':pin(ROUND/'planning/ratio-policy-before-generation.json'),
    'bounds':{'one_case':True,'logical_maker_roles':5,'worker_process_max':3,'initial_per_role':1,'repairs_per_role_max':2,'native_calls_max':15},
    'quality_method':'Same seven score categories, each >=4 per critic, all three diversity >=4 and mandatory conditions. Diversity scope prospectively follows the latest human style priority; shared good layouts are allowed. Historical scores and conditions are not changed. All low/NA retained.',
    'new_quality_gates':0,'native_calls_at_freeze':0,'r21_closure':prepared['previous_full_closure'],
    'limits':['ONE matched development five after R21 closure and explicit human style/copy-role steering, not unseen transfer.','Instructions, plan and supporting guides change together; no isolated causal claim.','Planning diagrams are not native requested posters or client-preserved coordinates.'],
})
print(json.dumps({'frozen':'R22','makers':len(queue),'native_calls':0,'guides':len(guide_sources)}))
