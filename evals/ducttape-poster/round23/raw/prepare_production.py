#!/usr/bin/env python3
"""Prepare isolated, pinned single-five maker jobs; never launch agents or image calls.

Invoke only after the coordinator, corpus/assets, snapshot and helpers are frozen.
--self-test uses temporary metadata fixtures, never the production corpus.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shlex
import struct
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUNDLED_PYTHON = Path('/Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
NATIVE_SKILL = Path('/Users/nahyeonbin/.codex/skills/.system/imagegen/SKILL.md')
SKILL_FILES = ('SKILL.md', 'agents/openai.yaml', 'references/art-direction.md',
               'references/parallel-production.md', 'references/visual-research.md',
               'references/evaluation-loop.md')
CASE_KEYS = {'case_id', 'phase', 'candidate', 'request', 'copy', 'count', 'ratios',
             'styles', 'conditions', 'roles', 'asset_readiness', 'source', 'purpose',
             'title', 'assets', 'held_out_after_feedback', 'held_out_from_development_critic_feedback'}
MAKER_CASE_KEYS = ('case_id', 'request', 'copy', 'count', 'ratios', 'styles', 'conditions')
IDENTIFIER = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]*\Z')
SHA256 = re.compile(r'[0-9a-f]{64}\Z')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_json(path):
    with Path(path).open(encoding='utf-8') as handle:
        return json.load(handle)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def pin(path):
    path = Path(path).resolve(strict=True)
    require(path.is_file(), f'Not a file: {path}')
    return {'path': str(path), 'sha256': digest(path)}


def canonical_digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def exclusive_json(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


def ratio_pair(value):
    if isinstance(value, str):
        match = re.fullmatch(r'([1-9][0-9]*):([1-9][0-9]*)', value)
        require(match is not None, f'Invalid width:height ratio: {value!r}')
        return tuple(map(int, match.groups()))
    require(isinstance(value, list) and len(value) == 2 and
            all(type(x) is int and x > 0 for x in value), f'Invalid ratio: {value!r}')
    return tuple(value)


def same_ratio(left, right):
    a, b = ratio_pair(left), ratio_pair(right)
    return a[0] * b[1] == b[0] * a[1]


def checked_assets(assets):
    require(isinstance(assets, list), 'Role assets must be an explicit list')
    result, seen = [], set()
    for asset in assets:
        require(isinstance(asset, dict) and asset.get('ready') is True, 'Every assigned asset must be ready')
        require(isinstance(asset.get('asset_id'), str) and asset['asset_id'] not in seen, 'Duplicate/missing asset_id')
        seen.add(asset['asset_id'])
        for path_key, hash_key in (('actual_path', 'sha256'), ('manifest_path', 'manifest_sha256')):
            path, expected = asset.get(path_key), asset.get(hash_key)
            require(isinstance(path, str) and Path(path).is_absolute(), f'{path_key} must be absolute')
            require(isinstance(expected, str) and SHA256.fullmatch(expected), f'Invalid {hash_key}')
            actual = pin(path)
            require(actual['sha256'] == expected, f'Changed assigned asset: {path}')
            result.append(actual['path'])
        require(all(type(asset.get(key)) is int and asset[key] > 0 for key in ('width', 'height')), 'Invalid asset dimensions')
        with Path(asset['actual_path']).open('rb') as handle:
            header = handle.read(24)
        require(len(header) == 24 and header[:8] == b'\x89PNG\r\n\x1a\n' and header[12:16] == b'IHDR', 'Assigned asset must be a PNG')
        require(struct.unpack('>II', header[16:24]) == (asset['width'], asset['height']), 'Asset dimensions differ from PNG header')
        manifest = read_json(asset['manifest_path'])
        original = manifest.get('original', {})
        require(original.get('sha256') == asset['sha256'] and
                Path(original.get('path', '')).resolve() == Path(asset['actual_path']).resolve(), 'Asset manifest original binding mismatch')
        if 'measured_layout' in asset:
            require(asset['measured_layout'] == manifest.get('measured_layout'), 'Protected layout differs from frozen asset manifest')
    return result


def validate_case(case, is_d1=False):
    require(isinstance(case, dict), 'Case must be an object')
    require(not (set(case) - CASE_KEYS), f'Unknown case fields need explicit sanitization: {sorted(set(case) - CASE_KEYS)}')
    cid = case.get('case_id')
    require(isinstance(cid, str) and IDENTIFIER.fullmatch(cid), 'Invalid case_id')
    require(isinstance(case.get('request'), str) and case['request'], f'{cid}: missing literal request')
    require(type(case.get('count')) is int and case['count'] >= 1, f'{cid}: response-only/conflicting or invalid count; no image jobs invented')
    require(isinstance(case.get('copy'), list), f'{cid}: explicit copy array required')
    for entry in case['copy']:
        require(isinstance(entry, dict) and isinstance(entry.get('text'), str) and
                entry.get('kind') in ('text', 'url') and type(entry.get('fixed_newlines')) is bool, f'{cid}: invalid copy entry')
    require(isinstance(case.get('conditions'), list), f'{cid}: conditions must be a list')
    ratios = case.get('ratios')
    require(isinstance(ratios, list) and len(ratios) == case['count'], f'{cid}: ratios/count mismatch')
    for ratio in ratios:
        ratio_pair(ratio)
    roles = case.get('roles')
    if is_d1 and roles is None:
        roles = [{'role_id': f'{cid}-M{i}', 'ordinal': i, 'ratio': ratios[i-1], 'assets': [],
                  'native_attempt_limit': 3, 'own_correction_limit': 2} for i in range(1, case['count'] + 1)]
    require(isinstance(roles, list) and len(roles) == case['count'], f'{cid}: roles/count mismatch')
    ordered = sorted(roles, key=lambda role: role.get('ordinal', -1) if isinstance(role, dict) else -1)
    for i, role in enumerate(ordered, 1):
        require(isinstance(role, dict) and type(role.get('ordinal')) is int and role['ordinal'] == i and
                role.get('role_id') == f'{cid}-M{i}', f'{cid}: role identity/ordinal mismatch')
        require(same_ratio(role.get('ratio'), ratios[i-1]), f'{cid}: assigned ratio mismatch')
        require(type(role.get('native_attempt_limit')) is int and role['native_attempt_limit'] == 3 and
                type(role.get('own_correction_limit')) is int and role['own_correction_limit'] == 2, f'{cid}: bounded call limits changed')
        require(isinstance(role.get('assets'), list), f'{cid}: missing explicit assets array')
    return ordered


def maker_prompt(assignment, own_case, paths, role_dir, python):
    role = assignment['role']
    required_reads = '\n'.join(f'- {p}' for p in paths)
    own_assets = json.dumps(assignment['assets'], ensure_ascii=False, indent=2)
    helper = assignment['evidence_helper']['path']
    save = ' '.join(map(shlex.quote, (str(python), helper, 'save-native', '--role', role,
                                     '--stage', 'STAGE', '--source', 'EXACT_RETURNED_ABSOLUTE_PATH', '--role-dir', str(role_dir))))
    seal = ' '.join(map(shlex.quote, (str(python), helper, 'finalize', '--role-dir', str(role_dir), '--selected-stage', 'CHOSEN_STAGE')))
    return f'''You are one fresh, isolated ducttape-poster maker. Own exactly {role}, one final independent poster.
Your working/output directory is {role_dir}. Do not spawn agents or create tasks. Do not read the full corpus, coordinator plans, other makers' directions/prompts/results, critic files, prior rounds, parent evaluation history or unrelated projects. Only read this job's pinned inputs and your own newly written evidence (plus the exact native source paths explicitly returned by your own tool). Never run another project executable or a wrapper/image-generation API, SDK, image CLI, credential/config/environment lookup. The only project helper you may execute is the pinned evidence_io.py below. Read-only access to exact pinned text and own-directory exclusive metadata writes/hash checks using the bundled Python are allowed. No Python/Pillow image or asset editing; the helper's QA-only reduction is the only pixel operation.

First read these exact pinned inputs, applying the current SKILL and needed references. Read review_rules.md's native evidence/transcription contract. The evaluation reference does not authorize you to judge or inspect peers/critics:
{required_reads}
Read case.json and assignment.json. They contain the complete literal user input/common conditions and ONLY your assigned direction. Before designing, actually view every supplied image with tools.view_image through functions.exec, emitting it via image(...,'original'). Honor each supplied asset role and every requested identity/style/ratio/copy condition. Preserve reference geometry or measured_layout only when the user requests composition/position/proportion preservation; a style-only reference does not impose its coordinates. Old reference-poster copy is not new copy. All supplied images for this role are:
{own_assets}

COMPLETE ORIGINAL USER REQUEST (maker understanding and full verification context, not a compulsory native-prompt prefix):
{own_case['request']}

ALL LITERAL COPY ENTRIES (full verification context; initial native spec prints this copy once, preserving exact strings, kinds, word spaces, punctuation and fixed-newline rules):
{json.dumps(own_case['copy'], ensure_ascii=False, indent=2)}

COMMON USER CONDITIONS/STYLES/RATIOS (honor every applicable condition in the result; the role's ratio is {json.dumps(assignment['ratio'], ensure_ascii=False)}):
{json.dumps({k: own_case[k] for k in ('conditions', 'styles', 'ratios') if k in own_case}, ensure_ascii=False, indent=2)}
COMMON COORDINATOR CONSTRAINTS:
{json.dumps(assignment['common_constraints'], ensure_ascii=False, indent=2)}
YOUR OWN DIRECTION, no peer plan:
{json.dumps(assignment['direction'], ensure_ascii=False, indent=2)}

Keep the complete request and verification record separate from a focused native production spec. Apply the skill's native-input boundary: exact printed copy once in the initial spec, all relevant client constraints, and your chosen concrete whole visual design. Do not mechanically prepend the request, copy JSON, plan JSON, rubric, or reference commentary to the tool prompt. Repairs state the observed change and protected relationships; retain any exact text needed for that edit and verify the entire copy after return. Do not drop necessary constraints to shorten a prompt.

Native generation ONLY: tools.image_gen__imagegen via functions.exec, exactly one single flat opaque poster per call, transparent_background:false, assigned width:height ratio. No multi-poster comparison panels, contact sheet, mockup or extra experiment image. A single finished poster may contain legitimate content-based image sequences or information modules as its chosen layout. For this aspect-only case, include: "요청한 화면 비율을 유지하면서 현재 도구와 모델이 지원하는 가능한 최대 해상도로 출력". Explicit user pixel dimensions or lower-resolution requests take precedence; for those requests use the specified output size instead. This is a request, not proof of maximum output; measure the returned native dimensions.
The predeclared ratio policy permits nearest-integer native rounding of one edge, <=0.5 pixel from the exact requested ratio on one dimension. Report actual dimensions, never resize or claim mathematically exact ratio, and do not spend a repair only on permitted rounding. Materially wrong aspect ratio still needs correction. This tolerance never overrides an explicit pixel-size request.
One initial attempt plus at most TWO own repairs, including actual failed native attempts: at most three native invocations for this role/candidate, named initial, repair-1, repair-2 in that order. A new role name or regeneration does not reset the budget. Correct only your own actually inspected defects while retaining the specified genre and user constraints. Do not claim quality PASS or assign scores from self-inspection. Do not seek or receive external critic scores before exclusive selection closure.

BEFORE EACH invocation, exclusively create stages/STAGE/call-input.json containing the COMPLETE EXACT JSON argument object that will be passed to tools.image_gen__imagegen (do not add metadata-only arguments). Separately exclusively create pre-call.json with role, stage, prepared_at_utc, native_tool, complete planned argument/input hash pins, supplied reference pins, own observed repair cause/maintained features, and attempt number. Save both before starting; do not retrofit them after a return. Keep the identical argument object in runtime store for the native invocation. Fresh initial without supplied references omits BOTH referenced_image_paths and num_last_images_to_include. With supplied assets, actually pass ALL required local asset paths using referenced_image_paths; omit num_last_images_to_include. For a bounded repair with a previous returned inspected own image, pass that exact own target and all required client assets using referenced_image_paths, never a peer result. If the immediate prior attempt failed, use the last actually returned inspected own target if any; otherwise make a fresh bounded retry with required client assets and no invented repair target. Preserve immediate-attempt failure evidence and record the actual target stage separately when it differs. Never guess a newer file or use directory newest-file scanning.

The native functions.exec cell starts with exactly this directive:
// @exec: {{"yield_time_ms":120000,"max_output_tokens":1000}}
Before awaiting tools.image_gen__imagegen, store/emit the actual caller UTC start and role/stage. Emit meaningful native-wait status at intervals <=45 seconds via notify()/setTimeout while awaiting (no invented model percentage). Clear the timer on return/failure. Record actual caller UTC end and whether the invocation returned or failed; preserve explicit returned path/result hints and real error metadata separately in stages/STAGE/native-call.json after return. Its wrapper interval describes the awaited native call, not helper runtime or model internals. Do not print/notify raw result/base64; retain needed result metadata in runtime store and display the generated image with generatedImage(result) as supported. Never infer source paths or generation times from filenames/helper saved_at. When yielded, resume only that exec cell, without submitting the image call again.

For every returned PNG, obtain its exact absolute source path from the actual tool return, then execute the pinned helper with safely quoted exact paths:
{save}
Replace only STAGE/EXACT_RETURNED_ABSOLUTE_PATH with actual values. The helper saves byte-identical original.png/final.png, QA views and manifest.json. It does NOT edit typography, materials, crop or assets. If the returned source path is unavailable or preservation fails, preserve the actual error/tool evidence and report the unsealable return honestly; do not invent an image path or relabel a returned image as a failed native call. Stop for root handling rather than claiming a selectable asset.

ACTUALLY inspect EVERY returned stage before deciding another native invocation, in this exact order: original.png at native detail, usage-720.png, thumbnail-320.png. For native display use:
const v = await tools.view_image({{path: exactOriginalPath, detail:'original'}}); image(v.image_url,'original');
Use tools.view_image and image(...) for both QA files too. All three views must actually appear; generatedImage alone is not this inspection. Never mark viewed based only on the prompt or a helper exit. Write exclusive inspection.json with role, stage, actual_viewed:true ONLY when truthful, actual_view_paths:[exact original, exact usage720, exact thumbnail320], raw_observed_text:[], residuals:[], plus located observations and mandatory checks. Transcribe every copy entry verbatim as first observed, then record required text, normalized comparison under nfc-ws-optical-v1, layout fidelity and ambiguities separately. Do not silently normalize the raw read or guess ambiguous Hangul. Follow the one-revisit rule on the same pinned asset and retain its initial read. Check content-grounded substantive non-glyph concept, copy, assigned style, ratio/dimensions, Hangul proportions/counters/word spacing, information relationship, function/contact if requested, and local material/edge finish. Residuals are concrete observed limits, not self-awarded PASS.

Every returned repair needs exclusive parent-comparison.json: role, stage, parent_stage, parent_outcome:'returned'|'failure', the immediate parent's exact parent_manifest_sha256 and parent_native_sha256 OR parent_failure_sha256, changes:[], residuals:[]. Compare actually viewed returned stages, preserving earlier advantages; a failure parent has no visual comparison. Prefer the most suitable inspected result, not automatically the latest; preserve ALL returned originals, failures and unselected stages.
For each actual failed native invocation, write failure.json with role, stage, outcome:'failure', native_call_count:1, error:the actual recorded error. Preserve its pre-call/input/native-call evidence. Failures count in the three-attempt cap; no placeholder images or false inspection.

When one or more inspected native outcomes exist, choose the most suitable returned stage and execute only:
{seal}
Replace CHOSEN_STAGE with initial, repair-1 or repair-2. selection.json is exclusive and immutable before any critics. Do not alter stage inputs, images, observations, selected pins or selection after closure. The helper rejects missing/out-of-order outcomes and nonexistent comparisons. Do not also create unavailable.json.
ONLY when all THREE actual attempts failed, do not call finalize or fabricate selection.json. Exclusively write unavailable.json with schema_version:1, kind:'role_unavailable', case_id, role, outcome:'unavailable', closed:true, reason:actual failure explanation, counts:{{native_calls:3,returned:0,failed:3,repair_calls:2}}, stages:[{{stage,outcome:'failure',failure:{{path,sha256}},input_pins:{{call_input:{{path,sha256}},pre_call:{{path,sha256}}}},native_call:{{path,sha256}}}}] for all three preserved actual stages. selection.json and unavailable.json may NEVER coexist. Any interruption or returned-but-unsealable outcome is explicitly incomplete, not an invented all-failed terminal record.

Return a compact account of the true terminal path, selected native dimensions if any, actual call/repair/failure counts, and concrete unresolved limits. No quality score, universal guarantee or extra image generation.
'''


def prepare(root, corpus_path, case_ids, candidate_dir, native_skill=NATIVE_SKILL,
            python=BUNDLED_PYTHON, output_root=None):
    root, candidate_dir = Path(root).resolve(), Path(candidate_dir).resolve()
    output_root = Path(output_root or root / 'production').resolve()
    corpus = read_json(corpus_path)
    require(isinstance(corpus, dict) and isinstance(corpus.get('cases'), list), 'Corpus must contain cases[]')
    cases = {}
    for case in corpus['cases']:
        require(isinstance(case, dict) and isinstance(case.get('case_id'), str) and case['case_id'] not in cases, 'Duplicate/missing corpus case_id')
        cases[case['case_id']] = case
    require(len(case_ids) == len(set(case_ids)) and case_ids, 'Select each intended case exactly once')
    if 'R7-D1' in case_ids:
        d1 = read_json(root / 'planning/D1-case.json')
        require(d1.get('case_id') == 'R7-D1', 'D1 identity mismatch')
        if 'R7-D1' in cases:
            require(cases['R7-D1']['request'] == d1['request'] and cases['R7-D1']['copy'] == d1['copy'], 'Conflicting D1 sources')
        else:
            cases['R7-D1'] = d1
    capability = read_json(root / 'capability-probe/result.json')
    require(capability.get('native_imagegen_exposed') is True and capability.get('native_view_image_exposed') is True and
            capability.get('native_imagegen', {}).get('callable_name') == 'tools.image_gen__imagegen' and
            capability.get('native_imagegen', {}).get('invoked_via') == 'functions.exec' and
            capability.get('native_view_image', {}).get('callable_name') == 'tools.view_image' and
            capability.get('native_view_image', {}).get('invoked_via') == 'functions.exec', 'Native generation/view capability not confirmed')
    shared = [candidate_dir / name for name in SKILL_FILES] + [Path(native_skill), root / 'review_rules.md',
              root / 'evidence_io.py', root / 'run_agent.py', root / 'capability-probe/result.json', Path(__file__).resolve()]
    shared = [pin(path)['path'] for path in shared]
    require(Path(python).is_file(), 'Bundled Python does not exist')
    prepared = []
    # Validate all requested inputs before writing even the first assignment.
    for cid in case_ids:
        require(cid in cases, f'Missing case: {cid}')
        original_case = cases[cid]
        roles = validate_case(original_case, is_d1=(cid == 'R7-D1'))
        plan_path = root / ('coordinator/H-D1/plan.json' if cid == 'R7-D1' else f'coordinator/{cid}/plan.json')
        plan = read_json(plan_path)
        require(isinstance(plan, dict) and plan.get('case_id') == cid, f'{cid}: coordinator identity mismatch')
        for key in ('request', 'copy'):
            if key in plan:
                require(plan[key] == original_case[key], f'{cid}: coordinator changed literal {key}')
        directions = plan.get('directions')
        require(isinstance(directions, list) and len(directions) == len(roles), f'{cid}: directions/count mismatch')
        mapped = {}
        for direction in directions:
            require(isinstance(direction, dict) and isinstance(direction.get('role'), str) and direction['role'] not in mapped, f'{cid}: duplicate/missing direction role')
            mapped[direction['role']] = direction
        require(set(mapped) == {role['role_id'] for role in roles}, f'{cid}: coordinator/role mismatch')
        common = plan.get('common_constraints', [])
        require(isinstance(common, list) and all(isinstance(item, str) for item in common), f'{cid}: invalid common_constraints')
        for role in roles:
            rid = role['role_id']
            direction = mapped[rid]
            if 'ratio' in direction:
                require(same_ratio(direction['ratio'], role['ratio']), f'{rid}: direction ratio mismatch')
            assets = checked_assets(role['assets'])
            role_dir = output_root / rid
            require(not role_dir.exists(), f'Refusing existing role directory: {role_dir}')
            own_case = copy.deepcopy({key: original_case[key] for key in MAKER_CASE_KEYS if key in original_case})
            own_case['roles'] = [copy.deepcopy(role)]
            own_case['assets'] = copy.deepcopy(role['assets'])
            assignment = {'schema_version': 1, 'kind': 'maker_assignment', 'case_id': cid, 'role': rid,
                          'candidate': original_case.get('candidate', 'I'),
                          'ordinal': role['ordinal'], 'expected_count': original_case['count'], 'ratio': copy.deepcopy(role['ratio']),
                          'direction': copy.deepcopy(direction), 'common_constraints': copy.deepcopy(common),
                          'assets': copy.deepcopy(role['assets']), 'evidence_helper': pin(root / 'evidence_io.py'),
                          'source_digest': {'case_entry_sha256': canonical_digest(original_case),
                                            'case_entry_digest_method': 'UTF-8 canonical JSON, sorted keys, no extra whitespace',
                                            'coordinator_plan_sha256': digest(plan_path)},
                          'input_scope': 'One literal case/common input and one own role/direction; no corpus policies, peer plan or evaluation history.'}
            prepared.append((role_dir, own_case, assignment, assets))
    jobs = []
    for role_dir, own_case, assignment, assets in prepared:
        role_dir.mkdir(parents=True, exist_ok=False)
        case_path, assignment_path = role_dir / 'case.json', role_dir / 'assignment.json'
        prompt_path, job_path = role_dir / 'prompt.txt', role_dir / 'job.json'
        exclusive_json(case_path, own_case)
        assignment['case'] = pin(case_path)
        exclusive_json(assignment_path, assignment)
        reads = [str(case_path), str(assignment_path)] + shared + assets
        with prompt_path.open('x', encoding='utf-8') as handle:
            handle.write(maker_prompt(assignment, own_case, reads, role_dir, python))
        inputs = list(dict.fromkeys([str(case_path), str(assignment_path), str(prompt_path)] + shared + assets))
        # The runner hashes these exact own inputs at launch and completion. Source corpus/plan are deliberately absent.
        job = {'output_dir': str(role_dir), 'prompt_file': str(prompt_path), 'case_id': assignment['case_id'],
               'wave': f"{assignment['candidate']}-{assignment['case_id']}-production", 'profile': assignment['role'],
               'inputs': inputs, 'expected_outputs': ['selection.json', 'unavailable.json']}
        exclusive_json(job_path, job)
        jobs.append({'case_id': assignment['case_id'], 'role': assignment['role'], 'job': pin(job_path),
                     'assignment': pin(assignment_path), 'prompt': pin(prompt_path),
                     'run_command': [str(python), str(root / 'run_agent.py'), '--job', str(job_path)]})
    return {'prepared_jobs': len(jobs), 'jobs': jobs, 'launched': False,
            'terminal_contract': 'exclusive selection.json OR unavailable.json; unavailable only for all three actual failures'}


def self_test():
    with tempfile.TemporaryDirectory(prefix='r7-production-schema-') as temp:
        root = Path(temp)
        (root / 'planning').mkdir()
        (root / 'capability-probe').mkdir()
        (root / 'capability-probe/result.json').write_text(json.dumps({'native_imagegen_exposed': True, 'native_view_image_exposed': True,
             'native_imagegen': {'callable_name': 'tools.image_gen__imagegen', 'invoked_via': 'functions.exec'},
             'native_view_image': {'callable_name': 'tools.view_image', 'invoked_via': 'functions.exec'}}))
        for name in ('review_rules.md', 'evidence_io.py', 'run_agent.py', 'native-skill.md'):
            (root / name).write_text('METADATA FIXTURE ONLY\n')
        candidate = root / 'snapshots/candidate-i'
        for name in SKILL_FILES:
            path = candidate / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('METADATA SKILL FIXTURE ONLY\n')
        cases = []
        for cid, count in (('TOY-ONE', 1), ('TOY-THREE', 3)):
            case = {'case_id': cid, 'phase': 'toy', 'candidate': 'H', 'request': 'literal request',
                    'copy': [{'text': 'A · B\nC', 'kind': 'text', 'fixed_newlines': True}], 'count': count,
                    'ratios': ['2:3'] * count, 'styles': ['literal style'], 'conditions': ['literal condition'],
                    'roles': [{'role_id': f'{cid}-M{i}', 'ordinal': i, 'ratio': '2:3', 'assets': [],
                               'native_attempt_limit': 3, 'own_correction_limit': 2} for i in range(1, count+1)],
                    'asset_readiness': 'ready', 'source': 'metadata fixture'}
            cases.append(case)
            folder = root / 'coordinator' / cid
            folder.mkdir(parents=True)
            exclusive_json(folder / 'plan.json', {'case_id': cid, 'request': case['request'], 'copy': case['copy'],
                          'common_constraints': ['exact common constraint'], 'directions': [
                              {'role': r['role_id'], 'ratio': r['ratio'], 'concept': 'OWN-CONCEPT-' + r['role_id']} for r in case['roles']]})
        d1 = {'case_id': 'R7-D1', 'purpose': 'DO-NOT-PASS-DEVELOPMENT-FLAG', 'request': 'literal D1 title-only request',
              'copy': [{'text': 'A · B\nC', 'kind': 'text', 'fixed_newlines': True}], 'count': 5,
              'ratios': ['2:3'] * 5, 'conditions': ['literal D1 condition']}
        exclusive_json(root / 'planning/D1-case.json', d1)
        d1_plan = root / 'coordinator/H-D1/plan.json'
        d1_plan.parent.mkdir(parents=True)
        exclusive_json(d1_plan, {'case_id': 'R7-D1', 'request': d1['request'], 'copy': d1['copy'],
                       'common_constraints': ['exact D1 constraint'], 'directions': [
                           {'role': f'R7-D1-M{i}', 'ratio': '2:3', 'concept': f'OWN-CONCEPT-R7-D1-M{i}'} for i in range(1, 6)]})
        corpus_path = root / 'planning/single-five-case.json'
        exclusive_json(corpus_path, {'cases': cases, 'evaluator_only_policy': 'FORBIDDEN-EVALUATOR-MARKER', 'scoretargets': 'FORBIDDEN-SCORE-MARKER'})
        result = prepare(root, corpus_path, [c['case_id'] for c in cases] + ['R7-D1'], candidate, root / 'native-skill.md')
        assert result['prepared_jobs'] == 9 and result['launched'] is False
        for row in result['jobs']:
            job = read_json(row['job']['path'])
            assignment = read_json(row['assignment']['path'])
            own = read_json(assignment['case']['path'])
            assert len(own['roles']) == 1 and own['roles'][0]['role_id'] == row['role']
            assert not (set(own) & {'phase', 'candidate', 'source', 'purpose', 'asset_readiness', 'held_out_after_feedback', 'held_out_from_development_critic_feedback'})
            assert own['copy'][0]['text'] == 'A · B\nC'
            assert job['expected_outputs'] == ['selection.json', 'unavailable.json']
            assert str(corpus_path) not in job['inputs']
            assert not any('/coordinator/' in p for p in job['inputs'])
            prompt = Path(row['prompt']['path']).read_text()
            assert 'FORBIDDEN-EVALUATOR-MARKER' not in prompt and 'FORBIDDEN-SCORE-MARKER' not in prompt
            assert 'DO-NOT-PASS-DEVELOPMENT-FLAG' not in prompt
            for other in result['jobs']:
                if other['role'] != row['role']:
                    assert 'OWN-CONCEPT-' + other['role'] not in prompt
            assert 'tools.image_gen__imagegen via functions.exec' in prompt and '"yield_time_ms":120000' in prompt
            assert pin(row['job']['path']) == row['job']
        try:
            prepare(root, corpus_path, ['TOY-ONE'], candidate, root / 'native-skill.md')
        except ValueError as error:
            assert 'existing role directory' in str(error)
        else:
            raise AssertionError('Existing role directory was overwritten')
        return {'metadata_fixture_smoke': 'PASS', 'toy_cases': 3, 'toy_jobs': 9,
                'checks': ['literal copy', 'N=1/N=3/N=5 role counts', 'D1 special plan path and role adapter',
                           'own-only direction', 'no corpus policies/plans/evaluation flags passed',
                           'fresh runner interface', 'terminal exclusivity instruction', 'existing output rejected'],
                'production_prepared': False, 'agents_launched': False, 'images_generated_or_viewed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--corpus', type=Path)
    parser.add_argument('--case', action='append', dest='case_ids')
    parser.add_argument('--candidate-dir', type=Path)
    parser.add_argument('--output-root', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        require(not args.case_ids, '--self-test cannot prepare production cases')
        result = self_test()
    else:
        require(args.case_ids, 'Select frozen cases explicitly with --case; no automatic corpus-wide launch/preparation')
        result = prepare(args.root, args.corpus or args.root / 'planning/single-five-case.json', args.case_ids,
                         args.candidate_dir or args.root / 'snapshots/candidate-i', output_root=args.output_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
