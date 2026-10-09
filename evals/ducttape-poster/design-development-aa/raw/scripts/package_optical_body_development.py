"""Preserve exact AA development text after the ONE R23 five fully closes."""
from pathlib import Path
import datetime
import hashlib
import json

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round23'
ARCHIVE = TASK / 'Skillsets/evals/ducttape-poster/round23'
DEST = TASK / 'Skillsets/evals/ducttape-poster/design-development-aa'
ROOTS = [
    'history/optical-body-draft', 'history/optical-body-scope-review',
    'history/optical-body-adoption', 'history/style-priority-critic-draft',
    'history/r23-script-preparation', 'history/r22-readme',
    'drafts/aa-five-design', 'drafts/optical-range-method',
    'history/final-scope-aa', 'history/r23-first-generation-diagnostic',
]
NAMES = [
    'history/optical-body-root-validation.json', 'history/r23-root-plan-observation.json',
    'history/optical-range-root-decision.json', 'drafts/style-priority-critic-rubric.md',
    'history/r23-root-initial-observation.json', 'history/r23-root-selected-observation.json',
    'scripts/freeze_optical_body_r23.py', 'scripts/close_r23_body_makers.py',
    'scripts/close_r23_body.py', 'scripts/package_optical_body_development.py',
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
assert closure['candidate'] == 'AA' and closure['all_actors_closed'] and closure['requested_images'] == 5
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
    'limits': ['Named AA development text/code only; native outputs and critic records are retained once under round23/raw; no guides supplied.',
               'General optical-body design adopted after closed R22; final critic paragraph prospectively clarified. Numerical floors/normalization unchanged, without historical rescoring or whole-method-unchanged claims.']})
write(DEST / 'byte-verification.json', {'verified_utc': now, 'copied_files': len(rows),
    'all_copy_hashes_match': True, 'round23_archive_reverified': True, 'quality_replayed': False})
locators = [{'source_absolute': row['source_absolute'], 'round23_archive_relative': row['archive_relative'],
             'link_from_development_archive': '../round23/' + row['archive_relative'],
             'sha256': row['sha256'], 'bytes': row['bytes'], 'copied_into_this_archive': False}
            for row in index['files'] if Path(row['source_absolute']).relative_to(ROUND).parts[0] in ('planning', 'coordinator')]
write(DEST / 'related-round23-records.json', {'records': locators, 'individual_guides_duplicated': 0})
table = ['| Stage | PASS | FAIL | NA | Set | Procedure |', '| --- | ---: | ---: | ---: | --- | --- |']
for name in ('initial', 'selected'):
    wave = closure['waves'][name]
    counts = wave['image_gate_counts']
    table.append(f"| {name} | {counts['PASS']} | {counts['FAIL']} | {counts['NA']} | {wave['set_gate']} | {wave['procedure_gate']} |")
report = f'''# Actual optical body, clear Title and supplied roles — AA development

This archive preserves {len(rows)} exact text/code files through the [inventory](archive-index.json) and [byte verification](byte-verification.json). AA changes only production-brief and layout-guide prose. It chooses comfortable actual body forms and continuous sentence area first, then resolves Title weight/contrast/space and image distance/crop/opening jointly. Nominal em or area fit does not certify actual reading; there is no new fixed font/size ratio, QA gate, source reopening or environment installation. Title-only and Title+body use only supplied roles, and complex practical-copy guides remain conditional.

[Body draft](raw/history/optical-body-draft/review.md) · [Independent scope review](raw/history/optical-body-scope-review/review.md) · [AA adoption](raw/history/optical-body-adoption/adoption.json) · [Adopted skill](raw/history/optical-body-adoption/adopted-aa/SKILL.md) · [New five-direction plan](raw/drafts/aa-five-design/plan.json) · [Design rationale](raw/drafts/aa-five-design/rationale.md)

R23 uses one new-topic urban-walking request with only Title and body, two landscape16:9 and three portrait2:3 posters, no client assets and no supporting guides. Five styles are planned through image expression/editing, colour/contrast, typographic voice, material/finish and emotion; good shared layouts/order/alignment are allowed. The existing critic rubric's final paragraph was prospectively clarified for the human's style/actual-role scope. All seven numerical scales/floors and nfc-ws-optical-v1 stay unchanged; all helper/method bytes are not claimed unchanged. The optional [numeric-range proposal](raw/drafts/optical-range-method/review.md) is an unintegrated pure-function draft, deferred by the [root decision](raw/history/optical-range-root-decision.json); its tests do not replay or rescore any native poster.

Actual closed outcomes:

''' + '\n'.join(table) + f'''

Native calls: {closure['native_calls']}; returns: {closure['returned']}; failures: {closure['failed']}; repairs: {closure['repair_calls']}. Initial selected: {closure['initial_selected']}; initials retained without repair: {closure['initial_retained_without_repairs']}. [Full-five closure](../round23/raw/planning/full-five-closure.json), [round report](../round23/report.md) and [related-record locators](related-round23-records.json) retain all initial/selected judgments, uncertainties, errors and selections. No low score/NA is deleted and no critic is replaced, averaged away or asked to rescore.

This new-topic development observation is not a pre-held-out trial or isolated causal proof: copy amount, ratios, topic, plan and the prospective rubric paragraph differ. Packaging checks exact bytes without running a generator/renderer/critic or proving universal high-end quality, native applied fonts, exact Unicode or AI authorship. Source artwork/font binaries are excluded from this named development package, not from all historical archives.
'''

with (DEST / 'report.md').open('x', encoding='utf-8') as handle:
    handle.write(report)
print(json.dumps({'destination': str(DEST), 'exact_text_files': len(rows),
                  'source_artwork_copied': 0, 'font_binaries_copied': 0}))
