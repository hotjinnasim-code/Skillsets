"""Record actual closed maker roles without visual scores or selection changes."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round22'

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

freeze_path = ROUND / 'planning/candidate-z-pre-generation-freeze.json'
frozen = read(freeze_path)
for item in frozen['runtime'] + frozen['actor_helpers']:
    assert pin(item['path']) == item
# Reuse the unchanged pinned validator, including its all-three-failed terminal.
sys.path.insert(0, str(ROUND / 'method-recording-v2'))
import prepare_reviews_compact as review_preparer

case = read(ROUND / 'planning/single-five-case.json')['cases'][0]
rows = []
totals = {'native_calls': 0, 'returned': 0, 'failed': 0, 'repair_calls': 0}
initial_ref_parameters = []
for role in case['roles']:
    directory = ROUND / 'production' / role['role_id']
    completion = read(directory / 'completion.json')
    assert completion['exit_code'] == 0 and completion['input_pins_unchanged']
    assert len(completion['session_ids']) == 1
    terminal = review_preparer.terminal(ROUND / 'production', role, case['case_id'])
    assert terminal['closed'] and not terminal['errors'], terminal['errors']
    for key in totals:
        totals[key] += terminal['counts'][key]
    call = read(directory / 'stages/initial/call-input.json')
    assert str(directory / 'guides/layout.png') in call.get('referenced_image_paths', [])
    assert 'num_last_images_to_include' not in call
    # Preserve actual structure; do not infer supplied parameters from a label.
    initial_ref_parameters.append({'role': role['role_id'], 'call_input': pin(directory / 'stages/initial/call-input.json'), 'top_level_keys': list(call)})
    rows.append({
        'role': role['role_id'], 'completion': pin(directory / 'completion.json'),
        'sessions': completion['session_ids'], 'outcome': terminal['outcome'],
        'terminal': terminal['terminal'],
        'selection': terminal['terminal'] if terminal['outcome'] == 'selection' else None,
        'unavailable': terminal['terminal'] if terminal['outcome'] == 'unavailable' else None,
        'selected_stage': terminal.get('selected_stage'), 'counts': terminal['counts'],
    })
assert len(rows) == 5 and totals['native_calls'] <= 15
assert len({row['sessions'][0] for row in rows}) == 5
record = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'all_five_completed': True,
    'makers': rows, 'counts': totals,
    'initial_selected': sum(row['selected_stage'] == 'initial' for row in rows),
    'initial_retained_without_repairs': sum(row['selected_stage'] == 'initial' and row['counts']['repair_calls'] == 0 for row in rows),
    'unavailable_roles': sum(row['outcome'] == 'unavailable' for row in rows),
    'initial_call_structure_pins': initial_ref_parameters,
    'client_assets_remain_empty': True, 'supporting_guides_supplied': 5,
    'new_quality_gates': 0, 'quality_verdict': None,
    'no_external_scores_seen_before_selections': True,
    'limits': ['Actual actor completion/byte records, not proof of design quality.', 'Native prompt/type descriptions do not certify font-file application.'],
}
path = ROUND / 'planning/all-five-maker-closure.json'
with path.open('x', encoding='utf-8') as handle:
    json.dump(record, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps({'closure': pin(path), 'counts': totals, 'initial_selected': record['initial_selected'], 'without_repairs': record['initial_retained_without_repairs']}))
