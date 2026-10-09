# R7-B07 selected — editorial

밝은 생활 도구의 관계는 세 장 모두 충분한 크기로 보인다. M1은 하나의 문에서 사용 관계를 보여 주고, M2는 손 동작을 직접 설명하며, M3는 접촉 표면을 확대한다. 그러나 M1은 날짜의 대시 주변 공백 때문에 정확 문구 조건에 실패하고, M2는 열쇠의 마모를 보여 주지 못해 요청의 핵심 조건과 두 점수가 낮다. 이 판단은 각 결함을 그대로 보존하며 평균으로 상쇄하지 않는다.

| 멤버 / stage | text | style | ratio | no_type_only | substantive_visual | content_form | hierarchy | typography | space | image_material | emotion_control | ai_slop |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| R7-B07-M1 / repair-2 | FAIL | FAIL | PASS | PASS | PASS | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R7-B07-M2 / repair-2 | PASS | FAIL | PASS | PASS | PASS | 3 | 4 | 4 | 4 | 3 | 4 | 4 |
| R7-B07-M3 / repair-1 | PASS | PASS | PASS | PASS | PASS | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

평가자는 editorial 한 명이다. case_id=R7-B07, wave=selected, session_id=null. 점수는 1–5 rubric anchors에 따라 각 차원을 독립적으로 판단했다. 원본 크기는 세 장 모두 실제 1024×1536이며 수학적으로 정확한 세로 2:3이다. 사전 선언된 nearest-integer-single-edge 정책을 확인했으나 이번 원본에는 반올림 예외가 필요하지 않다.

## 실제 확인 절차

Read only the explicitly authorized pinned inputs and verified their byte counts/SHA-256 values. Read the three pinned native-evidence manifests without following their embedded source, call-input, pre-call or final paths. The packet declares source_assets=[] and protected_layouts=[]. Used functions.exec to call tools.view_image with detail="original" and emit each returned image with image(...,"original"), sequentially in packet order: M1 native/usage720/thumbnail320, then M2 native/usage720/thumbnail320, then M3 native/usage720/thumbnail320. All nine exact poster views were visually inspected before the first transcription judgment, image score or diversity score. After those nine views and an initial M1 date transcription, made one additional exact M1 native revisit for the date-spacing ambiguity; both readings are retained in that transcription. viewed_count counts the nine required views, with the additional revisit recorded separately. No OCR, edited/cropped views, generation, peer review, spawn, fork or resume was used. session_id is null; runner provenance is not claimed from within this review.

source_assets_viewed=[]; protected_layouts_read=[]: 패킷에 원본 자료와 보호 레이아웃이 없다. 아래 순서는 첫 판독과 점수 이전에 완료한 필수 9개 뷰이며, M1 날짜 재확인은 별도 기록이다.

| 순서 | image_id | view | pinned path | SHA-256 |
|---:|---|---|---|---|
| 1 | R7-B07-M1 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/repair-2/original.png | 77049628becdf8f5fd1ac2cd2c2f1a418f6074a3370bf675c51a7e3e78a160c0 |
| 2 | R7-B07-M1 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/repair-2/usage-720.png | a972dcce287dc8cd69e6a94c0a28413aec1d795727ae12f26a033feb30eb32bb |
| 3 | R7-B07-M1 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/repair-2/thumbnail-320.png | cc7149d3b44e9766dc0db467e6a768ac5b7927cdf3b75f75bda2ffe1b329341b |
| 4 | R7-B07-M2 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M2/stages/repair-2/original.png | 1c10235a2262b6beb9d86a53905a8771daa6b10cbdae91d05b23538b2b5dff05 |
| 5 | R7-B07-M2 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M2/stages/repair-2/usage-720.png | efc79c0098a12650e34f17e505c1091928a3b6e82ff694d1f17ac39fa037ba86 |
| 6 | R7-B07-M2 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M2/stages/repair-2/thumbnail-320.png | 44a7826d557b5a660bb57ba9df80fd103ad8aef22ff3c1b4cd684ee34ce66e35 |
| 7 | R7-B07-M3 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M3/stages/repair-1/original.png | 035193422841ae976515f39f5d41391f3baa98510c3486e2b6ff4b4b5e826dbe |
| 8 | R7-B07-M3 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M3/stages/repair-1/usage-720.png | b80339f1ef81134036a9bebe90fd82d8151ba43b770663719c74ebfb33e726a3 |
| 9 | R7-B07-M3 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M3/stages/repair-1/thumbnail-320.png | 29e0c1ea9ed32bf2cec0937101f00dff41da69455bd2eb4506f183d8a283b873 |

읽은 native manifests:

- R7-B07-M1: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/repair-2/manifest.json — 7d1eb95f74837937bfb559a7123b6f2b4d7fd1d2d539cd72b5d2b456aff397f5 (read=true)
- R7-B07-M2: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M2/stages/repair-2/manifest.json — e73981e6ec00a05e64715e4e55598e36021c15e87c08d403aacf06784b7b197f (read=true)
- R7-B07-M3: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M3/stages/repair-1/manifest.json — 82ade18c5ad6a090486789a97a0455ee05baded84aa8e4dd8a12b0aa1cbe8c63 (read=true)

## R7-B07-M1 — repair-2

필수 style 판정: FAIL. `checked_requirement`는 해당 image.style_requirement의 전체 문자열을 JSON에 그대로 복사했다. 그 문자열의 모든 적용 조건을 아래에서 roll up했다.

- PASS — 생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. 이 멤버는 독립된 포스터 한 장이며 전체 요청 수량 3은 set.count_fidelity에서 확인했다. 제목·부제·운영 안내가 생활사 전시로 읽히게 한다.
- PASS — 모두 세로 2:3입니다. 실제 native 1024×1536으로 정확한 세로 2:3이다.
- PASS — 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. 시각적으로 흰색·검정·중성 회색만 사용한다. 사진/그래픽은 허용된 매체다.
- PASS — 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. 레버와 열쇠가 같은 흰색 문에 크게 배치되어 실제 사용 관계가 보인다. 레버 앞면의 긁힘과 밝은 접촉 면, 열쇠 머리의 닳은 표면이 오래 쓰인 물건이라는 제목에 연결된다.
- PASS — 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. 큰 레버 앞면의 접촉/긁힘과 보이는 열쇠 머리의 사용 흔적을 제목 및 실제 사용 관계에 연결한다. 보이지 않는 열쇠 날의 마모는 추정하지 않는다.
- PASS — 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. 레버와 열쇠가 같은 흰색 문에 크게 배치되어 실제 사용 관계가 보인다. 레버 앞면의 긁힘과 밝은 접촉 면, 열쇠 머리의 닳은 표면이 오래 쓰인 물건이라는 제목에 연결된다.
- PASS — 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. 밝은 일상 하드웨어 관찰 또는 보통 손 동작으로 읽힌다. 으스스한 범죄 단서나 골동품 판매 수사·가격표가 보이지 않는다.
- FAIL — 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 다만 날짜 대시 양옆 공백으로 필수 문구 그대로 조건은 실패한다.
- FAIL — Every role is one separate flat opaque poster at its specified ratio with all supplied copy. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 다만 날짜 대시 양옆 공백으로 필수 문구 그대로 조건은 실패한다.
- FAIL — Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 다만 날짜 대시 양옆 공백으로 필수 문구 그대로 조건은 실패한다.
- PASS — A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient. 레버와 열쇠가 같은 흰색 문에 크게 배치되어 실제 사용 관계가 보인다. 레버 앞면의 긁힘과 밝은 접촉 면, 열쇠 머리의 닳은 표면이 오래 쓰인 물건이라는 제목에 연결된다.

각 차원은 다음 관찰로 평가했다.

- **content_form = 4**
  native / 오른쪽의 레버와 열쇠가 꽂힌 원형 실린더: 같은 문에 붙은 두 도구를 함께 보여 주어 열쇠와 손잡이의 실제 관계가 분명하다. 레버 앞쪽의 긁힘/밝은 닿는 면과 열쇠 머리의 표면 흔적이 기억·반복 사용이라는 내용에 구체성을 준다.
- **hierarchy = 4**
  usage720 / 왼쪽 위 제목 → 부제 → 날짜/장소 → 하단 운영정보: 굵고 큰 두 줄 제목, 작은 부제, 일반 굵기의 일정 정보 순서가 명확하다. 오른쪽 레버가 제목 옆의 시각 중심을 만들되 글자를 가리지 않는다.
  thumbnail320 / 상단 제목과 오른쪽 레버: 축소해도 제목과 레버/열쇠 두 형태의 관계가 남는다. 하단 세부 정보는 가까이 읽어야 하는 보조 단계다.
- **typography = 4**
  native / 왼쪽 제목과 하단 운영정보/URL: 한글 획이 닫히거나 다른 글자로 뭉개지지 않고, 굵기 차이가 제목과 정보를 나눈다. 제목과 안내의 soft wrap은 단어 누락이 아니다. 날짜 대시 양옆 공백은 정확 문구 비교에서 별도의 실패로 보존했다.
  usage720 / 날짜부터 URL까지 왼쪽 정보열: 실사용 크기에서 일정, 장소, 휴관, 관람료와 URL을 읽을 수 있다. 문 표면 질감 위에서도 검정 글자의 대비가 유지된다.
- **space = 4**
  native / 왼쪽 정렬 정보열과 오른쪽 하드웨어, 위·아래 문 패널: 정보열 사이의 간격이 기능별 묶음을 구분하고 손잡이·열쇠를 위한 오른쪽 영역을 확보한다. 상하의 빈 문 면은 두 물건의 설치 맥락을 유지하며 글자 주변에 숨 쉴 공간을 준다.
- **image_material = 4**
  native / 레버 앞면, 원형 받침, 열쇠 머리 및 문 도장 면: 금속의 선형 긁힘과 둥근 반사, 문 도장의 요철이 다른 재료로 구별된다. 열쇠가 실린더에 들어가고 하드웨어가 문 면에 붙는 관계가 일관되며 주요 형태가 무너지지 않는다.
- **emotion_control = 4**
  usage720 / 밝은 문 전체와 일상적 손잡이/꽂힌 열쇠: 밝은 확산광과 평범한 문 표면이 익숙한 생활 도구를 차분하게 보게 한다. 극적 어둠·위협적 그림자·판매 수사 없이 손에 익은 물건이라는 전시 정서에 맞는다.
- **ai_slop = 4**
  native / 하드웨어 윤곽과 전체 정보 영역: 레버, 실린더, 열쇠의 윤곽을 따라 읽을 수 있고 의미 없는 장식이나 가짜 식별표가 없다. 닳은 표면이 내용에 기여한다. 날짜 공백 문제는 존재하지만 임의 문구나 형태 붕괴의 반복은 보이지 않는다.

문구 판독: `nfc-ws-optical-v1`을 사전 규칙대로 적용했다. word spaces를 보존하며, text 항목의 정확한 · 및 / 주변만 광학 공백 예외를 적용했다. URL은 별도 kind=url 항목으로 비교했다. 아래 raw 블록은 첫 판독의 줄바꿈과 공백을 보존한다.

**copy[0] / text**

required: 손이 기억하는 물건

first raw_observed:

```text
손이 기억하는
물건
```

normalized_required: "손이 기억하는 물건"

normalized_observed: "손이 기억하는 물건"

equal: true

layout PASS: 왼쪽 중상단 제목을 ‘손이 기억하는’ / ‘물건’ 두 줄로 배치했다. fixed_newlines=false이므로 이 줄바꿈은 허용된다.

ambiguity: null

revisit: null

**copy[1] / text**

required: 열쇠와 손잡이의 생활사

first raw_observed:

```text
열쇠와 손잡이의 생활사
```

normalized_required: "열쇠와 손잡이의 생활사"

normalized_observed: "열쇠와 손잡이의 생활사"

equal: true

layout PASS: 제목 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[2] / text**

required: 2026.12.08–2027.02.14

first raw_observed:

```text
2026.12.08 – 2027.02.14
```

normalized_required: "2026.12.08–2027.02.14"

normalized_observed: "2026.12.08 – 2027.02.14"

equal: false

layout PASS: 왼쪽 중단 날짜 한 줄이다. 대시 양옆의 간격은 줄바꿈과 별개로 판독했다.

ambiguity: 첫 판독에서 en dash 양옆에 공백을 읽었다. 이것이 시각적으로 분리된 공백인지 대시의 단순 여유 간격인지 한 번 재확인했다.

revisit: {"view": "native", "path": "/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/repair-2/original.png", "sha256": "77049628becdf8f5fd1ac2cd2c2f1a418f6074a3370bf675c51a7e3e78a160c0", "raw_observed": "2026.12.08 – 2027.02.14", "resolution": "원본 재확인에서도 날짜의 en dash 양옆이 분리된 공백으로 읽힌다. 첫 판독을 바꾸지 않는다. 숫자와 대시 글자 자체는 보존되었고, 문제는 그 양옆의 공백이다. 지정된 정규화는 en dash 주변 공백을 제거하지 않는다.", "resolved": true, "reason": "모든 9개 뷰를 본 뒤 날짜 구분자 주변의 첫 판독 간격을 확인하기 위해 동일한 pinned native를 한 번 다시 보았다."}

**copy[3] / text**

required: 생활기억박물관 작은전시실

first raw_observed:

```text
생활기억박물관 작은전시실
```

normalized_required: "생활기억박물관 작은전시실"

normalized_observed: "생활기억박물관 작은전시실"

equal: true

layout PASS: 날짜 바로 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[4] / text**

required: 화–일 10:00–18:00 / 월요일 휴관

first raw_observed:

```text
화–일 10:00–18:00 / 월요일 휴관
```

normalized_required: "화–일 10:00–18:00/월요일 휴관"

normalized_observed: "화–일 10:00–18:00/월요일 휴관"

equal: true

layout PASS: 왼쪽 하단 운영시간 한 줄이다. 슬래시 양옆 간격은 text 항목의 허용된 광학 정규화 대상이다.

ambiguity: null

revisit: null

**copy[5] / text**

required: 관람료 무료

first raw_observed:

```text
관람료 무료
```

normalized_required: "관람료 무료"

normalized_observed: "관람료 무료"

equal: true

layout PASS: 운영시간 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[6] / url**

required: 전시 안내 example.org/hand-memory

first raw_observed:

```text
전시 안내
example.org/hand-memory
```

normalized_required: "전시 안내 example.org/hand-memory"

normalized_observed: "전시 안내 example.org/hand-memory"

equal: true

layout PASS: ‘전시 안내’와 URL이 두 줄이다. URL 자체는 끊어지지 않았다. kind=url이며 슬래시 주변을 보정하지 않았다.

ambiguity: null

revisit: null

남은 사항:

- 날짜의 대시 양옆 공백은 exact-copy gate의 실패로 남는다. 다른 문구의 soft wrapping과 구분한다.
- 열쇠 날의 상당 부분은 실린더 안에 있다. 보이는 열쇠 머리의 사용 흔적과 큰 손잡이 접촉 면을 근거로 주제를 판단했으며 숨은 날의 마모를 추정하지 않았다.

## R7-B07-M2 — repair-2

필수 style 판정: FAIL. `checked_requirement`는 해당 image.style_requirement의 전체 문자열을 JSON에 그대로 복사했다. 그 문자열의 모든 적용 조건을 아래에서 roll up했다.

- PASS — 생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. 이 멤버는 독립된 포스터 한 장이며 전체 요청 수량 3은 set.count_fidelity에서 확인했다. 제목·부제·운영 안내가 생활사 전시로 읽히게 한다.
- PASS — 모두 세로 2:3입니다. 실제 native 1024×1536으로 정확한 세로 2:3이다.
- PASS — 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. 시각적으로 흰색·검정·중성 회색만 사용한다. 사진/그래픽은 허용된 매체다.
- FAIL — 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. 문손잡이를 감싼 손과 열쇠를 잡은 손이 각각 충분한 크기로 그려져 두 물건의 사용 관계를 보여 준다. 이는 문자·작은 기호·배경 질감과 구별되는 substantive nonglyph visual이다.
- FAIL — 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. 열쇠는 매끈한 검정/흰색 윤곽과 곧은 평행선, 선명한 이빨로 표현된다. 닳은 가장자리나 반복 사용에 따른 표면 변화가 구별되지 않는다. 손잡이의 닿는 부분은 손으로 명시했지만 열쇠의 마모 연결 조건은 충족하지 못한다.
- PASS — 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. 문손잡이를 감싼 손과 열쇠를 잡은 손이 각각 충분한 크기로 그려져 두 물건의 사용 관계를 보여 준다. 이는 문자·작은 기호·배경 질감과 구별되는 substantive nonglyph visual이다.
- PASS — 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. 밝은 일상 하드웨어 관찰 또는 보통 손 동작으로 읽힌다. 으스스한 범죄 단서나 골동품 판매 수사·가격표가 보이지 않는다.
- PASS — 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 모든 필수 문구의 정규화 비교는 일치한다.
- PASS — Every role is one separate flat opaque poster at its specified ratio with all supplied copy. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 모든 필수 문구의 정규화 비교는 일치한다.
- PASS — Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 모든 필수 문구의 정규화 비교는 일치한다.
- PASS — A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient. 문손잡이를 감싼 손과 열쇠를 잡은 손이 각각 충분한 크기로 그려져 두 물건의 사용 관계를 보여 준다. 이는 문자·작은 기호·배경 질감과 구별되는 substantive nonglyph visual이다.

각 차원은 다음 관찰로 평가했다.

- **content_form = 3**
  native / 상단 손잡이 접촉과 오른쪽 하단 열쇠 사용 장면: 두 손을 통해 실제 사용 관계와 손잡이의 닿는 부분을 직접 전달한다. 그러나 열쇠의 표면과 날은 깨끗한 도식으로 남아 ‘오래 써서 닳은 열쇠’의 구체성이 빠진다. 사용법 장면은 기능하지만 요청의 시간성은 충분히 해결하지 못했다.
- **hierarchy = 4**
  usage720 / 상단 손 동작, 중앙 대형 제목, 아래 일정·운영정보: 상단 동작이 시선을 잡고 매우 큰 두 줄 제목이 전시를 식별한다. 부제·날짜·장소·운영정보가 크기와 간격에 따라 내려가는 순서이며 오른쪽 열쇠 동작이 주제의 두 번째 축이다.
  thumbnail320 / 중앙 제목과 양쪽 손 동작: 작은 크기에서도 제목과 두 동작의 실루엣이 분명하다. 제목 아래 정보는 보조 역할로 남는다.
- **typography = 4**
  native / 제목·부제와 하단 운영시간: 굵은 한글 제목과 좁은 숫자 날짜가 선명하고 글자 파손이 없다. 슬래시 뒤 줄바꿈으로 휴관 문구를 분리했으며 전체 글자·단어·구두점은 보존된다.
  usage720 / 아래 장소, 휴관, 관람료와 맨 아래 URL: 본문과 URL을 읽을 수 있고 각 행이 손 그림과 겹치지 않는다. 별도 URL 항목의 점·슬래시·하이픈은 그대로 읽힌다.
- **space = 4**
  native / 왼쪽 정보 블록과 오른쪽 문 단면/열쇠 손: 손잡이 그림을 위쪽, 열쇠 그림을 오른쪽 아래에 두어 넓은 중앙 왼쪽을 글자에 배정했다. 큰 제목 아래의 간격은 정보 묶음을 구분하고, 가장자리에서 잘린 팔은 사용 장면의 프레이밍으로 읽힌다.
- **image_material = 3**
  native / 손잡이 위의 흰 하이라이트와 하단 열쇠 날·머리: 검정 덩어리와 흰 선으로 문 하드웨어 및 손 동작을 일관되게 구축했다. 하지만 하이라이트는 매끈한 광택으로만 읽히고 열쇠에는 구별되는 마모·닳음 표현이 없다. 허용된 그래픽 매체 안에서도 요청된 사용 흔적의 처리까지는 완성되지 않았다.
- **emotion_control = 4**
  usage720 / 두 손의 보통 잡는 동작과 밝은 배경: 위협적 인물이나 극적 어둠 없이 보통 사람이 일상적으로 쓰는 동작을 보여 준다. 몸짓은 분명하고 친숙하며 소규모 생활사 전시의 접근성을 유지한다.
- **ai_slop = 4**
  native / 상단 손가락과 레버 접합부, 하단 손·열쇠·실린더: 주요 손가락과 도구의 맞물리는 지점을 따라 읽을 수 있고 선화의 검정/흰색 규칙이 일관된다. 무관한 기호·허구 라벨·반복 장식으로 빈 곳을 채우지 않았다. 마모 부족은 내용/재료 처리의 결함으로 따로 낮게 평가했다.

문구 판독: `nfc-ws-optical-v1`을 사전 규칙대로 적용했다. word spaces를 보존하며, text 항목의 정확한 · 및 / 주변만 광학 공백 예외를 적용했다. URL은 별도 kind=url 항목으로 비교했다. 아래 raw 블록은 첫 판독의 줄바꿈과 공백을 보존한다.

**copy[0] / text**

required: 손이 기억하는 물건

first raw_observed:

```text
손이 기억하는
물건
```

normalized_required: "손이 기억하는 물건"

normalized_observed: "손이 기억하는 물건"

equal: true

layout PASS: 중앙 왼쪽 제목을 ‘손이 기억하는’ / ‘물건’ 두 줄로 배치했다. 고정 줄바꿈 요청은 없다.

ambiguity: null

revisit: null

**copy[1] / text**

required: 열쇠와 손잡이의 생활사

first raw_observed:

```text
열쇠와 손잡이의 생활사
```

normalized_required: "열쇠와 손잡이의 생활사"

normalized_observed: "열쇠와 손잡이의 생활사"

equal: true

layout PASS: 제목 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[2] / text**

required: 2026.12.08–2027.02.14

first raw_observed:

```text
2026.12.08–2027.02.14
```

normalized_required: "2026.12.08–2027.02.14"

normalized_observed: "2026.12.08–2027.02.14"

equal: true

layout PASS: 부제 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[3] / text**

required: 생활기억박물관 작은전시실

first raw_observed:

```text
생활기억박물관 작은전시실
```

normalized_required: "생활기억박물관 작은전시실"

normalized_observed: "생활기억박물관 작은전시실"

equal: true

layout PASS: 날짜 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[4] / text**

required: 화–일 10:00–18:00 / 월요일 휴관

first raw_observed:

```text
화–일 10:00–18:00 /
월요일 휴관
```

normalized_required: "화–일 10:00–18:00/월요일 휴관"

normalized_observed: "화–일 10:00–18:00/월요일 휴관"

equal: true

layout PASS: 슬래시 뒤에서 ‘월요일 휴관’을 다음 줄로 넘겼다. soft wrapping은 글자 누락으로 보지 않았다.

ambiguity: null

revisit: null

**copy[5] / text**

required: 관람료 무료

first raw_observed:

```text
관람료 무료
```

normalized_required: "관람료 무료"

normalized_observed: "관람료 무료"

equal: true

layout PASS: 휴관 문구 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[6] / url**

required: 전시 안내 example.org/hand-memory

first raw_observed:

```text
전시 안내 example.org/hand-memory
```

normalized_required: "전시 안내 example.org/hand-memory"

normalized_observed: "전시 안내 example.org/hand-memory"

equal: true

layout PASS: 맨 아래 ‘전시 안내’와 URL이 같은 줄이다. URL은 그대로 연결되어 있다.

ambiguity: null

revisit: null

남은 사항:

- 선화가 사용 동작은 잘 전달하지만 열쇠의 오래 쓰인 표면이나 닳은 윤곽은 보이지 않는다. 이 결함 때문에 content_form와 image_material은 각각 3이다.

## R7-B07-M3 — repair-1

필수 style 판정: PASS. `checked_requirement`는 해당 image.style_requirement의 전체 문자열을 JSON에 그대로 복사했다. 그 문자열의 모든 적용 조건을 아래에서 roll up했다.

- PASS — 생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. 이 멤버는 독립된 포스터 한 장이며 전체 요청 수량 3은 set.count_fidelity에서 확인했다. 제목·부제·운영 안내가 생활사 전시로 읽히게 한다.
- PASS — 모두 세로 2:3입니다. 실제 native 1024×1536으로 정확한 세로 2:3이다.
- PASS — 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. 시각적으로 흰색·검정·중성 회색만 사용한다. 사진/그래픽은 허용된 매체다.
- PASS — 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. 윗사진은 손이 닿는 레버 앞면을 크게, 아랫사진은 닳은 열쇠 머리와 잠금장치의 결합을 크게 보여 준다. 중앙 제목을 사이에 두고 두 생활 도구의 접촉과 사용을 비교하게 한다.
- PASS — 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. 큰 레버 앞면의 접촉/긁힘과 보이는 열쇠 머리의 사용 흔적을 제목 및 실제 사용 관계에 연결한다. 보이지 않는 열쇠 날의 마모는 추정하지 않는다.
- PASS — 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. 윗사진은 손이 닿는 레버 앞면을 크게, 아랫사진은 닳은 열쇠 머리와 잠금장치의 결합을 크게 보여 준다. 중앙 제목을 사이에 두고 두 생활 도구의 접촉과 사용을 비교하게 한다.
- PASS — 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. 밝은 일상 하드웨어 관찰 또는 보통 손 동작으로 읽힌다. 으스스한 범죄 단서나 골동품 판매 수사·가격표가 보이지 않는다.
- PASS — 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 모든 필수 문구의 정규화 비교는 일치한다.
- PASS — Every role is one separate flat opaque poster at its specified ratio with all supplied copy. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 모든 필수 문구의 정규화 비교는 일치한다.
- PASS — Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels. 한 장의 불투명 평면 포스터이고 허구 번호·연대·새 로고·후원자·추가 라벨은 보이지 않는다. 모든 필수 문구의 정규화 비교는 일치한다.
- PASS — A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient. 윗사진은 손이 닿는 레버 앞면을 크게, 아랫사진은 닳은 열쇠 머리와 잠금장치의 결합을 크게 보여 준다. 중앙 제목을 사이에 두고 두 생활 도구의 접촉과 사용을 비교하게 한다.

각 차원은 다음 관찰로 평가했다.

- **content_form = 4**
  native / 상단의 닿는 레버 앞면과 하단 잠금장치에 꽂힌 열쇠: 위아래 확대 사진으로 손잡이 접촉 면과 열쇠 표면의 사용 흔적을 충분한 크기로 비교한다. 열쇠가 실린더에 꽂힌 상태이므로 독립적인 장식 소품을 나열한 것보다 실제 도구 관계가 분명하다.
- **hierarchy = 4**
  usage720 / 위 사진 → 중앙 제목/부제와 일정 → 아래 사진: 중앙의 가장 굵은 제목이 정보를 정리하고 위·아래 물건 사진이 내용을 감싼다. 제목, 부제, 날짜, 장소, 운영정보가 단계적으로 작아져 시선의 순서가 정리된다.
  thumbnail320 / 중앙 제목과 위·아래 사진 구획: 작은 크기에서도 제목이 한 줄로 유지되고 두 도구 형태가 즉시 구별된다. 세부 안내는 명확히 보조 단계다.
- **typography = 4**
  native / 중앙 흰 띠의 제목과 운영정보/URL: 큰 한글 제목의 획과 자간이 안정적이며 나머지 필수 문구도 읽힌다. 제목은 한 줄, 운영시간은 한 줄, 관람료와 URL은 별도 행으로 명료하게 배치되었다.
  usage720 / 중앙 띠 하단 운영시간과 안내 URL: 배경이 평평한 흰색이어서 작은 본문의 대비가 유지되고 URL의 점·슬래시·하이픈이 이어져 읽힌다. 필수 문구의 정규화 비교가 모두 일치한다.
- **space = 4**
  native / 상·하 사진과 중앙 흰 띠의 경계, 띠 안의 왼쪽 정렬: 사진 두 장의 큰 면적과 중앙의 독립된 정보 공간이 명확하게 나뉜다. 본문은 왼쪽 공통 축을 따르고 오른쪽 여유가 정보 밀도를 완화한다. 띠 하단 URL과 사진 경계 사이에도 분리가 유지된다.
- **image_material = 4**
  native / 상단 레버 곡면의 밝은 접촉 면과 하단 열쇠 머리/원형 실린더: 곡면 반사, 표면 긁힘, 실린더의 둥근 가공 면이 구별되며 큰 확대에도 접합과 열쇠 삽입 상태를 읽을 수 있다. 열쇠 머리의 긁힌 표면과 가장자리 사용 흔적이 전시 주제의 물성을 전달한다.
- **emotion_control = 4**
  usage720 / 밝은 금속 사진 두 장과 흰색 중앙 안내 띠: 평범한 하드웨어를 가까이 관찰하게 하며 익숙함과 촉각을 만든다. 범죄 장면을 암시하는 어둠·위협이나 골동품 판매 분위기 없이 차분한 박물관 안내로 읽힌다.
- **ai_slop = 4**
  native / 위 손잡이의 부착부, 아래 열쇠/실린더 윤곽과 중앙 정보 띠: 주요 물건의 구조가 이어지고 가짜 번호·의미 없는 작은 장식·미완성 문자 조각이 없다. 긁힘이 다소 고르게 분포하지만 실제 물건의 실루엣과 사용 관계를 흐릴 정도의 반복 패턴이나 형태 충돌은 보이지 않는다.

문구 판독: `nfc-ws-optical-v1`을 사전 규칙대로 적용했다. word spaces를 보존하며, text 항목의 정확한 · 및 / 주변만 광학 공백 예외를 적용했다. URL은 별도 kind=url 항목으로 비교했다. 아래 raw 블록은 첫 판독의 줄바꿈과 공백을 보존한다.

**copy[0] / text**

required: 손이 기억하는 물건

first raw_observed:

```text
손이 기억하는 물건
```

normalized_required: "손이 기억하는 물건"

normalized_observed: "손이 기억하는 물건"

equal: true

layout PASS: 흰색 중앙 띠 맨 위 제목 한 줄이다.

ambiguity: null

revisit: null

**copy[1] / text**

required: 열쇠와 손잡이의 생활사

first raw_observed:

```text
열쇠와 손잡이의 생활사
```

normalized_required: "열쇠와 손잡이의 생활사"

normalized_observed: "열쇠와 손잡이의 생활사"

equal: true

layout PASS: 제목 바로 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[2] / text**

required: 2026.12.08–2027.02.14

first raw_observed:

```text
2026.12.08–2027.02.14
```

normalized_required: "2026.12.08–2027.02.14"

normalized_observed: "2026.12.08–2027.02.14"

equal: true

layout PASS: 중앙 띠 중단 날짜 한 줄이다.

ambiguity: null

revisit: null

**copy[3] / text**

required: 생활기억박물관 작은전시실

first raw_observed:

```text
생활기억박물관 작은전시실
```

normalized_required: "생활기억박물관 작은전시실"

normalized_observed: "생활기억박물관 작은전시실"

equal: true

layout PASS: 날짜 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[4] / text**

required: 화–일 10:00–18:00 / 월요일 휴관

first raw_observed:

```text
화–일 10:00–18:00 / 월요일 휴관
```

normalized_required: "화–일 10:00–18:00/월요일 휴관"

normalized_observed: "화–일 10:00–18:00/월요일 휴관"

equal: true

layout PASS: 운영시간과 휴관 문구가 한 줄이다.

ambiguity: null

revisit: null

**copy[5] / text**

required: 관람료 무료

first raw_observed:

```text
관람료 무료
```

normalized_required: "관람료 무료"

normalized_observed: "관람료 무료"

equal: true

layout PASS: 운영시간 아래 한 줄이다.

ambiguity: null

revisit: null

**copy[6] / url**

required: 전시 안내 example.org/hand-memory

first raw_observed:

```text
전시 안내 example.org/hand-memory
```

normalized_required: "전시 안내 example.org/hand-memory"

normalized_observed: "전시 안내 example.org/hand-memory"

equal: true

layout PASS: 중앙 띠 하단 안내와 URL이 같은 줄이다. URL 자체의 공백이나 분절은 보이지 않는다.

ambiguity: null

revisit: null

남은 사항:

- 접촉 표면 확대는 효과적이지만 금속 긁힘이 비교적 고르게 분포한다. 특별히 정교한 국소 마모 분석을 보여 주는 수준의 5점은 아니다.
- 두 사진의 관계는 큰 도구 형태와 실린더에 꽂힌 열쇠로 판단했다. 같은 순간이나 정확히 같은 문을 촬영한 것이라고 추정하지 않았다.

## 세 장의 관계

members=[R7-B07-M1, R7-B07-M2, R7-B07-M3]. 요청 3장, 관찰 3장으로 count_fidelity=PASS. 서로 다른 역할과 image_id의 독립된 평면 포스터를 모두 평가했다. diversity=4: 환경 사진, 손 동작 선화, 접촉 표면 확대의 실제 차이가 있으며 단순 색상 교체는 아니다.

- R7-B07-M1 / thumbnail320 / 전체: 문짝을 채운 사진과 왼쪽 정보열: M1은 하나의 문에 손잡이와 꽂힌 열쇠를 함께 둔 환경 사진이다. M3의 분리된 확대 사진 두 장과 중앙 흰 띠보다 공간을 연속적으로 보여 주고, M2의 손 동작 그래픽과도 시선·매체가 다르다.
- R7-B07-M2 / thumbnail320 / 상단 손잡이를 쥔 손과 오른쪽 하단 열쇠를 잡은 손: M2는 손 동작을 직접 보여 주는 흑백 선화다. 손이 없는 M1/M3의 물성 관찰과 다른 사용 장면을 만들며, 오른쪽 문 단면과 큰 중앙 제목으로 독자적인 구도를 갖는다.
- R7-B07-M3 / thumbnail320 / 위 손잡이 확대 / 중앙 정보 띠 / 아래 꽂힌 열쇠 확대: M3는 촉각적 표면을 두 개의 큰 사진 구획으로 나누었다. M1의 환경 맥락과 M2의 직접적인 사용 동작에 비해 접촉 표면의 크기와 비교를 전면에 내세운다. 세 작품의 차이는 단순 색상·필터 교체에 머물지 않는다.

세트의 남은 사항:

- M1과 M3는 밝은 문, 금속 레버, 원형 실린더와 꽂힌 열쇠라는 소재를 반복한다. 차별성은 환경/동작/표면 확대 및 정보 배치에 있으며, 서로 전혀 다른 물건 관계를 제시하는 정도의 예외적 다양성은 아니다.
- 3종의 수량과 다양성은 충족하지만 M1의 날짜 공백과 M2의 마모 표현 부족은 각 이미지에 그대로 남는다.

필수 판독 9개, 이미지 3개, 독립 차원 점수 21개와 각 차원의 located evidence를 모두 보존했다. 이는 이 editorial 원시 평가의 기록이며 다른 critic의 관찰·점수·세션을 포함하지 않는다.
