"""ROOT-only seven-file P freeze. No extra plan-review actor."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parent
FILES=('SKILL.md','agents/openai.yaml','references/art-direction.md','references/parallel-production.md','references/visual-research.md','references/evaluation-loop.md','references/production-brief.md')
def pin(p):
 p=Path(p);assert p.is_file() and not p.is_symlink();return {'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def save(p,v):
 with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def main():
 assert not (ROOT/'production').exists() and not (ROOT/'reviews').exists()
 casepath=ROOT/'planning/production-single-five-case.json';case=json.loads(casepath.read_bytes())['cases'][0]
 assert case['candidate']=='P' and case['count']==5
 planpath=ROOT/'coordinator/R15-C1/plan.json';plan=json.loads(planpath.read_bytes())
 assert plan['request']==case['request'] and plan['copy']==case['copy'] and plan['common_constraints']==case['conditions']
 runtime=[pin(ROOT/'snapshots/candidate-p'/n) for n in FILES]
 for n,row in zip(FILES,runtime):assert pin(Path('/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster')/n)['sha256']==row['sha256']
 helpers=[]
 for row in json.loads((ROOT/'planning/method-source-identity.json').read_bytes())['base_and_method_unchanged']:
  p=pin(ROOT/row['file']);assert p['sha256']==row['sha256'] and row['unchanged'];helpers.append(p)
 assert len(helpers)==19
 helpers.append(pin(ROOT/'capability-probe/result.json'))
 refs=[p for folder in ('research','development-context','coordinator/R15-C1','checks/root-p-handoff-history') for p in (ROOT/folder).rglob('*') if p.is_file()]
 refs += [ROOT/'planning'/n for n in ('root-whole-plan-preflight.json','generation-first-human-steering.json','prospective-critic-label.json','latest-human-style-requirement.json','literal-landscape-request.txt','method-source-identity.json')]
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();f=ROOT/'planning/candidate-p-pre-generation-freeze.json'
 save(f,{'candidate':'P','utc':now,'runtime_files':runtime,'helpers':helpers,'case':pin(casepath),'central_plan':pin(planpath),'ratio':pin(ROOT/'planning/ratio-policy-before-generation.json'),'references':[pin(p) for p in refs],'budget':{'native_calls_max':15,'fresh_critics_max':6,'max_worker_concurrency':3},'actual_native_calls_at_freeze':0,'scope':'One new-content request, five distinct whole styles16:9; first generation priority. Coordinator O before human steering; fresh makers P. No extra plan-review actor.','causality_limit':'ROOT knows closed historical results; guidance, source handoff and new planning differ together. No isolated causal or universal quality guarantee.'})
 save(ROOT/'planning/critic-recording-helper-freeze.json',{'utc':now,'production_and_quality_freeze':pin(f),'files':[pin(p) for p in sorted((ROOT/'method-recording-v2').iterdir()) if p.is_file()],'actual_native_calls_at_freeze':0,'actual_critic_sessions_at_freeze':0,'live_critic_jobs_at_freeze':0,'quality_gates_unchanged':True,'overall_critic_cap':6,'phases':['initial','selected']})
 print(json.dumps({'status':'FROZEN_BEFORE_ANY_NATIVE','runtime_files':7,'actor_method_helpers':19,'styles':5}))
if __name__=='__main__':main()
