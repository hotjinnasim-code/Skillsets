"""Close the known-request AB five without changing raw judgments or selections.

Root runs this only after the actual maker and original critic waves close.
Every output is exclusive; no actor, native, renderer or repair is launched here.
"""
from pathlib import Path
import datetime
import hashlib
import json

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round24'
PROFILES = ('editorial', 'craft', 'portfolio')
CASE_ID = 'R24-C1'
CASE_FIELDS = ('request', 'copy', 'conditions', 'assets', 'count', 'ratios', 'styles', 'roles')
RATIOS = ['16:9', '16:9', '2:3', '2:3', '2:3']
GUIDE_ROLES = [f'{CASE_ID}-M1', f'{CASE_ID}-M2']
GUIDE_NAMES = {'png': 'layout.png', 'svg': 'layout.svg',
               'spec': 'layout.spec.json', 'manifest': 'layout.manifest.json'}


def read(path):
    if isinstance(path, dict):
        path = path['path']
    return json.loads(Path(path).read_bytes())


def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}


def pins(value):
    """Include nested guide source/own pins as well as the ordinary freeze inputs."""
    if isinstance(value, dict):
        if all(key in value for key in ('path', 'sha256', 'bytes')):
            yield value
        else:
            for child in value.values():
                yield from pins(child)
    elif isinstance(value, list):
        for child in value:
            yield from pins(child)


def write(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


freeze_path = ROUND / 'planning/candidate-ab-pre-generation-freeze.json'
frozen = read(freeze_path)
assert frozen['candidate'] == 'AB' and frozen['case_id'] == CASE_ID
assert len(frozen['runtime']) == 12 and len(frozen['actor_helpers']) == 20
assert len(frozen['maker_jobs']) == len(frozen['maker_prompts']) == len(frozen['maker_assignments']) == 5
for key in ('prepared_workspace', 'case', 'expression_copy_plan_source', 'plan',
            'prepared_maker_jobs', 'maker_queue', 'ratio_policy', 'r23_closure',
            'r23_archive_index', 'r23_archived_closure', 'runtime_adoption',
            'r23_pre_generation_freeze', 'selected_guide_map'):
    assert pin(frozen[key]['path']) == frozen[key], frozen[key]['path']
for item in pins(frozen):
    assert pin(item['path']) == item, item['path']
assert frozen['client_assets'] == 0 and frozen['supporting_guides'] == 2
assert frozen['native_calls_at_freeze'] == 0 and frozen['new_quality_gates'] == 0
assert frozen['guide_roles'] == GUIDE_ROLES
assert frozen['actor_helpers_identical_to_r23'] is True
assert set(frozen['guides_by_role']) == set(frozen['coordinator_guide_sources']) == set(GUIDE_ROLES)
own_guide_inputs = []
for role in GUIDE_ROLES:
    own = frozen['guides_by_role'][role]
    source = frozen['coordinator_guide_sources'][role]
    assert set(own) == set(source) == set(GUIDE_NAMES)
    for key, name in GUIDE_NAMES.items():
        assert own[key] == pin(ROUND / 'production' / role / 'guides' / name)
        assert (own[key]['sha256'], own[key]['bytes']) == (source[key]['sha256'], source[key]['bytes'])
        own_guide_inputs.append(own[key])
assert frozen['own_guide_inputs'] == own_guide_inputs

prepared = read(frozen['prepared_workspace'])
assert prepared['candidate'] == 'AB' and prepared['critic_helpers_changed_this_round'] is False
historical_clarification = frozen['historical_critic_scope_clarification']
assert historical_clarification == prepared['historical_critic_scope_clarification']
assert historical_clarification['changed_helper_files'] == ['critic_rubric.md']
assert historical_clarification['numerical_scores_or_floors_changed'] is False
assert historical_clarification['normalization'] == 'nfc-ws-optical-v1'

previous_frozen = read(frozen['r23_pre_generation_freeze'])
assert previous_frozen['candidate'] == 'AA' and previous_frozen['case_id'] == 'R23-C1'
assert pin(previous_frozen['case']['path']) == previous_frozen['case']
assert previous_frozen['critic_scope_clarification'] == historical_clarification
previous_helpers = {
    str(Path(item['path']).relative_to(TASK / 'work/round23')): item
    for item in previous_frozen['actor_helpers']
}
helper_identity = []
assert len(previous_helpers) == 20
for item in frozen['actor_helpers']:
    relative = str(Path(item['path']).relative_to(ROUND))
    prior = previous_helpers[relative]
    assert pin(prior['path']) == prior, prior['path']
    assert (item['sha256'], item['bytes']) == (prior['sha256'], prior['bytes']), relative
    helper_identity.append({'relative_path': relative, 'r24': item, 'r23': prior, 'byte_identical': True})
assert {row['relative_path'] for row in helper_identity} == set(previous_helpers)

previous = read(frozen['r23_closure'])
assert previous['all_actors_closed'] and previous['case'] == 'R23-C1'
assert frozen['r23_closure'] == prepared['previous_full_closure']
assert frozen['r23_archive_index'] == prepared['previous_archive_index']
archive_path = Path(frozen['r23_archive_index']['path'])
archive = read(archive_path)
assert archive['source_root'] == str(TASK / 'work/round23')
assert archive['closed_evidence_source'] == 'planning/full-five-closure.json'
archived_closure = next(item for item in archive['files'] if item['source_absolute'] == frozen['r23_closure']['path'])
assert archived_closure['sha256'] == frozen['r23_closure']['sha256']
assert archived_closure['bytes'] == frozen['r23_closure']['bytes']
assert frozen['r23_archived_closure'] == pin(archive_path.parent / archived_closure['archive_relative'])
assert (frozen['r23_archived_closure']['sha256'], frozen['r23_archived_closure']['bytes']) == (
    frozen['r23_closure']['sha256'], frozen['r23_closure']['bytes'])
assert frozen['runtime_adoption'] == prepared['runtime_adoption']
adoption = read(frozen['runtime_adoption'])
assert adoption['candidate'] == 'AB' and adoption['closed_previous_five'] == frozen['r23_closure']
assert adoption['closed_previous_archive_index'] == frozen['r23_archive_index']

case = read(frozen['case'])['cases'][0]
plan = read(frozen['plan'])
assert case['case_id'] == plan['case_id'] == CASE_ID and case['candidate'] == 'AB'
for field in CASE_FIELDS:
    assert plan[field] == case[field], field
assert case['count'] == 5 and case['ratios'] == RATIOS
assert len(case['copy']) == 2 and not case['assets'] and len(case['roles']) == 5
assert case['asset_readiness']['all_resolved'] and case['asset_readiness']['client_assets'] == 0
prior_case = read(previous_frozen['case'])['cases'][0]
for field in CASE_FIELDS[:-1]:
    assert case[field] == prior_case[field], field
for ordinal, role in enumerate(case['roles'], 1):
    assert role['role_id'] == f'{CASE_ID}-M{ordinal}' and role['ordinal'] == ordinal
    assert role['ratio'] == RATIOS[ordinal - 1] and not role['assets']
    assert role['native_attempt_limit'] == 3 and role['own_correction_limit'] == 2
assert not (ROUND / 'planning/full-five-closure.json').exists()
assert not (ROUND / 'report.md').exists()

maker_path = ROUND / 'planning/all-five-maker-closure.json'
maker = read(maker_path)
assert maker['candidate'] == 'AB' and maker['case_id'] == CASE_ID
assert maker['all_five_completed'] and len(maker['makers']) == 5
assert [row['role'] for row in maker['makers']] == [role['role_id'] for role in case['roles']]
assert maker['pre_generation_freeze'] == pin(freeze_path)
assert maker['counts']['native_calls'] <= 15
assert maker['counts']['returned'] + maker['counts']['failed'] == maker['counts']['native_calls']
assert maker['bounds'] == frozen['bounds']
assert maker['client_assets_remain_empty'] and maker['supporting_guides_supplied'] == 2
assert maker['own_guide_inputs'] == own_guide_inputs
assert len(maker['initial_call_structure_pins']) == 5
assert [row['role'] for row in maker['initial_call_structure_pins']] == [role['role_id'] for role in case['roles']]
for row in maker['initial_call_structure_pins']:
    assert pin(row['call_input']['path']) == row['call_input']
    guided = row['role'] in GUIDE_ROLES
    assert row['guided'] is guided
    expected_png = frozen['guides_by_role'][row['role']]['png']['path'] if guided else None
    assert row['expected_guide_png'] == expected_png
    call = read(row['call_input'])
    assert row['top_level_keys'] == list(call)
    assert 'num_last_images_to_include' not in call
    if guided:
        assert call.get('referenced_image_paths') == [expected_png]
    else:
        assert 'referenced_image_paths' not in call

sessions = []
totals = {'native_calls': 0, 'returned': 0, 'failed': 0, 'repair_calls': 0}
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
    assert row['counts']['repair_calls'] == row['counts']['native_calls'] - 1
    if row['outcome'] == 'unavailable':
        assert row['counts'] == {'native_calls': 3, 'returned': 0, 'failed': 3, 'repair_calls': 2}
    for key in totals:
        totals[key] += row['counts'][key]
    sessions.extend(completion['session_ids'])
assert totals == maker['counts']
maker_session_count = len(sessions)
assert maker_session_count == maker['maker_session_count'] == 5
assert len(set(sessions)) == maker_session_count and maker['actual_session_ids_unique']

waves = {}
for wave in ('initial', 'selected'):
    phase = ROUND / 'reviews' / CASE_ID / wave
    readiness_path = phase / 'readiness.json'
    state = read(readiness_path)
    reused = wave == 'selected' and (phase / 'reuse.json').is_file()
    if state['status'] == 'UNREADY':
        assert not state['jobs'] and not reused and not (phase / 'summary.json').is_file()
        assert not any((phase / 'cli' / profile / 'completion.json').is_file() for profile in PROFILES)
        waves[wave] = {
            'recording_mode': 'unready complete-set wave; original readiness retained without replacement critics',
            'readiness_mode': state.get('mode'),
            'procedure_gate': 'NA', 'procedure_errors': state['errors'],
            'image_gate_counts': {'PASS': 0, 'FAIL': 0, 'NA': 5},
            'image_gates': {row['role']: 'NA' for row in maker['makers']}, 'set_gate': 'NA',
            'counts': {'requested_images': 5, 'critics': 0, 'expected_critics': 3, 'expected_image_profile_records': 15,
                       'observed_image_profile_records': 0, 'expected_score_values': 105,
                       'observed_score_slots': 0, 'valid_integer_1_to_5_score_values': 0},
            'summary': None, 'readiness': pin(readiness_path), 'critics': {}, 'audits': [],
            'new_critic_processes': 0, 'new_critic_sessions': 0, 'new_score_values': 0,
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
    assert summary['case_id'] == CASE_ID and summary['wave'] == ('initial' if reused else wave)
    assert summary['counts']['expected_image_profile_records'] == 15
    assert summary['counts']['expected_score_values'] == 105
    actors = {}
    for profile in PROFILES:
        completion_path = (ROUND / 'reviews' / CASE_ID / 'initial' if reused else phase) / 'cli' / profile / 'completion.json'
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
        'audits': ([pin(ROUND / 'reviews' / CASE_ID / 'initial/source-asset-audit.json'), pin(phase / 'compact-binding-audit.json')] if reused else [pin(phase / name) for name in ('source-asset-audit.json', 'compact-binding-audit.json')]),
        'critics': actors,
        'recording_mode': 'exact whole-context original initial records retained' if reused else 'three fresh complete-set critic processes; original errors and raw retained',
        'new_critic_processes': 0 if reused else len(actors),
        'new_critic_sessions': 0 if reused else sum(len(actor['session_ids']) for actor in actors.values()),
        'new_score_values': 0 if reused else summary['counts']['valid_integer_1_to_5_score_values'],
    }
critic_session_count = sum(data['new_critic_sessions'] for data in waves.values())
critic_process_count = sum(data['new_critic_processes'] for data in waves.values())
assert critic_process_count in (0, 3, 6)
assert len(sessions) == maker_session_count + critic_session_count
for item in pins(frozen):
    assert pin(item['path']) == item, item['path']

closure = {
    'closed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'candidate': 'AB', 'case': CASE_ID, 'one_request': True, 'requested_images': 5,
    'new_topic_development': False, 'known_request_development': True, 'pre_held_out': False,
    **maker['counts'], 'initial_selected': maker['initial_selected'],
    'initial_retained_without_repairs': maker['initial_retained_without_repairs'],
    'unavailable_roles': maker['unavailable_roles'],
    'client_assets': 0, 'supporting_guides': 2, 'guide_roles': GUIDE_ROLES,
    'own_guide_inputs': own_guide_inputs, 'actual_copy_roles': ['Title', 'body'],
    'ratios': RATIOS,
    'maker_sessions': maker_session_count, 'critic_sessions': critic_session_count, 'all_actors_closed': True,
    'critic_processes': critic_process_count, 'actor_processes': len(maker['makers']) + critic_process_count,
    'actual_session_ids_unique': len(set(sessions)) == len(sessions),
    'production_closure': pin(maker_path), 'pre_generation_freeze': pin(freeze_path),
    'waves': waves, 'no_post_critic_repair_or_reselection': True,
    'quality_thresholds_changed': False,
    'diversity_interpretation_prospectively_changed_by_user': False,
    'historical_critic_scope_clarification': historical_clarification,
    'critic_helpers_changed_this_round': False, 'actor_helpers_identical_to_r23': True,
    'actor_helper_byte_identity': helper_identity,
    'normalization': 'nfc-ws-optical-v1',
    'critic_sessions_expected_if_all_fresh_traces_complete': critic_process_count,
    'new_critic_sessions_complete': critic_session_count == critic_process_count,
    'r23_closure': frozen['r23_closure'], 'r23_archive_index': frozen['r23_archive_index'],
    'r23_archived_closure': frozen['r23_archived_closure'],
    'r23_pre_generation_freeze': frozen['r23_pre_generation_freeze'],
    'runtime_adoption': frozen['runtime_adoption'], 'bounds': frozen['bounds'],
    'limits': [
        'ONE known urban-walking Title+body five using the same R23 request after exact R23 closure/archive; not a new topic, pre-held-out trial, isolated causal comparison or universal quality rate.',
        'AB general expression-first concrete form/edge/detail/light and single exact-copy-block method; source copy is unchanged and soft display line breaks occur only at supplied word boundaries.',
        'Only M1/M2 receive optional coordinator-authored own planning guides; these two guides are not requested posters, client assets or fixed geometry/font-file constraints.',
        'All 20 actor helpers are byte-identical to R23; its final-paragraph critic clarification is historical, with the same seven categories, all >=4 per critic, all three diversity >=4 and nfc-ws-optical-v1.',
        'All low scores, ambiguities, failures, transport errors and original selections remain retained.',
        'The existing native production architecture, font descriptions, actual-font guide anatomy and accumulated reference observations do not certify final font-file application, exact Unicode or every image being high-end.',
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
initial_record_link = (f'[최초 원집계](reviews/{CASE_ID}/initial/summary.json)' if waves['initial']['summary']
                       else f'[최초 준비 상태](reviews/{CASE_ID}/initial/readiness.json)')
report = f'''# R24 / AB - one known-request Title+body five

After checking exact R23 full-closure, archive, pre-generation freeze and AB adoption pins, this round used the same known urban-walking request about newly noticed light and traces. It is a further development observation on the closed R23 request. Actual supplied copy remains unchanged and has only two roles, Title and body, each appearing once; absent eyebrow, Subtitle, dates, places, footer, logo and QR are not invented or required. Requested ratios remain two landscape 16:9 roles followed by three portrait 2:3 roles. AB's general first-generation method resolves a concrete expression through form, edge, detail and light, then connects that expression with immediately recognizable Title and comfortably continuous body reading. Its native brief uses one exact printed-copy block, with optional display-only soft lines at supplied word boundaries and current source copy unchanged. Each maker received its own central direction and the current production-brief/design-grammar runtime inputs.

There are zero client assets and exactly two optional coordinator-authored own supporting guides, for M1 and M2 only. Each guided landscape role receives only its own pinned PNG/SVG/spec/manifest and includes the own PNG alone in its initial referenced_image_paths; num_last_images_to_include is absent. M3, M4 and M5 use direct initial native calls with both reference arguments absent. Guide drawings express an authored image/copy relationship and actual-font anatomy, while geometry and line choices remain planning aids. Guides are excluded from the five requested posters and client-fidelity requirements; they do not certify applied font files or visual quality. No source-artwork reopening or font/environment installation is required.

All 20 actor helper files are byte-identical to R23. The critic rubric's final-paragraph style and actual-copy-role clarification was adopted in that previous round and is retained as historical context here; no new critic-helper clarification was introduced. It assesses achieved whole style identity through image expression/editing, color/contrast, typographic voice, material/finish and emotion, allows shared good layouts/order/alignment, and assesses only actual supplied copy roles. Material labels or filter/palette/font substitutions alone remain insufficient, but five unique component values, media or layouts are not required. The same seven categories/scales, all seven >=4 for each critic, diversity >=4 for all three critics, mandatory conditions and nfc-ws-optical-v1 normalization remain in force. Prior raw judgments were not rescored or retrospectively reclassified.

Actual native calls: {counts['native_calls']}; returned: {counts['returned']}; failed: {counts['failed']}; repair calls: {counts['repair_calls']}. Initial selected: {maker['initial_selected']}; initial retained with no repair: {maker['initial_retained_without_repairs']}; unavailable after all three actual failures: {maker['unavailable_roles']}. Actual maker sessions: {maker_session_count}. The per-role maximum of three / total maximum of fifteen attempts is recorded with all failures and unselected attempts retained. The maximum of three workers is an operational bound, not independent evidence of actual simultaneous concurrency. Repairs are not new style roles.

| Wave | PASS | FAIL | NA | Set gate | Valid seven-dimension original values |
| --- | ---: | ---: | ---: | --- | ---: |
''' + '\n'.join(rows) + f'''

Initial and selected waves close according to their actual readiness and fresh/whole-context-reuse/UNREADY records. UNREADY retains original readiness errors, all five role NAs, zero new scores and zero new critics. Complete valid initial whole-context reuse retains the original scores without counting new processes or sessions. Incomplete or procedure-invalid reuse is not rescued with replacement critics. A fresh wave retains the original three profile processes, nonzero exits, actual error/turn.failed events, input-pin issues and trace errors, distinguishing process closure from procedural validity. Original low scores, ambiguities, procedure NA, diversity and maker selections are retained. New critic processes were initial {waves['initial']['new_critic_processes']} and selected {waves['selected']['new_critic_processes']}; actual new trace sessions were {waves['initial']['new_critic_sessions']} and {waves['selected']['new_critic_sessions']}. No averaging away a weak dimension, critic replacement, rescoring, post-critic native repair or reselection occurred.

[Full closure](planning/full-five-closure.json) | {initial_record_link} | [Selected readiness](reviews/{CASE_ID}/selected/readiness.json) | [Actual selected images](gallery.html)

This is one known-request development observation using AB's general expression/copy method, a central plan and two optional own guides. It does not establish a new-topic result, isolated causal effect, pre-held-out trial, universal high-end quality, AI authorship or universal success rate. Runtime instructions, central directions and optional guides change together; their effects are not isolated. The existing native production architecture is retained. Native copy, body forms and whole relationships must be assessed from actual original results and records; font names/specifications, guide anatomy and helper capabilities do not certify final font-file application or exact Unicode. Actual low/NA/failure/unselected denominators remain visible.
'''
with (ROUND / 'report.md').open('x', encoding='utf-8') as handle:
    handle.write(report)
print(json.dumps({
    'closure': pin(ROUND / 'planning/full-five-closure.json'), 'counts': counts,
    'initial_selected': maker['initial_selected'], 'unavailable_roles': maker['unavailable_roles'],
    'maker_sessions': maker_session_count, 'critic_processes': critic_process_count,
    'critic_sessions': critic_session_count,
    'waves': {wave: {'counts': data['image_gate_counts'], 'set': data['set_gate'],
                     'valid_original_score_values': data['counts']['valid_integer_1_to_5_score_values']}
              for wave, data in waves.items()},
    'limits': closure['limits'],
}))
