"""Record the actual five AB maker terminals and per-role reference branches.

No scores, reselection, replacement role or native invocation is performed.
"""
from pathlib import Path
import datetime
import hashlib
import json
import sys

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round24'
CASE_ID = 'R24-C1'
GUIDE_ROLES = [f'{CASE_ID}-M1', f'{CASE_ID}-M2']
GUIDE_NAMES = {'png': 'layout.png', 'svg': 'layout.svg',
               'spec': 'layout.spec.json', 'manifest': 'layout.manifest.json'}


def read(path):
    return json.loads(Path(path).read_bytes())


def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}


freeze_path = ROUND / 'planning/candidate-ab-pre-generation-freeze.json'
frozen = read(freeze_path)
assert frozen['candidate'] == 'AB' and frozen['case_id'] == CASE_ID
for item in frozen['runtime'] + frozen['actor_helpers'] + frozen['maker_jobs'] + frozen['maker_prompts'] + frozen['maker_assignments'] + [
    frozen[key] for key in ('prepared_workspace', 'case', 'expression_copy_plan_source', 'plan',
                          'prepared_maker_jobs', 'maker_queue', 'ratio_policy', 'r23_closure',
                          'r23_archive_index', 'r23_archived_closure', 'r23_pre_generation_freeze',
                          'r23_archived_pre_generation_freeze', 'runtime_adoption', 'selected_guide_map')
]:
    assert pin(item['path']) == item, item['path']
for group in frozen['maker_input_pins']:
    for item in group['inputs']:
        assert pin(item['path']) == item, item['path']
assert frozen['client_assets'] == 0 and frozen['supporting_guides'] == 2
assert frozen['guide_roles'] == GUIDE_ROLES
assert frozen['actor_helpers_identical_to_r23'] and frozen['critic_helpers_changed_this_round'] is False
expected_own_pins = []
assert set(frozen['guides_by_role']) == set(frozen['coordinator_guide_sources']) == set(GUIDE_ROLES)
for rid in GUIDE_ROLES:
    assert set(frozen['guides_by_role'][rid]) == set(frozen['coordinator_guide_sources'][rid]) == set(GUIDE_NAMES)
    for key, name in GUIDE_NAMES.items():
        own_pin = frozen['guides_by_role'][rid][key]
        source_pin = frozen['coordinator_guide_sources'][rid][key]
        assert own_pin['path'] == str(ROUND / 'production' / rid / 'guides' / name)
        assert pin(own_pin['path']) == own_pin and pin(source_pin['path']) == source_pin
        assert own_pin['sha256'] == source_pin['sha256'] and own_pin['bytes'] == source_pin['bytes']
        expected_own_pins.append(own_pin)
assert frozen['own_guide_inputs'] == expected_own_pins
# Preserve the existing pinned terminal validator and actual all-three-failed branch.
sys.path.insert(0, str(ROUND / 'method-recording-v2'))
import prepare_reviews_compact as review_preparer

case = read(frozen['case']['path'])['cases'][0]
assert case['case_id'] == CASE_ID and case['count'] == 5 and len(case['roles']) == 5
jobs = read(frozen['prepared_maker_jobs']['path'])['jobs']
assert len(jobs) == 5 and [row['role'] for row in jobs] == [role['role_id'] for role in case['roles']]
input_groups = {group['role']: group['inputs'] for group in frozen['maker_input_pins']}
rows = []
totals = {'native_calls': 0, 'returned': 0, 'failed': 0, 'repair_calls': 0}
initial_ref_parameters = []
for role, job_row in zip(case['roles'], jobs):
    rid = role['role_id']
    directory = ROUND / 'production' / rid
    job = read(job_row['job']['path'])
    assert job['profile'] == rid and job['case_id'] == CASE_ID and job['output_dir'] == str(directory)
    assert [pin(path) for path in job['inputs']] == input_groups[rid]
    assignment = read(job_row['assignment']['path'])
    assert assignment['role'] == rid and not assignment['assets']
    guided = rid in GUIDE_ROLES
    expected_png = frozen['guides_by_role'][rid]['png']['path'] if guided else None
    if guided:
        assert assignment['direction']['guide']['png_path'] == expected_png
        assert all(item['path'] in job['inputs'] for item in frozen['guides_by_role'][rid].values())
    else:
        assert 'guide' not in assignment['direction'] and 'guide_spec' not in assignment['direction']
        assert not (directory / 'guides').exists()
    assert all(not Path(path).is_relative_to(ROUND / 'production' / other['role_id'])
               for path in job['inputs'] for other in case['roles'] if other['role_id'] != rid)
    completion = read(directory / 'completion.json')
    assert completion['exit_code'] == 0 and completion['input_pins_unchanged']
    assert completion.get('completed_utc')
    trace_path = Path(completion['trace']['path'])
    events = [json.loads(line) for line in trace_path.read_text().splitlines() if line.strip()]
    actual_sessions = [event['thread_id'] for event in events if isinstance(event, dict)
                       and event.get('type') == 'thread.started' and isinstance(event.get('thread_id'), str)
                       and event['thread_id']]
    assert actual_sessions == completion['session_ids'] and len(actual_sessions) == 1
    assert pin(trace_path)['sha256'] == completion['trace']['sha256']
    terminal = review_preparer.terminal(ROUND / 'production', role, CASE_ID)
    assert terminal['closed'] and not terminal['errors'], terminal['errors']
    assert terminal['outcome'] in ('selection', 'unavailable')
    counts = terminal['counts']
    assert 1 <= counts['native_calls'] <= 3 and 0 <= counts['repair_calls'] <= 2
    assert counts['returned'] + counts['failed'] == counts['native_calls']
    assert counts['repair_calls'] == counts['native_calls'] - 1
    if terminal['outcome'] == 'unavailable':
        assert counts == {'native_calls': 3, 'returned': 0, 'failed': 3, 'repair_calls': 2}
    for key in totals:
        totals[key] += counts[key]
    call_path = directory / 'stages/initial/call-input.json'
    call = read(call_path)
    assert 'num_last_images_to_include' not in call
    if guided:
        assert call.get('referenced_image_paths') == [expected_png]
    else:
        assert 'referenced_image_paths' not in call
    initial_ref_parameters.append({
        'role': rid, 'call_input': pin(call_path), 'top_level_keys': list(call),
        'guided': guided, 'expected_guide_png': expected_png,
        'both_reference_args_absent': not guided,
        'exact_own_guide_reference': guided,
    })
    rows.append({
        'role': rid, 'completion': pin(directory / 'completion.json'),
        'trace': pin(trace_path), 'sessions': actual_sessions, 'outcome': terminal['outcome'],
        'terminal': pin(terminal['terminal']['path']),
        'selection': pin(terminal['terminal']['path']) if terminal['outcome'] == 'selection' else None,
        'unavailable': pin(terminal['terminal']['path']) if terminal['outcome'] == 'unavailable' else None,
        'selected_stage': terminal.get('selected_stage'), 'counts': counts,
        'all_actual_stages': terminal['stages'],
    })
assert len(rows) == 5 and totals['native_calls'] <= 15
assert totals['returned'] + totals['failed'] == totals['native_calls']
assert len({row['sessions'][0] for row in rows}) == 5
record = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate': 'AB', 'case_id': CASE_ID,
    'all_five_completed': True, 'makers': rows, 'counts': totals,
    'initial_selected': sum(row['selected_stage'] == 'initial' for row in rows),
    'initial_retained_without_repairs': sum(row['selected_stage'] == 'initial' and row['counts']['repair_calls'] == 0 for row in rows),
    'unavailable_roles': sum(row['outcome'] == 'unavailable' for row in rows),
    'initial_call_structure_pins': initial_ref_parameters,
    'client_assets_remain_empty': True, 'supporting_guides_supplied': len(GUIDE_ROLES),
    'guide_roles': GUIDE_ROLES, 'own_guide_inputs': expected_own_pins,
    'maker_session_count': sum(len(row['sessions']) for row in rows), 'actual_session_ids_unique': True,
    'bounds': frozen['bounds'], 'pre_generation_freeze': pin(freeze_path),
    'new_quality_gates': 0, 'quality_verdict': None,
    'no_external_scores_seen_before_selections': True,
    'limits': ['Actual actor completion/terminal/attempt byte records, not proof of design quality.',
               'All failed and unselected attempts retained; no replacement role or budget reset.',
               'M1/M2 used exactly their own optional guide on initial; M3/M4/M5 initial reference arguments absent.',
               'Native prompt and guide type descriptions do not certify font-file application.'],
}
path = ROUND / 'planning/all-five-maker-closure.json'
with path.open('x', encoding='utf-8') as handle:
    json.dump(record, handle, ensure_ascii=False, indent=2, allow_nan=False)
    handle.write('\n')
print(json.dumps({'closure': pin(path), 'counts': totals, 'initial_selected': record['initial_selected'],
                  'without_repairs': record['initial_retained_without_repairs'], 'unavailable': record['unavailable_roles'],
                  'guides': record['supporting_guides_supplied']}))
