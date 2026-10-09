"""ROOT-only exact whole-archive inventory comparator, with no exclusions."""
import argparse
import hashlib
import json
from pathlib import Path


def inventory(root):
    root = root.resolve(strict=True)
    files, directories = {}, []
    for path in sorted(root.rglob('*')):
        assert not path.is_symlink(), 'Whole-copy symlink forbidden: '+str(path)
        relative = path.relative_to(root).as_posix()
        if path.is_dir():
            directories.append(relative)
        else:
            assert path.is_file(), 'Unknown whole-copy entry: '+str(path)
            data = path.read_bytes()
            files[relative] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
    return {'files': files, 'directories': directories}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--copy', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    before = inventory(args.source)
    after = inventory(args.copy)
    assert before == after, 'Whole archive copy changed or omitted entries'
    result = {'status': 'PASS', 'source': str(args.source.resolve()),
              'copy': str(args.copy.resolve()), 'file_count': len(before['files']),
              'directory_count': len(before['directories']),
              'bytes': sum(row['bytes'] for row in before['files'].values()),
              'inventory': before, 'exclusions': []}
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2); handle.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'inventory'}))


if __name__ == '__main__':
    main()
