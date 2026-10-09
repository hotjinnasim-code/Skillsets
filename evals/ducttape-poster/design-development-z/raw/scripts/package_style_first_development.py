"""Preserve exact Z development text after the ONE R22 five fully closes."""
from pathlib import Path
import datetime
import hashlib
import json

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round22'
ARCHIVE = TASK / 'Skillsets/evals/ducttape-poster/round22'
DEST = TASK / 'Skillsets/evals/ducttape-poster/design-development-z'
ROOTS = [
    'history/style-first-steering', 'history/style-first-draft',
    'history/style-first-scope-audit', 'history/style-first-preparation-amendment',
    'history/style-first-idea-review', 'history/style-first-idea-amendment',
    'history/style-first-idea-scope-audit', 'history/style-first-adoption',
    'history/style-first-readme', 'history/r22-script-scope-audit',
    'history/r22-freeze-case-amendment', 'history/r22-report-timing-amendment',
    'drafts/z-five-design', 'history/r22-first-generation-design-review',
    'history/r22-optical-type-method-review',
]
NAMES = [
    'history/style-first-live-validation.json',
    'scripts/prepare_style_first_workspace.py', 'scripts/render_style_first_guides.py',
    'scripts/freeze_style_first_r22.py', 'scripts/close_r22_style_makers.py',
    'scripts/close_r22_style.py', 'scripts/package_style_first_development.py',
]

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path)
    assert path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(TASK)
    data = path.read_bytes()
    return {'path': str(path.resolve()), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def write(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')

assert Path.cwd().resolve().is_relative_to(TASK) and not DEST.exists()
closure = read(ROUND / 'planning/full-five-closure.json')
assert closure['candidate'] == 'Z' and closure['all_actors_closed'] and closure['requested_images'] == 5
index = read(ARCHIVE / 'archive-index.json')
assert read(ARCHIVE / 'byte-verification.json')['all_copy_hashes_match']
for row in index['files']:
    for path in [Path(row['source_absolute']), ARCHIVE / row['archive_relative']]:
        actual = pin(path)
        assert actual['sha256'] == row['sha256'] and actual['bytes'] == row['bytes']
paths = []
for relative in ROOTS:
    directory = TASK / relative
    assert directory.is_dir()
    paths.extend(path for path in directory.rglob('*') if path.is_file())
paths.extend(TASK / relative for relative in NAMES)
assert len(paths) == len(set(paths))
rows = []
for path in sorted(paths):
    assert path.suffix in {'.md', '.json', '.py', '.yaml', '.txt', '.diff', '.patch'}
    raw = path.read_bytes()
    raw.decode('utf-8')
    assert b'\0' not in raw
    info = pin(path)
    rows.append({'source_absolute': info['path'], 'source_relative': str(path.relative_to(TASK)),
                 'archive_relative': 'raw/' + path.relative_to(TASK).as_posix(),
                 'sha256': info['sha256'], 'bytes': info['bytes']})
for row in rows:
    out = DEST / row['archive_relative']
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('xb') as handle:
        handle.write(Path(row['source_absolute']).read_bytes())
    assert pin(out)['sha256'] == row['sha256'] == pin(Path(row['source_absolute']))['sha256']
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
write(DEST / 'archive-index.json', {'schema_version': 1, 'archived_utc': now,
    'source_root': str(TASK), 'files': rows, 'raw_inventory_exclusions': [],
    'source_artwork_copied': 0, 'font_binaries_copied': 0, 'quality_replayed': False,
    'limits': ['Named Z development text/code only; native outputs, own guides and critic records are retained once under round22/raw.',
               'Human style-priority and actual-role scope changed prospectively after closed R21; no historical rescoring or unchanged-whole-method claim.']})
write(DEST / 'byte-verification.json', {'verified_utc': now, 'copied_files': len(rows),
    'all_copy_hashes_match': True, 'round22_archive_reverified': True, 'quality_replayed': False})
locators = [{'source_absolute': row['source_absolute'], 'round22_archive_relative': row['archive_relative'],
             'link_from_development_archive': '../round22/' + row['archive_relative'],
             'sha256': row['sha256'], 'bytes': row['bytes'], 'copied_into_this_archive': False}
            for row in index['files'] if Path(row['source_absolute']).relative_to(ROUND).parts[0] in ('planning', 'coordinator')]
write(DEST / 'related-round22-records.json', {'records': locators, 'individual_guides_duplicated': 0})
table = ['| Stage | PASS | FAIL | NA | Set | Procedure |', '| --- | ---: | ---: | ---: | --- | --- |']
for name in ('initial', 'selected'):
    wave = closure['waves'][name]
    counts = wave['image_gate_counts']
    table.append(f"| {name} | {counts['PASS']} | {counts['FAIL']} | {counts['NA']} | {wave['set_gate']} | {wave['procedure_gate']} |")
report = f'''# Style identity, readable type hierarchy and actual copy roles — Z development

This archive preserves {len(rows)} exact text/code files through the [SHA-256 inventory](archive-index.json) and [byte verification](byte-verification.json). The human explicitly prioritised style differences, allowed shared good layouts, and noted Title-only and Title+body requests. Those instructions were incorporated before the ONE R22 five; historical R21 images, conditions and scores stay unchanged.

[Human steering](raw/history/style-first-steering/steering.json) · [Style-first draft](raw/history/style-first-draft/review.md) · [Optional accumulated expression ideas](raw/history/style-first-idea-review/review.md) · [Narrow amended scope review](raw/history/style-first-idea-scope-audit/review.md) · [Z adoption](raw/history/style-first-adoption/adoption.json) · [Adopted Z](raw/history/style-first-adoption/adopted-z/SKILL.md)

The skill connects content with image expression/editing, colour relationships, typographic voice, material/finish and mood. Effective layouts, alignment and Title/body order may be shared; five unique component values or a fixed five-style menu are not required. It assigns only supplied copy, keeps the main Title immediately recognisable and body fonts harmonious, and invents no absent eyebrow, Subtitle, footer, event data or URL. Complex practical-copy planning stays conditional; Title+body without practical information does not require the guide workflow. Accumulated source ideas are optional, without mandatory new browsing or original-artwork reopening.

[New five-direction plan](raw/drafts/z-five-design/plan.json) · [Design rationale](raw/drafts/z-five-design/rationale.md) · [Exact case reconciliation](raw/drafts/z-five-design/case-reconciliation.json) · [Prospective scripts review](raw/history/r22-script-scope-audit/review.md)

The same dense plant-market content, 12 copy entries, landscape 16:9 and empty client assets were retained. The request's style/layout sentence and one matching condition changed prospectively according to the human; the seven numerical categories and per-critic floors did not change. This is matched development after feedback and explicit scope steering, not unseen transfer or an isolated causal comparison. Five new own planning guides were rendered and actually viewed before generation, and each maker received only its own. Actual outcomes:

''' + '\n'.join(table) + f'''

Native calls: {closure['native_calls']}; returns: {closure['returned']}; failures: {closure['failed']}; repairs: {closure['repair_calls']}. [Full-five closure](../round22/raw/planning/full-five-closure.json), [round report](../round22/report.md) and [exact related-record locators](related-round22-records.json) retain all initial/selected outcomes and actual fresh, reuse or UNREADY evaluation provenance. No low score, NA, error, disagreement or unselected output is discarded.

Packaging checks bytes and executes no generator, renderer, critic, source script or test. Reference quantity, font metrics and static scope audits do not certify native applied fonts, every-image high-end quality, universal authorship detection or generalisation. Source artwork and font binaries are excluded from this named development package; this is not a claim about all older archives.
'''
with (DEST / 'report.md').open('x', encoding='utf-8') as handle:
    handle.write(report)
print(json.dumps({'destination': str(DEST), 'exact_text_files': len(rows),
                  'source_artwork_copied': 0, 'font_binaries_copied': 0}))
