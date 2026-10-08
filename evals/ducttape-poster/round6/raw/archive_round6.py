#!/usr/bin/env python3
"""Archive exact R6 bytes with caller-derived stage coverage and raw inventory.

--evidence-only permits explicit NOT_ASSESSABLE terminal review evidence. It never
converts invalid review procedure into an independently assessable visual result.
"""
from pathlib import Path
import argparse
import datetime as dt
import json
import shutil

from audit_portable_archive import derive_inventory, digest, source_path


class SourceReader:
    def __init__(self, root):
        self.source_root = str(root)
        self.errors = []
        self.required = {}

    def exists(self, source):
        return Path(source_path(self.source_root, source)).is_file()

    def require(self, source, expected=None, reason='required metadata'):
        source = source_path(self.source_root, source)
        item = self.required.setdefault(source, {'path': source, 'expected_sha256': expected, 'reasons': []})
        if expected is not None and item['expected_sha256'] not in (None, expected):
            self.errors.append('Conflicting required source pins: ' + source)
        if expected is not None:
            item['expected_sha256'] = expected
        if reason not in item['reasons']:
            item['reasons'].append(reason)
        path = Path(source)
        if not path.is_file():
            self.errors.append('Missing required source: ' + source)
            return None
        actual = digest(path)
        if expected is not None and actual != expected:
            self.errors.append('Required source digest differs: ' + source)
            return None
        return path

    def document(self, source, expected=None, reason='required JSON'):
        path = self.require(source, expected, reason)
        if path is None:
            return {}
        try:
            return json.loads(path.read_text())
        except (OSError, ValueError, TypeError) as error:
            self.errors.append('Invalid source JSON ' + str(source) + ': ' + str(error))
            return {}

    def pin(self, value, reason='pinned file'):
        return self.require(value['path'], value['sha256'], reason)


def archive_round6(root, destination, evidence_only=False):
    root = root.resolve()
    destination = destination.resolve()
    if destination.exists() or destination.is_relative_to(root):
        raise ValueError('Existing archive or source-contained destination refused')
    reader = SourceReader(root)
    evidence_path = root / 'planning/final-evidence.json'
    e = reader.document(evidence_path, reason='terminal combined evidence')
    if len(e.get('images', {})) != 20 or len(e.get('sets', {})) != 4:
        raise ValueError('Complete 20-image/four-context terminal record required')
    invalid = e.get('recorded_evidence_integrity') != 'PASS' or bool(e.get('integrity_errors'))
    if evidence_only:
        if not invalid or e.get('recorded_evidence_integrity') != 'FAIL' or e.get('predeclared_core_diversity_gate') != 'NOT_ASSESSABLE':
            raise ValueError('--evidence-only requires explicit integrity FAIL and NOT_ASSESSABLE terminal evidence')
        for image in e['images'].values():
            group = e['sets'][image['case_id']]
            for phase, key in [('initial', 'initial_image_gate'), ('final', 'final_image_gate')]:
                if group.get(phase + '_case_gate') == 'NOT_ASSESSABLE' and image.get(key) != 'NOT_ASSESSABLE':
                    raise ValueError('Invalid review stage claims a visual result: ' + image['case_id'])
    elif invalid:
        raise ValueError('Invalid review evidence requires explicit --evidence-only archive mode')
    graph = derive_inventory(reader, e)
    calls = graph['calls']
    if calls.get('status') != 'PASS' or calls.get('call_phase') != 'CLOSED' or len(calls.get('records', [])) != calls.get('recorded_attempts') or calls.get('recorded_attempts', 61) > 60:
        raise ValueError('Closed PASS call inventory within recorded cap required')
    if calls.get('prior_R5_closed_recorded') != 128 or calls.get('prior_R5_retirement_unchanged') is not True:
        raise ValueError('Closed prior-history metadata differs')
    # Compute native inventory from EVERY successful caller outcome, never a
    # selected-only scan or a list declared by the archive itself.
    native = {m['final']['sha256'] for rec, m in graph['outcomes'].values() if rec['kind'] == 'returned native'}
    raw_sources = []
    for file in sorted(root.rglob('*')):
        if not file.is_file() or '__pycache__' in file.parts or '.git' in file.parts:
            continue
        if file.is_symlink():
            reader.errors.append('Source-tree symlink refused: ' + str(file))
            continue
        source = str(file)
        h = digest(file)
        raw_sources.append({'path': source, 'sha256': h})
        reader.require(source, reason='complete caller source-tree raw inventory')
    if reader.errors:
        raise ValueError('Archive source byte/coverage errors: ' + json.dumps(reader.errors, ensure_ascii=False))
    # Do not create a partial destination until all expected sources are found
    # and pinned. All native bytes remain exact; duplicate bytes share a blob.
    files = []
    required_rows = []
    for source, requirement in sorted(reader.required.items()):
        src = Path(source)
        h = digest(src)
        if src.suffix.lower() == '.png':
            kind = 'native' if h in native else 'qa'
            relative = Path('images') / kind / (h + '.png')
        elif src.is_relative_to(root):
            kind = 'exact raw source/protocol/evidence/tooling bytes'
            relative = Path('raw') / src.relative_to(root)
        else:
            kind = 'retained external pinned metadata'
            relative = Path('retained-context') / (h + src.suffix)
        out = destination / relative
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists():
            shutil.copyfile(src, out)
        if digest(out) != h:
            raise ValueError('Copied bytes differ: ' + source)
        files.append({'source_absolute': source, 'archive_relative': relative.as_posix(), 'sha256': h, 'kind': kind})
        required_rows.append({**requirement, 'sha256': h})
    successes = sum(x['kind'] == 'returned native' for x in calls['records'])
    index = {
        'schema_version': 2,
        'archived_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'source_root': str(root),
        'source_commit': e['source_commit'],
        'archive_mode': 'evidence-only' if evidence_only else 'assessable-evidence',
        'recorded_evidence_integrity': e['recorded_evidence_integrity'],
        'scope': 'Exact bytes for every caller-recorded successful/failed native stage, all unused repairs, stage inputs/precall/inspection/comparison, all raw source-tree files and CLI evidence, frozen sources and closed prior-history metadata. Explicit source identifiers resolve only through this index. Native aliases are deduplicated by byte digest. Evidence-only mode preserves invalid terminal evidence without visual certification.',
        'files': files,
        'file_count': len(files),
        'required_sources': required_rows,
        'required_source_count': len(required_rows),
        'required_inventory_origin': 'Reconstructed from calls.records outcomes and declared stage/closure/summary/CLI pins, augmented by complete caller source-tree enumeration; not inferred from files after copying.',
        'raw_sources': raw_sources,
        'raw_source_count': len(raw_sources),
        'recorded_attempts': calls['recorded_attempts'],
        'successful_native_attempts': successes,
        'failed_native_attempts': len(calls['records']) - successes,
        'unique_native_hashes': sorted(native),
        'selected_image_count': 20,
        'final_quality_gate': e['predeclared_core_diversity_gate'],
    }
    (destination / 'archive-index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
    return dict(destination=str(destination), archive_mode=index['archive_mode'], mapped_sources=len(files), required_sources=len(required_rows), unique_native_images=len(native), recorded_attempts=calls['recorded_attempts'], selected_images=20, recorded_evidence_integrity=index['recorded_evidence_integrity'], quality_gate=index['final_quality_gate'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', required=True, type=Path)
    parser.add_argument('--evidence-only', action='store_true', help='Preserve explicit invalid/NOT_ASSESSABLE terminal review evidence; byte coverage still required')
    args = parser.parse_args()
    try:
        result = archive_round6(Path(__file__).resolve().parent, args.destination, args.evidence_only)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'FAIL', 'error': str(error)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
