"""Root-only closure of one five-poster run; never alters actor inputs or scores."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from prepare_reviews_v2 import terminal as validate_terminal

ROOT = Path(__file__).resolve().parent
PROFILES = ('editorial', 'craft', 'portfolio')

def phase_auditor(wave):
    assert wave in ('initial','selected')
    path = ROOT/'method-recording-v2/audit_compact_bindings.py'
    spec = importlib.util.spec_from_file_location('closed_r14_auditor_'+wave, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

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
    """Read literal caller return fields; never infer a path from artifacts."""
    representations = []

    def hint_path(value):
        assert isinstance(value, str) and value.splitlines(), 'Unsealable native return hint'
        match = re.fullmatch(r'Generated images are saved to (/[^\r\n]+) as (/[^\r\n]+) by default\.', value.splitlines()[0])
        assert match, 'Unrecognized native return-hint grammar; caller remains unsealable'
        directory, path = match.groups()
        assert str(Path(path).parent) == directory, 'Native return directory/path mismatch'
        return path

    def typed_hints(value):
        assert isinstance(value, list), 'Unsealable native return-hint list'
        for hint in value:
            assert isinstance(hint, dict) and isinstance(hint.get('field'), str), 'Unsealable typed native return hint'
            if hint['field'] == 'result.output_hint':
                representations.append([hint_path(hint.get('value'))])

    for key in ('returned_source_path', 'exact_source_path_from_return', 'explicit_returned_source_path'):
        if key in caller:
            value = caller[key]
            assert isinstance(value, str), 'Unsealable returned-source field'
            representations.append([value])
    for key in ('returned_source_paths', 'explicit_returned_source_paths', 'explicit_returned_png_paths'):
        if key in caller:
            value = caller[key]
            assert isinstance(value, list) and all(isinstance(p, str) for p in value), 'Unsealable returned-source list'
            representations.append(value)
    for key in ('result_metadata', 'tool_return_metadata', 'tool_result_metadata', 'returned_metadata', 'returned_result_metadata', 'result_hints'):
        if key not in caller:
            continue
        metadata = caller[key]
        assert isinstance(metadata, dict), 'Unsealable native return metadata'
        if 'output_hint' in metadata:
            representations.append([hint_path(metadata['output_hint'])])
        if 'hints' in metadata:
            typed_hints(metadata['hints'])
    if 'returned_result_hints' in caller:
        value = caller['returned_result_hints']
        if isinstance(value, dict):
            # Actual caller metadata container; keep the same literal grammar.
            assert 'output_hint' in value, 'Missing literal native return hint'
            representations.append([hint_path(value['output_hint'])])
            if 'hints' in value:
                typed_hints(value['hints'])
        else:
            typed_hints(value)
    assert representations and all(len(paths) == 1 for paths in representations), 'Exactly one explicit returned source is required'
    path = representations[0][0]
    assert Path(path).is_absolute() and Path(path).suffix == '.png' and '..' not in Path(path).parts
    assert str(Path(path)) == path and not any(c in path for c in ('\x00', '\r', '\n')), 'Nonliteral returned-source path'
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
    freeze = read(ROOT/'planning/candidate-n-pre-generation-freeze.json')
    for row in freeze['runtime_files'] + freeze['helpers'] + freeze['references']:
        checked(row)
    for key in ('case', 'central_plan', 'ratio'):
        checked(freeze[key])
    recording_freeze_path = ROOT/'planning/critic-recording-helper-freeze.json'
    recording_freeze = read(recording_freeze_path)
    assert recording_freeze['actual_critic_sessions_at_freeze'] == recording_freeze['live_critic_jobs_at_freeze'] == 0
    assert checked(recording_freeze['production_and_quality_freeze']) == pin(ROOT/'planning/candidate-n-pre-generation-freeze.json')
    for row in recording_freeze['files']:
        checked(row)
    assert recording_freeze['actual_native_calls_at_freeze'] == 0
    assert recording_freeze['quality_gates_unchanged'] and recording_freeze['overall_critic_cap'] == 6
    production_closure_path = ROOT/'planning/single-five-production-closure.json'
    production_closure = read(production_closure_path)
    assert production_closure['all5_before_critics'] is True
    critic_start = production_closure['critic_start_proof']
    assert critic_start['production_closure_before_review_preparation'] is True and critic_start['reviews_directory_existed'] is False
    assert critic_start['actual_critic_sessions_observed'] == critic_start['critic_launch_trace_completion_or_report_files'] == critic_start['critic_runner_output_directories'] == 0
    assert not critic_start['live_critic_or_runner_processes']
    for row in critic_start['prepared_files']:
        checked(row)
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
    assert production_closure['native_attempts'] == len(calls) and production_closure['native_attempt_cap'] == 15
    assert {r['session'] for r in production_closure['roles']} == set(sessions)
    for role in production_closure['roles']:
        checked(role['completion']); checked(role['terminal'])
    stages, critic_sessions = {}, []
    actual_counts = {'records': 0, 'score_slots': 0, 'valid_scores': 0}
    raw_counts = {'records': 0, 'score_slots': 0, 'valid_scores': 0}
    raw_inventory = []
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
        compact_path = directory/'compact-recording-audit.json'
        compact = read(compact_path)
        auditor = phase_auditor(wave)
        recomputed = (auditor.audit_reuse(directory/'packet.json', directory/'reuse.json') if reused
                      else auditor.audit(directory/'packet.json', directory/'cli'))
        assert compact == recomputed, 'Stored compact binding audit differs from actual raw/export/completion proof'
        assert compact['gate'] in ('PASS', 'NA')
        supplemental_pass = asset['gate'] == compact['gate'] == 'PASS'
        effective = summary['set_gate'] if supplemental_pass else 'NA'
        effective_images = summary['image_gates'] if supplemental_pass else {r['role_id']:'NA' for r in case['roles']}
        item = {'gate': effective, 'original_v4_set_gate': summary['set_gate'], 'original_v4_image_gates': summary['image_gates'], 'source_attestation_gate': asset['gate'], 'source_attestation_audit': pin(asset_path), 'compact_recording_gate': compact['gate'], 'compact_recording_audit': pin(compact_path), 'summary': pin(summary_path), 'reused_complete_initial_three': reused}
        if reused:
            assert compact['gate'] == 'PASS', 'Invalid initial compact evidence cannot authorize reuse'
            item['reuse'] = pin(directory/'reuse.json')
        else:
            for profile in PROFILES:
                completion = read(directory/'cli'/profile/'completion.json')
                assert completion['exit_code'] == 0 and completion['input_pins_unchanged'] is True and len(completion['session_ids']) == 1
                assert completion['started_utc'] > recording_freeze['utc']
                assert completion['started_utc'] > production_closure['closed_utc'], 'Critic started before completed ROOT production provenance closure'
                critic_sessions += completion['session_ids']
                raw_path = directory/'cli'/profile/(profile+'.observations.json')
                checked(completion['reports'][raw_path.name])
                raw = read(raw_path)
                assert raw['case_id'] == case['case_id'] and raw['wave'] == wave and raw['profile'] == profile
                assert set(raw['images']) == set(summary['image_gates'])
                counts = {'records':len(raw['images']), 'score_slots':0, 'valid_scores':0}
                for image in raw['images'].values():
                    for rating in image['ratings'].values():
                        score = rating.get('score')
                        counts['score_slots'] += 1
                        counts['valid_scores'] += type(score) is int and 1 <= score <= 5
                for key in raw_counts:
                    raw_counts[key] += counts[key]
                raw_inventory.append({'wave':wave, 'profile':profile, 'raw_observations':pin(raw_path), 'completion':pin(directory/'cli'/profile/'completion.json'), 'counts':counts})
            counts = summary['counts']
            actual_counts['records'] += counts['observed_image_profile_records']
            actual_counts['score_slots'] += counts['observed_score_slots']
            actual_counts['valid_scores'] += counts['valid_integer_1_to_5_score_values']
        stages[wave] = {'cases': {case['case_id']: item}, 'image_gates': effective_images, 'image_gate_counts': {s:sum(g==s for g in effective_images.values()) for s in ('PASS','FAIL','NA')}, 'whole_corpus_gate': effective}
    assert len(critic_sessions) == len(set(critic_sessions)) <= 6
    assert not set(critic_sessions).intersection(sessions)
    return {'schema_version': 1, 'closed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate': 'N', 'corpus': pin(freeze['case']['path']), 'pre_generation_freeze': pin(ROOT/'planning/candidate-n-pre-generation-freeze.json'), 'critic_recording_freeze': pin(recording_freeze_path), 'production_provenance_closure': pin(production_closure_path), 'poster_role_denominator': 5, 'cases': 1, 'poster_calls_closed': True, 'poster_native_attempts': len(calls), 'poster_attempt_cap': 15, 'makers': makers, 'caller_records': calls, 'native_source_cache_checks': cache_rows, 'stages': stages, 'actual_unique_review_sessions': len(critic_sessions), 'actual_review_counts': actual_counts, 'raw_observation_counts_separate':raw_counts, 'raw_observation_inventory':raw_inventory, 'limits': ['Exactly one known architecture exhibition16:9 request with the prospectively added human whole-template exclusion after full R13 closure; not unseen transfer or a20-image campaign.', 'N runtime guidance, reference choice and planning differ together; no isolated causal/statistical or future universal quality claim.', 'Same compact recording v2, raw schema1, v4 gates, normalization and bounded1+2 calls remain unchanged. Low, NULL and NA records are retained.', 'Fresh actors are trace-backed; semantic viewing remains an attestation. Native source joins caller-literal returns, persistence commands, sessions, cache, manifests and hashes; ephemeral traces expose no direct native MCP invocation/return events.', 'All five makers and successful ROOT production closure precede initial quality packet preparation/critic starts. No quality feedback is used to regenerate or reselect.', 'Both phases use predeclared anonymous-single-five; case/path identifiers remain visible. ROOT knows case/plans and is not a blind scored critic.', 'N developmental advisories do not replace original scored critics. Whole-style advisory used byte-identical final.png aliases; its actual input access limitation remains in untouched records.', 'No supplied client assets; preservation and one-image follow-up edits remain untested.']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--preflight-only', action='store_true'); args = parser.parse_args()
    result = seal()
    if not args.preflight_only:
        with (ROOT/'planning/final-evidence.json').open('x') as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'CLOSED', 'roles': 5, 'native_attempts': result['poster_native_attempts'], 'actual_unique_review_sessions': result['actual_unique_review_sessions'], 'stages': {k: {'image_gate_counts': v['image_gate_counts'], 'whole_corpus_gate': v['whole_corpus_gate']} for k,v in result['stages'].items()}}))
