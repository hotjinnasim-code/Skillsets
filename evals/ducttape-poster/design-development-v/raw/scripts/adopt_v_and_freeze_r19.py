"""Adopt reviewed general instructions and freeze ONE new-topic five request."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import sys

TASK = Path(__file__).resolve().parents[1]
OLD = TASK / 'work/round18'
ROUND = TASK / 'work/round19'
DRAFT = TASK / 'drafts/candidate-v'
LIVE = TASK / 'Skillsets/skills/ducttape-poster'
HISTORY = TASK / 'history/optical-hierarchy-v'

def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

def read(path):
    return json.loads(Path(path).read_bytes())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')

closure_path = OLD / 'planning/full-five-closure.json'
closed = read(closure_path)
assert closed['all_actors_closed'] and closed['requested_images'] == 5
assert closed['no_post_critic_repair_or_reselection']
assert not ROUND.exists() and not HISTORY.exists()
case_source = TASK / 'drafts/next-five-request.json'
plan_source = TASK / 'drafts/next-five-design/root-plan.json'
corpus = read(case_source)
case = corpus['cases'][0]
plan = read(plan_source)
assert len(corpus['cases']) == 1 and case['count'] == 5
assert plan['case_id'] == case['case_id'] == 'R19-C1'
assert plan['request'] == case['request'] and plan['copy'] == case['copy']
assert len(plan['directions']) == 5
assert {d['role'] for d in plan['directions']} == {r['role_id'] for r in case['roles']}
assert (TASK / 'history/v-scope-audit/status.json').is_file()
assert '한 열·패널·같은 읽는 순서를 모든 방향에 일률적으로 강요하지 않는다.' in (DRAFT / 'references/production-brief.md').read_text()
changed = []
for source in sorted(DRAFT.rglob('*')):
    if source.is_file():
        relative = source.relative_to(DRAFT)
        if source.read_bytes() != (LIVE / relative).read_bytes():
            changed.append(relative.as_posix())
assert changed == ['SKILL.md', 'references/parallel-production.md', 'references/production-brief.md'], changed

shutil.copytree(LIVE, HISTORY / 'before-u')
shutil.copytree(DRAFT, HISTORY / 'adopted-v')
for source in DRAFT.rglob('*'):
    if source.is_file():
        shutil.copy2(source, LIVE / source.relative_to(DRAFT))
snapshot = ROUND / 'snapshots/candidate-v'
shutil.copytree(DRAFT, snapshot)
prior_freeze = read(OLD / 'planning/candidate-u-pre-generation-freeze.json')
helpers = []
for item in prior_freeze['actor_helpers']:
    source = Path(item['path'])
    assert pin(source) == item
    destination = ROUND / source.relative_to(OLD)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    helpers.append(pin(destination))
case_path = ROUND / 'planning/single-five-case.json'
plan_path = ROUND / 'coordinator/R19-C1/plan.json'
write(case_path, corpus)
write(plan_path, plan)
ratio_path = ROUND / 'planning/ratio-policy-before-generation.json'
write(ratio_path, {'declared_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'policy': 'nearest-integer-single-edge', 'max_deviation_px': 0.5, 'explicit_pixel_request_overrides': True, 'source': 'Unchanged aspect-only policy; no quality threshold change.'})
sys.path.insert(0, str(ROUND))
import prepare_production
prepared = prepare_production.prepare(ROUND, case_path, ['R19-C1'], snapshot)
for row in prepared['jobs']:
    job_path = Path(row['job']['path'])
    job = read(job_path)
    prompt_path = Path(job['prompt_file'])
    more = [snapshot / 'references/production-brief.md', snapshot / 'references/design-grammar.md']
    job['inputs'].extend(str(path) for path in more)
    with prompt_path.open('a', encoding='utf-8') as handle:
        handle.write('\nADDITIONAL FIRST-GENERATION DESIGN INPUTS: read ' + ', '.join(str(path) for path in more) + '. Reuse learned ideas without source-artwork reopening. The actual own direction includes optical copy roles, body line groups and concrete next-information transitions. Implement those positive relationships without a fixed shared panel or treating internal dimensions as client preservation conditions. No supporting layout image or client asset is supplied for this case, so a brand-new initial omits both image-reference parameters. Do not create code guides or add image-generation calls beyond your single role and unchanged bounds.\n')
    job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + '\n')
    row['job'] = pin(job_path)
    row['prompt'] = pin(prompt_path)
write(ROUND / 'planning/prepared-maker-jobs.json', prepared)
queue = [row['job']['path'] for row in prepared['jobs']]
write(ROUND / 'planning/maker-queue.json', queue)
write(HISTORY / 'adoption.json', {
    'candidate': 'V', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'previous': 'U', 'previous_full_closure': pin(closure_path), 'changed_files': changed,
    'runtime': [pin(path) for path in sorted((HISTORY / 'adopted-v').rglob('*')) if path.is_file()],
    'synthesis': pin(TASK / 'history/u-general-failure-synthesis/status.json'),
    'draft_record_before_scope_fix': pin(TASK / 'history/v-draft/status.json'),
    'scope_review_before_fix': pin(TASK / 'history/v-scope-audit/status.json'),
    'scope_fix': 'Single-column/panel statement now prohibits uniform imposition across all directions, not a suitable individual layout. ROOT applied the exact narrow correction and quick_validate passed before adoption.',
    'new_quality_gates': 0, 'quality_thresholds_changed': False, 'native_calls_at_adoption': 0,
    'changes': ['Optical priority between actual supplied copy roles', 'Concrete next-information transitions co-designed with image openings/crops', 'Distinguishable actual punctuation and meaningful word spacing in first-generation typography'],
    'limits': ['V has no native quality result at adoption.', 'New-topic development after feedback is not pre-held-out independent validation or causal isolation.', 'Optional guide renderer/catalog/method and the other nine runtime files are identical to U.'],
})
write(ROUND / 'planning/candidate-v-pre-generation-freeze.json', {
    'candidate': 'V', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'runtime': [pin(path) for path in sorted(snapshot.rglob('*')) if path.is_file()],
    'actor_helpers': helpers, 'case': pin(case_path), 'plan': pin(plan_path),
    'maker_jobs': [pin(Path(path)) for path in queue], 'ratio_policy': pin(ratio_path),
    'bounds': {'one_case': True, 'logical_maker_roles': 5, 'worker_process_max': 3, 'initial_per_role': 1, 'repairs_per_role_max': 2, 'native_calls_max': 15},
    'quality_method': 'Unchanged: three independent critics, all seven scores each>=4 and all three diversity>=4 plus mandatory conditions. All low/NA retained.',
    'new_quality_gates': 0, 'native_calls_at_freeze': 0, 'r18_closure': pin(closure_path),
    'new_topic': 'Consumer houseplant market with long Korean description, Latin identity, dates/times/access/care/invitation/URL. No attachments or code guide.',
    'limits': ['One new-topic five request, not a success-rate estimate or universal high-end guarantee.', 'Directions, instructions and topic change together; no isolated attribution.'],
})
print(json.dumps({'adopted': 'V', 'frozen': 'R19', 'requests': 1, 'makers': 5, 'native_calls': 0}))
