"""Synthetic metadata only: no real review, image, actor, or visual score.

The prep validation and maker inventories are mocked because fixture view files
are explicitly text metadata, not pixels. Real helper shell commands run only in
temporary synthetic directories. Synthetic CLI events model the frozen runner
schema; no critic session is launched or claimed by these tests.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import shlex
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


prep = module('selected_test_preparer', HERE/'prepare_reviews_compact.py')
audit = prep.compact_audit
adapter = audit.adapter
summary = audit.summary_helper
v1 = module('frozen_v1_adapter_metadata_test', ROOT/'method-only/compact_critic_adapter.py')


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


def runner_pin(path):
    """Exact frozen run_agent.py receipt shape: path/hash, without bytes."""
    result = audit.pin(path)
    return {key: result[key] for key in ('path', 'sha256')}


def raw_record(packet, packet_path, profile):
    reason = 'Synthetic metadata fixture contains no pixels; no visual inspection occurred.'
    ev = [['native', 'metadata fixture', reason]]
    result = {'schema_version': 1, 'kind': 'compact_critic_observations',
              'case_id': packet['case_id'], 'wave': packet['wave'], 'profile': profile,
              'session_id': None, 'packet': prep.evidence.pin(packet_path),
              'procedure': {'fresh_session': False, 'all_views_before_scoring': False,
                            'order_compliant': False, 'method': reason,
                            'source_assets_viewed': [{'asset_id': source['asset_id'],
                                                     'path': source['actual_path'], 'sha256': source['sha256'],
                                                     'viewed': False, 'reason': reason}
                                                    for source in packet['source_assets']],
                            'protected_layouts_read': [{'manifest': row['manifest'], 'read': False, 'reason': reason}
                                                       for row in packet['protected_layouts']]},
              'viewed': [], 'images': {}}
    ids = [image['image_id'] for image in packet['images']]
    for image in packet['images']:
        iid = image['image_id']
        for view in adapter.VIEWS:
            bound = image['views'][view]
            result['viewed'].append({'image_id': iid, 'view': view, 'path': bound['path'],
                                     'sha256': bound['sha256'], 'viewed': False, 'reason': reason})
        mandatory = {name: {'status': 'NA', 'issues': [reason]}
                     for name in ('text', 'style', 'ratio', 'no_type_only', 'substantive_visual')}
        for name in ('style', 'no_type_only', 'substantive_visual'):
            mandatory[name]['evidence'] = copy.deepcopy(ev)
        result['images'][iid] = {
            'copy': [{'raw': '', 'layout': {'status': 'NA', 'observations': reason},
                      'ambiguity': None, 'revisit': None} for _ in packet['copy']],
            'mandatory': mandatory,
            'ratings': {dimension: {'score': None, 'reason': reason, 'evidence': copy.deepcopy(ev)}
                        for dimension in adapter.DIMENSIONS},
            'source_fidelity': [{'asset_id': source['asset_id'], 'status': 'NA', 'observations': reason}
                                for source in packet['source_assets']],
            'residuals': [reason]}
    result['set'] = {'members': ids, 'count_fidelity': {'status': 'NA', 'observed_count': 0, 'issues': [reason]},
                     'diversity': None, 'reason': reason,
                     'evidence': [[iid, 'thumbnail320', 'metadata fixture', reason] for iid in ids],
                     'residuals': [reason]}
    return result


@contextmanager
def prepared_fixture(*, all_closed=True, wave='selected'):
    with tempfile.TemporaryDirectory(prefix='synthetic-selected-v2-', dir=HERE) as temp:
        root = Path(temp)
        production = root/'production-metadata'; production.mkdir()
        source = root/'source.metadata'; source.write_bytes(b'NO SOURCE PIXELS; SYNTHETIC METADATA ONLY\n')
        layout = root/'source-layout.json'; write(layout, {'synthetic_metadata_only': True})
        source_pin, layout_pin = audit.pin(source), audit.pin(layout)
        asset = {'asset_id': 'SYNTHETIC-SOURCE', 'ready': True, 'actual_path': source_pin['path'],
                 'sha256': source_pin['sha256'], 'manifest_path': layout_pin['path'],
                 'manifest_sha256': layout_pin['sha256'], 'measured_layout': {'synthetic_metadata_only': True}}
        case = {'case_id': 'SYNTHETIC-METADATA-ONLY', 'count': 5,
                'request': 'Synthetic metadata only; no client request or image quality claim.',
                'copy': [{'text': f'Synthetic copy {i}', 'kind': 'text', 'fixed_newlines': False} for i in range(10)],
                'styles': [], 'conditions': [],
                'roles': [{'role_id': f'SYNTHETIC-M{i+1}', 'ordinal': i+1, 'ratio': '16:9', 'assets': [asset]}
                          for i in range(5)]}
        corpus = root/'synthetic-corpus.json'; write(corpus, case)
        inventories = {}
        for role in case['roles']:
            iid = role['role_id']
            manifest = root/(iid+'-manifest.json'); write(manifest, {'synthetic_metadata_only': True})
            files = {}
            for view, dimensions in zip(adapter.VIEWS, ((1600, 900), (720, 405), (320, 180))):
                path = root/(iid+'-'+view+'.metadata')
                path.write_bytes(b'NO POSTER PIXELS; SYNTHETIC METADATA ONLY\n'+(iid+view).encode())
                files['original' if view == 'native' else view] = {**audit.pin(path), 'width': dimensions[0], 'height': dimensions[1]}
            stage = {'stage': 'initial', 'outcome': 'returned', 'manifest': audit.pin(manifest), 'files': files}
            inventories[iid] = {'role': iid, 'closed': all_closed or role['ordinal'] <= 2,
                                'outcome': 'synthetic-metadata', 'stages': [stage],
                                'selected_stage': 'initial', 'errors': []}
        args = SimpleNamespace(corpus=str(corpus), production=str(production), out=str(root/'prepared-metadata'),
                               wave=wave, candidate_label='SYNTHETIC', initial_root=None)
        # Only fixture PNG/maker checks are stubbed. The actual v2 prep writes the
        # packet, prompt, and job schema used by the subsequent shell/audit test.
        with patch.object(prep, 'terminal', side_effect=lambda _p, role, _c: inventories[role['role_id']]), \
             patch.object(prep.summary_helper, 'validate_packet', return_value=([], {}, {})):
            prepared = prep.prepare(args)
        phase = root/'prepared-metadata'/case['case_id']/wave
        yield root, phase, prepared


def record_synthetic_completion(phase, profile, packet, *, invoke=True):
    job_path = phase/'jobs'/(profile+'.json')
    job = json.loads(job_path.read_bytes())
    folder = Path(job['output_dir']); folder.mkdir(parents=True)
    packet_path = phase/'packet.json'
    raw_path = folder/(profile+'.observations.json')
    raw = raw_record(packet, packet_path, profile); write(raw_path, raw)
    before = raw_path.read_bytes()
    command = audit.adapter_command(packet, packet_path, raw_path, folder)
    if invoke:
        completed = subprocess.run(command, shell=True, executable='/bin/zsh', text=True, capture_output=True)
        if completed.returncode:
            raise AssertionError(completed.stderr)
        if raw_path.read_bytes() != before:
            raise AssertionError('Synthetic raw record was modified')
    launch = {'started_utc': '2026-10-08T00:00:00+00:00',
              'argv': ['codex', '--no-daemon', '--ask-for-approval', 'never', 'exec', '--ephemeral'],
              'fresh_session': True, 'case_id': packet['case_id'], 'wave': packet['wave'], 'profile': profile,
              'prompt': runner_pin(job['prompt_file']), 'job': runner_pin(job_path),
              'input_pins': [runner_pin(path) for path in job['inputs']]}
    # Synthetic event IDs are fixture data, never real actor/session evidence.
    thread_id = 'SYNTHETIC-NOT-A-REAL-SESSION-'+profile
    events = [{'type': 'thread.started', 'thread_id': thread_id}]
    if invoke:
        events.append({'type': 'item.completed', 'item': {'type': 'command_execution',
                       'command': '/bin/zsh -lc '+shlex.quote(command), 'status': 'completed', 'exit_code': 0}})
    events.append({'type': 'turn.completed'})
    trace_path = folder/'trace.jsonl'
    with trace_path.open('xb') as handle:
        for event in events:
            handle.write(json.dumps(event).encode()+b'\n')
    write(folder/'launch.json', launch)
    completion = {**launch, 'completed_utc': '2026-10-08T00:01:00+00:00', 'exit_code': 0,
                  'session_ids': [thread_id], 'turn_completed_count': 1, 'input_pins_unchanged': True,
                  'trace': runner_pin(trace_path),
                  'reports': {name: runner_pin(folder/name) for name in job['expected_outputs'] if (folder/name).is_file()}}
    write(folder/'completion.json', completion)
    return command, raw_path


class SelectedRecordingTest(unittest.TestCase):
    def test_exact_frozen_assessment_and_normalization_logic(self):
        def functions(path):
            return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(path.read_text()).body
                    if isinstance(node, ast.FunctionDef)}
        original = functions(ROOT/'method-only/compact_critic_adapter.py')
        current = functions(HERE/'compact_critic_adapter.py')
        for name in original:
            if name not in ('pin', 'load_json'):
                self.assertEqual(original[name], current[name], name)
        old_preparer = functions(ROOT/'method-only/prepare_reviews_compact.py')
        new_preparer = functions(HERE/'prepare_reviews_compact.py')
        for name in old_preparer:
            if name not in ('prompt', 'prepare', 'main'):
                self.assertEqual(old_preparer[name], new_preparer[name], name)
        self.assertEqual(hashlib.sha256((ROOT/'summarize.py').read_bytes()).hexdigest(), adapter.SUMMARY_SHA256)
        for kind in ('text', 'url'):
            for fixed in (True, False):
                entry = {'kind': kind, 'fixed_newlines': fixed}
                for value in ('가 나 · 다', '가나·다', 'a / b', 'https://example.invalid/a/b', '  첫  줄\r\n 둘째 줄 ', '\u1100\u1161'):
                    self.assertEqual(adapter.normalize(value, entry), summary.normalize(value, entry))

    def test_explicit_v2_import_even_with_frozen_names_cached(self):
        frozen_audit = module('frozen_audit_test', ROOT/'method-only/audit_compact_bindings.py')
        with patch.dict(sys.modules, {'audit_compact_bindings': frozen_audit, 'compact_critic_adapter': v1}):
            imported = module('selected_import_precedence_test', HERE/'prepare_reviews_compact.py')
        self.assertEqual(Path(imported.compact_audit.__file__).resolve(), HERE/'audit_compact_bindings.py')
        self.assertEqual(Path(imported.compact_audit.adapter.__file__).resolve(), HERE/'compact_critic_adapter.py')

    def test_prep_raw_shell_adapter_and_audit_actual_runner_pin_shapes(self):
        with prepared_fixture() as (_root, phase, result):
            self.assertEqual(result['jobs_written'], 3)
            self.assertFalse(result['launched'])
            packet = json.loads((phase/'packet.json').read_bytes())
            self.assertEqual(packet['compact_recording']['schema_version'], 2)
            self.assertEqual(packet['compact_recording']['pin_schema'], 'path-sha256-bytes-v2')
            for profile in prep.PROFILES:
                command, raw_path = record_synthetic_completion(phase, profile, packet)
                prompt = (phase/'prompts'/(profile+'.txt')).read_text()
                literal = 'text(await tools.exec_command({cmd: '+json.dumps(command, ensure_ascii=False)+'}));'
                self.assertIn(literal, prompt)
                self.assertIn(json.dumps(prep.evidence.pin(phase/'packet.json'), ensure_ascii=False), prompt)
                self.assertIn('all 15 exact poster views before the first text-reading/transcription', prompt)
                old_packet, old_pin = v1.load_json(phase/'packet.json')
                with self.assertRaisesRegex(ValueError, 'Raw observations must bind the exact input packet'):
                    v1.export(old_packet, json.loads(raw_path.read_bytes()), packet_pin=old_pin)
            checked = audit.audit(phase/'packet.json', phase/'cli')
            self.assertEqual(checked['gate'], 'PASS', checked)
            for profile in prep.PROFILES:
                report = json.loads((phase/'cli'/profile/(profile+'.json')).read_bytes())
                self.assertEqual(report['procedure']['viewed_count'], 0)
                self.assertFalse(report['procedure']['fresh_session'])
                self.assertIsNone(report['set']['diversity'])
                self.assertEqual(report['set']['count_fidelity']['status'], 'NA')
                self.assertTrue(all(score is None for row in report['images'].values() for score in row['scores'].values()))
                self.assertTrue(all(check['status'] == 'NA' for row in report['images'].values() for check in row['mandatory'].values()))
                self.assertTrue(checked['profiles'][profile]['bindings']['adapter_trace_events'])
            # Archive replay reads only explicit stored metadata and helpers.
            files = {str(path.resolve()): path.read_bytes() for path in _root.rglob('*') if path.is_file()}
            for pin in packet['helper_pins'].values():
                files[pin['path']] = Path(pin['path']).read_bytes()
            for name in ('review_rules', 'critic_rubric', 'ratio_policy'):
                pin = packet[name]; files[pin['path']] = Path(pin['path']).read_bytes()
            replay = audit.audit(phase/'packet.json', phase/'cli', access=audit.ByteAccess(reader=lambda path: files[path]))
            self.assertEqual(replay['gate'], 'PASS', replay)

    def test_missing_wrong_extra_packet_pin_fields_fail_before_outputs(self):
        for mode in ('missing_bytes', 'wrong_bytes', 'bool_bytes', 'wrong_hash', 'wrong_path', 'extra'):
            with self.subTest(mode=mode), prepared_fixture() as (_root, phase, _result):
                packet = json.loads((phase/'packet.json').read_bytes())
                job = json.loads((phase/'jobs/editorial.json').read_bytes())
                folder = Path(job['output_dir']); folder.mkdir(parents=True)
                raw_path = folder/'editorial.observations.json'
                raw = raw_record(packet, phase/'packet.json', 'editorial')
                if mode == 'missing_bytes': raw['packet'].pop('bytes')
                if mode == 'wrong_bytes': raw['packet']['bytes'] += 1
                if mode == 'bool_bytes': raw['packet']['bytes'] = True
                if mode == 'wrong_hash': raw['packet']['sha256'] = '0'*64
                if mode == 'wrong_path': raw['packet']['path'] = '/unknown-synthetic-packet'
                if mode == 'extra': raw['packet']['unexpected'] = 1
                write(raw_path, raw); before = raw_path.read_bytes()
                completed = subprocess.run(audit.adapter_command(packet, phase/'packet.json', raw_path, folder),
                                           shell=True, executable='/bin/zsh', capture_output=True, text=True)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn('Raw observations must bind the exact input packet', completed.stderr)
                self.assertEqual(raw_path.read_bytes(), before)
                self.assertFalse((folder/'editorial.json').exists())
                self.assertFalse((folder/'editorial.md').exists())

    def test_byte_access_exact_hash_and_optional_runner_size(self):
        data = b'SYNTHETIC METADATA BYTES\n'
        access = audit.ByteAccess(reader=lambda _path: data)
        expected = {'path': '/synthetic-metadata', 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        self.assertEqual(access.pin(expected['path']), expected)
        self.assertEqual(access.checked_pin(expected), expected)
        self.assertEqual(access.checked_pin({key: expected[key] for key in ('path', 'sha256')}), expected)
        for pin in ({**expected, 'bytes': len(data)+1}, {**expected, 'bytes': True}, {**expected, 'sha256': '0'*64}):
            with self.assertRaises(ValueError): access.checked_pin(pin)
        with self.assertRaises(ValueError):
            access.checked_pin({'path': expected['path'], 'sha256': expected['sha256']}, require_size=True)
        with self.assertRaises(ValueError): audit.ByteAccess(path_map={}).pin(HERE/'compact_critic_adapter.py')

    def test_audit_integrated_bad_pins_and_missing_or_late_call_are_na(self):
        for mode in ('raw_packet_missing_bytes', 'raw_packet_wrong_bytes', 'raw_packet_wrong_hash',
                     'completion_wrong_bytes', 'completion_wrong_hash', 'missing_call', 'late_call'):
            with self.subTest(mode=mode), prepared_fixture() as (_root, phase, _result):
                packet = json.loads((phase/'packet.json').read_bytes())
                for profile in prep.PROFILES:
                    record_synthetic_completion(phase, profile, packet)
                folder = phase/'cli/editorial'
                # Mutations are confined to this temporary synthetic fixture.
                if mode.startswith('raw_packet_'):
                    path = folder/'editorial.observations.json'; value = json.loads(path.read_bytes())
                    if mode.endswith('missing_bytes'): value['packet'].pop('bytes')
                    if mode.endswith('wrong_bytes'): value['packet']['bytes'] += 1
                    if mode.endswith('wrong_hash'): value['packet']['sha256'] = '0'*64
                    path.write_text(json.dumps(value))
                elif mode.startswith('completion_'):
                    path = folder/'completion.json'; value = json.loads(path.read_bytes())
                    receipt = value['reports']['editorial.observations.json']
                    if mode.endswith('wrong_bytes'): receipt['bytes'] = audit.pin(receipt['path'])['bytes']+1
                    if mode.endswith('wrong_hash'): receipt['sha256'] = '0'*64
                    path.write_text(json.dumps(value))
                else:
                    path = folder/'trace.jsonl'
                    events = [json.loads(line) for line in path.read_bytes().splitlines()]
                    events = [events[0], events[2]] if mode == 'missing_call' else [events[0], events[2], events[1]]
                    path.write_bytes(b''.join(json.dumps(event).encode()+b'\n' for event in events))
                    completion_path = folder/'completion.json'; value = json.loads(completion_path.read_bytes())
                    value['trace'] = runner_pin(path)
                    completion_path.write_text(json.dumps(value))
                checked = audit.audit(phase/'packet.json', phase/'cli')
                self.assertEqual(checked['gate'], 'NA', checked)
                self.assertEqual(checked['profiles']['editorial']['gate'], 'NA', checked)

    def test_shell_and_functions_exec_proof_absent_or_late_is_rejected(self):
        command = '/synthetic/python /synthetic/adapter.py --packet /synthetic/packet --observations /synthetic/raw --output-dir /synthetic/output'
        shell_event = {'type': 'item.completed', 'item': {'type': 'command_execution',
                       'command': '/bin/zsh -lc '+shlex.quote(command), 'status': 'completed', 'exit_code': 0}}
        code = 'text(await tools.exec_command({cmd: '+json.dumps(command)+'}));'
        function_event = {'type': 'item.completed', 'item': {'type': 'mcp_tool_call', 'server': 'functions', 'tool': 'exec',
                          'arguments': {'code': code}, 'result': {'exit_code': 0}}}
        ending = {'type': 'turn.completed'}
        for event in (shell_event, function_event):
            self.assertEqual(audit.adapter_trace_events([event, ending], command), [0])
            self.assertEqual(audit.adapter_trace_events([ending, event], command), [])
        self.assertEqual(audit.adapter_trace_events([ending], command), [])
        bad = copy.deepcopy(shell_event); bad['item']['exit_code'] = 1
        self.assertEqual(audit.adapter_trace_events([bad, ending], command), [])

    def test_global_barrier_and_initial_scope_rejection(self):
        with prepared_fixture(all_closed=False) as (_root, _phase, result):
            self.assertFalse(result['all_makers_closed'])
            self.assertEqual(result['jobs_written'], 0)
        with self.assertRaisesRegex(ValueError, 'cannot prepare or repair initial'):
            with prepared_fixture(wave='initial'): pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
