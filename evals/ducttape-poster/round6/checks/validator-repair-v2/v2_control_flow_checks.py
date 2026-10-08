"""Exactly targeted v2 metadata assertions; no archive/source bytes change."""
from pathlib import Path
import copy,json,types
A=Path('/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6').resolve()
O=Path('/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6-final-auditor-fixes-v2')
module=types.ModuleType('patched_v2_auditor');module.__file__=str(O/'audit_portable_archive.py')
exec(compile((O/'audit_portable_archive.py').read_text(),module.__file__,'exec'),module.__dict__)
original=module.ArchiveReader.document
results=[]
def run(name,edit,reject=True,expected_error=None):
 def document(self,source,*args,**kwargs):
  value=original(self,source,*args,**kwargs)
  if str(source).endswith('/planning/final-evidence.json'):
   value=copy.deepcopy(value);edit(value)
  return value
 module.ArchiveReader.document=document
 result,code=module.audit_archive(A)
 module.ArchiveReader.document=original
 errors=result.get('evidence_errors',[])+result.get('errors',[])
 results.append({'test':name,'expected_rejection':reject,'status':result['status'],'exit_code':code,'expectation_met':((code==1)==reject) and (expected_error is None or any(expected_error in x for x in errors)),'errors':result.get('errors',[]),'evidence_errors':result.get('evidence_errors',[])})
run('unmodified archive baseline',lambda d:None,reject=False)
def hide_invalid_stage(d,path):
 cid='R6-C2';ref=d['summary_refs'][cid+'/final'];ref['available']=False;ref['accepted']=False;ref['path']=path
 d['sets'][cid]['final_case_gate']='NOT_ASSESSABLE';d['sets'][cid]['final_reviewers']=[]
 for role in d['sets'][cid]['roles']:
  d['images'][role]['reviewers']=[];d['images'][role]['final_image_gate']='NOT_ASSESSABLE'
 d['final_image_critic_records']=45;d['final_score_observations']=315
 d['final_image_pass_count']=sum(x['final_image_gate']=='PASS' for x in d['images'].values())
 d['final_image_gate_counts']={g:sum(x['final_image_gate']==g for x in d['images'].values()) for g in ['PASS','FAIL','NOT_ASSESSABLE']}
run('available=false and empty ref.path cannot hide existing closure canonical summary',lambda d:hide_invalid_stage(d,''),expected_error='available closure-canonical summary concealed')
run('available=false and repointed ref.path cannot hide existing closure canonical summary',lambda d:hide_invalid_stage(d,'/synthetic/nonexistent-summary.json'),expected_error='available closure-canonical summary concealed')
def falsify_distribution(d,key):
 counts=d[key];counts['FAIL']-=1;counts['NOT_ASSESSABLE']+=1
run('first gate distribution changed with PASS count held fixed',lambda d:falsify_distribution(d,'initial_image_gate_counts'),expected_error='complete PASS/FAIL/NOT_ASSESSABLE distribution differs')
run('final gate distribution changed with PASS count held fixed',lambda d:falsify_distribution(d,'final_image_gate_counts'),expected_error='complete PASS/FAIL/NOT_ASSESSABLE distribution differs')
run('boolean cannot masquerade as integer PASS count',lambda d:d['final_image_gate_counts'].update(PASS=True),expected_error='complete PASS/FAIL/NOT_ASSESSABLE distribution differs')
run('unknown distribution key rejected',lambda d:d['final_image_gate_counts'].update(UNKNOWN=0),expected_error='complete PASS/FAIL/NOT_ASSESSABLE distribution differs')
run('negative distribution value rejected',lambda d:d['final_image_gate_counts'].update(FAIL=-1),expected_error='complete PASS/FAIL/NOT_ASSESSABLE distribution differs')
result={'scope':'Only the two targeted v2 fixes: closure-canonical summary availability/path binding and complete typed nonnegative gate distributions. Post-reader in-memory mutations; original archive unchanged; no visual rescore.','results':results,'unexpected_results':[x['test'] for x in results if not x['expectation_met']]}
(O/'v2-control-flow-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'tests':len(results),'unexpected_results':result['unexpected_results']},ensure_ascii=False))
