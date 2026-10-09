# 스타일 우선 critic 마지막 문단의 미래용 초안

`drafts/style-priority-critic-rubric.md`를 만들었다. 동결된 `work/round22/critic_rubric.md`의 **마지막 문단 하나만** 명료화했으며, 현재 R22에 적용하거나 재채점하지 않았다. 이는 이후 한 번의 다섯 장 비교를 위한 미채택 초안이고 새 품질 게이트나 현재 작업의 차단 조건이 아니다.

## 명료화한 내용

- 각 최종 포스터에서 실제로 구현된 전체 스타일 정체성을 이미지 표현·편집, 색·대비, 글자의 목소리, 재질·마감·정서가 현재 내용과 함께 만드는 결과로 판단한다.
- 같은 좋은 레이아웃·읽기 순서·정렬·실제 카피 역할 구조를 공유해도 독립된 스타일이 될 수 있다. 같은 title/hero/footer 구성이라는 이유만으로 차이를 부정하지 않는다.
- 재료 이름이나 필터·팔레트·폰트 교체만으로 스타일 정체성을 대신하지 않는다. 동시에 다섯 고유한 요소 값·매체·레이아웃을 의무로 배정하지 않는다.
- 카피 위계와 정보 구조는 실제 공급된 역할만으로 평가한다. Title-only와 Title+body에 없는 eyebrow·Subtitle·footer·실용 정보를 요구하거나 그 부재를 감점 근거로 삼지 않는다. 새 역할·카피도 만들지 않는다. 이는 카피 역할의 범위 명료화이며 앞의 protocol을 삭제하거나 면제하는 변경은 아니다.
- 원작 레이아웃의 무비판적 복사를 보상하지 않는다는 문구와 스튜디오·Canva 참고의 역할은 유지한다. 좋은 읽기 구조를 공유하는 것과 원작을 그대로 복사하는 것을 구별했다.

## 정확한 pins와 보존 검사

| 대상 | bytes | SHA-256 |
|---|---:|---|
| Before / 동결 원문 `work/round22/critic_rubric.md` | 6580 | `d1f4544bdcb03eb1bac2d0eaeb5c84277ac7effc6e2164479be52e7be235745c` |
| Draft `drafts/style-priority-critic-rubric.md` | 7141 | `d997b1520582986724a9873dd25212eaf27fbb079aed45cb1bd57e64175acada` |
| 마지막 문단 전의 동일 prefix | 5920 | `6e673bf0fce6eb4270bfd05117d1b0635ff892ea5d93562ac5bf4712cdb0faf0` |
| Before 마지막 문단 | 660 | `ba81ea87bf0ddf83a712d28097cbcdf22e95c0dcf42fe4a403d787a17d835319` |
| Draft 마지막 문단 | 1221 | `ea1c7f1e8d328240ece8d593c82c32671fb14ff3cc25690818ff0bb04f00cc29` |

직접 byte 대조에서 마지막 문단 전 5920 bytes는 모두 같다. `diff -u`도 마지막 문단 한 줄의 교체만 보인다. 마지막 문단에 있던 다음 floor 문장은 그대로 유지했다: `Critic scores remain the same seven categories, each 1–5 with located evidence, all >=4 per critic for PASS.` 따라서 일곱 범주, 1–5 척도, 기존 floor 및 그 외 보기·정규화·필수 조건·보고 protocol의 byte-text는 바뀌지 않았다. 동결 원문도 작성 전후 byte 단위로 같다.

## 적용 상태와 제한

미래용·미채택 초안이다. 현재 R22의 rubric·critic 결과·점수·선택·보정·평가 이력은 변경하지 않았고, LIVE skill이나 기존 case·job도 바꾸지 않았다. native 호출, 새 다섯 장 계획·생성, 새 이미지 보기·재채점은 수행하지 않았다. 문구 정합성 검토이지 시각 품질의 증거가 아니다.

이번 작업의 출력은 draft 한 파일과 `history/style-priority-critic-draft/review.md`, `status.json`뿐이다.
