# 선택적 전향 초안: nfc-ws-optical-ranges-v2

이 초안은 순수 비교 함수다. 현재 R22의 `nfc-ws-optical-v1`, 카피·원전사·원점수·FAIL/NA·선택 평가·helper는 그대로다. 새 case, packet, job, critic 또는 평가 체계를 만들지 않는다. 숫자 범위가 없는 Title-only·Title+body 제작에는 이 제안이 필요 없으며 다음 디자인 작업의 관문도 아니다.

일반 text 카피에는 기존 NFC·공백 run·soft newline·middle-dot/slash 광학 정책을 유지한다. **숫자 range의 예외는 자동 추론하지 않는다.** 해당 카피 항목에서 원문의 정확한 양끝과 동일한 U+2013을 사전에 선언하고 `fixed_spacing:false`를 명시했을 때만 바로 주변의 광학 간격을 비교용으로 제거한다. 이 false는 카피의 어절을 지우는 권한이 아니며 사용자 고정 공백·참조 배치를 덮어쓸 수 없다. `fixed_newlines:false`만으로 예외를 허용하지 않는다.

다음은 함수의 per-entry 메타데이터 예이며 제작 요청·시험 case가 아니다.

```json
{
  "text": "09:15–17:40",
  "kind": "text",
  "fixed_newlines": false,
  "fixed_spacing": false,
  "optical_numeric_ranges": [
    {"left": "09:15", "separator": "–", "right": "17:40"}
  ]
}
```

양끝은 ASCII 숫자 및 숫자 사이 점·colon으로 이루어진 **완전한 원문 token**이어야 한다. 선언된 쌍은 원문에 정확히 한 번 나타나야 하고, 단어·더 긴 수치·URL·부호에 붙은 일부 token이나 겹치는 선언은 받지 않는다. 날짜·시간의 실제 유효성이나 그 문자열이 range인지 ID인지의 의미를 함수가 판정하지 않는다. 적합한 클라이언트 의미와 고정 공백 여부를 생성 전에 선언하는 책임은 별도로 남는다. 동일한 쌍이 반복되는 카피는 이 작은 초안에서 지원하지 않는다.

선언된 범위에서만 동일한 원시 관찰의 양끝·U+2013을 재사용해 비교 문자열을 만든다. 다른 숫자·순서·점·colon·hyphen·minus·em dash·기호 누락을 바꾸거나 추정하지 않는다. 숫자 token 내부의 공백과 카피의 모든 어절 경계, 미선언 range 간격은 보존한다. URL 항목은 어떤 광학 예외도 받지 않는다. 원문과 관찰의 raw 문자열이나 metadata는 수정하지 않는다. 잘못된 선언은 비교 전에 오류로 드러나고, 관찰에 범위가 없거나 여러 번 나타나면 추측해 선택하지 않는다.

`fixed_spacing:true`는 모든 수평 공백의 종류·run·앞뒤 간격을 그대로 비교하며 middle-dot/slash의 기존 광학 예외도 적용하지 않는다. `fixed_newlines:true`는 LF를 별도로 보존한다. 공백은 고정되고 줄만 soft이면 LF 하나가 일반 간격 하나로 바뀔 수 있지만 주변 수평 공백을 합쳐 없애지 않는다. 고정된 LF를 가로질러 range의 공백을 제거하지 않는다. `fixed` 인자는 기존 summary의 layout 무시 진단에 대응하는 선택적 override일 뿐 필수 조건 비교에는 기본값을 사용해야 한다.

원전사·literal required·비교 결과·layout·ambiguity는 계속 별도 필드다. 래스터에서 native 폰트 파일·ASCII space·Unicode 코드포인트를 증명할 수 있다는 뜻이 아니다. 기호 종류가 불확실하면 기존 ambiguity/NA를 유지한다. 정규화된 동등성은 낮은 typography 점수를 올리거나 미숙한 간격을 면제하지 않는다. 숫자의 리듬·separator 판독·묶음·폰트 조화·사용 크기 가독성은 기존 미적 평가 대상이다. 일곱 점수 각 4 이상·세 평가자 다양성 각 4 이상과 모든 낮은/NA 기록을 유지한다.

## 아직 연결하지 않은 지점

현재 두 normalizer(`summarize.py`, `compact_critic_adapter.py`), 버전 선언과 rules, producer의 검사 명세, preparer의 helper/input pin, adapter의 실제 summary digest, whole-context/reuse binding, 기존 verification의 주장 범위를 함께 맞춰야 선택적 통합이 성립한다. 상세한 현재 20개 helper의 위치·핀은 [integration-map.json](integration-map.json)에 있다. 현재 packet과 old/new 결과의 reuse를 허용하도록 context를 줄이면 안 된다. 기존 v1 역사 검증을 v2 성공으로 재표기하지 않는다.

이 초안은 그 파일들을 수정하지 않았다. 숫자 범위 없이 기존 v1로 디자인 작업을 이어 가는 선택도 그대로 가능하다. 통합·채택·새 평가 여부는 R22 원기록을 닫은 뒤 별도로 검토할 일이며, 이 초안이 추가 다섯 장이나 평가 반복을 요구하지 않는다.
