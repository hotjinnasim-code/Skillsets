"""Additional metadata control-flow tests; no original archive bytes change."""
from pathlib import Path
import copy,json,types
A=Path('/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6').resolve()
O=Path('/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6-final-auditor-fixes')
module=types.ModuleType('patched_auditor');module.__file__=str(O/'audit_portable_archive.py')
exec(compile((O/'audit_portable_archive.py').read_text(),module.__file__,'exec'),module.__dict__)
original=module.ArchiveReader.document
original_pin=module.ArchiveReader.pin
results=[]
def run(name,mutate=None,pin_hook=None,reject=True):
 def document(self,source,*args,**kwargs):
  value=original(self,source,*args,**kwargs)
  return mutate(str(source),copy.deepcopy(value)) if mutate else value
 def pin(self,value,reason='pinned file'):
  path=original_pin(self,value,reason)
  return pin_hook(path,reason) if pin_hook else path
 module.ArchiveReader.document=document;module.ArchiveReader.pin=pin
 result,code=module.audit_archive(A)
 results.append({'test':name,'expected_rejection':reject,'status':result['status'],'exit_code':code,'expectation_met':(code==1)==reject,'evidence_errors':result.get('evidence_errors',[]),'errors':result.get('errors',[])})
 module.ArchiveReader.document=original;module.ArchiveReader.pin=original_pin
 return result
def evidence_edit(edit):
 def mutate(source,value):
  if source.endswith('/planning/final-evidence.json'):edit(value)
  return value
 return mutate
run('unmodified baseline evidence-only archive is accepted',reject=False)
run('copied observation case identity cannot change',evidence_edit(lambda d:d['images']['R6-C1-M1']['reviewers'][0].update(case_id='R6-C2')))
run('copied observation profile identity cannot change',evidence_edit(lambda d:d['images']['R6-C1-M1']['reviewers'][0].update(profile='craft')))
run('declared first-stage all-seven score count cannot change',evidence_edit(lambda d:d.update(firstpass_score_observations=419)))
run('declared final-stage record count cannot change',evidence_edit(lambda d:d.update(final_image_critic_records=59)))
run('declared first image gate cannot flip',evidence_edit(lambda d:d['images']['R6-C1-M1'].update(initial_image_gate='FAIL' if d['images']['R6-C1-M1']['initial_image_gate']=='PASS' else 'PASS')))
run('declared final case gate cannot flip',evidence_edit(lambda d:d['sets']['R6-C1'].update(final_case_gate='FAIL' if d['sets']['R6-C1']['final_case_gate']=='PASS' else 'PASS')))
def accept_false(d):
 d['summary_refs']['R6-C1/final']['accepted']=False
 d['sets']['R6-C1']['final_case_gate']='NOT_ASSESSABLE'
 for role in d['sets']['R6-C1']['roles']:d['images'][role]['final_image_gate']='NOT_ASSESSABLE'
 d['final_image_pass_count']=sum(x['final_image_gate']=='PASS' for x in d['images'].values())
run('accepted=false cannot conceal an available valid source stage',evidence_edit(accept_false))
def unavailable_false(d):
 accept_false(d);d['summary_refs']['R6-C1/final']['available']=False
 d['sets']['R6-C1']['final_reviewers']=[]
 for role in d['sets']['R6-C1']['roles']:d['images'][role]['reviewers']=[]
 d['final_image_critic_records']=45;d['final_score_observations']=315
run('available=false cannot conceal archived source stage',evidence_edit(unavailable_false))
class WithoutCompleted:
 def __init__(self,path):self.path=path
 def read_text(self):return '\n'.join(line for line in self.path.read_text().splitlines() if json.loads(line).get('type')!='turn.completed')
def omit_completed(path,reason):return WithoutCompleted(path) if path is not None and reason=='CLI acceptance trace' else path
run('successful assignment requires turn.completed trace event',pin_hook=omit_completed)
def wrong_profile_schema(source,value):
 if '/planning/summary-' in source:value['critics']=['editorial','editorial','portfolio']
 return value
run('source summary exact profile identities required',wrong_profile_schema)
result={'scope':'Post-reader in-memory metadata/trace control-flow injection. Original archive bytes and report observations stay unchanged; no pixels displayed or decoded. Baseline success is tested separately.','results':results,'unexpected_results':[x['test'] for x in results if not x['expectation_met']]}
(O/'additional-control-flow-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'tests':len(results),'unexpected_results':result['unexpected_results']},ensure_ascii=False))
