"""Root-only closure of one five-poster run; never alters actor inputs or scores."""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path
from reuse_binding import check_reuse
from prepare_reviews_v2 import terminal as validate_terminal

ROOT = Path(__file__).resolve().parent
PROFILES = ('editorial', 'craft', 'portfolio')

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path)
    assert '..' not in path.parts and not any(p.is_symlink() for p in (path, *path.parents)), 'Symlink/traversal in evidence path'
    path = path.resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

def checked(row):
    actual = pin(row['path'])
    assert actual['sha256'] == row['sha256'], 'Changed frozen input: ' + row['path']
    return actual

def returned_source(caller):
    """Read only typed caller fields and the exact native return-hint grammar."""
    representations = []
    if 'returned_source_path' in caller:
        value = caller['returned_source_path']
        assert isinstance(value, str), 'Unsealable returned-source field'
        representations.append([value])
    for key in ('returned_source_paths', 'explicit_returned_source_paths'):
        if key in caller:
            value = caller[key]
            assert isinstance(value, list) and all(isinstance(p, str) for p in value), 'Unsealable returned-source list'
            representations.append(value)
    for key in ('result_metadata', 'tool_return_metadata', 'returned_metadata', 'returned_result_metadata'):
        if key not in caller:
            continue
        metadata = caller[key]
        assert isinstance(metadata, dict), 'Unsealable native return metadata'
        if 'output_hint' not in metadata:
            continue
        hint = metadata['output_hint']
        assert isinstance(hint, str) and hint.splitlines(), 'Unsealable native return hint'
        match = re.fullmatch(r'Generated images are saved to (/[^\r\n]+) as (/[^\r\n]+) by default\.', hint.splitlines()[0])
        assert match, 'Unrecognized native return-hint grammar; caller remains unsealable'
        directory, path = match.groups()
        assert str(Path(path).parent) == directory, 'Native return directory/path mismatch'
        representations.append([path])
    assert representations and all(len(paths) == 1 for paths in representations), 'Exactly one explicit returned source is required'
    path = representations[0][0]
    assert Path(path).is_absolute() and Path(path).suffix == '.png' and '..' not in Path(path).parts
    assert all(paths == [path] for paths in representations), 'Ambiguous/conflicting returned-source identifiers'
    return path

def review_state(readiness, local, case, wave):
    roles = [r['role_id'] for r in case['roles']]
    assert readiness['wave'] == wave and set(readiness['cases']) == {case['case_id']}
    assert readiness['planned_roles'] == roles and readiness['planned_role_count'] == readiness['closed_role_count'] == 5
    assert readiness['planned_case_count'] == 1 and readiness['all_makers_closed'] is True
    state = readiness['cases'][case['case_id']]
    assert local == state, 'Global/per-case readiness state differs'
    assert state['expected_count'] == 5 and state['roles'] == roles
    assert [i['image_id'] for i in state['images']] == roles and [i['role'] for i in state['images']] == roles
    assert state['status'] in ('READY', 'UNREADY') and isinstance(state['errors'], list)
    if state['status'] == 'READY':
        assert not state['errors'] and all(i['ready'] is True for i in state['images'])
        assert state['mode'] in ('THREE_FRESH_COMPLETE_CRITICS', 'COMPLETE_FIRST_THREE_REUSED')
        assert wave == 'selected' or state['mode'] == 'THREE_FRESH_COMPLETE_CRITICS'
    else:
        assert state['errors'], 'An unready phase must retain its actual reasons'
    return state

def maker_provenance(directory, rid, terminal_path):
    launch = read(directory/'launch.json'); completion = read(directory/'completion.json')
    assert all(completion[k] == v for k,v in launch.items())
    assert completion['exit_code'] == 0 and completion['fresh_session'] is True and completion['input_pins_unchanged'] is True
    assert launch['profile'] == rid and '--ephemeral' in launch['argv'] and 'exec' in launch['argv']
    assert not any(x in launch['argv'] for x in ('resume','fork'))
    for row in launch['input_pins'] + [launch['job'],launch['prompt'],completion['trace']]:
        checked(row)
    checked(completion['reports'][terminal_path.name])
    assert Path(completion['reports'][terminal_path.name]['path']).resolve() == terminal_path.resolve()
    events = [json.loads(line) for line in Path(completion['trace']['path']).read_text().splitlines() if line.strip()]
    sessions = [e['thread_id'] for e in events if e.get('type') == 'thread.started']
    assert len(sessions) == 1 and completion['session_ids'] == sessions
    turns = sum(e.get('type') == 'turn.completed' for e in events)
    assert turns >= 1 and completion['turn_completed_count'] == turns
    assert not any(e.get('type') == 'turn.failed' for e in events)
    errors = [e for e in events if e.get('type') == 'error']
    # These recorded transport reconnects recovered inside this same successful
    # maker session. They are retained, not counted as native-image failures.
    reconnect = r'Reconnecting\.\.\. [1-5]/5 \(stream disconnected before completion: websocket closed by server before response\.completed\)'
    assert all(re.fullmatch(reconnect,e.get('message','')) for e in errors), 'Unclassified runner error'
    return completion, sessions[0]

def seal():
    freeze = read(ROOT/'planning/candidate-i-pre-generation-freeze.json')
    for row in freeze['runtime_files'] + freeze['helpers'] + freeze['references']:
        checked(row)
    for key in ('case', 'central_plan', 'ratio'):
        checked(freeze[key])
    corpus = read(freeze['case']['path'])
    assert len(corpus['cases']) == 1 and corpus['cases'][0]['count'] == 5
    case = corpus['cases'][0]
    makers, calls, sessions, cache_rows, validated_roles = [], [], [], [], {}
    assert [r['role_id'] for r in case['roles']] == [case['case_id']+'-M'+str(i) for i in range(1,6)]
    for role in case['roles']:
        rid = role['role_id']; directory = ROOT/'production'/rid
        assert directory.resolve().is_relative_to(ROOT/'production') and not directory.is_symlink()
        validated = validate_terminal(ROOT/'production', role, case['case_id'])
        assert validated['closed'] is True and not validated['errors'], validated['errors']
        validated_roles[rid] = validated
        terminal_paths = [p for p in (directory/'selection.json', directory/'unavailable.json') if p.is_file()]
        assert len(terminal_paths) == 1
        completion, session = maker_provenance(directory, rid, terminal_paths[0]); sessions.append(session)
        terminal = read(terminal_paths[0])
        assert terminal['role'] == rid and 1 <= len(validated['stages']) <= 3
        expected_callers = {str((directory/'stages'/s['stage']/'native-call.json').resolve()) for s in validated['stages']}
        assert {str(p.resolve()) for p in directory.rglob('native-call.json')} == expected_callers
        expected_sources = {}
        for stage in validated['stages']:
            stage_dir = directory/'stages'/stage['stage']
            assert stage_dir.resolve().is_relative_to(directory.resolve()) and not stage_dir.is_symlink()
            caller = read(stage_dir/'native-call.json')
            assert caller['role'] == rid and caller['stage'] == stage['stage']
            assert caller['outcome'] == stage['outcome']
            calls.append({'role': rid, 'stage': stage['stage'], 'caller': pin(stage_dir/'native-call.json'), 'raw': caller})
            if caller['outcome'] == 'returned':
                manifest = read(stage_dir/'manifest.json')
                source = manifest['source']; checked(source)
                assert returned_source(caller) == source['path'], 'Caller returned source differs from exact manifest source'
                assert checked(manifest['files']['original'])['sha256'] == source['sha256']
                expected_sources[str(Path(source['path']).resolve())] = source['sha256']
        cache = Path('/Users/nahyeonbin/.codex/generated_images')/session
        actual_sources = {str(p.resolve()): pin(p)['sha256'] for p in cache.glob('*.png')}
        assert expected_sources == actual_sources, rid + ': complete returned-source coverage mismatch'
        cache_rows.append({'role': rid, 'session': session, 'matches': True, 'sources': expected_sources})
        runner_events = [json.loads(line) for line in Path(completion['trace']['path']).read_text().splitlines() if line.strip()]
        makers.append({'case_id': case['case_id'], 'role': rid, 'terminal': pin(terminal_paths[0]), 'completion': pin(directory/'completion.json'), 'counts': terminal['counts'], 'selected_stage': terminal.get('selected_stage'), 'recovered_transport_events':[e for e in runner_events if e.get('type')=='error']})
    assert len(sessions) == len(set(sessions)) == 5 and len(calls) <= 15
    stages, critic_sessions = {}, []
    actual_counts = {'records': 0, 'score_slots': 0, 'valid_scores': 0}
    for wave in ('initial', 'selected'):
        readiness = read(ROOT/'reviews'/(wave+'-stage-readiness.json'))
        assert readiness['corpus'] == pin(freeze['case']['path'])
        assert readiness['maker_inventory'] == validated_roles
        directory = ROOT/'reviews'/case['case_id']/wave
        state = review_state(readiness, read(directory/'readiness.json'), case, wave)
        if state['status'] != 'READY':
            item = {'gate':'NA','readiness':pin(directory/'readiness.json'),'reason':state['errors']}
            gates = {r['role_id']:'NA' for r in case['roles']}
            stages[wave] = {'cases':{case['case_id']:item},'image_gates':gates,'image_gate_counts':{'PASS':0,'FAIL':0,'NA':5},'whole_corpus_gate':'NA'}
            continue
        reused = state.get('mode') == 'COMPLETE_FIRST_THREE_REUSED'
        summary_path = ROOT/'reviews'/case['case_id']/'initial'/'summary.json' if reused else directory/'summary.json'
        summary = read(summary_path); asset_path = summary_path.parent/'source-asset-audit.json'; asset = read(asset_path)
        actual_wave = 'initial' if reused else wave
        assert summary['case_id'] == asset['case_id'] == case['case_id'] and summary['wave'] == asset['wave'] == actual_wave
        assert summary['packet'] == pin(summary_path.parent/'packet.json')
        assert checked(state['packet']) == pin(directory/'packet.json')
        assert set(summary['image_gates']) == {r['role_id'] for r in case['roles']}
        assert asset['case_id'] == case['case_id'] and asset['gate'] in ('PASS','FAIL','NA')
        assert asset['packet'] == {k:v for k,v in summary['packet'].items() if k in ('path','sha256')}
        effective = summary['set_gate'] if asset['gate'] == 'PASS' else 'NA'
        effective_images = summary['image_gates'] if asset['gate'] == 'PASS' else {r['role_id']:'NA' for r in case['roles']}
        item = {'gate': effective, 'original_v4_set_gate': summary['set_gate'], 'original_v4_image_gates': summary['image_gates'], 'source_attestation_gate': asset['gate'], 'source_attestation_audit': pin(asset_path), 'summary': pin(summary_path), 'reused_complete_initial_three': reused}
        if reused:
            check_reuse(read(summary_path.parent/'packet.json'), read(directory/'packet.json'), summary, read(directory/'reuse.json'), pin(summary_path.parent/'packet.json'), pin(summary_path), checked)
            item['reuse'] = pin(directory/'reuse.json')
        else:
            for profile in PROFILES:
                completion = read(directory/'cli'/profile/'completion.json')
                assert completion['exit_code'] == 0 and completion['input_pins_unchanged'] is True and len(completion['session_ids']) == 1
                critic_sessions += completion['session_ids']
            counts = summary['counts']
            actual_counts['records'] += counts['observed_image_profile_records']
            actual_counts['score_slots'] += counts['observed_score_slots']
            actual_counts['valid_scores'] += counts['valid_integer_1_to_5_score_values']
        stages[wave] = {'cases': {case['case_id']: item}, 'image_gates': effective_images, 'image_gate_counts': {s:sum(g==s for g in effective_images.values()) for s in ('PASS','FAIL','NA')}, 'whole_corpus_gate': effective}
    assert len(critic_sessions) == len(set(critic_sessions)) <= 6
    assert not set(critic_sessions).intersection(sessions)
    return {'schema_version': 1, 'closed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate': 'I', 'corpus': pin(freeze['case']['path']), 'pre_generation_freeze': pin(ROOT/'planning/candidate-i-pre-generation-freeze.json'), 'poster_role_denominator': 5, 'cases': 1, 'poster_calls_closed': True, 'poster_native_attempts': len(calls), 'poster_attempt_cap': 15, 'makers': makers, 'caller_records': calls, 'native_source_cache_checks': cache_rows, 'stages': stages, 'actual_unique_review_sessions': len(critic_sessions), 'actual_review_counts': actual_counts, 'limits': ['One development request; not held-out certification or a guarantee for unseen requests.', 'Runtime and focused-input harness both differ from H; no isolated causal claim.', 'Fresh maker/critic sessions are trace-backed; semantic viewing remains an attestation.', 'No client assets; preservation and one-image editing remain untested by this case.']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--preflight-only', action='store_true'); args = parser.parse_args()
    result = seal()
    if not args.preflight_only:
        with (ROOT/'planning/final-evidence.json').open('x') as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'CLOSED', 'roles': 5, 'native_attempts': result['poster_native_attempts'], 'actual_unique_review_sessions': result['actual_unique_review_sessions'], 'stages': {k: {'image_gate_counts': v['image_gate_counts'], 'whole_corpus_gate': v['whole_corpus_gate']} for k,v in result['stages'].items()}}))
