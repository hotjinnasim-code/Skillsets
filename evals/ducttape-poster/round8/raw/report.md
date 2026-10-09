# 덕테이프 포스터: 한 요청의 다섯 방향 검증

동네 수선·교환 행사 한 요청으로 서로 다른 스타일 다섯 장을 제작했다. 초기에는 **통과 2 · 미통과 3 · 판정 불가 0**, 보정 후 선택한 전체 세트는 **통과 5 · 미통과 0 · 판정 불가 0**이다. 최종 새 평가자 세 명 각각에게 모든 필수 조건과 일곱 항목이 4 이상이며, 전체 다양성도 각각 4였다. 초기 낮은 점수와 모든 미선택 보정본을 그대로 보존한다.

I는 개발 사례다. 이 결과만으로 모든 향후 요청의 품질이나 안정적인 성공률을 보증하지 않는다. 다음에는 같은 스킬을 고정하고 새 요청의 16:9 다섯 스타일을 확인한다.

## 실제로 바꾼 흐름

타이포그래피 중심의 자료 수집을 이미지 표현·행동·크롭·색·레이아웃·정보 계층·재질·정서까지 보는 전체 시각 체계 조사로 바꿨다. 공식 스튜디오 작품과 Canva 공개 행사 템플릿의 실제 픽셀을 확인해 내용별 다섯 방향을 함께 설계했다. 원작 이미지·로고·카피·특정 구도는 생성 참조나 저장소 산출물로 이식하지 않았다. 참고 출처가 AI를 사용하지 않았다고 인증하지 않는다.

[실제 레퍼런스 관찰](planning/whole-visual-reference-study.md)과 [동결 전 설계 감사](planning/i-design-audit.md)를 남겼다. 클레이·강한 보색·장난감 패키지와 반복적인 대제목·중앙 오브젝트·하단 안내의 우선순위를 함께 낮췄다. 모든 장을 차분한 종이·작은 제목으로 바꾸는 획일화도 피한다.

이번 다섯 방향은 작업대 사진의 두 행동, 평면 교환 제스처, 직물 접합의 정보 경계, 사물 배열의 하단 제목, 연속 장면의 이야기 구성이다. 매 요청에서 같은 다섯 매체를 채우는 고정 목록이 아니다.

## 실제 실행과 선택

다섯 제작자 역할은 독립된 새 CLI 세션으로 실행했다. 다른 평가자와 root를 포함한 총 4개 실행 한도 때문에 I 제작자는 최대 2개씩 실행했다. 논리적인 다섯 역할을 다섯 명 동시 실행으로 부르지 않는다. Native 호출은 14회, 반환 14회, 실패 0회이며 역할별 한도 3회·전체 15회 이내다. 전부 원본 1024×1536, 사용 보기 720×1080, 축소 213×320이다. 도구가 노출하지 않은 최대 크기를 인증하지 않는다.

M1·M2·M3·M5는 각 3회, M4는 2회 호출했다. 최종 선택은 M4 repair-1, 나머지 repair-2다. M5의 네 websocket 재연결은 동일 세션에서 성공한 완료로 회복됐으며 기록을 남겼다. 이를 native 이미지 실패나 새 제작자로 세지 않는다. 최초·최종 각 세 명, 총 6개 새 평가 세션·30개 이미지/평가자 기록·210개 원점수가 있다.

제작자의 자체 보정 뒤 root는 전체 초기·최종의 세 크기를 직접 봤다. 중앙 확인 뒤 native 추가 보정은 0회이므로 그 경로까지 실증했다고 말하지 않는다. [중앙 검수 범위](planning/central-qa-coverage-finding.json)를 구별한다.

## 관찰한 개선과 한계

초기 M2는 지원 정보가 여러 강한 구역으로 갈라졌고, M3는 수선·교환의 결합 개념에서 한 평가자에게 3점을 받았다. M4는 행사 정체성·일정·준비 정보의 분리, 사물·카피 밀도, 상투적인 하이라이트·테이프·방사선 장식으로 낮은 점수가 있었다. Portfolio의 초기 AI 슬롭 점수 3도 남겼다. 보정 후 새 평가 세 명은 전체 5장을 기준 이상으로 봤지만, 평가자도 달라져 특정 수정만의 인과 효과나 통계적인 향상률로 해석하지 않는다.

I는 H가 강요했던 원문/카피 중복 native 입력을 제거했다. 스킬과 계측 방식이 함께 달라져 H와의 차이를 스킬만의 효과로 분리하지 않는다. [호출 계측 범위](planning/harness-native-input-change.json)를 보존했다. 이 사례는 클라이언트 이미지가 없으므로 실제 제품 동일성·참조 구도 보존·한 장 수정은 검증하지 않았다.

## 연결된 증거

[다섯 장 갤러리](gallery.html) · [전체 실행 종료](planning/final-evidence.json) · [native 원본 전체 대조](planning/single-five-native-source-inventory.json) · [생성 전 고정본](planning/candidate-i-pre-generation-freeze.json) · [같은 버전으로 다음 한 요청을 검증하는 결정](planning/closed-five-next-loop-decision.json)

각 production 역할 아래 모든 최초·보정 원본, 실제 호출 인자와 caller 구간, 세 크기의 보기·자체 관찰·전후 비교·선택·runner 출처를 보존한다. 각 reviews 단계 아래 세 평가자의 최초 관찰·일곱 점수·세트 판단·새 세션과 완료 기록을 보존한다. 경로·해시는 출처 연결을 확인하며, 실제 의미적 열람·전사 순서는 평가자의 진술이라는 한계가 있다.

이 보고서는 source tree를 닫을 때 작성했다. 실제 바이트 보존 아카이브와 원래 호스트 파일을 읽지 않는 재검증은 별도 실행 결과를 확인해야 한다.

## initial raw scores

| Image | Critic | Content | Hierarchy | Type | Space | Material | Emotion | AI slop |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R8-C1-M1 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M1 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M1 | portfolio | 5 | 4 | 4 | 5 | 4 | 4 | 4 |
| R8-C1-M2 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M2 | portfolio | 4 | 3 | 4 | 3 | 4 | 4 | 4 |
| R8-C1-M3 | editorial | 3 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M3 | craft | 4 | 4 | 4 | 4 | 5 | 4 | 4 |
| R8-C1-M3 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M4 | editorial | 4 | 3 | 4 | 3 | 4 | 3 | 4 |
| R8-C1-M4 | craft | 4 | 3 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M4 | portfolio | 4 | 3 | 4 | 3 | 4 | 4 | 3 |
| R8-C1-M5 | editorial | 5 | 4 | 4 | 4 | 4 | 5 | 4 |
| R8-C1-M5 | craft | 4 | 4 | 4 | 4 | 4 | 5 | 4 |
| R8-C1-M5 | portfolio | 5 | 4 | 4 | 4 | 4 | 5 | 4 |

[Raw scores, readings, locations and provenance](reviews/R8-C1/initial/summary.json)


## selected raw scores

| Image | Critic | Content | Hierarchy | Type | Space | Material | Emotion | AI slop |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R8-C1-M1 | editorial | 5 | 4 | 4 | 4 | 4 | 5 | 4 |
| R8-C1-M1 | craft | 4 | 4 | 4 | 5 | 4 | 4 | 4 |
| R8-C1-M1 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M2 | editorial | 4 | 5 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M2 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M2 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M3 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M3 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M3 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M4 | editorial | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M4 | craft | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M4 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R8-C1-M5 | editorial | 5 | 4 | 4 | 4 | 4 | 5 | 4 |
| R8-C1-M5 | craft | 5 | 4 | 4 | 4 | 4 | 5 | 4 |
| R8-C1-M5 | portfolio | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

[Raw scores, readings, locations and provenance](reviews/R8-C1/selected/summary.json)

