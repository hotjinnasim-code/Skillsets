"""Copy closed single-five evidence as exact bytes; no review or gate recomputation."""
import argparse, datetime, hashlib, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pinned_objects(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(value.get('sha256', ''))):
            yield value
        for member in value.values(): yield from pinned_objects(member)
    elif isinstance(value, list):
        for member in value: yield from pinned_objects(member)

def authoritative_data(name, value):
    """Exclude preserved observations without rewriting any source document."""
    if name in ('inspection.json', 'parent-comparison.json'):
        return {}
    if name == 'summary.json':
        return {k:v for k,v in value.items() if k not in ('reviews', 'raw_packet')}
    if name == 'source-asset-audit.json':
        observed = ('observed_source_assets_viewed', 'observed_protected_layouts_read')
        return {**value, 'profiles': {profile: {k:v for k,v in record.items() if k not in observed}
                                    for profile,record in value['profiles'].items()}}
    return value

def archive(destination):
    destination = destination.resolve()
    assert not destination.exists() and not destination.is_relative_to(ROOT)
    final = json.loads((ROOT/'planning/final-evidence.json').read_bytes())
    assert final['poster_calls_closed'] is True and final['poster_role_denominator'] == 5
    corpus = json.loads((ROOT/'planning/single-five-case.json').read_bytes())
    sources, source_directories = {}, []
    for p in sorted(ROOT.rglob('*')):
        assert not p.is_symlink(), 'Source symlink entry: '+str(p)
        if p.is_dir():
            source_directories.append(p.relative_to(ROOT).as_posix())
            continue
        assert p.is_file(), 'Unknown source inventory entry: '+str(p)
        sources[str(p.resolve())] = {'sha256': digest(p), 'bytes': p.stat().st_size, 'origin': 'complete raw candidate-M single-five source tree'}
    authoritative = [ROOT/'planning'/name for name in ('final-evidence.json', 'single-five-case.json', 'candidate-m-pre-generation-freeze.json', 'critic-recording-helper-freeze.json')]
    for case in corpus['cases']:
        cid = case['case_id']
        authoritative += list((ROOT/'coordinator'/cid).glob('*.json'))
        if cid == 'R7-D1': authoritative += list((ROOT/'coordinator'/'H-D1').glob('*.json'))
        for role in case['roles']:
            d = ROOT/'production'/role['role_id']
            authoritative += list(d.glob('*.json')) + list((d/'stages').glob('*/*.json'))
        authoritative += list((ROOT/'reviews'/cid).glob('*/*.json')) + list((ROOT/'reviews'/cid).glob('*/cli/*/launch.json')) + list((ROOT/'reviews'/cid).glob('*/cli/*/completion.json'))
    for document in authoritative:
        data = json.loads(document.read_bytes())
        # The unchanged raw bytes are copied above. Observed/revisit claims are
        # evidence to judge, not artifact declarations that must be made true.
        data = authoritative_data(document.name, data)
        for item in pinned_objects(data):
            p = Path(item['path'])
            p = document.parent/p if not p.is_absolute() else p
            assert '..' not in p.parts and not any(q.is_symlink() for q in (p,*p.parents)), 'Source pin symlink/traversal'
            p = p.resolve(strict=True)
            assert p.is_file() and digest(p) == item['sha256'], str(p)
            if str(p) in sources: assert sources[str(p)]['sha256'] == item['sha256']
            else: sources[str(p)] = {'sha256': item['sha256'], 'bytes': p.stat().st_size, 'origin': 'actual authoritative external pin'}
    rows, by_hash = [], {}
    # Prefer retained raw originals for byte-identical external native-cache
    # identifiers; every distinct raw artifact still keeps its own raw path.
    owned = [(source,data) for source,data in sources.items() if Path(source).is_relative_to(ROOT)]
    for source,data in sorted(owned, key=lambda item: (Path(item[0]).name != 'original.png', item[0])):
        by_hash.setdefault(data['sha256'], Path('raw')/Path(source).relative_to(ROOT))
    # Validate the complete source inventory before creating a destination.
    for source, data in sorted(sources.items()):
        p = Path(source); h = data['sha256']; assert digest(p) == h and p.stat().st_size == data['bytes']
        if p.is_relative_to(ROOT): rel = Path('raw')/p.relative_to(ROOT)
        elif h in by_hash: rel = by_hash[h]
        else: rel = Path('retained-context')/(h+p.suffix)
        by_hash.setdefault(h, rel)
        rows.append({'source_absolute': source, 'archive_relative': rel.as_posix(), **data})
    for relative in source_directories:
        (destination/'raw'/relative).mkdir(parents=True, exist_ok=True)
    for row in rows:
        out = destination/row['archive_relative']; out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists(): shutil.copyfile(row['source_absolute'], out)
        assert digest(out) == row['sha256']
    index = {'schema_version': 1, 'archived_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_root': str(ROOT), 'files': rows, 'source_directories': source_directories, 'raw_inventory_exclusions': [], 'mapped_sources': len(rows), 'unique_exact_byte_hashes': len(by_hash), 'closed_evidence': final, 'limits': ['Copies preserve raw FAIL/NA and unused native images; no quality certification is added.', 'Absolute source identifiers resolve through this index on another machine.', 'All five requested roles remain in the denominator. Complete reference-research images are retained for provenance only, not passed to native generation as client assets or represented as generated posters.']}
    with (destination/'archive-index.json').open('x') as f: json.dump(index, f, ensure_ascii=False, indent=2)
    return {'destination': str(destination), 'mapped_sources': len(rows), 'unique_hashes': len(by_hash)}

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--destination', type=Path, required=True); a = p.parse_args()
    print(json.dumps(archive(a.destination)))
