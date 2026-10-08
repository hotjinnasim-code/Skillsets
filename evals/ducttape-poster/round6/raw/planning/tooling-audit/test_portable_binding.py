"""Inject one synthetic association error into read-only archive metadata."""
import copy, importlib.util, json, sys
from pathlib import Path
r=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('r6_portable',r/'audit_portable_archive.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original=m.ArchiveReader.document
def injected(self,source,*a,**k):
    d=original(self,source,*a,**k)
    if str(source).endswith('/planning/final-evidence.json') and d:
        d=copy.deepcopy(d);roles=list(d['images'])
        original_binding=d['images'][roles[0]]['binding']
        substituted=copy.deepcopy(d['images'][roles[1]]['binding'])
        # All substituted native/manifest/view file hashes remain valid; only
        # the declared selection-to-binding association is deliberately wrong.
        substituted.update(role=original_binding['role'],image_id=original_binding['image_id'])
        d['images'][roles[0]]['binding']=substituted
    return d
m.ArchiveReader.document=injected
result,code=m.audit_archive(Path(sys.argv[1]))
assert result['status']=='FAIL' and code==1
assert result.get('archive_byte_integrity')=='PASS',result
assert any('selection/binding' in x or 'native/manifest' in x for x in result.get('evidence_errors',[]))
print(json.dumps({'scope':'One deliberately wrong native association injected only in the in-memory metadata returned by the archive reader. No archive byte, image, source report or score changed.', 'passed':True,'rejected_including_evidence_only_mode':True,'archive_mode':result.get('archive_mode'),'evidence_errors':result.get('evidence_errors',[])},ensure_ascii=False,indent=2))
