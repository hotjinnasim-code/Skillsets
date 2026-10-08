"""Mechanical fresh CLI assignment binding; no proof of semantic viewing/order."""
from pathlib import Path
import datetime, hashlib, json

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check_cli_assignment(root, wave, profile, packet_pins, raw_paths):
    root=Path(root).resolve();base=root/'cli-reviews'/wave/profile
    read=lambda p:json.loads(Path(p).read_text())
    errors=[]
    def need(ok,msg):
        if not ok:errors.append(msg)
    launch_path=base/'launch.json';completed_path=base/'completion.json'
    launch=read(launch_path);done=read(completed_path);plan=read(root/'cli-reviews/dispatch-plan.json')
    need(launch['dispatch_plan']=={'path':str(root/'cli-reviews/dispatch-plan.json'),'sha256':sha(root/'cli-reviews/dispatch-plan.json')},'Pre-dispatch plan pin differs')
    need(0<len(plan['jobs'])==plan['primary_assignments']<=24 and len({(x['wave'],x['profile']) for x in plan['jobs']})==len(plan['jobs']) and plan['automatic_retry'] is False,'CLI primary finite assignment coverage differs')
    need({'wave':wave,'profile':profile} in plan['jobs'],'Assignment missing from pre-dispatch plan')
    need(done['wave']==launch['wave']==wave and done['profile']==launch['profile']==profile,'Assignment identity differs')
    argv=launch['argv'];expected_cwd=root/f'blind-{wave}'
    need(argv==done['argv'] and argv[:6]==['codex','--no-daemon','--ask-for-approval','never','exec','--ephemeral']
         and '--json' in argv and not {'resume','fork'} & set(argv),'Fresh CLI command differs')
    need(argv[argv.index('-C')+1]==str(expected_cwd),'CLI input CWD differs')
    need(launch['fresh_session'] is True and done['fresh_session'] is True and launch['model_override'] is None,'Fresh/model declaration differs')
    need(not {'--model','-m'} & set(argv) and launch['raw_outputs_absent_at_dispatch'] is True,'Unexpected model override/preexisting raw output declaration')
    need(done['exit_code']==0 and done['input_pins_unchanged'] is True,'CLI process/input preservation failed')
    need(launch['input_pins']==done['input_pins']==packet_pins,'CLI sealed input pins differ')
    for key in launch:
        need(done.get(key)==launch[key],'Completion launch field changed: '+key)
    prompt=launch['prompt'];need(Path(prompt['path']).resolve()==base/'prompt.txt' and sha(prompt['path'])==prompt['sha256'],'CLI original prompt pin differs')
    trace=done['trace'];need(Path(trace['path']).resolve()==base/'trace.jsonl' and sha(trace['path'])==trace['sha256'],'CLI trace pin differs')
    events=[json.loads(line) for line in Path(trace['path']).read_text().splitlines() if line.strip()]
    sessions=[x['thread_id'] for x in events if x.get('type')=='thread.started']
    need(len(sessions)==1 and len(set(sessions))==1 and done.get('cli_session_id')==(sessions[0] if len(sessions)==1 else None),'CLI unique session event differs')
    need(any(x.get('type')=='turn.completed' for x in events),'CLI completed turn absent')
    need(not any(x.get('type')=='turn.failed' for x in events),'CLI turn failure retained')
    need(set(done['reports'])==set(raw_paths),'CLI report coverage differs')
    for name,path in raw_paths.items():
        pin=done['reports'].get(name,{})
        need(pin.get('path')==str(Path(path).resolve()) and pin.get('sha256')==sha(path),'CLI completed raw bytes differ: '+name)
    def utc(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
    closed=read(root/'planning/calls-closed.json')
    need(plan['calls_closed']=={'path':str(root/'planning/calls-closed.json'),'sha256':sha(root/'planning/calls-closed.json')},'Production close pin differs')
    need(utc(closed['closed_utc'])<=utc(launch['started_utc'])<=utc(done['completed_utc']),'CLI launched before all20 production close or reversed')
    proc={'cli_completion':{'path':str(completed_path),'sha256':sha(completed_path)},
          'cli_launch':{'path':str(launch_path),'sha256':sha(launch_path)},
          'cli_trace':trace,'cli_session_id':sessions[0] if len(sessions)==1 else None,
          'cli_assignment_valid':not errors,
          'cli_scope':'Exact launch/completion/input/raw/session joins. Semantic viewing and before-copy chronology are still critic attestations unless separately trace-checked.'}
    return proc,errors
