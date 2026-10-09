"""Verify exact copied bytes and replay frozen v4 gates in a portable namespace.

Only decoded path identifiers are aliased in memory. No raw file, score, literal
copy, evidence observation, normalization rule or quality threshold is changed.
"""
import argparse,hashlib,importlib.util,json,os,types
from pathlib import Path

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def archive_root(root):
    """Reject a root symlink prefix before resolving or opening its index."""
    if not isinstance(root, (str, Path)) or not str(root):
        raise ValueError('missing explicit archive root')
    candidate = Path(os.path.abspath(root))
    if '..' in Path(root).parts:
        raise ValueError('Archive root traversal forbidden: '+str(root))
    prefix = Path(candidate.anchor)
    for part in candidate.parts[1:]:
        prefix = prefix/part
        if prefix.is_symlink():
            raise ValueError('Archive root symlink path forbidden: '+str(prefix))
    if not candidate.is_dir():
        raise ValueError('Archive root must be a real directory: '+str(candidate))
    return candidate


def archive_path(path, root, base=None):
    """Contain lexically before consulting metadata; never resolve host claims."""
    if not isinstance(path, (str, Path)) or not str(path):
        raise ValueError('missing explicit path')
    candidate = Path(path)
    if '..' in candidate.parts:
        raise ValueError('Archive path traversal forbidden: '+str(path))
    if not candidate.is_absolute() and base is not None:
        candidate = Path(base)/candidate
    if '..' in candidate.parts:
        raise ValueError('Archive path traversal forbidden: '+str(path))
    candidate = Path(os.path.normpath(str(candidate)))
    if not candidate.is_absolute() or not candidate.is_relative_to(root):
        raise ValueError('Original-host metadata/read forbidden: '+str(path))
    # Walk from the filesystem anchor, including root and index prefixes, so a
    # symlink is rejected before any child metadata operation can follow it.
    prefix = Path(candidate.anchor)
    for part in candidate.parts[1:]:
        prefix = prefix/part
        if prefix.is_symlink():
            raise ValueError('Archive symlink path forbidden: '+str(prefix))
    return candidate.resolve(strict=True)

def review_state(readiness, local, case, wave, makers):
    roles = [r['role_id'] for r in case['roles']]
    assert readiness['wave'] == wave and set(readiness['cases']) == {case['case_id']}
    assert readiness['planned_roles'] == roles and readiness['planned_role_count'] == readiness['closed_role_count'] == 5
    assert readiness['planned_case_count'] == 1 and readiness['all_makers_closed'] is True
    inventory = readiness['maker_inventory']
    assert set(inventory) == set(roles)
    for maker in makers:
        row = inventory[maker['role']]
        assert row['closed'] is True and not row['errors']
        assert row['terminal'] == maker['terminal'] and row['counts'] == maker['counts']
        assert row.get('selected_stage') == maker['selected_stage']
    state = readiness['cases'][case['case_id']]
    assert local == state, 'Global/per-case readiness state differs'
    assert state['expected_count'] == 5 and state['roles'] == roles
    assert [i['image_id'] for i in state['images']] == roles and [i['role'] for i in state['images']] == roles
    assert state['status'] in ('READY', 'UNREADY') and isinstance(state['errors'], list)
    if state['status'] == 'READY':
        assert not state['errors'] and all(i['ready'] is True for i in state['images'])
        assert state['mode'] in ('THREE_FRESH_COMPLETE_CRITICS', 'COMPLETE_FIRST_THREE_REUSED')
        assert wave == 'selected' or state['mode'] == 'THREE_FRESH_COMPLETE_CRITICS'
    else:
        assert state['errors'], 'An unready phase must retain its actual reasons'
    return state

def verify(root):
    root=archive_root(root); index_path=archive_path(root/'archive-index.json',root); index=json.loads(index_path.read_bytes());mapping={}
    for row in index['files']:
        rel=Path(row['archive_relative']);assert not rel.is_absolute() and '..' not in rel.parts
        # Reject every symlink prefix before resolving or reading any child.
        actual=archive_path(root/rel,root)
        assert actual.is_file() and digest(actual)==row['sha256'],str(actual)
        old=row['source_absolute'];assert old not in mapping;mapping[old]=actual
    assert len(mapping)==index['mapped_sources']
    source_root=index['source_root']
    physical=lambda p:mapping[str(p)]
    final=json.loads(physical(source_root+'/planning/final-evidence.json').read_bytes())
    assert final==index['closed_evidence'] and final['poster_calls_closed'] is True
    assert final['poster_role_denominator']==5 and len(final['makers'])==5 and final['poster_native_attempts']==len(final['caller_records'])<=15
    def authoritative(row):
        actual=physical(row['path']);assert digest(actual)==row['sha256']
        if 'bytes' in row:assert actual.stat().st_size==row['bytes']
        return actual
    freeze=json.loads(authoritative(final['pre_generation_freeze']).read_bytes())
    for row in freeze['runtime_files']+freeze['helpers']+freeze['references']+[freeze[k] for k in ('case','central_plan','ratio')]:authoritative(row)
    recording_freeze=json.loads(authoritative(final['critic_recording_freeze']).read_bytes())
    assert recording_freeze['actual_critic_sessions_at_freeze']==recording_freeze['live_critic_jobs_at_freeze']==0
    assert recording_freeze['production_and_quality_freeze']==final['pre_generation_freeze']
    for row in recording_freeze['files']:authoritative(row)
    assert recording_freeze['actual_native_calls_at_freeze']==0
    assert recording_freeze['quality_gates_unchanged'] and recording_freeze['overall_critic_cap']==6
    corpus=json.loads(authoritative(final['corpus']).read_bytes())
    assert len(corpus['cases'])==1 and corpus['cases'][0]['count']==5
    case=corpus['cases'][0];case_id=case['case_id'];role_ids={r['role_id'] for r in case['roles']}
    assert len(role_ids)==5 and set(final['stages'])=={'initial','selected'}
    assert all(set(stage['cases'])=={case_id} for stage in final['stages'].values())
    assert {m['role'] for m in final['makers']}==role_ids
    def compact_bytes(old):
        old=str(old)
        if old not in mapping:
            raise ValueError('Unarchived authoritative byte identifier: '+old)
        return physical(old).read_bytes()
    maker_sessions=[];call_count=0
    for maker in final['makers']:
        terminal=json.loads(authoritative(maker['terminal']).read_bytes())
        completion=json.loads(authoritative(maker['completion']).read_bytes())
        assert terminal['role']==maker['role'] and terminal['counts']==maker['counts']
        assert terminal.get('selected_stage')==maker['selected_stage']
        assert 1<=terminal['counts']['native_calls']<=3
        assert completion['exit_code']==0 and completion['input_pins_unchanged'] is True and len(completion['session_ids'])==1
        authoritative(completion['reports'][Path(maker['terminal']['path']).name]);authoritative(completion['trace'])
        maker_sessions+=completion['session_ids'];call_count+=terminal['counts']['native_calls']
    assert len(maker_sessions)==len(set(maker_sessions))==5 and call_count==final['poster_native_attempts']
    engine=module(physical(source_root+'/summarize.py'),'single_five_archived_frozen_v4')
    original_read=engine.read_json
    original_digest=engine.digest
    engine.resolve=lambda path,base:archive_path(path,root,base)
    def portable_digest(path):
        return original_digest(archive_path(path,root))
    engine.digest=portable_digest
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
        raw,byte_pin=original_read(path)
        observed=path.name in ('editorial.json','craft.json','portfolio.json')
        return alias(raw,observational=observed),byte_pin
    engine.read_json=read_json
    source_checker=module(physical(source_root+'/audit_source_assets.py'),'single_five_archived_source_checker')
    replays=[];unique_summaries=set();critic_sessions=[];actual_counts={'records':0,'score_slots':0,'valid_scores':0}
    for wave,stage in final['stages'].items():
        assert len(stage['image_gates'])==5
        global_readiness=json.loads(physical(source_root+'/reviews/'+wave+'-stage-readiness.json').read_bytes())
        authoritative(global_readiness['corpus'])
        assert global_readiness['corpus']==final['corpus']
        local_path=source_root+'/reviews/'+case_id+'/'+wave+'/readiness.json'
        local_readiness=json.loads(physical(local_path).read_bytes())
        state=review_state(global_readiness,local_readiness,case,wave,final['makers'])
        for cid,item in stage['cases'].items():
            assert set(stage['image_gates'])==role_ids
            if 'summary' not in item:
                assert state['status']=='UNREADY' and item['reason']==state['errors']
                assert item['readiness']['path']==local_path
                assert item['gate']=='NA' and stage['whole_corpus_gate']=='NA' and all(g=='NA' for g in stage['image_gates'].values())
                assert stage['image_gate_counts']=={'PASS':0,'FAIL':0,'NA':5}
                authoritative(item['readiness'])
                continue
            assert state['status']=='READY'
            reused=state['mode']=='COMPLETE_FIRST_THREE_REUSED'
            assert item['reused_complete_initial_three'] is reused
            original=item['summary']['path']
            actual_wave='initial' if reused else wave
            assert original==source_root+'/reviews/'+cid+'/'+actual_wave+'/summary.json'
            stored=json.loads(authoritative(item['summary']).read_bytes())
            stored_source=json.loads(authoritative(item['source_attestation_audit']).read_bytes())
            assert stored['case_id']==stored_source['case_id']==cid and stored['wave']==stored_source['wave']==actual_wave
            assert stored['packet']['path']==source_root+'/reviews/'+cid+'/'+actual_wave+'/packet.json'
            authoritative(stored['packet']);authoritative(state['packet'])
            assert state['packet']['path']==source_root+'/reviews/'+cid+'/'+wave+'/packet.json'
            assert stored_source['packet']=={k:v for k,v in stored['packet'].items() if k in ('path','sha256')}
            assert item['original_v4_set_gate']==stored['set_gate'] and item['original_v4_image_gates']==stored['image_gates']
            assert item['source_attestation_gate']==stored_source['gate']
            compact_path=source_root+'/reviews/'+cid+'/'+wave+'/compact-recording-audit.json'
            assert item['compact_recording_audit']['path']==compact_path
            stored_compact=json.loads(authoritative(item['compact_recording_audit']).read_bytes())
            checker_source=source_root+'/method-recording-v2/audit_compact_bindings.py'
            compact_checker=module(physical(checker_source),'single_five_archived_compact_checker_'+wave)
            compact_access=compact_checker.ByteAccess(reader=compact_bytes)
            if reused:
                authoritative(item['reuse'])
                compact=compact_checker.audit_reuse(state['packet']['path'],item['reuse']['path'],access=compact_access)
            else:
                compact=compact_checker.audit(state['packet']['path'],source_root+'/reviews/'+cid+'/'+wave+'/cli',access=compact_access)
            assert compact==stored_compact, 'Portable raw/export/completion binding replay differs'
            assert item['compact_recording_gate']==compact['gate']
            supplemental_pass=stored_source['gate']==compact['gate']=='PASS'
            expected_gate=stored['set_gate'] if supplemental_pass else 'NA'
            expected_images=stored['image_gates'] if supplemental_pass else {k:'NA' for k in stored['image_gates']}
            assert item['gate']==expected_gate and stage['image_gates']==expected_images
            assert stage['image_gate_counts']=={s:sum(g==s for g in expected_images.values()) for s in ('PASS','FAIL','NA')}
            assert stage['whole_corpus_gate']==expected_gate
            if reused:assert compact['gate']=='PASS', 'Invalid original recording cannot authorize reuse'
            if original in unique_summaries:continue
            unique_summaries.add(original); sp=physical(original); stored=json.loads(sp.read_bytes()); packet=physical(stored['packet']['path']); cli=packet.parent/'cli'
            args=types.SimpleNamespace(packet=str(packet),report=[p+'='+str(cli/p/(p+'.json')) for p in ('editorial','craft','portfolio')],completions_dir=str(cli))
            result=engine.summary(args)
            for profile in ('editorial','craft','portfolio'):
                critic_sessions.append(result['reviews'][profile]['provenance']['derived_session_id'])
            counts=result['counts'];actual_counts['records']+=counts['observed_image_profile_records'];actual_counts['score_slots']+=counts['observed_score_slots'];actual_counts['valid_scores']+=counts['valid_integer_1_to_5_score_values']
            for key in ('procedure_gate','image_gates','image_gate_counts','set_gate','counts'):
                assert result[key]==stored[key],cid+'/'+wave+'/'+key
            assert item['original_v4_set_gate']==stored['set_gate']
            assert item['original_v4_image_gates']==stored['image_gates']
            for p in ('editorial','craft','portfolio'):
                for image_id,record in result['reviews'][p]['images'].items():
                    saved=stored['reviews'][p]['images'][image_id]
                    assert ('scores' in record)==('scores' in saved) and record.get('scores')==saved.get('scores')
            source=source_checker.audit(packet,cli)
            stored_source=json.loads(physical(item['source_attestation_audit']['path']).read_bytes())
            assert source['gate']==stored_source['gate']
            assert item['source_attestation_gate']==source['gate']
            expected_gate=stored['set_gate'] if source['gate']==compact['gate']=='PASS' else 'NA'
            expected_images=stored['image_gates'] if source['gate']==compact['gate']=='PASS' else {k:'NA' for k in stored['image_gates']}
            assert item['gate']==expected_gate
            assert stage['image_gates']==expected_images
            assert stage['image_gate_counts']=={s:sum(g==s for g in expected_images.values()) for s in ('PASS','FAIL','NA')}
            assert stage['whole_corpus_gate']==expected_gate
            for p in ('editorial','craft','portfolio'):assert source['profiles'][p]['gate']==stored_source['profiles'][p]['gate']
            replays.append({'case_id':cid,'actual_summary_wave':stored['wave'],'procedure_gate':result['procedure_gate'],'image_gate_counts':result['image_gate_counts'],'set_gate':result['set_gate'],'source_attestation_gate':source['gate'],'compact_recording_gate':compact['gate'],'effective_set_gate':expected_gate})
    assert len(critic_sessions)==len(set(critic_sessions))==final['actual_unique_review_sessions']<=6
    assert not set(critic_sessions).intersection(maker_sessions) and actual_counts==final['actual_review_counts']
    raw_counts={'records':0,'score_slots':0,'valid_scores':0}
    for record in final['raw_observation_inventory']:
        raw=json.loads(authoritative(record['raw_observations']).read_bytes())
        completion=json.loads(authoritative(record['completion']).read_bytes())
        assert raw['wave']==record['wave'] and raw['profile']==record['profile'] and raw['case_id']==case_id
        assert completion['reports'][Path(record['raw_observations']['path']).name]['sha256']==record['raw_observations']['sha256']
        counts={'records':len(raw['images']),'score_slots':0,'valid_scores':0}
        for image in raw['images'].values():
            for rating in image['ratings'].values():
                counts['score_slots']+=1
                score=rating.get('score');counts['valid_scores']+=type(score) is int and 1<=score<=5
        assert counts==record['counts']
        for key in counts:raw_counts[key]+=counts[key]
    assert raw_counts==final['raw_observation_counts_separate']
    return {'status':'PASS','mapped_source_byte_checks':len(mapping),'unique_summaries_replayed':len(replays),'replays':replays,'raw_observation_counts_separate':raw_counts,'limits':['No original host path is required for aliased metadata reads. Raw byte digests and all scores/copy remain unchanged.','Raw observations and canonical quality records are both retained and explicitly bound; no absent output is fabricated.','Unready phases are retained rather than invented or replayed. Semantic viewing remains an attestation.']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=verify(a.archive)
    if a.output:
        with a.output.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2)
    print(json.dumps(r))
