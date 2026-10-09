"""ROOT-only actual archive replay, host-access blocking and local-link audit.

This does not edit actor inputs, reviews, scores, thresholds or native images.
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
from html.parser import HTMLParser
from pathlib import Path


def load_module(path):
    spec = importlib.util.spec_from_file_location('r9_actual_archive_verifier', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            self.images += 1
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


def check_links(root, index, pending_output=None):
    source_root = index['source_root']
    mapping = {row['source_absolute']: root / row['archive_relative'] for row in index['files']}
    gallery = mapping[source_root + '/gallery.html']
    parser = Links()
    parser.feed(gallery.read_text())
    assert parser.images == 5 and len(parser.links) == 20
    checked = []
    for link in parser.links:
        target = gallery.parent / link
        assert not Path(link).is_absolute() and '..' not in Path(link).parts
        assert target.resolve().is_relative_to(root) and target.is_file(), link
        checked.append(str(target.relative_to(root)))
    report = mapping[source_root + '/report.md']
    report_links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', report.read_text())
    for link in report_links:
        target = report.parent / link
        assert not Path(link).is_absolute() and '..' not in Path(link).parts
        assert target.resolve().is_relative_to(root) and target.is_file(), link
    wrapper_links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', (root/'report.md').read_text())
    for link in wrapper_links:
        target = root / link
        assert not Path(link).is_absolute() and '..' not in Path(link).parts
        assert target.resolve().is_relative_to(root), link
        if pending_output is None or target != pending_output:
            assert target.is_file(), link
    return {'gallery_images': parser.images, 'gallery_local_links': len(checked),
            'closed_report_local_links': len(report_links), 'wrapper_report_local_links':len(wrapper_links), 'missing_links': []}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.archive.resolve(strict=True)
    index = json.loads((root / 'archive-index.json').read_bytes())
    sys.dont_write_bytecode = True
    verifier = load_module(root / 'raw/verify_archive.py')
    links = check_links(root, index, args.output.absolute())
    original_sources = {Path(row['source_absolute']) for row in index['files']}
    source_root = Path(index['source_root'])
    original_home = Path.home()
    runtime = Path(sys.executable).resolve().parents[2]
    operations = []
    blocked = []

    def allowed(value, operation):
        if not isinstance(value, (str, bytes, Path)):
            return
        path = Path(os.path.abspath(os.fsdecode(value)))
        if path.is_relative_to(root):
            return
        if path in original_sources or path.is_relative_to(source_root):
            blocked.append(str(path))
            raise AssertionError('Original source access attempted: ' + str(path))
        if operation in ('stat', 'lstat', 'readlink', 'access') and (root.is_relative_to(path) or runtime.is_relative_to(path)):
            return
        if path.is_relative_to(original_home) and not path.is_relative_to(runtime):
            blocked.append(str(path))
            raise AssertionError('Original home metadata/read attempted: ' + str(path))

    def install(owner, name):
        original = getattr(owner, name)

        def guarded(path, *args, **kwargs):
            allowed(path, name)
            return original(path, *args, **kwargs)

        setattr(owner, name, guarded)
        operations.append((owner, name, original))

    for owner, names in ((builtins, ('open',)), (io, ('open',)),
                         (os, ('open', 'stat', 'lstat', 'readlink', 'scandir', 'access'))):
        for name in names:
            install(owner, name)
    try:
        replay = verifier.verify(root)
        assert replay['status'] == 'PASS' and not blocked
        outside = [str(source_root / 'planning/final-evidence.json'),
                   str(root / '..' / source_root.name / 'planning/final-evidence.json'),
                   '../original-host-path', '', 'relative-without-base']
        for value in outside:
            try:
                verifier.archive_path(value, root)
            except ValueError:
                pass
            else:
                raise AssertionError('Outside path accepted: ' + value)
        assert not blocked, 'Lexical rejection consulted original-host metadata'
        assert not blocked
    finally:
        for owner, name, original in reversed(operations):
            setattr(owner, name, original)
    with tempfile.TemporaryDirectory(prefix='r9-archive-containment-') as temp:
        fixture = Path(temp)
        archive = fixture / 'archive'
        archive.mkdir()
        external = fixture / 'outside'
        external.mkdir()
        (external / 'sentinel').write_text('root-only containment fixture')
        (archive / 'escape').symlink_to(external, target_is_directory=True)
        for candidate in (archive / 'escape', archive / 'escape/sentinel'):
            try:
                verifier.archive_path(candidate, archive)
            except ValueError as exc:
                assert 'symlink' in str(exc)
            else:
                raise AssertionError('Symlink escape accepted')
    fixture_blocked = []
    with tempfile.TemporaryDirectory(prefix='r9-index-containment-') as temp:
        fixture = Path(temp)
        archive = fixture/'archive'; archive.mkdir()
        external = fixture/'outside'; external.mkdir()
        (external/'sentinel').write_text('root-only indexed containment fixture')
        (archive/'escape').symlink_to(external, target_is_directory=True)
        (archive/'file-escape').symlink_to(external/'sentinel')
        fixture_operations = []
        def guard_fixture(owner, name):
            original = getattr(owner, name)
            def guarded(path, *args, **kwargs):
                if isinstance(path, (str,bytes,Path)):
                    p=Path(os.path.abspath(os.fsdecode(path)))
                    if p.is_relative_to(external):
                        fixture_blocked.append({'operation':name,'path':str(p)})
                        raise AssertionError('Outside fixture metadata/read consulted')
                return original(path,*args,**kwargs)
            setattr(owner,name,guarded); fixture_operations.append((owner,name,original))
        for candidate in ('escape/sentinel','file-escape'):
            (archive/'archive-index.json').write_text(json.dumps({'files':[{'archive_relative':candidate,'source_absolute':'/explicit/index-fixture','sha256':'0'*64}]}))
            for owner,names in ((builtins,('open',)),(io,('open',)),(os,('open','stat','lstat','readlink','scandir','access'))):
                for name in names:guard_fixture(owner,name)
            try:
                try:verifier.verify(archive)
                except ValueError as exc:assert 'symlink' in str(exc)
                else:raise AssertionError('Indexed symlink escape accepted')
                assert not fixture_blocked
            finally:
                for owner,name,original in reversed(fixture_operations):setattr(owner,name,original)
                fixture_operations.clear()
    result = {'status': 'PASS', 'actual_archive': str(root),
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'archive_index_sha256': hashlib.sha256((root / 'archive-index.json').read_bytes()).hexdigest(),
              'portable_frozen_v4_replay': replay,
              'original_source_metadata_and_read_attempts': blocked,
              'host_access_guard': 'Original source identifiers and original home are blocked, except this archive, bundled Python runtime and their shared ancestor metadata.',
              'guarded_operations': [name for _, name, _ in operations],
              'lexically_rejected_outside_paths': len(outside),
              'rejected_symlink_escape_paths': 2, 'rejected_actual_index_symlink_escape_paths':2, 'outside_index_fixture_metadata_and_read_attempts':fixture_blocked, 'local_links': links,
              'native_calls_or_critics_launched': 0,
              'limits': ['This verifies byte provenance, gate replay and file links; no pixels are visually inspected by this checker.',
                         'Native image/source viewing remains the original critics\u2019 semantic attestation.']}
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    assert check_links(root,index)==links
    print(json.dumps({key: value for key, value in result.items() if key not in ('portable_frozen_v4_replay',)}))


if __name__ == '__main__':
    main()
