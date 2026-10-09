"""Freeze ONE new-topic AA Title+body five before any native generation.

This script prepares jobs only when root executes it; it launches no actors.
All outputs are exclusive. Common Title+body uses no mandatory planning guide.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import sys

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round23'
SNAP = ROUND / 'snapshots/candidate-aa'
CASE_PATH = ROUND / 'planning/single-five-case.json'
PLAN_SOURCE = TASK / 'drafts/aa-five-design/plan.json'
CASE_ID = 'R23-C1'
CASE_FIELDS = ('request', 'copy', 'conditions', 'assets', 'count', 'ratios', 'styles', 'roles')
RATIOS = ['16:9', '16:9', '2:3', '2:3', '2:3']


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


prepared_path = ROUND / 'planning/prepared-workspace.json'
prepared_pin = pin(prepared_path)
prepared = read(prepared_path)
assert prepared['candidate'] == 'AA'
assert len(prepared['runtime']) == 12 and len(prepared['actor_helpers']) == 20
for group in ('runtime', 'actor_helpers'):
    assert len({item['path'] for item in prepared[group]}) == len(prepared[group])
required_pins = prepared['runtime'] + prepared['actor_helpers'] + [
    prepared['case'], prepared['previous_full_closure'], prepared['previous_archive_index'],
    prepared['runtime_adoption'],
] + list(prepared['critic_scope_clarification'][key] for key in ('source', 'old', 'adopted'))
for item in required_pins:
    assert pin(item['path']) == item, item['path']
assert pin(CASE_PATH) == prepared['case']
assert {str(path.resolve()) for path in SNAP.rglob('*') if path.is_file()} == {item['path'] for item in prepared['runtime']}
previous = read(prepared['previous_full_closure']['path'])
assert previous['all_actors_closed'] and previous['case'] == 'R22-C1'
archive_path = Path(prepared['previous_archive_index']['path'])
archive = read(archive_path)
assert archive['source_root'] == str(TASK / 'work/round22')
assert archive['closed_evidence_source'] == 'planning/full-five-closure.json'
archived_closure = next(item for item in archive['files'] if item['source_absolute'] == prepared['previous_full_closure']['path'])
assert archived_closure['sha256'] == prepared['previous_full_closure']['sha256']
assert archived_closure['bytes'] == prepared['previous_full_closure']['bytes']
archived_closure_pin = pin(archive_path.parent / archived_closure['archive_relative'])
assert archived_closure_pin['sha256'] == archived_closure['sha256'] and archived_closure_pin['bytes'] == archived_closure['bytes']
adoption = read(prepared['runtime_adoption']['path'])
assert adoption['candidate'] == 'AA' and adoption['closed_previous_five'] == prepared['previous_full_closure']
assert adoption['closed_previous_archive_index'] == prepared['previous_archive_index']
assert prepared['critic_scope_clarification']['changed_helper_files'] == ['critic_rubric.md']
assert prepared['critic_scope_clarification']['numerical_scores_or_floors_changed'] is False
assert prepared['critic_scope_clarification']['normalization'] == 'nfc-ws-optical-v1'
old_rubric = Path(prepared['critic_scope_clarification']['old']['path']).read_bytes()
new_rubric = Path(prepared['critic_scope_clarification']['adopted']['path']).read_bytes()
old_final = old_rubric.index(b'For this single-five candidate, assess complete visual systems:')
new_final = new_rubric.index(b'For a future single-five review using this clarification,')
assert old_rubric[:old_final] == new_rubric[:new_final]
floor_sentence = 'Critic scores remain the same seven categories, each 1\u20135 with located evidence, all >=4 per critic for PASS.\n'.encode('utf-8')
assert old_rubric.endswith(floor_sentence) and new_rubric.endswith(floor_sentence)

corpus = read(CASE_PATH)
assert len(corpus['cases']) == 1
case = corpus['cases'][0]
assert case['case_id'] == CASE_ID and case['candidate'] == 'AA'
assert case['count'] == 5 and case['ratios'] == RATIOS
assert len(case['copy']) == 2 and not case['assets']
assert case['asset_readiness']['all_resolved'] and case['asset_readiness']['client_assets'] == 0
assert len(case['roles']) == 5
plan_source_pin = pin(PLAN_SOURCE)
plan = copy.deepcopy(read(PLAN_SOURCE))
assert plan['case_id'] == CASE_ID
for case_field in CASE_FIELDS:
    assert plan[case_field] == case[case_field], case_field
assert len(plan['directions']) == 5
for ordinal, (role, direction) in enumerate(zip(case['roles'], plan['directions']), 1):
    assert role['role_id'] == f'{CASE_ID}-M{ordinal}' and role['ordinal'] == ordinal
    assert role['ratio'] == RATIOS[ordinal - 1] and not role['assets']
    assert role['native_attempt_limit'] == 3 and role['own_correction_limit'] == 2
    assert direction['role'] == role['role_id'] and direction['ratio'] == role['ratio']
    assert 'guide' not in direction and not direction.get('assets', [])
assert not plan.get('supporting_guides', [])
assert prepared['jobs_prepared'] == 0 and prepared['native_calls'] == 0 and prepared['supporting_guides'] == 0

plan_path = ROUND / f'coordinator/{CASE_ID}/plan.json'
ratio_path = ROUND / 'planning/ratio-policy-before-generation.json'
jobs_path = ROUND / 'planning/prepared-maker-jobs.json'
queue_path = ROUND / 'planning/maker-queue.json'
freeze_path = ROUND / 'planning/candidate-aa-pre-generation-freeze.json'
for path in (plan_path, ratio_path, jobs_path, queue_path, freeze_path):
    assert not path.exists(), f'Refusing existing output: {path}'
for role in case['roles']:
    assert not (ROUND / 'production' / role['role_id']).exists()
plan['status'] = 'all-five new-topic Title+body plan, frozen before native generation'
write(plan_path, plan)
write(ratio_path, {
    'declared_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'policy': 'nearest-integer-single-edge', 'max_deviation_px': 0.5,
    'explicit_pixel_request_overrides': True,
    'source': 'Unchanged R22 aspect-only nearest-integer single-edge policy; no changed quality threshold.',
})

sys.path.insert(0, str(ROUND))
import prepare_production as prep
# Extend the existing preparer's input list in memory, before its exclusive writes.
# No actor helper, prepared prompt/job or runtime file is rewritten.
prep.SKILL_FILES = tuple(dict.fromkeys(prep.SKILL_FILES + (
    'references/production-brief.md', 'references/design-grammar.md',
)))
result = prep.prepare(ROUND, CASE_PATH, [CASE_ID], SNAP)
assert result['prepared_jobs'] == 5 and result['launched'] is False
assert [row['role'] for row in result['jobs']] == [role['role_id'] for role in case['roles']]
input_groups = []
for row in result['jobs']:
    job_path = Path(row['job']['path'])
    job = read(job_path)
    assert job['case_id'] == CASE_ID and job['profile'] == row['role']
    assert str(SNAP / 'references/production-brief.md') in job['inputs']
    assert str(SNAP / 'references/design-grammar.md') in job['inputs']
    assert not (Path(job['output_dir']) / 'guides').exists()
    row['job'] = pin(job_path)
    row['assignment'] = pin(row['assignment']['path'])
    row['prompt'] = pin(row['prompt']['path'])
    input_groups.append({'role': row['role'], 'inputs': [pin(path) for path in job['inputs']]})
write(jobs_path, result)
queue = [row['job']['path'] for row in result['jobs']]
write(queue_path, queue)
# Recheck immutable inputs immediately before publishing the all-job freeze.
for item in required_pins:
    assert pin(item['path']) == item
assert pin(prepared_path) == prepared_pin
assert pin(PLAN_SOURCE) == plan_source_pin
write(freeze_path, {
    'candidate': 'AA', 'case_id': CASE_ID, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'prepared_workspace': prepared_pin,
    'runtime': prepared['runtime'], 'actor_helpers': prepared['actor_helpers'], 'case': pin(CASE_PATH),
    'optical_body_plan_source': plan_source_pin, 'plan': pin(plan_path),
    'prepared_maker_jobs': pin(jobs_path), 'maker_queue': pin(queue_path),
    'maker_jobs': [row['job'] for row in result['jobs']],
    'maker_prompts': [row['prompt'] for row in result['jobs']],
    'maker_assignments': [row['assignment'] for row in result['jobs']],
    'maker_input_pins': input_groups,
    'ratio_policy': pin(ratio_path),
    'bounds': {'one_case': True, 'logical_maker_roles': 5, 'worker_process_max': 3,
               'initial_per_role': 1, 'repairs_per_role_max': 2, 'native_calls_max': 15},
    'client_assets': 0, 'supporting_guides': 0,
    'fresh_initial_contract': 'Both referenced_image_paths and num_last_images_to_include absent; no guide or client assets.',
    'quality_method': 'Same seven score categories, each >=4 per critic, diversity >=4 for each of three critics and mandatory conditions; nfc-ws-optical-v1 normalization. Only final critic paragraph is prospectively clarified for human style priority/shared good layouts and actual supplied copy roles. All low/NA retained.',
    'critic_scope_clarification': prepared['critic_scope_clarification'],
    'new_quality_gates': 0, 'native_calls_at_freeze': 0,
    'r22_closure': prepared['previous_full_closure'],
    'r22_archive_index': prepared['previous_archive_index'], 'r22_archived_closure': archived_closure_pin,
    'runtime_adoption': prepared['runtime_adoption'],
    'limits': [
        'ONE new-topic Title+body development five after exact R22 closure/archive, not a pre-held-out or isolated causal trial.',
        'AA general optical body/Title/image area design; only two supplied copy roles and no mandatory guide or source-artwork reopening.',
        'Runtime/central plan and prospective final-paragraph critic scope changed; numerical floors and optical-v1 normalization did not. No claim all helper/method bytes are unchanged.',
        'Native descriptions and guide-font capabilities do not certify final font-file application, Unicode or universal quality.',
    ],
})
print(json.dumps({'frozen': 'R23', 'makers': len(queue), 'native_calls': 0, 'guides': 0, 'freeze': pin(freeze_path)}))
