"""ROOT-only R10 archive replay, exact inventory, containment and link checks.

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
from contextlib import contextmanager
from html.parser import HTMLParser
from pathlib import Path

GUARDED = ((builtins, ('open',)), (io, ('open',)),
           (os, ('open', 'stat', 'lstat', 'readlink', 'scandir', 'listdir', 'access')))


def load_module(path):
    spec = importlib.util.spec_from_file_location('r10_root_archive_verifier', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


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
    with tempfile.TemporaryDirectory(prefix='r10-archive-containment-') as temp:
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
    mapping = {row['source_absolute']: root/row['archive_relative'] for row in index['files']}
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
                  'selected_raw_scores_or_reports_read': False,
                  'native_calls_or_critics_launched': 0}
    else:
        verifier = load_module(args.archive/'raw/verify_archive.py')
        root = verifier.archive_root(args.archive)
        index_path = verifier.archive_path(root/'archive-index.json', root)
        index = json.loads(index_path.read_bytes())
        links = check_links(root, index, verifier, args.output.absolute())
        inventory = raw_inventory(root, index)
        original_sources = {Path(row['source_absolute']) for row in index['files']}
        source_root = Path(index['source_root'])
        runtime = Path(sys.executable).resolve().parents[2]
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
            replay = verifier.verify(root)
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
        assert replay['unique_summaries_replayed'] == 2
        assert {r['actual_summary_wave'] for r in replay['replays']} == {'initial', 'selected'}
        result = {'status': 'PASS', 'actual_archive': str(root),
                  'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'archive_index_sha256': hashlib.sha256(index_path.read_bytes()).hexdigest(),
                  'portable_frozen_v4_replay': replay, 'exact_raw_inventory': inventory,
                  'original_host_metadata_and_read_attempts': blocked,
                  'unknown_outside_metadata_and_read_attempts': outside,
                  'guarded_operations': [name for _, names in GUARDED for name in names],
                  'containment': containment_fixtures(verifier), 'local_links': links,
                  'native_calls_or_critics_launched': 0,
                  'limits': ['Exact bytes and both frozen v4/source/compact gates are replayed through explicit archive mapping.',
                             'Original low, NULL and NA records are retained. No result is replaced or invented.',
                             'Semantic image viewing remains the original critics\u2019 attestation.',
                             'One seen-development film request; no unseen, isolated causal, universal quality, or AI authorship proof.']}
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2); handle.write('\n')
    if args.archive is not None:
        assert check_links(root, index, verifier) == links
    print(json.dumps({k: v for k, v in result.items() if k != 'portable_frozen_v4_replay'}))


if __name__ == '__main__':
    main()
