# M · 새 내용의 16:9 다섯 스타일 검증

닫힌 R12의 공통 보정·선택 실패 원인을 M 지침에 반영한 뒤, 이전에 제작·평가하지 않은 성인 건축 사진전과 공간 해설 요청 한 건을 새 제작자 다섯 명으로 실행했습니다. 문구11개와 서로 다른 전체 스타일 다섯 장이 한 요청의 전체 결과이며 보정본은 새 스타일로 세지 않습니다. 한 새 내용의 제한된 전이 검증으로 모든 향후 요청의 품질이나 인과적 효과를 보장하지 않습니다.

[실제 선택본 갤러리](gallery.html) · [원문](planning/literal-landscape-request.txt) · [전체 종료 기록](planning/final-evidence.json) · [고정한 M 스킬](snapshots/candidate-m/SKILL.md)

실제 포스터 생성 8/15회, 독립 제작자5명, 실제 새 평가 세션6개. 원본 v4 호환 출력 집계 `{'records': 30, 'score_slots': 210, 'valid_scores': 210}`, 별도 원관찰 집계 `{'records': 30, 'score_slots': 210, 'valid_scores': 210}`.

실제 반환 원본의 너비·높이를 기록합니다. 비율 요청은16:9이며, 생성 전 선언한 한 변의 최근접 정수 반올림 허용은 최대0.5픽셀입니다. 명시적 픽셀 크기 요청에는 이 허용을 적용하지 않습니다. 원본을 자르거나 확대해 생성 해상도로 세지 않습니다. 검수용 파일의 실제 크기는 각 고정한 보기 메타데이터에 있습니다. 가로형을 폭720 및 긴 변320 이하로 축소하며 크롭·확대를 하지 않습니다. 계획 좌표와 실제 표시 크기를 구별합니다.

[모든 실제 반환의 비율 관찰](checks/root-all-stage-ratio-observations.json)을 보존합니다. 도구 반환 성공과 결과 조건·품질 통과를 구별합니다.

| 시안 | 선택 단계 | 실제 원본 | 생성 호출 |
| --- | --- | --- | ---: |
| R13-C1-M1 | initial | 1672 × 941 | 1 |
| R13-C1-M2 | initial | 1672 × 941 | 1 |
| R13-C1-M3 | initial | 1672 × 941 | 1 |
| R13-C1-M4 | repair-1 | 1672 × 941 | 2 |
| R13-C1-M5 | repair-1 | 1672 × 941 | 3 |

| 단계 | 개별 PASS / FAIL / NA | 전체 세트 |
| --- | --- | --- |
| initial | {'PASS': 0, 'FAIL': 0, 'NA': 5} | NA |
| selected | {'PASS': 0, 'FAIL': 4, 'NA': 1} | NA |

세 독립 평가자 각각 모든 필수 조건 PASS, 일곱 품질 항목 각각4점 이상, 다섯 장 모두 PASS와 전체 다양성 각각4점 이상을 요구합니다. 평균·다수결·평가자 교체로 낮은 점수나 NA를 지우지 않습니다. AI 슬롭은 별도 품질 항목이며 제작 주체를 인증하는 검사가 아닙니다.

M은 내부 계획과 다른 결과라도 사용자 조건과 필요한 관계가 작동하면 그대로 선택하도록 합니다. 실제 실패를 해결할 때 목표 변화와 기존 장점의 변화 모두 대조하며, 보정 한도를 채울 의무나 최신 파일 자동 선택은 없습니다. 모든 포스터에 고정 격자·읽는 순서·스타일을 강요하지 않습니다. 전체 스튜디오 작업과 실제 Canva 템플릿을 현재 요청에 맞춰 적용합니다.

두 단계 모두 생성 전 고정한 동일한3필드 파일 메타데이터 기록 방식 v2를 사용합니다. 원관찰 스키마1, v4 판정·점수 바닥·정규화·루브릭·생성 한도는 바꾸지 않았습니다. 각 평가자는 자기 새 세션이 종료되기 전에 원관찰과 호환 출력을 기록합니다. [생성 전 전체 고정](planning/candidate-m-pre-generation-freeze.json) · [기록 방식 고정](planning/critic-recording-helper-freeze.json) · [메타데이터 검증](method-recording-v2/verification.json).

모든 제작자가 선택을 닫은 뒤 최초 전체 세 평가를 실행합니다. 완전히 같은 이미지·평가 맥락일 때만 불리한 기록도 포함한 최초 세 평가 전체를 재사용하고, 하나라도 달라지면 전체 다섯 장을 예정된 새 세 평가가 봅니다. 평가 피드백 뒤 추가 생성·재선택을 하지 않습니다.

## initial 원점수

v4 절차 `NA`, 출처 `PASS`, 원관찰 연결 `NA`, 적용 세트 `NA`.

[원본 v4와 원점수](reviews/R13-C1/initial/summary.json)

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R13-C1-M1 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M1 | craft | 4 | 4 | 4 | 3 | 4 | 3 | 4 |
| R13-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M3 | editorial | 3 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M3 | craft | 3 | 3 | 4 | 3 | 4 | 4 | 4 |
| R13-C1-M3 | portfolio | 3 | 3 | 4 | 4 | 4 | 3 | 4 |
| R13-C1-M4 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M4 | craft | 4 | 4 | 3 | 4 | 4 | 4 | 4 |
| R13-C1-M4 | portfolio | 4 | 4 | 3 | 4 | 4 | 4 | 4 |
| R13-C1-M5 | editorial | 3 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M5 | craft | 3 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M5 | portfolio | 3 | 4 | 4 | 4 | 4 | 3 | 4 |

실제 원관찰의 다양성: editorial=4, craft=3, portfolio=4.

- [editorial 원관찰](reviews/R13-C1/initial/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R13-C1/initial/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R13-C1/initial/cli/portfolio/portfolio.observations.json)

## selected 원점수

v4 절차 `PASS`, 출처 `PASS`, 원관찰 연결 `PASS`, 적용 세트 `NA`.

[원본 v4와 원점수](reviews/R13-C1/selected/summary.json)

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R13-C1-M1 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M1 | craft | 4 | 3 | 3 | 3 | 4 | 4 | 4 |
| R13-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M3 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M3 | craft | 3 | 3 | 3 | 4 | 4 | 4 | 4 |
| R13-C1-M3 | portfolio | 4 | 3 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M4 | editorial | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M4 | craft | 4 | 4 | 3 | 3 | 4 | 4 | 4 |
| R13-C1-M4 | portfolio | 5 | 4 | 3 | 4 | 4 | 4 | 4 |
| R13-C1-M5 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R13-C1-M5 | craft | 3 | 3 | 3 | 4 | 4 | 3 | 4 |
| R13-C1-M5 | portfolio | 3 | 4 | 4 | 4 | 4 | 4 | 4 |

실제 원관찰의 다양성: editorial=4, craft=3, portfolio=4.

- [editorial 원관찰](reviews/R13-C1/selected/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R13-C1/selected/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R13-C1/selected/cli/portfolio/portfolio.observations.json)

## 확인 범위

- One prospectively new architecture-photography exhibition landscape request after whole R12 closure; bounded transfer, no future guarantee.
- M generic guidance, new case content, actual references and specific planning differ together; no isolated causal/statistical success-rate claim.
- Same prospective three-field recording instrumentation in both phases; score gates and normalization unchanged.
- Fresh sessions are trace-backed; semantic image viewing remains an attestation.
- Source joins caller-literal returned identifiers, persistence/save-native commands, fresh CLI sessions, source/cache/manifests and exact hashes. Ephemeral CLI traces expose no direct native MCP invocation/result events.
- All five makers and ROOT production closure precede initial review preparation and actual critic starts. No critic feedback is used to regenerate or reselect.
- Both phases use predeclared supported anonymous-single-five label; raw case/path identifiers remain visible, so no universal or copy blindness is claimed.
- ROOT views are recorded separately with actual unique files and reused phase slots; ROOT has read the case/plan and is not a blind scored critic.
- First ROOT production closure failed on the existing literal tool_result_metadata container alias; a ROOT-only explicit alias was added and 8 actual joins plus 12 unsafe synthetic representations were checked before successful closure and any critic packet/launch. Raw actors, images, choices and frozen methods were unchanged; checks/source-alias-history retains the failure and reader diff.
- After production closure and during the initial critic run the human explicitly rejected solid/near-solid backgrounds dominated by gothic text blocks. The later message is not in either original packet and does not replace raw ratings; planning/user-style-exclusion-after-production.json records the separate development requirement. M is not adopted as final on the basis of these original scores.
- Initial editorial completed a fresh session and all 35 valid raw scores with exit 0 after recoverable WebSocket reconnect/fallback messages. The frozen v4 procedure treats these trace errors as invalid, so initial canonical procedure/recording and all five gates remain NA; raw ratings are retained separately. No scoring-method change or critic replacement is made.
- No client assets; supplied-asset preservation and one-image follow-up editing remain untested by this case.
