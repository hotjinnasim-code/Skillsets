"""Verify exact copied bytes and replay frozen v4 gates in a portable namespace.

Only decoded path identifiers are aliased in memory. No raw file, score, literal
copy, evidence observation, normalization rule or quality threshold is changed.
"""
import argparse,hashlib,importlib.util,json,os,types
from pathlib import Path

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def archive_path(path, root, base=None):
    """Contain lexically before consulting metadata; never resolve host claims."""
    if not isinstance(path, (str, Path)) or not str(path):
        raise ValueError('missing explicit path')
    candidate = Path(path)
    if not candidate.is_absolute() and base is not None:
        candidate = Path(base)/candidate
    candidate = Path(os.path.normpath(str(candidate)))
    if not candidate.is_absolute() or not candidate.is_relative_to(root):
        raise ValueError('Original-host metadata/read forbidden: '+str(path))
    # Inspect prefixes from the archive root outward so a parent symlink is
    # rejected before any metadata operation on its child could follow it.
    prefix = root
    for part in candidate.relative_to(root).parts:
        prefix = prefix/part
        if prefix.is_symlink():
            raise ValueError('Archive symlink path forbidden: '+str(prefix))
    return candidate.resolve(strict=True)

def verify(root):
    root=root.resolve(strict=True); index=json.loads((root/'archive-index.json').read_bytes());mapping={}
    for row in index['files']:
        rel=Path(row['archive_relative']);assert not rel.is_absolute() and '..' not in rel.parts
        actual=root/rel
        assert actual.resolve().is_relative_to(root) and not any(p.is_symlink() for p in [actual,*actual.parents] if p.is_relative_to(root)), 'Archive symlink escape'
        assert actual.is_file() and digest(actual)==row['sha256'],str(actual)
        old=row['source_absolute'];assert old not in mapping;mapping[old]=actual
    assert len(mapping)==index['mapped_sources']
    source_root=index['source_root']
    physical=lambda p:mapping[str(p)]
    final=json.loads(physical(source_root+'/planning/final-evidence.json').read_bytes())
    assert final==index['closed_evidence'] and final['poster_calls_closed'] is True
    assert len(final['makers'])==20 and final['poster_native_attempts']==len(final['caller_records'])<=60
    engine=module(physical(source_root+'/summarize.py'),'r7_archived_frozen_v4')
    corpus=json.loads(physical(final['corpus']['path']).read_bytes())
    case_map={c['case_id']:c for c in corpus['cases']};role_ids={r['role_id'] for c in corpus['cases'] for r in c['roles']}
    assert len(case_map)==7 and len(role_ids)==20 and set(final['stages'])=={'initial','selected'}
    assert all(set(st['cases'])==set(case_map) for st in final['stages'].values())
    original_read=engine.read_json
    original_digest=engine.digest
    engine.resolve=lambda path,base:archive_path(path,root,base)
    engine.digest=lambda path:original_digest(archive_path(path,root))
    def alias(value,key=None,observational=False):
        if isinstance(value,dict):return {k:alias(v,k,observational) for k,v in value.items()}
        if isinstance(value,list):return [alias(v,key,observational) for v in value]
        if isinstance(value,str) and key in ('path','actual_path','manifest_path'):
            if value not in mapping:
                if observational:return value
                raise ValueError('Unarchived authoritative source path: '+value)
            return str(mapping[value])
        return value
    def read_json(path):
        path=archive_path(path,root)
        raw,byte_pin=original_read(path);return alias(raw,observational=path.name in ('editorial.json','craft.json','portfolio.json')),byte_pin
    engine.read_json=read_json
    source_checker=module(physical(source_root+'/audit_source_assets.py'),'r7_archived_source_checker')
    reuse_checker=module(physical(source_root+'/reuse_binding.py'),'r7_archived_reuse_checker')
    replays=[];unique_summaries=set();critic_sessions=[];actual_counts={'records':0,'score_slots':0,'valid_scores':0}
    for wave,stage in final['stages'].items():
        assert set(stage['image_gates'])==role_ids
        readiness=json.loads(physical(source_root+'/reviews/'+wave+'-stage-readiness.json').read_bytes())
        assert readiness['wave']==wave and set(readiness['cases'])==set(case_map)
        assert readiness['planned_role_count']==readiness['closed_role_count']==20 and readiness['all_makers_closed'] is True
        for cid,item in stage['cases'].items():
            state=readiness['cases'][cid];case=case_map[cid]
            assert json.loads(physical(source_root+'/reviews/'+cid+'/'+wave+'/readiness.json').read_bytes())==state
            assert state['expected_count']==case['count'] and state['roles']==[r['role_id'] for r in case['roles']]
            if 'summary' not in item:
                assert state['status']=='UNREADY' and state['errors'] and item['reason']==state['errors'] and item['gate']=='NA'
                assert all(stage['image_gates'][r['role_id']]=='NA' for r in case['roles'])
                continue
            assert state['status']=='READY' and not state['errors']
            original=item['summary']['path']
            stored=json.loads(physical(original).read_bytes());stored_source=json.loads(physical(item['source_attestation_audit']['path']).read_bytes())
            assert stored['case_id']==stored_source['case_id']==cid and stored['wave']==stored_source['wave']==('initial' if item.get('reused_complete_initial_three') else wave)
            assert item['original_v4_set_gate']==stored['set_gate'] and item['original_v4_image_gates']==stored['image_gates']
            assert item['source_attestation_gate']==stored_source['gate']
            assert item['gate']==(stored['set_gate'] if stored_source['gate']=='PASS' else 'NA')
            expected_images=stored['image_gates'] if stored_source['gate']=='PASS' else {k:'NA' for k in stored['image_gates']}
            assert all(stage['image_gates'][k]==v for k,v in expected_images.items())
            if item.get('reused_complete_initial_three'):
                pp=source_root+'/reviews/'+cid+'/initial/packet.json'; selected=source_root+'/reviews/'+cid+'/selected/packet.json'
                raw_read=lambda p:json.loads(physical(p).read_bytes())
                def original_pin(p):
                    actual=physical(p);return {'path':p,'sha256':digest(actual),'bytes':actual.stat().st_size}
                def exact_pin(row):
                    actual=original_pin(row['path']);assert actual['sha256']==row['sha256'];return actual
                reuse_checker.check_reuse(raw_read(pp),raw_read(selected),raw_read(original),raw_read(item['reuse']['path']),original_pin(pp),original_pin(original),exact_pin)
            if original in unique_summaries:continue
            unique_summaries.add(original); sp=physical(original); stored=json.loads(sp.read_bytes()); packet=physical(stored['packet']['path']); cli=packet.parent/'cli'
            args=types.SimpleNamespace(packet=str(packet),report=[p+'='+str(cli/p/(p+'.json')) for p in ('editorial','craft','portfolio')],completions_dir=str(cli))
            result=engine.summary(args)
            critic_sessions += [result['reviews'][p]['provenance']['derived_session_id'] for p in ('editorial','craft','portfolio')]
            cc=result['counts'];actual_counts['records']+=cc['observed_image_profile_records'];actual_counts['score_slots']+=cc['observed_score_slots'];actual_counts['valid_scores']+=cc['valid_integer_1_to_5_score_values']
            for key in ('procedure_gate','image_gates','image_gate_counts','set_gate','counts'):
                assert result[key]==stored[key],cid+'/'+wave+'/'+key
            for p in ('editorial','craft','portfolio'):
                for image_id,record in result['reviews'][p]['images'].items():
                    saved=stored['reviews'][p]['images'][image_id]
                    assert ('scores' in record)==('scores' in saved) and record.get('scores')==saved.get('scores')
            source=source_checker.audit(packet,cli)
            stored_source=json.loads(physical(item['source_attestation_audit']['path']).read_bytes())
            assert source['gate']==stored_source['gate']
            for p in ('editorial','craft','portfolio'):assert source['profiles'][p]['gate']==stored_source['profiles'][p]['gate']
            replays.append({'case_id':cid,'actual_summary_wave':stored['wave'],'procedure_gate':result['procedure_gate'],'image_gate_counts':result['image_gate_counts'],'set_gate':result['set_gate'],'source_attestation_gate':source['gate']})
        assert stage['image_gate_counts']=={s:sum(g==s for g in stage['image_gates'].values()) for s in ('PASS','FAIL','NA')}
        gates=[v['gate'] for v in stage['cases'].values()]
        assert stage['whole_corpus_gate']==('NA' if 'NA' in gates else 'FAIL' if 'FAIL' in gates else 'PASS')
    assert len(critic_sessions)==len(set(critic_sessions))==final['actual_unique_review_sessions'] and actual_counts==final['actual_review_counts']
    return {'status':'PASS','mapped_source_byte_checks':len(mapping),'unique_summaries_replayed':len(replays),'replays':replays,'limits':['No original host path is required for aliased metadata reads. Raw byte digests and all scores/copy remain unchanged.','Unready phases are retained rather than invented or replayed. Semantic viewing remains an attestation.']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=verify(a.archive)
    if a.output:
        with a.output.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2)
    print(json.dumps(r))
