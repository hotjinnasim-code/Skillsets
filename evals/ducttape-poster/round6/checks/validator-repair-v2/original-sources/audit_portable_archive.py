#!/usr/bin/env python3
"""Audit confined archive bytes, complete recorded calls and exact evidence joins.

This checks recorded metadata only. It does not view or independently rescore images,
prove semantic viewing/order/authorship, or authenticate an externally signed history.
"""
from pathlib import Path, PurePosixPath, PureWindowsPath
import argparse
import collections
import datetime as dt
import hashlib
import json
import os
import struct

PROFILES = {'editorial', 'craft', 'portfolio'}
DIMS = {'content_form', 'hierarchy', 'typography', 'space', 'image_material', 'emotion_control', 'ai_slop'}
CORE = {'content_form', 'typography', 'image_material', 'ai_slop'}
STAGES = {'initial': 0, 'repair-1': 1, 'repair-2': 2}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_path(root, value):
    """Normalize source identifiers lexically, never consult the source filesystem."""
    path = PurePosixPath(str(value))
    return os.path.normpath(str(path if path.is_absolute() else PurePosixPath(root) / path))


def confined_path(root, relative):
    """Reject ambiguous, absolute, traversal and symlink paths before any file read."""
    value = str(relative)
    path = PurePosixPath(value)
    if not value or '\\' in value or path.is_absolute() or PureWindowsPath(value).is_absolute() or '..' in path.parts:
        raise ValueError('Unsafe archive-relative path: ' + value)
    candidate = root / Path(value)
    walk = root
    for part in path.parts:
        walk = walk / part
        if walk.is_symlink():
            raise ValueError('Archive symlinks are disallowed: ' + value)
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError('Archive path escaped: ' + value)
    return resolved


def png_dimensions(path):
    with Path(path).open('rb') as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Invalid PNG header: ' + str(path))
    return list(struct.unpack('>II', header[16:24]))


def timestamp(value):
    result = dt.datetime.fromisoformat(value.replace(' UTC', '+00:00').replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timestamp lacks timezone')
    return result.timestamp()


class ArchiveReader:
    def __init__(self, root):
        self.root = root.resolve()
        self.errors = []
        self.lookup = {}
        self.checked = set()
        self.required = {}
        self.index = self.read_relative('archive-index.json')
        for row in self.index.get('files', []):
            try:
                source = row['source_absolute']
                if not PurePosixPath(source).is_absolute() or source in self.lookup:
                    raise ValueError('Duplicate/nonabsolute indexed source: ' + str(source))
                # Confinement must precede is_file, hashes and metadata reads.
                out = confined_path(self.root, row['archive_relative'])
                if not out.is_file():
                    raise ValueError('Missing archive blob: ' + str(out))
                if digest(out) != row['sha256']:
                    raise ValueError('Archive blob byte mismatch: ' + str(out))
                self.lookup[source] = dict(row, resolved=out)
                self.checked.add(str(out))
            except (KeyError, TypeError, ValueError, OSError) as error:
                self.errors.append(str(error))
        if self.index.get('file_count') != len(self.index.get('files', [])):
            self.errors.append('Index file_count differs from files inventory')

    def read_relative(self, relative):
        try:
            return json.loads(confined_path(self.root, relative).read_text())
        except (OSError, ValueError, TypeError) as error:
            self.errors.append(str(error))
            return {}

    def require(self, source, expected=None, reason='required metadata'):
        source = source_path(self.index.get('source_root', '/'), source)
        entry = self.required.setdefault(source, {'path': source, 'expected_sha256': expected, 'reasons': []})
        if expected is not None and entry['expected_sha256'] not in (None, expected):
            self.errors.append('Conflicting required source pins: ' + source)
        if expected is not None:
            entry['expected_sha256'] = expected
        if reason not in entry['reasons']:
            entry['reasons'].append(reason)
        row = self.lookup.get(source)
        if row is None:
            self.errors.append('Unmapped required source: ' + source)
            return None
        if expected is not None and row['sha256'] != expected:
            self.errors.append('Required source pin mismatch: ' + source)
            return None
        # No source checkout or original absolute-path fallback, including on errors.
        return row['resolved']

    def document(self, source, expected=None, reason='required JSON'):
        path = self.require(source, expected, reason)
        if path is None:
            return {}
        try:
            return json.loads(path.read_text())
        except (OSError, ValueError, TypeError) as error:
            self.errors.append('Invalid archived JSON ' + str(source) + ': ' + str(error))
            return {}

    def pin(self, value, reason='pinned file'):
        return self.require(value['path'], value['sha256'], reason)


def derive_inventory(reader, evidence):
    """Derive required sources from caller records, not the index's self-listed files.

    Reader.require/document are also used by the archiver before writing its index.
    Every recorded stage is traversed, including unselected repairs and failures.
    """
    root = reader.source_root if hasattr(reader, 'source_root') else reader.index['source_root']
    plan_path = source_path(root, 'planning/phase-plan.json')
    plan = reader.document(plan_path, reason='frozen phase plan')
    calls_pin = evidence['call_validation']
    calls = reader.document(calls_pin['path'], calls_pin['sha256'], 'closed native call inventory')
    registry_pin = evidence.get('production_registry')
    if registry_pin is None:
        reader.errors.append('Missing exact production_registry pin')
        registry = {}
    else:
        registry = reader.document(registry_pin['path'], registry_pin['sha256'], 'closed production staffing and selection registry')
    reader.require(source_path(root, 'planning/skill-freeze.json'), reason='frozen skill inventory')
    for key in ('cases', 'directions'):
        if key in plan:
            reader.pin(plan[key], 'frozen ' + key)
    for pin in plan.get('frozen_skill_files', []) + plan.get('prior_closed_records', []):
        reader.require(source_path(root, pin['path']), pin['sha256'], 'frozen/prior closed source')
    outcomes = {}
    selections = {}
    for record in calls.get('records', []):
        m = reader.document(record['outcome_path'], record['outcome_sha256'], 'recorded call outcome, including unused/failure')
        outcomes[(record['role'], record['stage'])] = (record, m)
        folder = str(PurePosixPath(record['outcome_path']).parent)
        for key, name in [('call_input_path', 'call-input.json'), ('precall_plan_path', 'pre-call.json')]:
            reader.require(m.get(key, source_path(folder, name)), reason='all-stage ' + name)
        reader.require(source_path(folder, 'prompt.txt'), reason='all-stage literal prompt')
        if record.get('kind') == 'returned native':
            for field in ('tool_source', 'original', 'final'):
                if field in m:
                    reader.pin(m[field], 'all-stage exact native ' + field)
            for key, q in m.get('qa_views', {}).items():
                reader.pin(q, 'all-stage QA ' + key)
            reader.require(source_path(folder, 'inspection.json'), reason='all returned-stage manual inspection')
            if record.get('stage') != 'initial':
                reader.require(source_path(folder, 'parent-comparison.json'), reason='all repair-stage parent comparison')
        elif record.get('kind') == 'failed native attempt':
            # The failed outcome and its input/pre-call/prompt are required. There
            # is no invented native/QA/inspection for a call returning no image.
            pass
        else:
            reader.errors.append('Unknown recorded call outcome kind: ' + str(record.get('kind')))
    for role in calls.get('completed_selection_roles', []):
        path = source_path(root, 'production/' + role + '/selection.json')
        selections[role] = reader.document(path, reason='all closed ordinary selections')
    closures = {}
    for cid in evidence.get('sets', {}):
        pin = evidence.get('closure_refs', {}).get(cid)
        if pin is None:
            reader.errors.append('Missing exact closure_refs pin: ' + cid)
            path = source_path(root, 'planning/' + cid + '-ordinary-closed.json')
            closure = reader.document(path, reason='case closure without declared pin')
        else:
            closure = reader.document(pin['path'], pin['sha256'], 'ordinary whole-case closure')
        closures[cid] = closure
        for key in ('first_selection', 'final_selection', 'root_inspection'):
            if key in closure:
                reader.pin(closure[key], 'sealed ' + key)
    summaries = {}
    for label, ref in evidence.get('summary_refs', {}).items():
        if ref.get('available') is False:
            continue  # explicit terminal missing-review record, never fabricated
        summary = reader.document(ref['path'], ref['sha256'], 'first/final exact summary')
        summaries[label] = summary
        for pin in summary.get('source_pin_checks', []):
            reader.require(pin['path'], pin['expected_sha256'], 'summary source/packet pin')
        for proc in summary.get('review_procedure', {}).values():
            for key, hkey in [('raw_report', 'raw_report_sha256'), ('raw_markdown', 'raw_markdown_sha256'), ('preflight', 'preflight_sha256')]:
                if key in proc:
                    reader.require(proc[key], proc[hkey], 'preserved raw review ' + key)
            for key in ('cli_completion', 'cli_launch', 'cli_trace'):
                if key in proc:
                    reader.pin(proc[key], 'review CLI provenance ' + key)
            if 'cli_completion' in proc:
                completion = reader.document(proc['cli_completion']['path'], proc['cli_completion']['sha256'], 'CLI completion')
                for pin in completion.get('reports', {}).values():
                    reader.pin(pin, 'all emitted CLI reports, including invalid assignments')
                for key in ('prompt', 'trace', 'stderr'):
                    if key in completion:
                        reader.pin(completion[key], 'CLI ' + key)
    # Entire caller-dispatched assignments, not only accepted profiles. Existing
    # raw files are additionally inventoried by the archiver under raw_sources.
    dispatch_path = source_path(root, 'cli-reviews/dispatch-plan.json')
    has_assignments = any(ref.get('available') is not False for ref in evidence.get('summary_refs', {}).values())
    if has_assignments or dispatch_path in getattr(reader, 'lookup', {}) or getattr(reader, 'exists', lambda _: False)(dispatch_path):
        dispatch = reader.document(dispatch_path, reason='complete CLI dispatch inventory')
        all_path = source_path(root, 'cli-reviews/all-completed.json')
        if has_assignments or all_path in getattr(reader, 'lookup', {}) or getattr(reader, 'exists', lambda _: False)(all_path):
            completed = reader.document(all_path, reason='complete CLI completion inventory')
            for result in completed.get('results', []):
                for pin in result.get('reports', {}).values():
                    reader.pin(pin, 'all raw completion reports')
                for key in ('prompt', 'trace', 'stderr'):
                    if key in result:
                        reader.pin(result[key], 'all CLI completion ' + key)
        for job in dispatch.get('jobs', []):
            folder = source_path(root, 'cli-reviews/' + job['wave'] + '/' + job['profile'])
            for name in ('launch.json', 'completion.json', 'trace.jsonl', 'prompt.txt', 'stderr.log'):
                path = source_path(folder, name)
                if has_assignments or path in getattr(reader, 'lookup', {}) or getattr(reader, 'exists', lambda _: False)(path):
                    reader.require(path, reason='caller assignment artifact')
    for image in evidence.get('images', {}).values():
        if image.get('ordinary_selection'):
            reader.pin(image['ordinary_selection'], 'evidence ordinary selection pin')
        for key in ('binding', 'initial_binding'):
            b = image.get(key)
            if not b:
                continue
            reader.require(b['source_native'], b['native_sha256'], 'selected/initial binding native')
            reader.require(b['source_manifest'], b['source_manifest_sha256'], 'selected/initial binding manifest')
            for pin in b.get('views', {}).values():
                reader.pin(pin, 'selected/initial binding view')
        for key in ('reviewers', 'initial_reviewers'):
            for obs in image.get(key, []):
                reader.require(obs['raw_path'], obs['raw_sha256'], 'exact raw image observation')
    for item in evidence.get('sets', {}).values():
        for key in ('initial_reviewers', 'final_reviewers'):
            for obs in item.get(key, []):
                reader.require(obs['raw_path'], obs['raw_sha256'], 'exact raw set observation')
    return dict(plan=plan, calls=calls, outcomes=outcomes, selections=selections, closures=closures, summaries=summaries, registry=registry)


def audit_archive(root):
    reader = ArchiveReader(root)
    evidence_errors = []
    need = lambda ok, msg: reader.errors.append(msg) if not ok else None
    eneed = lambda ok, msg: evidence_errors.append(msg) if not ok else None
    e = reader.document(source_path(reader.index.get('source_root', '/'), 'planning/final-evidence.json'), reason='terminal combined evidence')
    if not reader.index or not e:
        return dict(status='FAIL', archive_byte_integrity='FAIL', errors=reader.errors), 1
    try:
        graph = derive_inventory(reader, e)
        calls, plan = graph['calls'], graph['plan']
        need(reader.index.get('schema_version') == 2, 'Caller-inventory archive schema_version 2 required')
        need(reader.index.get('source_commit') == e.get('source_commit') == plan.get('source_commit'), 'Frozen source commit metadata differs')
        need(len(plan.get('frozen_skill_files', [])) == 6, 'Six frozen skill pins required')
        freeze = reader.document(source_path(reader.index['source_root'], 'planning/skill-freeze.json'), reason='exact frozen skill inventory')
        need(freeze.get('frozen_skill_files') == plan.get('frozen_skill_files'), 'Frozen skill inventory differs from phase plan')
        cases = reader.document(plan['cases']['path'], plan['cases']['sha256'], 'frozen scheduled cases')
        scheduled = {slot['id']: case['id'] for case in cases.get('cases', []) for slot in case.get('slots', [])}
        need(len(cases.get('cases', [])) == 4 and len(scheduled) == 20 and all(len(case.get('slots', [])) == 5 for case in cases.get('cases', [])), 'Frozen four/five/20 schedule differs')
        need(calls.get('status') == 'PASS' and calls.get('call_phase') == 'CLOSED', 'Native call history is not closed PASS')
        records = calls.get('records', [])
        need(len(records) == calls.get('recorded_attempts') <= 60, 'Reconstructed call count/cap differs')
        need(calls.get('new_R6_attempt_ceiling') == 60 and calls.get('unused_new_R6_attempts_retired') == 60 - len(records), 'Closed retired-attempt cap differs')
        need(calls.get('prior_R5_closed_recorded') == 128 and calls.get('prior_R5_retirement_unchanged') is True, 'Prior closed history differs')
        need(calls.get('no_further_native_generation') is True and calls.get('all20_ordinary_selections_closed_before_external_critics') is True, 'Closed native phase attestations absent')
        need(len(e.get('images', {})) == 20 and len(e.get('sets', {})) == 4, '20-image/four-context scope missing')
        counts = collections.Counter(x['role'] for x in records)
        need(dict(counts) == calls.get('role_counts') and len(counts) == 20, 'Reconstructed role counts differ')
        need(set(counts) == set(scheduled) == set(calls.get('completed_selection_roles', [])) == set(e.get('images', {})), 'Caller/scheduled/ordinary/evidence role coverage differs')
        need(all(1 <= n <= 3 for n in counts.values()), 'Own-stage cap exceeded')
        registry = graph['registry']
        registered = {x.get('role'): x for x in registry.get('roles', [])}
        need(len(registry.get('roles', [])) == len(registered) == 20 and set(registered) == set(scheduled), 'Closed staffing registry exact20 role coverage differs')
        need(registry.get('logical_roles') == 20 and registry.get('per_case') == 5 and registry.get('recorded_native_call_peak') == calls.get('actual_recorded_interval_peak'), 'Closed staffing registry count/peak differs')
        for role, row in registered.items():
            need(e['images'].get(role, {}).get('ordinary_selection') == {'path': row.get('selection'), 'sha256': row.get('sha256')}, role + ' registry/evidence ordinary selection pin differs')
            need(row.get('native_calls') == counts[role] and row.get('own_corrections') == counts[role]-1, role + ' staffing registry call counts differ')
        resumed = {role for role,row in registered.items() if row.get('resumed_worker_name')}
        need(resumed == set(registry.get('fresh_context_exception_roles', [])), 'Closed staffing registry resumed-role disclosure differs')
        need(len(graph['outcomes']) == len(records), 'Duplicate role/stage outcomes')
        native = set()
        events = []
        prompt_file_adapters = []
        for (role, stage), (rec, m) in graph['outcomes'].items():
            label = role + '/' + stage
            k = STAGES.get(stage)
            need(k is not None and m.get('role') == role and m.get('case_id') == rec['case_id'] and m.get('stage') == stage, label + ' outcome identity differs')
            need(rec['case_id'] == scheduled.get(role), label + ' outcome case differs from frozen schedule')
            need(m.get('own_correction_number') == k and m.get('native_call_number_for_role') == k + 1, label + ' native call numbering differs')
            folder = str(PurePosixPath(rec['outcome_path']).parent)
            args = reader.document(m['call_input_path'], reason='stage exact call input')
            pre = reader.document(m['precall_plan_path'], reason='stage precall lineage')
            need(m.get('call_input') == args, label + ' embedded/saved call input differs')
            need(m['call_input_path'] == source_path(folder, 'call-input.json') and m['precall_plan_path'] == source_path(folder, 'pre-call.json'), label + ' stage input/precall path differs')
            prompt_path = reader.require(source_path(folder, 'prompt.txt'), reason='stage prompt bytes')
            if prompt_path:
                text = prompt_path.read_text()
                exact = text == args.get('prompt')
                terminal_lf = isinstance(args.get('prompt'), str) and text == args['prompt'] + '\n'
                need(exact or terminal_lf, label + ' prompt.txt differs from actual saved input beyond one terminal LF')
                if terminal_lf:
                    prompt_file_adapters.append({'role': role, 'stage': stage, 'adapter': 'One additional terminal LF in text-file wrapper only; saved tool-input prompt remains exact and raw bytes unchanged.'})
            need(all(pre.get(key) == m.get(key) for key in ('role', 'case_id', 'stage', 'own_correction_number')), label + ' precall identity differs')
            need(pre.get('phase_plan') == {'path': source_path(reader.index['source_root'], 'planning/phase-plan.json'), 'sha256': reader.lookup[source_path(reader.index['source_root'], 'planning/phase-plan.json')]['sha256']}, label + ' frozen phase plan pin differs')
            for key in ('cases', 'directions'):
                need(pre.get(key) == plan.get(key), label + ' frozen ' + key + ' differs')
            normalized = lambda pins: sorted((source_path(reader.index['source_root'], p['path']), p['sha256']) for p in pins)
            need(normalized(pre.get('frozen_skill_files', [])) == normalized(plan.get('frozen_skill_files', [])), label + ' six frozen pins differ')
            start, end = timestamp(m['started_at_utc']), timestamp(m['completed_at_utc'])
            need(start <= end and start == rec.get('start') and end == rec.get('end'), label + ' recorded interval differs')
            events.extend([(start, 1), (end, -1)])
            previous = graph['outcomes'].get((role, 'initial' if k == 1 else 'repair-1')) if k else None
            if k:
                need(previous is not None, label + ' skipped immediate own stage')
                if previous:
                    need(previous[0]['end'] <= start, label + ' own stages overlap')
            parent = previous[1].get('final') if previous else None
            need(pre.get('parent_native') == (parent['path'] if parent else None) and pre.get('parent_sha256') == (parent['sha256'] if parent else None), label + ' immediate own parent pin differs')
            need(args.get('transparent_background') is False and 'num_last_images_to_include' not in args, label + ' opaque/local-reference policy differs')
            if 'referenced_image_paths' in args:
                need(parent is not None and args['referenced_image_paths'] == [parent['path']], label + ' edit references differ from immediate parent')
            if rec['kind'] == 'failed native attempt':
                need(PurePosixPath(rec['outcome_path']).name == 'failure.json' and m.get('tool_attempted') is True and isinstance(m.get('error'), str) and bool(m.get('error')), label + ' failed outcome metadata absent')
                continue
            need(rec['manifest'] == rec['outcome_path'] and rec['manifest_sha256'] == rec['outcome_sha256'], label + ' manifest/outcome pin differs')
            hashes = [m[f]['sha256'] for f in ('tool_source', 'original', 'final')]
            need(len(set(hashes)) == 1 and hashes[0] == rec.get('native_sha256'), label + ' native source/original/final byte inventory differs')
            native.add(hashes[0])
            for field in ('original', 'final'):
                need(m[field]['path'] == source_path(folder, field + '.png'), label + ' canonical ' + field + ' path differs')
            path = reader.pin(m['final'], 'all-stage native dimensions')
            dims = png_dimensions(path) if path else None
            need(dims == rec.get('dimensions') == [m.get('width'), m.get('height')], label + ' native dimensions differ')
            need(set(m.get('qa_views', {})) == {'usage720', 'thumbnail320'}, label + ' all-stage QA views missing')
            for key, q in m.get('qa_views', {}).items():
                path = reader.pin(q, 'all-stage QA dimensions')
                expected = [720, round(m['height'] * 720 / m['width'])] if key == 'usage720' else [round(m['width'] * 320 / max(m['width'], m['height'])), round(m['height'] * 320 / max(m['width'], m['height']))]
                need(q['path'] == source_path(folder, key + '.png') and path is not None and png_dimensions(path) == [q['width'], q['height']] == expected, label + ' QA path/dimensions differ: ' + key)
        active = peak = 0
        for _, delta in sorted(events):
            active += delta
            peak = max(peak, active)
        need(peak <= 3 and peak == calls.get('actual_recorded_interval_peak'), 'Recorded native interval peak differs/exceeds cap')
        need(sorted(native) == reader.index.get('unique_native_hashes'), 'Reconstructed unique native inventory differs from index')
        need(reader.index.get('recorded_attempts') == len(records) and reader.index.get('successful_native_attempts') == sum(x['kind'] == 'returned native' for x in records) and reader.index.get('failed_native_attempts') == sum(x['kind'] == 'failed native attempt' for x in records), 'Index outcome counts differ from caller inventory')
        for pin in plan.get('prior_closed_records', []):
            prior = reader.document(pin['path'], pin['sha256'], 'closed prior history metadata')
            need(prior.get('whole_recorded') == 128 and prior.get('call_phases') == 'ALL_CLOSED', 'Pinned prior closed inventory differs')
        for role, selection in graph['selections'].items():
            stage = selection.get('selected_stage')
            pair = graph['outcomes'].get((role, stage))
            need(pair is not None and pair[0]['kind'] == 'returned native', role + ' ordinary selection lacks returned stage')
            if not pair:
                continue
            m = pair[1]
            need(selection.get('role') == role and selection.get('case_id') == m.get('case_id') and selection.get('selected_native') == m['final']['path'] and selection.get('sha256') == m['final']['sha256'] and [selection.get('width'), selection.get('height')] == [m['width'], m['height']], role + ' ordinary selection/native join differs')
            need(selection.get('manifest', selection.get('manifest_path')) == pair[0]['outcome_path'], role + ' ordinary selection manifest differs')
            need(not ('manifest' in selection and 'manifest_path' in selection) or selection['manifest'] == selection['manifest_path'], role + ' conflicting ordinary manifest aliases')
            need(selection.get('call_count') == counts[role] and selection.get('own_corrections') == counts[role] - 1, role + ' ordinary selection call counts differ')
            listed = {source_path(reader.index['source_root'], x['path'] if isinstance(x, dict) else x) for x in selection.get('all_stage_paths', [])}
            expected = {str(PurePosixPath(rec['outcome_path']).parent) for (r, _), (rec, _) in graph['outcomes'].items() if r == role}
            need(listed == expected, role + ' ordinary selection all-stage coverage differs')
        observations = 0
        quality = []
        sessions = {}
        session_assignments = {}
        for label, summary in graph['summaries'].items():
            cid, phase = label.split('/')
            closure = graph['closures'][cid]
            wave = closure['review_waves'][phase]
            eneed(summary.get('wave') == wave == e['summary_refs'][label].get('wave'), label + ' summary/closure wave differs')
            selection_pin = closure['first_selection' if phase == 'first' else 'final_selection']
            # With exact whole-set reuse the original summary pins FIRST selection.
            expected_selection = closure['first_selection'] if phase == 'final' and not closure['physical_set_changed'] else selection_pin
            declared = [x for x in summary.get('source_pin_checks', []) if x.get('kind') == 'selection']
            eneed(len(declared) == 1 and declared[0]['path'] == expected_selection['path'] and declared[0]['expected_sha256'] == expected_selection['sha256'], label + ' summary selection pin differs from closure')
            procmap = summary.get('review_procedure', {})
            accepted = summary.get('recorded_evidence_integrity') == 'PASS'
            if accepted:
                eneed(set(procmap) == PROFILES, label + ' exact critic assignment coverage differs')
            sessions[label] = set()
            for profile, proc in procmap.items():
                try:
                    completion = reader.document(proc['cli_completion']['path'], proc['cli_completion']['sha256'], 'CLI acceptance completion')
                    launch = reader.document(proc['cli_launch']['path'], proc['cli_launch']['sha256'], 'CLI acceptance launch')
                    trace = reader.pin(proc['cli_trace'], 'CLI acceptance trace')
                    eneed(completion.get('wave') == launch.get('wave') == wave and completion.get('profile') == launch.get('profile') == profile, label + '/' + profile + ' assignment identity differs')
                    for key in ('started_utc', 'argv', 'prompt', 'input_pins', 'fresh_session'):
                        eneed(completion.get(key) == launch.get(key), label + '/' + profile + ' launch/completion differs: ' + key)
                    eneed(completion.get('trace') == proc['cli_trace'], label + '/' + profile + ' completion trace pin differs')
                    trace_ids = []
                    if trace:
                        for line in trace.read_text().splitlines():
                            item = json.loads(line)
                            if item.get('type') == 'thread.started':
                                trace_ids.append(item.get('thread_id'))
                    eneed(len(trace_ids) == 1 and trace_ids[0] == proc.get('cli_session_id') and bool(trace_ids[0]), label + '/' + profile + ' trace session identity differs')
                    if len(trace_ids) == 1:
                        sessions[label].add(trace_ids[0])
                        assignment = (wave, profile)
                        eneed(session_assignments.get(trace_ids[0], assignment) == assignment, label + '/' + profile + ' session reused across distinct assignments')
                        session_assignments[trace_ids[0]] = assignment
                    argv = launch.get('argv', [])
                    eneed('exec' in argv and '--ephemeral' in argv and '--no-daemon' in argv and not {'resume', 'fork'} & set(argv) and launch.get('fresh_session') is True, label + '/' + profile + ' fresh launch flags differ')
                    eneed(completion.get('input_pins_unchanged') is True, label + '/' + profile + ' CLI input pins changed')
                    # Input pins name exactly the three sealed packet files.
                    inputchecks = {PurePosixPath(x['path']).name: x['expected_sha256'] for x in summary.get('source_pin_checks', []) if x.get('kind') == 'sealed packet file'}
                    eneed(launch.get('input_pins') == inputchecks and set(inputchecks) == {'packet.json', 'preflight.json', 'review-protocol.md'}, label + '/' + profile + ' launch/summary packet input pins differ')
                    for key, hkey in [('raw_report', 'raw_report_sha256'), ('raw_markdown', 'raw_markdown_sha256'), ('preflight', 'preflight_sha256')]:
                        expected = {'path': proc[key], 'sha256': proc[hkey]}
                        eneed(completion.get('reports', {}).get(PurePosixPath(proc[key]).name) == expected, label + '/' + profile + ' emitted raw report pin differs: ' + key)
                    if accepted:
                        eneed(completion.get('exit_code') == 0 and proc.get('cli_assignment_valid') is True and proc.get('order_compliant') is True and proc.get('preflight_order_compliant') is True, label + '/' + profile + ' accepted assignment has invalid procedure')
                except (KeyError, TypeError, ValueError, OSError) as error:
                    evidence_errors.append(label + '/' + profile + ' CLI provenance missing/invalid: ' + str(error))
            if accepted:
                eneed(len(sessions[label]) == 3, label + ' three distinct CLI sessions absent')
                if 'accepted_session_ids' in e['summary_refs'][label]:
                    eneed(set(e['summary_refs'][label]['accepted_session_ids']) == sessions[label], label + ' declared accepted sessions differ from CLI traces')
        for cid, group in e['sets'].items():
            closure = graph['closures'][cid]
            rows = {}
            for phase in ('first', 'final'):
                pin = closure[phase + '_selection']
                doc = reader.document(pin['path'], pin['sha256'], 'exact sealed selection rows')
                selected = doc.get('selected', [])
                rows[phase] = {x['role']: x for x in selected}
                eneed(len(selected) == len(rows[phase]) == 5 and set(rows[phase]) == set(group['roles']), cid + '/' + phase + ' complete five-role selection differs')
            changed = {k: v.get('sha256') for k, v in rows['first'].items()} != {k: v.get('sha256') for k, v in rows['final'].items()}
            eneed(changed == closure.get('physical_set_changed') == group.get('physical_set_changed'), cid + ' full five-role SHA change decision differs')
            waves = closure['review_waves']
            eneed((waves['first'] != waves['final']) == changed, cid + ' changed/reused complete review wave differs')
            if changed:
                eneed(sessions.get(cid + '/first', set()).isdisjoint(sessions.get(cid + '/final', set())), cid + ' changed case reuses a CLI session')
            else:
                firstref, finalref = e['summary_refs'][cid + '/first'], e['summary_refs'][cid + '/final']
                eneed(firstref.get('path') == finalref.get('path') and firstref.get('sha256') == finalref.get('sha256') and finalref.get('reuse_complete_initial_three') is True, cid + ' unchanged full set lacks exact summary reuse')
            for phase, skey, bkey, okey in [('first', 'initial_selection', 'initial_binding', 'initial_reviewers'), ('final', 'selected', 'binding', 'reviewers')]:
                ref = e['summary_refs'][cid + '/' + phase]
                summary = graph['summaries'].get(cid + '/' + phase, {})
                accepted = ref.get('accepted', summary.get('recorded_evidence_integrity') == 'PASS')
                expected_ids = set()
                for role in group['roles']:
                    image = e['images'][role]
                    row = rows[phase].get(role)
                    b = image.get(bkey)
                    eneed(image.get(skey) == row, role + '/' + phase + ' sealed/evidence selection row differs')
                    if not row or not b:
                        eneed(image.get('initial_image_gate' if phase == 'first' else 'final_image_gate') == 'NOT_ASSESSABLE', role + '/' + phase + ' unsupported missing binding claims a visual result')
                        continue
                    eneed(row['role'] == b.get('role') and row['case_id'] == b.get('case_id') == cid and row['stage'] == b.get('stage') and row['final_native'] == b.get('source_native') and row['sha256'] == b.get('native_sha256') and row['manifest'] == b.get('source_manifest') and row['manifest_sha256'] == b.get('source_manifest_sha256'), role + '/' + phase + ' selection/binding native/manifest join differs')
                    m = reader.document(b['source_manifest'], b['source_manifest_sha256'], 'bound native manifest')
                    eneed(m.get('role') == role and m.get('case_id') == cid and m.get('stage') == row['stage'] and m.get('final') == {'path': row['final_native'], 'sha256': row['sha256']} and [m.get('width'), m.get('height')] == [row['width'], row['height']], role + '/' + phase + ' selected row/manifest identity differs')
                    if phase == 'final':
                        ordinary = graph['selections'].get(role, {})
                        eneed(ordinary.get('selected_stage') == row['stage'] and ordinary.get('selected_native') == row['final_native'] and ordinary.get('sha256') == row['sha256'], role + ' sealed final/ordinary selection differs')
                    eneed(set(b.get('views', {})) == {'native', 'usage720', 'thumbnail320'}, role + '/' + phase + ' three bound views absent')
                    for view, pin in b.get('views', {}).items():
                        path = reader.pin(pin, 'bound anonymous review view')
                        sourcepin = m['final'] if view == 'native' else m['qa_views'][view]
                        eneed(pin['sha256'] == sourcepin['sha256'] and path is not None and png_dimensions(path) == pin['dimensions'], role + '/' + phase + ' view differs from native/stage QA')
                    if b.get('image_id') is not None:
                        expected_ids.add(b['image_id'])
                    obs = image.get(okey, [])
                    if accepted:
                        eneed({o['profile'] for o in obs} == PROFILES and len(obs) == 3, role + '/' + phase + ' complete reviewer records absent')
                        eneed(any(x == b for x in summary.get('image_bindings', [])), role + '/' + phase + ' accepted summary binding differs')
                    else:
                        eneed(image.get('initial_image_gate' if phase == 'first' else 'final_image_gate') == 'NOT_ASSESSABLE', role + '/' + phase + ' invalid procedure claims image PASS/FAIL')
                    for o in obs:
                        raw = reader.document(o['raw_path'], o['raw_sha256'], 'raw observation preservation')
                        observations += 1
                        z = raw.get('images', {}).get(b.get('image_id'))
                        if z is None:
                            evidence_errors.append(role + '/' + phase + ' raw image observation absent')
                            continue
                        eneed(all(z.get(k) == o.get(k) for k in ('mandatory', 'scores', 'evidence', 'residuals')), role + '/' + phase + ' copied/raw image record differs')
                        proc = summary.get('review_procedure', {}).get(o['profile'], {})
                        eneed(o['raw_path'] == proc.get('raw_report') and o['raw_sha256'] == proc.get('raw_report_sha256'), role + '/' + phase + ' raw observation/procedure report differs')
                        eneed(set(z.get('scores', {})) == DIMS and all(type(v) is int and 1 <= v <= 5 for v in z.get('scores', {}).values()), role + '/' + phase + ' seven-score record differs')
                        eneed({(b['image_id'], view, pin['path']) for view, pin in b['views'].items()} <= {(v.get('image_id'), v.get('view'), v.get('path')) for v in raw.get('viewed', [])}, role + '/' + phase + ' recorded exact views missing')
                        if phase == 'final' and accepted and (z['mandatory'].get('pass') is not True or z['mandatory'].get('use_readings', {}).get('all_required_copy_legible_at720') is not True or any(z['scores'].get(k, 0) < 4 for k in CORE)):
                            quality.append(role + '/' + o['profile'])
                setobs = group.get('initial_reviewers' if phase == 'first' else 'final_reviewers', [])
                if accepted:
                    eneed(len(setobs) == 3 and {o['profile'] for o in setobs} == PROFILES, cid + '/' + phase + ' three whole-case reviews absent')
                for o in setobs:
                    raw = reader.document(o['raw_path'], o['raw_sha256'], 'raw whole-set observation')
                    z = raw.get('sets', {}).get(cid, {})
                    eneed(len(z.get('members', [])) == 5 and set(z.get('members', [])) == expected_ids, cid + '/' + phase + ' complete five-member raw set differs')
                    eneed(all(z.get(k) == o.get(k) for k in ('members', 'diversity', 'closest_pair', 'evidence', 'residuals')), cid + '/' + phase + ' copied/raw set record differs')
                    proc = summary.get('review_procedure', {}).get(o['profile'], {})
                    eneed(o['raw_path'] == proc.get('raw_report') and o['raw_sha256'] == proc.get('raw_report_sha256'), cid + '/' + phase + ' set observation/procedure report differs')
                    if phase == 'final' and accepted and type(o.get('diversity')) is int and o['diversity'] < 4:
                        quality.append(cid + '/' + o['profile'] + ' diversity')
        # Validate caller-derived coverage separately from all indexed extras.
        declared = reader.index.get('required_sources', [])
        declared_by_path = {x['path']: x for x in declared}
        need(len(declared_by_path) == len(declared), 'Duplicate required-source inventory rows')
        need(reader.index.get('required_source_count') == len(declared), 'Required-source inventory count differs')
        for source, required in reader.required.items():
            row = declared_by_path.get(source)
            need(row is not None and row.get('sha256') == reader.lookup.get(source, {}).get('sha256'), 'Caller-derived required source absent/different in index inventory: ' + source)
            if row and required['expected_sha256'] is not None:
                need(row.get('expected_sha256') == required['expected_sha256'], 'Caller-derived expected pin differs in index: ' + source)
        rawrows = reader.index.get('raw_sources', [])
        need(reader.index.get('raw_source_count') == len(rawrows) == len({row['path'] for row in rawrows}), 'Raw caller inventory count/uniqueness differs')
        for row in rawrows:
            reader.require(row['path'], row['sha256'], 'full caller raw-file inventory')
        evidence_only = reader.index.get('archive_mode') == 'evidence-only'
        invalid = e.get('recorded_evidence_integrity') != 'PASS' or bool(e.get('integrity_errors'))
        if invalid:
            eneed(e.get('predeclared_core_diversity_gate') == 'NOT_ASSESSABLE', 'Invalid terminal evidence lacks NOT_ASSESSABLE gate')
        elif evidence_errors:
            eneed(False, 'Declared evidence PASS contradicts reconstructed evidence joins')
        else:
            eneed(observations == 120, 'First/final 120 preserved observation records missing')
            eneed((e.get('predeclared_core_diversity_gate') == 'PASS') == (not quality and all(x.get('final_case_gate') == 'PASS' for x in e['sets'].values())), 'Declared gate contradicts preserved raw observations')
        need(not evidence_only or (invalid and e.get('predeclared_core_diversity_gate') == 'NOT_ASSESSABLE' and reader.index.get('recorded_evidence_integrity') == 'FAIL'), 'Evidence-only archive lacks explicit invalid terminal label')
        # Evidence-only permits an honestly labelled invalid review procedure;
        # it never waives a wrong native/selection/raw/session association.
        ok = not reader.errors and not evidence_errors and (evidence_only or not invalid)
        result = dict(status='PASS' if ok else 'FAIL', archive_byte_integrity='PASS' if not reader.errors else 'FAIL', evidence_binding_integrity='FAIL' if invalid or evidence_errors else 'PASS', archive_mode=reader.index.get('archive_mode'), scope='Confined portable bytes, caller-derived complete native inventory and exact recorded joins only. No source-path fallback, visual rescore, semantic view/order proof or authenticity certificate. Evidence-only PASS describes archive bytes, never review validity.', mapped_sources=len(reader.lookup), unique_files_checked=len(reader.checked), required_sources=len(reader.required), reconstructed_attempts=len(records), reconstructed_unique_native_images=len(native), image_critic_records_first_and_final=observations, final_quality_gate=e.get('predeclared_core_diversity_gate'), raw_final_mandatory_core_diversity_failures=len(quality), errors=reader.errors, evidence_errors=evidence_errors)
        result['prompt_file_adapters'] = prompt_file_adapters
        return result, 0 if ok else 1
    except (KeyError, TypeError, ValueError, OSError, struct.error) as error:
        reader.errors.append('Malformed/incomplete archive graph: ' + type(error).__name__ + ': ' + str(error))
        return dict(status='FAIL', archive_byte_integrity='FAIL', errors=reader.errors, evidence_errors=evidence_errors), 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    result, code = audit_archive(args.archive)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
