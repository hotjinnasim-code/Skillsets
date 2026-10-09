"""Root-only run of unchanged frozen quality/source plus compact binding helpers."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
PROFILES=('editorial','craft','portfolio')
PYTHON='/Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def pin(p):
 b=p.read_bytes();return {'path':str(p.resolve()),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--wave',choices=['initial','selected'],required=True);a=p.parse_args()
 d=ROOT/'reviews/R13-C1'/a.wave;state=json.loads((d/'readiness.json').read_bytes());assert state['status']=='READY'
 assert state['mode']=='THREE_FRESH_COMPLETE_CRITICS','Whole original record reuse must use the explicit reuse path, not new sessions.'
 completions=[]
 for profile in PROFILES:
  c=json.loads((d/'cli'/profile/'completion.json').read_bytes())
  assert c['exit_code']==0 and c['input_pins_unchanged'] is True and len(c['session_ids'])==1
  completions.append(c)
 assert len({c['session_ids'][0] for c in completions})==3
 for c in completions:
  for n in (c['profile']+'.observations.json',c['profile']+'.json',c['profile']+'.md'):
   assert n in c['reports'], 'Missing actual in-session output retained; do not export afterward.'
 cmds=[[PYTHON,str(ROOT/'summarize.py'),'--packet',str(d/'packet.json'),'--completions-dir',str(d/'cli'),'--output',str(d/'summary.json')],
       [PYTHON,str(ROOT/'audit_source_assets.py'),'--packet',str(d/'packet.json'),'--report-dir',str(d/'cli'),'--output',str(d/'source-asset-audit.json')],
       [PYTHON,str(ROOT/'method-recording-v2/audit_compact_bindings.py'),'--packet',str(d/'packet.json'),'--report-dir',str(d/'cli'),'--output',str(d/'compact-recording-audit.json')]]
 for profile in PROFILES:cmds[0].extend(['--report',profile+'='+str(d/'cli'/profile/(profile+'.json'))])
 for cmd in cmds:
  result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);assert result.returncode==0,(cmd,result.stdout,result.stderr)
 result=json.loads((d/'summary.json').read_bytes());src=json.loads((d/'source-asset-audit.json').read_bytes());compact=json.loads((d/'compact-recording-audit.json').read_bytes())
 record={'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wave':a.wave,'all_three_closed':True,'sessions':[c['session_ids'][0] for c in completions],'summary':pin(d/'summary.json'),'source_audit':pin(d/'source-asset-audit.json'),'compact_binding':pin(d/'compact-recording-audit.json'),'original_procedure_gate':result['procedure_gate'],'original_image_gate_counts':result['image_gate_counts'],'original_set_gate':result['set_gate'],'source_gate':src['gate'],'recording_gate':compact['gate'],'counts':result['counts']}
 with (d/'whole-phase-closure.json').open('x') as f:json.dump(record,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps(record,ensure_ascii=False))
if __name__=='__main__':main()
