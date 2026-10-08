"""Read-only negative procedure test; no new critic or changed raw observation."""
import contextlib, importlib.util, io, json, sys
from pathlib import Path
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r))
spec=importlib.util.spec_from_file_location('r6_summary',r/'summarize.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
original=s.check_cli_assignment
def injected(*a,**k):
    proc,errors=original(*a,**k)
    if a[2]=='portfolio':
        errors.append('SYNTHETIC TEST ONLY: one assignment invalidated')
        proc['cli_assignment_valid']=False
    return proc,errors
s.check_cli_assignment=injected
sys.argv=['summarize.py','--wave','W1BAF76CA']
out=io.StringIO()
with contextlib.redirect_stdout(out):code=s.main()
d=json.loads(out.getvalue())
assert d['recorded_evidence_integrity']=='FAIL' and d['predeclared_core_diversity_gate']=='NOT_ASSESSABLE'
assert d['located_gate_failures'] and d['all_scores_below4']
print(json.dumps({'scope':'Synthetic procedure invalidity injected in read-only evaluation of preserved first-wave metadata. No new score, critic, raw-file write or image alteration.', 'passed':True,'exit_code':code,'recorded_evidence_integrity':d['recorded_evidence_integrity'],'predeclared_core_diversity_gate':d['predeclared_core_diversity_gate'],'available_record_count':d['image_critic_record_count'],'retained_failure_count':len(d['located_gate_failures'])},indent=2))
