"""ROOT-only prospective N runtime/case/plan/helper freeze; no actors/native calls."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parent
FILES=('SKILL.md','agents/openai.yaml','references/art-direction.md','references/parallel-production.md','references/visual-research.md','references/evaluation-loop.md')
def pin(p):
 p=Path(p);assert p.is_file() and not p.is_symlink();return {'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def save(p,d):
 with p.open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def main():
 assert not (ROOT/'production').exists() and not (ROOT/'reviews').exists()
 casepath=ROOT/'planning/single-five-case.json';case=json.loads(casepath.read_bytes())['cases'][0]
 assert case['case_id']=='R14-C1' and case['count']==5 and case['ratios']==['16:9']*5 and case['candidate']=='N'
 planpath=ROOT/'coordinator/R14-C1/plan.json';plan=json.loads(planpath.read_bytes())
 assert plan['case_id']==case['case_id'] and plan['request']==case['request'] and plan['copy']==case['copy']
 assert plan['common_constraints']==case['conditions'] and len(plan['directions'])==5
 for i,d in enumerate(plan['directions'],1):
  assert d['role']==f'R14-C1-M{i}' and d['ratio']=='16:9'
  indexes=[j for g in d['copy_groups'] for j in g['copy_indexes']]
  assert sorted(indexes)==list(range(len(case['copy']))),(i,indexes)
 runtime=[pin(ROOT/'snapshots/candidate-n'/n) for n in FILES]
 for n,row in zip(FILES,runtime):assert pin(Path('/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster')/n)['sha256']==row['sha256']
 identity=json.loads((ROOT/'planning/method-source-identity.json').read_bytes())
 helpers=[]
 for row in identity['base_and_method_unchanged']:
  actual=pin(ROOT/row['file']);assert actual['sha256']==row['sha256'] and row['unchanged'];helpers.append(actual)
 assert len(helpers)==19
 helpers.append(pin(ROOT/'capability-probe/result.json'))
 methodpaths=sorted(p for p in (ROOT/'method-recording-v2').iterdir() if p.is_file() and p.suffix!='.pyc')
 references=[ROOT/'coordinator/R14-C1/own-reference-view-note.md',ROOT/'plan-review/plan-review.md',ROOT/'planning/root-whole-plan-preflight.json',ROOT/'planning/plan-advisory-disposition-before-generation.json',ROOT/'planning/prospective-critic-label.json',ROOT/'planning/root-helper-adaptation-before-generation.json',ROOT/'planning/latest-human-style-requirement.json',ROOT/'planning/literal-landscape-request.txt',ROOT/'planning/method-source-identity.json']
 references += sorted(p for p in (ROOT/'research').rglob('*') if p.is_file())
 references += sorted(p for p in (ROOT/'development-context/n-adoption').rglob('*') if p.is_file())
 for d in ('coordinator/R14-C1','plan-review'):
  c=json.loads((ROOT/d/'completion.json').read_bytes());assert c['exit_code']==0 and c['input_pins_unchanged']
  for name in ('job.json','prompt.txt','launch.json','trace.jsonl','completion.json'):references.append(ROOT/d/name)
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();fp=ROOT/'planning/candidate-n-pre-generation-freeze.json'
 freeze={'candidate':'N','utc':now,'runtime_files':runtime,'helpers':helpers,'case':pin(casepath),'central_plan':pin(planpath),'ratio':pin(ROOT/'planning/ratio-policy-before-generation.json'),'references':[pin(p) for p in references],'scope':'Exactly one known architecture event request with prospectively added whole-template exclusion. Five new whole styles16:9; no previous R14 native/critic.','budget':{'native_calls_max':15,'fresh_critics_max':6,'max_worker_concurrency':3},'actual_native_calls_at_freeze':0,'recording_method':'Same three-fieldcompactv2 before both phases; rawschema1/v4 score gates/normalization/ratios unchanged.','causality_limit':'ROOT knows closed R13 and latest human requirement. N guidance, reference choice and planning differ together; known-case development. Fresh makers and quality critics see no previous poster outputs/scores. No isolated causal/statistical/universal proof.'}
 save(fp,freeze)
 save(ROOT/'planning/critic-recording-helper-freeze.json',{'utc':now,'production_and_quality_freeze':pin(fp),'files':[pin(p) for p in methodpaths],'actual_native_calls_at_freeze':0,'actual_critic_sessions_at_freeze':0,'live_critic_jobs_at_freeze':0,'quality_gates_unchanged':True,'overall_critic_cap':6,'phases':['initial','selected'],'scope':'One prospective recording method in both phases; no retrospective score export or reviewer replacement.'})
 print(json.dumps({'status':'FROZEN_BEFORE_ANY_NATIVE','runtime_files':6,'actor_method_helpers':19,'styles':5,'case':'R14-C1'}))
if __name__=='__main__':main()
