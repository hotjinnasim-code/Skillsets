#!/usr/bin/env python3
"""Fresh CLI critics; no generation, score aggregation, or automatic retry."""
from pathlib import Path
import argparse, concurrent.futures, datetime, hashlib, json, subprocess, time

r = Path(__file__).resolve().parent
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--concurrency', type=int, default=3)
a = p.parse_args()
assert 1 <= a.concurrency <= 3
read = lambda path: json.loads(Path(path).read_text())
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
closed = read(r/'planning/calls-closed.json')
assert closed['status'] == 'PASS' and closed['call_phase'] == 'CLOSED'
assert len(closed['completed_selection_roles']) == 20
launch_root = r/'cli-reviews'
launch_root.mkdir(exist_ok=False)
profiles = ['editorial', 'craft', 'portfolio']
jobs = []
for c in read(r/'planning/cases.json')['cases']:
    closure = read(r/'planning'/f'{c["id"]}-ordinary-closed.json')
    for wave in dict.fromkeys(closure['review_waves'].values()):
        for profile in profiles:
            jobs.append((wave, profile))
assert len(jobs) <= 24
plan = {
    'created_utc': utc(), 'transport': 'fresh Codex CLI exec; no-daemon, ephemeral, no resume/fork',
    'calls_closed': {'path': str(r/'planning/calls-closed.json'), 'sha256': sha(r/'planning/calls-closed.json')},
    'concurrency': a.concurrency, 'primary_assignments': len(jobs),
    'model_override': None, 'automatic_retry': False,
    'no_generation_or_feedback_to_production': True,
    'jobs': [{'wave': w, 'profile': q} for w,q in jobs]
}
with (launch_root/'dispatch-plan.json').open('x') as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)

def run(job):
    wave, profile = job
    folder = r/f'blind-{wave}'
    launch = launch_root/wave/profile
    launch.mkdir(parents=True, exist_ok=False)
    prompt = f'''You are one independent external poster critic in a fresh session. Your profile is {profile}.
Your only allowed input directory is {folder}. Do not inspect its parent, other packets, private mappings, production, skills, prompts, plans, histories, peer reviews or expected score targets. Do not search the web, use connectors, spawn agents, generate or edit images, or alter any existing input. You may only create your own three review files in this packet's reviews directory. Do not open other profiles' files.

Read review-protocol.md for the unchanged rubric/schema. Then read preflight.json FIRST, without packet.json/full copy. For every listed image actually call the available view_image tool on the exact usage720 path, manually transcribe each named full printed field from pixels. Save reviews/{profile}-action-first.json and read it back through a tool BEFORE opening packet.json. Empty preflight images means save/read back unchanged empty viewed/readings arrays; do not view the packet early. These first observations must remain unchanged after supplied-copy cross-check.

Only then read packet.json, full user request/copy/conditions. Actually view each of its FIVE images at all THREE exact provided paths (native, usage720, thumbnail320) with the image-view tool, FIFTEEN views. Use original detail if supported; do not create altered/cropped substitute images, use OCR, infer a view from a statement, or paste expected copy into observed fields. Record actual image_id/view/path. Note any viewer limitation in method/uncertainties rather than hiding it. Read every full provided string manually from the image; normalise whitespace only for equal, preserving actual punctuation and disagreements. Pixel ambiguity stays uncertain. All required copy must be legible at720, even if tiny details cannot be read at320.

Give all seven integer1–5 scores with located visible evidence, mandatory boolean/issues/uncertainties/transcription/use_readings, and whole five-member set diversity/closest-pair evidence per review-protocol.md. Preserve low scores and genre-faithful judgments: explicitly requested 3D/color is judged for execution, not banned by genre; minimal monochrome is not automatically high end. Do not claim human authorship or actual physical/printing performance. Do not average or aim for a pass.

Save reviews/{profile}.json and reviews/{profile}.md with EXACT schemas in review-protocol.md, read your own saved files back and verify their complete coverage. Schema uses scores/evidence keys content_form,hierarchy,typography,space,image_material,emotion_control,ai_slop; mandatory.use_readings includes boolean all_required_copy_legible_at720 plus observations. Main viewed must contain all15 actual view records; sets keys exactly the case keys in packet.cases and packet.sets. Preflight viewed has view usage720, and readings.fields keys exactly requested field names; full `_line` fields mean the whole printed line/sentence, and URL means entire displayed URL. For each transcription required is exact supplied string; observed remains what you read, not rewritten to match.

Do not silently replace adverse observations. Complete one review only, then return compact saved paths and concrete residual findings. Your files become immutable when this process completes. No fresh peer review or generation can be requested by you.
'''
    (launch/'prompt.txt').write_text(prompt)
    argv = ['codex','--no-daemon','--ask-for-approval','never','exec','--ephemeral','--json',
            '--skip-git-repo-check','--sandbox','workspace-write','-C',str(folder),
            '--output-last-message',str(launch/'final.txt'),'-']
    before = {x.name: sha(x) for x in [folder/'packet.json', folder/'preflight.json',folder/'review-protocol.md']}
    meta = {'started_utc':utc(), 'wave':wave,'profile':profile,'argv':argv,
            'prompt':{'path':str(launch/'prompt.txt'),'sha256':sha(launch/'prompt.txt')},
            'input_pins':before, 'model_override':None, 'fresh_session':True,
            'scope':'One opaque complete case; no prior conversation supplied'}
    with (launch/'launch.json').open('x') as f: json.dump(meta,f,ensure_ascii=False,indent=2)
    print(json.dumps({'event':'started','wave':wave,'profile':profile,'utc':meta['started_utc']}),flush=True)
    with (launch/'prompt.txt').open() as inp,(launch/'trace.jsonl').open('x') as out,(launch/'stderr.log').open('x') as err:
        process = subprocess.run(argv,stdin=inp,stdout=out,stderr=err)
    reports = {}
    for suffix in ['-action-first.json','.json','.md']:
        path = folder/'reviews'/f'{profile}{suffix}'
        if path.is_file(): reports[path.name]={'path':str(path),'sha256':sha(path)}
    after = {x.name:sha(x) for x in [folder/'packet.json',folder/'preflight.json',folder/'review-protocol.md']}
    result = {**meta,'completed_utc':utc(),'exit_code':process.returncode,
              'input_pins_unchanged':before==after,'reports':reports,
              'trace':{'path':str(launch/'trace.jsonl'),'sha256':sha(launch/'trace.jsonl')},
              'stderr':{'path':str(launch/'stderr.log'),'sha256':sha(launch/'stderr.log')}}
    with (launch/'completion.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'event':'completed','wave':wave,'profile':profile,'exit_code':process.returncode,'report_files':len(reports),'utc':result['completed_utc']}),flush=True)
    return result

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=a.concurrency) as pool:
    futures = [pool.submit(run,j) for j in jobs]
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())
with (launch_root/'all-completed.json').open('x') as f:
    json.dump({'completed_utc':utc(),'assignments':len(results),'results':results,
               'automatic_retry':False,'quality_assessment':'Raw visual reviewers, not determined by process exit'},f,ensure_ascii=False,indent=2)
print(json.dumps({'event':'all-completed','assignments':len(results),'exit_failures':sum(x['exit_code']!=0 for x in results)}),flush=True)
