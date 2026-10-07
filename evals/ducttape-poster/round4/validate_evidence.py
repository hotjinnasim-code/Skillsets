#!/usr/bin/env python3
"""Read-only, standard-library round4 file/call audit; no visual-quality claims."""
import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

FILES = {'SKILL.md', 'agents/openai.yaml', 'references/art-direction.md',
         'references/evaluation-loop.md', 'references/parallel-production.md',
         'references/visual-research.md'}
ROLES = {f'G{i:02}' for i in range(1, 6)} | {'C01', 'C02', 'P01', 'P02',
         'N01', 'N02', 'H01', 'H02', 'H03'}
HISTORY_SHA = '0c243b3488d10bdb3d70bf6c3963319313e7998a18cdb3315d3c9b891846ec6a'
COUNT_KEYS = ('native_image_call_count', 'native_image_calls', 'call_count',
              'native_image_call_count_this_stage', 'native_image_calls_in_this_wave',
              'native_image_calls_this_assignment', 'native_image_calls_this_repair',
              'native_image_call_count_this_correction', 'native_call_count_this_run',
              'native_call_count', 'image_calls')
PATHS = {
    'source': ('source_path', 'source_generated_path', 'tool_original_path',
               'native_tool_original_path', 'tool_return_path', 'native_source_path'),
    'original': ('original_copy_path', 'native_preserved_path', 'preserved_original_path',
                 'native_original_copy_path', 'native_original_path', 'original_path'),
    'final': ('final_path', 'selected_final_path', 'selected_candidate_path', 'final_native'),
}
HASHES = {
    'source': ('source_sha256', 'tool_original_sha256', 'native_original_sha256'),
    'original': ('original_copy_sha256', 'native_original_copy_sha256', 'original_sha256'),
    'final': ('final_sha256',),
}


def dimensions(value):
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return list(value) if all(type(n) is int and n > 0 for n in value) else None
    if isinstance(value, dict):
        for a, b in [('width', 'height'), ('native_width', 'native_height')]:
            if a in value and b in value:
                return dimensions([value[a], value[b]])
        for key in ('native_dimensions', 'output_dimensions', 'dimensions', 'final_dimensions', 'native'):
            if key in value:
                found = dimensions(value[key])
                if found:
                    return found
    return None


def image_size(data):
    if data[:8] == b'\x89PNG\r\n\x1a\n' and data[12:16] == b'IHDR' and len(data) >= 33:
        return list(struct.unpack('>II', data[16:24]))
    if data[:2] == b'\xff\xd8':
        i = 2
        while i < len(data):
            if data[i] != 255:
                i += 1
                continue
            while i < len(data) and data[i] == 255:
                i += 1
            marker = data[i]; i += 1
            if marker in (0, 1, 216) or 208 <= marker <= 215:
                continue
            length = int.from_bytes(data[i:i+2], 'big')
            if length < 2:
                break
            if marker in {192, 193, 194, 195, 197, 198, 199, 201, 202, 203, 205, 206, 207}:
                h, w = struct.unpack('>HH', data[i+3:i+7])
                return [w, h]
            i += length
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        kind = data[12:16]
        if kind == b'VP8X' and len(data) >= 30:
            return [1 + int.from_bytes(data[24:27], 'little'), 1 + int.from_bytes(data[27:30], 'little')]
        if kind == b'VP8L' and data[20:21] == b'\x2f':
            bits = int.from_bytes(data[21:25], 'little')
            return [(bits & 16383) + 1, ((bits >> 14) & 16383) + 1]
        if kind == b'VP8 ' and data[23:26] == b'\x9d\x01\x2a':
            return [int.from_bytes(data[26:28], 'little') & 16383,
                    int.from_bytes(data[28:30], 'little') & 16383]
    raise ValueError('unsupported or malformed image header (PNG/JPEG/WebP supported)')


class Audit:
    def __init__(self, args):
        self.root = args.source_root.resolve()
        self.incomplete = args.allow_incomplete
        self.errors, self.missing, self.warnings = [], [], []
        self.summary, self.cache, self.stages, self.ratios = {}, {}, {}, {}

    def check(self, ok, message):
        if not ok:
            self.errors.append(message)

    def need(self, ok, message):
        if not ok:
            self.missing.append(message)
        return bool(ok)

    @staticmethod
    def path(value, base):
        p = Path(value)
        return (p if p.is_absolute() else base / p).resolve()

    def read(self, p):
        if not self.need(p.is_file(), f'missing JSON: {p}'):
            return None
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except (OSError, ValueError) as e:
            self.errors.append(f'{p}: {e}')
            return None

    def image(self, value, base, size=None, digest=None):
        p = self.path(value, base)
        if not self.need(p.is_file(), f'missing recorded image: {p}'):
            return p, None, None
        try:
            if p not in self.cache:
                data = p.read_bytes()
                self.cache[p] = (image_size(data), hashlib.sha256(data).hexdigest())
            actual_size, actual_hash = self.cache[p]
            if size is not None:
                self.check(actual_size == size, f'dimension mismatch: {p}: {actual_size} != {size}')
            if digest is not None:
                self.check(isinstance(digest, str) and bool(re.fullmatch('[0-9a-fA-F]{64}', digest)), f'invalid SHA256: {p}')
                self.check(actual_hash == str(digest).lower(), f'SHA256 mismatch: {p}')
            return p, actual_size, actual_hash
        except (OSError, ValueError, IndexError, struct.error) as e:
            self.errors.append(f'unreadable image {p}: {e}')
            return p, None, None

    def planning(self):
        plan = self.read(self.root / 'planning/phase-plan.json')
        if isinstance(plan, dict):
            expected = {'new_native_initial_calls': 14, 'new_automatic_repairs_per_new_output_max': 2,
                        'new_phase_native_call_cap': 42, 'cumulative_round3_round4_native_call_cap': 76}
            for key, n in expected.items():
                self.check(plan.get(key) == n, f'phase plan {key} must equal {n}')
            self.check(plan.get('previous_phase', {}).get('actual_native_calls') == 34, 'historical phase total must remain 34')
        cases = self.read(self.root / 'planning/cases.json')
        if isinstance(cases, dict):
            rows = cases.get('cases', [])
            self.check(len(rows) == 6, 'cases must contain exactly six cases')
            for case in rows:
                slots = case.get('slots', [])
                self.check(case.get('expected_final_count') == len(slots), f'case count mismatch: {case.get("id")}')
                for slot in slots:
                    role = slot.get('id')
                    self.check(role not in self.ratios, f'duplicate case role: {role}')
                    a, b = map(float, slot['ratio'].split(':'))
                    self.check(a > 0 and b > 0, f'invalid ratio for {role}')
                    self.ratios[role] = a / b
            self.check(set(self.ratios) == ROLES, 'case role set must be exactly the fourteen C roles')
        frozen = self.read(self.root / 'planning/candidate-c-hashes.json')
        if isinstance(frozen, dict):
            records = frozen.get('files', frozen)
            hashes = {e['path']: e for e in records} if isinstance(records, list) else records
            self.check(set(hashes) == FILES, 'frozen manifest must name exactly six skill files')
            tree = self.root / 'candidate-c-skill'
            self.check({str(p.relative_to(tree)) for p in tree.rglob('*') if p.is_file()} == FILES,
                       'frozen C tree must contain exactly six files')
            for rel, record in hashes.items():
                if rel not in FILES:
                    continue
                p = tree / rel
                if not self.need(p.is_file(), f'missing frozen file: {p}'):
                    continue
                data = p.read_bytes()
                digest = record.get('sha256') if isinstance(record, dict) else record
                self.check(hashlib.sha256(data).hexdigest() == digest, f'frozen C hash changed: {rel}')
                if isinstance(record, dict) and 'bytes' in record:
                    self.check(len(data) == record['bytes'], f'frozen C byte count changed: {rel}')
            self.summary['frozen_files_checked'] = len(hashes)
        history = self.root.parent / 'ducttape-poster-round3/call-ledger.json'
        old = self.read(history)
        if isinstance(old, dict):
            self.check(hashlib.sha256(history.read_bytes()).hexdigest() == HISTORY_SHA,
                       'closed round3 ledger bytes changed; historical history must remain immutable')
            self.check(old.get('current_total_calls') == 34, 'round3 ledger total must remain 34')
            self.summary['historical_round3_calls'] = 34
            self.summary['historical_calls_by_role'] = {
                e['slot']: 1 + sum(a['image_calls'] for a in e['post_initial_attempts'])
                for e in old.get('candidate_slots', [])}
            self.summary['historical_prior_comparison_calls'] = old.get('prior_comparison_calls')

    def stage(self, p, role, stage):
        data = self.read(p)
        if not isinstance(data, dict):
            self.need(False, f'{p}: manifest must be a JSON object')
            return
        label = str(p.relative_to(self.root))
        identity = [data[k] for k in ('role', 'slot', 'slot_id', 'role_id', 'id') if k in data]
        if self.need(identity, f'{label}: missing role/slot identity'):
            self.check(all(v == role for v in identity), f'{label}: role identity differs from directory')
        counts = [data[k] for k in COUNT_KEYS if k in data]
        if self.need(counts, f'{label}: missing native stage call count'):
            self.check(all(type(v) is int and v == 1 for v in counts), f'{label}: stage must record exactly one native call')
        for key in ('repair_call_count', 'repair_calls', 'repair_image_call_count',
                    'repair_calls_after_this_stage', 'additional_calls', 'additional_call_count_this_run'):
            if key in data:
                self.check(data[key] == 0, f'{label}: {key} must be zero; additional calls need their own stage manifests')
        call = next((data[k] for k in ('call_input', 'actual_call_input', 'actual_tool_input', 'tool_call') if k in data), None)
        if isinstance(call, dict) and 'prompt' not in call:
            call = next((call[k] for k in ('arguments', 'input', 'args') if isinstance(call.get(k), dict)), call)
        if self.need(isinstance(call, dict), f'{label}: missing recorded call arguments'):
            allowed = {'prompt', 'transparent_background', 'referenced_image_paths', 'num_last_images_to_include'}
            self.check(set(call) <= allowed and isinstance(call.get('prompt'), str) and bool(call['prompt'].strip()),
                       f'{label}: unsupported native arguments or missing prompt')
            refs = {'referenced_image_paths', 'num_last_images_to_include'} & set(call)
            self.check(len(refs) <= 1, f'{label}: both reference mechanisms recorded')
            if stage == 'initial':
                self.check(not refs, f'{label}: fresh C initial must omit both reference arguments, including null/empty values')
        size = dimensions(data)
        self.need(size, f'{label}: missing positive native dimensions')
        native = {}
        artifacts = data.get('artifacts', {})
        for group, keys in PATHS.items():
            paths = [(data[k], None) for k in keys if isinstance(data.get(k), str)]
            for name, record in artifacts.items() if isinstance(artifacts, dict) else []:
                accepted = {'source': ('source', 'tool-original', 'tool_original'),
                            'original': ('original', 'native-original', 'native_original'), 'final': ('final',)}[group]
                if Path(name).stem in accepted and isinstance(record, dict) and isinstance(record.get('path'), str):
                    paths.append((record['path'], record))
            if not self.need(paths, f'{label}: missing explicit {group} path'):
                continue
            digests = [data[k] for k in HASHES[group] if k in data]
            common = data.get('sha256')
            if isinstance(common, str):
                digests.append(common)
            mapping = common if isinstance(common, dict) else data.get('sha256_by_path', {})
            if isinstance(mapping, dict):
                digests += [mapping[k] for k in (group, *[v for v, _ in paths]) if k in mapping]
            digests += [o['sha256'] for _, o in paths if o and 'sha256' in o]
            self.need(digests, f'{label}: missing recorded {group} SHA256')
            entries = [self.image(v, p.parent, dimensions(o) or size if o else size) for v, o in paths]
            native[group] = entries
            for _, _, actual in entries:
                for digest in digests:
                    self.check(actual is None or actual == str(digest).lower(), f'{label}: recorded {group} SHA256 mismatch')
        entries = [e for values in native.values() for e in values]
        real = [e for e in entries if e[2] is not None]
        self.check(len({e[2] for e in real}) <= 1, f'{label}: source/original/final are not byte-identical')
        if len(native) == 3:
            self.check(len({e[0] for e in entries}) >= 3, f'{label}: source, preserved original, final require three distinct paths')
            groups = [{e[0] for e in native[k]} for k in ('source', 'original', 'final')]
            self.check(all(not groups[i] & groups[j] for i in range(3) for j in range(i+1, 3)),
                       f'{label}: source/original/final semantic path groups must be distinct')
        for _, actual_size, _ in real:
            expected = self.ratios.get(role)
            if expected:
                self.check(abs(actual_size[0] / actual_size[1] / expected - 1) <= .01 + 1e-12,
                           f'{label}: requested aspect ratio differs by more than 1%')
        finals = native.get('final', [])
        self.stages[(role, stage)] = {'manifest': p.resolve(), 'finals': finals,
                                      'sources': native.get('source', [])}

    def production(self):
        prod = self.root / 'production-c'
        for p in sorted(prod.rglob('manifest.json')):
            parts = p.relative_to(prod).parts
            self.check(len(parts) in (2, 3) and parts[0] in ROLES, f'unexpected production manifest: {p}')
            if len(parts) == 2 and parts[0] in ROLES:
                self.stage(p, parts[0], 'initial')
            elif len(parts) == 3 and parts[0] in ROLES:
                self.check(parts[1] in {'repair-1', 'repair-2'}, f'unsupported repair stage: {p}')
                if parts[1] in {'repair-1', 'repair-2'}:
                    self.stage(p, parts[0], parts[1])
        for role in sorted(ROLES):
            self.need((role, 'initial') in self.stages, f'{role}: initial C manifest pending')
            if (role, 'repair-2') in self.stages:
                self.need((role, 'repair-1') in self.stages, f'{role}: repair-2 exists without repair-1')
        for p in sorted(prod.glob('*/repair-*')):
            self.check(p.name in {'repair-1', 'repair-2'}, f'new C output exceeds repair stages: {p}')
            self.need((p / 'manifest.json').exists(), f'pending repair directory: {p}')
        n = len(self.stages)
        seen_sources = set()
        for key, value in self.stages.items():
            sources = {e[0] for e in value['sources']}
            self.check(not sources & seen_sources, f'{key}: a native tool-source path was counted in multiple stages')
            seen_sources.update(sources)
        self.check(n <= 42 and 34 + n <= 76, 'new phase42 or combined76 call cap exceeded')
        by_role = {role: sum(r == role for r, _ in self.stages) for role in sorted(ROLES)}
        historical = self.summary.get('historical_calls_by_role', {})
        self.summary.update(completed_c_stage_manifests=n, completed_c_initials=sum(s == 'initial' for _, s in self.stages),
                            new_phase_cap=42, combined_recorded_calls=34+n, combined_cap=76,
                            new_calls_by_role=by_role,
                            cumulative_calls_by_role={r: historical.get(r, 0)+v for r, v in by_role.items()})

    def ledger(self):
        p = self.root / 'call-ledger.json'
        if not p.exists():
            self.warnings.append('No round4 call-ledger.json; accounting is based on stage manifests only.')
            return
        data = self.read(p)
        if not isinstance(data, dict):
            return
        for key, expected in {'historical_round3_calls': 34, 'new_phase_call_cap': 42,
                              'combined_round3_round4_call_cap': 76, 'combined_call_cap': 76,
                              'new_phase_calls': len(self.stages), 'current_phase_calls': len(self.stages),
                              'combined_total_calls': 34+len(self.stages)}.items():
            if key in data:
                self.check(data[key] == expected, f'ledger {key} != {expected}')
        rows = data.get('calls')
        if not self.need(isinstance(rows, list), 'ledger: missing calls list (cannot infer unsupported accounting schema)'):
            return
        seen = set()
        for e in rows:
            value = e.get('manifest_path')
            if not self.need(isinstance(value, str), 'ledger call: missing manifest_path'):
                continue
            mp = self.path(value, self.root)
            self.check(mp not in seen, f'ledger duplicate call: {mp}')
            seen.add(mp)
            matches = [(r, s) for (r, s), v in self.stages.items() if v['manifest'] == mp]
            self.need(matches, f'ledger call has no completed stage manifest: {mp}')
            if matches:
                role, stage = matches[0]
                self.check(e.get('slot_id', e.get('slot', e.get('role'))) == role, f'ledger role mismatch: {mp}')
                self.check(e.get('stage') in ({'initial', 'first-production', 'initial-c'} if stage == 'initial' else {stage}),
                           f'ledger stage mismatch: {mp}')
            for k in COUNT_KEYS:
                if k in e:
                    self.check(e[k] == 1, f'ledger call count must equal one: {mp}')
        self.check({v['manifest'] for v in self.stages.values()} <= seen, 'ledger omits completed stage manifest calls')

    def selection(self):
        data = self.read(self.root / 'final-selection.json')
        if not isinstance(data, dict):
            return
        rows = next((data[k] for k in ('selected', 'items', 'selections', 'finals') if k in data), None)
        if not self.need(isinstance(rows, list), 'selection: missing selected/items list'):
            return
        roles = [e.get('slot_id', e.get('slot', e.get('role', e.get('id')))) for e in rows]
        self.check(len(rows) == 14 and set(roles) == ROLES, 'final selection must contain exactly fourteen entries, one per C role')
        seen = set()
        for e, role in zip(rows, roles):
            value = next((e[k] for k in ('final_native', 'external_native_path', 'final_path', 'native_path') if k in e), None)
            digest = e.get('sha256', e.get('native_sha256', e.get('final_sha256')))
            size = dimensions(e)
            self.need(digest is not None and size is not None, f'selection {role}: missing SHA256/dimensions')
            if not self.need(isinstance(value, str), f'selection {role}: missing explicit native path'):
                continue
            path, _, actual = self.image(value, self.root, size, digest)
            self.check(path not in seen, f'selection reuses a native file: {path}')
            seen.add(path)
            matches = [a for (r, _), v in self.stages.items() if r == role for a in v['finals'] if a[0] == path]
            self.check(bool(matches), f'selection {role}: final does not belong to a recorded C stage')
            self.check(not matches or actual == matches[0][2], f'selection {role}: stage native hash differs')
        self.summary['selected_final_count'] = len(rows)

    def run(self):
        for method in (self.planning, self.production, self.ledger, self.selection):
            try:
                method()
            except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
                self.errors.append(f'{method.__name__}: malformed evidence: {e}')
        status = 'FAIL' if self.errors or (self.missing and not self.incomplete) else ('INCOMPLETE' if self.missing else 'PASS')
        return {'status': status, 'scope': 'Recorded bytes, header dimensions, ratios, frozen files and call accounting; no visual quality or exhaustive tool-history certification.',
                'summary': self.summary, 'errors': self.errors, 'missing_required_evidence': self.missing, 'warnings': self.warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--allow-incomplete', action='store_true', help='Allow missing/pending evidence; contradictions still fail')
    args = parser.parse_args()
    result = Audit(args).run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['status'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
