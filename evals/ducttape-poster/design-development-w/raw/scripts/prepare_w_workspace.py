"""Adopt scoped general W instructions; prepare ONE matched development workspace."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import shutil

TASK = Path(__file__).resolve().parents[1]
OLD = TASK / 'work/round19'
ROUND = TASK / 'work/round20'
DRAFT = TASK / 'drafts/candidate-w'
LIVE = TASK / 'Skillsets/skills/ducttape-poster'
HISTORY = TASK / 'history/first-generation-sketch-w'

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')

closure_path = OLD / 'planning/full-five-closure.json'
closed = read(closure_path)
assert closed['all_actors_closed'] and closed['requested_images'] == 5
assert closed['no_post_critic_repair_or_reselection']
assert (TASK / 'Skillsets/evals/ducttape-poster/round19/byte-verification.json').is_file()
assert not ROUND.exists() and not HISTORY.exists()
scope_review = TASK / 'history/w-scope-audit/status.json'
assert scope_review.is_file()
expected = ['SKILL.md', 'references/layout-guide-contract.md', 'references/layout-guide.md', 'references/parallel-production.md', 'references/production-brief.md']
draft_files = sorted(path for path in DRAFT.rglob('*') if path.is_file())
assert len(draft_files) == 12
changed = [path.relative_to(DRAFT).as_posix() for path in draft_files if path.read_bytes() != (LIVE / path.relative_to(DRAFT)).read_bytes()]
assert changed == expected
shutil.copytree(LIVE, HISTORY / 'before-v')
shutil.copytree(DRAFT, HISTORY / 'adopted-w')
for source in draft_files:
    shutil.copy2(source, LIVE / source.relative_to(DRAFT))
snapshot = ROUND / 'snapshots/candidate-w'
shutil.copytree(DRAFT, snapshot)

corpus = copy.deepcopy(read(OLD / 'planning/single-five-case.json'))
original = read(OLD / 'planning/single-five-case.json')['cases'][0]
assert len(corpus['cases']) == 1
case = corpus['cases'][0]
case['case_id'] = 'R20-C1'
case['candidate'] = 'W'
case['phase'] = 'matched-development-actual-copy-and-content-geometry-before-generation'
case['source'] = 'Same R19 request/copy/conditions/ratio/assets, after complete R19 closure. W changes general first-generation co-design and conditional actual-font planning. This is matched development after feedback, not pre-held-out transfer or isolated causal proof.'
for ordinal, role in enumerate(case['roles'], 1):
    role['role_id'] = f'R20-C1-M{ordinal}'
assert all(case[key] == original[key] for key in ('request', 'copy', 'conditions', 'styles', 'count', 'ratios', 'assets'))
case_path = ROUND / 'planning/single-five-case.json'
write(case_path, corpus)
prior = read(OLD / 'planning/candidate-v-pre-generation-freeze.json')
helpers = []
for item in prior['actor_helpers']:
    source = Path(item['path'])
    assert pin(source) == item
    target = ROUND / source.relative_to(OLD)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    helpers.append(pin(target))
write(ROUND / 'planning/prepared-workspace.json', {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate': 'W',
    'case': pin(case_path), 'runtime': [pin(path) for path in sorted(snapshot.rglob('*')) if path.is_file()],
    'actor_helpers': helpers, 'native_calls': 0, 'jobs_prepared': 0,
    'previous_full_closure': pin(closure_path),
    'limits': ['This workspace is not the pre-generation freeze; all-five plan and authored guides must still be prepared and pinned.', 'No W native quality result exists.'],
})
write(HISTORY / 'adoption.json', {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate': 'W', 'previous': 'V',
    'previous_full_closure': pin(closure_path), 'draft': pin(TASK / 'history/w-draft/changed-files.json'),
    'scope_review': pin(scope_review), 'changed_files': changed,
    'runtime': [pin(path) for path in sorted((HISTORY / 'adopted-w').rglob('*')) if path.is_file()],
    'native_calls_at_adoption': 0, 'new_quality_gates': 0, 'quality_thresholds_changed': False,
    'changes': [
        'Complex supplied prose and practical information are concretized with actual fonts/copy and content-specific substantive image geometry before first native generation when an existing runtime is usable.',
        'A chosen actual-content relation determines viewpoint, scale, image editing and copy shape together; material or entry-word changes over a common pictorial opening do not define separate systems.',
        'Simple/no-copy/unsupported-runtime use stays on positive native briefs; user references take priority and guides remain authored planning inputs, not protected client layouts.',
    ],
    'limits': ['W has no native quality result at adoption.', 'Helper code, evaluation loop and thresholds are unchanged.', 'Authored guide font rendering does not certify final native font-file application.', 'Matched development changes planning, guides and instruction together; no isolated attribution.'],
})
print(json.dumps({'adopted': 'W', 'round': 20, 'requests': 1, 'makers': 5, 'jobs': 0, 'native_calls': 0, 'helpers': len(helpers)}))
