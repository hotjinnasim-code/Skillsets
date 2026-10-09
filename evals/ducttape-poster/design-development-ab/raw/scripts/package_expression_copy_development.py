"""Preserve exact AB development text after the ONE R24 five fully closes."""
from pathlib import Path
import datetime
import hashlib
import json

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round24'
ARCHIVE = TASK / 'Skillsets/evals/ducttape-poster/round24'
DEST = TASK / 'Skillsets/evals/ducttape-poster/design-development-ab'
ROOTS = [
    'history/expression-copy-draft', 'history/expression-copy-scope-review',
    'history/expression-copy-adoption', 'history/r24-script-preparation',
    'history/r23-readme', 'drafts/ab-five-design',
    'drafts/candidate-expression-copy', 'drafts/candidate-expression-copy-v2',
    'history/final-scope-ab',
    'history/final-publication-advisory',
]
NAMES = [
    'history/expression-copy-root-validation.json',
    'history/expression-copy-v2-root-validation.json',
    'history/expression-copy-scope-advisory-resolution.json',
    'history/r24-root-pre-generation-observation.json',
    'history/r24-root-native-observation.json',
    'scripts/freeze_expression_copy_r24.py', 'scripts/close_r24_makers.py',
    'scripts/close_r24.py', 'scripts/package_expression_copy_development.py',
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
assert closure['candidate'] == 'AB' and closure['all_actors_closed'] and closure['requested_images'] == 5
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
    'limits': ['Named AB development text/code only; native outputs/own guides/critic records retained once under round24/raw.',
               'General first-native expression and display-copy groups adopted after closed R23; all20 actor helper bytes copied exactly from R23. Numerical floors/normalization unchanged, no historical rescoring or whole-method-unchanged claim.']})
write(DEST / 'byte-verification.json', {'verified_utc': now, 'copied_files': len(rows),
    'all_copy_hashes_match': True, 'round24_archive_reverified': True, 'quality_replayed': False})
locators = [{'source_absolute': row['source_absolute'], 'round24_archive_relative': row['archive_relative'],
             'link_from_development_archive': '../round24/' + row['archive_relative'],
             'sha256': row['sha256'], 'bytes': row['bytes'], 'copied_into_this_archive': False}
            for row in index['files'] if Path(row['source_absolute']).relative_to(ROUND).parts[0] in ('planning', 'coordinator')]
write(DEST / 'related-round24-records.json', {'records': locators, 'individual_guides_duplicated': 0})
table = ['| Stage | PASS | FAIL | NA | Set | Procedure |', '| --- | ---: | ---: | ---: | --- | --- |']
for name in ('initial', 'selected'):
    wave = closure['waves'][name]
    counts = wave['image_gate_counts']
    table.append(f"| {name} | {counts['PASS']} | {counts['FAIL']} | {counts['NA']} | {wave['set_gate']} | {wave['procedure_gate']} |")
report = f'''# Expression-led first native brief and actual display-copy groups — AB development

This archive preserves {len(rows)} exact text/code files in the [inventory](archive-index.json), with [byte verification](byte-verification.json). The final change is general: describe how forms, edges, detail density and light construct the chosen expression first; place the actual supplied copy once in its designed word-boundary soft-line shape; then specify the scene, composition, colour and finish. Original/verification copy stays unchanged. Title remains immediately identifiable, body receives a continuous comfortable reading area, and absent roles are not invented. Title-only and Title+body do not gain obligatory guides, fixed fonts/sizes or extra QA. Final posters still use the native image tool.

[Draft](raw/history/expression-copy-draft/review.md) · [Scope review](raw/history/expression-copy-scope-review/review.md) · [Source/display clarification](raw/history/expression-copy-scope-advisory-resolution.json) · [AB adoption](raw/history/expression-copy-adoption/adoption.json) · [Adopted skill](raw/history/expression-copy-adoption/adopted-ab/SKILL.md) · [Five-direction plan](raw/drafts/ab-five-design/plan.json) · [Design rationale](raw/drafts/ab-five-design/rationale.md)

R24 starts after exact whole R23 closure/archive. It uses the same supplied Title+body urban-walking request, conditions and five ratios (two16:9, three2:3); this known development fixture is not held out. Two landscape directions optionally use newly authored actual-copy/font and expression sketches; the other three are direct. Sketch geometry/line counts are design inputs, not client preservation constraints or new quality gates, and actual guide fonts do not prove native font-file application. The 20 actor helper files are byte-equal to R23. Local orchestration supplies each guided maker only its own guide and pins the final inputs before native dispatch; this is recorded rather than described as an entirely unchanged method. No source-original reopening, font installation or manual bitmap typography overlay was added. Seven categories, each critic’s floor4, three critics’ diversity floor4, mandatory conditions and nfc-ws-optical-v1 stay unchanged.

Actual closed outcomes:

''' + '\n'.join(table) + f'''

Native calls: {closure['native_calls']}; returns: {closure['returned']}; failures: {closure['failed']}; repairs: {closure['repair_calls']}. Initial selected: {closure['initial_selected']}; initials retained without repair: {closure['initial_retained_without_repairs']}. [Full closure](../round24/raw/planning/full-five-closure.json), [round report](../round24/report.md) and [related locators](related-round24-records.json) retain the full initial/selected records and actual process/session counts. Complete unchanged whole-context initial reuse does not count new critics; fresh/UNREADY/error stages retain their original low/NA/failed records without replacements, averaging or rescoring. No post-critic repair or reselection occurred.

This is one prospective general production change and one complete development five, with multiple design-input changes. It does not establish an isolated causal effect, independent transfer, stable success rate across genres, universal high-end quality or AI authorship. Earlier [AA](../design-development-aa/report.md) and historical raw outcomes remain intact. Packaging verifies bytes, not visual replay.
'''

with (DEST / 'report.md').open('x', encoding='utf-8') as handle:
    handle.write(report)
print(json.dumps({'destination': str(DEST), 'exact_text_files': len(rows),
                  'source_artwork_copied': 0, 'font_binaries_copied': 0}))
