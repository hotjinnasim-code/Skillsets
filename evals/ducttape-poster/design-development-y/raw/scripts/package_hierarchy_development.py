"""Preserve exact general hierarchy development after the ONE R21 five closes."""
from pathlib import Path
import datetime,hashlib,json,shutil
TASK=Path(__file__).resolve().parents[1]
ROUND=TASK/'work/round21'
ARCHIVE=TASK/'Skillsets/evals/ducttape-poster/round21'
DEST=TASK/'Skillsets/evals/ducttape-poster/design-development-y'
ROOTS=['history/purpose-and-whole-plan-x','history/x-draft','history/x-draft-amendment','history/x-scope-audit','history/x-scope-audit-amendment','history/x-publication-prep','history/x-closure-amendment','history/hierarchy-draft','history/hierarchy-scope-audit','history/hierarchy-adoption']
NAMES=['history/x-root-live-validation.json','history/hierarchy-live-validation.json','drafts/x-five-design/plan.json','drafts/x-five-design/rationale.md','drafts/x-five-design/prepare_plan.py','drafts/x-five-design/plan-hierarchy-v2.json','drafts/x-five-design/rationale-hierarchy-v2.md','drafts/x-five-design/prepare_hierarchy_revision.py','drafts/x-five-design/plan-hierarchy-v3.json','drafts/x-five-design/geometry-amendment.md','scripts/prepare_x_workspace.py','scripts/prepare_hierarchy_workspace.py','scripts/render_hierarchy_guides.py','scripts/freeze_hierarchy_r21.py','scripts/close_r21_hierarchy_makers.py','scripts/close_r21_hierarchy.py','scripts/package_hierarchy_development.py','scripts/update_final_y_docs.py']
def read(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(TASK)
 data=p.read_bytes();return {'path':str(p.resolve()),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
def write(p,d):
 with p.open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
assert Path.cwd().resolve().is_relative_to(TASK) and not DEST.exists()
closure=read(ROUND/'planning/full-five-closure.json')
assert closure['candidate']=='Y' and closure['all_actors_closed'] and closure['requested_images']==5
index=read(ARCHIVE/'archive-index.json');assert read(ARCHIVE/'byte-verification.json')['all_copy_hashes_match']
for row in index['files']:
 for p in [Path(row['source_absolute']),ARCHIVE/row['archive_relative']]:
  actual=pin(p);assert actual['sha256']==row['sha256'] and actual['bytes']==row['bytes']
paths=[]
for rel in ROOTS:
 directory=TASK/rel;assert directory.is_dir()
 paths.extend(p for p in directory.rglob('*') if p.is_file())
paths.extend(TASK/rel for rel in NAMES)
assert len(paths)==len(set(paths))
rows=[]
for p in sorted(paths):
 assert p.suffix in {'.md','.json','.py','.yaml','.txt','.diff'}
 raw=p.read_bytes();raw.decode('utf-8');assert b'\0' not in raw
 info=pin(p);rows.append({'source_absolute':info['path'],'source_relative':str(p.relative_to(TASK)),'archive_relative':'raw/'+p.relative_to(TASK).as_posix(),'sha256':info['sha256'],'bytes':info['bytes']})
for row in rows:
 out=DEST/row['archive_relative'];out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('xb') as f:f.write(Path(row['source_absolute']).read_bytes())
 assert pin(out)['sha256']==row['sha256']==pin(Path(row['source_absolute']))['sha256']
time=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(DEST/'archive-index.json',{'schema_version':1,'archived_utc':time,'source_root':str(TASK),'files':rows,'raw_inventory_exclusions':[],'source_artwork_copied':0,'font_binaries_copied':0,'quality_replayed':False,'limits':['Exact named development text/code only; every native output, own guide, failure and original critic record is retained once in the closed round21 archive.','Original X preparation had zero jobs/native calls. The human hierarchy steering and Y revision occurred before the ONE R21 five. X ungenerated plans remain preserved without quality claims.']})
write(DEST/'byte-verification.json',{'verified_utc':time,'copied_files':len(rows),'all_copy_hashes_match':True,'round21_archive_reverified':True,'quality_replayed':False})
locators=[{'source_absolute':r['source_absolute'],'round21_archive_relative':r['archive_relative'],'link_from_development_archive':'../round21/'+r['archive_relative'],'sha256':r['sha256'],'bytes':r['bytes'],'copied_into_this_archive':False} for r in index['files'] if Path(r['source_absolute']).relative_to(ROUND).parts[0] in ('planning','coordinator')]
write(DEST/'related-round21-records.json',{'records':locators,'individual_guides_duplicated':0})
table=['| Stage | PASS | FAIL | NA | Set | Procedure |','| --- | ---: | ---: | ---: | --- | --- |']
for name in ('initial','selected'):
 w=closure['waves'][name];c=w['image_gate_counts'];table.append(f"| {name} | {c['PASS']} | {c['FAIL']} | {c['NA']} | {w['set_gate']} | {w['procedure_gate']} |")
report=f'''# Purpose, readable text-role hierarchy and harmonious type — development archive

This archive preserves {len(rows)} exact text/code files and the original sequence from W through X purpose/continuity planning to the human-requested Y hierarchy revision. The [SHA-256 inventory](archive-index.json) and [byte verification](byte-verification.json) identify their historical bytes. X preparation and its original plan had zero native calls; no X quality result was replaced or relabelled. Y was adopted and frozen before the ONE R21 five began.

[Original X draft](raw/history/x-draft/review.md) · [X scope and narrow amendment](raw/history/x-scope-audit-amendment/review.md) · [Hierarchy draft](raw/history/hierarchy-draft/review.md) · [Independent hierarchy scope review](raw/history/hierarchy-scope-audit/review.md) · [Y adoption](raw/history/hierarchy-adoption/adoption.json) · [Before X](raw/history/hierarchy-adoption/before-x/SKILL.md) · [Adopted Y](raw/history/hierarchy-adoption/adopted-y/SKILL.md)

The general design instructions assign only supplied copy to eyebrow, Title, Subtitle, body and footer functions; an ordinary supplied Title is an immediately recognisable main typographic anchor. Subordinate copy stays readable, and font anatomy, width, stroke contrast, weight and Korean/Latin/numeral alignment form one harmonious system. The instructions do not invent missing roles/copy, impose fixed font/pixel ratios or reuse one layout across five styles. Explicit user roles, text-free/title-only cases and existing-runtime fallback remain authoritative. Complex prose uses own actual-font/copy and substantive image geometry planning before native generation. Reference ideas are reused without mandatory original-artwork reopening.

[Ungenerated original plan](raw/drafts/x-five-design/plan.json) · [Hierarchy revision](raw/drafts/x-five-design/plan-hierarchy-v2.json) · [Final prospective plan](raw/drafts/x-five-design/plan-hierarchy-v3.json) · [Hierarchy rationale](raw/drafts/x-five-design/rationale-hierarchy-v2.md) · [M3 geometry correction](raw/drafts/x-five-design/geometry-amendment.md) · [Bounded-failure closure amendment](raw/history/x-closure-amendment/review.md)

R21 was fully closed and its raw archive reverified before packaging. Actual original outcomes, with unchanged thresholds and no rescoring or critic replacement:

'''+ '\n'.join(table)+f'''

Native calls: {closure['native_calls']}; returns: {closure['returned']}; failures: {closure['failed']}; repair calls: {closure['repair_calls']}. [Full-five closure](../round21/raw/planning/full-five-closure.json) retains initial selection, unrepaired first results, actual critic processes/sessions and original score counts. [Round21 report](../round21/report.md) and [exact related-record locators](related-round21-records.json) connect the guides and all production/evaluation evidence, retained once under round21/raw. The failed M3 polygon specification and corrected own guide are retained; native artwork was not edited with code.

Static scope checks, source quantities and guide font files do not certify native final font-file application, universal high-end quality, authorship detection, held-out transfer or an isolated instruction effect. All lows, NA, errors, disagreements and original selections remain unchanged. This packaging script executes no source script, generator, renderer, critic or test and changes no runtime or Git state. Source artwork and font binaries are excluded from this named development package; this is not a claim about every older archive.
'''
with (DEST/'report.md').open('x',encoding='utf-8') as f:f.write(report)
print(json.dumps({'destination':str(DEST),'exact_text_files':len(rows),'source_artwork_copied':0,'font_binaries_copied':0}))
