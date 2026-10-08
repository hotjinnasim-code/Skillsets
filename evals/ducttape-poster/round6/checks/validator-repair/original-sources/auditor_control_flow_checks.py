"""In-memory metadata fixtures only; no archive/input file is modified."""
from reviewlib import *
import copy,types
module=types.ModuleType('archived_auditor');module.__file__=str(A/'raw/audit_portable_archive.py')
exec(compile(read('raw/audit_portable_archive.py'),module.__file__,'exec'),module.__dict__)
original=module.ArchiveReader.document
results=[]
def run(name,mutate,should_reject=True):
    def document(self,source,*args,**kwargs):
        d=original(self,source,*args,**kwargs)
        return mutate(str(source),copy.deepcopy(d))
    module.ArchiveReader.document=document
    result,code=module.audit_archive(A)
    results.append({'test':name,'expected_rejection':should_reject,'actual_status':result['status'],'exit_code':code,'expectation_met':(code==1)==should_reject,'archive_byte_integrity':result.get('archive_byte_integrity'),'image_critic_records_first_and_final':result.get('image_critic_records_first_and_final'),'errors':result.get('errors',[]),'evidence_errors':result.get('evidence_errors',[])})
    module.ArchiveReader.document=original
def evidence_edit(edit):
    def mutate(source,d):
        if source.endswith('/planning/final-evidence.json'):edit(d)
        return d
    return mutate
def swap(d):
    roles=list(d['images']);old=d['images'][roles[0]]['binding'];new=copy.deepcopy(d['images'][roles[1]]['binding'])
    new.update(role=old['role'],image_id=old['image_id']);d['images'][roles[0]]['binding']=new
run('different native/manifest binding for sealed role',evidence_edit(swap))
run('changed case declared unchanged',evidence_edit(lambda d:d['sets']['R6-C1'].update(physical_set_changed=False)))
run('raw observation declares another role',evidence_edit(lambda d:d['images']['R6-C1-M1']['reviewers'][0].update(role='R6-C1-M2')))
run('raw observation declares another anonymous image ID',evidence_edit(lambda d:d['images']['R6-C1-M1']['reviewers'][0].update(image_id='X8943')))
run('retained invalid stage drops one observation without changing declared counts',evidence_edit(lambda d:d['images']['R6-C2-M1']['reviewers'].pop()))
run('valid adverse final image relabelled PASS while terminal remains invalid',evidence_edit(lambda d:d['images']['R6-C1-M1'].update(final_image_gate='PASS')))
def wrong_done_session(source,d):
    if source.endswith('/cli-reviews/W1BAF76CA/editorial/completion.json'):d['cli_session_id']='wrong-completion-session'
    return d
run('completion session ID differs from trace and procedure',wrong_done_session)
def missing_unused(self,source,*args,**kwargs):
    if str(source).endswith('/production/R6-C1-M1/repair-1/manifest.json'):
        self.errors.append('Synthetic unmapped unused outcome');return {}
    return original(self,source,*args,**kwargs)
module.ArchiveReader.document=missing_unused
r,code=module.audit_archive(A)
results.append({'test':'unused repair outcome unavailable','expected_rejection':True,'actual_status':r['status'],'exit_code':code,'expectation_met':code==1,'errors':r.get('errors',[]),'evidence_errors':r.get('evidence_errors',[])})
module.ArchiveReader.document=original

# Confinement checks use only files created in the output directory.
fixture=O/'confinement-fixture';fixture.mkdir(exist_ok=True)
(fixture/'inside.json').write_text('{}\n')
link=fixture/'link.json'
if not link.exists() and not link.is_symlink():link.symlink_to(fixture/'inside.json')
for value in ['../outside.json','/absolute.json','C:\\absolute.json','sub\\file.json','link.json']:
    try:
        module.confined_path(fixture.resolve(),value);rejected=False;error=None
    except (ValueError,OSError) as exc:rejected=True;error=str(exc)
    results.append({'test':'confined path '+value,'expected_rejection':True,'expectation_met':rejected,'error':error})

out={'scope':'Control-flow fixtures inject JSON changes after the real confined reader verifies immutable archived bytes. These exercise acceptance logic, not a byte-consistent alternate archive; the source archive was never changed. All real pins and actual joins were independently checked separately. No pixels displayed or decoded.','results':results,'unexpected_acceptances':[r['test'] for r in results if not r['expectation_met']]}
(O/'auditor-control-flow-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
