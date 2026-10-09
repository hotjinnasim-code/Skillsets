# R7-B07 · initial · editorial

실제 고정 입력에 대한 독립 시각 평가. `session_id: null`이며 런너의 세션 식별을 대신 주장하지 않는다. 이 보고서는 이 critic 한 명의 관찰이며 다른 critic의 결과나 최종 합산 판정을 포함하지 않는다.

## 관찰 절차

Fresh independent review in this conversation; no spawning, forking, resuming, peer review or author-intent lookup. Read and hash-verified the explicitly pinned packet, case, rules, rubric, ratio policy and three native manifests. Packet source_assets and protected_layouts are both empty. Checked all nine PNG hashes, byte lengths and IHDR dimensions. Then called tools.view_image with detail="original" via functions.exec and emitted its returned image_url for actual visual inspection, once per view in nine successive calls: M1 native, usage720, thumbnail320; M2 native, usage720, thumbnail320; M3 native, usage720, thumbnail320. All nine images were visibly returned and inspected before the first transcription judgment, any image score or set-diversity score. No OCR, crops, edits or ambiguity revisits were used. Judgments use only visible supplied pixels. Session identity is left null for runner binding; no tool-event serialization or trace ID is asserted.

제공된 source_assets 및 protected_layouts는 모두 빈 배열이다. 세 원본 manifest를 읽었고, 고정 입력과 9개 PNG의 해시/바이트 크기 및 실제 PNG 크기를 확인했다. 추가 경로를 따라가지 않았다. 실제 본 첫 9개 뷰의 순서는 다음과 같다.

| 순서 | 이미지 | 뷰 | 실제 크기 | 경로 | SHA-256 |
|---:|---|---|---|---|---|
| 1 | R7-B07-M1 | native | 1024×1536 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/initial/original.png` | `ff929dbc8f73c98412dac7db0deea1b1e7bbb168f4e2846e84d71cb4bfc98cd6` |
| 2 | R7-B07-M1 | usage720 | 720×1080 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/initial/usage-720.png` | `0856668907331796c9cc6bd3b17fe713336a7bec48f58946b253bd3689756349` |
| 3 | R7-B07-M1 | thumbnail320 | 213×320 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M1/stages/initial/thumbnail-320.png` | `68c5815dc6ddae5dc196dac6bb9175e1cee9c071500ee34a15a94493a45cd041` |
| 4 | R7-B07-M2 | native | 1024×1536 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M2/stages/initial/original.png` | `06c899df1fb3b6547da43a9e24ad5cce58e6127d754a81e2dd21a626672dcc08` |
| 5 | R7-B07-M2 | usage720 | 720×1080 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M2/stages/initial/usage-720.png` | `57b3f9d95e0403a05716cce39a1675ddaa668e36682720e9bed1b12552370814` |
| 6 | R7-B07-M2 | thumbnail320 | 213×320 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M2/stages/initial/thumbnail-320.png` | `6dc236ace0bdbb6faa4ef53e9a5b217e7b38c6d997f4d6e9b2d9648001c42add` |
| 7 | R7-B07-M3 | native | 1024×1536 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M3/stages/initial/original.png` | `69bdbb8945091475211b81a10589f5a357620191ddd4938296bb816bb3bdb376` |
| 8 | R7-B07-M3 | usage720 | 720×1080 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M3/stages/initial/usage-720.png` | `53f0a5fa35af435793236bb2c9b0300762623cf62948797faea4bd8f09443822` |
| 9 | R7-B07-M3 | thumbnail320 | 213×320 | `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B07-M3/stages/initial/thumbnail-320.png` | `73f9290b32fa4dacd249fe02fea00d1e3ccf9ac5ac5a4cfc2b85e3acbb39739c` |

모든 뷰를 본 뒤에 첫 전사 판단과 점수를 기록했다. 재방문은 없으며, 애매한 글리프를 추측해 보충하지 않았다.

## 전사 비교 원칙

`nfc-ws-optical-v1`을 적용했다. NFC와 공백 연속 축약을 적용하며 소프트 줄바꿈은 공백으로 비교한다. text 항목의 정확한 `·`와 `/` 주변에만 optical-space 예외가 적용된다. 다른 구두점은 치환하지 않는다. URL은 별도의 `kind: url` 항목으로, 슬래시·점·단어 간격을 보호했다. 운영시간의 `/` 주변 공백 제거는 text 항목의 사전 선언된 예외이며, 주소 수정이 아니다. 아래 raw JSON 문자열의 `\n`은 실제 관찰한 줄바꿈이다.

## R7-B07-M1

`role=R7-B07-M1`, `stage=initial`, `case_id=R7-B07`, `profile=editorial`.

필수 text/style/ratio/no_type_only/substantive_visual: 모두 PASS. 원본은 실제 1024×1536, 요청은 2:3이며 수학적으로 정확하다. nearest-integer-single-edge 정책을 확인했으나 반올림 예외를 사용하지 않았다.

검사한 style_requirement를 정확히 보존한다:

```text
생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. 모두 세로 2:3입니다. 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요.

Literal client styles:
{"mode": "explicit monochrome", "colour": "흑백만", "allowed_media": ["사진", "그래픽"]}

Literal mandatory client conditions:
생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요.
모두 세로 2:3입니다.
흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다.
오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다.
열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요.
이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요.
으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다.
아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요.
Every role is one separate flat opaque poster at its specified ratio with all supplied copy.
Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels.
A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient.
```

| 항목 | 첫 raw 관찰 (JSON 문자열) | 요구 문구 | normalized_required | normalized_observed | equal | 레이아웃 | 모호성/재방문 |
|---:|---|---|---|---|---|---|---|
| 0 (text) | `"손이 기억하는\n물건"` | `"손이 기억하는 물건"` | `"손이 기억하는 물건"` | `"손이 기억하는 물건"` | true | 실제 줄바꿈을 raw_observed의 \n으로 보존했다. fixed_newlines=false인 소프트 줄바꿈이며, 공백으로 비교한다. 글리프 누락으로 판단하지 않았다. | 없음 / 없음 |
| 1 (text) | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 2 (text) | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 3 (text) | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 4 (text) | `"화–일 10:00–18:00 / 월요일 휴관"` | `"화–일 10:00–18:00 / 월요일 휴관"` | `"화–일 10:00–18:00/월요일 휴관"` | `"화–일 10:00–18:00/월요일 휴관"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 5 (text) | `"관람료 무료"` | `"관람료 무료"` | `"관람료 무료"` | `"관람료 무료"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 6 (url) | `"전시 안내\nexample.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | true | 실제 줄바꿈을 raw_observed의 \n으로 보존했다. fixed_newlines=false인 소프트 줄바꿈이며, 공백으로 비교한다. 글리프 누락으로 판단하지 않았다. | 없음 / 없음 |

| 차원 | 점수 | 위치를 가진 관찰 |
|---|---:|---|
| content_form | 4 | **native · 상단 중앙의 손잡이와 오른쪽 아래 열쇠/실린더**: 닳고 긁힌 레버와 실제 실린더에 꽂힌 열쇠가 한 문 표면 안에 함께 보인다. 오래 만지고 사용하는 물건이라는 내용이 큰 사물 관계로 전달된다.<br>**usage720 · 레버 윗면과 열쇠 머리**: 밝아진 손 접촉 면과 열쇠 머리의 촘촘한 긁힘이 720 뷰에서도 남아 있어 전시 주제가 단순한 열쇠 아이콘보다 구체적이다. |
| hierarchy | 4 | **thumbnail320 · 전체 구도, 상단 레버–중앙 제목–하단 정보**: 큰 레버와 두 줄의 굵은 제목이 먼저 읽히며, 부제와 일정/장소, 관람 정보가 그 아래 순서로 구분된다.<br>**usage720 · 왼쪽 문구와 오른쪽 열쇠**: 열쇠가 정보 블록 옆에 자리해 텍스트를 가리지 않고 제목에서 실제 사용 장면으로 시선을 돌린다. |
| typography | 4 | **native · 제목과 하단 일곱 문구**: 한글 획이 분명하고 제목/부제/정보의 크기 차이가 명확하다. 제목과 안내 URL의 줄바꿈은 문구를 보존한다.<br>**usage720 · 날짜, 운영시간, 하단 URL**: 숫자와 구두점, 슬래시와 URL이 읽히며, 배경 문결 위에서도 검은 글자가 충분히 분리된다.<br>**thumbnail320 · 제목 및 가장 아래 URL**: 제목은 즉시 식별된다. 세부 정보는 작아지지만 줄끼리 합쳐지지 않고 정보 블록으로 유지된다; 썸네일만으로 모든 글리프를 재전사하지 않았다. |
| space | 4 | **native · 위쪽 문 패널과 중앙/아래 텍스트 영역**: 위쪽의 넓은 문 표면이 사물을 놓을 환경을 만들고, 레버 아래 왼쪽에 문구를 정렬해 오른쪽 실린더를 위한 공간을 남긴다.<br>**usage720 · 왼쪽 정보 블록과 하단 문 몰딩**: 정보 묶음 사이 간격이 구분되며 마지막 URL과 몰딩 사이에 여유가 있다. 상단 빈 문 면의 비중은 크지만 하단 정보가 잘리거나 사물과 충돌하지 않는다. |
| image_material | 4 | **native · 레버의 굽은 접촉 면, 원형 받침, 열쇠 머리**: 금속의 방향성 있는 가공선, 밝아진 접촉 면, 열쇠의 긁힘이 서로 구별된다. 레버–받침과 열쇠–키홀의 접합이 읽힌다.<br>**usage720 · 흰 문 표면과 오른쪽 문 틈**: 칠한 문결, 금속 반사와 문 틈의 그림자가 같은 장면 안에서 일관되어 물건이 배경에 붙은 생활 도구로 보인다. |
| emotion_control | 4 | **native · 밝은 문 면 위 닳은 하드웨어**: 밝은 일상적 문과 마모의 가까운 관찰이 차분한 생활사 전시 분위기를 만든다. 위협하는 인물, 어둠 속 단서나 판매 가격/품목 표시는 없다.<br>**thumbnail320 · 전체**: 짙은 글자와 밝은 문 면의 대비가 정보 전달을 담당하고, 범죄물의 긴장감을 만드는 장치가 중심이 되지 않는다. |
| ai_slop | 4 | **native · 사물 접합부와 전체 배경**: 레버가 원형 받침에 연결되고 열쇠가 키홀에 들어간다. 유물 번호, 추가 연대, 로고, 가짜 설명표나 임의 장식이 보이지 않는다.<br>**usage720 · 문구 블록 및 열쇠 주변**: 텍스트와 사물 경계가 충돌하지 않으며, 물건을 대신하는 작은 기호나 반복 장식 없이 장면이 유지된다. |

각 점수는 해당 차원의 관찰로 별도 판단했다. 4점은 해결된 전문적 실행이며, 예외적인 5점으로 주장하지 않는다. 평균으로 약한 차원을 상쇄하지 않는다.

문자만인 구성 여부와 substantive_visual의 관찰: 큰 금속 손잡이와 실제로 삽입된 긁힌 열쇠가 한 문 면에 보인다. 충분한 크기의 비문자 중심이며 마모와 사용 관계를 담당한다.

| 적용 조건 | 상태 | 관찰 |
|---|---|---|
| 생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. | PASS | native · 이 레코드는 세트의 별도 포스터 한 종이며 박물관/전시/관람 정보를 포함한다. |
| 모두 세로 2:3입니다. | PASS | native · 실제 원본 1024×1536으로 세로 2:3이다. |
| 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. | PASS | native · 전체가 검정, 흰색과 회색의 사진/텍스트이다. |
| 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. | PASS | native · 문에 설치된 닳은 레버와 삽입된 긁힌 열쇠가 크게 보인다. |
| 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. | PASS | native · 레버 접촉 면의 밝은 닳음과 열쇠 머리의 긁힘이 가까이 보인다. |
| 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. | PASS | native · 같은 문 면 안의 레버와 실제 키홀에 꽂힌 열쇠가 비문자 중심이다. |
| 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. | PASS | native · 밝은 일상적 문과 사용 흔적이 중심이며 범죄/판매 장치가 없다. |
| 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요. | PASS | native · 일곱 필수 문구가 일치하고 추가 유물 번호나 연대가 보이지 않는다. |
| Every role is one separate flat opaque poster at its specified ratio with all supplied copy. | PASS | native · 한 개의 세로 평면 포스터로 전체 문구와 이미지가 담긴다. |
| Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels. | PASS | native · 제목/문구가 보존되며 추가 로고, 후원자, 설명표가 없다. |
| A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient. | PASS | native · 레버와 열쇠/실린더가 큰 내용 기반 사물 이미지이다. |

잔여 관찰: 위쪽 문 표면의 여백 비중이 크고 디자인의 중심 어법은 굵은 산세리프와 문 하드웨어에 머문다. 읽기나 내용 연결을 막는 수준은 아니다.

## R7-B07-M2

`role=R7-B07-M2`, `stage=initial`, `case_id=R7-B07`, `profile=editorial`.

필수 text/style/ratio/no_type_only/substantive_visual: 모두 PASS. 원본은 실제 1024×1536, 요청은 2:3이며 수학적으로 정확하다. nearest-integer-single-edge 정책을 확인했으나 반올림 예외를 사용하지 않았다.

검사한 style_requirement를 정확히 보존한다:

```text
생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. 모두 세로 2:3입니다. 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요.

Literal client styles:
{"mode": "explicit monochrome", "colour": "흑백만", "allowed_media": ["사진", "그래픽"]}

Literal mandatory client conditions:
생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요.
모두 세로 2:3입니다.
흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다.
오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다.
열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요.
이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요.
으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다.
아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요.
Every role is one separate flat opaque poster at its specified ratio with all supplied copy.
Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels.
A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient.
```

| 항목 | 첫 raw 관찰 (JSON 문자열) | 요구 문구 | normalized_required | normalized_observed | equal | 레이아웃 | 모호성/재방문 |
|---:|---|---|---|---|---|---|---|
| 0 (text) | `"손이 기억하는\n물건"` | `"손이 기억하는 물건"` | `"손이 기억하는 물건"` | `"손이 기억하는 물건"` | true | 실제 줄바꿈을 raw_observed의 \n으로 보존했다. fixed_newlines=false인 소프트 줄바꿈이며, 공백으로 비교한다. 글리프 누락으로 판단하지 않았다. | 없음 / 없음 |
| 1 (text) | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 2 (text) | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 3 (text) | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 4 (text) | `"화–일 10:00–18:00 /\n월요일 휴관"` | `"화–일 10:00–18:00 / 월요일 휴관"` | `"화–일 10:00–18:00/월요일 휴관"` | `"화–일 10:00–18:00/월요일 휴관"` | true | 실제 줄바꿈을 raw_observed의 \n으로 보존했다. fixed_newlines=false인 소프트 줄바꿈이며, 공백으로 비교한다. 글리프 누락으로 판단하지 않았다. | 없음 / 없음 |
| 5 (text) | `"관람료 무료"` | `"관람료 무료"` | `"관람료 무료"` | `"관람료 무료"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 6 (url) | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |

| 차원 | 점수 | 위치를 가진 관찰 |
|---|---:|---|
| content_form | 4 | **native · 상단의 손/손잡이와 오른쪽 아래의 손/열쇠**: 한 손은 레버를 쥐고 다른 손은 실린더에 꽂힌 열쇠를 잡는다. 만지는 행위가 크게 그려져 손에 익는 물건이라는 내용을 직접 연결한다.<br>**usage720 · 손가락 아래 레버의 밝은 닳은 띠와 열쇠 테두리**: 손이 닿는 레버 위치에 밝은 마모 띠가 있고 열쇠 머리 테두리는 닳은 선으로 표시되어, 사용과 마모를 같이 읽을 수 있다. |
| hierarchy | 4 | **thumbnail320 · 상단 행위 그림–중앙 두 줄 제목–하단 관람 정보**: 손잡이를 쥐는 그림과 굵은 제목이 먼저 보이고 부제, 날짜/장소, 운영 정보로 읽기가 내려간다.<br>**usage720 · 왼쪽 정보와 오른쪽 아래 열쇠를 잡는 손**: 열쇠 장면은 정보 옆에 남아 제목 이후에도 사용 행위가 계속 보인다. 오른쪽 문 가장자리가 두 그림의 공통 설치 환경을 드러낸다. |
| typography | 4 | **native · 제목/부제와 하단 일정**: 굵은 한글 제목과 부제, 폭이 좁은 날짜 숫자, 더 작은 운영 정보가 각각 읽히며 필수 글리프가 보존된다.<br>**usage720 · 운영시간 두 줄 및 가장 아래 URL**: 슬래시 뒤 월요일 휴관이 다음 줄로 내려가지만 문구는 이어진다. URL은 한 줄로 연속되어 슬래시/하이픈을 포함한 주소를 읽을 수 있다.<br>**thumbnail320 · 전체 텍스트**: 굵은 제목과 부제가 강하게 남고 날짜가 분리된다. 전체가 무거운 검은 글자에 의존해 섬세한 대비는 제한되지만 읽기 단계가 무너지지는 않는다. |
| space | 4 | **native · 왼쪽 텍스트 축과 오른쪽 문 가장자리/손**: 왼쪽 제목과 정보의 시작점을 대체로 맞추고 오른쪽에 문과 열쇠를 쥔 손을 배치해 긴 URL 아래까지 충돌 없이 담았다.<br>**usage720 · 날짜/장소 묶음과 운영 정보 사이**: 정보 묶음 사이 흰 간격이 유지되어 큰 검정 그림과 굵은 문구가 한 덩어리로 뭉치지 않는다. |
| image_material | 4 | **native · 상단 손의 손가락, 레버 곡면과 마모 띠**: 윤곽 위주의 손과 검은 금속에 남긴 밝은 마모가 일관된 흑백 그래픽 어법으로 구성된다. 손가락이 레버를 감싸는 동작이 식별된다.<br>**usage720 · 아래쪽 열쇠/키홀과 오른쪽 문 측면**: 열쇠 날이 키홀에 들어가고 머리를 손가락이 잡는 관계가 읽힌다. 금속 테두리와 문 측면이 설치 상태를 받쳐 준다; 마모의 세밀한 질감은 사진 두 종보다 단순하다. |
| emotion_control | 4 | **native · 두 손의 일상적 사용 동작과 밝은 바탕**: 강한 검정 그래픽이지만 장면은 손잡이를 쥐고 열쇠를 다루는 생활 동작이다. 위협, 범죄 단서나 골동품 판매 장치 없이 박물관 관찰 주제로 읽힌다.<br>**thumbnail320 · 전체**: 상단의 손 동작과 전시 제목이 함께 남아, 검정의 비중이 곧바로 으스스한 장르로 바뀌지는 않는다. |
| ai_slop | 4 | **native · 손–레버, 손–열쇠의 경계**: 손과 물건의 윤곽이 구분되며 두 동작의 접촉 위치가 읽힌다. 무의미한 장식, 추가 번호/연대/브랜드나 허구 설명표가 보이지 않는다.<br>**usage720 · 텍스트 옆 열쇠와 하단 URL**: 삽입된 열쇠 장면과 글자가 겹치지 않고 URL이 이어진다. 그래픽의 밝은 마모 띠는 실제 손잡이 표면 안에 머문다. |

각 점수는 해당 차원의 관찰로 별도 판단했다. 4점은 해결된 전문적 실행이며, 예외적인 5점으로 주장하지 않는다. 평균으로 약한 차원을 상쇄하지 않는다.

문자만인 구성 여부와 substantive_visual의 관찰: 두 손/물건의 사용 동작이 큰 그림으로 보인다. 레버의 닳은 접촉 면과 열쇠/키홀 접합을 텍스트와 독립적으로 전달한다.

| 적용 조건 | 상태 | 관찰 |
|---|---|---|
| 생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. | PASS | native · 이 레코드는 세트의 별도 포스터 한 종이며 박물관/전시/관람 정보를 포함한다. |
| 모두 세로 2:3입니다. | PASS | native · 실제 원본 1024×1536으로 세로 2:3이다. |
| 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. | PASS | native · 검정/흰색과 회색으로 구성된 손/물건 그래픽과 문자이다. |
| 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. | PASS | native · 손이 레버와 삽입된 열쇠를 잡는 일상 사용 동작이다. |
| 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. | PASS | native · 레버의 손 닿는 면에 밝은 마모 띠가 있고 열쇠 테두리에 닳은 선이 있다. |
| 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. | PASS | native · 손잡이를 쥐는 손과 키홀의 열쇠를 잡는 손이 큰 비문자 중심이다. |
| 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. | PASS | native · 강한 검정 대비에도 생활 동작과 전시 정보가 중심이고 범죄/판매 요소가 없다. |
| 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요. | PASS | native · 일곱 필수 문구가 일치하고 추가 유물 번호나 연대가 보이지 않는다. |
| Every role is one separate flat opaque poster at its specified ratio with all supplied copy. | PASS | native · 한 개의 세로 평면 포스터로 전체 문구와 그림이 담긴다. |
| Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels. | PASS | native · 제목/문구가 보존되며 추가 로고, 후원자, 설명표가 없다. |
| A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient. | PASS | native · 두 손과 하드웨어가 큰 내용 기반 사용 장면이다. |

잔여 관찰: 대부분의 지지 문구도 굵은 검정이며 날짜는 폭이 좁은 숫자체여서 세밀한 타이포그래피 대비는 제한된다. 마모 질감은 사진 두 종보다 간략하다.

## R7-B07-M3

`role=R7-B07-M3`, `stage=initial`, `case_id=R7-B07`, `profile=editorial`.

필수 text/style/ratio/no_type_only/substantive_visual: 모두 PASS. 원본은 실제 1024×1536, 요청은 2:3이며 수학적으로 정확하다. nearest-integer-single-edge 정책을 확인했으나 반올림 예외를 사용하지 않았다.

검사한 style_requirement를 정확히 보존한다:

```text
생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. 모두 세로 2:3입니다. 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요.

Literal client styles:
{"mode": "explicit monochrome", "colour": "흑백만", "allowed_media": ["사진", "그래픽"]}

Literal mandatory client conditions:
생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요.
모두 세로 2:3입니다.
흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다.
오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다.
열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요.
이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요.
으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다.
아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요.
Every role is one separate flat opaque poster at its specified ratio with all supplied copy.
Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels.
A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient.
```

| 항목 | 첫 raw 관찰 (JSON 문자열) | 요구 문구 | normalized_required | normalized_observed | equal | 레이아웃 | 모호성/재방문 |
|---:|---|---|---|---|---|---|---|
| 0 (text) | `"손이 기억하는 물건"` | `"손이 기억하는 물건"` | `"손이 기억하는 물건"` | `"손이 기억하는 물건"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 1 (text) | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | `"열쇠와 손잡이의 생활사"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 2 (text) | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | `"2026.12.08–2027.02.14"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 3 (text) | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | `"생활기억박물관 작은전시실"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 4 (text) | `"화–일 10:00–18:00 / 월요일 휴관"` | `"화–일 10:00–18:00 / 월요일 휴관"` | `"화–일 10:00–18:00/월요일 휴관"` | `"화–일 10:00–18:00/월요일 휴관"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 5 (text) | `"관람료 무료"` | `"관람료 무료"` | `"관람료 무료"` | `"관람료 무료"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |
| 6 (url) | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | `"전시 안내 example.org/hand-memory"` | true | 한 줄로 표시된다. fixed_newlines=false이며 요구된 고정 줄바꿈은 없다. | 없음 / 없음 |

| 차원 | 점수 | 위치를 가진 관찰 |
|---|---:|---|
| content_form | 4 | **native · 상단 레버 접사와 하단 꽂힌 열쇠 접사**: 크게 확대한 접촉 면과 긁힌 열쇠 머리, 키홀에 들어간 날이 생활 도구의 사용 흔적을 구체적으로 보여 준다.<br>**usage720 · 중앙 정보 띠의 위/아래 이미지**: 두 이미지가 손잡이와 열쇠/실린더를 짝으로 제시한다. 하나의 연속 장면으로 보이는 M1이나 손의 동작을 보여 주는 M2보다 두 물건의 통합 관계는 약하지만, 실제 설치와 사용 관계는 사물 이미지로 읽힌다. |
| hierarchy | 4 | **thumbnail320 · 사진–제목/정보 흰 띠–사진**: 위 손잡이와 중앙 한 줄 제목이 먼저 읽히고 아래 열쇠가 두 번째 사물 중심을 만든다. 정보가 한 흰 띠에 모여 찾기 쉽다.<br>**usage720 · 중앙 띠의 제목, 부제, 일정/장소, 운영정보, URL**: 제목이 가장 크고 부제와 날짜가 그 다음, 장소와 운영 정보/URL이 뒤따르는 순서가 명확하다. |
| typography | 4 | **native · 중앙 흰 띠의 모든 문구**: 한 줄 제목, 한 줄 부제, 날짜와 정보가 높은 대비로 정돈되어 있으며 필수 문구의 글리프와 구두점이 읽힌다.<br>**usage720 · 날짜 및 운영정보/URL**: 문결 위에 직접 놓지 않은 문구는 작은 크기에서도 분리되어 읽힌다. URL 전체와 슬래시는 한 줄에 보존된다.<br>**thumbnail320 · 제목/부제와 정보 묶음**: 제목과 부제가 분리되어 남고 일정/장소와 하단 정보가 각각의 블록으로 유지된다; 작은 썸네일은 원본 전사를 대체하지 않았다. |
| space | 4 | **native · 세 가로 구간과 중앙 정보 띠**: 위 손잡이 사진, 흰 정보 띠, 아래 열쇠 사진의 경계가 명확하다. 흰 띠 안에서는 일관된 왼쪽 여백으로 다양한 길이의 문구를 받는다.<br>**usage720 · 중앙 띠 아래 URL과 아래 사진 시작점**: 마지막 주소와 사진 경계 사이 여유가 있고 금속 사물은 각 사진 구간 안에서 충분히 큰 면적을 차지한다. |
| image_material | 4 | **native · 상단 레버 앞면과 하단 열쇠 머리/날**: 레버의 벗겨진 접촉 면, 어두운 주변 금속, 열쇠 머리의 긁힘과 두께가 구분된다. 열쇠 날이 실린더에 삽입된 연결도 분명하다.<br>**usage720 · 두 사진의 금속과 문 면**: 두 구간 모두 부드러운 문 면과 방향성 있는 금속 반사가 자연스럽게 이어지는 재료 어법을 갖고 있다. 두 컷의 실제 동일한 문 여부는 단정하지 않았다. |
| emotion_control | 4 | **native · 밝은 정보 띠와 중립적인 금속 접사**: 사용 흔적을 자세히 보는 담담한 전시 분위기다. 위협을 만드는 그림자 연출이나 판매용 가격/골동품 설명이 보이지 않는다.<br>**thumbnail320 · 전체**: 강한 확대가 마모와 물건 형태를 강조하며, 감정 효과는 차분한 관찰에 머문다. |
| ai_slop | 4 | **native · 레버 받침과 열쇠/키홀 접합, 중앙 문구**: 하드웨어 접합과 삽입 방향이 읽히고 금속 디테일이 사물 표면 안에 있다. 추가 유물 번호, 연대, 로고나 임의 장식이 없다.<br>**usage720 · 사진 경계 및 정보 띠**: 사진을 가르는 흰 띠는 정보 영역으로 기능하며, 문자나 사물의 잘못된 겹침 또는 의미 없는 장식 패턴이 보이지 않는다. |

각 점수는 해당 차원의 관찰로 별도 판단했다. 4점은 해결된 전문적 실행이며, 예외적인 5점으로 주장하지 않는다. 평균으로 약한 차원을 상쇄하지 않는다.

문자만인 구성 여부와 substantive_visual의 관찰: 문에 설치된 닳은 레버와 실린더에 꽂힌 긁힌 열쇠가 각각 큰 사진 구간을 차지한다. 작은 기호나 질감 배경을 넘어 사용 흔적과 실제 결합을 보여 준다.

| 적용 조건 | 상태 | 관찰 |
|---|---|---|
| 생활사 박물관의 소규모 전시 포스터 3종을 만들어 주세요. | PASS | native · 이 레코드는 세트의 별도 포스터 한 종이며 박물관/전시/관람 정보를 포함한다. |
| 모두 세로 2:3입니다. | PASS | native · 실제 원본 1024×1536으로 세로 2:3이다. |
| 흑백만 쓰되 사진과 그래픽은 사용할 수 있습니다. | PASS | native · 검정/흰색과 회색의 금속 사진 및 검정 문자/흰 띠이다. |
| 오래 쓰며 손에 익은 열쇠와 손잡이를 주제로 한 전시입니다. | PASS | native · 닳은 레버와 긁힌 열쇠가 설치된 사용 상태로 크게 보인다. |
| 열쇠의 마모와 손잡이의 닿는 부분이 주제에 연결되게 해 주세요. | PASS | native · 레버 앞면의 닳음과 열쇠 머리의 긁힘이 접사로 읽힌다. |
| 이 물건의 실제 관계가 충분한 크기의 비문자 시각 중심이어야 하고, 글자와 여백이나 작은 기호만으로 끝내지 마세요. | PASS | native · 위/아래 큰 사물 사진에 문에 설치된 레버와 실제 실린더에 꽂힌 열쇠가 보인다. 두 컷이 동일한 문이라는 사실까지 추론하지 않았다. |
| 으스스한 범죄물이나 골동품 상점 광고처럼 보이지 않았으면 합니다. | PASS | native · 밝은 정보 띠와 담담한 재료 관찰이며 범죄/판매 장치가 없다. |
| 아래 문구를 모두 그대로 넣고, 없는 유물 번호나 연대는 만들지 마세요. | PASS | native · 일곱 필수 문구가 일치하고 추가 유물 번호나 연대가 보이지 않는다. |
| Every role is one separate flat opaque poster at its specified ratio with all supplied copy. | PASS | native · 한 개의 세로 평면 포스터로 전체 문구와 두 사진 구간이 담긴다. |
| Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels. | PASS | native · 제목/문구가 보존되며 추가 로고, 후원자, 설명표가 없다. |
| A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient. | PASS | native · 상단/하단 금속 사진이 충분히 큰 내용 기반 비문자 시각이다. |

잔여 관찰: 두 사진을 정보 띠가 분리해 M1의 한 장면이나 M2의 사용 동작보다 열쇠/손잡이 관계가 덜 통합된다. 동일한 문/동일한 촬영 장면 여부는 픽셀로 확인할 수 없어 주장하지 않았다.

## 세트

정확한 멤버 순서는 R7-B07-M1, R7-B07-M2, R7-B07-M3이다. 요청 3종 / 실제 관찰 3종: count_fidelity PASS. 이 보고서에는 이미지 레코드 3개, 일곱 차원 점수 21개, 최초 뷰 9개가 모두 있다.

**다양성: 3/5.** 식별 가능한 변주가 있지만 같은 하드웨어 구도와 굵은 제목 어법에 집중한다. 다양성의 4점 문턱에 도달하지 않았으며, 이미지의 높은 점수로 이를 상쇄하지 않는다.

- **R7-B07-M1 · thumbnail320 · 전체 구도**: 칠한 문 위에 제목과 정보를 직접 얹은 연속 사진 장면이다. 환경과 사물의 연결이 M3보다 통합되어 있지만 레버 위/열쇠 아래라는 사물 순서와 굵은 왼쪽 정렬 제목은 다른 두 종과 반복된다.
- **R7-B07-M2 · thumbnail320 · 상단 손/레버와 오른쪽 아래 손/열쇠**: 흑백 그림과 실제 손 동작이 사진 두 종과 구별되는 의미 있는 변화다. 다만 위쪽 레버–중앙 굵은 제목–아래쪽 삽입 열쇠라는 기본 장면과 읽기 구조는 M1과 가깝다.
- **R7-B07-M3 · thumbnail320 · 사진 두 구간 사이 흰 정보 띠**: 중앙 띠와 두 접사가 M1의 직접 겹침 배치 및 M2의 손 그림과 구분된다. 그러나 M1과 같은 종류의 금속 레버, 원형 실린더, 삽입된 열쇠를 같은 위/아래 순서로 확대해 제시하므로 별개의 시각 전제까지 넓어지지는 않는다.

세 종은 식별 가능한 매체/행위/배치 변화를 갖지만, 핵심 사물 구도와 제목 어법을 반복한다. 다양성은 기능적 변주인 3점으로 판단했으며, 흑백 팔레트의 반복 자체를 감점 근거로 삼지 않았다.

이 한 명의 editorial 평가에서 이미지별 일곱 차원과 필수 항목은 모두 문턱을 충족하지만, 세트 다양성은 미달이다. 결과는 이번 고정된 3종에만 해당한다.
