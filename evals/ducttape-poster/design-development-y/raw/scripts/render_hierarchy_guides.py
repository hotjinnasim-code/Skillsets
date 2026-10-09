"""Create own coded planning diagrams only; no native/final image editing."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
TASK=Path(__file__).resolve().parents[1]
PLAN=TASK/'drafts/x-five-design/plan-hierarchy-v2.json'
HELPER=TASK/'Skillsets/skills/ducttape-poster/scripts/make_layout_guide.py'
OUT=TASK/'work/round21/coordinator/guides'
def pin(p):return {'path':str(p.resolve(strict=True)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
plan=json.loads(PLAN.read_bytes());rows=[];guide_map={}
assert len(plan['directions'])==5
for d in plan['directions']:
 role=d['role'];folder=OUT/role;spec=folder/'layout.spec.json'
 write(spec,d['guide_spec'])
 command=[sys.executable,'-B',str(HELPER),str(spec),'--output-dir',str(folder),'--name','layout']
 result=subprocess.run(command,cwd=TASK,capture_output=True,text=True)
 record={'role':role,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'plan':pin(PLAN),'helper':pin(HELPER),'spec':pin(spec),'native_calls':0,'not_a_requested_poster':True}
 if result.returncode==0:
  files={'png':folder/'layout.png','svg':folder/'layout.svg','spec':spec,'manifest':folder/'layout.manifest.json'}
  record['outputs']={k:pin(v) for k,v in files.items()}
  guide_map[role]={k:str(v.resolve(strict=True)) for k,v in files.items()}
 write(folder/'render-status.json',record);rows.append({'role':role,'exit_code':result.returncode,'error':result.stderr.strip()})
if len(guide_map)==5:write(OUT/'selected-guides.json',guide_map)
print(json.dumps({'renders':rows,'successful':len(guide_map),'native_calls':0},ensure_ascii=False))
