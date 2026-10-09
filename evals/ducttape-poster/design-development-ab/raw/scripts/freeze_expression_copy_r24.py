"""Prepare and freeze ONE known Title+body AB five; launch no actors.

Root executes this only after the two optional coordinator guides are ready.
The pinned actor preparer is wrapped in memory before its exclusive first writes.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import sys

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round24'
SNAP = ROUND / 'snapshots/candidate-ab'
LIVE = TASK / 'Skillsets/skills/ducttape-poster'
CASE_PATH = ROUND / 'planning/single-five-case.json'
PLAN_SOURCE = TASK / 'drafts/ab-five-design/plan.json'
GUIDE_MAP_PATH = ROUND / 'coordinator/guides/selected-guides.json'
CASE_ID = 'R24-C1'
CASE_FIELDS = ('request', 'copy', 'conditions', 'assets', 'count', 'ratios', 'styles', 'roles')
RATIOS = ['16:9', '16:9', '2:3', '2:3', '2:3']
GUIDE_ROLES = [f'{CASE_ID}-M1', f'{CASE_ID}-M2']
GUIDE_NAMES = {'png': 'layout.png', 'svg': 'layout.svg',
               'spec': 'layout.spec.json', 'manifest': 'layout.manifest.json'}
GUIDE_REFS = ('references/layout-guide.md', 'references/layout-guide-contract.md')


def read(path):
    return json.loads(Path(path).read_bytes())


def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


def relative_pins(items, root):
    return {str(Path(item['path']).relative_to(root)): (item['sha256'], item['bytes']) for item in items}


prepared_path = ROUND / 'planning/prepared-workspace.json'
prepared_pin = pin(prepared_path)
prepared = read(prepared_path)
assert prepared['candidate'] == 'AB'
assert len(prepared['runtime']) == 12 and len(prepared['actor_helpers']) == 20
for group in ('runtime', 'actor_helpers'):
    assert len({item['path'] for item in prepared[group]}) == len(prepared[group])
required_pins = prepared['runtime'] + prepared['actor_helpers'] + [
    prepared['case'], prepared['previous_full_closure'], prepared['previous_archive_index'],
    prepared['runtime_adoption'],
]
for item in required_pins:
    assert pin(item['path']) == item, item['path']
assert pin(CASE_PATH) == prepared['case']
assert {str(path.resolve()) for path in SNAP.rglob('*') if path.is_file()} == {item['path'] for item in prepared['runtime']}
assert relative_pins(prepared['runtime'], SNAP) == relative_pins([pin(LIVE / path) for path in relative_pins(prepared['runtime'], SNAP)], LIVE)

previous = read(prepared['previous_full_closure']['path'])
assert previous['all_actors_closed'] and previous['case'] == 'R23-C1'
assert previous['no_post_critic_repair_or_reselection']
r23_freeze_pin = previous['pre_generation_freeze']
assert pin(r23_freeze_pin['path']) == r23_freeze_pin
r23_freeze = read(r23_freeze_pin['path'])
assert r23_freeze['case_id'] == 'R23-C1' and r23_freeze['candidate'] == 'AA'
for item in r23_freeze['actor_helpers']:
    assert pin(item['path']) == item
assert relative_pins(prepared['actor_helpers'], ROUND) == relative_pins(r23_freeze['actor_helpers'], TASK / 'work/round23')
assert prepared['critic_helpers_changed_this_round'] is False
assert prepared['historical_critic_scope_clarification'] == r23_freeze['critic_scope_clarification']
assert prepared['historical_critic_scope_clarification']['numerical_scores_or_floors_changed'] is False
assert prepared['historical_critic_scope_clarification']['normalization'] == 'nfc-ws-optical-v1'

archive_path = Path(prepared['previous_archive_index']['path'])
archive = read(archive_path)
assert archive['source_root'] == str(TASK / 'work/round23')
assert archive['closed_evidence_source'] == 'planning/full-five-closure.json'


def archived_pin(source_pin):
    entries = [item for item in archive['files'] if item['source_absolute'] == source_pin['path']]
    assert len(entries) == 1
    entry = entries[0]
    assert entry['sha256'] == source_pin['sha256'] and entry['bytes'] == source_pin['bytes']
    actual = pin(archive_path.parent / entry['archive_relative'])
    assert actual['sha256'] == source_pin['sha256'] and actual['bytes'] == source_pin['bytes']
    return actual


# Require actual archived previous closure and freeze bytes before preparing jobs.
archived_closure_pin = archived_pin(prepared['previous_full_closure'])
archived_r23_freeze_pin = archived_pin(r23_freeze_pin)
adoption = read(prepared['runtime_adoption']['path'])
assert adoption['candidate'] == 'AB' and adoption['closed_previous_five'] == prepared['previous_full_closure']
assert adoption['closed_previous_archive_index'] == prepared['previous_archive_index']
assert adoption['quality_gates_changed'] is False and adoption['normalization'] == 'nfc-ws-optical-v1'
for item in adoption['runtime']:
    assert pin(item['path']) == item
assert relative_pins(adoption['runtime'], LIVE) == relative_pins(prepared['runtime'], SNAP)

corpus = read(CASE_PATH)
assert len(corpus['cases']) == 1
case = corpus['cases'][0]
assert case['case_id'] == CASE_ID and case['candidate'] == 'AB'
assert case['count'] == 5 and case['ratios'] == RATIOS
assert len(case['copy']) == 2 and not case['assets']
assert case['asset_readiness']['all_resolved'] and case['asset_readiness']['client_assets'] == 0
assert len(case['roles']) == 5
r23_case = read(r23_freeze['case']['path'])['cases'][0]
assert pin(r23_freeze['case']['path']) == r23_freeze['case']
for key in CASE_FIELDS[:-1]:
    assert case[key] == r23_case[key], f'Same known request changed: {key}'
plan_source_pin = pin(PLAN_SOURCE)
plan = copy.deepcopy(read(PLAN_SOURCE))
assert plan['case_id'] == CASE_ID
for case_field in CASE_FIELDS:
    assert plan[case_field] == case[case_field], case_field
assert len(plan['directions']) == 5
assert not plan.get('supporting_guides', []) and not plan.get('assets', [])
assert prepared['jobs_prepared'] == 0 and prepared['native_calls'] == 0 and prepared['supporting_guides_prepared'] == 0

guide_map_pin = pin(GUIDE_MAP_PATH)
guide_map = read(GUIDE_MAP_PATH)
assert set(guide_map) == set(GUIDE_ROLES)
guide_sources = {}
guide_source_pins = {}
for ordinal, (role, direction) in enumerate(zip(case['roles'], plan['directions']), 1):
    rid = role['role_id']
    assert rid == f'{CASE_ID}-M{ordinal}' and role['ordinal'] == ordinal
    assert role['ratio'] == RATIOS[ordinal - 1] and not role['assets']
    assert role['native_attempt_limit'] == 3 and role['own_correction_limit'] == 2
    assert {key: value for key, value in role.items() if key != 'role_id'} == {key: value for key, value in r23_case['roles'][ordinal - 1].items() if key != 'role_id'}
    assert direction['role'] == rid and direction['ratio'] == role['ratio']
    assert 'guide' not in direction and not direction.get('assets', [])
    if rid not in GUIDE_ROLES:
        assert 'guide_spec' not in direction
        continue
    assert isinstance(direction['guide_spec'], dict)
    files = guide_map[rid]
    assert isinstance(files, dict) and set(files) == set(GUIDE_NAMES)
    assert all(isinstance(value, str) and Path(value).is_absolute() for value in files.values())
    guide_sources[rid] = {key: Path(value).resolve(strict=True) for key, value in files.items()}
    assert all(path.is_file() and path.is_relative_to(TASK) for path in guide_sources[rid].values())
    guide_source_pins[rid] = {key: pin(path) for key, path in guide_sources[rid].items()}
    assert len({item['path'] for item in guide_source_pins[rid].values()}) == 4
    spec = read(guide_sources[rid]['spec'])
    assert spec == direction['guide_spec']
    assert len(spec['text_blocks']) == len(case['copy']) == 2
    assert sorted(block['copy'] for block in spec['text_blocks']) == sorted(entry['text'] for entry in case['copy'])
    for block in spec['text_blocks']:
        entry = next(entry for entry in case['copy'] if entry['text'] == block['copy'])
        assert block['fixed_newlines'] == entry['fixed_newlines']
        assert (block['lines'] == block['copy'].split('\n') if block['fixed_newlines'] else ' '.join(block['lines']) == block['copy'].replace('\n', ' '))
    manifest = read(guide_sources[rid]['manifest'])
    assert manifest['draft_only'] and manifest['purpose'] == 'optional native planning reference'
    assert manifest['input']['sha256'] == guide_source_pins[rid]['spec']['sha256']
    assert manifest['canvas'] == spec['canvas']
    for key in ('png', 'svg'):
        assert manifest['outputs'][key]['sha256'] == guide_source_pins[rid][key]['sha256']
    direction['guide'] = {
        'png_path': str(ROUND / 'production' / rid / 'guides/layout.png'),
        'role': 'Optional coordinator-owned actual-copy/font and expression planning reference; not a client asset, final artwork, protected geometry or native font-file-application proof',
    }

plan_path = ROUND / f'coordinator/{CASE_ID}/plan.json'
ratio_path = ROUND / 'planning/ratio-policy-before-generation.json'
jobs_path = ROUND / 'planning/prepared-maker-jobs.json'
queue_path = ROUND / 'planning/maker-queue.json'
freeze_path = ROUND / 'planning/candidate-ab-pre-generation-freeze.json'
for path in (plan_path, ratio_path, jobs_path, queue_path, freeze_path):
    assert not path.exists(), f'Refusing existing output: {path}'
for role in case['roles']:
    assert not (ROUND / 'production' / role['role_id']).exists()
plan['status'] = 'all-five same-request Title+body plan with two optional own guides, frozen before native generation'
write(plan_path, plan)
write(ratio_path, {
    'declared_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'policy': 'nearest-integer-single-edge', 'max_deviation_px': 0.5,
    'explicit_pixel_request_overrides': True,
    'source': 'Unchanged R23 aspect-only nearest-integer single-edge policy; no changed quality threshold.',
})

sys.path.insert(0, str(ROUND))
import prepare_production as prep
# Only in-memory orchestration changes; all 20 actor helper byte files stay exact.
prep.SKILL_FILES = tuple(dict.fromkeys(prep.SKILL_FILES + (
    'references/production-brief.md', 'references/design-grammar.md',
)))
original_maker_prompt = prep.maker_prompt
original_exclusive_json = prep.exclusive_json
own_guides = {}


def guided_inputs(rid):
    return [str(ROUND / 'production' / rid / 'guides' / name) for name in GUIDE_NAMES.values()] + [str(SNAP / relative) for relative in GUIDE_REFS]


def own_guide_maker_prompt(assignment, own_case, paths, role_dir, python):
    rid = assignment['role']
    if rid not in GUIDE_ROLES:
        return original_maker_prompt(assignment, own_case, paths, role_dir, python)
    directory = role_dir / 'guides'
    directory.mkdir(exist_ok=False)
    own_guides[rid] = {}
    for key, name in GUIDE_NAMES.items():
        target = directory / name
        with target.open('xb') as handle:
            handle.write(guide_sources[rid][key].read_bytes())
        own_guides[rid][key] = pin(target)
        assert own_guides[rid][key]['sha256'] == guide_source_pins[rid][key]['sha256']
        assert own_guides[rid][key]['bytes'] == guide_source_pins[rid][key]['bytes']
    text = original_maker_prompt(assignment, own_case, list(dict.fromkeys(paths + guided_inputs(rid))), role_dir, python)
    return text + f'''
OWN OPTIONAL COORDINATOR GUIDE: actually view {directory/'layout.png'} at original detail before the first native call; read {directory/'layout.spec.json'}, {directory/'layout.manifest.json'}, {SNAP/'references/layout-guide.md'} and {SNAP/'references/layout-guide-contract.md'}. {directory/'layout.svg'} is pinned supporting evidence. This is your own actual-copy/font and expression planning diagram, not a client image asset, final artwork or protected coordinate requirement. Only the supplied Title and body exist; do not invent roles. Soft display line breaks may replace source word spaces when fixed_newlines is false, while the immutable verification copy keeps every original word boundary and punctuation. Geometry, line counts and font sizes in the diagram are planning choices, not new client constraints. Do not open font files or execute the renderer. The diagram's actual-font anatomy does not assert native application of a font file.
Create the assigned complete image expression/editing, color/contrast, typographic voice, material/finish and emotion; the guide is a starting design reference. Good layouts, Title/body order and alignment may be shared. Five unique media/layouts/component values are not required, and superficial filter/palette/font substitution alone is insufficient. No original-artwork reopening, full catalog read or fresh browsing is required.
EXACT INITIAL REFERENCE BRANCH FOR THIS ROLE: pass referenced_image_paths:["{directory/'layout.png'}"] and omit num_last_images_to_include. Actually view that exact own PNG first and record its pin and planning role in pre-call.json. The case's client assets remain empty. For bounded repairs, include this same own guide plus the exact inspected previous returned own native target when one exists; after an actual failure use the last inspected own returned target if any, otherwise this own guide only. No peer guide/poster, coordinator source paths, additional reference or invented repair target. Preserve all actual failures and the unchanged three-call/two-repair limit. The focused native prompt prints the exact supplied copy once and describes the concrete design; do not pass plan/spec JSON or evaluation instructions.
'''


def own_guide_exclusive_json(path, value):
    if Path(path).name == 'job.json':
        rid = value['profile']
        if rid in GUIDE_ROLES:
            assert rid in own_guides
            value = copy.deepcopy(value)
            value['inputs'] = list(dict.fromkeys(value['inputs'] + guided_inputs(rid)))
    return original_exclusive_json(path, value)


prep.maker_prompt = own_guide_maker_prompt
prep.exclusive_json = own_guide_exclusive_json
try:
    result = prep.prepare(ROUND, CASE_PATH, [CASE_ID], SNAP)
finally:
    prep.maker_prompt = original_maker_prompt
    prep.exclusive_json = original_exclusive_json
assert result['prepared_jobs'] == 5 and result['launched'] is False
assert [row['role'] for row in result['jobs']] == [role['role_id'] for role in case['roles']]
assert set(own_guides) == set(GUIDE_ROLES)
input_groups = []
for row in result['jobs']:
    rid = row['role']
    job_path = Path(row['job']['path'])
    job = read(job_path)
    assert job['case_id'] == CASE_ID and job['profile'] == rid
    assert job['output_dir'] == str(ROUND / 'production' / rid)
    assert str(SNAP / 'references/production-brief.md') in job['inputs']
    assert str(SNAP / 'references/design-grammar.md') in job['inputs']
    assignment = read(row['assignment']['path'])
    if rid in GUIDE_ROLES:
        assert assignment['direction']['guide']['png_path'] == own_guides[rid]['png']['path']
        assert set(guided_inputs(rid)).issubset(job['inputs'])
    else:
        assert 'guide' not in assignment['direction'] and 'guide_spec' not in assignment['direction']
        assert not (Path(job['output_dir']) / 'guides').exists()
        assert all(str(SNAP / relative) not in job['inputs'] for relative in GUIDE_REFS)
    for input_path in job['inputs']:
        path = Path(input_path)
        assert not any(path.is_relative_to(ROUND / 'production' / other['role_id']) for other in case['roles'] if other['role_id'] != rid)
        assert not any(input_path == item['path'] for files in guide_source_pins.values() for item in files.values())
    row['job'] = pin(job_path)
    row['assignment'] = pin(row['assignment']['path'])
    row['prompt'] = pin(row['prompt']['path'])
    input_groups.append({'role': rid, 'inputs': [pin(path) for path in job['inputs']]})
write(jobs_path, result)
queue = [row['job']['path'] for row in result['jobs']]
write(queue_path, queue)
# Recheck every immutable source immediately before publishing the all-job freeze.
for item in required_pins + [r23_freeze_pin, archived_closure_pin, archived_r23_freeze_pin, guide_map_pin, plan_source_pin]:
    assert pin(item['path']) == item
for files in guide_source_pins.values():
    for item in files.values():
        assert pin(item['path']) == item
assert pin(prepared_path) == prepared_pin
own_guide_inputs = [own_guides[rid][key] for rid in GUIDE_ROLES for key in GUIDE_NAMES]
write(freeze_path, {
    'candidate': 'AB', 'case_id': CASE_ID, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'prepared_workspace': prepared_pin, 'runtime': prepared['runtime'], 'actor_helpers': prepared['actor_helpers'],
    'actor_helpers_identical_to_r23': True, 'critic_helpers_changed_this_round': False,
    'case': pin(CASE_PATH), 'expression_copy_plan_source': plan_source_pin, 'plan': pin(plan_path),
    'prepared_maker_jobs': pin(jobs_path), 'maker_queue': pin(queue_path),
    'maker_jobs': [row['job'] for row in result['jobs']],
    'maker_prompts': [row['prompt'] for row in result['jobs']],
    'maker_assignments': [row['assignment'] for row in result['jobs']], 'maker_input_pins': input_groups,
    'ratio_policy': pin(ratio_path), 'guide_roles': GUIDE_ROLES, 'selected_guide_map': guide_map_pin,
    'coordinator_guide_sources': guide_source_pins, 'guides_by_role': own_guides, 'own_guide_inputs': own_guide_inputs,
    'bounds': {'one_case': True, 'logical_maker_roles': 5, 'worker_process_max': 3,
               'initial_per_role': 1, 'repairs_per_role_max': 2, 'native_calls_max': 15},
    'client_assets': 0, 'supporting_guides': len(GUIDE_ROLES),
    'fresh_initial_contract': 'M1/M2 referenced_image_paths exactly [own production guide PNG], num_last_images_to_include absent; M3/M4/M5 both reference arguments absent.',
    'quality_method': 'Unchanged R23 seven categories, each >=4 per critic; all three diversity >=4 and mandatory conditions; nfc-ws-optical-v1. Historical R23 final-paragraph human style/shared-layout/actual-role clarification remains exact. All low/NA retained.',
    'historical_critic_scope_clarification': prepared['historical_critic_scope_clarification'],
    'new_quality_gates': 0, 'native_calls_at_freeze': 0,
    'r23_closure': prepared['previous_full_closure'], 'r23_archive_index': prepared['previous_archive_index'],
    'r23_archived_closure': archived_closure_pin, 'r23_pre_generation_freeze': r23_freeze_pin,
    'r23_archived_pre_generation_freeze': archived_r23_freeze_pin, 'runtime_adoption': prepared['runtime_adoption'],
    'orchestration_changes': ['In-memory brief/grammar runtime reads for all roles.',
                              'M1/M2 own four guide copies and layout-guide/contract reads before each prompt/job exclusive first write.',
                              'No prepared-job amendment, actor-helper byte change, actor launch or native call by this preparer.'],
    'limits': ['ONE same known urban-walking Title+body request five after exact R23 closure/archive; not a new-topic, held-out or isolated causal trial.',
               'AB first-native expression and exact-copy/display-break instructions, central design and two optional guides change together.',
               'Actor helpers including the historical critic paragraph are exact R23 bytes; numerical floors and optical-v1 normalization are unchanged.',
               'Guide font rendering and native type descriptions do not certify final font-file application, exact Unicode or universal quality.'],
})
print(json.dumps({'frozen': 'R24', 'makers': len(queue), 'native_calls': 0,
                  'guides': len(GUIDE_ROLES), 'freeze': pin(freeze_path)}))
