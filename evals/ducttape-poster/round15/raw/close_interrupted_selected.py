"""ROOT-only record of an authoritatively stopped phase. No critic replacement."""
from pathlib import Path
import datetime,hashlib,json,shlex,subprocess,sys
R=Path(__file__).resolve().parent
P=('editorial','craft','portfolio')
PY='/Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def read(p):return json.loads(p.read_bytes())
def pin(p):return {'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def save(p,v):
 with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def main():
 d=R/'reviews/R15-C1/selected';snapshot=subprocess.check_output(['ps','-axo','pid=,ppid=,command='],text=True)
 live=[]
 for line in snapshot.splitlines():
  parts=line.strip().split(None,2)
  if len(parts)!=3:continue
  try:a=shlex.split(parts[2])
  except ValueError:continue
  if not a:continue
  name=Path(a[0]).name
  actor=('codex' in name and 'exec' in a) or (name.startswith('python') and any(Path(x).name in ('run_agent.py','run_pool.py') for x in a[1:]))
  if actor:live.append({'pid':parts[0],'ppid':parts[1],'argv':a})
 assert not live,live
 rows=[]
 for profile in P:
  folder=d/'cli'/profile;launch=read(folder/'launch.json')
  assert not (folder/'completion.json').exists()
  assert not any((folder/(profile+s)).exists() for s in ('.json','.md','.observations.json'))
  events=[json.loads(l) for l in (folder/'trace.jsonl').read_text().splitlines() if l.strip()]
  sessions=[e['thread_id'] for e in events if e.get('type')=='thread.started']
  assert len(sessions)==1 and not any(e.get('type')=='turn.completed' for e in events)
  for p in launch['input_pins']:assert pin(Path(p['path']))['sha256']==p['sha256']
  rows.append({'profile':profile,'session':sessions[0],'launch':pin(folder/'launch.json'),'trace':pin(folder/'trace.jsonl'),'job':pin(d/'jobs'/(profile+'.json')),'completion_available':False,'reports_available':False,'exit_code':None,'observed_terminal_state':'process absent and tool handle missing following explicit turn_aborted; no invented completion','input_pins_unchanged_at_observation':True})
 assert len({r['session'] for r in rows})==3
 marker={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Intentional parent turn interruption; runner/CLI processes and exec handle are absent. All three launched selected critics stopped before producing final raw/compatibility reports.','sessions':rows,'live_actor_processes':live,'process_snapshot_sha256':hashlib.sha256(snapshot.encode()).hexdigest(),'native_production_unchanged':True,'replacement_sessions':0,'original_quality_gates_unchanged':True,'effective_selected_gate':'NA','completed_selected_reviews':0,'selected_valid_scores':0}
 save(d/'interrupted-phase.json',marker)
 cmds=[[PY,'-B',str(R/'summarize.py'),'--packet',str(d/'packet.json'),'--completions-dir',str(d/'cli'),'--output',str(d/'summary.json')],
       [PY,'-B',str(R/'audit_source_assets.py'),'--packet',str(d/'packet.json'),'--report-dir',str(d/'cli'),'--output',str(d/'source-asset-audit.json')],
       [PY,'-B',str(R/'method-recording-v2/audit_compact_bindings.py'),'--packet',str(d/'packet.json'),'--report-dir',str(d/'cli'),'--output',str(d/'compact-recording-audit.json')]]
 for profile in P:cmds[0].extend(['--report',profile+'='+str(d/'cli'/profile/(profile+'.json'))])
 for cmd in cmds:
  r=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
  assert r.returncode==0,(cmd,r.stdout,r.stderr)
 s=read(d/'summary.json');a=read(d/'source-asset-audit.json');b=read(d/'compact-recording-audit.json')
 assert s['procedure_gate']==s['set_gate']=='NA' and s['image_gate_counts']=={'PASS':0,'FAIL':0,'NA':5}
 assert s['counts']['valid_integer_1_to_5_score_values']==0 and a['gate']==b['gate']=='NA'
 save(d/'whole-phase-closure.json',{'closed_as':'authoritatively_interrupted_not_evaluated','observed_utc':marker['observed_utc'],'interruption':pin(d/'interrupted-phase.json'),'summary':pin(d/'summary.json'),'source_audit':pin(d/'source-asset-audit.json'),'compact_binding':pin(d/'compact-recording-audit.json'),'original_image_gate_counts':s['image_gate_counts'],'original_set_gate':s['set_gate'],'actual_started_sessions':3,'actual_completed_sessions':0,'replacement_sessions':0})
 print(json.dumps({'status':'STOPPED_RETAINED_AS_NA','started':3,'completed':0,'valid_selected_scores':0,'selected_image_gate_counts':s['image_gate_counts']}))
if __name__=='__main__':main()
