"""Build isolated zero-generation coordinator jobs for each fixed case."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
corpus=json.loads((root/'planning/corpus20.json').read_text())
skill=root/'snapshots/candidate-h'
skillfiles=[skill/'SKILL.md',skill/'agents/openai.yaml',*[skill/'references'/n for n in ['art-direction.md','evaluation-loop.md','parallel-production.md','visual-research.md']]]
queue=[]
for case in corpus['cases']:
 if case['case_id']=='R7-D1':continue
 out=root/'coordinator'/case['case_id'];out.mkdir(parents=True,exist_ok=True)
 sanitized={k:case[k] for k in ['case_id','request','copy','count','ratios','styles','conditions','roles']}
 casefile=out/'case.json';casefile.write_text(json.dumps(sanitized,ensure_ascii=False,indent=2))
 inputs=[str(casefile),*[str(x) for x in skillfiles]]
 for role in case['roles']:
  for asset in role['assets']:
   for key in ['actual_path','manifest_path']:
    if asset[key] not in inputs:inputs.append(asset[key])
 prompt=f'''You are a fresh central coordinator simulating actual use of the ducttape-poster skill. Apply the skill at {skill/'SKILL.md'}, read its applicable references. Full client request and exact copy/count/ratios/style/assets are in {casefile}. Treat supplied assets as actual synthetic test-fixture client inputs; inspect their exact files with the native view_image tool before preservation/layout decisions. Read asset manifests where relevant. Do not read parent directories, previous rounds, scores, other case plans or credentials/config. Do not generate or edit any image, spawn, resume, send messages or invoke another CLI. Your task is only to plan this case's requested count of separate directions consistent with the actual skill, not to help an evaluator pass. Preserve every literal condition and copy entry; no invented client facts. For N=1 reference-preservation, layout/asset fidelity takes priority over novelty or diversity.
Write only {out/'plan.json'} and optional verification.json. plan.json schema: case_id,request,copy,common_constraints:[strings],directions:[{{role:exact role_id,ratio:exact role ratio,fullcopy:all copy strings joined by newline,concept,substantive_non_glyph_visual,expression_system,copy_visual_relationship,closest_other_role:null for N1 otherwise validotherrole,distinction}}]. Each direction: actual content relation -> scene/form/action -> firstlook/type role -> information space relation; substantial nonglyph concept, faithfully requested genre/asset/viewpoint. No shared generic title-object-footer template or fixed palettes; count/ranges exactly client. Review directions together for real differences and feasible legibility; don't print internal style labels. Save actual verification scope honestly, zero calls. Final concise planned-rolecount. All input paths are exact pinned files; only write own directory.'''
 promptfile=out/'prompt.txt';promptfile.write_text(prompt)
 job={'output_dir':str(out),'prompt_file':str(promptfile),'case_id':case['case_id'],'wave':'planning','profile':'coordinator','inputs':inputs,'expected_outputs':['plan.json']}
 jobfile=out/'job.json';jobfile.write_text(json.dumps(job,ensure_ascii=False,indent=2));queue.append(str(jobfile))
queuefile=root/'planning/coordinator-queue.json'
with queuefile.open('x') as f:json.dump(queue,f,indent=2)
print(json.dumps({'prepared':len(queue),'generation_calls':0}))
