"""Root-only prospective J case/plan/helpers freeze; no actors or image calls."""
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
 assert case['case_id']=='R10-C1' and case['count']==5 and case['ratios']==['16:9']*5
 planpath=ROOT/'coordinator/R10-C1/plan.json';plan=json.loads(planpath.read_bytes())
 assert plan['case_id']==case['case_id'] and plan['request']==case['request'] and plan['copy']==case['copy']
 assert len(plan['directions'])==5
 for i,d in enumerate(plan['directions'],1):
  assert d['role']==f'R10-C1-M{i}' and d['ratio']=='16:9'
  indexes=[j for g in d['copy_groups'] for j in g['copy_indexes']]
  assert sorted(indexes)==list(range(10)),(i,indexes)
 runtime=[pin(ROOT/'snapshots/candidate-j'/n) for n in FILES]
 for n,row in zip(FILES,runtime):assert pin(Path('/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster')/n)['sha256']==row['sha256']
 helpernames=['prepare_production.py','run_agent.py','run_pool.py','evidence_io.py','prepare_reviews_v2.py','summarize.py','audit_source_assets.py','review_rules.md','critic_rubric.md','reuse_binding.py','capability-probe/result.json']
 methodpaths=sorted(p for p in (ROOT/'method-recording-v2').iterdir() if p.is_file() and p.suffix!='.pyc')
 assert methodpaths and json.loads((ROOT/'method-recording-v2/verification.json').read_bytes())
 references=[ROOT/'research/root-canva-landscape-observations.json',ROOT/'coordinator/R10-C1/own-reference-view-note.md',ROOT/'planning/fresh-j-runtime-review.md',ROOT/'planning/fresh-whole-plan-audit.md',ROOT/'planning/root-whole-plan-preflight.json']
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 fp=ROOT/'planning/candidate-j-pre-generation-freeze.json'
 freeze={'candidate':'J','utc':now,'runtime_files':runtime,'helpers':[pin(ROOT/n) for n in helpernames]+[pin(p) for p in methodpaths],'case':pin(casepath),'central_plan':pin(planpath),'ratio':pin(ROOT/'planning/ratio-policy-before-generation.json'),'references':[pin(p) for p in references],'scope':'Exactly one seen-development request of five different styles, all native16:9; no prior R10 actor/call/review.','budget':{'native_calls_max':15,'fresh_critics_max':6,'max_worker_concurrency':3},'actual_native_calls_at_freeze':0,'recording_method':'Prospective three-field compact v2 supports both phases before generation; rawschema1/v4 gates/normalization unchanged.','causality_limit':'Same literal R9 request seen during J development. New J guidance and new case-specific planning; no isolated causal/unseen/statistical/universal quality claim.'}
 save(fp,freeze)
 save(ROOT/'planning/critic-recording-helper-freeze.json',{'utc':now,'production_and_quality_freeze':pin(fp),'files':[pin(p) for p in methodpaths],'actual_native_calls_at_freeze':0,'actual_critic_sessions_at_freeze':0,'live_critic_jobs_at_freeze':0,'quality_gates_unchanged':True,'overall_critic_cap':6,'phases':['initial','selected'],'scope':'One pre-generation recording method in both phases; no retrospective R9 repair or output export.'})
 print(json.dumps({'status':'FROZEN_BEFORE_ANY_NATIVE','runtime_files':6,'helpers':len(freeze['helpers']),'styles':5,'case':'R10-C1'}))
if __name__=='__main__':main()
