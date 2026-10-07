#!/usr/bin/env python3
# coding: utf-8
"""Generate bounded evaluation tables directly from preserved closed records."""
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);a=ap.parse_args();r=a.archive.resolve();read=lambda p:json.loads(p.read_text());idx=read(r/'archive-index.json');lookup={x['source_absolute']:x['archive_relative'] for x in idx['files']};f=read(r/'raw/planning/final-delivery-evidence.json');calls=read(r/'raw/planning/full-validation-closed.json');control=f.get('required_transfer_evidence');status='PASS' if f['predeclared_gate_pass'] else 'FAIL'
def link(source):return lookup[source]
rows=[]
for cid,c in f['sets'].items():
 critics=[critic for role in c['selected_roles'] for critic in f['selected_images'][role]['reviewers'].values()]
 vals=[min(x['scores'][d] for x in critics) for d in ['content_form','typography','image_material','ai_slop']]
 diversity=min(x['diversity'] for x in c['reviewers'].values()) if len(c['selected_roles'])>1 else '단일'
 rows.append('| '+cid+' | '+' | '.join(map(str,[*vals,diversity]))+' |')
if control:
 vals=[min(x['scores'][d] for x in control['image_critic_records']) for d in ['content_form','typography','image_material','ai_slop']];rows.append('| type-only-control (추가) | '+' | '.join(map(str,[*vals,'단일']))+' |')
history=[]
for wave,label in [('initial','D 초기'),('correction1','E/D 첫 보정'),('correction2','E/D 두 번째 보정'),('material-initial','F 사진 전이·이전 짝'),('transfer-initial','G 자형/접점 전이·F 짝'),('transfer-correction1','F/G 첫 보정 묶음'),('transfer-correction2','F/G 두 번째 보정 묶음'),('transfer-correction3','T01 마지막 자체 보정 후 전체 묶음')]:
 p=r/f'raw/planning/neutral-{wave}-closed-summary.json'
 if not p.exists():continue
 s=read(p);history.append(f"| {label} | {s['selected_image_count']} | {len(s['critics'])} | {s['core_below4_count']} | {s['noncore_below4_count']} | {s['diversity_below4_count']} | {s['predeclared_core_diversity_gate']} |")
physical=[]
for role,x in f['selected_images'].items():physical.append(f"| {role} | {x.get('phase','이전')} / {x['stage']} | {x['width']}×{x['height']} | [원본]({link(x['final_native_absolute'])}) · [720]({link(x['views']['usage720']['path'])}) · [320]({link(x['views']['thumbnail320']['path'])}) |")
noncore=[]
for x in f['other_sub4_scores']:noncore.append(f"| {x['role']} | {x['profile']} | {x['dimension']} | {x['score']} |")
if control:
 for x in control['other_sub4']:noncore.append(f"| T01 (추가) | {x['profile']} | {x['dimension']} | {x['score']} |")
phase=[]
for name in ['D','E','F','G']:
 cap=24 if name=='D' else 6 if name in ['E','F'] else 9
 used=calls[name+'_used'];phase.append(f'| {name} | {used} | {cap} | {cap-used} |')
text=f'''# 덕테이프 포스터: 재질·자형·접점 전이 평가

선택 14장과 추가 제약 전이 1장의 **사전 핵심/다양성 기준은 {status}**다. 문구·사용자 조건을 먼저 확인하고 내용·형태, 타이포그래피, 이미지·재질, AI 슬롭은 모든 해당 평가자에게 각각 4 이상, 다중 이미지 세트 다양성도 각각 4 이상이어야 한다. 평균으로 낮은 점수를 상쇄하지 않았다. [선택 근거](raw/planning/final-delivery-evidence.json), [오프라인 갤러리](gallery.html), [정확한 바이트 대응표](archive-index.json)를 함께 제공한다.

이는 여러 버전의 검증된 선택 모음이다. 최신 G 전체를 14장 새로 생성한 시험이나 모든 미래 입력의 품질·인간 제작 여부·실제 제품 기능·인쇄 적합성의 보장이 아니다. 가장 최근 G는 서로 다른 새 원본 3개를 검사했다. 이전 전체 FAIL과 낮은 점수·평가 차이도 보존했다.

## 일반 사용과 변경

기본 요청은 중앙 조정자가 내용에서 다섯 방향을 정하고 제작자 다섯 명이 한 장씩 맡는다. 가용 자리가 다섯이면 동시에 시작하고, 자리가 적으면 5개 역할을 유지해 나누어 실행한다. 사용자 지정 수량·스타일·참조와 한 장의 후속 수정이 우선한다. 이 환경은 root 포함 4자리였으며 실제 정원 기본 5개 역할은 2+2+1로 실행했다. 정원 호출 구간의 최대 중첩은 2, 전체 기록의 최대 중첩은 {calls['actual_cross_phase_interval_peak']}이다. 다섯 명의 실제 동시 실행을 주장하지 않는다. 협업 도구가 없으면 직접 동일 기준으로 만들고 에이전트 실행을 주장하지 않는다.

일반 생성에는 별도 세 평가자를 강제로 추가하지 않는다. 이번 개선 요청에서 생성·수정과 독립된 평가자 세 명의 루프를 실행했다. 기본 스타일은 고정 목록 대신 내용의 행동·구조·글자·매체에서 결정하며, 주제보다 효과가 먼저 보이는 범용 패키지의 우선순위를 낮춘다. 사용자가 지정한 네온·3D·거친 표현은 같은 완성도 기준으로 존중한다.

동결 D에 E/F/G의 일반 지침 6문단을 더했다. E는 카피·공간의 실제 관계를 먼저 정하고 생성 뒤 찾도록 한다. F는 표면의 세부가 대상 규모·빛·초점에 맞는지, 국소 보정 밖의 사진 표면·윤곽도 변했는지 비교한다. G는 긴 문자열·혼합 문자의 자형에 맞춰 폭과 크기를 확보하고, 압축 대신 면적·줄 묶음·간격을 조정하며, 실제 글자 끝과 대상 경계의 접점까지 설계한다. 스타일 금지·새로움 강요·평가 점수 인상으로 해결하지 않았다. [G 동결](raw/continuation-g/planning/phase-plan.json)에 실제 적용 6파일 해시와 호출 전 경계를 남겼다.

## 자료와 적용 판단

앞 단계에서 실제 확인한 공식 디자인 자료와 GitHub 경로 이력을 [고정된 조사 출처](raw/planning/research-provenance.json)로 재사용했다. 28개 디자인 이미지의 확인 이력이 있으며 이번 단계에 다시 열었다고 주장하지 않는다. 원작 픽셀·카피·로고·구도를 제작자나 저장소에 이식하지 않았다.

[Everyday Practice 2025 한국 예술축제](https://everyday-practice.com/2025-korea-art-festival/)와 [2026 대한민국 문학축제](https://everyday-practice.com/2026-%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD-%EB%AC%B8%ED%95%99%EC%B6%95%EC%A0%9C/)의 실제 정보 위계, [HAY Backflip 공식 자료](https://www.hay.com/news/news-2026/backflip-chair-by-gudmundur-ludvik)의 접힘·접점, [2019 시민 민요축제](https://everyday-practice.com/the-1st-folk-song-festival-poster/)의 운영 정보 관계를 비교했다. 이는 새 구성에 적용한 해석이다. 2026 문학축제 페이지 게시일은 10월 6일이고 HAY의 정확한 게시일은 확인되지 않았다. [frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)와 [canvas-design](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md)의 실제 경로 커밋도 앞 단계 출처 기록에 고정했다.

## 독립 평가 이력

각 행은 그때의 전체 익명 패킷 결과이며 서로 다른 평가자의 원점수다. 사전 원본/너비720/장변320 세 보기를 실제 열고 각 카피를 수동 전사했다. 새 신청 포스터는 원문 패킷 전에 720에서 행사일·신청 기한·전체 URL·위치를 읽어 저장했다. 첫 보정의 craft는 저장 실패 뒤 원문을 열었음을 기록했고, 사전 선언한 추가 ordered craft를 포함해 **네 평가자의 점수를 모두 유지**했다. 그 절차 실패를 소급 해소하거나 불리한 점수를 버리지 않았다.

| 단계 | 패킷 이미지 | 평가자 | 핵심 <4 | 기타 <4 | 세트 다양성 <4 | 판정 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
'''+ '\n'.join(history)+'''

[G 전이 전체 리뷰](raw/blind-transfer-initial/reviews/)에는 F P01 자체 첫 보정, F H01 원본, G P02/H02 새 원본, G T01 한 장 제약이 포함된다. 추가 T01은 글자와 여백만 사용하며 선택 14장의 대체물이 아니다. T01 실패도 최종 완료 기준에 포함하며 단일 결과에 없는 다양성/가까운 짝 점수를 만들지 않았다. 모든 7항목의 원점수·보이는 근거·불확실성과 가까운 짝의 비기준 점수를 유지했다.

F P01 자체 첫 보정은 글자의 역할을 바꾸면서 접힌 컵·뚜껑을 약85–90 원본 픽셀 이동시키고 미세 표면을 다소 부드럽게 했다. [보존 비교](raw/continuation-f/production/P01/repair-1/preservation-inspection.json)에 남겼으며 정확한 사진 보존을 주장하지 않는다. 보정 전후 중 최신이라는 이유만으로 채택하지 않았다.

## 선택 묶음의 기준

정원 5개는 닫힌 correction2의 완전한 세트 근거, 제품·모집 각2개는 최신 전이의 완전한 세트 근거다. 그대로 유지한 해안 정화2·명시 네온2·사진 독서대1은 [이전 5장 대응 근거](raw/planning/retained-five-bindings.json)의 원본·실제 보기·리뷰·절차 63개 파일과 해시로 연결한다. 전체 옛 FAIL을 새 선택 PASS로 복사하지 않았다. 아래는 각 사례의 모든 이미지/평가자 중 최저점이다.

| 사례 | 내용·형태 | 타이포 | 이미지·재질 | AI 슬롭 | 다양성 |
| --- | ---: | ---: | ---: | ---: | --- |
'''+ '\n'.join(rows)+'''

핵심 네 항목 외에 4 미만으로 남은 관찰은 다음과 같다. 위치·원인과 모든 점수 차이는 원본 근거에 있다.

| 역할 | 평가자 | 항목 | 점수 |
| --- | --- | --- | ---: |
'''+ ('\n'.join(noncore) if noncore else '| 없음 | — | — | — |')+'''

## 실제 파일과 닫힌 경계

| 역할 | 버전·단계 | 실제 원본 크기 | 파일 |
| --- | --- | --- | --- |
'''+ '\n'.join(physical)+'''

원본 바이트를 보존하고 확인용 720/320만 축소했다. 1122×1402의 4:5 상대 오차 0.035663%는 사전1% 허용 안이지만 수학적으로 정확한4:5라고 부르지 않는다. 내장 도구에 가능한 최대 해상도를 요청했으며 실제 크기는 위에 공개한다. 도구가 크기 설정을 제공하지 않아 최대 달성을 인증하지 않았다.

| 단계 | 실제 호출 | 변경하지 않은 상한 | 미사용 폐기 |
| --- | ---: | ---: | ---: |
'''+ '\n'.join(phase)+f'''

앞서 닫힌95회를 포함한 전체 기록은 **{calls['whole_recorded']}회**다. D/E 호출은116에서 닫아 미사용9회를 폐기했다. 일반 지침을 실제 바꾼 F/G는 각6/9의 별도 사전 경계에서 이전 장면을 참조하지 않는 새 발상을 검사했다. 닫힌 D/E의 숨긴 세 번째 보정이나 상한 초기화로 세지 않았다. 모든 원본은 재생성을 포함해 자체 보정 최대2회를 지켰다. 새 단계 전후의 계획125/122/131 최대값 스냅샷과 도중 INCOMPLETE도 그대로 보존했다. F 계획의 종료 설명에 이전24라는 문구가 남았으나 수치 상한6과 검증기는 처음부터6으로 고정됐으며 실제 호출과 폐기를 공개한다.

[닫힌 호출 검증](raw/planning/full-validation-closed.json), [별도 품질 조립](raw/planning/final-delivery-evidence.json), [이식 가능한 바이트 감사](portable-audit.json)를 구분한다. 저장소 대응표를 사용하는 감사는 옛 작업 폴더 없이 해시·PNG 치수·리뷰 원점수·보기·절차를 확인한다. 실제 보기/선행 순서/위치 근거는 평가자의 기록이며 코드가 시각 판단이나 시간 순서를 인증하지 않는다. 옛 전체 패킷·리뷰에 언급된 미선택 비교 원본 전체까지 보관했다고 주장하지 않는다. 브라우저 렌더링 검수를 수행했다고 주장하지 않으며 갤러리는 파일 대응으로 확인했다.
'''
if control:
 latest=read(r/link(control['source_summary_ref']['path']))['wave']
 text=text.replace('raw/blind-transfer-initial/reviews/', 'raw/blind-'+latest+'/reviews/').replace('F P01 자체 첫 보정, F H01 원본', 'F P01 '+f['selected_images']['P01']['stage']+', F H01 '+f['selected_images']['H01']['stage']).replace('G P02/H02 새 원본, G T01 한 장 제약', 'G P02 '+f['selected_images']['P02']['stage']+', G H02 '+f['selected_images']['H02']['stage']+', G T01 한 장 제약 선택본')
 text+='''

## 절차 오류와 보존 비교

transfer-correction1은 품질 FAIL이며 H02 제작 기록의 해시가 평가 묶음 고정 이후 변경돼 전체 출처 연결도 FAIL이다. 원본 이미지 바이트는 같았지만 옛 기록을 소급 통과시키지 않았다. [불일치 기록](raw/planning/transfer-correction1-manifest-drift.json)을 보존하고 다음 전체 묶음은 제작자의 저장 완료 뒤 새로 고정했다. 마감일 필드에서 “신청”을 제외한 관찰도 마감일로 읽도록 형식 어댑터를 수정했으며, 전체 문구 대조와 평가 원점수는 그대로 남겼다.

F P01은 자체 두 보정에서 남은 타이포 문제를 기록하고, 사전에 원본을 다시 선택해 변경된 짝과 함께 전체 사례를 새로 평가했다. 이전 짝의 다양성 점수를 빌려오지 않았다. F H01의 첫 보정은 렌즈·금속 미세 표면이, G P02의 첫 보정은 천의 미세 결이 바뀌었다. [H01 비교](raw/continuation-f/production/H01/repair-1/parent-comparison.json)와 [P02 비교](raw/continuation-g/production/P02/repair-1/parent-comparison.json)에 남겼으며 정확한 사진 보존을 주장하지 않는다.

[별도 사전 감사](raw/planning/pre-archive-independent-audit.md)는 G의 제약 사례 T01 근거를 빼도 조립기가 통과하던 결함을 발견했다. 수정 뒤 T01 누락을 거부하는지 확인했으며, 기존 FAIL의 점수·보기·해시는 보존했다.

transfer-correction2의 제품·모집 사례는 세 평가자 모두 핵심·다양성 기준을 통과했지만, T01에서 한 평가자가 희미한 이중 글자 윤곽에 이미지·재질 3과 AI 슬롭 3을 주어 전체는 FAIL이다. [마지막 자체 보정 사전 계획](raw/continuation-g/planning/T01-repair-2-plan.json)은 해당 원인만 고치도록 제한하고, 두 번째 보정 뒤에도 전체 다섯 이미지를 새 평가자 세 명이 판단하도록 정했다. 불리한 평가자를 제외하거나 점수를 평균내지 않았다.

T01 두 번째 보정은 검정 채움이 균일해졌지만 제작자는 희미한 윤곽과 바탕 얼룩의 완전 제거를 확인하지 못했다고 [검수](raw/continuation-g/production/T01/repair-2/inspection.json)에 남겼다. 마지막 독립 판정과 이 불확실성을 함께 보존하며, 통과를 모든 합성 흔적의 절대적 부재로 해석하지 않는다.
'''
(r/'report.md').write_text(text,encoding='utf-8');print('Wrote report from exact closed records; no scores rewritten.')
