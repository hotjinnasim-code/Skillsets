# J · 16:9 한 요청의 다섯 스타일 개발 검증

닫힌 R9에서 드러난 공통 원인을 J 지침에 반영한 뒤 같은 야외 영화 행사 원문을 새 제작자 다섯 명으로 실행했습니다. 이미 피드백을 본 요청을 다시 쓰는 개발 검증이며, 미관측 전이 시험은 아닙니다. 서로 다른 스타일 다섯 장이 한 요청의 전체 결과이고 보정본은 새 스타일로 세지 않습니다.

[실제 선택본 갤러리](gallery.html) · [원문](planning/literal-landscape-request.txt) · [전체 종료 기록](planning/final-evidence.json) · [고정한 J 스킬](snapshots/candidate-j/SKILL.md)

실제 포스터 생성 11/15회, 독립 제작자5명, 실제 새 평가 세션6개. 원본 v4 호환 출력 집계 `{'records': 30, 'score_slots': 210, 'valid_scores': 208}`, 별도 원관찰 집계 `{'records': 30, 'score_slots': 210, 'valid_scores': 208}`.

실제 반환 원본의 너비·높이를 기록합니다. 비율 요청은16:9이며, 생성 전 선언한 한 변의 최근접 정수 반올림 허용은 최대0.5픽셀입니다. 명시적 픽셀 크기 요청에는 이 허용을 적용하지 않습니다. 원본을 자르거나 확대해 생성 해상도로 세지 않습니다. 실제 검수용 사용 크기는720×405, 축소는320×180입니다. 계획의1280×720은 실제 렌더링이 아닌 설계 좌표입니다.

| 시안 | 선택 단계 | 실제 원본 | 생성 호출 |
| --- | --- | --- | ---: |
| R10-C1-M1 | initial | 1672 × 941 | 1 |
| R10-C1-M2 | initial | 1672 × 941 | 1 |
| R10-C1-M3 | repair-2 | 1672 × 941 | 3 |
| R10-C1-M4 | repair-2 | 1672 × 941 | 3 |
| R10-C1-M5 | repair-2 | 1672 × 941 | 3 |

| 단계 | 개별 PASS / FAIL / NA | 전체 세트 |
| --- | --- | --- |
| initial | {'PASS': 2, 'FAIL': 3, 'NA': 0} | FAIL |
| selected | {'PASS': 2, 'FAIL': 1, 'NA': 2} | NA |

세 독립 평가자 각각 모든 필수 조건 PASS, 일곱 품질 항목 각각4점 이상, 다섯 장 모두 PASS와 전체 다양성 각각4점 이상을 요구합니다. 평균·다수결·평가자 교체로 낮은 점수나 NA를 지우지 않습니다. AI 슬롭은 별도 품질 항목이며 제작 주체를 인증하는 검사가 아닙니다.

J는 호출명과 표현 조건 구분, 실제 비율에서 정보 면적·읽는 흐름 배분, 접촉 소유·연결의 표현 후 재검사, 작은 기호의 형태·간격과 판독을 강화합니다. 명시적 글자만의 구성은 사용자 조건을 따릅니다. 다섯 매체·팔레트·레이아웃을 미래의 고정 목록으로 만들지 않습니다. 실제 전체 스튜디오 작품과 대중적 Canva 정보 묶음을 참고해 이 요청의 방향을 다시 설계했습니다.

두 단계 모두 생성 전 고정한 동일한3필드 파일 메타데이터 기록 방식 v2를 사용합니다. 원관찰 스키마1, v4 판정·점수 바닥·정규화·루브릭·생성 한도는 바꾸지 않았습니다. 각 평가자는 자기 새 세션이 종료되기 전에 원관찰과 호환 출력을 기록합니다. [생성 전 전체 고정](planning/candidate-j-pre-generation-freeze.json) · [기록 방식 고정](planning/critic-recording-helper-freeze.json) · [메타데이터 검증](method-recording-v2/verification.json).

모든 제작자가 선택을 닫은 뒤 최초 전체 세 평가를 실행합니다. 완전히 같은 이미지·평가 맥락일 때만 불리한 기록도 포함한 최초 세 평가 전체를 재사용하고, 하나라도 달라지면 전체 다섯 장을 예정된 새 세 평가가 봅니다. 평가 피드백 뒤 추가 생성·재선택을 하지 않습니다.

## initial 원점수

v4 절차 `PASS`, 출처 `PASS`, 원관찰 연결 `PASS`, 적용 세트 `FAIL`.

[원본 v4와 원점수](reviews/R10-C1/initial/summary.json)

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R10-C1-M1 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M1 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M3 | editorial | 4 | 3 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M3 | craft | 4 | 3 | 4 | 3 | 4 | 4 | 4 |
| R10-C1-M3 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M4 | editorial | 4 | 4 | 3 | 4 | 4 | 4 | 4 |
| R10-C1-M4 | craft | 4 | 4 | 3 | 4 | 4 | 4 | 4 |
| R10-C1-M4 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M5 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M5 | craft | 4 | 4 | 4 | 4 | 3 | 4 | 4 |
| R10-C1-M5 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

실제 원관찰의 다양성: editorial=4, craft=4, portfolio=4.

- [editorial 원관찰](reviews/R10-C1/initial/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R10-C1/initial/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R10-C1/initial/cli/portfolio/portfolio.observations.json)

## selected 원점수

v4 절차 `PASS`, 출처 `PASS`, 원관찰 연결 `PASS`, 적용 세트 `NA`.

[원본 v4와 원점수](reviews/R10-C1/selected/summary.json)

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R10-C1-M1 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M1 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M3 | editorial | 3 | 3 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M3 | craft | 4 | 3 | 4 | 3 | 4 | 4 | 4 |
| R10-C1-M3 | portfolio | 3 | 3 | 4 | 4 | 4 | 3 | 4 |
| R10-C1-M4 | editorial | 4 | 4 | None | 4 | 4 | 4 | 4 |
| R10-C1-M4 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M4 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M5 | editorial | 4 | 4 | None | 4 | 4 | 4 | 4 |
| R10-C1-M5 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R10-C1-M5 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

실제 원관찰의 다양성: editorial=4, craft=4, portfolio=4.

- [editorial 원관찰](reviews/R10-C1/selected/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R10-C1/selected/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R10-C1/selected/cli/portfolio/portfolio.observations.json)

## 확인 범위

- One seen-development landscape request after whole R9 closure; not an unseen holdout or future guarantee.
- J generic runtime guidance and new case-specific planning differ from I; no isolated causal or statistical success-rate claim.
- Same prospective three-field recording instrumentation in both phases; score gates and normalization unchanged.
- Fresh sessions are trace-backed; semantic image viewing remains an attestation.
- No client assets; preservation and one-image editing remain untested by this case.

