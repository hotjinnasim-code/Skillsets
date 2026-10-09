"""Close actual H evidence without rejudging raw reviews or hiding missing roles."""
import argparse, datetime, hashlib, json, re
from pathlib import Path
from reuse_binding import check_reuse
from prepare_reviews_v2 import terminal as validate_terminal

ROOT = Path(__file__).resolve().parent
PROFILES = ('editorial', 'craft', 'portfolio')
STATES = ('PASS', 'FAIL', 'NA')

def read(p):
    return json.loads(Path(p).read_bytes())

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
    for key in ('returned_source_path','exact_source_path_from_return'):
        if key in caller:
            value = caller[key]
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
    for hint in caller.get('returned_result_hints', []):
        if isinstance(hint,dict) and hint.get('field') == 'result.output_hint':
            value = hint.get('value')
            assert isinstance(value,str) and value.splitlines()
            match = re.fullmatch(r'Generated images are saved to (/[^\r\n]+) as (/[^\r\n]+) by default\.',value.splitlines()[0])
            assert match, 'Unrecognized explicit tool return hint'
            directory,path = match.groups()
            assert str(Path(path).parent) == directory
            representations.append([path])
    assert representations and all(len(paths) == 1 for paths in representations), 'Exactly one explicit returned source is required'
    path = representations[0][0]
    assert Path(path).is_absolute() and Path(path).suffix == '.png' and '..' not in Path(path).parts
    assert all(paths == [path] for paths in representations), 'Ambiguous/conflicting returned-source identifiers'
    return path

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

def gate(values):
    return 'NA' if 'NA' in values else 'FAIL' if 'FAIL' in values else 'PASS'

def seal():
    corpus_path = ROOT/'planning/corpus20.json'; corpus = read(corpus_path)
    assert sum(c['count'] for c in corpus['cases']) == 20
    for document, key in [('preproduction-input-freeze.json', 'files'), ('final-preparer-freeze.json', 'inputs')]:
        for row in read(ROOT/'planning'/document)[key]:
            assert pin(row['path'])['sha256'] == row['sha256'], 'Frozen source changed'
    for row in read(ROOT/'planning/source-asset-audit-freeze.json')['files']:
        assert pin(row['path'])['sha256'] == row['sha256'], 'Supplementary source checker changed'
    assert read(ROOT/'planning/review-preparer-schema-repair.json')['before_any_critic_or_review_packet'] is True
    assert pin(ROOT/'prepare_reviews_v2.py')['sha256'] == '6fcb2f3e792c174f65c38684b0447b5a137f5de72f01df3cf0bd029968996771', 'Actual schema-corrected preparer changed'
    inventory_path = ROOT/'planning/native-source-inventory.json'
    inventory = read(inventory_path)
    assert inventory['status'] == 'PASS' and inventory['audited_roles'] == 20 and not inventory['open_roles'] and not inventory['errors'], 'Complete native cache coverage required'
    inventory_rows = {row['role']:row for row in inventory['records']}
    assert len(inventory_rows) == 20
    makers, calls, sessions, validated_roles = [], [], [], {}
    for case in corpus['cases']:
        for role in case['roles']:
            d = ROOT/'production'/role['role_id']; comp = read(d/'completion.json')
            assert comp['exit_code'] == 0 and comp['input_pins_unchanged'] is True
            assert len(comp['session_ids']) == 1
            inv = inventory_rows[role['role_id']]
            assert inv['completion_path'] == str((d/'completion.json').resolve()) and inv['completion_sha256'] == pin(d/'completion.json')['sha256'] and inv['session'] == comp['session_ids'][0] and inv['matches'] is True
            sessions += comp['session_ids']
            choices = [p for p in (d/'selection.json', d/'unavailable.json') if p.is_file()]
            assert len(choices) == 1
            validated = validate_terminal(ROOT/'production',role,case['case_id'])
            assert validated['closed'] is True and not validated['errors'], validated['errors']
            validated_roles[role['role_id']] = validated
            _, actual_session = maker_provenance(d,role['role_id'],choices[0])
            assert actual_session == comp['session_ids'][0]
            terminal = read(choices[0]); stages = terminal['stages']
            assert {str(p.resolve()) for p in d.rglob('native-call.json')} == {str((d/'stages'/st['stage']/'native-call.json').resolve()) for st in stages}
            assert terminal['role'] == role['role_id'] and 1 <= len(stages) <= 3
            assert terminal['counts']['native_calls'] == len(stages)
            for stage in stages:
                sd = d/'stages'/stage['stage']; call = read(sd/'native-call.json')
                assert call['role'] == role['role_id'] and call['stage'] == stage['stage']
                assert call['outcome'] == stage['outcome'] and call['outcome'] in ('returned','failure')
                if call['outcome'] == 'returned':
                    manifest = read(sd/'manifest.json'); checked(manifest['source'])
                    assert returned_source(call) == manifest['source']['path']
                calls.append({'role': role['role_id'], 'stage': stage['stage'], 'caller': pin(sd/'native-call.json'), 'raw': call})
            makers.append({'case_id': case['case_id'], 'role': role['role_id'], 'terminal': pin(choices[0]), 'completion': pin(d/'completion.json'), 'counts': terminal['counts'], 'selected_stage': terminal.get('selected_stage')})
    assert len(set(sessions)) == 20 and len(calls) <= 60
    stages, unique_review_sessions, unique_counts = {}, [], {'records': 0, 'score_slots': 0, 'valid_scores': 0}
    for wave in ('initial', 'selected'):
        readiness = read(ROOT/'reviews'/(wave+'-stage-readiness.json'))
        assert readiness['all_makers_closed'] is True and readiness['planned_role_count'] == readiness['closed_role_count'] == 20
        assert readiness['wave'] == wave and set(readiness['cases']) == {c['case_id'] for c in corpus['cases']}
        assert readiness['maker_inventory'] == validated_roles and readiness['corpus'] == pin(corpus_path)
        phase = {'cases': {}, 'image_gates': {}, 'projected_records': 0, 'projected_valid_scores': 0}
        for case in corpus['cases']:
            cid = case['case_id']; state = readiness['cases'][cid]; d = ROOT/'reviews'/cid/wave
            assert read(d/'readiness.json') == state
            assert state['expected_count'] == case['count'] and state['roles'] == [r['role_id'] for r in case['roles']]
            assert state['status'] in ('READY','UNREADY') and isinstance(state['errors'],list)
            assert state['errors'] if state['status']=='UNREADY' else not state['errors']
            if state['status'] != 'READY':
                phase['cases'][cid] = {'gate': 'NA', 'readiness': pin(d/'readiness.json'), 'reason': state['errors']}
                phase['image_gates'].update({r['role_id']: 'NA' for r in case['roles']})
                continue
            reused = state.get('mode') == 'COMPLETE_FIRST_THREE_REUSED'
            summary_path = ROOT/'reviews'/cid/'initial'/'summary.json' if reused else d/'summary.json'
            data = read(summary_path)
            assert data['wave'] == ('initial' if reused else wave)
            assert data['case_id'] == cid and set(data['image_gates']) == {r['role_id'] for r in case['roles']}
            asset_audit_path = summary_path.parent/'source-asset-audit.json'
            asset_audit = read(asset_audit_path)
            assert asset_audit['case_id'] == cid and asset_audit['packet'] == {k:v for k,v in data['packet'].items() if k in ('path','sha256')}
            phase['image_gates'].update(data['image_gates'] if asset_audit['gate']=='PASS' else {r['role_id']:'NA' for r in case['roles']})
            counts = data['counts']; phase['projected_records'] += counts['observed_image_profile_records']; phase['projected_valid_scores'] += counts['valid_integer_1_to_5_score_values']
            phase['cases'][cid] = {'gate': data['set_gate'] if asset_audit['gate']=='PASS' else 'NA', 'original_v4_set_gate':data['set_gate'], 'original_v4_image_gates':data['image_gates'], 'source_attestation_gate':asset_audit['gate'], 'source_attestation_audit':pin(asset_audit_path), 'summary': pin(summary_path), 'reused_complete_initial_three': reused}
            if reused:
                def exact_pin(row):
                    actual = pin(row['path']); assert actual['sha256'] == row['sha256']; return actual
                check_reuse(read(summary_path.parent/'packet.json'), read(d/'packet.json'), data, read(d/'reuse.json'), pin(summary_path.parent/'packet.json'), pin(summary_path), exact_pin)
                phase['cases'][cid]['reuse'] = pin(d/'reuse.json')
                continue
            for profile in PROFILES:
                comp = read(d/'cli'/profile/'completion.json')
                assert comp['exit_code']==0 and comp['input_pins_unchanged'] is True and len(comp['session_ids']) == 1
                unique_review_sessions += comp['session_ids']
            unique_counts['records'] += counts['observed_image_profile_records']
            unique_counts['score_slots'] += counts['observed_score_slots']
            unique_counts['valid_scores'] += counts['valid_integer_1_to_5_score_values']
        assert len(phase['image_gates']) == 20
        phase['image_gate_counts'] = {s: sum(v == s for v in phase['image_gates'].values()) for s in STATES}
        phase['whole_corpus_gate'] = gate([v['gate'] for v in phase['cases'].values()])
        stages[wave] = phase
    assert len(unique_review_sessions) == len(set(unique_review_sessions)) <= 42
    assert not set(unique_review_sessions).intersection(sessions)
    return {'schema_version': 1, 'closed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate': 'H', 'corpus': pin(corpus_path), 'review_preparer_schema_repair': pin(ROOT/'planning/review-preparer-schema-repair.json'), 'native_source_inventory':pin(inventory_path), 'poster_role_denominator': 20, 'cases': 7, 'poster_calls_closed': True, 'poster_native_attempts': len(calls), 'poster_attempt_cap': 60, 'fixture_native_attempts_separate': 3, 'makers': makers, 'caller_records': calls, 'stages': stages, 'actual_unique_review_sessions': len(unique_review_sessions), 'actual_review_counts': unique_counts, 'instrumentation_scope_finding': pin(ROOT/'planning/instrumentation-scope-finding.md'), 'limits': ['All seven aesthetics and mandatory gates unchanged; no averaging or critic replacement.', 'Projected selected-stage records may reuse complete initial reviews; actual unique reviews are counted separately.', 'Semantic image viewing is attested by critics; CLI traces do not serialize all native viewing events.', 'Instrumented H maker instructions require a full literal user-request prefix in every native call, beyond the runtime skill; these are not unmodified ordinary-use prompt-construction results.', 'H tests used for the next skill revision become its development evidence, not its held-out certification.', 'Finite test results do not guarantee every future image.']}

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--preflight-only', action='store_true'); a = p.parse_args()
    result = seal()
    if not a.preflight_only:
        with (ROOT/'planning/final-evidence.json').open('x') as f: json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({'status': 'CLOSED', 'roles': 20, 'native_attempts': result['poster_native_attempts'], 'actual_unique_review_sessions': result['actual_unique_review_sessions'], 'stages': {k: {'image_gate_counts': v['image_gate_counts'], 'whole_corpus_gate': v['whole_corpus_gate']} for k, v in result['stages'].items()}}))
