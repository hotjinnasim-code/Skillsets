"""Close a completed single five without changing raw judgments or selections."""
from pathlib import Path
import datetime
import hashlib
import json

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round23'
PROFILES = ('editorial', 'craft', 'portfolio')
CASE_ID = 'R23-C1'

def read(path):
    if isinstance(path, dict):
        path = path['path']
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

def write(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')

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
assert not (ROUND / 'planning/full-five-closure.json').exists()
assert not (ROUND / 'report.md').exists()
maker_path = ROUND / 'planning/all-five-maker-closure.json'
maker = read(maker_path)
assert maker['candidate'] == 'AA' and maker['case_id'] == CASE_ID
assert maker['all_five_completed'] and len(maker['makers']) == 5
assert maker['pre_generation_freeze'] == pin(freeze_path)
assert maker['counts']['native_calls'] <= 15
assert maker['counts']['returned'] + maker['counts']['failed'] == maker['counts']['native_calls']
assert maker['bounds'] == frozen['bounds']
sessions = []
for row in maker['makers']:
    assert pin(row['completion']['path']) == row['completion']
    assert pin(row['trace']['path']) == row['trace']
    assert row['outcome'] in ('selection', 'unavailable')
    assert pin(row['terminal']['path']) == row['terminal']
    if row['outcome'] == 'selection':
        assert row['selection'] == row['terminal'] and row['unavailable'] is None
    else:
        assert row['unavailable'] == row['terminal'] and row['selection'] is None
        assert row['selected_stage'] is None
    completion = read(row['completion'])
    assert completion['exit_code'] == 0 and completion['input_pins_unchanged']
    assert completion['session_ids'] == row['sessions']
    assert 1 <= row['counts']['native_calls'] <= 3 and 0 <= row['counts']['repair_calls'] <= 2
    assert row['counts']['returned'] + row['counts']['failed'] == row['counts']['native_calls']
    if row['outcome'] == 'unavailable':
        assert row['counts'] == {'native_calls': 3, 'returned': 0, 'failed': 3, 'repair_calls': 2}
    sessions.extend(completion['session_ids'])
maker_session_count = len(sessions)
assert maker_session_count == 5 and len(set(sessions)) == maker_session_count

waves = {}
for wave in ('initial', 'selected'):
    phase = ROUND / 'reviews/R23-C1' / wave
    readiness_path = phase / 'readiness.json'
    state = read(readiness_path)
    reused = wave == 'selected' and (phase / 'reuse.json').is_file()
    if state['status'] == 'UNREADY':
        assert not state['jobs'] and not reused and not (phase / 'summary.json').is_file()
        assert not any((phase / 'cli' / profile / 'completion.json').is_file() for profile in PROFILES)
        waves[wave] = {
            'recording_mode':'unready complete-set wave; original readiness retained without replacement critics',
            'readiness_mode':state.get('mode'),
            'procedure_gate':'NA','procedure_errors':state['errors'],
            'image_gate_counts':{'PASS':0,'FAIL':0,'NA':5},
            'image_gates':{row['role']:'NA' for row in maker['makers']},'set_gate':'NA',
            'counts':{'requested_images':5,'critics':0,'expected_critics':3,'expected_image_profile_records':15,
                      'observed_image_profile_records':0,'expected_score_values':105,
                      'observed_score_slots':0,'valid_integer_1_to_5_score_values':0},
            'summary':None,'readiness':pin(readiness_path),'critics':{},'audits':[],
            'new_critic_processes':0,'new_critic_sessions':0,'new_score_values':0,
        }
        continue
    assert state['status'] == 'READY'
    if reused:
        assert state['mode'] == 'COMPLETE_FIRST_THREE_REUSED'
        assert all(row['selected_stage'] == 'initial' for row in maker['makers'])
        reuse = read(phase / 'reuse.json')
        assert read(phase / 'compact-binding-audit.json')['gate'] == 'PASS'
        assert pin(reuse['initial_summary']['path'])['sha256'] == reuse['initial_summary']['sha256']
        summary_path = Path(reuse['initial_summary']['path'])
    else:
        assert state['mode'] == 'THREE_FRESH_COMPLETE_CRITICS' and len(state['jobs']) == 3
        summary_path = phase / 'summary.json'
    summary = read(summary_path)
    assert summary['case_id'] == 'R23-C1' and summary['wave'] == ('initial' if reused else wave)
    assert summary['counts']['expected_image_profile_records'] == 15
    assert summary['counts']['expected_score_values'] == 105
    actors = {}
    for profile in PROFILES:
        completion_path = (ROUND / 'reviews/R23-C1/initial' if reused else phase) / 'cli' / profile / 'completion.json'
        completion = read(completion_path)
        # A process can close with a nonzero exit; the original summary retains
        # its procedure NA rather than requiring a replacement critic.
        assert type(completion['exit_code']) is int and completion.get('completed_utc')
        trace_path = Path(completion['trace']['path'])
        trace_error = None
        try:
            events = [json.loads(line) for line in trace_path.read_text().splitlines() if line.strip()]
        except (ValueError, OSError) as exc:
            events = []
            trace_error = str(exc)
        actual_sessions = [event['thread_id'] for event in events if isinstance(event, dict)
                           and event.get('type') == 'thread.started' and isinstance(event.get('thread_id'), str)
                           and event['thread_id']]
        if not reused:
            sessions.extend(actual_sessions)
        actors[profile] = {
            'completion': pin(completion_path), 'completed_utc': completion['completed_utc'],
            'exit_code': completion['exit_code'], 'input_pins_unchanged': completion.get('input_pins_unchanged'),
            'trace': pin(trace_path) if trace_path.is_file() else None,
            'trace_path': str(trace_path), 'reported_trace': completion['trace'], 'trace_read_error': trace_error,
            'session_ids': actual_sessions, 'reported_session_ids': completion.get('session_ids'),
            'session_ids_match_trace': actual_sessions == completion.get('session_ids'),
            'trace_error_events_retained': [event for event in events if isinstance(event, dict)
                                           and event.get('type') in ('error', 'turn.failed')],
        }
    waves[wave] = {
        **{key: summary[key] for key in ('procedure_gate', 'procedure_errors', 'image_gate_counts', 'image_gates', 'set_gate', 'counts')},
        'summary': pin(summary_path),
        'readiness': pin(readiness_path), 'readiness_mode': state['mode'],
        'diversity_original': {profile: summary['reviews'][profile]['set']['raw'].get('diversity') for profile in PROFILES},
        'audits': ([pin(ROUND / 'reviews/R23-C1/initial/source-asset-audit.json'),pin(phase / 'compact-binding-audit.json')] if reused else [pin(phase / name) for name in ('source-asset-audit.json', 'compact-binding-audit.json')]),
        'critics': actors,
        'recording_mode':'exact whole-context original initial records retained' if reused else 'three fresh complete-set critic processes; original errors and raw retained',
        'new_critic_processes':0 if reused else len(actors),
        'new_critic_sessions':0 if reused else sum(len(actor['session_ids']) for actor in actors.values()),
        'new_score_values':0 if reused else summary['counts']['valid_integer_1_to_5_score_values'],
    }
critic_session_count = sum(data['new_critic_sessions'] for data in waves.values())
critic_process_count = sum(data['new_critic_processes'] for data in waves.values())
assert critic_process_count in (0,3,6)
assert len(sessions) == maker_session_count + critic_session_count
for row in read(freeze_path)['runtime']:
    assert pin(row['path']) == row

closure = {
    'closed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'candidate': 'AA', 'case': 'R23-C1', 'one_request': True, 'requested_images': 5,
    'new_topic_development': True, 'pre_held_out': False,
    **maker['counts'], 'initial_selected': maker['initial_selected'],
    'initial_retained_without_repairs': maker['initial_retained_without_repairs'],
    'unavailable_roles': maker['unavailable_roles'],
    'client_assets': 0, 'supporting_guides': 0, 'actual_copy_roles': ['Title', 'body'],
    'ratios': ['16:9', '16:9', '2:3', '2:3', '2:3'],
    'maker_sessions': maker_session_count, 'critic_sessions': critic_session_count, 'all_actors_closed': True,
    'critic_processes': critic_process_count, 'actor_processes': len(maker['makers']) + critic_process_count,
    'actual_session_ids_unique': len(set(sessions)) == len(sessions),
    'production_closure': pin(maker_path), 'pre_generation_freeze': pin(freeze_path),
    'waves': waves, 'no_post_critic_repair_or_reselection': True,
    'quality_thresholds_changed': False,
    'diversity_interpretation_prospectively_changed_by_user': True,
    'critic_scope_clarification': frozen['critic_scope_clarification'],
    'normalization': 'nfc-ws-optical-v1',
    'critic_sessions_expected_if_all_fresh_traces_complete': critic_process_count,
    'new_critic_sessions_complete': critic_session_count == critic_process_count,
    'r22_closure': frozen['r22_closure'], 'r22_archive_index': frozen['r22_archive_index'],
    'runtime_adoption': frozen['runtime_adoption'],
    'bounds': frozen['bounds'],
    'limits': [
        'ONE new-topic urban-walking Title+body five after exact R22 closure/archive; not a pre-held-out trial, isolated causal comparison or universal quality rate.',
        'All low scores, ambiguities, failures, transport errors and original selections remain retained.',
        'Native font descriptions and accumulated reference observations do not certify applied font files, exact Unicode or every image being high-end.',
        'Five logical maker roles with an operational maximum of three workers; this limit is not independent evidence of actual simultaneous concurrency.',
    ],
}
write(ROUND / 'planning/full-five-closure.json', closure)
counts = maker['counts']
rows = []
for wave, label in (('initial', '최초'), ('selected', '선택')):
    data = waves[wave]
    c = data['image_gate_counts']
    rows.append(f"| {label} | {c['PASS']} | {c['FAIL']} | {c['NA']} | {data['set_gate']} | {data['counts']['valid_integer_1_to_5_score_values']} / 105 |")
initial_record_link = ('[최초 원집계](reviews/R23-C1/initial/summary.json)' if waves['initial']['summary']
                       else '[최초 준비 상태](reviews/R23-C1/initial/readiness.json)')
report = f'''# R23 / AA - one new-topic Title+body five

After checking exact R22 full-closure and archive pins, this round used ONE new urban-walking request about newly noticed light and traces. Actual supplied copy has only two roles, Title and body, each appearing once; absent eyebrow, Subtitle, dates, places, footer, logo and QR are not invented or required. Requested ratios are two landscape 16:9 roles followed by three portrait 2:3 roles. AA's general first-generation method distinguishes nominal em and area fit from actual optical body readability, then resolves the needed continuous sentence area jointly with an immediately recognizable Title's weight/contrast/space and image distance/crop/opening. Each maker received its own central direction and the current production-brief/design-grammar runtime inputs. This common Title+body case has no practical information, no mandatory guide, zero supporting guides and zero client assets. Fresh initial native argument objects omit both reference arguments. No source-artwork reopening or font/environment installation is required.

Only the critic rubric's final paragraph was prospectively clarified among the existing actor helpers. It assesses achieved whole style identity through image expression/editing, color/contrast, typographic voice, material/finish and emotion, allows shared good layouts/order/alignment, and assesses only actual supplied copy roles. Material labels or filter/palette/font substitutions alone remain insufficient, but five unique component values, media or layouts are not required. The same seven categories/scales, each critic's dimension and diversity floors of 4, mandatory conditions and nfc-ws-optical-v1 normalization remain in force. This is not a claim that all helper/method bytes are unchanged. R22 raw judgments were not rescored or retrospectively reclassified.

Actual native calls: {counts['native_calls']}; returned: {counts['returned']}; failed: {counts['failed']}; repair calls: {counts['repair_calls']}. Initial selected: {maker['initial_selected']}; initial retained with no repair: {maker['initial_retained_without_repairs']}; unavailable after all three actual failures: {maker['unavailable_roles']}. Five actual maker sessions and the per-role maximum of three / total maximum of fifteen attempts are recorded with all failures and unselected attempts retained. The maximum of three workers is an operational bound, not independent evidence of actual simultaneous concurrency. Repairs are not new style roles.

| Wave | PASS | FAIL | NA | Set gate | Valid seven-dimension original values |
| --- | ---: | ---: | ---: | --- | ---: |
''' + '\n'.join(rows) + f'''

Initial and selected waves close according to their actual readiness and fresh/whole-context-reuse/UNREADY records. UNREADY retains original readiness errors, all five role NAs, zero new scores and zero new critics. Complete valid initial whole-context reuse retains the original scores without counting new processes or sessions. Incomplete or procedure-invalid reuse is not rescued with replacement critics. A fresh wave retains the original three profile processes, nonzero exits, actual error/turn.failed events, input-pin issues and trace errors, distinguishing process closure from procedural validity. Original low scores, ambiguities, procedure NA, diversity and maker selections are retained. New critic processes were initial {waves['initial']['new_critic_processes']} and selected {waves['selected']['new_critic_processes']}; actual new trace sessions were {waves['initial']['new_critic_sessions']} and {waves['selected']['new_critic_sessions']}. No averaging away a weak dimension, critic replacement, rescoring, post-critic native repair or reselection occurred.

[Full closure](planning/full-five-closure.json) | {initial_record_link} | [Selected readiness](reviews/R23-C1/selected/readiness.json) | [Actual selected images](gallery.html)

This is one new-topic development observation using AA's general optical body/Title-area method, a central plan and a prospective final-paragraph critic clarification. It does not establish an isolated causal effect, a pre-held-out trial, universal high-end quality, AI authorship or universal success rate. Native copy, body forms and whole relationships must be assessed from actual original results and records; font names/specifications/helper capabilities do not certify final font-file application or exact Unicode. Actual low/NA/failure/unselected denominators remain visible.
'''
with (ROUND / 'report.md').open('x', encoding='utf-8') as handle:
    handle.write(report)
print(json.dumps({'closure': pin(ROUND / 'planning/full-five-closure.json'), 'waves': {wave: {'counts': data['image_gate_counts'], 'set': data['set_gate']} for wave, data in waves.items()}}))
