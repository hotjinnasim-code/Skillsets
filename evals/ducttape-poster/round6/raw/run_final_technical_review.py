"""Fresh read-only technical review of the finalized portable artifact."""
import argparse, datetime, hashlib, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--archive',required=True,type=Path);p.add_argument('--output-dir',required=True,type=Path)
a=p.parse_args();archive=a.archive.resolve();out=a.output_dir.resolve();out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs=[archive/x for x in ['archive-index.json','report.md','gallery.html','findings.md','raw/planning/final-evidence.json','raw/planning/procedural-recovery-decisions.json','raw/planning/transcription-discrepancies.json','raw/planning/review-trace-inventory.json']]
inputs += sorted((archive/'raw').glob('*.py'))
pins=[{'path':str(x),'sha256':sha(x)} for x in inputs]
prompt=f'''You are a fresh independent TECHNICAL evidence reviewer. Your input archive is {archive}. Your output directory is {out}.
Read the pinned inputs listed below, and relevant metadata/JSON files within this archive as needed. You may inspect archived evaluation code and the retained earlier technical audit report/inputs to check its six static findings. Do not view poster pixels, rescore images, generate/edit images, change any archive/input, inspect outside source absolute paths or earlier rounds, read credentials/configuration, use web/connectors, or spawn agents. The index maps original source identifiers to confined archived bytes; no source-path fallback is allowed.
Run the archived raw/audit_portable_archive.py against this archive, saving its complete output only to your output directory. Independently assess selected-role/case/stage/native/manifest/source association joins, all20 roles and all47 closed calls including unused stages, closure first/final SHA change decisions, exact emitted CLI report/input/session pins, raw seven-score preservation and pass/fail/not-assessable counts. Check portable path confinement and evidence-only behavior: it may preserve honestly invalid procedure but cannot waive incorrect structural associations.
Verify report/gallery claims against metadata, including three resumed makers, actual maximum3 CLI/recorded native concurrency, four contexts rather than twenty independent requests, native resolution limitations and the distinction between runtime provenance and semantic viewing. Serialized CLI image-tool events may be unavailable; do not turn stated view records into proof of actual viewing/order. Check that whitespace-only equality discrepancies and NOT_ASSESSABLE stages are disclosed without quietly changing the primary comparator or raw observations. A technically correct archive can retain visual quality FAIL or NOT_ASSESSABLE. Do not try to improve scores.
Save report.json and report.md, read them back, then return a concise result. JSON must include technical_integrity (PASS/FAIL/NOT_ASSESSABLE), checks with evidence, findings (severity, exact source location, reproduced or static concern, impact), files_read with actual SHA256, explicit limitations, and the separately reported archived visual/procedural gate. State any code defect that remains; do not assume the earlier fixes work. Missing completion or files must remain explicit.
Pinned inputs: {json.dumps(pins,ensure_ascii=False)}
'''
(out/'prompt.txt').write_text(prompt)
argv=['codex','--no-daemon','--ask-for-approval','never','exec','--ephemeral','--json','--skip-git-repo-check','--sandbox','workspace-write','-C',str(out),'--output-last-message',str(out/'final.txt'),'-']
launch={'started_utc':utc(),'argv':argv,'fresh_session':True,'model_override':None,'input_pins':pins,'prompt':{'path':str(out/'prompt.txt'),'sha256':sha(out/'prompt.txt')},'scope':'Technical evidence review only; no new visual critic, rescore or production feedback.'}
(out/'launch.json').write_text(json.dumps(launch,ensure_ascii=False,indent=2))
with (out/'prompt.txt').open() as stdin,(out/'trace.jsonl').open('x') as stdout,(out/'stderr.log').open('x') as stderr:process=subprocess.run(argv,stdin=stdin,stdout=stdout,stderr=stderr)
events=[json.loads(x) for x in (out/'trace.jsonl').read_text().splitlines() if x.strip()]
sessions=[x['thread_id'] for x in events if x.get('type')=='thread.started']
completion={**launch,'completed_utc':utc(),'exit_code':process.returncode,'session_ids':sessions,'input_pins_unchanged':all(sha(Path(x['path']))==x['sha256'] for x in pins),'outputs':{x.name:{'path':str(x),'sha256':sha(x)} for x in out.iterdir() if x.is_file()}}
(out/'completion.json').write_text(json.dumps(completion,ensure_ascii=False,indent=2))
print(json.dumps({'exit_code':process.returncode,'session_ids':sessions,'inputs_unchanged':completion['input_pins_unchanged'],'report_saved':(out/'report.json').is_file()}))
