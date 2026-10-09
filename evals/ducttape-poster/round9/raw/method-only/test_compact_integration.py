"""Synthetic metadata tests only: no live request, job launch, critic, or image bytes."""
import ast
import copy
import hashlib
import importlib.util
import json
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
import audit_compact_bindings as audit
import compact_critic_adapter as adapter
import prepare_reviews_compact as prep

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


class MemoryArchive:
    def __init__(self):
        self.files, self.reads = {}, []
        self.access = audit.ByteAccess(reader=self.read)

    def read(self, name):
        self.reads.append(name)
        if name not in self.files:
            raise ValueError('No explicit synthetic archive member: ' + name)
        return self.files[name]

    def store(self, path, data):
        data = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False, indent=2).encode() + b'\n'
        path = self.access.logical(path)
        self.files[path] = data
        return {'path': path, 'sha256': hashlib.sha256(data).hexdigest()}


def fixture(unknown_receipt=False, low_score=False):
    archive = MemoryArchive()
    root = Path('/synthetic-original-host-does-not-exist/compact-method')
    packet_path, cli = root / 'packet.json', root / 'cli'
    helper_names = ('evidence_io.py', 'summarize.py', 'run_agent.py', 'prepare_reviews_compact.py',
                    'compact_critic_adapter.py', 'README.md', 'compact-recording-addendum.md', 'audit_compact_bindings.py')
    helpers = {}
    for name in helper_names:
        source = HERE / name if (HERE / name).is_file() else BASE / name
        helpers[name] = archive.store(root / 'pinned' / name, source.read_bytes())
    rules = archive.store(root / 'pinned/review_rules.md', (BASE / 'review_rules.md').read_bytes())
    rubric = archive.store(root / 'pinned/critic_rubric.md', (BASE / 'critic_rubric.md').read_bytes())
    ratio = archive.store(root / 'pinned/ratio-policy.json', b'SYNTHETIC METADATA ONLY\n')
    method = {'schema_version': 1, 'kind': 'compact_critic_observations', 'python': '/synthetic/python',
              'adapter': helpers['compact_critic_adapter.py'], 'method': helpers['README.md'],
              'addendum': helpers['compact-recording-addendum.md'], 'binding_audit': helpers['audit_compact_bindings.py'],
              'preparer': helpers['prepare_reviews_compact.py'],
              'expected_outputs': ['PROFILE.observations.json', 'PROFILE.json', 'PROFILE.md'],
              'execution': 'Inside the same fresh critic session before immutable CLI completion; no post-completion export'}
    packet = {'schema_version': 1, 'case_id': 'SYNTHETIC-METADATA-ONLY', 'candidate_label': 'synthetic',
              'wave': 'initial', 'expected_count': 5, 'critic_profiles': list(prep.PROFILES),
              'full_request': 'Synthetic metadata only, no actual client request.', 'literal_case_sha256': '0' * 64,
              'normalization': adapter.NORMALIZATION, 'copy': [{'text': 'entry %02d' % i, 'kind': 'text', 'fixed_newlines': False} for i in range(10)],
              'requirements': {'style': 'Synthetic literal conditions.', 'ratio': [16, 9], 'no_type_only': True},
              'review_rules': rules, 'critic_rubric': rubric, 'ratio_policy': ratio, 'helper_pins': helpers,
              'source_assets': [], 'protected_layouts': [], 'images': [], 'compact_recording': method}
    for i in range(5):
        iid = 'SYNTHETIC-%d' % i
        manifest = archive.store(root / (iid + '-manifest.json'), {'synthetic': True})
        views = {}
        for view, dimensions in zip(adapter.VIEWS, [(1600, 900), (720, 405), (320, 180)]):
            # Plain text metadata bytes: intentionally not PNGs or generated images.
            views[view] = archive.store(root / (iid + '-' + view + '.metadata'), b'SYNTHETIC NONIMAGE METADATA ' + (iid + view).encode())
            views[view].update(width=dimensions[0], height=dimensions[1])
        packet['images'].append({'image_id': iid, 'role': iid, 'stage': 'initial', 'source_manifest': manifest,
                                 'views': views, 'ratio_requirement': [16, 9], 'style_requirement': 'Synthetic literal conditions.'})
    packet_pin = archive.store(packet_path, packet)
    input_pins = [packet_pin, rules, rubric, ratio] + list(helpers.values())
    for image in packet['images']:
        input_pins += [image['source_manifest']] + list(image['views'].values())
    input_pins = [{'path': p['path'], 'sha256': p['sha256']} for p in input_pins]
    ids = [image['image_id'] for image in packet['images']]
    for profile in prep.PROFILES:
        folder = cli / profile
        raw = {'schema_version': 1, 'kind': 'compact_critic_observations', 'case_id': packet['case_id'], 'wave': packet['wave'],
               'profile': profile, 'session_id': None, 'packet': packet_pin,
               'procedure': {'fresh_session': True, 'all_views_before_scoring': True, 'order_compliant': True,
                             'method': 'Synthetic recording/provenance metadata only; no actual viewing.',
                             'source_assets_viewed': [], 'protected_layouts_read': []}, 'viewed': [], 'images': {}}
        ev = [['native', 'synthetic position', 'Synthetic evidence metadata, not an image observation.']]
        for image in packet['images']:
            iid = image['image_id']
            for view in adapter.VIEWS:
                pin = image['views'][view]
                raw['viewed'].append({'image_id': iid, 'view': view, 'path': pin['path'], 'sha256': pin['sha256'], 'viewed': True})
            raw['images'][iid] = {'copy': [{'raw': 'entry %02d' % i, 'layout': {'status': 'PASS', 'observations': 'Synthetic layout only.'},
                                           'ambiguity': None, 'revisit': None} for i in range(10)],
                                  'mandatory': {'text': {'status': 'PASS', 'issues': []}, 'ratio': {'status': 'PASS', 'issues': []},
                                                'style': {'status': 'PASS', 'issues': [], 'evidence': copy.deepcopy(ev)},
                                                'no_type_only': {'status': 'PASS', 'evidence': copy.deepcopy(ev)},
                                                'substantive_visual': {'status': 'PASS', 'evidence': copy.deepcopy(ev)}},
                                  'ratings': {d: {'score': 4, 'evidence': copy.deepcopy(ev)} for d in adapter.DIMENSIONS},
                                  'source_fidelity': [], 'residuals': []}
        if unknown_receipt:
            raw['viewed'][0].update(path='/unknown-raw-observed-path-never-an-alias', viewed=False, reason='Synthetic unavailable view.')
            raw['procedure']['all_views_before_scoring'] = False
        if low_score:
            raw['images'][ids[0]]['ratings']['space']['score'] = 2
        raw['set'] = {'members': ids, 'count_fidelity': {'status': 'PASS', 'observed_count': 5, 'issues': []}, 'diversity': 4,
                      'evidence': [[iid, 'thumbnail320', 'synthetic composition', 'Synthetic full-set relationship.'] for iid in ids], 'residuals': []}
        raw_path = folder / (profile + '.observations.json')
        raw_pin = archive.store(raw_path, raw)
        exported = adapter.export(packet, raw, packet_pin=packet_pin, raw_pin=raw_pin, adapter_pin=method['adapter'])
        export_pin = archive.store(folder / (profile + '.json'), exported)
        md_pin = archive.store(folder / (profile + '.md'), adapter.markdown(exported).encode())
        prompt = archive.store(root / ('prompt-' + profile + '.txt'), b'SYNTHETIC PROMPT METADATA\n')
        job = {'profile': profile, 'case_id': packet['case_id'], 'wave': packet['wave'], 'output_dir': str(folder),
               'prompt_file': prompt['path'], 'inputs': [p['path'] for p in input_pins], 'expected_outputs': audit.expected_outputs(profile)}
        job_pin = archive.store(root / ('job-' + profile + '.json'), job)
        launch = {'started_utc': '2026-10-08T00:00:00+00:00', 'argv': ['codex', '--no-daemon', '--ask-for-approval', 'never', 'exec', '--ephemeral'],
                  'fresh_session': True, 'case_id': packet['case_id'], 'wave': packet['wave'], 'profile': profile,
                  'prompt': prompt, 'input_pins': input_pins, 'job': job_pin}
        archive.store(folder / 'launch.json', launch)
        command = audit.adapter_command(packet, packet_path, raw_path, folder)
        code = 'text(await tools.exec_command({cmd: ' + json.dumps(command) + '}));'
        events = [{'type': 'thread.started', 'thread_id': 'SYNTHETIC-SESSION-' + profile},
                  {'type': 'item.completed', 'item': {'type': 'mcp_tool_call', 'server': 'functions', 'tool': 'exec',
                                                     'arguments': {'code': code}, 'result': {'exit_code': 0}}},
                  {'type': 'turn.completed'}]
        trace = archive.store(folder / 'trace.jsonl', b''.join(json.dumps(e).encode() + b'\n' for e in events))
        completion = {**launch, 'completed_utc': '2026-10-08T00:01:00+00:00', 'exit_code': 0,
                      'session_ids': ['SYNTHETIC-SESSION-' + profile], 'turn_completed_count': 1, 'input_pins_unchanged': True,
                      'trace': trace, 'reports': dict(zip(audit.expected_outputs(profile), (raw_pin, export_pin, md_pin)))}
        archive.store(folder / 'completion.json', completion)
    return archive, packet_path, cli, packet


class IntegrationTest(unittest.TestCase):
    def test_shell_wrapped_adapter_event(self):
        command = '/synthetic/python /synthetic/adapter.py --packet /synthetic/packet.json --observations /synthetic/raw.json --output-dir /synthetic/critic'
        events = [{'type': 'item.completed', 'item': {'type': 'command_execution', 'command': '/bin/zsh -lc ' + shlex.quote(command), 'status': 'completed', 'exit_code': 0}}, {'type': 'turn.completed'}]
        self.assertEqual(audit.adapter_trace_events(events, command), [0])

    def test_v2_core_functions_unchanged(self):
        def functions(path):
            return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(path.read_text()).body if isinstance(node, ast.FunctionDef)}
        original, compact = functions(BASE / 'prepare_reviews_v2.py'), functions(HERE / 'prepare_reviews_compact.py')
        for name in ('read', 'canonical', 'value_sha', 'resolve', 'pinned', 'write', 'ratio', 'roles', 'terminal', 'client_style', 'assets', 'main'):
            self.assertEqual(original[name], compact[name], name)

    def test_pinned_three_outputs_and_in_session_prompt(self):
        archive, path, cli, packet = fixture()
        with patch.object(prep.evidence, 'pin', side_effect=archive.access.pin):
            prompt = prep.prompt(path, Path('/synthetic/case.json'), 'editorial', packet, [], cli / 'editorial')
        self.assertIn('all 15 exact poster views before the first text-reading/transcription', prompt)
        self.assertIn('all 10 entries in packet order once', prompt)
        self.assertIn('compact-recording-addendum.md explicitly overrides ONLY', prompt)
        self.assertIn('tools.exec_command({cmd:', prompt)
        self.assertEqual(audit.expected_outputs('editorial'), ['editorial.observations.json', 'editorial.json', 'editorial.md'])

    def test_all_three_raw_export_completion_bindings_archive_only(self):
        archive, path, cli, _ = fixture(low_score=True)
        result = audit.audit(path, cli, access=archive.access)
        self.assertEqual(result['gate'], 'PASS', result)
        self.assertEqual(len(result['profiles']), 3)
        raw, _ = archive.access.load(result['profiles']['editorial']['bindings']['raw_observations']['path'])
        exported, _ = archive.access.load(result['profiles']['editorial']['bindings']['compatibility_json']['path'])
        self.assertEqual(raw['images']['SYNTHETIC-0']['ratings']['space']['score'], 2)
        self.assertEqual(exported['images']['SYNTHETIC-0']['scores']['space'], 2)
        self.assertTrue(all(p in archive.files for p in archive.reads))

    def test_unknown_raw_path_is_not_an_archive_alias(self):
        archive, path, cli, _ = fixture(unknown_receipt=True)
        result = audit.audit(path, cli, access=archive.access)
        self.assertEqual(result['gate'], 'PASS', result)  # Byte bindings valid; actual viewing gate still NA.
        self.assertNotIn('/unknown-raw-observed-path-never-an-alias', archive.reads)
        exported, _ = archive.access.load(result['profiles']['editorial']['bindings']['compatibility_json']['path'])
        self.assertFalse(exported['procedure']['order_compliant'])
        self.assertEqual(exported['procedure']['viewed_count'], 14)

    def test_raw_tampering_export_tampering_or_missing_launch_method_pin_is_na(self):
        for mode in ('raw', 'export', 'input'):
            archive, path, cli, _ = fixture()
            folder = cli / 'editorial'
            if mode in ('raw', 'export'):
                target = folder / ('editorial.observations.json' if mode == 'raw' else 'editorial.json')
                data, _ = archive.access.load(target)
                if mode == 'raw':
                    data['images']['SYNTHETIC-0']['copy'][0]['raw'] = 'tampered synthetic text'
                else:
                    data['images']['SYNTHETIC-0']['scores']['space'] = 5
                archive.store(target, data)
            else:
                launch, _ = archive.access.load(folder / 'launch.json')
                launch['input_pins'] = [p for p in launch['input_pins'] if not p['path'].endswith('compact_critic_adapter.py')]
                archive.store(folder / 'launch.json', launch)
            self.assertEqual(audit.audit(path, cli, access=archive.access)['gate'], 'NA')

    def test_no_adapter_trace_or_post_completion_call_is_na(self):
        for mode in ('absent', 'late'):
            archive, path, cli, _ = fixture()
            folder = cli / 'editorial'
            trace_path = folder / 'trace.jsonl'
            events = [json.loads(x) for x in archive.access.read_bytes(trace_path).splitlines()]
            events = [events[0], events[2]] if mode == 'absent' else [events[0], events[2], events[1]]
            trace_pin = archive.store(trace_path, b''.join(json.dumps(e).encode() + b'\n' for e in events))
            completion, _ = archive.access.load(folder / 'completion.json')
            completion['trace'] = trace_pin
            archive.store(folder / 'completion.json', completion)
            self.assertEqual(audit.audit(path, cli, access=archive.access)['gate'], 'NA')

    def test_archive_map_has_no_host_fallback(self):
        access = audit.ByteAccess(path_map={})
        with self.assertRaises(ValueError):
            access.pin(HERE / 'compact_critic_adapter.py')  # Real host file exists, but is not in the archive map.

    def test_global_maker_barrier_emits_no_critic_jobs(self):
        with tempfile.TemporaryDirectory(prefix='synthetic-compact-barrier-', dir=HERE) as tmp:
            tmp = Path(tmp)
            source = tmp / 'synthetic-metadata-input.json'
            case = {'case_id': 'SYNTHETIC', 'count': 5, 'ratios': ['16:9'] * 5, 'request': 'Synthetic metadata only.',
                    'copy': [{'text': 'entry', 'kind': 'text', 'fixed_newlines': False}], 'conditions': [], 'styles': []}
            source.write_text(json.dumps(case))
            production = tmp / 'synthetic-production-metadata'; production.mkdir()
            args = SimpleNamespace(corpus=str(source), production=str(production), out=str(tmp / 'metadata-readiness'),
                                   wave='selected', candidate_label='synthetic', initial_root=None)
            def terminal(_production, role, _cid):
                return {'role': role['role_id'], 'closed': role['ordinal'] <= 2, 'stages': [], 'errors': [], 'outcome': 'open'}
            def fake_pin(path):
                return {'path': str(Path(path).absolute()), 'sha256': hashlib.sha256(str(path).encode()).hexdigest()}
            with patch.object(prep, 'terminal', side_effect=terminal), patch.object(prep.evidence, 'pin', side_effect=fake_pin):
                result = prep.prepare(args)
            self.assertFalse(result['all_makers_closed'])
            self.assertEqual(result['jobs_written'], 0)
            self.assertFalse(result['launched'])

    def test_complete_reuse_retains_compact_raw_and_original_wave(self):
        archive, packet_path, cli, packet = fixture(low_score=True)
        profile_audit = audit.audit(packet_path, cli, access=archive.access)
        retained, reviews = {}, {}
        for profile, record in profile_audit['profiles'].items():
            b = record['bindings']
            retained[profile] = {'raw_report': b['compatibility_json'], 'launch': b['launch'], 'completion': b['completion'],
                                 'trace': b['trace'], 'actual_session_id': b['actual_session_id'],
                                 'compact_observations': b['raw_observations'], 'compact_binding': b}
            exported, _ = archive.access.load(b['compatibility_json']['path'])
            reviews[profile] = {'raw_data': exported, 'procedure_errors': [], 'set': {'errors': []},
                                'images': {iid: {'errors': []} for iid in exported['images']}}
        summary = {'raw_packet': packet, 'packet': archive.access.pin(packet_path), 'procedure_gate': 'PASS', 'procedure_errors': [],
                   'counts': {'observed_image_profile_records': 15, 'valid_integer_1_to_5_score_values': 105}, 'reviews': reviews}
        summary_pin = archive.store(packet_path.parent / 'summary.json', summary)
        selected = copy.deepcopy(packet); selected['wave'] = 'selected'
        selected_path = packet_path.parent / 'selected-packet.json'; archive.store(selected_path, selected)
        mapping = [{'image_id': i['image_id'], 'role': i['role'], 'initial_stage': i['stage'], 'selected_stage': i['stage'], 'native_sha256': i['views']['native']['sha256']} for i in packet['images']]
        reuse = {'initial_packet': archive.access.pin(packet_path), 'initial_summary': summary_pin, 'retained_critics': retained,
                 'mapping': mapping, 'low_or_na_gates_retained': True, 'context_sha256': prep.value_sha(prep.context(packet))}
        reuse_path = packet_path.parent / 'reuse.json'; archive.store(reuse_path, reuse)
        result = audit.audit_reuse(selected_path, reuse_path, access=archive.access)
        self.assertEqual(result['gate'], 'PASS', result)
        self.assertEqual(result['profiles']['editorial']['bindings']['raw_observations'], retained['editorial']['compact_observations'])
        raw, _ = archive.access.load(retained['editorial']['compact_observations']['path'])
        self.assertEqual(raw['wave'], 'initial')
        reuse['retained_critics']['editorial'].pop('compact_observations')
        archive.store(reuse_path, reuse)
        self.assertEqual(audit.audit_reuse(selected_path, reuse_path, access=archive.access)['gate'], 'NA')


if __name__ == '__main__':
    unittest.main()
