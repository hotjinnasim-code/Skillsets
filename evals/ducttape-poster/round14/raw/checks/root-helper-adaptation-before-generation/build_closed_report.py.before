"""Render closed R13 facts and raw scores; no actor edits or authored scores."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DIMS=('content_form','hierarchy','typography','space','image_material','emotion_control','ai_slop')
PROFILES=('editorial','craft','portfolio')
def read(p):return json.loads(Path(p).read_bytes())
def main():
 final=read(ROOT/'planning/final-evidence.json');case=read(ROOT/'planning/single-five-case.json')['cases'][0]
 assert final['poster_calls_closed'] and final['poster_role_denominator']==case['count']==5 and final['candidate']=='M'
 lines=['# M · 새 내용의 16:9 다섯 스타일 검증','',
 '닫힌 R12의 공통 보정·선택 실패 원인을 M 지침에 반영한 뒤, 이전에 제작·평가하지 않은 성인 건축 사진전과 공간 해설 요청 한 건을 새 제작자 다섯 명으로 실행했습니다. 문구11개와 서로 다른 전체 스타일 다섯 장이 한 요청의 전체 결과이며 보정본은 새 스타일로 세지 않습니다. 한 새 내용의 제한된 전이 검증으로 모든 향후 요청의 품질이나 인과적 효과를 보장하지 않습니다.','',
 '[실제 선택본 갤러리](gallery.html) · [원문](planning/literal-landscape-request.txt) · [전체 종료 기록](planning/final-evidence.json) · [고정한 M 스킬](snapshots/candidate-m/SKILL.md)','',
 f"실제 포스터 생성 {final['poster_native_attempts']}/{final['poster_attempt_cap']}회, 독립 제작자5명, 실제 새 평가 세션{final['actual_unique_review_sessions']}개. 원본 v4 호환 출력 집계 `{final['actual_review_counts']}`, 별도 원관찰 집계 `{final['raw_observation_counts_separate']}`.",'',
 '실제 반환 원본의 너비·높이를 기록합니다. 비율 요청은16:9이며, 생성 전 선언한 한 변의 최근접 정수 반올림 허용은 최대0.5픽셀입니다. 명시적 픽셀 크기 요청에는 이 허용을 적용하지 않습니다. 원본을 자르거나 확대해 생성 해상도로 세지 않습니다. 검수용 파일의 실제 크기는 각 고정한 보기 메타데이터에 있습니다. 가로형을 폭720 및 긴 변320 이하로 축소하며 크롭·확대를 하지 않습니다. 계획 좌표와 실제 표시 크기를 구별합니다.','',
 '[모든 실제 반환의 비율 관찰](checks/root-all-stage-ratio-observations.json)을 보존합니다. 도구 반환 성공과 결과 조건·품질 통과를 구별합니다.','',
 '| 시안 | 선택 단계 | 실제 원본 | 생성 호출 |','| --- | --- | --- | ---: |']
 for m in final['makers']:
  t=read(m['terminal']['path']);n=t.get('selected_files',{}).get('original',{})
  lines.append(f"| {m['role']} | {m['selected_stage']} | {n.get('width','NA')} × {n.get('height','NA')} | {m['counts']['native_calls']} |")
 lines+=['','| 단계 | 개별 PASS / FAIL / NA | 전체 세트 |','| --- | --- | --- |']
 for wave in ('initial','selected'):
  s=final['stages'][wave];lines.append(f"| {wave} | {s['image_gate_counts']} | {s['whole_corpus_gate']} |")
 lines+=['',
 '세 독립 평가자 각각 모든 필수 조건 PASS, 일곱 품질 항목 각각4점 이상, 다섯 장 모두 PASS와 전체 다양성 각각4점 이상을 요구합니다. 평균·다수결·평가자 교체로 낮은 점수나 NA를 지우지 않습니다. AI 슬롭은 별도 품질 항목이며 제작 주체를 인증하는 검사가 아닙니다.','',
 'M은 내부 계획과 다른 결과라도 사용자 조건과 필요한 관계가 작동하면 그대로 선택하도록 합니다. 실제 실패를 해결할 때 목표 변화와 기존 장점의 변화 모두 대조하며, 보정 한도를 채울 의무나 최신 파일 자동 선택은 없습니다. 모든 포스터에 고정 격자·읽는 순서·스타일을 강요하지 않습니다. 전체 스튜디오 작업과 실제 Canva 템플릿을 현재 요청에 맞춰 적용합니다.','',
 '두 단계 모두 생성 전 고정한 동일한3필드 파일 메타데이터 기록 방식 v2를 사용합니다. 원관찰 스키마1, v4 판정·점수 바닥·정규화·루브릭·생성 한도는 바꾸지 않았습니다. 각 평가자는 자기 새 세션이 종료되기 전에 원관찰과 호환 출력을 기록합니다. [생성 전 전체 고정](planning/candidate-m-pre-generation-freeze.json) · [기록 방식 고정](planning/critic-recording-helper-freeze.json) · [메타데이터 검증](method-recording-v2/verification.json).','',
 '모든 제작자가 선택을 닫은 뒤 최초 전체 세 평가를 실행합니다. 완전히 같은 이미지·평가 맥락일 때만 불리한 기록도 포함한 최초 세 평가 전체를 재사용하고, 하나라도 달라지면 전체 다섯 장을 예정된 새 세 평가가 봅니다. 평가 피드백 뒤 추가 생성·재선택을 하지 않습니다.','']
 matrices=[]
 for wave in ('initial','selected'):
  item=final['stages'][wave]['cases'][case['case_id']];lines+=['## '+wave+' 원점수','']
  if 'summary' not in item:lines+=['실제 준비 불가 사유와 NA를 종료 기록에 보존했습니다.',''];continue
  summary=read(item['summary']['path']);sp=Path(item['summary']['path']);source_dir=sp.parent
  lines += [f"v4 절차 `{summary['procedure_gate']}`, 출처 `{item['source_attestation_gate']}`, 원관찰 연결 `{item['compact_recording_gate']}`, 적용 세트 `{item['gate']}`.",'',
   '[원본 v4와 원점수]('+sp.relative_to(ROOT).as_posix()+')'+(' · 최초 세 평가 전체 재사용' if item['reused_complete_initial_three'] else ''),'',
   '| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |','| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
  raw={p:read(source_dir/'cli'/p/(p+'.observations.json')) for p in PROFILES}
  for role in case['roles']:
   for p in PROFILES:
    obs=raw[p]['images'][role['role_id']];scores={k:obs['ratings'][k]['score'] for k in DIMS};canon=summary['reviews'][p]['images'].get(role['role_id'],{})
    if 'scores' in canon:assert scores==canon['scores']
    lines.append('| '+role['role_id']+' | '+p+' | '+' | '.join(str(scores[k]) for k in DIMS)+' |')
    matrices.append({'displayed_wave':wave,'actual_raw_wave':raw[p]['wave'],'role':role['role_id'],'profile':p,'scores':scores,'summary':item['summary'],'source_kind':'actual_immutable_raw_observations','reused_complete_initial_three':item['reused_complete_initial_three']})
  lines += ['','실제 원관찰의 다양성: '+', '.join(p+'='+str(raw[p]['set']['diversity']) for p in PROFILES)+'.','']
  for p in PROFILES:lines.append('- ['+p+' 원관찰]('+str((source_dir/'cli'/p/(p+'.observations.json')).relative_to(ROOT))+')')
  lines.append('')
 lines+=['## 확인 범위','',*['- '+x for x in final['limits']],'']
 with (ROOT/'report.md').open('x') as f:f.write('\n'.join(lines).rstrip()+'\n')
 with (ROOT/'raw-score-matrices.json').open('x') as f:json.dump({'presentation_records':matrices,'actual_unique_record_counts':final['actual_review_counts'],'source':'Untouched actual raw ratings, matched canonical records when valid. Displayed reused stages add no sessions or unique scores.'},f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps({'report':str(ROOT/'report.md'),'displayed_rows':len(matrices),'new_native_calls':0}))
if __name__=='__main__':main()
