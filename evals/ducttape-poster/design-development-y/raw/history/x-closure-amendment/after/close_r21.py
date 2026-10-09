"""Close a completed single five without changing raw judgments or selections."""
from pathlib import Path
import datetime
import hashlib
import json

TASK = Path(__file__).resolve().parents[1]
ROUND = TASK / 'work/round21'
PROFILES = ('editorial', 'craft', 'portfolio')

def read(path):
    if isinstance(path, dict):
        path = path['path']
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path).resolve(strict=True)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

def write(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')

maker_path = ROUND / 'planning/all-five-maker-closure.json'
maker = read(maker_path)
assert maker['all_five_completed'] and len(maker['makers']) == 5
sessions = []
for row in maker['makers']:
    assert pin(row['completion']['path']) == row['completion']
    assert row['outcome'] in ('selection', 'unavailable')
    assert pin(row['terminal']['path']) == row['terminal']
    if row['outcome'] == 'selection':
        assert row['selection'] == row['terminal'] and row['unavailable'] is None
    else:
        assert row['unavailable'] == row['terminal'] and row['selection'] is None
        assert row['selected_stage'] is None
    completion = read(row['completion'])
    assert completion['exit_code'] == 0 and completion['input_pins_unchanged']
    assert completion['session_ids'] == row['sessions']
    sessions.extend(completion['session_ids'])
maker_session_count = len(sessions)
assert maker_session_count == 5 and len(set(sessions)) == maker_session_count

waves = {}
for wave in ('initial', 'selected'):
    phase = ROUND / 'reviews/R21-C1' / wave
    readiness_path = phase / 'readiness.json'
    state = read(readiness_path)
    reused = wave == 'selected' and (phase / 'reuse.json').is_file()
    if state['status'] == 'UNREADY':
        assert not state['jobs'] and not reused and not (phase / 'summary.json').is_file()
        assert not any((phase / 'cli' / profile / 'completion.json').is_file() for profile in PROFILES)
        waves[wave] = {
            'recording_mode':'unready complete-set wave; original readiness retained without replacement critics',
            'readiness_mode':state.get('mode'),
            'procedure_gate':'NA','procedure_errors':state['errors'],
            'image_gate_counts':{'PASS':0,'FAIL':0,'NA':5},
            'image_gates':{row['role']:'NA' for row in maker['makers']},'set_gate':'NA',
            'counts':{'requested_images':5,'critics':0,'expected_critics':3,'expected_image_profile_records':15,
                      'observed_image_profile_records':0,'expected_score_values':105,
                      'observed_score_slots':0,'valid_integer_1_to_5_score_values':0},
            'summary':None,'readiness':pin(readiness_path),'critics':{},'audits':[],
            'new_critic_processes':0,'new_critic_sessions':0,'new_score_values':0,
        }
        continue
    assert state['status'] == 'READY'
    if reused:
        assert state['mode'] == 'COMPLETE_FIRST_THREE_REUSED'
        assert all(row['selected_stage'] == 'initial' for row in maker['makers'])
        reuse = read(phase / 'reuse.json')
        assert read(phase / 'compact-binding-audit.json')['gate'] == 'PASS'
        assert pin(reuse['initial_summary']['path'])['sha256'] == reuse['initial_summary']['sha256']
        summary_path = Path(reuse['initial_summary']['path'])
    else:
        assert state['mode'] == 'THREE_FRESH_COMPLETE_CRITICS' and len(state['jobs']) == 3
        summary_path = phase / 'summary.json'
    summary = read(summary_path)
    assert summary['case_id'] == 'R21-C1' and summary['wave'] == ('initial' if reused else wave)
    assert summary['counts']['expected_image_profile_records'] == 15
    assert summary['counts']['expected_score_values'] == 105
    actors = {}
    for profile in PROFILES:
        completion_path = (ROUND / 'reviews/R21-C1/initial' if reused else phase) / 'cli' / profile / 'completion.json'
        completion = read(completion_path)
        # A process can close with a nonzero exit; the original summary retains
        # its procedure NA rather than requiring a replacement critic.
        assert type(completion['exit_code']) is int and completion.get('completed_utc')
        trace_path = Path(completion['trace']['path'])
        trace_error = None
        try:
            events = [json.loads(line) for line in trace_path.read_text().splitlines() if line.strip()]
        except (ValueError, OSError) as exc:
            events = []
            trace_error = str(exc)
        actual_sessions = [event['thread_id'] for event in events if isinstance(event, dict)
                           and event.get('type') == 'thread.started' and isinstance(event.get('thread_id'), str)
                           and event['thread_id']]
        if not reused:
            sessions.extend(actual_sessions)
        actors[profile] = {
            'completion': pin(completion_path), 'completed_utc': completion['completed_utc'],
            'exit_code': completion['exit_code'], 'input_pins_unchanged': completion.get('input_pins_unchanged'),
            'trace': pin(trace_path), 'reported_trace': completion['trace'], 'trace_read_error': trace_error,
            'session_ids': actual_sessions, 'reported_session_ids': completion.get('session_ids'),
            'session_ids_match_trace': actual_sessions == completion.get('session_ids'),
            'trace_error_events_retained': [event for event in events if isinstance(event, dict)
                                           and event.get('type') in ('error', 'turn.failed')],
        }
    waves[wave] = {
        **{key: summary[key] for key in ('procedure_gate', 'procedure_errors', 'image_gate_counts', 'image_gates', 'set_gate', 'counts')},
        'summary': pin(summary_path),
        'readiness': pin(readiness_path), 'readiness_mode': state['mode'],
        'diversity_original': {profile: summary['reviews'][profile]['set']['raw'].get('diversity') for profile in PROFILES},
        'audits': ([pin(ROUND / 'reviews/R21-C1/initial/source-asset-audit.json'),pin(phase / 'compact-binding-audit.json')] if reused else [pin(phase / name) for name in ('source-asset-audit.json', 'compact-binding-audit.json')]),
        'critics': actors,
        'recording_mode':'exact whole-context original initial records retained' if reused else 'three fresh complete-set critic processes; original errors and raw retained',
        'new_critic_processes':0 if reused else len(actors),
        'new_critic_sessions':0 if reused else sum(len(actor['session_ids']) for actor in actors.values()),
        'new_score_values':0 if reused else summary['counts']['valid_integer_1_to_5_score_values'],
    }
critic_session_count = sum(data['new_critic_sessions'] for data in waves.values())
critic_process_count = sum(data['new_critic_processes'] for data in waves.values())
assert critic_process_count in (0,3,6)
assert len(sessions) == maker_session_count + critic_session_count
freeze_path = ROUND / 'planning/candidate-x-pre-generation-freeze.json'
for row in read(freeze_path)['runtime']:
    assert pin(row['path']) == row

closure = {
    'closed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'candidate': 'X', 'case': 'R21-C1', 'one_request': True, 'requested_images': 5,
    'matched_development': True, 'pre_held_out': False,
    **maker['counts'], 'initial_selected': maker['initial_selected'],
    'initial_retained_without_repairs': maker['initial_retained_without_repairs'],
    'unavailable_roles': maker['unavailable_roles'],
    'client_assets': 0, 'supporting_guides': 5,
    'maker_sessions': maker_session_count, 'critic_sessions': critic_session_count, 'all_actors_closed': True,
    'critic_processes': critic_process_count, 'actor_processes': len(maker['makers']) + critic_process_count,
    'actual_session_ids_unique': len(set(sessions)) == len(sessions),
    'production_closure': pin(maker_path), 'pre_generation_freeze': pin(freeze_path),
    'waves': waves, 'no_post_critic_repair_or_reselection': True,
    'quality_thresholds_changed': False,
    'limits': [
        'The same plant-market request after complete R20 feedback is matched development, not a pre-held-out trial, causal isolation or universal success rate.',
        'All low scores, ambiguities, failures, transport errors and original selections remain retained.',
        'Native font descriptions and accumulated reference observations do not certify applied font files, exact Unicode or every image being high-end.',
        'Five logical maker roles ran with an actual maximum of three workers; this is not simultaneous five execution.',
    ],
}
write(ROUND / 'planning/full-five-closure.json', closure)
counts = maker['counts']
rows = []
for wave, label in (('initial', '최초'), ('selected', '선택')):
    data = waves[wave]
    c = data['image_gate_counts']
    rows.append(f"| {label} | {c['PASS']} | {c['FAIL']} | {c['NA']} | {data['set_gate']} | {data['counts']['valid_integer_1_to_5_score_values']} / 105 |")
initial_record_link = ('[최초 원집계](reviews/R21-C1/initial/summary.json)' if waves['initial']['summary']
                       else '[최초 준비 상태](reviews/R21-C1/initial/readiness.json)')
report = f'''# R21 / X — 목적 식별·본문 안내 연결·전체 구성 차이를 먼저 설계한 다섯 방향

R20 전체 평가를 닫은 뒤 같은 식물 마켓 원문·12개 카피·조건·16:9 비율·빈 사용자 자산을 보존해 한 요청의 다섯 제작 역할을 실행했다. 첫 읽기에서 실제 목적·이름·약속·참여를 연결하고, 본문과 실용 안내의 실제 시작·끝·정렬·전환 및 다섯 방향의 큰 이미지와 카피 형태를 함께 설계하는 X 일반 지침을 먼저 고정했다. 복합 본문과 안내를 기존 글꼴·렌더러로 먼저 스케치하는 조건부 W 흐름은 유지했다. 사용자 자산은 없으며 중앙이 새로 만든 독립 스케치 다섯 개를 각 제작자에게 자기 것만 제공했다. 축적한 디자인 아이디어를 사용하고 조사 원본을 매 제작자에게 다시 열도록 요구하지 않았다. 스케치는 클라이언트 구도 보존 조건이나 최종 중립 스타일이 아니며, 이미지는 네이티브 도구로 요청하고 실제 반환·선택 여부를 종료 기록에 남겼다.

다섯 제작자의 네이티브 호출은 {counts['native_calls']}회, 반환 {counts['returned']}회, 실패 {counts['failed']}회다. 보정 호출은 {counts['repair_calls']}회이며 최초본 선택은 {maker['initial_selected']}개, 보정 없이 최초본으로 종료한 역할은 {maker['initial_retained_without_repairs']}개다. 세 호출 모두 실패해 선택 이미지가 없는 역할은 {maker['unavailable_roles']}개다. 실제 최대 세 작업자로 논리적 다섯 역할을 실행했다. 보정본은 새 스타일로 세지 않는다.

| 단계 | PASS | FAIL | NA | 전체 세트 | 유효 일곱 원점수 |
| --- | ---: | ---: | ---: | --- | ---: |
''' + '\n'.join(rows) + f'''

최초·선택 단계는 실제 준비 상태와 fresh·reuse·UNREADY 기록 방식에 따라 닫았다. 준비되지 않은 단계는 해당 오류·5 NA·새 점수 0개·새 평가자 0명을 보존한다. 준비된 새 평가 단계에는 전체 다섯 장의 원본·사용 크기·축소 보기를 판단할 독립 평가자 세 명을 배정한다. 모두 같은 최초본이고 전체 문맥의 유효한 원기록을 재사용할 수 있으면 그 기록을 그대로 연결하며 새 점수나 세션으로 세지 않는다. 같은 최초본의 재사용이 절차 오류로 불가능하면 오류를 남기고 평가자를 교체하지 않는다. 실제 새 평가 CLI 프로세스는 최초 {waves['initial']['new_critic_processes']}개, 선택 {waves['selected']['new_critic_processes']}개이며 trace에서 확인된 새 세션은 최초 {waves['initial']['new_critic_sessions']}개, 선택 {waves['selected']['new_critic_sessions']}개다. 프로세스의 종료와 평가 절차의 유효성은 구분하고 실패한 종료·입력 핀·trace 오류도 그대로 보존한다. 세 평가자 각각의 일곱 항목 모두 4 이상, 전체 다양성 각각 4 이상, 필수 조건이라는 기존 기준을 유지했다. 평균·낮은 점수 삭제·평가자 교체·평가 뒤 재생성·재선택을 하지 않았다. 실제 오류·불확실성·절차 NA도 원기록에 남긴다.

[전체 종료](planning/full-five-closure.json) · {initial_record_link} · [선택 단계 기록](reviews/R21-C1/selected/readiness.json) · [실제 선택 이미지](gallery.html)

이 기록은 피드백 뒤 같은 요청의 개발 관찰이다. 지침·중앙 계획·가이드가 함께 달라졌으며 사전에 격리한 시험·보편적인 하이엔드 품질·AI 제작 주체 판별·지침 하나의 인과 효과를 입증하지 않는다. 복합 본문의 실제 면적과 읽는 길, 내용 관계에 따른 전체 구성을 첫 생성 전에 구체화하는 일반 절차를 강화했다. 레퍼런스의 수·명성이나 가이드의 폰트 렌더링은 최종 네이티브 폰트 적용 또는 결과 품질의 증거가 아니다. 단순 문구·글자 없는 요청·사용 가능한 런타임이 없는 경우는 새 설치 없이 긍정적인 네이티브 명세를 사용한다.
'''
with (ROUND / 'report.md').open('x', encoding='utf-8') as handle:
    handle.write(report)
print(json.dumps({'closure': pin(ROUND / 'planning/full-five-closure.json'), 'waves': {wave: {'counts': data['image_gate_counts'], 'set': data['set_gate']} for wave, data in waves.items()}}))
