# 미채택 optical-body 초안의 독립 범위 검토

결론: **일반적인 최초 생성의 본문·Title 설계 명료화라는 좁은 범위를 유지한다. 채택을 막는 새 범위 확장은 발견하지 않았다.** 현재 문구는 em 수치나 영역 수용과 실제 글자 몸체의 읽기를 구별하고, 필요한 문장 면적과 Title의 강약·여백·이미지 편집을 함께 정하도록 구체화한다. 이 결론은 문서 변경 범위에 대한 판단이며, 실제 최초 이미지의 품질 향상이나 가독성을 입증하지 않는다. LIVE 채택은 수행하지 않았다.

## 비교한 자료와 실제 변경 범위

`drafts/candidate-optical-body`를 현재 `Skillsets/skills/ducttape-poster`와 직접 비교하고, `history/optical-body-draft`의 초안 기록·baseline pins 및 `history/r22-first-generation-design-review`의 방법 제안 기록을 읽었다. 새 이미지·가이드·렌더·R22 raw 결과·critic 점수는 열지 않았다.

- LIVE와 초안은 각각 12개 파일이다.
- 다른 파일은 `references/production-brief.md`와 `references/layout-guide.md` 두 개뿐이다. 나머지 10개는 LIVE와 바이트 단위로 같다.
- 현재 LIVE 12개 파일의 SHA-256과 바이트 수가 `history/optical-body-draft/current12pins.json`의 baseline과 모두 일치한다.
- helper, SKILL.md, agents metadata, renderer contract, normalization/evaluation 및 기존 수치 규칙은 이번 초안에서 바뀌지 않았다.

R22 방법 제안의 최소 조치와 실제 diff가 일치한다. 해당 제안에 있던 향후 별도 문서 저작 논의는 이번 diff에 들어오지 않았으며, native 전체 포스터 생성 방식은 유지된다. R22 기록에 실린 특정 시안의 em·표시 높이 추정은 초안의 보편적인 숫자 조건으로 복사되지 않았다.

## 요청한 범위 항목별 확인

| 항목 | 판정과 직접 근거 |
|---|---|
| 일반 최초 생성 개선 | `production-brief.md:27–29`는 현재 읽기 상황·서체의 실제 몸체·속공간·획·대비에서 문장 면적을 정하고 Title 및 이미지 관계를 함께 해결한다. 특정 R22 장면·시안·보정 결과에 한정된 처방이 아니다. |
| 실제 Title-only | `production-brief.md:13`은 Title만 있으면 그 제목으로 완결하며 빠진 역할을 만들지 않는다. `layout-guide.md:3`은 Title만의 요청에 복잡한 스케치를 의무화하지 않는다. |
| 실제 Title+body | 같은 `production-brief.md:13`은 두 실제 역할의 위계와 이어 읽기만 설계하며 eyebrow·Subtitle·footer·날짜·장소·URL을 새로 채우지 않는다. 실용 안내가 없는 Title+body는 `SKILL.md:38`, `layout-guide.md:3`의 가이드 의무에서 제외된다. |
| 스타일 우선·좋은 레이아웃 공유 | `production-brief.md:7–9`, `SKILL.md:30,42`, `layout-guide.md:5`는 스타일의 이미지·색·글자·마감·정서를 우선하고 좋은 읽기 순서·정렬·카피 형태의 공유를 허용한다. 새 body 문단은 이 조건을 뒤집지 않는다. |
| Title의 독립적인 설계 | 새 `production-brief.md:29`, `layout-guide.md:7`은 본문 증가만을 근거로 동일 배율 확대하지 말라는 조건이다. 필요한 Title 크기 조정 자체를 금지하지 않고 크기·무게·대비·여백으로 즉각적인 제목 인지를 유지한다. 기존의 사용자 지정 역할·배치 우선 조건도 유지된다. |
| 새 수치 문턱 없음 | 새 문단에 본문 px·Title/body 배율·글자 높이 하한이 없다. 기존 예시를 고정 폰트·픽셀·크기 비율·새 사용자 조건으로 바꾸지 말라는 조건이 명시돼 있다. 기존 예시·일곱 기준·점수 하한 문서는 그대로다. |
| 새 QA·보기·보정 게이트 없음 | `layout-guide.md:7`은 이미 하던 한 번의 전체 PNG 보기에서 설계 초점을 바꾼다. 새 증명표·glyph 높이 검사·추가 호출·추가 보기·평가 통과 절차를 넣지 않는다. `production-brief.md:29`는 채택한 읽기 상황을 실제 반환 결과에서 확인한 범위와 구별하고 새 보정 기준으로 삼지 않는다. 기존 검수는 유지된다. |
| 설치·환경 확장 없음 | `layout-guide.md:13,17`은 사용 가능한 글꼴·렌더러가 없으면 긍정적인 native 명세로 직접 생성하고 API·새 글꼴 설치·환경 설정을 새 기본 단계로 넣지 않는다. helper도 바뀌지 않았다. |
| 원작 재열람 의무 없음 | `SKILL.md:30`, `production-brief.md:43`, `layout-guide.md:13`의 선택적 아이디어 참고·재열람 비의무 조건이 유지된다. |
| native의 실제 폰트 적용 주장 없음 | `production-brief.md:33,37`, `layout-guide.md:11`, `layout-guide-contract.md:128–129`는 실제 폰트로 그린 가이드와 image_gen의 최종 래스터를 구별한다. “현재 서체의 실제 몸체”는 계획에서 선택하는 글자 형태의 근거이며 최종 image_gen에 폰트 파일이 적용된다는 인증이 아니다. |

## 범위 위험과 해석

새로운 차단 수준의 범위 위험은 없다. 특히 “본문 면적부터”를 없는 본문을 만들라는 요구로, “현재 서체”를 설치·글꼴 측정 의무로, “Title 유지”를 모든 스타일의 동일 위치·배율 요구로 읽을 근거가 전체 문서에는 없다. 실제 역할만 사용·가이드 조건부 사용·사용자 배치 우선·native fallback·고정 수치 금지 조건이 각각 바로 이를 제한한다.

짧은 제작 명세를 만들 때에도 이 제한 안에서 실제 역할에 적용해야 한다. “본문이 커졌다는 이유만으로”라는 조건을 생략해 Title 확대 자체를 금지하거나, 계획의 읽기 가정을 반환 결과의 검증 사실로 전달하면 초안의 뜻과 달라진다. 현재 문구는 두 경우를 구별하므로 이를 고치기 위한 새 의무·게이트를 제안하지 않는다.

## 검증 상태와 한계

조정자는 기존 `TASK/evaluation/base/.venv/bin/python -B quick_validate.py` 실행이 이미 통과했다고 전달했다. 이 독립 리뷰에서는 이를 다시 실행하거나 의존성을 설치하지 않았다. `history/optical-body-draft/status.json`의 PyYAML 미사용 가능 기록은 당시 기록으로 읽고 그대로 보존했다; 이번 리뷰가 그 과거 상태를 성공으로 바꾸지 않는다.

직접 수행한 검사는 현재 LIVE/초안 diff와 baseline hash·바이트 대조 및 지침의 문맥 검토다. 실제 이미지·광학 측정·모든 케이스의 신뢰성·원문 문자 또는 폰트 파일 적용을 검증하지 않았다. 초안은 이 기록에서 여전히 미채택이며, 다음 다섯 장의 계획·제작·평가를 시작하지 않았다.

이 리뷰의 유일한 출력은 `history/optical-body-scope-review/review.md`와 `status.json`이다. LIVE, 초안, helper, case, 현재 R22, 과거 raw 기록을 수정하지 않았다.
