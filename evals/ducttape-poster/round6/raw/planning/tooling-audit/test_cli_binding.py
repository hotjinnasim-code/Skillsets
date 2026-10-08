"""Synthetic metadata-only CLI binding regression; no actual critic scores/images."""
import copy, importlib.util, json, tempfile
from pathlib import Path

root_source=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('cli_provenance',root_source/'cli_provenance.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def put(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x));return p

results=[]
with tempfile.TemporaryDirectory(prefix='r6-metadata-only-') as d:
    r=Path(d).resolve();w='TOY';p='editorial';b=r/'cli-reviews'/w/p
    closed=put(r/'planning/calls-closed.json',{'closed_utc':'2026-01-01T00:00:00+00:00'})
    plan=put(r/'cli-reviews/dispatch-plan.json',{'jobs':[{'wave':w,'profile':p}], 'primary_assignments':1,'automatic_retry':False,'calls_closed':{'path':str(closed),'sha256':m.sha(closed)}})
    prompt=put(b/'prompt.txt',{'synthetic':True})
    trace=b/'trace.jsonl';trace.write_text(json.dumps({'type':'thread.started','thread_id':'synthetic-session'})+'\n'+json.dumps({'type':'turn.completed'})+'\n')
    raw={f'{p}{s}':put(r/f'blind-{w}/reviews'/f'{p}{s}',{'synthetic':True}) for s in ['-action-first.json','.json','.md']}
    pins={'packet.json':'toy-pin','preflight.json':'toy-pin','review-protocol.md':'toy-pin'}
    launch={'wave':w,'profile':p,'dispatch_plan':{'path':str(plan),'sha256':m.sha(plan)},'argv':['codex','--no-daemon','--ask-for-approval','never','exec','--ephemeral','--json','-C',str(r/f'blind-{w}')],'fresh_session':True,'model_override':None,'raw_outputs_absent_at_dispatch':True,'input_pins':pins,'prompt':{'path':str(prompt),'sha256':m.sha(prompt)},'started_utc':'2026-01-01T00:01:00+00:00'}
    done={**copy.deepcopy(launch),'exit_code':0,'input_pins_unchanged':True,'reports':{n:{'path':str(x),'sha256':m.sha(x)} for n,x in raw.items()},'trace':{'path':str(trace),'sha256':m.sha(trace)},'cli_session_id':'synthetic-session','completed_utc':'2026-01-01T00:02:00+00:00'}
    def check(name,l,c,expected):
        put(b/'launch.json',l);put(b/'completion.json',c)
        proc,errors=m.check_cli_assignment(r,w,p,pins,raw)
        assert proc['cli_assignment_valid'] is expected,(name,errors)
        results.append({'test':name,'passed':True,'valid_expected':expected,'errors':errors})
    check('valid metadata-only assignment',launch,done,True)
    c=copy.deepcopy(done);c['reports'][p+'.json']['sha256']='wrong';check('swapped raw bytes',launch,c,False)
    c=copy.deepcopy(done);c['input_pins']['packet.json']='wrong';check('different sealed input',launch,c,False)
    l=copy.deepcopy(launch);l['argv'][4]='resume';c={**copy.deepcopy(done),'argv':l['argv']};check('nonfresh argv',l,c,False)
    l=copy.deepcopy(launch);l['raw_outputs_absent_at_dispatch']=False;c={**copy.deepcopy(done),'raw_outputs_absent_at_dispatch':False};check('preexisting raw declaration',l,c,False)
    c=copy.deepcopy(done);c['cli_session_id']='different';check('session mismatch',launch,c,False)
    l=copy.deepcopy(launch);l['started_utc']='2025-12-31T23:00:00+00:00';c={**copy.deepcopy(done),'started_utc':l['started_utc']};check('launch before production close',l,c,False)
    c=copy.deepcopy(done);c['exit_code']=1;check('failed process',launch,c,False)
print(json.dumps({'scope':'Synthetic metadata only; no actual R6 quality observations','checks':len(results),'results':results},indent=2))
