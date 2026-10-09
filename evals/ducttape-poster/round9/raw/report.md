# 16:9 가로형 · 한 요청의 다섯 스타일 검증

새로운 야외 영화 행사 요청 한 건을 서로 다른 다섯 방향으로 제작했습니다. 다음 20장을 일괄 실행하지 않았으며 보정본을 새 스타일로 세지 않습니다.

[실제 선택본 갤러리](gallery.html) · [원문](planning/literal-landscape-request.txt) · [전체 종료 기록](planning/final-evidence.json) · [고정한 스킬](snapshots/candidate-i/SKILL.md)

실제 포스터 생성 시도 **15/15**. 새 제작자 5명, 실제 독립 평가 세션 6개. 동결 v4가 읽은 호환 출력의 집계: `{'records': 15, 'score_slots': 105, 'valid_scores': 104}`. 별도로 보존한 원관찰의 실제 집계: `{'records': 30, 'score_slots': 210, 'valid_scores': 209}`.

가로형은 반환된 원본의 실제 너비·높이를 평가합니다. 요청은 16:9이며 생성 전 고정한 기준은 한 변의 최근접 정수 반올림 최대0.5픽셀입니다. 반환 원본을 잘라 정확한 비율이라고 주장하지 않습니다. 사용 크기720과 축소320은 별도의 검수용 보기입니다.

| 시안 | 선택 단계 | 실제 원본 크기 | 생성 시도 |
| --- | --- | --- | ---: |
| R9-C1-M1 | repair-2 | 1672 × 941 | 3 |
| R9-C1-M2 | repair-2 | 1672 × 941 | 3 |
| R9-C1-M3 | repair-2 | 1672 × 941 | 3 |
| R9-C1-M4 | repair-2 | 1672 × 941 | 3 |
| R9-C1-M5 | repair-2 | 1672 × 941 | 3 |

| 평가 단계 | 개별 PASS / FAIL / NA | 세트 판정 |
| --- | --- | --- |
| initial | {'PASS': 0, 'FAIL': 0, 'NA': 5} | NA |
| selected | {'PASS': 0, 'FAIL': 4, 'NA': 1} | NA |

필수 조건과 일곱 품질 기준은 평가자 세 명 각각4점 이상이어야 하며, 다섯 장의 다양성도 세 명 각각4점 이상이어야 합니다. 평균으로 낮은 점수나 판정 불가를 지우지 않습니다.

개발용 세로형(R8) 종료 뒤 고정한 I 스킬의 여섯 파일을 바꾸지 않고 새 내용과 가로 비율에서 실행했습니다. 간결한 원관찰과 호환 출력 방식은 생성 전에 선언했습니다. 초기 v1에서는 packet의 파일 크기 필드 비교 오류(편집·마감 평가)와 잘못 지정한 출력 디렉터리(포트폴리오 평가)로 호환 출력이 생성되지 않았습니다. 세 평가의 실제 원관찰·점수와 오류를 그대로 보존하고 초기 전체 판정은 NA로 닫았습니다. [초기 오류와 없는 출력의 기록](planning/initial-recording-v1-finding.json).

선택본에 예정된 새 세 평가를 시작하기 전에 파일 메타데이터 기록 방식만 v2로 고쳤습니다. 점수·문자 정규화·필수 조건·v4 판정·루브릭·이미지·스킬은 바꾸지 않았습니다. 최초 세 평가를 교체하거나 종료 후 원관찰에서 호환 출력을 만들지 않았으며, 새 평가자는 자기 세션이 종료되기 전에 모든 출력을 기록했습니다. 초기와 선택 단계의 기록 방식이 달라 품질 개선의 대조 실험이라고 주장하지 않습니다. [초기 고정](planning/critic-recording-helper-freeze.json) · [선택 평가 전 별도 고정](planning/selected-recording-v2-helper-freeze.json) · [v2 메타데이터 검증](method-selected-v2/verification.json).

평가 뒤 새 생성·재선택·평가자 교체를 하지 않습니다. 초기 결과와 선택 결과의 낮은 점수, 실제 판독 및 오류는 모두 보존합니다. 전달된 기록의 내용·모든 보기 검사 여부는 의미상의 진술이며, 바이트·세션·도구 반환 경로와 실행 완료는 별도 근거로 확인합니다.

이 한 요청은 유한한 전이 관찰입니다. 향후 모든 요청의 하이엔드 품질, 제작 주체를 알아볼 수 없음, 원본 보존 또는 한 장 수정 성능을 보장하지 않습니다.

## initial 원점수

원본 v4 절차 판정 `NA`, 원본 세트 판정 `NA`, 출처 확인 `NA`, 원관찰 연결 `NA`. 최종 적용 판정 `NA`.

[실제 v4 판정과 오류 기록](reviews/R9-C1/initial/summary.json)

초기는 호환 출력이 없으므로 아래 원관찰 점수가 v4의 NA를 대체하지 않습니다. 원관찰의 실제 낮은 점수도 삭제하지 않습니다.

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R9-C1-M1 | editorial | 4 | 4 | 3 | 4 | 4 | 4 | 3 |
| R9-C1-M1 | craft | 4 | 4 | 3 | 4 | 4 | 4 | 3 |
| R9-C1-M1 | portfolio | 4 | 4 | 3 | 4 | 4 | 4 | 3 |
| R9-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M3 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M3 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M3 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M4 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M4 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M4 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M5 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M5 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M5 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

원관찰의 전체 세트 다양성: editorial=4, craft=4, portfolio=4.

- [editorial 원관찰](reviews/R9-C1/initial/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R9-C1/initial/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R9-C1/initial/cli/portfolio/portfolio.observations.json)

절차 오류 36개를 삭제하지 않고 연결된 실제 v4 기록에 유지합니다.

## selected 원점수

원본 v4 절차 판정 `PASS`, 원본 세트 판정 `NA`, 출처 확인 `PASS`, 원관찰 연결 `PASS`. 최종 적용 판정 `NA`.

[실제 v4 판정과 오류 기록](reviews/R9-C1/selected/summary.json)

아래 원관찰 점수와 호환 출력 점수의 연결은 별도 바이트·실행 감사로 확인합니다.

| 시안 | 평가자 | 내용 | 계층 | 글자 | 공간 | 이미지 | 정서 | AI 슬롭 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R9-C1-M1 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M1 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 3 | 4 | 4 |
| R9-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 3 | 4 | 4 |
| R9-C1-M3 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M3 | craft | 4 | 4 | None | 4 | 4 | 4 | 4 |
| R9-C1-M3 | portfolio | 4 | 4 | 4 | 4 | 3 | 4 | 4 |
| R9-C1-M4 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M4 | craft | 4 | 4 | 4 | 4 | 3 | 4 | 3 |
| R9-C1-M4 | portfolio | 4 | 4 | 4 | 4 | 3 | 4 | 4 |
| R9-C1-M5 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M5 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R9-C1-M5 | portfolio | 4 | 3 | 4 | 3 | 3 | 4 | 4 |

원관찰의 전체 세트 다양성: editorial=4, craft=4, portfolio=4.

- [editorial 원관찰](reviews/R9-C1/selected/cli/editorial/editorial.observations.json)
- [craft 원관찰](reviews/R9-C1/selected/cli/craft/craft.observations.json)
- [portfolio 원관찰](reviews/R9-C1/selected/cli/portfolio/portfolio.observations.json)

## 확인 범위

- One new content/landscape request after I development closed; bounded transfer observation, not a guarantee for future requests.
- All six I runtime files are unchanged from closed R8. Compact recording v1 initial failures remain NA; selected v2 prospectively fixes metadata pins only. No paired-quality, isolated causal or statistical success-rate claim.
- Initial raw scores are separately retained; they do not replace the missing initial v4 compatibility exports.
- Fresh maker/critic sessions are trace-backed; semantic viewing remains an attestation.
- No client assets; preservation and one-image editing remain untested by this case.

