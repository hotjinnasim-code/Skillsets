"""Closed I archive checks; all controlled fixtures are synthetic metadata only."""
import builtins, contextlib, copy, hashlib, html.parser, importlib.util, json, os, shutil, sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
INDEX = json.loads((ROOT/'archive-index.json').read_bytes())
OLD = INDEX['source_root']
MAPPING = {r['source_absolute']:ROOT/r['archive_relative'] for r in INDEX['files']}
FIXTURES = ROOT/'synthetic-metadata-fixtures'

def load(name, file):
    spec=importlib.util.spec_from_file_location(name,file)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

verify=load('i_archive_checks_verifier',ROOT/'raw/verify_archive.py')
archive=load('i_archive_checks_archiver',ROOT/'raw/archive_single_five.py')
source_checker=load('i_archive_checks_source_audit',ROOT/'raw/audit_source_assets.py')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        assert json.loads(path.read_bytes())==value, 'Existing synthetic/check result differs: '+str(path)
        return
    with path.open('x') as handle:json.dump(value,handle,ensure_ascii=False,indent=2)

blocked=[]
def guard_path(value):
    if isinstance(value,(str,bytes,os.PathLike)):
        path=os.path.normpath(os.fsdecode(value))
        for prefix in (OLD, '/Users/nahyeonbin/.codex/generated_images'):
            if path==prefix or path.startswith(prefix+'/'):
                blocked.append(path)
                raise RuntimeError('Original-host access attempted: '+path)

@contextlib.contextmanager
def no_original_host():
    def guarded(original):
        def call(path,*args,**kwargs):guard_path(path);return original(path,*args,**kwargs)
        return call
    with contextlib.ExitStack() as stack:
        for owner,name in ((Path,'resolve'),(Path,'stat'),(Path,'lstat'),(Path,'open'),
                           (Path,'read_bytes'),(Path,'read_text'),(builtins,'open'),
                           (os,'stat'),(os,'lstat'),(os,'open')):
            stack.enter_context(patch.object(owner,name,guarded(getattr(owner,name))))
        yield

class Links(html.parser.HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.images=[]
    def handle_starttag(self,tag,attributes):
        attributes=dict(attributes)
        for key in ('href','src'):
            if key in attributes:self.links.append(attributes[key])
        if tag=='img':self.images.append(attributes['src'])

def preserve(source,retained):
    before={p.relative_to(source).as_posix():sha(p) for p in source.rglob('*') if p.is_file()}
    shutil.copytree(source,retained)
    after={p.relative_to(retained).as_posix():sha(p) for p in retained.rglob('*') if p.is_file()}
    assert before==after
    return before

def source_fixture(name,wrong_path=False,wrong_hash=False):
    source=FIXTURES/name/'source';source.mkdir(parents=True)
    asset=source/'synthetic-asset-observation.txt';asset.write_text('SYNTHETIC metadata identity only; no image or visual evaluation.\n')
    packet={'synthetic_metadata_fixture':True,'case_id':'SYNTHETIC-'+name,'wave':'synthetic',
            'source_assets':[{'asset_id':'synthetic-asset','actual_path':str(asset),'sha256':sha(asset)}],
            'protected_layouts':[]}
    write(source/'packet.json',packet)
    for profile in ('editorial','craft','portfolio'):
        seen={'asset_id':'synthetic-asset','path':str(asset),'sha256':sha(asset),'viewed':True}
        if profile=='editorial':
            if wrong_path:seen['path']=OLD+'/production'
            if wrong_hash:seen['sha256']='0'*64
        write(source/'cli'/profile/(profile+'.json'),{'synthetic_metadata_fixture':True,
              'procedure':{'source_assets_viewed':[seen],'protected_layouts_read':[]}})
    with no_original_host():result=source_checker.audit(source/'packet.json',source/'cli')
    assert result['gate']=='NA' and result['profiles']['editorial']['gate']=='NA'
    write(source/'source-asset-audit.json',result)
    raw_before=(source/'source-asset-audit.json').read_bytes()
    pins=list(archive.pinned_objects(archive.authoritative_data('source-asset-audit.json',result)))
    with no_original_host():
        for pin in pins:assert sha(pin['path'])==pin['sha256']
    assert (source/'source-asset-audit.json').read_bytes()==raw_before
    retained=FIXTURES/name/'retained';digests=preserve(source,retained)
    with no_original_host():again=source_checker.audit(retained/'packet.json',retained/'cli')
    assert again['gate']=='NA'
    return {'synthetic':True,'gate':'NA','preserved_files':len(digests),'authoritative_pins':len(pins),'file_sha256':digests}

def unknown_view_fixture():
    source=FIXTURES/'unknown-raw-view-host-path'/'source';source.mkdir(parents=True)
    phase=ROOT/'raw/reviews/R8-C1/initial'
    for profile in ('editorial','craft','portfolio'):
        folder=source/'cli'/profile;folder.mkdir(parents=True)
        for name in ('launch.json','completion.json',profile+'.json'):
            shutil.copyfile(phase/'cli'/profile/name,folder/name)
    report=source/'cli/editorial/editorial.json'
    original=json.loads(report.read_bytes());changed=copy.deepcopy(original)
    changed['synthetic_metadata_fixture']=True
    changed['viewed'][0]['path']=OLD+'/production'
    report.write_text(json.dumps(changed,ensure_ascii=False,indent=2))
    assert changed['images']==original['images']
    completion=source/'cli/editorial/completion.json'
    value=json.loads(completion.read_bytes());value['reports']['editorial.json']['sha256']=sha(report)
    completion.write_text(json.dumps(value,ensure_ascii=False,indent=2))
    write(source/'SYNTHETIC-ONLY.json',{'synthetic':True,'scope':'Controlled metadata mutation only; copied provenance is not a new critic session. Scores/images are unchanged.','unknown_host_identifier':OLD+'/production'})
    retained=FIXTURES/'unknown-raw-view-host-path'/'retained';digests=preserve(source,retained)
    mapping=dict(MAPPING)
    for profile in ('editorial','craft','portfolio'):
        for name in ('launch.json','completion.json',profile+'.json'):
            mapping[OLD+'/reviews/R8-C1/initial/cli/'+profile+'/'+name]=retained/'cli'/profile/name
    engine=load('i_archive_synthetic_unknown_view_engine',ROOT/'raw/summarize.py')
    original_read,original_digest=engine.read_json,engine.digest
    engine.resolve=lambda path,base:verify.archive_path(path,ROOT,base)
    engine.digest=lambda path:original_digest(verify.archive_path(path,ROOT))
    def alias(value,key=None,observational=False):
        if isinstance(value,dict):return {k:alias(v,k,observational) for k,v in value.items()}
        if isinstance(value,list):return [alias(v,key,observational) for v in value]
        if isinstance(value,str) and key in ('path','actual_path','manifest_path'):
            if value in mapping:return str(mapping[value])
            if observational:return value
            raise ValueError('Unarchived authoritative path: '+value)
        return value
    def read(path):
        path=verify.archive_path(path,ROOT);raw,pin=original_read(path)
        return alias(raw,observational=path.name in ('editorial.json','craft.json','portfolio.json')),pin
    engine.read_json=read
    import types
    args=types.SimpleNamespace(packet=str(phase/'packet.json'),completions_dir=str(retained/'cli'),
           report=[p+'='+str(retained/'cli'/p/(p+'.json')) for p in ('editorial','craft','portfolio')])
    with no_original_host():result=engine.summary(args)
    assert result['procedure_gate']=='NA' and result['set_gate']=='NA' and result['image_gate_counts']=={'PASS':0,'FAIL':0,'NA':5}
    errors=result['reviews']['editorial']['procedure_errors']
    assert len(errors)==1 and 'viewed sequence' in errors[0],errors
    assert result['counts']['valid_integer_1_to_5_score_values']==105
    write(FIXTURES/'unknown-raw-view-host-path'/'synthetic-result.json',{'synthetic':True,'gate':'NA','procedure_errors':errors,'image_gate_counts':result['image_gate_counts'],'scores_unchanged':True})
    return {'synthetic':True,'gate':'NA','sole_procedure_error':'viewed sequence mismatch','scores_unchanged':True,'preserved_files':len(digests),'file_sha256':digests}

if __name__=='__main__':
    FIXTURES.mkdir(exist_ok=True)
    write(FIXTURES/'SYNTHETIC-ONLY.json',{'synthetic':True,'scope':'Metadata-only controlled fixtures outside real raw evidence. No new image or critic sessions; no quality claim.'})
    with no_original_host():replay=verify.verify(ROOT)
    write(ROOT/'portable-replay-host-blocked.json',replay)
    parser=Links();parser.feed((ROOT/'raw/gallery.html').read_text())
    targets=[]
    with no_original_host():
        for link in parser.links:
            target=verify.archive_path(link,ROOT,ROOT/'raw');assert target.is_file();targets.append(target)
    assert len(parser.images)==5 and len(targets)==21
    for case in json.loads((ROOT/'raw/planning/single-five-case.json').read_bytes())['cases']:
        for role in case['roles']:
            selected=json.loads((ROOT/'raw/production'/role['role_id']/'selection.json').read_bytes())
            assert MAPPING[selected['selected_files']['original']['path']] in targets
            assert MAPPING[selected['selected_files']['usage720']['path']] in targets
    fixtures={'wrong_observed_source_path':source_fixture('wrong-observed-source-path',wrong_path=True),
              'wrong_observed_source_hash':source_fixture('wrong-observed-source-hash',wrong_hash=True),
              'unknown_raw_view_host_path':unknown_view_fixture()}
    assert not blocked
    external=[r for r in INDEX['files'] if not Path(r['source_absolute']).is_relative_to(OLD)]
    report={'status':'PASS','scope':'Exact-byte archive/replay and gallery integration; synthetic metadata fixture checks are separate from real quality results.',
            'mapped_sources':len(MAPPING),'unique_hashes':INDEX['unique_exact_byte_hashes'],
            'physical_indexed_files':len({r['archive_relative'] for r in INDEX['files']}),
            'external_sources':len(external),'external_native_cache_aliases_to_raw_originals':sum(r['archive_relative'].startswith('raw/production/') and r['archive_relative'].endswith('/original.png') for r in external),
            'native_originals':len(list((ROOT/'raw/production').glob('*/stages/*/original.png'))),
            'stage_png_files':len(list((ROOT/'raw/production').glob('*/stages/*/*.png'))),
            'gallery_image_count':len(parser.images),'gallery_link_references':len(targets),'gallery_unique_targets':len(set(targets)),
            'original_host_metadata_or_read_attempts':len(blocked),'real_replay':replay,'synthetic_metadata_fixtures':fixtures,
            'limits':['Semantic viewing remains an attestation.','Synthetic fixtures create no new critic or poster outcome.','The development request does not certify unseen requests; no client-asset preservation or one-image editing was exercised.']}
    write(ROOT/'archive-integration-checks.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('synthetic_metadata_fixtures','real_replay')},ensure_ascii=False))
