# K · 새 내용의 16:9 다섯 스타일 검증

닫힌 R10의 공통 실패 원인을 K 지침에 반영한 뒤, 이전에 제작·평가하지 않은 성인 인쇄·낭독 행사 요청 한 건을 새 제작자 다섯 명으로 실행했습니다. 확정 문구11개, 서로 연결되는 인쇄·낭독 행동과 실제 사용 크기의 참여 안내를 요구합니다. 서로 다른 스타일 다섯 장이 이 요청의 전체 결과이며 보정본은 새 스타일로 세지 않습니다. 한 새 내용의 제한된 전이 검증으로 모든 향후 요청·장르의 품질이나 인과적 효과를 보장하지 않습니다.

[실제 선택본 갤러리](gallery.html) · [원문](planning/literal-landscape-request.txt) · [전체 종료 기록](planning/final-evidence.json) · [고정한 K 스킬](snapshots/candidate-k/SKILL.md)

실제 포스터 생성 15/15회, 독립 제작자5명, 실제 새 평가 세션6개. 원본 v4 호환 출력 집계 `{'records': 30, 'score_slots': 210, 'valid_scores': 210}`, 별도 원관찰 집계 `{'records': 30, 'score_slots': 210, 'valid_scores': 210}`.

실제 반환 원본의 너비·높이를 기록합니다. 비율 요청은16:9이며, 생성 전 선언한 한 변의 최근접 정수 반올림 허용은 최대0.5픽셀입니다. 명시적 픽셀 크기 요청에는 이 허용을 적용하지 않습니다. 원본을 자르거나 확대해 생성 해상도로 세지 않습니다. 검수용 파일의 실제 크기는 각 고정한 보기 메타데이터에 있습니다. 가로형을 폭720 및 긴 변320 이하로 축소하며 크롭·확대를 하지 않습니다. 계획 좌표와 실제 표시 크기를 구별합니다.

| 시안 | 선택 단계 | 실제 원본 | 생성 호출 |
| --- | --- | --- | ---: |
| R11-C1-M1 | repair-2 | 1672 × 941 | 3 |
| R11-C1-M2 | repair-2 | 1672 × 941 | 3 |
| R11-C1-M3 | repair-2 | 1672 × 941 | 3 |
| R11-C1-M4 | repair-2 | 1672 × 941 | 3 |
| R11-C1-M5 | repair-2 | 1672 × 941 | 3 |

| 단계 | 개별 PASS / FAIL / NA | 전체 세트 |
| --- | --- | --- |
| initial | {'PASS': 0, 'FAIL': 5, 'NA': 0} | FAIL |
| selected | {'PASS': 2, 'FAIL': 3, 'NA': 0} | FAIL |

세 독립 평가자 각각 모든 필수 조건 PASS, 일곱 품질 항목 각각4점 이상, 다섯 장 모두 PASS와 전체 다양성 각각4점 이상을 요구합니다. 평균·다수결·평가자 교체로 낮은 점수나 NA를 지우지 않습니다. AI 슬롭은 별도 품질 항목이며 제작 주체를 인증하는 검사가 아닙니다.

K는 한 행사·과정에 속한 여러 행동의 요청된 관계, 분산 정보의 다음 목적지와 함께 읽는 그룹, 실제 사용 크기의 기능 검수, 원문 기호의 광학적 구별과 제작자의 실패한 설계 관계 재구성을 강화합니다. 원문에 없는 순서·인물·활동을 만들지 않으며 명시적 스타일·분리·배치·글자만의 구성은 사용자 조건을 따릅니다. 다섯 매체·팔레트·레이아웃을 미래의 고정 목록으로 만들지 않습니다. 새 전체 스튜디오 작품과 실제 Canva 템플릿에서 관찰한 관계를 이 요청의 내용에 맞춰 설계했습니다.

두 단계 모두 생성 전 고정한 동일한3필드 파일 메타데이터 기록 방식 v2를 사용합니다. 원관찰 스키마1, v4 판정·점수 바닥·정규화·루브릭·생성 한도는 바꾸지 않았습니다. 각 평가자는 자기 새 세션이 종료되기 전에 원관찰과 호환 출력을 기록합니다. [생성 전 전체 고정](planning/candidate-k-pre-generation-freeze.json) · [기록 방식 고정](planning/critic-recording-helper-freeze.json) · [메타데이터 검증](method-recording-v2/verification.json).

모든 제작자가 선택을 닫은 뒤 최초 전체 세 평가를 실행합니다. 완전히 같은 이미지·평가 맥락일 때만 불리한 기록도 포함한 최초 세 평가 전체를 재사용하고, 하나라도 달라지면 전체 다섯 장을 예정된 새 세 평가가 봅니다. 평가 피드백 뒤 추가 생성·재선택을 하지 않습니다.

## initial 원점수

v4 절차 `PASS`, 출처 `PASS`, 원관찰 연결 `PASS`, 적용 세트 `FAIL`.

[원본 v4와 원점수](reviews/R11-C1/initial/summary.json)

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R11-C1-M1 | editorial | 4 | 4 | 4 | 4 | 3 | 4 | 3 |
| R11-C1-M1 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M2 | craft | 4 | 3 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 3 | 4 |
| R11-C1-M3 | editorial | 4 | 4 | 4 | 4 | 3 | 4 | 3 |
| R11-C1-M3 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M3 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M4 | editorial | 4 | 4 | 4 | 4 | 3 | 4 | 3 |
| R11-C1-M4 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M4 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M5 | editorial | 4 | 4 | 4 | 4 | 3 | 4 | 3 |
| R11-C1-M5 | craft | 3 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M5 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

실제 원관찰의 다양성: editorial=4, craft=4, portfolio=4.

- [editorial 원관찰](reviews/R11-C1/initial/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R11-C1/initial/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R11-C1/initial/cli/portfolio/portfolio.observations.json)

## selected 원점수

v4 절차 `PASS`, 출처 `PASS`, 원관찰 연결 `PASS`, 적용 세트 `FAIL`.

[원본 v4와 원점수](reviews/R11-C1/selected/summary.json)

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R11-C1-M1 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M1 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M2 | craft | 4 | 3 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M3 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M3 | craft | 4 | 3 | 4 | 4 | 3 | 4 | 4 |
| R11-C1-M3 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M4 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M4 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M4 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M5 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R11-C1-M5 | craft | 4 | 4 | 4 | 4 | 3 | 4 | 3 |
| R11-C1-M5 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

실제 원관찰의 다양성: editorial=4, craft=4, portfolio=4.

- [editorial 원관찰](reviews/R11-C1/selected/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R11-C1/selected/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R11-C1/selected/cli/portfolio/portfolio.observations.json)

## 확인 범위

- One prospectively new landscape request after whole R10 closure; bounded transfer, no future guarantee.
- K generic runtime guidance and new case-specific planning differ from J; no isolated causal or statistical success-rate claim.
- Same prospective three-field recording instrumentation in both phases; score gates and normalization unchanged.
- Fresh sessions are trace-backed; semantic image viewing remains an attestation.
- Source provenance joins caller-literal returned identifiers, caller persistence/save-native commands, fresh CLI sessions, source/cache/manifests and exact hashes. Preserved ephemeral CLI traces expose no direct native MCP invocation/result events.
- All five makers closed before initial review preparation. ROOT provenance closure first failed on unsupported literal-return metadata; gallery and initial review packet/jobs were then prepared prematurely. Those files were retained; successful corrected production closure precedes all actual critic starts, as checked against their runner timestamps.
- No client assets; preservation and one-image editing remain untested by this case.

