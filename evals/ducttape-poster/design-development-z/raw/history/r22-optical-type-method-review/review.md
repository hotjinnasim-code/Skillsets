# R22 광학 범위 간격의 방법·설계 검토

**R22에는 기존 엄격한 v1을 그대로 적용해야 한다.** 이미 본 결과의 공백 예외를 바꿔 원 FAIL이나 낮은 typography 점수를 구제할 수 없다. 다만 새 일반 요청에서는 사용자가 공백을 고정하지 않은 숫자 날짜·시간 범위의 광학 간격을 사전에 좁게 구분하는 명세가 타당하다. 이는 현재 원판정의 오류를 선언하거나 수치 기준을 낮추는 제안이 아니다.

## 실제 확인한 사실

M5의 기존 own guide spec·manifest에는 `2027.06.12–06.13`, `토·일 11:00–19:00`가 그대로 있으며, 두 U+2013의 바로 앞뒤에 ASCII U+0020은 없다. 시간 줄에는 요일과 시간 사이의 의미 있는 한 공백만 존재한다. manifest는 두 줄을 AppleMyungjo Regular, 34px, BASIC engine으로 기록하고 전체 advance를 각각 340px·350px로 기록한다. PNG 해시는 manifest 출력 핀과 같다. 이미 렌더된 이 PNG를 original detail로 실제 열람하니 대시 양쪽의 열린 잉크 간격이 보였다. 가이드를 새로 렌더하거나 자르거나 보정하지 않았다.

고정된 renderer는 line 문자열을 `font.getlength`/`getbbox`로 재고 동일한 문자열을 `draw.text`에 전달한다. 별도의 ASCII 공백 삽입이나 글자별 강제 tracking 코드는 이 경로에 없다. 따라서 이 한 가이드는 **공백 문자를 추가하지 않은 정확한 문자열도 벌어진 시각 간격을 만들 수 있다**는 반례다. OpenType는 advance width·sidebearing·outline bounds를 구별해 기록한다. 잉크의 빈 면과 인코딩된 공백이 같은 것은 아니다. [OpenType hmtx 공식 명세](https://learn.microsoft.com/en-us/typography/opentype/spec/hmtx)

이번 검토는 각 글리프의 sidebearing을 새로 측정하지 않았다. 기존 계획의 34px dash advance와 hyphen 17px 기록은 글리프 지표의 관찰이며 모든 숫자·대시 접점의 정확한 빈 면 원인까지 분해하지 않는다. native가 AppleMyungjo를 적용했는지, 어떤 코드포인트를 생성했는지, 가시 간격이 ASCII space·kerning·glyph advance 중 무엇에서 생겼는지는 native bitmap만으로 인증할 수 없다. 같은 그림에서 다른 인코딩·조판 경로도 가능하다. 기호 클래스조차 판독이 애매하면 원문을 추정해 맞추지 않고 ambiguity를 남겨야 한다.

## 현재 규칙의 범위

`nfc-ws-optical-v1`은 NFC, 공백 run collapse, 고정 newline 처리 뒤 text의 middle-dot `·`와 slash `/` 바로 주변 간격만 제거한다. URL은 보호한다. U+2013 주변은 예외가 아니다. 따라서 전사에 range gap이 공백으로 기록되면 v1 비교는 그 공백을 보존한다. 이번 관찰이 그 계산 또는 원전사를 바꾸는 권한을 주지 않는다. 평가 지침도 규칙을 생성·평가 전에 확정하고, raw·문자/어절/기호 충실도·layout·ambiguity를 분리하며, 결과를 본 뒤 바꾸지 말라고 명시한다.

현재 R22 양 단계에는 이 방법을 유지한다. 최초 all-five FAIL과 기존 원점수·낮은/NA 및 앞으로 동일 규칙으로 진행되는 선택 평가를 그대로 보존한다. 이번 검토는 native 포스터나 critic 원판정을 읽거나 다시 점수화하지 않았다. `fixed_newlines:false`는 줄바꿈 필드이며 ‘공백 고정이 없다’는 의미로 확대할 수 없다. 명시적 literal spacing·배치 보존 요청이 있으면 그대로 우선해야 한다.

## 최소한의 전향적 접근

별도 버전의 사전 명세에서 **text로 선언된 숫자 날짜·시간 range span**만 대상으로, 사용자가 literal spacing을 고정하지 않았을 때 동일한 U+2013 바로 주변의 광학 공백을 정규화할 수 있다고 정한다. 전체 대시·문장부호·공백을 지우는 전역 규칙으로 만들지 않는다. range의 숫자·점·colon·기호 종류와 순서, 숫자 토큰 내부, 요일/시간 등 어절 경계, URL, 명시적 공백·줄바꿈은 모두 보존한다. hyphen·minus·em dash·다른 lookalike로 바꾸지 않는다. 문장 속 dash·ID·수식·음수·URL까지 자동 range로 판단하지 않는다. 필요한 범위를 내용과 함께 사전에 선언하는 좁은 해석으로 충분하며 새 결과를 통과시키기 위한 사례별 예외는 만들지 않는다.

원시 전사와 layout 관찰은 유지하고 정규화된 동등성만 별도로 계산한다. 보기만으로 코드포인트가 확정되지 않으면 기호 클래스 관찰과 불확실성을 명시한다. 형식상 동등해도 대시가 약하거나 수치가 흩어져 보이는 문제, 나쁜 숫자 리듬·폰트 조화·사용 크기 판독은 typography/위계의 독립 평가 대상이다. 7항목 각 4 이상·세 다양성 각 4 이상은 그대로이며, 이런 명세가 typography 3을 4로 올리거나 품질 PASS를 보장하지 않는다.

제작 지침은 원문 범위를 유지하면서 선택한 숫자 골격·separator의 길이/위치·광학 간격으로 양끝이 한 범위로 자연스럽게 읽히게 하는 긍정적 조판 설명이면 충분하다. 한 폰트·좌표·px floor·overlay를 강요하거나 native 코드포인트/폰트 파일 적용을 인증하지 않는다.

이번 쓰기는 이 review.md와 [status.json](status.json)뿐이다. code·규칙·case·guide·native·critic·원점수·기존 raw를 변경하지 않았다. 외부 열람은 위 OpenType 공식 텍스트 한 페이지뿐이며 source 작품 이미지를 새로 열지 않았다. 제안은 앞으로의 방법을 설명할 뿐 현재 적용·새 테스트·재평가를 요청하거나 수행하지 않는다.
