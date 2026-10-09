"""ROOT-only R11 archive replay, exact inventory, containment and link checks.

Never launches actors/native calls or changes observations, scores or gates.
Preflight uses synthetic fixtures only; actual replay requires whole closure.
"""
import argparse
import builtins
import hashlib
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import types
from contextlib import contextmanager
from html.parser import HTMLParser
from pathlib import Path

GUARDED = ((builtins, ('open',)), (io, ('open',)),
           (os, ('open', 'stat', 'lstat', 'readlink', 'scandir', 'listdir', 'access')))


def load_module(path):
    spec = importlib.util.spec_from_file_location('r11_root_archive_verifier', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def bootstrap_archive(root):
    """Check every root/helper prefix before importing archived code."""
    assert str(root) and '..' not in root.parts
    root = Path(os.path.abspath(root))
    helper = root/'raw/verify_archive.py'
    for candidate in (root, helper):
        prefix = Path(candidate.anchor)
        for part in candidate.parts[1:]:
            prefix = prefix/part
            if prefix.is_symlink():
                raise ValueError('Archive bootstrap symlink forbidden: '+str(prefix))
    assert root.is_dir() and helper.is_file()
    return root, helper


@contextmanager
def access_guard(allow):
    installed = []
    def install(owner, name):
        original = getattr(owner, name)
        def guarded(path, *args, **kwargs):
            if isinstance(path, (str, bytes, Path)):
                allow(Path(os.path.abspath(os.fsdecode(path))), name)
            return original(path, *args, **kwargs)
        setattr(owner, name, guarded)
        installed.append((owner, name, original))
    for owner, names in GUARDED:
        for name in names:
            install(owner, name)
    try:
        yield
    finally:
        for owner, name, original in reversed(installed):
            setattr(owner, name, original)


def containment_fixtures(verifier):
    attempts = []
    rejected = []
    with tempfile.TemporaryDirectory(prefix='r11-archive-containment-') as temp:
        fixture = Path(temp).resolve(strict=True)
        archive = fixture/'archive'; archive.mkdir()
        external = fixture/'outside'; external.mkdir()
        sentinel = external/'sentinel'; sentinel.write_text('synthetic external sentinel')
        (archive/'escape').symlink_to(external, target_is_directory=True)
        (archive/'file-escape').symlink_to(sentinel)
        (fixture/'root-escape').symlink_to(external, target_is_directory=True)
        (fixture/'root-prefix').symlink_to(fixture, target_is_directory=True)
        index = archive/'archive-index.json'
        def allowed(path, operation):
            if path.is_relative_to(external):
                attempts.append({'operation': operation, 'path': str(path)})
                raise AssertionError('External fixture metadata/read consulted')
        def reject(call, label, match=None):
            with access_guard(allowed):
                try:
                    call()
                except ValueError as exc:
                    if match is not None:
                        assert match in str(exc), str(exc)
                else:
                    raise AssertionError('Unsafe path accepted: '+label)
                assert not attempts
            rejected.append(label)
        for path in (external/'sentinel', archive/'..'/'outside'/'sentinel',
                     '../original-host-path', '', 'relative-without-base'):
            reject(lambda p=path: verifier.archive_path(p, archive), 'outside:'+str(path))
        for path in (archive/'escape', archive/'escape'/'sentinel', archive/'file-escape'):
            reject(lambda p=path: verifier.archive_path(p, archive), 'prefix:'+str(path), 'symlink')
        for relative in ('escape/sentinel', 'file-escape'):
            index.write_text(json.dumps({'files': [{'archive_relative': relative,
                                                    'source_absolute': '/explicit/index-fixture',
                                                    'sha256': '0'*64}]}))
            reject(lambda: verifier.verify(archive), 'indexed:'+relative, 'symlink')
        index.unlink(); index.symlink_to(sentinel)
        reject(lambda: verifier.verify(archive), 'real-index-symlink', 'symlink')
        for root in (fixture/'root-escape', fixture/'root-prefix'/'archive'):
            reject(lambda p=root: verifier.verify(p), 'root-prefix:'+str(root), 'symlink')
    return {'rejected_synthetic_paths': rejected,
            'external_fixture_metadata_and_read_attempts': attempts}


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.images = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.images += tag == 'img'
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


def check_links(root, index, verifier, pending_output=None):
    mapping = {row['source_absolute']: verifier.archive_path(root/row['archive_relative'], root)
               for row in index['files']}
    source_root = index['source_root']
    gallery = mapping[source_root+'/gallery.html']
    parser = Links(); parser.feed(gallery.read_text())
    assert parser.images == 5 and len(parser.links) == 20
    def target(base, link):
        value = Path(link)
        assert not value.is_absolute() and '..' not in value.parts, link
        candidate = base/value
        if pending_output is not None and candidate == pending_output:
            return
        actual = verifier.archive_path(candidate, root)
        assert actual.is_file(), link
    for link in parser.links:
        target(gallery.parent, link)
    report = mapping[source_root+'/report.md']
    report_links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', report.read_text())
    for link in report_links:
        target(report.parent, link)
    wrapper_links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', (root/'report.md').read_text())
    for link in wrapper_links:
        target(root, link)
    return {'gallery_images': parser.images, 'gallery_local_links': len(parser.links),
            'closed_report_local_links': len(report_links),
            'wrapper_report_local_links': len(wrapper_links), 'missing_links': []}


def raw_inventory(root, index):
    source_root = Path(index['source_root'])
    raw = root/'raw'
    declared = {}
    for row in index['files']:
        source = Path(row['source_absolute'])
        if source.is_relative_to(source_root):
            relative = source.relative_to(source_root)
            assert row['archive_relative'] == (Path('raw')/relative).as_posix()
            declared[relative.as_posix()] = row['sha256']
    actual = {}
    for file in raw.rglob('*'):
        assert not file.is_symlink(), str(file)
        if file.is_file():
            assert '__pycache__' not in file.parts and file.suffix != '.pyc'
            actual[file.relative_to(raw).as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
    assert declared == actual, 'Raw source inventory differs from complete mapped tree'
    return {'status': 'PASS', 'complete_raw_source_files': len(actual),
            'indexed_source_identifiers': len(index['files'])}


def check_phase_coverage(final, replay):
    """Require both logical phases, including exact complete-initial reuse."""
    rows = replay['replays']
    assert replay['phases_replayed'] == len(rows) == 2
    by_wave = {row['wave']: row for row in rows}
    assert len(by_wave) == 2 and set(by_wave) == {'initial', 'selected'}
    actual_summaries = set()
    for wave in ('initial', 'selected'):
        stage = final['stages'][wave]
        assert len(stage['cases']) == 1
        cid, item = next(iter(stage['cases'].items()))
        assert 'summary' in item, 'Actual whole-phase evidence required'
        row = by_wave[wave]
        reused = item['reused_complete_initial_three']
        assert not reused or wave == 'selected'
        assert row['case_id'] == cid and row['reused_complete_initial_three'] is reused
        assert row['actual_summary_wave'] == ('initial' if reused else wave)
        assert row['source_attestation_gate'] == item['source_attestation_gate']
        assert row['compact_recording_gate'] == item['compact_recording_gate']
        assert row['effective_set_gate'] == item['gate'] == stage['whole_corpus_gate']
        actual_summaries.add(item['summary']['path'])
    assert replay['unique_summaries_replayed'] == len(actual_summaries)
    return {'logical_phases_replayed': 2,
            'unique_actual_summaries_replayed': len(actual_summaries),
            'selected_reuses_complete_initial_three':
                by_wave['selected']['reused_complete_initial_three']}


def score_matrix_inventory(root, index, verifier):
    """Compare every displayed score to its actual immutable observation."""
    mapping = {row['source_absolute']: verifier.archive_path(root/row['archive_relative'], root)
               for row in index['files']}
    final = index['closed_evidence']
    corpus = json.loads(mapping[final['corpus']['path']].read_bytes())
    case = corpus['cases'][0]
    dims = ('content_form', 'hierarchy', 'typography', 'space',
            'image_material', 'emotion_control', 'ai_slop')
    expected = []
    for wave in ('initial', 'selected'):
        item = final['stages'][wave]['cases'][case['case_id']]
        summary_source = Path(item['summary']['path']).parent
        summary = json.loads(mapping[item['summary']['path']].read_bytes())
        raw = {p: json.loads(mapping[str(summary_source/'cli'/p/(p+'.observations.json'))].read_bytes())
               for p in ('editorial', 'craft', 'portfolio')}
        for role in case['roles']:
            for profile in ('editorial', 'craft', 'portfolio'):
                obs = raw[profile]['images'][role['role_id']]
                scores = {dim: obs['ratings'][dim]['score'] for dim in dims}
                canon = summary['reviews'][profile]['images'].get(role['role_id'], {})
                if 'scores' in canon:
                    assert scores == canon['scores']
                expected.append({'displayed_wave': wave, 'actual_raw_wave': raw[profile]['wave'],
                                 'role': role['role_id'], 'profile': profile, 'scores': scores,
                                 'summary': item['summary'],
                                 'source_kind': 'actual_immutable_raw_observations',
                                 'reused_complete_initial_three': item['reused_complete_initial_three']})
    matrix = json.loads(mapping[index['source_root']+'/raw-score-matrices.json'].read_bytes())
    assert matrix['presentation_records'] == expected
    assert matrix['actual_unique_record_counts'] == final['actual_review_counts']
    return {'status': 'PASS', 'displayed_rows': len(expected),
            'score_dimensions': len(dims),
            'actual_unique_record_counts': matrix['actual_unique_record_counts'],
            'low_null_na_values_preserved': True}


def phase_replay_fixtures(verifier):
    """Exercise phase paths/counting with synthetic metadata and stub auditors.

    This never imports an actor or quality engine. FAIL/NULL observations in
    these fixtures are test values, not an evaluation of a poster or v4.
    """
    results = []
    original_module = verifier.module
    for reused in (False, True):
        with tempfile.TemporaryDirectory(prefix='r11-synthetic-phase-') as temp:
            root = Path(temp).resolve(strict=True)/'archive'; root.mkdir()
            source = '/synthetic-r11-metadata-only/source'
            rows = []
            def put(relative, value):
                data = (json.dumps(value, sort_keys=True)+'\n').encode()
                physical = root/'raw'/relative; physical.parent.mkdir(parents=True, exist_ok=True)
                physical.write_bytes(data)
                pin = {'path': source+'/'+relative,
                       'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
                rows.append({'source_absolute': pin['path'], 'archive_relative': 'raw/'+relative,
                             'sha256': pin['sha256']})
                return pin
            cid = 'SYNTHETIC-R11'
            roles = [cid+'-M'+str(i) for i in range(1, 6)]
            case = {'case_id': cid, 'count': 5, 'roles': [{'role_id': role} for role in roles]}
            corpus = put('planning/single-five-case.json', {'cases': [case]})
            freeze = put('planning/candidate-k-pre-generation-freeze.json', {
                'runtime_files': [], 'helpers': [], 'references': [], 'case': corpus,
                'central_plan': put('planning/synthetic-plan.json', {}),
                'ratio': put('planning/synthetic-ratio.json', {})})
            recording = put('planning/critic-recording-helper-freeze.json', {
                'actual_critic_sessions_at_freeze': 0, 'live_critic_jobs_at_freeze': 0,
                'production_and_quality_freeze': freeze, 'files': [],
                'actual_native_calls_at_freeze': 0, 'quality_gates_unchanged': True,
                'overall_critic_cap': 6})
            makers = []
            for role in roles:
                terminal = put('production/'+role+'/selection.json', {
                    'role': role, 'selected_stage': 'initial', 'counts': {'native_calls': 1}})
                completion = put('production/'+role+'/completion.json', {
                    'exit_code': 0, 'input_pins_unchanged': True, 'session_ids': ['maker-'+role],
                    'reports': {'selection.json': terminal},
                    'trace': put('production/'+role+'/synthetic-trace.json', {})})
                makers.append({'role': role, 'terminal': terminal, 'completion': completion,
                               'selected_stage': 'initial', 'counts': {'native_calls': 1}})
            dims = ('content_form', 'hierarchy', 'typography', 'space',
                    'image_material', 'emotion_control', 'ai_slop')
            scores = {dim: (None if dim == 'content_form' else 2) for dim in dims}
            summaries, assets, raw_inventory, raw_records = {}, {}, [], {}
            counts = {'observed_image_profile_records': 15, 'observed_score_slots': 105,
                      'valid_integer_1_to_5_score_values': 90}
            image_gates = dict.fromkeys(roles, 'FAIL')
            packets = {wave: put('reviews/'+cid+'/'+wave+'/packet.json', {'wave': wave})
                       for wave in ('initial', 'selected')}
            for wave in (('initial',) if reused else ('initial', 'selected')):
                reviews = {}
                for profile in ('editorial', 'craft', 'portfolio'):
                    raw = {'case_id': cid, 'wave': wave, 'profile': profile,
                           'images': {role: {'ratings': {dim: {'score': score}
                                      for dim, score in scores.items()}} for role in roles},
                           'set': {'diversity': 1}}
                    raw_records[(wave, profile)] = raw
                    prefix = 'reviews/'+cid+'/'+wave+'/cli/'+profile+'/'
                    raw_pin = put(prefix+profile+'.observations.json', raw)
                    comp_pin = put(prefix+'completion.json', {
                        'reports': {profile+'.observations.json': raw_pin}})
                    raw_inventory.append({'wave': wave, 'profile': profile,
                        'raw_observations': raw_pin, 'completion': comp_pin,
                        'counts': {'records': 5, 'score_slots': 35, 'valid_scores': 30}})
                    reviews[profile] = {'provenance': {'derived_session_id': wave+'-'+profile},
                                       'images': {role: {'scores': scores} for role in roles}}
                summaries[wave] = put('reviews/'+cid+'/'+wave+'/summary.json', {
                    'case_id': cid, 'wave': wave, 'packet': packets[wave],
                    'procedure_gate': 'PASS', 'image_gates': image_gates,
                    'image_gate_counts': {'PASS': 0, 'FAIL': 5, 'NA': 0},
                    'set_gate': 'FAIL', 'counts': counts, 'reviews': reviews})
                assets[wave] = put('reviews/'+cid+'/'+wave+'/source-asset-audit.json', {
                    'case_id': cid, 'wave': wave, 'gate': 'PASS',
                    'packet': {key: value for key, value in packets[wave].items() if key != 'bytes'},
                    'profiles': {p: {'gate': 'PASS'} for p in ('editorial', 'craft', 'portfolio')}})
            stages = {}
            for wave in ('initial', 'selected'):
                reuse = reused and wave == 'selected'; actual_wave = 'initial' if reuse else wave
                compact = put('reviews/'+cid+'/'+wave+'/compact-recording-audit.json',
                              {'gate': 'PASS', 'synthetic_wave': wave})
                item = {'gate': 'FAIL', 'original_v4_set_gate': 'FAIL',
                        'original_v4_image_gates': image_gates,
                        'source_attestation_gate': 'PASS', 'source_attestation_audit': assets[actual_wave],
                        'compact_recording_gate': 'PASS', 'compact_recording_audit': compact,
                        'summary': summaries[actual_wave], 'reused_complete_initial_three': reuse}
                if reuse:
                    item['reuse'] = put('reviews/'+cid+'/'+wave+'/reuse.json', {'synthetic': True})
                state = {'expected_count': 5, 'roles': roles, 'status': 'READY', 'errors': [],
                         'images': [{'image_id': role, 'role': role, 'ready': True} for role in roles],
                         'mode': 'COMPLETE_FIRST_THREE_REUSED' if reuse else 'THREE_FRESH_COMPLETE_CRITICS',
                         'packet': packets[wave]}
                put('reviews/'+cid+'/'+wave+'/readiness.json', state)
                put('reviews/'+wave+'-stage-readiness.json', {
                    'wave': wave, 'cases': {cid: state}, 'planned_roles': roles,
                    'planned_role_count': 5, 'closed_role_count': 5, 'planned_case_count': 1,
                    'all_makers_closed': True, 'corpus': corpus,
                    'maker_inventory': {m['role']: {'closed': True, 'errors': [],
                        'terminal': m['terminal'], 'counts': m['counts'], 'selected_stage': 'initial'}
                        for m in makers}})
                stages[wave] = {'cases': {cid: item}, 'image_gates': image_gates,
                               'image_gate_counts': {'PASS': 0, 'FAIL': 5, 'NA': 0},
                               'whole_corpus_gate': 'FAIL'}
            n = 1 if reused else 2
            final = {'poster_calls_closed': True, 'poster_role_denominator': 5,
                     'poster_native_attempts': 5, 'caller_records': [{} for _ in roles],
                     'makers': makers, 'stages': stages, 'pre_generation_freeze': freeze,
                     'critic_recording_freeze': recording, 'corpus': corpus,
                     'actual_unique_review_sessions': 3*n,
                     'actual_review_counts': {'records': 15*n, 'score_slots': 105*n, 'valid_scores': 90*n},
                     'raw_observation_inventory': raw_inventory,
                     'raw_observation_counts_separate': {'records': 15*n, 'score_slots': 105*n, 'valid_scores': 90*n}}
            put('planning/final-evidence.json', final)
            matrix = []
            for wave in ('initial', 'selected'):
                item = stages[wave]['cases'][cid]
                for role in roles:
                    for profile in ('editorial', 'craft', 'portfolio'):
                        matrix.append({'displayed_wave': wave,
                            'actual_raw_wave': 'initial' if reused else wave,
                            'role': role, 'profile': profile, 'scores': scores,
                            'summary': item['summary'], 'source_kind': 'actual_immutable_raw_observations',
                            'reused_complete_initial_three': item['reused_complete_initial_three']})
            put('raw-score-matrices.json', {'presentation_records': matrix,
                'actual_unique_record_counts': final['actual_review_counts']})
            for relative in ('summarize.py', 'audit_source_assets.py',
                             'method-recording-v2/audit_compact_bindings.py'):
                put(relative, {'synthetic_metadata_marker_not_executed': True})
            index = {'source_root': source, 'files': rows, 'mapped_sources': len(rows), 'closed_evidence': final}
            (root/'archive-index.json').write_text(json.dumps(index))
            calls = {'v4': [], 'source': [], 'compact': [], 'reuse': []}
            def json_read(path):
                return json.loads(Path(path).read_bytes())
            def synthetic_module(path, name):
                if Path(path).name == 'summarize.py':
                    def summary(args):
                        calls['v4'].append(json_read(args.packet)['wave'])
                        return json_read(Path(args.packet).parent/'summary.json')
                    return types.SimpleNamespace(summary=summary, read_json=lambda path: (json_read(path), {}),
                                                 digest=lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest())
                if Path(path).name == 'audit_source_assets.py':
                    def audit(packet, cli):
                        calls['source'].append(json_read(packet)['wave'])
                        return json_read(Path(packet).parent/'source-asset-audit.json')
                    return types.SimpleNamespace(audit=audit)
                assert Path(path).name == 'audit_compact_bindings.py'
                def audit(packet, cli, access):
                    calls['compact'].append(json.loads(access.reader(packet))['wave'])
                    return json.loads(access.reader(str(Path(packet).parent/'compact-recording-audit.json')))
                def audit_reuse(packet, reuse_path, access):
                    calls['reuse'].append(json.loads(access.reader(packet))['wave'])
                    return json.loads(access.reader(str(Path(packet).parent/'compact-recording-audit.json')))
                return types.SimpleNamespace(ByteAccess=lambda reader: types.SimpleNamespace(reader=reader),
                                             audit=audit, audit_reuse=audit_reuse)
            verifier.module = synthetic_module
            attempts = []
            def allowed(path, operation):
                if path.is_relative_to(root) or (operation in ('stat', 'lstat', 'readlink', 'access')
                                                and root.is_relative_to(path)):
                    return
                attempts.append({'operation': operation, 'path': str(path)})
                raise AssertionError('Outside synthetic archive metadata/read attempted')
            try:
                with access_guard(allowed):
                    replay = verifier.verify(root)
                    coverage = check_phase_coverage(final, replay)
                    matrix_result = score_matrix_inventory(root, index, verifier)
                    assert not attempts
                expected_waves = ['initial', 'initial' if reused else 'selected']
                assert calls['v4'] == calls['source'] == expected_waves
                assert calls['compact'] == (['initial'] if reused else ['initial', 'selected'])
                assert calls['reuse'] == (['selected'] if reused else [])
                results.append({'synthetic_complete_initial_reuse': reused, 'phase_coverage': coverage,
                                'auditor_call_waves': calls, 'raw_score_matrices': matrix_result,
                                'outside_metadata_and_read_attempts': attempts})
            finally:
                verifier.module = original_module
    return {'fixtures': results, 'actual_quality_engines_or_actors_executed': 0,
            'actual_quality_claim': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--helper', type=Path)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert (args.helper is None) != (args.archive is None)
    sys.dont_write_bytecode = True
    if args.helper is not None:
        verifier = load_module(args.helper)
        result = {'status': 'PASS', 'mode': 'SYNTHETIC_PREFLIGHT_ONLY',
                  'helper_sha256': hashlib.sha256(args.helper.read_bytes()).hexdigest(),
                  'containment': containment_fixtures(verifier),
                  'synthetic_phase_replay': phase_replay_fixtures(verifier),
                  'selected_raw_scores_or_reports_read': False,
                  'native_calls_or_critics_launched': 0}
    else:
        root = Path(os.path.abspath(args.archive))
        runtime = Path(sys.executable).resolve().parents[2]
        bootstrap_outside = []
        def bootstrap_allowed(path, operation):
            metadata = operation in ('stat', 'lstat', 'readlink', 'access')
            if path.is_relative_to(root) or path.is_relative_to(runtime):
                return
            if metadata and (root.is_relative_to(path) or runtime.is_relative_to(path)):
                return
            bootstrap_outside.append({'operation': operation, 'path': str(path)})
            raise AssertionError('Unknown outside bootstrap metadata/read attempted')
        with access_guard(bootstrap_allowed):
            root, helper = bootstrap_archive(args.archive)
            verifier = load_module(helper)
            root = verifier.archive_root(root)
            index_path = verifier.archive_path(root/'archive-index.json', root)
            index = json.loads(index_path.read_bytes())
            assert not bootstrap_outside
        original_sources = {Path(row['source_absolute']) for row in index['files']}
        source_root = Path(index['source_root'])
        blocked = []
        outside = []
        def allowed(path, operation):
            metadata = operation in ('stat', 'lstat', 'readlink', 'access')
            if path in original_sources or path.is_relative_to(source_root):
                blocked.append({'operation': operation, 'path': str(path)})
                raise AssertionError('Original host metadata/read attempted')
            if path.is_relative_to(root) or path.is_relative_to(runtime):
                return
            if metadata and (root.is_relative_to(path) or runtime.is_relative_to(path)):
                return
            outside.append({'operation': operation, 'path': str(path)})
            raise AssertionError('Unknown outside metadata/read attempted')
        with access_guard(allowed):
            links = check_links(root, index, verifier, args.output.absolute())
            inventory = raw_inventory(root, index)
            replay = verifier.verify(root)
            matrices = score_matrix_inventory(root, index, verifier)
            assert replay['status'] == 'PASS' and not blocked and not outside
            for value in (source_root/'planning/final-evidence.json',
                          root/'..'/source_root.name/'planning/final-evidence.json',
                          '/unknown/outside/artifact', '../original-host-path', '',
                          'relative-without-base'):
                try:
                    verifier.archive_path(value, root)
                except ValueError:
                    pass
                else:
                    raise AssertionError('Outside path accepted: '+str(value))
            assert not blocked and not outside
        phase_coverage = check_phase_coverage(index['closed_evidence'], replay)
        result = {'status': 'PASS', 'actual_archive': str(root),
                  'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'archive_index_sha256': hashlib.sha256(index_path.read_bytes()).hexdigest(),
                  'portable_frozen_v4_replay': replay, 'phase_coverage': phase_coverage,
                  'exact_raw_inventory': inventory, 'raw_score_matrices': matrices,
                  'original_host_metadata_and_read_attempts': blocked,
                  'unknown_outside_metadata_and_read_attempts': outside,
                  'unknown_outside_bootstrap_metadata_and_read_attempts': bootstrap_outside,
                  'guarded_operations': [name for _, names in GUARDED for name in names],
                  'containment': containment_fixtures(verifier), 'local_links': links,
                  'native_calls_or_critics_launched': 0,
                  'limits': ['Exact bytes and both frozen v4/source/compact gates are replayed through explicit archive mapping.',
                             'Original low, NULL and NA records are retained. No result is replaced or invented.',
                             'Semantic image viewing remains the original critics\u2019 attestation.',
                             'One prospectively new landscape request after whole R10 closure; bounded transfer, no isolated causal, universal quality, or AI authorship proof.']}
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2); handle.write('\n')
    if args.archive is not None:
        with access_guard(allowed):
            assert check_links(root, index, verifier) == links
            assert not blocked and not outside
    print(json.dumps({k: v for k, v in result.items() if k != 'portable_frozen_v4_replay'}))


if __name__ == '__main__':
    main()
