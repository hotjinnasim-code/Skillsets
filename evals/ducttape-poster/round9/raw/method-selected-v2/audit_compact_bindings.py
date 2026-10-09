#!/usr/bin/env python3
"""Read-only compact/raw/adapter/CLI binding audit; no review or image mutation."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shlex
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
ROOT = SCRIPT_ROOT if (SCRIPT_ROOT/'summarize.py').is_file() else SCRIPT_ROOT.parent
METHOD_ROOT = SCRIPT_ROOT
# The selected v2 siblings must precede the frozen ROOT v1 helpers.
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(METHOD_ROOT))
import summarize as summary_helper
_adapter_spec = importlib.util.spec_from_file_location('selected_v2_compact_critic_adapter', METHOD_ROOT/'compact_critic_adapter.py')
adapter = importlib.util.module_from_spec(_adapter_spec)
_adapter_spec.loader.exec_module(adapter)

CONTEXT_KEYS = ('case_id', 'candidate_label', 'expected_count', 'full_request', 'literal_case_sha256',
                'normalization', 'requirements', 'copy', 'review_rules', 'critic_rubric', 'ratio_policy',
                'helper_pins', 'source_assets', 'protected_layouts', 'images', 'compact_recording')


def require(value, message):
    if not value:
        raise ValueError(message)


class ByteAccess:
    """Inject reader or an explicit archive map. No original-path fallback in archive mode."""
    def __init__(self, *, reader=None, path_map=None):
        require(reader is None or path_map is None, 'Choose one explicit archive reader/map')
        self.reader = reader
        self.path_map = None if path_map is None else {self.logical(k): str(v) for k, v in path_map.items()}

    @staticmethod
    def logical(path):
        # Lexical normalization only: never consult an original-host symlink/path.
        return os.path.abspath(os.path.normpath(str(path)))

    def read_bytes(self, path):
        name = self.logical(path)
        if self.reader is not None:
            data = self.reader(name)
        elif self.path_map is not None:
            require(name in self.path_map, 'Declared pin absent from explicit archive map: ' + name)
            data = Path(self.path_map[name]).read_bytes()
        else:
            data = Path(name).read_bytes()
        require(isinstance(data, bytes), 'Injected pin reader must return exact bytes')
        return data

    def pin(self, path):
        data = self.read_bytes(path)
        return {'path': self.logical(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

    def load(self, path):
        data = self.read_bytes(path)
        return json.loads(data), {'path': self.logical(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

    def checked_pin(self, value, *, require_size=False):
        require(isinstance(value, dict) and set(('path', 'sha256')).issubset(value), 'Missing explicit byte pin')
        require(not require_size or 'bytes' in value, 'Missing pinned byte count: ' + str(value['path']))
        actual = self.pin(value['path'])
        require(actual['sha256'] == value['sha256'], 'Changed pinned bytes: ' + str(value['path']))
        if 'bytes' in value:
            require(type(value['bytes']) is int and value['bytes'] == actual['bytes'], 'Changed pinned byte count: ' + str(value['path']))
        return actual


def pin(path):
    return ByteAccess().pin(path)


def load(path):
    return ByteAccess().load(path)


def expected_outputs(profile):
    return [profile + '.observations.json', profile + '.json', profile + '.md']


def adapter_command(packet, packet_path, observations_path, output_dir):
    method = packet['compact_recording']
    return ' '.join(shlex.quote(str(x)) for x in (method['python'], method['adapter']['path'], '--packet', packet_path,
                                                 '--observations', observations_path, '--output-dir', output_dir))


def context(packet):
    return {key: packet[key] for key in CONTEXT_KEYS}


def exit_zero(value):
    if isinstance(value, dict):
        if type(value.get('exit_code')) is int and value['exit_code'] == 0:
            return True
        return any(exit_zero(item) for item in value.values())
    if isinstance(value, list):
        return any(exit_zero(item) for item in value)
    if isinstance(value, str):
        try:
            return exit_zero(json.loads(value))
        except (ValueError, TypeError):
            return bool(re.search(r'"exit_code"\s*:\s*0(?:\D|$)', value))
    return False


def adapter_trace_events(events, command):
    """Recognize completed command or literal functions.exec→exec_command events only."""
    endings = [i for i, event in enumerate(events) if event.get('type') == 'turn.completed']
    limit = max(endings) if endings else -1
    result = []
    for index, event in enumerate(events):
        if index >= limit or event.get('type') != 'item.completed':
            continue
        item = event.get('item', {})
        candidates = []
        if item.get('type') == 'command_execution' and type(item.get('exit_code')) is int and item['exit_code'] == 0:
            candidates = [item.get('command', '')]
        elif item.get('type') == 'mcp_tool_call' and item.get('tool') == 'exec' and item.get('server') == 'functions' and not item.get('error') and exit_zero(item.get('result')):
            arguments = item.get('arguments', {})
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except ValueError:
                    arguments = {}
            code = arguments.get('code', '') if isinstance(arguments, dict) else ''
            if isinstance(code, str) and 'tools.exec_command' in code:
                for match in re.finditer(r'cmd\s*:\s*("(?:\\.|[^"\\])*")', code):
                    try:
                        candidates.append(json.loads(match.group(1)))
                    except ValueError:
                        pass
        for candidate in candidates:
            try:
                observed_argv = shlex.split(candidate)
                if len(observed_argv) == 3 and Path(observed_argv[0]).name in ('zsh', 'bash', 'sh') and observed_argv[1] in ('-lc', '-c'):
                    observed_argv = shlex.split(observed_argv[2])
                if observed_argv == shlex.split(command):
                    result.append(index)
                    break
            except ValueError:
                pass
    return result


def audit_profile(packet_path, profile, folder, *, access=None):
    errors, bindings = [], {}
    access = access or ByteAccess()
    load, checked_pin = access.load, access.checked_pin
    try:
        packet, packet_pin = load(packet_path)
        require(profile in packet['critic_profiles'], 'Undeclared critic profile')
        folder = Path(access.logical(folder))
        method = packet['compact_recording']
        require(packet['wave'] == 'selected', 'Selected recording v2 is bounded to future selected reviews')
        require(method['schema_version'] == 2 and method['kind'] == 'compact_critic_observations' and method.get('pin_schema') == 'path-sha256-bytes-v2', 'Undeclared selected compact recording v2 method')
        require(method['expected_outputs'] == ['PROFILE.observations.json', 'PROFILE.json', 'PROFILE.md'], 'Recording output contract changed')
        for name, key in (('compact_critic_adapter.py', 'adapter'), ('README.md', 'method'),
                          ('compact-recording-addendum.md', 'addendum'), ('audit_compact_bindings.py', 'binding_audit'),
                          ('prepare_reviews_compact.py', 'preparer')):
            require(packet['helper_pins'][name] == method[key], 'Packet helper/method pin mismatch: ' + name)
        helper_pins = [checked_pin(item) for item in packet['helper_pins'].values()]
        require(packet['helper_pins']['summarize.py']['sha256'] == adapter.SUMMARY_SHA256, 'Declared adapter is for a different frozen summary')
        raw_path = folder / (profile + '.observations.json')
        raw, raw_pin = load(raw_path)
        exported, export_pin = load(folder / (profile + '.json'))
        md_pin = access.pin(folder / (profile + '.md'))
        bindings.update(packet=packet_pin, raw_observations=raw_pin, compatibility_json=export_pin,
                        compatibility_markdown=md_pin, adapter=method['adapter'], method=method['method'],
                        addendum=method['addendum'], binding_audit=method['binding_audit'], preparer=method['preparer'])
        for key, value in (('case_id', packet['case_id']), ('wave', packet['wave']), ('profile', profile)):
            require(raw.get(key) == value and exported.get(key) == value, 'Raw/export packet/profile/wave mismatch: ' + key)
        reproduced = adapter.export(packet, raw, packet_pin=packet_pin, raw_pin=raw_pin, adapter_pin=method['adapter'])
        require(exported == reproduced, 'Compatibility JSON is not the exact declared export of the preserved raw bytes')
        require(access.read_bytes(folder / (profile + '.md')) == adapter.markdown(reproduced).encode('utf-8'), 'Compatibility Markdown is not the deterministic export')
        rules_pin = checked_pin(packet['review_rules'])
        launch, launch_pin = load(folder / 'launch.json')
        completion, completion_pin = load(folder / 'completion.json')
        for key in ('started_utc', 'argv', 'fresh_session', 'case_id', 'wave', 'profile', 'prompt', 'input_pins'):
            require(key in launch and completion.get(key) == launch[key], 'Immutable CLI launch/completion field differs: ' + key)
        for key, expected in (('case_id', packet['case_id']), ('wave', packet['wave']), ('profile', profile)):
            require(launch.get(key) == expected, 'CLI launch identity differs: ' + key)
        require(launch.get('fresh_session') is True and summary_helper.fresh_exec_argv(launch.get('argv')), 'Actual fresh exec --ephemeral argv required; no resume/fork')
        require(type(completion.get('exit_code')) is int and completion['exit_code'] == 0 and completion.get('input_pins_unchanged') is True, 'CLI exit zero/unchanged input pins required')
        started = datetime.fromisoformat(completion['started_utc'].replace('Z', '+00:00'))
        ended = datetime.fromisoformat(completion['completed_utc'].replace('Z', '+00:00'))
        require(started.tzinfo is not None and ended.tzinfo is not None and ended >= started, 'Ordered timezone-aware CLI timestamps required')
        checked_pin(launch['prompt'])
        reports = completion.get('reports', {})
        require(set(reports) == set(expected_outputs(profile)), 'Immutable completion must pin exactly compact raw + JSON + Markdown')
        for name, expected in zip(expected_outputs(profile), (raw_pin, export_pin, md_pin)):
            require(checked_pin(reports[name]) == expected, 'Completion does not join actual report bytes: ' + name)
        job_pin = checked_pin(launch['job'])
        job, _ = load(job_pin['path'])
        require(job['expected_outputs'] == expected_outputs(profile), 'Runner job expected outputs are not exactly the three declared files')
        require(job['profile'] == profile and job['case_id'] == packet['case_id'] and job['wave'] == packet['wave'], 'Runner job identity changed')
        require(access.logical(job['output_dir']) == str(folder), 'Runner output directory changed')
        require(access.logical(job['prompt_file']) == access.logical(launch['prompt']['path']), 'Runner job/launch prompt path differs')
        input_pins = [checked_pin(item) for item in launch['input_pins']]
        actual_inputs = {(item['path'], item['sha256']) for item in input_pins}
        job_inputs = {access.logical(path) for path in job['inputs']}
        require(len(input_pins) == len(job['inputs']) and {p['path'] for p in input_pins} == job_inputs, 'Immutable job/launch input inventory differs')
        needed = [packet_pin, rules_pin, checked_pin(packet['critic_rubric']), checked_pin(packet['ratio_policy'])] + helper_pins
        for image in packet['images']:
            needed += [checked_pin(image['source_manifest'])]
            needed += [checked_pin(image['views'][view]) for view in adapter.VIEWS]
        for source in packet.get('source_assets', []):
            needed += [checked_pin({'path': source['actual_path'], 'sha256': source['sha256']}, require_size=False),
                       checked_pin({'path': source['manifest_path'], 'sha256': source['manifest_sha256']}, require_size=False)]
        for layout in packet.get('protected_layouts', []):
            needed.append(checked_pin(layout['manifest']))
        require({(p['path'], p['sha256']) for p in needed}.issubset(actual_inputs), 'Launch omits packet/rules/rubric/method/helper/exact source or view pins')
        trace_pin = checked_pin(completion['trace'])
        events = [json.loads(line) for line in access.read_bytes(trace_pin['path']).decode('utf-8').splitlines() if line.strip()]
        require(all(isinstance(event, dict) for event in events), 'Trace events must be JSON objects')
        starts = [event.get('thread_id') for event in events if event.get('type') == 'thread.started']
        require(len(starts) == 1 and isinstance(starts[0], str) and bool(starts[0]), 'Exactly one actual thread.started ID required')
        completed = sum(event.get('type') == 'turn.completed' for event in events)
        require(type(completion.get('turn_completed_count')) is int and completion['turn_completed_count'] == completed and completed >= 1, 'CLI completion count must join actual completed turns')
        require(not any(event.get('type') in ('turn.failed', 'error') for event in events), 'Actual trace contains a failed turn/error')
        require(completion.get('session_ids') == starts and exported.get('session_id') in (None, starts[0]), 'CLI/report session binding differs from actual trace')
        hits = adapter_trace_events(events, adapter_command(packet, access.logical(packet_path), raw_path, folder))
        require(bool(hits), 'No recognized successful exact adapter invocation before CLI turn completion; do not infer it from export existence')
        bindings.update(launch=launch_pin, completion=completion_pin, trace=trace_pin, job=job_pin,
                        actual_session_id=starts[0], adapter_trace_events=hits)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        errors.append(str(exc))
    return {'profile': profile, 'gate': 'NA' if errors else 'PASS', 'errors': errors, 'bindings': bindings,
            'limits': ['Checks recording bytes/bindings and recognized invocation, not design scores or semantic visual inspection.',
                       'Unrecognized trace serialization is NA; no invented command event or post-completion repair.']}


def audit(packet_path, report_dir, *, access=None):
    access = access or ByteAccess()
    packet, packet_pin = access.load(packet_path)
    profiles = packet['critic_profiles']
    require(len(profiles) == 3 and len(set(profiles)) == 3, 'Exactly three independent profiles required')
    records = {p: audit_profile(packet_path, p, Path(report_dir) / p, access=access) for p in profiles}
    sessions = [record['bindings'].get('actual_session_id') for record in records.values()]
    errors = [] if len(set(sessions)) == 3 and all(isinstance(s, str) and s for s in sessions) else ['Three unique actual trace sessions required']
    return {'kind': 'compact_recording_binding_audit', 'packet': packet_pin, 'case_id': packet['case_id'], 'wave': packet['wave'],
            'gate': 'NA' if errors or any(r['errors'] for r in records.values()) else 'PASS', 'errors': errors, 'profiles': records,
            'quality_gate_unchanged': True, 'limits': ['No image editing, scores recomputed, raw rewriting, critic replacement or gate relaxation.']}


def audit_reuse(selected_packet_path, reuse_path, *, access=None):
    access = access or ByteAccess()
    load, checked_pin = access.load, access.checked_pin
    selected, selected_pin = load(selected_packet_path)
    reuse, reuse_pin = load(reuse_path)
    errors, records = [], {}
    try:
        initial_pin, summary_pin = checked_pin(reuse['initial_packet']), checked_pin(reuse['initial_summary'])
        initial, _ = load(initial_pin['path'])
        summary, _ = load(summary_pin['path'])
        require(context(initial) == context(selected), 'Entire compact evaluation context changed; whole-case reuse forbidden')
        require(summary['raw_packet'] == initial and summary['packet']['sha256'] == initial_pin['sha256'] and summary['procedure_gate'] == 'PASS' and not summary['procedure_errors'], 'Initial summary/packet/procedure mismatch')
        n = initial['expected_count']
        require(summary['counts']['observed_image_profile_records'] == 3*n and summary['counts']['valid_integer_1_to_5_score_values'] == 21*n, 'Initial complete three-critic record/score count mismatch')
        require(set(reuse['retained_critics']) == set(initial['critic_profiles']) == set(summary['reviews']), 'Reuse must retain all three exact critics')
        sessions = []
        for profile in initial['critic_profiles']:
            retained = reuse['retained_critics'][profile]
            folder = Path(checked_pin(retained['completion'])['path']).parent
            result = audit_profile(initial_pin['path'], profile, folder, access=access)
            records[profile] = result
            require(not result['errors'], 'Retained compact raw/CLI binding invalid: ' + '; '.join(result['errors']))
            require(retained['compact_observations'] == result['bindings']['raw_observations'] and retained['compact_binding'] == result['bindings'], 'Reuse dropped or changed original compact raw pin/binding')
            for old, key in (('raw_report', 'compatibility_json'), ('launch', 'launch'), ('completion', 'completion'), ('trace', 'trace'), ('actual_session_id', 'actual_session_id')):
                require(retained[old] == result['bindings'][key], 'Retained legacy/compact provenance differs: ' + old)
            review = summary['reviews'][profile]
            require(not review['procedure_errors'] and not review['set']['errors'] and all(not r['errors'] for r in review['images'].values()), 'Initial invalid review cannot be repaired by reuse')
            exported, _ = load(result['bindings']['compatibility_json']['path'])
            require(review['raw_data'] == exported, 'Initial summary did not retain the exact compatibility export')
            sessions.append(result['bindings']['actual_session_id'])
        require(len(sessions) == 3 and len(set(sessions)) == 3, 'Reuse session independence changed')
        require(reuse['context_sha256'] == hashlib.sha256(json.dumps(context(selected), ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(), 'Reuse full-context digest differs')
        expected_map = [{'image_id': image['image_id'], 'role': image['role'], 'initial_stage': image['stage'], 'selected_stage': image['stage'], 'native_sha256': image['views']['native']['sha256']} for image in selected['images']]
        require(reuse['mapping'] == expected_map and reuse['low_or_na_gates_retained'] is True, 'Whole-member mapping or low-record preservation changed')
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        errors.append(str(exc))
    return {'kind': 'compact_whole_context_reuse_audit', 'packet': selected_pin, 'reuse': reuse_pin,
            'gate': 'NA' if errors else 'PASS', 'errors': errors, 'profiles': records,
            'limit': 'Retains original wave/raw bytes and unfavorable judgments; does not re-label initial reviews as new sessions.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', type=Path, required=True)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--report-dir', type=Path)
    mode.add_argument('--reuse', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--archive-map', type=Path, help='Explicit JSON object original absolute path -> archived file; no host-path fallback')
    args = p.parse_args()
    archive_map = None
    if args.archive_map:
        mapping = json.loads(args.archive_map.read_bytes())
        require(isinstance(mapping, dict), 'Archive map must be an explicit path object')
        archive_map = {key: str(Path(value) if Path(value).is_absolute() else args.archive_map.parent / value) for key, value in mapping.items()}
    access = ByteAccess(path_map=archive_map)
    result = audit(args.packet, args.report_dir, access=access) if args.report_dir else audit_reuse(args.packet, args.reuse, access=access)
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')
    print(json.dumps({'output': pin(args.output), 'compact_binding_gate': result['gate']}))


if __name__ == '__main__':
    main()
