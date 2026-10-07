#!/usr/bin/env python3
"""Read-only round-3 evidence checks. Does not judge pixels or generate images.

python3 evidence-validator.py --source-root ROUND3 --live-skill SKILL \
  --evidence-root REPO/evals/ducttape-poster/round3 --require-selection

External native paths resolve ONLY against source-root; preview paths resolve
ONLY against evidence-root. Manifest-relative paths resolve against that exact
manifest's parent. No basename searches, resizes, or file writes are performed.
PNG dimensions use the standard library; other image types require Pillow.
YAML parsing uses PyYAML when installed, otherwise Ruby's safe YAML parser.
"""

import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

FILES = {
    'SKILL.md', 'agents/openai.yaml', 'references/art-direction.md',
    'references/evaluation-loop.md', 'references/parallel-production.md',
    'references/visual-research.md',
}
SLOTS = {f'G{i:02}' for i in range(1, 6)} | {
    'C01', 'C02', 'P01', 'P02', 'N01', 'N02',
}
CALL_KEYS = [
    'native_image_call_count', 'native_image_calls', 'call_count',
    'native_image_call_count_this_stage', 'native_image_calls_in_this_wave',
    'native_image_calls_this_assignment', 'native_image_calls_this_repair',
    'native_image_call_count_this_correction', 'native_call_count_this_run',
]
NATIVE_KEYS = [
    'tool_original_path', 'native_tool_original_path', 'source_path',
    'original_copy_path', 'native_preserved_path', 'preserved_original_path',
    'native_original_copy_path', 'native_original_path', 'final_path',
    'selected_final_path', 'selected_candidate_path',
]


class Audit:
    def __init__(self, args):
        self.root = args.source_root.resolve()
        self.live = args.live_skill.resolve()
        self.evidence = args.evidence_root.resolve()
        self.require_selection = args.require_selection
        self.errors, self.warnings = [], []
        self.summary, self.image_cache = {}, {}
        self.claimed_images = set()
        self.production_finals = {}

    def check(self, condition, message):
        if not condition:
            self.errors.append(message)

    def path(self, value, base):
        p = Path(value)
        return p.resolve() if p.is_absolute() else (base / p).resolve()

    def read_json(self, path):
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as e:
            self.errors.append(f'{path}: {e}')
            return None

    def sha(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def image(self, value, base, dims=None, digest=None, context='image'):
        p = self.path(value, base)
        try:
            if p not in self.image_cache:
                data = p.read_bytes()
                if data[:8] == b'\x89PNG\r\n\x1a\n':
                    if len(data) < 33 or data[12:16] != b'IHDR':
                        raise ValueError('invalid PNG header')
                    size = list(struct.unpack('>II', data[16:24]))
                else:
                    from PIL import Image
                    with Image.open(p) as im:
                        size = list(im.size)
                self.image_cache[p] = (size, hashlib.sha256(data).hexdigest())
            size, actual_hash = self.image_cache[p]
            self.claimed_images.add(p)
            if dims is not None:
                self.check(size == list(dims), f'{context}: dimensions {size} != {dims}: {p}')
            if digest is not None:
                self.check(actual_hash == digest, f'{context}: SHA256 mismatch: {p}')
            return size, actual_hash
        except (OSError, ValueError, ImportError) as e:
            self.errors.append(f'{context}: unreadable image {p}: {e}')
            return None, None

    @staticmethod
    def dimensions(data):
        for key in ['output_dimensions', 'native_dimensions', 'dimensions', 'final_dimensions']:
            value = data.get(key)
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return list(value)
            if isinstance(value, dict) and 'width' in value and 'height' in value:
                return [value['width'], value['height']]
            if isinstance(value, dict) and isinstance(value.get('native'), list) and len(value['native']) == 2:
                return value['native']
        if 'width' in data and 'height' in data:
            return [data['width'], data['height']]
        if 'native_width' in data and 'native_height' in data:
            return [data['native_width'], data['native_height']]
        return None

    def recorded_paths(self, obj, base):
        """Check explicit paths and image metadata; never resolve prose as paths."""
        if isinstance(obj, list):
            for item in obj:
                self.recorded_paths(item, base)
        elif isinstance(obj, dict):
            if isinstance(obj.get('path'), str):
                p = self.path(obj['path'], base)
                if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}:
                    self.image(obj['path'], base, self.dimensions(obj), obj.get('sha256'), 'manifest artifact')
            for key, value in obj.items():
                if isinstance(value, str) and (
                    key == 'path' or key.endswith('_path') or key in {
                        'brief_source', 'brief_copy', 'skill', 'skill_reference_read',
                        'imagegen_skill', 'imagegen_reference_read', 'inspection_record', 'copy_record',
                    }
                ) and not value.startswith(('http://', 'https://')):
                    self.check(self.path(value, base).exists(), f'missing recorded path: {value} (base {base})')
                elif key == 'referenced_image_paths' and isinstance(value, list):
                    for ref in value:
                        self.image(ref, base, context='call reference')
                elif isinstance(value, (dict, list)):
                    self.recorded_paths(value, base)

    @staticmethod
    def yaml(text):
        try:
            import yaml
            return yaml.safe_load(text)
        except ImportError:
            code = 'puts JSON.generate(YAML.safe_load(STDIN.read, permitted_classes: [], aliases: false))'
            proc = subprocess.run(['ruby', '-ryaml', '-rjson', '-e', code],
                                  input=text, capture_output=True, text=True, check=True)
            return json.loads(proc.stdout)

    def skills(self):
        hashes = self.read_json(self.root / 'planning/candidate-b-hashes.json')
        if not isinstance(hashes, dict):
            return
        self.check(set(hashes) == FILES, 'frozen hash manifest is not the exact six skill files')
        trees = {'live': self.live, 'external frozen B': self.root / 'candidate-b-skill'}
        repo_snapshot = self.evidence / 'snapshots/candidate-b'
        if repo_snapshot.exists():
            trees['repository snapshot B'] = repo_snapshot
        for label, directory in trees.items():
            actual = {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}
            self.check(actual == FILES, f'{label}: file set differs from six-file manifest: {sorted(actual ^ FILES)}')
            for rel, digest in hashes.items():
                p = directory / rel
                self.check(p.exists() and self.sha(p) == digest, f'{label}: frozen SHA mismatch: {rel}')
        repo_hashes = self.evidence / 'candidate-b-hashes.json'
        if repo_hashes.exists():
            self.check(self.read_json(repo_hashes) == hashes, 'repository/external hash manifests differ')
        try:
            skill = (self.live / 'SKILL.md').read_text(encoding='utf-8')
            match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', skill, re.S)
            self.check(bool(match), 'SKILL.md frontmatter boundaries missing')
            if match:
                front = self.yaml(match.group(1))
                self.check(isinstance(front, dict) and front.get('name') == 'ducttape-poster'
                           and isinstance(front.get('description'), str) and bool(front['description']),
                           'invalid skill frontmatter name/description')
            config = self.yaml((self.live / 'agents/openai.yaml').read_text(encoding='utf-8'))
            interface = config.get('interface', {}) if isinstance(config, dict) else {}
            self.check(all(isinstance(interface.get(k), str) and interface[k] for k in
                           ['display_name', 'short_description', 'default_prompt']), 'invalid agents/openai.yaml interface')
        except (OSError, ValueError, subprocess.SubprocessError) as e:
            self.errors.append(f'YAML/frontmatter: {e}')
        links = 0
        for rel in FILES:
            if not rel.endswith('.md'):
                continue
            p = self.live / rel
            if not p.exists():
                continue
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                target = target.strip().strip('<>')
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                links += 1
                self.check((p.parent / target).exists(), f'broken local skill link: {rel} -> {target}')
        self.summary['skill_files_matched'] = len(FILES)
        self.summary['local_skill_links_checked'] = links

    def initial_calls(self):
        # These explicit manifest locations define call identity; duplicate copies are not calls.
        entries = []
        garden = self.read_json(self.root / 'garden-a/generation-log.json')
        if isinstance(garden, dict):
            self.check(garden.get('total_invocation_count') == 5, 'garden A must contain exactly five initial calls')
            self.check(garden.get('correction_invocation_count') == 0, 'garden A claims unaccounted corrections')
            for e in garden.get('entries', []):
                base = self.root / 'garden-a'
                entries.append(('G' + e['id'], e['initial_final_path'], base, e))
                dims = self.dimensions(e)
                for k in ['tool_return_path', 'raw_path', 'initial_final_path']:
                    self.image(e[k], base, dims, e.get('sha256'), 'garden A native')
                self.recorded_paths(e, base)
        for folder, prefix in [('coast-a', 'C'), ('neon-a', 'N'), ('product-a', 'P')]:
            data = self.read_json(self.root / folder / 'manifest.json')
            if not isinstance(data, dict):
                continue
            count = data.get('initial_generation_calls', data.get('initial_call_count'))
            self.check(count == 2, f'{folder}: initial call count must be two')
            self.check(data.get('correction_calls', data.get('repair_call_count')) == 0,
                       f'{folder}: unaccounted corrections')
            values = data.get('directions', data.get('poster_records', []))
            for i, e in enumerate(values, 1):
                base = self.root / folder
                entries.append((f'{prefix}{i:02}', e['initial_final_path'], base, e))
                dims = self.dimensions(e)
                for k in ['source_generated_path', 'source_path', 'raw_copy_path', 'raw_path', 'initial_final_path']:
                    if k in e:
                        digest = e.get('source_sha256', e.get('sha256_by_path', {}).get(e[k]))
                        self.image(e[k], base, dims, digest, folder + ' native')
                self.recorded_paths(e, base)
        prior = self.read_json(self.root / 'garden-prior/mapping.json')
        prior_calls = prior.get('calls', []) if isinstance(prior, dict) else []
        self.check(len(prior_calls) == 5, 'prior comparison must contain exactly five calls')
        for e in prior_calls:
            self.check(e.get('repair_count') == 0, 'prior comparison has an unaccounted repair')
            for k, hashkey in [('original_tool_path', 'sha256_original'), ('raw_path', 'sha256_raw'), ('final_path', 'sha256_final')]:
                self.image(e[k], self.root / 'garden-prior', e.get('dimensions'), e.get(hashkey), 'prior native')
        self.check({e[0] for e in entries} == SLOTS and len(entries) == 11, 'initial candidate slot set is not exactly eleven')
        self.initial_entries = {slot: self.path(path, base) for slot, path, base, _ in entries}
        self.summary['initial_candidate_native_calls'] = len(entries)
        self.summary['prior_native_calls'] = len(prior_calls)

    def production(self):
        total = 0
        manifests = sorted((self.root / 'production-b').rglob('manifest.json'))
        for p in manifests:
            data = self.read_json(p)
            if not isinstance(data, dict):
                continue
            present = [(key, data[key]) for key in CALL_KEYS if key in data]
            self.check(bool(present) and all(value == 1 for _, value in present), f'{p}: stage native call count must be exactly one')
            for key in ['repair_call_count', 'repair_calls', 'repair_image_call_count',
                        'repair_calls_after_this_stage', 'additional_calls', 'additional_call_count_this_run']:
                if key in data:
                    self.check(data[key] == 0, f'{p}: additional stage calls require separate manifest/ledger accounting ({key}={data[key]})')
            total += present[0][1] if present else 0
            self.recorded_paths(data, p.parent)
            call_input = data.get('call_input', data.get('actual_call_input'))
            allowed = {'prompt', 'transparent_background', 'referenced_image_paths', 'num_last_images_to_include'}
            self.check(isinstance(call_input, dict) and set(call_input) <= allowed
                       and isinstance(call_input.get('prompt'), str),
                       f'{p}: native call arguments differ from the current imagegen schema')
            if isinstance(call_input, dict):
                self.check(not ('referenced_image_paths' in call_input and 'num_last_images_to_include' in call_input),
                           f'{p}: mutually exclusive native reference mechanisms used together')
            dims = self.dimensions(data)
            self.check(dims is not None, f'{p}: missing native dimensions')
            source = data.get('source_path')
            self.check(isinstance(source, str), f'{p}: missing exact source_path')
            source_hash = self.image(source, p.parent, dims, data.get('source_sha256'), 'tool source')[1] if source else None
            for key in ['tool_original_sha256', 'native_original_sha256', 'original_copy_sha256',
                        'native_original_copy_sha256', 'final_sha256']:
                if key in data:
                    self.check(data[key] == source_hash, f'{p}: recorded {key} differs from native source bytes')
            native_paths = []
            for key in NATIVE_KEYS:
                if isinstance(data.get(key), str):
                    native_paths.append(self.path(data[key], p.parent))
                    self.image(data[key], p.parent, dims, source_hash, 'preserved native')
            artifacts = data.get('artifacts', {})
            for name in ['final.png', 'native-original.png', 'original.png']:
                if name in artifacts:
                    ap = artifacts[name]['path']
                    native_paths.append(self.path(ap, p.parent))
                    self.image(ap, p.parent, dims, source_hash, 'preserved native artifact')
            self.check(len(set(native_paths)) >= 3, f'{p}: missing separate tool source, preserved original, or final')
            hashes = data.get('sha256')
            if isinstance(hashes, str):
                self.check(hashes == source_hash, f'{p}: manifest native hash mismatch')
            elif isinstance(hashes, dict):
                aliases = {'tool_original': 'tool_original_path', 'original_copy': 'original_copy_path',
                           'native_original_copy': 'native_original_copy_path', 'final': 'final_path'}
                for key, digest in hashes.items():
                    target = data.get(aliases.get(key, ''), key)
                    self.image(target, p.parent, digest=digest, context='manifest hash mapping')
            # Explicit preview filenames/dimensions used by G03/G05.
            for name, size in data.get('qa_dimensions', {}).items():
                self.image(name, p.parent, self.dimensions(size), context='QA dimensions')
            for label, name in data.get('inspection_files', {}).items():
                size = self.dimensions(data.get(label + '_dimensions', {}))
                self.image(name, p.parent, size, context='QA view')
            for key in ['qa_only_copies']:
                for item in data.get(key, []) if isinstance(data.get(key), list) else []:
                    if isinstance(item, str):
                        self.image(item, p.parent, context='QA copy')
            final = p.parent / 'final.png'
            self.check(final.exists(), f'{p}: stage final.png missing')
            self.production_finals[final.resolve()] = (p, present[0][1] if present else None)
        pending = [str(p.relative_to(self.root)) for p in (self.root / 'production-b').glob('*/repair-*')
                   if p.is_dir() and not (p / 'manifest.json').exists()]
        if pending:
            self.warnings.append('Unfinalized repair directories excluded from completed call count: ' + ', '.join(pending))
        self.summary['production_b_completed_manifest_calls'] = total
        self.summary['production_b_completed_manifest_count'] = len(manifests)

    def ledger(self):
        data = self.read_json(self.root / 'call-ledger.json')
        if not isinstance(data, dict):
            return
        slots = data.get('candidate_slots', [])
        self.check(len(slots) == 11 and {e.get('slot') for e in slots} == SLOTS, 'ledger candidate slots must be exactly eleven')
        finals, budgets = set(), {}
        for e in slots:
            slot = e['slot']
            initial = self.path(e['initial'], self.root)
            self.check(initial == self.initial_entries.get(slot), f'{slot}: ledger initial path differs from original slot manifest')
            self.image(e['initial'], self.root, digest=e.get('initial_sha256'), context=slot + ' ledger initial')
            attempts = e.get('post_initial_attempts', [])
            count = sum(a.get('image_calls', 0) for a in attempts)
            limit = e.get('post_initial_limit')
            self.check(isinstance(limit, int) and 0 <= count <= limit <= 2, f'{slot}: post-initial call budget exceeded or invalid ({count}/{limit})')
            self.check([a.get('repair_or_regeneration_index') for a in attempts] == list(range(1, len(attempts) + 1)),
                       f'{slot}: retry indices are not contiguous from one')
            for a in attempts:
                self.check(a.get('image_calls') == 1, f'{slot}: each recorded native call must be one')
                p = self.path(a['external_native_path'], self.root)
                self.check(p in self.production_finals, f'{slot}: ledger attempt has no completed production manifest: {p}')
                self.check(p not in finals, f'{slot}: native call path counted twice: {p}')
                finals.add(p)
                self.image(a['external_native_path'], self.root, digest=a.get('sha256'), context=slot + ' ledger attempt')
                self.check(p.is_relative_to(self.root / 'production-b' / slot), f'{slot}: ledger refers to another slot')
            budgets[slot] = count
        self.check(finals == set(self.production_finals), 'ledger and completed production manifests differ; unrecorded/orphan native call')
        actual = (self.summary.get('initial_candidate_native_calls', 0) + self.summary.get('prior_native_calls', 0)
                  + self.summary.get('production_b_completed_manifest_calls', 0))
        self.check(data.get('current_total_calls') == actual, f'ledger current_total_calls {data.get("current_total_calls")} != completed recorded calls {actual}')
        self.check(data.get('initial_candidate_calls') == 11 and data.get('prior_comparison_calls') == 5,
                   'ledger initial/prior counts inconsistent')
        self.check(actual <= data.get('maximum_total_calls', -1) == 38, 'global call cap exceeded or wrong cap')
        self.check(data.get('prior_slot_repairs') == 0, 'prior comparison repair accounting changed')
        repo_ledger = self.evidence / 'call-ledger.json'
        if repo_ledger.exists():
            self.check(self.read_json(repo_ledger) == data, 'repository/external call ledgers differ')
        self.summary['completed_recorded_native_calls'] = actual
        self.summary['post_initial_calls_by_original_slot'] = budgets

    def evidence_records(self):
        records = []
        for name in ['initial-evidence.json', 'fresh-b-evidence.json', 'repair-evidence.json']:
            data = self.read_json(self.evidence / name)
            self.check(isinstance(data, list), f'{name}: expected evidence record list')
            if not isinstance(data, list):
                continue
            self.summary[name + '_records'] = len(data)
            for e in data:
                required = ['external_native_path', 'native_dimensions', 'native_sha256', 'preview', 'preview_dimensions', 'preview_sha256']
                self.check(all(k in e for k in required), f'{name}: incomplete native/preview record')
                if not all(k in e for k in required):
                    continue
                self.image(e['external_native_path'], self.root, e['native_dimensions'], e['native_sha256'], name + ' native')
                self.image(e['preview'], self.evidence, e['preview_dimensions'], e['preview_sha256'], name + ' preview')
                records.append(e)
        self.check(len([e for e in records if e.get('stage') == 'initial']) == 16, 'initial evidence must include prior five and candidate eleven')
        fresh = [e for e in records if e.get('stage') == 'fresh B']
        self.check(len(fresh) == 11 and {e.get('slot') for e in fresh} == SLOTS, 'fresh B evidence must cover exactly eleven slots')
        expected = set(self.initial_entries.values()) | set(self.production_finals)
        expected |= {self.path(e['external_native_path'], self.root) for e in records if str(e.get('external_native_path', '')).startswith('garden-prior/')}
        represented = {self.path(e['external_native_path'], self.root) for e in records}
        self.check(represented == expected, 'evidence JSON does not cover every native call exactly by source path')
        self.check(len(represented) == len(records), 'evidence JSON duplicates a native call path')
        self.records = records

    def selection(self):
        p = self.evidence / 'final-selection.json'
        if not p.exists():
            if self.require_selection:
                self.errors.append('final-selection.json is required but absent')
            else:
                self.warnings.append('Final selection pending: selected eleven images not audited yet')
            return
        data = self.read_json(p)
        if not isinstance(data, dict):
            return
        self.check(data.get('frozen_skill') == 'snapshots/candidate-b'
                   and (self.evidence / 'snapshots/candidate-b').is_dir(),
                   'selection must reference the existing frozen candidate-B repository snapshot')
        self.check(self.path(data.get('source_root', ''), self.root) == self.root, 'selection source_root differs from requested exact source root')
        items = data.get('items', [])
        self.check(data.get('selected_count') == 11 and len(items) == 11 and {e.get('slot') for e in items} == SLOTS,
                   'selection must contain exactly one final for each of eleven original slots')
        self.check(data.get('selection_status') == 'chosen_by_coordinator', 'selection status is not chosen_by_coordinator')
        bypath = {self.path(e['external_native_path'], self.root): e for e in self.records}
        selected = set()
        for e in items:
            native = self.path(e['external_native_path'], self.root)
            self.check(native not in selected, 'selection reuses a native image in multiple slots')
            selected.add(native)
            self.check(native in bypath, f'selected final lacks evidence record: {native}')
            if native in bypath:
                for key in ['native_sha256', 'native_dimensions', 'preview', 'preview_sha256', 'preview_dimensions']:
                    self.check(e.get(key) == bypath[native].get(key), f'selection/evidence {key} mismatch for {e.get("slot")}')
            self.image(e['external_native_path'], self.root, e.get('native_dimensions'), e.get('native_sha256'), 'selected final')
            self.image(e['preview'], self.evidence, e.get('preview_dimensions'), e.get('preview_sha256'), 'selected preview')
            self.check(native.is_relative_to(self.root / 'production-b' / e['slot']), f'{e["slot"]}: selected final belongs to another slot')
        external_selection = self.root / 'final-selection.json'
        if external_selection.exists():
            self.check(self.read_json(external_selection) == data, 'repository/external final selections differ')
        self.summary['selected_finals_checked'] = len(items)
        self.summary['selection_high_end_gate'] = data.get('high_end_gate')

    def run(self):
        for method in [self.skills, self.initial_calls, self.production, self.ledger, self.evidence_records, self.selection]:
            try:
                method()
            except (KeyError, TypeError, ValueError, OSError) as e:
                self.errors.append(f'{method.__name__}: malformed or incomplete evidence: {e}')
        self.summary['unique_image_paths_checked'] = len(self.image_cache)
        return {'status': 'PASS' if not self.errors else 'FAIL', 'scope': 'instruction artifacts, exact file paths, dimensions, SHA256, and recorded call accounting; no pixel-quality certification or exhaustive tool-history proof',
                'summary': self.summary, 'errors': self.errors, 'warnings': self.warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--live-skill', type=Path, default=Path(__file__).resolve().parent.parent / 'Skillsets/skills/ducttape-poster')
    parser.add_argument('--evidence-root', type=Path)
    parser.add_argument('--require-selection', action='store_true')
    args = parser.parse_args()
    if args.evidence_root is None:
        args.evidence_root = args.live_skill.parent.parent / 'evals/ducttape-poster/round3'
    result = Audit(args).run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
