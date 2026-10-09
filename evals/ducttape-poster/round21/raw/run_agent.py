"""Run one fresh native-tool Codex agent and preserve its actual provenance."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--job',type=Path,required=True)
a=p.parse_args();job=json.loads(a.job.read_text());out=Path(job['output_dir']);out.mkdir(parents=True,exist_ok=True)
sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
pins=[{'path':str(Path(x).resolve()),'sha256':sha(x)} for x in job['inputs']]
prompt=Path(job['prompt_file']);argv=['codex','--no-daemon','--ask-for-approval','never','exec','--ephemeral','--json','--skip-git-repo-check','--sandbox','workspace-write','-C',str(out),'--output-last-message',str(out/'final.txt'),'-']
launch={'started_utc':utc(),'argv':argv,'fresh_session':True,'case_id':job['case_id'],'wave':job['wave'],'profile':job['profile'],'model_override':None,'prompt':{'path':str(prompt),'sha256':sha(prompt)},'input_pins':pins,'job':{'path':str(a.job.resolve()),'sha256':sha(a.job)}}
with (out/'launch.json').open('x') as f:json.dump(launch,f,ensure_ascii=False,indent=2)
print(json.dumps({'event':'started','profile':job['profile'],'utc':launch['started_utc']}),flush=True)
with prompt.open() as stdin,(out/'trace.jsonl').open('x') as stdout,(out/'stderr.log').open('x') as stderr:
 proc=subprocess.run(argv,stdin=stdin,stdout=stdout,stderr=stderr)
events=[json.loads(x) for x in (out/'trace.jsonl').read_text().splitlines() if x.strip()]
sessions=[x['thread_id'] for x in events if x.get('type')=='thread.started']
reports={}
for name in job['expected_outputs']:
 path=out/name
 if path.is_file():reports[name]={'path':str(path),'sha256':sha(path)}
completion={**launch,'completed_utc':utc(),'exit_code':proc.returncode,'session_ids':sessions,'turn_completed_count':sum(x.get('type')=='turn.completed' for x in events),'input_pins_unchanged':all(sha(x['path'])==x['sha256'] for x in pins),'trace':{'path':str(out/'trace.jsonl'),'sha256':sha(out/'trace.jsonl')},'reports':reports}
with (out/'completion.json').open('x') as f:json.dump(completion,f,ensure_ascii=False,indent=2)
print(json.dumps({'event':'completed','profile':job['profile'],'exit_code':proc.returncode,'sessions':sessions,'input_pins_unchanged':completion['input_pins_unchanged'],'outputs':list(reports)}),flush=True)
