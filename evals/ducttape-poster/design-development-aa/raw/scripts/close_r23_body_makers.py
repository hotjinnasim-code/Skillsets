"""Record actual five closed AA maker roles without scores or selection changes."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round23'
CASE_ID = 'R23-C1'


def read(path):
    return json.loads(Path(path).read_bytes())


def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}


freeze_path = ROUND / 'planning/candidate-aa-pre-generation-freeze.json'
frozen = read(freeze_path)
assert frozen['candidate'] == 'AA' and frozen['case_id'] == CASE_ID
for item in frozen['runtime'] + frozen['actor_helpers'] + frozen['maker_jobs'] + frozen['maker_prompts'] + frozen['maker_assignments'] + [
    frozen[key] for key in ('prepared_workspace', 'case', 'optical_body_plan_source', 'plan',
                          'prepared_maker_jobs', 'maker_queue', 'ratio_policy', 'r22_closure',
                          'r22_archive_index', 'r22_archived_closure', 'runtime_adoption')
]:
    assert pin(item['path']) == item, item['path']
for group in frozen['maker_input_pins']:
    for item in group['inputs']:
        assert pin(item['path']) == item, item['path']
assert frozen['client_assets'] == 0 and frozen['supporting_guides'] == 0
# Use the same pinned terminal validator, including actual all-three-failed closure.
sys.path.insert(0, str(ROUND / 'method-recording-v2'))
import prepare_reviews_compact as review_preparer

case = read(frozen['case']['path'])['cases'][0]
assert case['case_id'] == CASE_ID and case['count'] == 5 and len(case['roles']) == 5
rows = []
totals = {'native_calls': 0, 'returned': 0, 'failed': 0, 'repair_calls': 0}
initial_ref_parameters = []
for role in case['roles']:
    directory = ROUND / 'production' / role['role_id']
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
    assert 'referenced_image_paths' not in call and 'num_last_images_to_include' not in call
    initial_ref_parameters.append({'role': role['role_id'], 'call_input': pin(call_path),
                                   'top_level_keys': list(call), 'both_reference_args_absent': True})
    rows.append({
        'role': role['role_id'], 'completion': pin(directory / 'completion.json'),
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
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate': 'AA', 'case_id': CASE_ID,
    'all_five_completed': True, 'makers': rows, 'counts': totals,
    'initial_selected': sum(row['selected_stage'] == 'initial' for row in rows),
    'initial_retained_without_repairs': sum(row['selected_stage'] == 'initial' and row['counts']['repair_calls'] == 0 for row in rows),
    'unavailable_roles': sum(row['outcome'] == 'unavailable' for row in rows),
    'initial_call_structure_pins': initial_ref_parameters,
    'client_assets_remain_empty': True, 'supporting_guides_supplied': 0,
    'maker_session_count': sum(len(row['sessions']) for row in rows), 'actual_session_ids_unique': True,
    'bounds': frozen['bounds'], 'pre_generation_freeze': pin(freeze_path),
    'new_quality_gates': 0, 'quality_verdict': None,
    'no_external_scores_seen_before_selections': True,
    'limits': ['Actual actor completion/terminal/attempt byte records, not proof of design quality.',
               'All failed and unselected attempts retained; no replacement role or budget reset.',
               'Native prompt/type descriptions do not certify font-file application.'],
}
path = ROUND / 'planning/all-five-maker-closure.json'
with path.open('x', encoding='utf-8') as handle:
    json.dump(record, handle, ensure_ascii=False, indent=2, allow_nan=False)
    handle.write('\n')
print(json.dumps({'closure': pin(path), 'counts': totals, 'initial_selected': record['initial_selected'],
                  'without_repairs': record['initial_retained_without_repairs'], 'unavailable': record['unavailable_roles']}))
