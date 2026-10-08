"""Independent metadata/byte review. Never decode or display image pixels."""
from reviewlib import A,O,read,js
from pathlib import PurePosixPath,PureWindowsPath
import os,json,hashlib,struct,re,datetime,collections
from html.parser import HTMLParser

index=js('archive-index.json');root=index['source_root']
lookup={};cache={};checks=[]
def check(name,ok,detail,location):
    checks.append({'check':name,'passed':bool(ok),'detail':detail,'source':location})
def source(s):
    return os.path.normpath(s if PurePosixPath(s).is_absolute() else root+'/'+s)
def blob(s,expected=None):
    s=source(str(s));r=lookup[s]
    b=cache[r['archive_relative']]
    if expected is not None:
        check('exact source pin',hashlib.sha256(b).hexdigest()==expected,s,s)
    return b
def doc(s,expected=None):return json.loads(blob(s,expected))
def pin(p):return blob(p['path'],p['sha256'])
def pd(p):return json.loads(pin(p))
def dims(p):
    b=pin(p);assert b[:8]==b'\x89PNG\r\n\x1a\n' and b[12:16]==b'IHDR'
    return list(struct.unpack('>II',b[16:24]))
def time(s):
    z=datetime.datetime.fromisoformat(s.replace(' UTC','+00:00').replace('Z','+00:00'))
    assert z.tzinfo is not None
    return z.timestamp()
def peak(intervals):
    active=maximum=0
    for _,d in sorted([(s,1) for s,e in intervals]+[(e,-1) for s,e in intervals]):
        active+=d;maximum=max(active,maximum)
    assert active==0
    return maximum
def norm(s):return ' '.join(s.split())

for r in index['files']:
    rel=r['archive_relative'];p=PurePosixPath(rel)
    assert rel and '\\' not in rel and not p.is_absolute() and not PureWindowsPath(rel).is_absolute() and '..' not in p.parts
    walk=A
    for part in p.parts:
        walk=walk/part;assert not walk.is_symlink()
    assert walk.resolve().is_relative_to(A) and walk.is_file()
    if rel not in cache:cache[rel]=read(rel,binary=True)
    check('indexed bytes',hashlib.sha256(cache[rel]).hexdigest()==r['sha256'],rel,'archive-index.json#/files')
    assert r['source_absolute'] not in lookup
    lookup[r['source_absolute']]=r
assert index['file_count']==len(lookup)==1125
for r in index['required_sources']:
    blob(r['path'],r['sha256'])
    if r.get('expected_sha256') is not None:blob(r['path'],r['expected_sha256'])
for r in index['raw_sources']:pin(r)
e=js('raw/planning/final-evidence.json')
plan=doc('planning/phase-plan.json');cases=pd(plan['cases'])['cases']
directions=pd(plan['directions'])['directions']
scheduled={s['id']:(c['id'],s['ratio']) for c in cases for s in c['slots']}
assert len(cases)==4 and len(scheduled)==20 and len(directions)==20
assert set(scheduled)==set(e['images'])=={d['role'] for d in directions}
assert len(plan['frozen_skill_files'])==6
for p in plan['frozen_skill_files']:pin(p)
for p in plan['prior_closed_records']:
    old=pd(p);assert old['whole_recorded']==128 and old['call_phases']=='ALL_CLOSED'
calls=pd(e['call_validation']);records=calls['records']
assert calls['status']=='PASS' and calls['call_phase']=='CLOSED'
assert not calls['missing'] and not calls['pending'] and not calls['errors']
assert len(records)==47 and calls['unused_new_R6_attempts_retired']==13
assert calls['no_further_native_generation'] is True
counts=collections.Counter(r['role'] for r in records)
assert dict(counts)==calls['role_counts'] and set(counts)==set(scheduled)
assert max(counts.values())==3
outcomes={};intervals=[];prompt_lf=[];native_dimensions=collections.Counter()
for r in records:
    role,stage=r['role'],r['stage'];k={'initial':0,'repair-1':1,'repair-2':2}[stage]
    m=doc(r['outcome_path'],r['outcome_sha256']);outcomes[role,stage]=m
    base=root+'/production/'+role+'/'+stage
    assert r['kind']=='returned native' and r['case_id']==scheduled[role][0]
    assert (m['role'],m['case_id'],m['stage'])==(role,r['case_id'],stage)
    assert m['target_ratio']==scheduled[role][1]
    assert r['outcome_path']==base+'/manifest.json'==r['manifest']
    assert r['outcome_sha256']==r['manifest_sha256']
    assert m['own_correction_number']==k and m['native_call_number_for_role']==k+1
    args=doc(m['call_input_path']);pre=doc(m['precall_plan_path'])
    assert m['call_input_path']==base+'/call-input.json' and m['precall_plan_path']==base+'/pre-call.json'
    assert args==m['call_input'] and args.get('transparent_background') is False and 'num_last_images_to_include' not in args
    assert (pre['role'],pre['case_id'],pre['stage'],pre['own_correction_number'])==(role,r['case_id'],stage,k)
    assert pre['phase_plan']=={'path':root+'/planning/phase-plan.json','sha256':lookup[root+'/planning/phase-plan.json']['sha256']}
    for key in ['cases','directions']:assert pre[key]==plan[key]
    assert sorted((source(p['path']),p['sha256']) for p in pre['frozen_skill_files'])==sorted((source(p['path']),p['sha256']) for p in plan['frozen_skill_files'])
    prompt=blob(base+'/prompt.txt').decode()
    assert prompt==args['prompt'] or prompt==args['prompt']+'\n'
    if prompt!=args['prompt']:prompt_lf.append([role,stage])
    assert re.search(r'maximum.{0,60}resolution|최대.{0,40}해상도',args['prompt'],re.I|re.S)
    assert time(plan['created_utc'])<=r['start']==time(m['started_at_utc'])<=r['end']==time(m['completed_at_utc'])
    intervals.append((r['start'],r['end']))
    hashes=[]
    for key in ['tool_source','original','final']:
        pin(m[key]);hashes.append(m[key]['sha256'])
        if key!='tool_source':assert m[key]['path']==base+'/'+key+'.png'
    assert len(set(hashes))==1 and hashes[0]==r['native_sha256']
    d=dims(m['final']);assert d==[m['width'],m['height']]==r['dimensions']
    native_dimensions[tuple(d)]+=1
    for key,q in m['qa_views'].items():
        expected=[720,round(d[1]*720/d[0])] if key=='usage720' else [round(d[0]*320/max(d)),round(d[1]*320/max(d))]
        assert q['path']==base+'/'+key+'.png' and dims(q)==[q['width'],q['height']]==expected
    inspection=doc(base+'/inspection.json')
    assert (inspection['role'],inspection['case_id'],inspection['stage'])==(role,r['case_id'],stage)
    if k:
        previous=outcomes[role,'initial' if k==1 else 'repair-1'];parent=previous['final']
        assert time(previous['completed_at_utc'])<=r['start']
        assert pre['parent_native']==parent['path'] and pre['parent_sha256']==parent['sha256']
        if 'referenced_image_paths' in args:assert args['referenced_image_paths']==[parent['path']]
        comp=doc(base+'/parent-comparison.json')
        if 'role' in comp:assert comp['role']==role
        if 'stage' in comp:assert comp['stage']==stage
        if 'case_id' in comp:assert comp['case_id']==r['case_id']
        if 'parent_stage' in comp:assert comp['parent_stage']==('initial' if k==1 else 'repair-1')
        for key in ['parent_native','actual_parent_native']:
            if key in comp:assert comp[key]==parent['path']
        for key in ['current_native','child_native','actual_child_native']:
            if key in comp:assert comp[key]==m['final']['path']
        for key in ['parent_sha256']:
            if key in comp:assert comp[key]==parent['sha256']
        for key in ['current_sha256','child_sha256']:
            if key in comp:assert comp[key]==m['final']['sha256']
    else:
        assert pre['parent_native'] is None and pre['parent_sha256'] is None and 'referenced_image_paths' not in args
assert peak(intervals)==calls['actual_recorded_interval_peak']==3
native_hashes={m['final']['sha256'] for m in outcomes.values()}
assert sorted(native_hashes)==index['unique_native_hashes'] and len(native_hashes)==47
registry=pd(e['production_registry']);registered={r['role']:r for r in registry['roles']}
assert set(registered)==set(scheduled)
resumed=sorted(r for r,v in registered.items() if v.get('resumed_worker_name'))
assert resumed==sorted(registry['fresh_context_exception_roles'])==['R6-C4-M3','R6-C4-M4','R6-C4-M5']
for role,reg in registered.items():
    assert e['images'][role]['ordinary_selection']=={'path':reg['selection'],'sha256':reg['sha256']}
    s=doc(reg['selection'],reg['sha256']);m=outcomes[role,s['selected_stage']]
    assert s['role']==role and s['case_id']==m['case_id']
    assert s['selected_native']==m['final']['path'] and s['sha256']==m['final']['sha256']
    assert [s['width'],s['height']]==[m['width'],m['height']]
    assert s.get('manifest',s.get('manifest_path'))==root+'/production/'+role+'/'+s['selected_stage']+'/manifest.json'
    assert s['call_count']==reg['native_calls']==counts[role] and s['own_corrections']==reg['own_corrections']==counts[role]-1
    assert {source(x['path'] if isinstance(x,dict) else x) for x in s['all_stage_paths']}=={root+'/production/'+role+'/'+stage for r,stage in outcomes if r==role}

dispatch=doc('cli-reviews/dispatch-plan.json');all_done=doc('cli-reviews/all-completed.json')
jobs={(j['wave'],j['profile']) for j in dispatch['jobs']}
assert len(jobs)==len(dispatch['jobs'])==dispatch['primary_assignments']==all_done['assignments']==24
assert dispatch['concurrency']==3 and dispatch['automatic_retry'] is False
assert dispatch['calls_closed']==e['call_validation']
completed={(r['wave'],r['profile']):r for r in all_done['results']}
assert set(completed)==jobs
sessions={};cli_intervals=[];trace_stats={};raws={};discrepancies=[]
for wave,profile in sorted(jobs):
    base='cli-reviews/'+wave+'/'+profile
    launch=doc(base+'/launch.json');done=doc(base+'/completion.json')
    assert all(done[k]==v for k,v in launch.items()) and completed[wave,profile]==done
    assert launch['dispatch_plan']=={'path':root+'/cli-reviews/dispatch-plan.json','sha256':lookup[root+'/cli-reviews/dispatch-plan.json']['sha256']}
    assert (launch['wave'],launch['profile'])==(wave,profile)
    argv=launch['argv'];assert argv[:6]==['codex','--no-daemon','--ask-for-approval','never','exec','--ephemeral']
    assert not {'resume','fork','--model','-m'}&set(argv) and '--json' in argv
    assert argv[argv.index('-C')+1]==root+'/blind-'+wave
    assert launch['fresh_session'] is True and launch['model_override'] is None and launch['raw_outputs_absent_at_dispatch'] is True
    assert done['exit_code']==0 and done['input_pins_unchanged'] is True
    assert time(calls['closed_utc'])<=time(launch['started_utc'])<=time(done['completed_utc'])
    cli_intervals.append((time(launch['started_utc']),time(done['completed_utc'])))
    assert launch['prompt']['path']==root+'/'+base+'/prompt.txt';pin(launch['prompt']);pin(done['stderr'])
    assert done['trace']['path']==root+'/'+base+'/trace.jsonl'
    events=[json.loads(l) for l in pin(done['trace']).decode().splitlines() if l.strip()]
    ids=[v['thread_id'] for v in events if v.get('type')=='thread.started']
    assert len(ids)==1 and ids[0]==done['cli_session_id'] and done['thread_started_event_count']==1
    assert ids[0] not in sessions;sessions[ids[0]]=[wave,profile]
    assert any(v.get('type')=='turn.completed' for v in events) and not any(v.get('type')=='turn.failed' for v in events)
    items=[v['item'] for v in events if v.get('type')=='item.completed']
    commands=[v['command'] for v in items if v.get('type')=='command_execution']
    imageitems=[v for v in items if 'view_image' in str(v.get('tool','')) or v.get('type') in ['image_view','view_image']]
    first_packet=next((i for i,v in enumerate(commands) if 'packet.json' in v),None)
    action_reads=[i for i,v in enumerate(commands) if profile+'-action-first.json' in v and ('cat ' in v or 'read_text' in v or 'json.load' in v)]
    for name,h in launch['input_pins'].items():blob('blind-'+wave+'/'+name,h)
    assert set(launch['input_pins'])=={'packet.json','preflight.json','review-protocol.md'}
    assert set(done['reports'])=={profile+'.json',profile+'.md',profile+'-action-first.json'}
    for name,p in done['reports'].items():
        assert p['path']==root+'/blind-'+wave+'/reviews/'+name;pin(p)
    raw=pd(done['reports'][profile+'.json']);raws[wave,profile]=raw
    action=pd(done['reports'][profile+'-action-first.json'])
    assert raw['reviewer']==action['reviewer']==profile
    assert raw['order_compliant'] is True and action['order_compliant'] is True
    trace_stats[wave,profile]={'wave':wave,'profile':profile,'session_id':ids[0],'serialized_image_view_item_count':len(imageitems),'reported_main_view_record_count':len(raw['viewed']),'completed_item_types':dict(collections.Counter(v.get('type') for v in items)),'visible_command_count':len(commands),'first_packet_command_index':first_packet,'visible_action_record_read_command_indices':action_reads,'visible_action_read_before_first_packet_command':first_packet is not None and any(i<first_packet for i in action_reads)}
    for ident,obs in raw['images'].items():
        for t in obs['mandatory']['transcription']:
            computed=norm(t['required'])==norm(t['observed'])
            if t['equal']!=computed:
                discrepancies.append({'wave':wave,'profile':profile,'image_id':ident,'raw_report':done['reports'][profile+'.json'],'required':t['required'],'observed':t['observed'],'reported_equal':t['equal'],'primary_comparator_equal':computed,'same_non_whitespace_characters':''.join(t['required'].split())==''.join(t['observed'].split())})
assert peak(cli_intervals)==3
inventory=doc('planning/review-trace-inventory.json')
assert inventory['assignments']==24 and inventory['actual_recorded_cli_interval_peak']==3
for row in inventory['rows']:
    assert all(row[k]==v for k,v in trace_stats[row['wave'],row['profile']].items());pin(row['trace'])

DIMS={'content_form','hierarchy','typography','space','image_material','emotion_control','ai_slop'}
CORE={'content_form','typography','image_material','ai_slop'}
PROFILES={'editorial','craft','portfolio'}
observation_counts=collections.Counter();score_counts=collections.Counter();gate_counts={};cases_summary=[]
selected_hashes=set();changed_member_total=0
for cid,group in e['sets'].items():
    closure=pd(e['closure_refs'][cid]);assert closure['case_id']==cid and closure['external_critics_not_yet_dispatched'] is True
    pin(closure['root_inspection']);rows={};phase_sessions={};phase_gates={}
    for phase in ['first','final']:
        rows[phase]={r['role']:r for r in pd(closure[phase+'_selection'])['selected']}
        assert set(rows[phase])==set(group['roles']) and len(rows[phase])==5
    changed_roles=[r for r in group['roles'] if rows['first'][r]['sha256']!=rows['final'][r]['sha256']]
    changed_member_total+=len(changed_roles)
    assert bool(changed_roles)==closure['physical_set_changed']==group['physical_set_changed']
    assert (closure['review_waves']['first']!=closure['review_waves']['final'])==bool(changed_roles)
    for phase,skey,bkey,okey,gatekey in [('first','initial_selection','initial_binding','initial_reviewers','initial_image_gate'),('final','selected','binding','reviewers','final_image_gate')]:
        ref=e['summary_refs'][cid+'/'+phase];summary=pd(ref);wave=closure['review_waves'][phase]
        assert summary['wave']==ref['wave']==wave and ref['available'] is True
        expected_selection=closure['first_selection' if phase=='final' and not changed_roles else phase+'_selection']
        selectionchecks=[r for r in summary['source_pin_checks'] if r['kind']=='selection']
        assert len(selectionchecks)==1 and selectionchecks[0]['path']==expected_selection['path'] and selectionchecks[0]['expected_sha256']==selectionchecks[0]['actual_sha256']==expected_selection['sha256']
        for p in summary['source_pin_checks']:
            blob(p['path'],p['expected_sha256']);assert p['actual_sha256']==p['expected_sha256']
        assert summary['selected_image_count']==5 and summary['image_critic_record_count']==len(summary['image_critic_records'])==15 and summary['score_observation_count']==105
        assert set(summary['review_procedure'])==PROFILES
        phase_sessions[phase]=set()
        for profile,proc in summary['review_procedure'].items():
            done=pd(proc['cli_completion']);launch=pd(proc['cli_launch']);pin(proc['cli_trace'])
            assert (done['wave'],done['profile'])==(wave,profile)
            assert proc['cli_session_id']==done['cli_session_id'] and proc['cli_assignment_valid'] is True
            assert proc['cli_trace']==done['trace']
            for key,hkey in [('raw_report','raw_report_sha256'),('raw_markdown','raw_markdown_sha256'),('preflight','preflight_sha256')]:
                assert done['reports'][PurePosixPath(proc[key]).name]=={'path':proc[key],'sha256':proc[hkey]}
            assert launch['input_pins']=={PurePosixPath(p['path']).name:p['expected_sha256'] for p in summary['source_pin_checks'] if p['kind']=='sealed packet file'}
            phase_sessions[phase].add(proc['cli_session_id'])
        assert len(phase_sessions[phase])==3
        accepted=ref['accepted'];assert accepted==(summary['recorded_evidence_integrity']=='PASS')
        if accepted:assert set(ref['accepted_session_ids'])==phase_sessions[phase]
        else:assert ref['accepted_session_ids']==[]
        mapping_doc=doc('private/'+wave+'-mapping.json');packet=doc('blind-'+wave+'/packet.json')
        assert mapping_doc['selection']==expected_selection
        byrole={r['role']:r for r in mapping_doc['mapping']};byid={r['image_id']:r for r in packet['images']}
        assert len(byrole)==len(byid)==5 and set(byrole)==set(group['roles'])
        bindings={b['role']:b for b in summary['image_bindings']}
        obs_by_pair={(r['role'],r['profile']):r for r in summary['image_critic_records']}
        assert len(obs_by_pair)==15 and set(obs_by_pair)=={(r,p) for r in group['roles'] for p in PROFILES}
        image_gates={}
        for role in group['roles']:
            image=e['images'][role];row=rows[phase][role];b=image[bkey];selected_hashes.add(row['sha256'])
            assert row==image[skey] and b==bindings[role]
            assert b['role']==row['role']==role and b['case_id']==row['case_id']==cid and b['stage']==row['stage']
            assert b['source_native']==row['final_native'] and b['native_sha256']==row['sha256']
            assert b['source_manifest']==row['manifest'] and b['source_manifest_sha256']==row['manifest_sha256']
            m=doc(row['manifest'],row['manifest_sha256']);assert m==outcomes[role,row['stage']]
            assert m['final']=={'path':row['final_native'],'sha256':row['sha256']}
            mapped=byrole[role];item=byid[b['image_id']]
            assert all(mapped[k]==v for k,v in row.items()) and mapped['image_id']==b['image_id'] and item['case_id']==cid
            assert set(b['views'])=={'native','usage720','thumbnail320'}
            for view,p in b['views'].items():
                assert p['path']==item[view] and dims(p)==p['dimensions']
                assert mapped['qa_hashes'][p['path']]==p['sha256']==(m['final'] if view=='native' else m['qa_views'][view])['sha256']
            obs=image[okey];assert len(obs)==3 and {o['profile'] for o in obs}==PROFILES
            fails=[]
            for o in obs:
                assert o==obs_by_pair[role,o['profile']] and o['image_id']==b['image_id'] and o['role']==role and o['case_id']==cid
                raw=doc(o['raw_path'],o['raw_sha256']);z=raw['images'][b['image_id']]
                assert all(o[k]==z[k] for k in ['mandatory','scores','evidence','residuals'])
                assert set(z['scores'])==DIMS and all(type(v) is int and 1<=v<=5 for v in z['scores'].values())
                expected_views={(b['image_id'],v,p['path']) for v,p in b['views'].items()}
                assert expected_views<={(v['image_id'],v['view'],v['path']) for v in raw['viewed']}
                mandatory=z['mandatory'];fails.append(mandatory['pass'] is not True or mandatory['use_readings']['all_required_copy_legible_at720'] is not True or any(norm(t['required'])!=norm(t['observed']) for t in mandatory['transcription']) or any(z['scores'][d]<4 for d in CORE))
                observation_counts[phase]+=1;score_counts[phase]+=len(z['scores'])
            gate='NOT_ASSESSABLE' if not accepted else ('FAIL' if any(fails) else 'PASS')
            assert image[gatekey]==gate and image['initial_binding_assessable' if phase=='first' else 'binding_assessable']==accepted
            image_gates[role]=gate
        setobs=group['initial_reviewers' if phase=='first' else 'final_reviewers'];assert len(setobs)==3 and {o['profile'] for o in setobs}==PROFILES
        assert set(packet['sets'][cid]['members'])==set(byid)
        for o in setobs:
            raw=doc(o['raw_path'],o['raw_sha256']);z=raw['sets'][cid]
            assert all(o[k]==z[k] for k in ['members','diversity','closest_pair','evidence','residuals'])
            assert set(o['members'])==set(byid) and len(o['members'])==5
        gate='NOT_ASSESSABLE' if not accepted else ('PASS' if all(v=='PASS' for v in image_gates.values()) and all(o['diversity']>=4 for o in setobs) else 'FAIL')
        assert group['initial_case_gate' if phase=='first' else 'final_case_gate']==gate
        phase_gates[phase]=gate
    if changed_roles:assert phase_sessions['first'].isdisjoint(phase_sessions['final'])
    cases_summary.append({'case_id':cid,'changed_roles':changed_roles,'physical_set_changed':bool(changed_roles),'case_gates':phase_gates,'first_sessions':sorted(phase_sessions['first']),'final_sessions':sorted(phase_sessions['final'])})
for phase,key in [('first','initial_image_gate'),('final','final_image_gate')]:
    counts=dict(collections.Counter(x[key] for x in e['images'].values()));gate_counts[phase]=counts
    assert counts==e['initial_image_gate_counts' if phase=='first' else 'final_image_gate_counts']=={'PASS':1,'FAIL':14,'NOT_ASSESSABLE':5}
    assert observation_counts[phase]==60 and score_counts[phase]==420
assert len(selected_hashes)==33 and changed_member_total==13
saved=doc('planning/transcription-discrepancies.json')
assert saved['discrepancy_count']==saved['whitespace_only_discrepancy_count']==len(discrepancies)==16
key=lambda r:(r['wave'],r['profile'],r['image_id'],r['required'])
assert sorted(saved['rows'],key=key)==sorted(discrepancies,key=key)
assert all(r['same_non_whitespace_characters'] for r in discrepancies)
recover=doc('planning/procedural-recovery-decisions.json')
assert len(recover['decisions'])==2 and all(r['case_id']=='R6-C2' and r['additional_assignments']==0 and r['terminal_stage_gate']=='NOT_ASSESSABLE' for r in recover['decisions'])

class Gallery(HTMLParser):
    def __init__(self):super().__init__();self.cards=[];self.links=[];self.cur=None;self.in_h3=False;self.cell=None;self.row=None;self.texts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article':self.cur={'title':'','rows':[],'images':[],'hrefs':[]}
        if tag=='h3':self.in_h3=True
        if tag=='tr' and self.cur is not None:self.row=[]
        if tag in ['td','th'] and self.row is not None:self.cell=''
        for key in ['href','src']:
            if key in a:
                self.links.append(a[key])
                if self.cur is not None:self.cur['images' if key=='src' else 'hrefs'].append(a[key])
    def handle_data(self,s):
        self.texts.append(s)
        if self.cur is not None and self.in_h3:self.cur['title']+=s
        if self.cell is not None:self.cell+=s
    def handle_endtag(self,tag):
        if tag=='h3':self.in_h3=False
        if tag in ['th','td'] and self.cell is not None:self.row.append(self.cell);self.cell=None
        if tag=='tr' and self.row is not None:
            self.cur['rows'].append(self.row);self.row=None
        if tag=='article':self.cards.append(self.cur);self.cur=None
gallery=Gallery();gallery.feed(read('gallery.html'))
assert len(gallery.cards)==20
ordered=['content_form','hierarchy','typography','space','image_material','emotion_control','ai_slop']
for card in gallery.cards:
    role,gate=card['title'].split(' · ');image=e['images'][role]
    assert gate==image['final_image_gate']
    assert card['images']==[lookup[image['binding']['views']['usage720']['path']]['archive_relative']]
    assert lookup[image['selected']['final_native']]['archive_relative'] in card['hrefs']
    assert lookup[image['initial_selection']['final_native']]['archive_relative'] in card['hrefs']
    table={row[0]:list(map(int,row[1:])) for row in card['rows'] if row and row[0] in PROFILES}
    assert table=={o['profile']:[o['scores'][d] for d in ordered] for o in image['reviewers']}
for link in gallery.links:
    if link.startswith('#'):continue
    assert '://' not in link and not PurePosixPath(link).is_absolute() and '..' not in PurePosixPath(link).parts
    assert (A/link).is_file() and (A/link).resolve().is_relative_to(A)
md=read('report.md')
sections=re.split(r'^### (R6-C[1-4]-M[1-5]): ',md,flags=re.M)
assert (len(sections)-1)//2==20
for i in range(1,len(sections),2):
    role,section=sections[i:i+2];image=e['images'][role]
    assert section.startswith(image['initial_image_gate']+' → '+image['final_image_gate'])
    table={m.group(1):list(map(int,m.group(2).strip().split(' | '))) for m in re.finditer(r'^\| (editorial|craft|portfolio) \| (.*?) \|$',section,re.M)}
    assert table=={o['profile']:[o['scores'][d] for d in ordered] for o in image['reviewers']}
assert all(role in md for role in resumed)
assert '최대 지원 해상도는 요청했지만 실제 반환 픽셀만 기록한다' in md
assert '실제 시각 조회·전사·읽는 순서는 별도의 평가자 진술' in md
assert '네 요청에 묶인 20장' in md

result={'status':'PASS','indexed_source_count':len(lookup),'unique_indexed_files':len(cache),'raw_source_count':len(index['raw_sources']),'pinned_source_count':len(index['required_sources']),
        'closed_native_calls':len(records),'returned_native_calls':47,'failed_native_calls':0,'pending_calls':calls['pending'],'missing_roles':calls['missing'],
        'native_peak':peak(intervals),'cli_peak':peak(cli_intervals),'cli_assignments':len(jobs),'unique_cli_sessions':len(sessions),'resumed_roles':resumed,
        'native_dimension_counts':{'x'.join(map(str,k)):v for k,v in native_dimensions.items()},'first_final_native_union':len(selected_hashes),'unused_native_stages_outside_first_final_reviews':47-len(selected_hashes),
        'prompt_extra_terminal_lf':prompt_lf,'case_closures':cases_summary,'image_critic_counts':dict(observation_counts),'raw_score_counts':dict(score_counts),'image_gate_counts':gate_counts,
        'whitespace_discrepancy_count':len(discrepancies),'trace_serialized_image_view_counts':sorted({s['serialized_image_view_item_count'] for s in trace_stats.values()}),
        'reported_main_views':sum(s['reported_main_view_record_count'] for s in trace_stats.values()),'gallery_cards':len(gallery.cards),'checks_executed':len(checks),'check_failures':[c for c in checks if not c['passed']]}
assert not result['check_failures']
(O/'independent-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(O/'independent-pin-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
