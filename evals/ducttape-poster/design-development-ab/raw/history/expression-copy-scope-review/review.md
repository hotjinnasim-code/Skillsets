# expression-copy 미채택 초안의 독립 범위 검토

결론: **차단 수준의 범위 확장은 발견하지 않았다.** 변경은 최초 native 명세에서 구현할 표현 규칙을 먼저 구체화하고, 실제 카피 한 벌에 원래 어절 경계의 선택적 soft 줄바꿈을 담는 방법 및 단순 카피의 선택적 자기 저작 스케치에 한정된다. Title-only·Title+body, 스타일 우선·좋은 레이아웃 공유, AA의 광학 본문·Title 면적 설계와 native 전체 포스터 생성은 유지된다. 아래에 공백/soft 줄바꿈에 관한 낮은 수준의 문구 정리 권고 한 개를 남긴다.

초안은 미채택이다. root가 현재 다섯 역할의 완전한 종료를 확인한 뒤 채택 여부를 결정한다. 이 리뷰는 그 종료·이미지 품질·최초 생성 효과를 인증하지 않는다.

## 직접 확인한 범위

현재 LIVE AA와 `drafts/candidate-expression-copy`는 각각 12파일이다. LIVE의 12개 SHA-256·바이트 수는 `history/expression-copy-draft/current12pins.json`과 모두 같다. 차이는 정확히 `SKILL.md`와 `references/production-brief.md` 두 파일뿐이며, 나머지 10파일은 byte 단위로 동일하다. SKILL frontmatter도 같다. 저장된 `expression-copy.diff`는 현재 두 파일의 실제 통합 차이와 일치한다.

`history/expression-copy-draft`의 current12pins·status·diff·review를 읽고, 변경된 두 문서의 실제 역할·사용자 조건·본문·native 전달 문맥을 검토했다. 현재 R23 점수·이미지·critic·선택 기록은 읽지 않았다. unchanged 파일들은 hash·바이트 대조의 대상이며 이번에 모두 재열람한 것은 아니다.

주요 변경 입력의 정확한 pins는 다음과 같다. 모든 LIVE/draft 12파일 및 읽은 history 4파일의 pins는 `status.json`에 보존한다.

| 입력 | bytes | SHA-256 |
|---|---:|---|
| LIVE `SKILL.md` | 23624 | `194ef2f6b9ff344af8ce2d4d1d642d86a048d3b1ea5ed3165892b72000957023` |
| Draft `SKILL.md` | 24754 | `9e16b3a8f39fa11211eac46f410b6ac350c03bfe8034a528014776b5ca94048c` |
| LIVE `references/production-brief.md` | 18840 | `001e8b80a97a74d443018bf02d0b18a632d20f4eeec1c390af2387ba5e97def6` |
| Draft `references/production-brief.md` | 20273 | `8c8fb38b740fb0a0d9a2fc1a868336cd719a5f7f9160873e9f44ed7bfbbb01bd` |

## 범위 항목별 판단

- **Exact copy와 soft 줄바꿈:** `SKILL.md:56` 및 `production-brief.md:58`은 사용자 고정 줄바꿈이 없을 때만 원래 어절 경계의 공백을 의미 단위의 soft 줄바꿈으로 표시하게 한다. 철자·어절·숫자·기호·나머지 공백·고정 줄바꿈은 보존하고 같은 카피를 원문·JSON·반복 문장으로 중복 전달하지 않는다. 새 역할 라벨은 인쇄하지 않으며 선택한 줄 수를 사용자 조건이나 결과 검수 문턱으로 삼지 않는다. 어절 안 분절, 문자·기호 대체 또는 고정 줄바꿈 무시에 대한 허가가 아니다.
- **실제 카피 역할:** `production-brief.md:13,58`과 `SKILL.md:32`는 실제 공급 역할만 사용한다. Title-only는 제목으로 완결하고 Title+body는 그 두 역할로 완결하며, 없는 eyebrow·Subtitle·footer·날짜·장소·URL을 채우지 않는다. 새 전달 순서가 필수 다섯 블록을 만들지 않는다.
- **표현과 스타일 우선:** `SKILL.md:8,30,42`, `production-brief.md:7–9,49`의 스타일 정체성과 공유 가능한 읽기 순서·정렬·좋은 레이아웃 조건은 유지된다. 새 표현 규칙은 사진의 거리·초점·명암 또는 그림의 면·선·묘사 밀도처럼 선택한 표현이 전체 장면을 조직하게 하는 방법이다. 특정 도시 소재, 사진 금지, 고정 다섯 매체·폰트·팔레트·레이아웃 목록으로 바뀌지 않는다.
- **명세 순서와 설계 순서:** 새 세 단계는 image_gen에 전달할 최초 명세의 구성이다. 앞의 AA 광학 본문 면적 설계 문단은 바뀌지 않았다. 표현 명세를 먼저 쓴다는 것과 실제 카피 면적을 남는 공간으로 미루는 것은 같지 않으며, 새 문단도 Title·본문 면적과 이미지 경계를 함께 정하도록 한다.
- **가이드·환경:** `SKILL.md:38`, `production-brief.md:51`은 단순 카피의 새 자기 저작 스케치를 표현/명세를 구체화할 때만 선택적으로 허용한다. 명세만으로 충분하면 직접 생성한다. Title-only·실용 안내 없는 Title+body의 복잡한 가이드 의무를 추가하지 않는다. 사용 가능한 폰트·렌더러가 없으면 설치 없이 긍정적인 native 명세를 사용하며 원작 재열람·새 설치·수동 합성도 요구하지 않는다.
- **새 숫자·QA 없음:** 폰트·픽셀·Title/body 비율 하한, 추가 이미지 보기·증명표·승인·검수 게이트·점수 floor가 추가되지 않았다. 기존 helper, guide contract, design-grammar, evaluation-loop는 byte 단위로 같다. 기존 수치 예시나 기존 검수가 사라졌다는 주장도 하지 않는다.
- **Native 구조:** `SKILL.md:54`의 문구를 포함한 단일 flat native image_gen 최종 포스터가 유지된다. 새 문서 저작, 반환 래스터의 코드 편집·가리기·글자 덧씌우기 방식으로 바뀌지 않는다. `production-brief.md:33,37`은 명세나 실제 폰트 가이드가 최종 래스터에 실제 폰트 파일을 적용했다는 증거가 아님을 계속 명시한다.

## 행동 가능한 권고

**EC-01 — 낮음, 문구 명료화 권고이며 차단 조건은 아님.** `production-brief.md:35`의 기존 “원문 기호·공백을 교체하거나 … 대신” 문장과 `:58`의 새 “어절 경계의 공백을 … soft 줄바꿈으로 바꿔” 문장은 원문/검수 기준과 표시용 조판을 구별하면 양립한다. 다만 한 문단만 전달받는 제작자는 전자를 줄바꿈 자체의 금지로, 후자를 원문 저장·검수 문자열의 변경 허가로 읽을 수 있다.

채택 시 원한다면 새 soft 줄바꿈 문장 바로 뒤에 다음과 같은 설명 한 줄로 관계를 명시할 수 있다: **“원문 카피와 검수 기준은 그대로 보존하고, 이 줄바꿈은 기존 어절 경계의 공백을 시각적으로 표시하는 조판 선택이다.”** 이는 별도 원문을 native 프롬프트에 중복 넣으라는 요구가 아니다. 새 helper·증명표·자동 equality 게이트·추가 보기·재검수 단계는 제안하지 않는다. 현재 문구도 고정 줄바꿈과 나머지 literal을 보존하므로 이 권고를 품질 PASS 요건으로 삼지 않는다.

## 제한과 변경하지 않은 것

기록된 quick_validate의 PyYAML 의존성 실패는 당시 실제 상태로 읽고 보존했다. 이번 범위 검토에서는 검증기를 다시 실행하거나 skill-creator workflow를 실행할 필요가 없어 사용하지 않았고, 패키지를 설치하지 않았다. 새 렌더·native·guide·이미지 보기·critic·점수·다음 case/plan/job은 만들지 않았다.

문서와 pins의 정합성은 native 구현의 exact Unicode·soft 줄바꿈·폰트 적용·가독성·스타일 차이를 보장하지 않는다. 효과나 보편적인 품질을 판단할 시각 증거가 없다. LIVE·초안·helper·현재 라운드·기존 raw는 변경하지 않았으며, 유일한 출력은 이 `review.md`와 `status.json`이다.
