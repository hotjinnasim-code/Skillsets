# Independent portfolio review

review-protocol.md와 action-first.json만 읽고 X770/X943의 실제 usage720를 view_image로 먼저 열었다. portfolio-action-first.json을 저장하고 같은 저장 파일을 읽어 확인한 다음 packet.json을 처음 열었다. 초기 기록은 수정하지 않았다.

27개 서로 다른 이미지 경로를 실제 view_image로 보았다. observed 배열의 47개 항목은 이미지에서 수동으로 판독·전사했다. OCR을 사용하거나 required를 observed로 복제하지 않았다. 디자인 줄바꿈은 어절 순서를 유지한 한 줄 문자열로 기록했다.

동일한 7개 1–5 정수 앵커를 적용했다. 점수를 합산해 낮은 항목을 덮지 않았으며 제작 주체, 실제 접힘/용량, 실물 인쇄 적합성을 픽셀로 보증하지 않는다.

All nine mandatory gates pass: exact visible copy, 720-width legibility, required formats and count, and visible product attributes. All 47 manually transcribed items match. Actual native ratios are checked within 1%. Physical capacity/mechanics/material composition and authorship are outside pixel review.

The weakest gate-relevant quality observations remain X800 image_material=3 / ai_slop=3, and X943 space=3. No score totals or consensus adjustment were used.

| Image | Content/form | Hierarchy | Type | Space | Image/material | Emotion/control | AI-slop |
| --- | --- | --- | --- | --- | --- | --- | --- |
| X800 | 4 | 4 | 4 | 4 | 3 | 4 | 3 |
| X738 | 4 | 5 | 4 | 4 | 4 | 4 | 4 |
| X847 | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| X641 | 5 | 4 | 5 | 5 | 5 | 5 | 5 |
| X300 | 5 | 5 | 4 | 5 | 4 | 5 | 4 |
| X943 | 4 | 5 | 4 | 3 | 4 | 4 | 4 |
| X762 | 5 | 4 | 4 | 4 | 5 | 5 | 5 |
| X770 | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| X340 | 4 | 4 | 5 | 4 | 4 | 5 | 4 |

## X800

Mandatory PASS. Native 1122×1402, target 4:5, relative ratio error 0.03566%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: FOLN | Observed: FOLN | Equal: True
- Required: Fold Cup | Observed: Fold Cup | Equal: True
- Required: 가볍게 접고, 다시 펼치다 | Observed: 가볍게 접고, 다시 펼치다 | Equal: True
- Required: 350 mL · 접이식 실리콘 컵 | Observed: 350 mL · 접이식 실리콘 컵 | Equal: True
- Required: 2026.12.01 RELEASE | Observed: 2026.12.01 RELEASE | Equal: True
- Required: 온라인 사전 주문 11.10–11.30 | Observed: 온라인 사전 주문 11.10–11.30 | Equal: True
- Required: foln.example/store | Observed: foln.example/store | Equal: True

Located evidence:
- content_form (4): 왼쪽의 펼친 컵과 오른쪽의 접힌 컵을 같은 바닥에 함께 보여 주어, 제목의 접고/펼치다를 실루엣 차이로 설명한다. 잎 그림자는 휴대 제품의 바깥 생활을 암시하지만 그 자체는 범용적인 생활용품 광고 어휘다.
- hierarchy (4): 320에서 먼저 두 높이가 다른 녹색 컵과 오른쪽 Fold Cup이 보이며, 720에서 바로 아래 문구와 하단 출시/주문/주소를 이어 읽을 수 있다. FOLN은 하단 작은 크기여서 브랜드보다 제품 기능을 먼저 인식한다.
- typography (4): 오른쪽 Fold Cup, 두 줄 한글 슬로건, 한 줄 용량 설명이 하나의 왼쪽 정렬 묶음을 만든다. 하단 FOLN/출시일/주문일/URL의 굵기 차이는 정보 종류를 구분하며 글자 획은 안정적이다.
- space (4): 긴 컵의 높이와 오른쪽 상단 글자 묶음이 균형을 이루고, 접힌 컵 아래 빈 바닥에 출시 정보를 놓아 물체와 문자를 분리한다. 하단 정보 블록의 왼쪽 시작은 접힌 컵 중심보다 조금 왼쪽으로 안정적으로 잡힌다.
- image_material (3): 뚜껑의 흰 반투명 테두리와 접힌 실리콘의 둥근 단은 사진처럼 읽힌다. 그러나 native의 녹색 몸체와 밝은 석재 바닥에 모두 매우 촘촘한 구불구불한 미세 선이 반복되어, 서로 다른 재질의 고유 표면보다 공통 합성 질감이 앞선다.
- emotion_control (4): 옅은 녹색 배경과 아침빛, 검정에 가까운 녹색 글자는 제품의 색을 중심으로 차분한 분위기를 만든다. 컵의 두 상태가 주역이고 별도 장식 표식이나 허구 정보는 보이지 않는다.
- ai_slop (3): 두 상태를 직접 비교하는 편집은 이 제품에 맞는다. 다만 native에서 컵 몸체와 바닥에 재등장하는 미세 구불선이 제작 재질을 평준화한다. 720에서는 덜 두드러지지만 원본 마감 문제를 통과시킬 근거는 되지 않는다.

Residuals:
- native 녹색 컵과 석재 바닥에 반복되는 구불구불한 미세 질감 → 실리콘과 석재의 재질 분리가 약해지고 합성 마감이 먼저 보임 → 컵은 실리콘 고유의 고운 무광 표면, 바닥은 더 큰 비정형 석재 입자로 각각 정리. image_material=3, ai_slop=3을 유지하며 하이엔드 후보로 무조건 통과시키지 않음.

Uncertainties:
- 350 mL 표기는 판독됨. 실제 용량, 실제 접힘 기구와 실리콘 성분은 픽셀만으로 검증할 수 없으며 검수 범위 밖이다.

Use readings:
- thumbnail320: Fold Cup과 두 상태 컵이 먼저 보임. 출시 안내는 보이지만 작은 보조 정보다.
- usage720: 7개 필수 문구 모두 판독. FOLN은 하단에 있으며 긴 URL도 명확함.
- native: 미세 재질 질감의 반복이 드러남.

## X738

Mandatory PASS. Native 1024×1536, target 2:3, relative ratio error 0.00000%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: 밤에 피는 정원 | Observed: 밤에 피는 정원 | Equal: True

Located evidence:
- content_form (4): 밤에/피는/정원의 세 줄 큰 글자를 식재 구획처럼 만들고, 밤의 어두운 자주색 바탕에 밝은 꽃과 잎을 심었다. 특히 ㅇ과 ㅁ의 내부도 정원으로 채워 제목과 이미지가 직접 연결된다.
- hierarchy (5): 320에서도 세 줄 전체 제목이 명확히 읽힌다. 작은 꽃의 세부는 뒤로 물러나고 커다란 옅은 글자 면이 먼저 보여, 이미지가 글자를 가리지 않는다.
- typography (4): 넓은 굵기의 둥근 한글은 세 줄의 큰 면을 만들고 내부 식물과 확실한 대비를 유지한다. 꽃이 각 글자의 윤곽을 따라가 글자와 이미지가 묶이지만 모든 글자에 비슷한 장식 밀도를 적용한 점은 다소 균질하다.
- space (4): 상하좌우로 식물 외곽을 남기면서 세 줄이 거의 화면 전체를 채운다. 글자 사이 좁은 틈에도 식물이 이어져 큰 블록들이 끊기지 않으며, 외곽은 잘린 식물 덩어리가 아니라 마감된 테두리로 읽힌다.
- image_material (4): native에서 작은 잎, 자주색 봉오리, 분홍/흰 꽃의 모양이 대체로 분명하며, 어두운 바탕과 옅은 글자 표면의 약한 균열도 일관된다. 식물 가장자리는 명확하나 짙은 외곽 그림자가 전반적으로 같은 장식 깊이를 만든다.
- emotion_control (4): 깊은 자주색과 청록 잎은 밤을, 작은 밝은 꽃은 개화를 표현한다. 풍성함이 제목의 정원에 쓰이므로 과잉 식물을 곧바로 결함으로 보지는 않는다. 다만 각 구획의 비슷한 장식 밀도는 긴장 변화를 줄인다.
- ai_slop (4): 제목의 획과 내부 공간을 식재 영역으로 편집한 결정은 내용에 맞고, 불규칙한 한글 획이나 가짜 문자는 보이지 않는다. 익숙한 꽃 장식 글자 패키지의 성격은 남지만 내부/외부를 다르게 채운 세부가 단순 효과 덧씌우기보다 구체적이다.

Residuals:
- 모든 글자 주위가 비슷하게 촘촘한 꽃/잎 테두리 → 세 줄 사이의 긴장 변화가 줄어듦 → 일부 외곽을 비우거나 개화 밀도를 다르게 해 주요 구획의 강조를 분명히 할 수 있음.

Use readings:
- thumbnail320: 밤에/피는/정원 세 줄 전체 판독.
- usage720: 유일한 필수 제목 판독, 꽃은 글자 영역을 침범하지 않음.
- native: 식물 세부와 글자 표면 균열 확인.

## X847

Mandatory PASS. Native 1122×1402, target 4:5, relative ratio error 0.03566%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: FOLN | Observed: FOLN | Equal: True
- Required: Fold Cup | Observed: Fold Cup | Equal: True
- Required: 가볍게 접고, 다시 펼치다 | Observed: 가볍게 접고, 다시 펼치다 | Equal: True
- Required: 350 mL · 접이식 실리콘 컵 | Observed: 350 mL · 접이식 실리콘 컵 | Equal: True
- Required: 2026.12.01 RELEASE | Observed: 2026.12.01 RELEASE | Equal: True
- Required: 온라인 사전 주문 11.10–11.30 | Observed: 온라인 사전 주문 11.10–11.30 | Equal: True
- Required: foln.example/store | Observed: foln.example/store | Equal: True

Located evidence:
- content_form (5): 접힌 컵을 손으로 들고 천 가방에 넣는 순간을 중심에 놓아 가볍게 접는다는 문구를 휴대 행동으로 설명한다. 단순 제품 초상보다 이 접이식 물건을 사용할 상황이 구체적이다.
- hierarchy (4): 320에서 큰 한글 슬로건과 손에 든 컵이 먼저 보이고 720에서는 상단 FOLN/Fold Cup과 하단 용량/출시/주문/URL이 쉽게 이어진다. 제품명은 작지만 읽을 수 있으며 초점은 기능과 휴대성이다.
- typography (4): 왼쪽 정렬의 흰 글자가 어두운 배경과 가방 면을 따라 배치된다. 슬로건의 두 줄과 하단 주문 안내의 굵기/크기 관계가 안정적이며 얇은 영문 브랜드/주소도 720에서 흐려지지 않는다.
- space (4): 오른쪽 팔의 사선이 중앙 컵으로 들어오고 가방 입구의 사선이 아래로 받아 준다. 빈 상단 왼쪽에 슬로건, 비교적 어두운 하단 왼쪽에 안내를 배치해 물체/손/문자가 간섭하지 않는다.
- image_material (4): native에서 피부의 주름, 가방의 직물 결, 매트한 녹색 실리콘, 반투명 흰 뚜껑이 구분된다. 손가락의 압력 위치와 컵 하단 받침이 대체로 설득력 있고 접힌 단의 가장자리도 안정적이다.
- emotion_control (4): 흰색 글자와 차콜 직물의 낮은 채도는 실용적인 휴대 제품의 느낌을 유지한다. 사진의 사용 행동 하나에 집중하며 효과나 장식으로 기능을 가리지 않는다.
- ai_slop (4): 손과 가방, 접힌 컵의 관계가 문구를 실제 장면으로 만드는 내용 맞춤 결정이다. native에서 뚜렷한 손가락/재질 합성 오류는 보이지 않는다. 다만 큰 기능 문구와 생활 사진의 조합은 익숙한 광고 틀이므로 최상위의 독자적 편집으로 단정하지 않는다.

Residuals:
- FOLN/Fold Cup이 슬로건보다 매우 작음 → 320 첫인상은 기능을 기억하고 제품명을 덜 기억함 → 제품명 기억이 목표라면 상단 Fold Cup을 한 단계 키울 수 있음. 필수 조건 실패는 아님.

Uncertainties:
- 350 mL 표기는 판독됨. 실제 용량, 실제 접힘 기구와 실리콘 성분은 픽셀만으로 검증할 수 없으며 검수 범위 밖이다.

Use readings:
- thumbnail320: 슬로건/손/접힌 컵 먼저 보임. 제품명은 작음.
- usage720: 7개 필수 문구 모두 판독.
- native: 손·직물·실리콘·뚜껑 재질 구분 확인.

## X641

Mandatory PASS. Native 1024×1536, target 2:3, relative ratio error 0.00000%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: 밤에 피는 정원 | Observed: 밤에 피는 정원 | Equal: True

Located evidence:
- content_form (5): 어두운 잎 사이에서 크게 열린 흰 꽃을 밀착 크롭하고, 밤에는 어두운 잎 위의 옅은 글자, 피는 정원은 밝은 꽃잎 위의 검정 글자로 놓았다. 제목의 밤/개화 관계가 사진과 글자 색의 관계까지 연결된다.
- hierarchy (4): 320에서도 밤에와 피는 정원이 모두 읽히며, 크게 열린 꽃과 검정의 주 글자가 먼저 들어온다. 밤에가 상대적으로 작아서 첫 순간은 피는 정원에 치우치지만 왼쪽에서 중앙으로 이어 읽는 경로는 분명하다.
- typography (5): 밤에의 옅은 획과 중앙의 검정 서예적 획이 사진의 밝은 면/어두운 면을 따라 역할을 나눈다. 피는/정원의 두 줄이 꽃잎 중심의 넓은 면을 활용하고 글자 끝이 식물 경계와 우연히 겹치지 않는다.
- space (5): 오른쪽 꽃의 과감한 크롭과 왼쪽 잎의 어두운 여백이 균형을 이룬다. 길게 뻗은 위쪽 꽃잎과 아래쪽 꽃잎의 사선이 제목을 감싸며, 화면에 들어온 일부 꽃만으로 큰 공간을 설계한다.
- image_material (5): native에서 흰 꽃잎의 얇은 주름과 표면 변화, 잎의 광택과 잎맥, 수술의 가는 그림자가 서로 구분되어 보인다. 흰 면이 평평하게 날아가지 않고 빛 방향과 세부 음영이 이어져 사진의 마감이 세밀하다.
- emotion_control (5): 차가운 어두운 잎과 빛나는 흰 꽃만으로 조용하고 집중된 밤의 정서를 만든다. 별/빛 입자 같은 추가 효과 없이 크롭과 명암이 역할을 한다.
- ai_slop (5): 글자 색을 배경 면에 따라 바꾸고 꽃의 크롭 안에 주 문구를 놓은 편집은 이 이미지와 제목에 맞는다. native에서도 눈에 띄는 녹은 경계, 이상한 한글, 무관한 표식은 보이지 않는다. 사진으로 제작 주체를 추론하지 않는다.

Residuals:
- 320 첫 시선은 큰 피는 정원과 흰 꽃에 모여 작은 밤에가 뒤에 읽힐 수 있음. 현재 전체 문구의 판독을 막지 않으며, 시간 어절을 더 먼저 읽히게 하려면 밤에의 크기를 소폭 키울 수 있음.

Use readings:
- thumbnail320: 전체 제목 판독. 피는 정원이 밤에보다 먼저 눈에 띔.
- usage720: 유일한 제목 판독. 밝은/어두운 면과 글자 색 대응 유지.
- native: 꽃잎과 잎의 재질/빛/그림자 세부 확인.

## X300

Mandatory PASS. Native 1024×1536, target 2:3, relative ratio error 0.00000%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: 밤에 피는 정원 | Observed: 밤에 피는 정원 | Equal: True

Located evidence:
- content_form (5): 밤의 정원 길을 화면 위에서 아래로 굽히고 밤에/피는/정원을 그 길의 세 지점에 놓았다. 제목을 따라 읽는 이동과 정원을 걷는 경로가 같은 구도로 연결된다.
- hierarchy (5): 320에서도 세 어절을 위에서 아래로 읽을 수 있고, 밝은 글자와 꽃이 어두운 길/잎에서 분명히 분리된다. 밤에에서 피는을 거쳐 정원으로 내려가는 대각선 순서가 자연스럽다.
- typography (4): 부드럽고 불균일한 두꺼운 획의 옅은 글자는 꽃의 밝은 색을 받아 길 위에 읽을 면을 만든다. 세 어절의 배치가 각각 길의 폭에 맞지만 글자 자체는 익숙한 둥근 손글씨 성격이 남는다.
- space (5): 중앙 S자 길의 여백을 오른쪽과 왼쪽의 식물 덩어리가 번갈아 열고 닫는다. 상단 밤에, 중간 피는, 하단 정원이 길의 굴곡을 타며 식물과 글자 사이에 어두운 완충 면을 확보한다.
- image_material (4): native에서 흙의 돌, 큰 청록 잎, 작은 흰 꽃, 하단의 가는 꽃잎이 일관된 회화적 표현으로 구분된다. 일부 꽃잎/꽃 중심은 단순한 반복 도식이지만 매체 전체의 세밀한 그림 처리와 충돌하지 않는다.
- emotion_control (5): 어두운 녹색 잎과 흰 개화의 반복은 조용한 산책의 정서를 만든다. 화면을 가득 채운 식물은 길을 열어 주는 데 쓰이고, 밝은 꽃이 제목에서 시선을 빼앗지 않는다.
- ai_slop (4): 길의 빈 면을 읽기 경로로 사용한 편집은 구체적이며 의미 없는 표식이나 가짜 문자는 없다. 다만 촘촘한 청록 잎/흰꽃과 크림색 둥근 글자의 조합에는 익숙한 환상 정원 삽화 습관이 조금 남는다. 이것은 제작 주체 판별이 아니라 표현 틀에 대한 관찰이다.

Residuals:
- 청록색 식물/흰꽃/크림색 둥근 글자에는 익숙한 환상 정원 삽화 어휘가 남음 → 매우 구체적인 개화 시각의 특색은 약함 → 길 편집을 유지하면서 특정 한 구역의 개화 단계 차이를 더 명확히 할 수 있음.

Use readings:
- thumbnail320: 길을 따라 밤에→피는→정원 판독.
- usage720: 유일한 제목 전체 판독.
- native: 식물·흙·바위의 회화적 묘사 확인.

## X943

Mandatory PASS. Native 1254×1254, target 1:1, relative ratio error 0.00000%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: 고쳐 쓰는 토요일 | Observed: 고쳐 쓰는 토요일 | Equal: True
- Required: 이웃 수리 작업실 참여자 모집 | Observed: 이웃 수리 작업실 참여자 모집 | Equal: True
- Required: 2026년 12월 5일 토요일 | Observed: 2026년 12월 5일 토요일 | Equal: True
- Required: 오후 2시–5시 · 입장은 오후 1시 40분부터 | Observed: 오후 2시–5시 · 입장은 오후 1시 40분부터 | Equal: True
- Required: 하람시 잇는집 2층 · 수선길 12 | Observed: 하람시 잇는집 2층 · 수선길 12 | Equal: True
- Required: 대상: 만 16세 이상 · 회차별 12명 | Observed: 대상: 만 16세 이상 · 회차별 12명 | Equal: True
- Required: 작은 생활용품 한 점을 가져와 주세요. | Observed: 작은 생활용품 한 점을 가져와 주세요. | Equal: True
- Required: 전기·배터리 제품과 위험한 물건은 받지 않습니다. | Observed: 전기·배터리 제품과 위험한 물건은 받지 않습니다. | Equal: True
- Required: 도구는 제공하며 부품 비용은 현장에서 안내합니다. | Observed: 도구는 제공하며 부품 비용은 현장에서 안내합니다. | Equal: True
- Required: 수리 여부는 상태 확인 후 결정하며 완성을 보장하지 않습니다. | Observed: 수리 여부는 상태 확인 후 결정하며 완성을 보장하지 않습니다. | Equal: True
- Required: 촬영은 동의한 참여자에 한해 진행합니다. | Observed: 촬영은 동의한 참여자에 한해 진행합니다. | Equal: True
- Required: 참가비 5,000원 · 현장 결제 | Observed: 참가비 5,000원 · 현장 결제 | Equal: True
- Required: 12월 2일까지 신청: haram-mend.example/join | Observed: 12월 2일까지 신청: haram-mend.example/join | Equal: True
- Required: 문의: 이웃 수리 운영팀 | Observed: 문의: 이웃 수리 운영팀 | Equal: True

Located evidence:
- content_form (4): 거울 옆축에 드라이버를 넣는 작은 생활용품 수리 그림을 우상단에 놓았다. 받지 않는 전기 제품 대신 간단한 생활 물건의 수리를 보여 주며, 큰 신청 안내가 참여 행위를 먼저 만든다.
- hierarchy (5): 320의 첫 시선이 파란 12월 2일까지 신청과 전체 URL로 향한다. 720에서 아래의 행사명, 왼쪽 날짜/장소/자격/비용, 오른쪽 참여 조건을 읽을 수 있어 신청 정보를 찾는 과제가 잘 해결된다.
- typography (4): 파란 굵은 신청/주소, 검정 큰 행사명, 작은 두 열 본문이 일관된 굵기/크기 관계를 만든다. 긴 URL도 하나의 행으로 유지되고 본문 행간이 대체로 충분하지만 오른쪽 안내는 비슷한 무게의 여러 문단이어서 작은 구분은 약하다.
- space (3): 상단의 큰 글자와 우상단 그림, 하단의 두 열은 큰 관계가 안정적이다. 그러나 native에서 URL 끝 join과 거울 왼쪽 아래 외곽선이 매우 근접하며, 720에서도 글자 끝과 선이 거의 맞닿아 보인다. 참여 안내의 끝에 시각적 잡음을 만들므로 거울을 오른쪽/위로 이동해 명확한 간격을 확보하는 것이 좋다.
- image_material (4): 가는 검정 선의 거울, 받침, 드라이버가 동일한 도해 체계로 그려진다. 약한 푸른 바탕에는 불필요한 광택이나 종이 질감이 없고, 물체 가장자리도 대체로 안정적이다. 거울 축의 작은 복잡한 선은 320에서 세부 구분이 줄어든다.
- emotion_control (4): 파랑 한 가지로 신청과 날짜를 강조하고 다른 내용은 검정으로 읽게 해 실용적인 동네 안내의 정서를 유지한다. 별도 장식 효과 없이 거울 수리 그림이 친근함을 더한다.
- ai_slop (4): 신청 우선 편집과 실제 수리 지점을 그린 그림은 내용에 맞고, 이상한 글자나 허구 안내는 보이지 않는다. URL와 그림의 가까운 접촉은 합성 여부를 뜻하지 않지만 정밀한 마감에서 남은 관계 문제다. 이 지점을 해결해야 높은 완성도로 단정하기 쉬워진다.

Residuals:
- native URL 끝 join과 거울 왼쪽 아래 선의 매우 가까운 접촉 → 신청 안내 끝에 원치 않는 시각 간섭 → 거울을 오른쪽/위로 옮기거나 약간 줄여 URL와 충분한 간격 확보. space=3은 큰 구조가 기능해도 이 작은 관계의 결함을 보존함.

Use readings:
- thumbnail320: 신청 기한과 전체 주소 먼저 읽힘. 조건 문구의 완전 판독은 이 크기에 요구하지 않음.
- usage720: 14개 문구 모두 판독. 신청/주소를 즉시 찾음.
- native: 주소 끝과 거울 선의 좁은 간격 확인.
- event_date: 2026년 12월 5일 토요일
- deadline: 12월 2일까지 신청
- application_url: haram-mend.example/join
- location: 하람시 잇는집 2층 · 수선길 12

## X762

Mandatory PASS. Native 1024×1536, target 2:3, relative ratio error 0.00000%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: 밤에 피는 정원 | Observed: 밤에 피는 정원 | Equal: True

Located evidence:
- content_form (5): 위의 봉오리, 가운데 부분 개화, 아래의 크게 열린 꽃이라는 세 상태에 밤에/피는/정원을 각각 대응했다. 단어가 커지는 것과 꽃이 열리는 진행이 함께 작동해 제목의 피는을 형태로 설명한다.
- hierarchy (4): 320에서 세 단계와 모든 단어가 읽힌다. 하단 정원과 큰 꽃이 먼저 보일 수 있으나 위쪽 봉오리부터 아래까지 세로 연속성이 분명해 전체 문구를 빠르게 따라갈 수 있다.
- typography (4): 크림색의 둥근 두꺼운 획이 꽃잎의 곡선과 맞는다. 밤에는 작은 봉오리 아래, 피는은 열린 꽃 아래, 정원은 큰 꽃의 어두운 중심 안에 있어 글자가 이미지의 다른 상태를 담당한다.
- space (4): 상단 작은 봉오리와 큰 하단 개화가 넓어지는 삼각형 무게를 만든다. 중심축이 안정적이고, 하단 꽃의 가장 넓은 양옆과 하단 끝이 프레임에 가까워 충분히 힘 있는 마감을 갖지만 여백의 압박은 조금 남는다.
- image_material (5): 복숭아색과 분홍색 꽃잎 면, 올리브색 꽃받침, 짙은 남색 바탕이 일관된 평면 콜라주 체계다. native에서도 종이 같은 미세 표면과 명확한 가장자리가 유지되고 재질/조명 혼동이 보이지 않는다.
- emotion_control (5): 따뜻한 꽃색과 깊은 밤색의 대비가 차분한 생동감을 만든다. 개화 단계가 표현의 주역이며 질감이나 효과를 여러 겹 쌓지 않아 큰 면의 색과 형태가 정확히 역할을 한다.
- ai_slop (5): 세 단계 개화와 세 어절의 대응, 마지막 단어를 꽃 중심 안에 넣은 결정이 내용에 특화되어 있다. 평면 꽃잎과 글자의 가장자리는 안정적이며 우연히 녹은 선이나 가짜 미세문자는 보이지 않는다. 익숙한 콜라주 매체 자체를 감점하지 않았다.

Residuals:
- 큰 하단 꽃잎 끝의 좁은 가장자리 여백 → 완성된 꽃 단계가 프레임에 조금 눌리는 인상 → 하단 개화 덩어리를 소폭 줄이거나 하단 여백을 늘릴 수 있음. 판독 실패는 아님.

Use readings:
- thumbnail320: 세 단계 꽃과 전체 제목 판독. 정원이 먼저 클 수 있음.
- usage720: 유일한 제목 판독, 꽃 중심 속 정원도 분명함.
- native: 평면 콜라주 경계/표면 확인.

## X770

Mandatory PASS. Native 1086×1448, target 3:4, relative ratio error 0.00000%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: 고쳐 쓰는 토요일 | Observed: 고쳐 쓰는 토요일 | Equal: True
- Required: 이웃 수리 작업실 참여자 모집 | Observed: 이웃 수리 작업실 참여자 모집 | Equal: True
- Required: 2026년 12월 5일 토요일 | Observed: 2026년 12월 5일 토요일 | Equal: True
- Required: 오후 2시–5시 · 입장은 오후 1시 40분부터 | Observed: 오후 2시–5시 · 입장은 오후 1시 40분부터 | Equal: True
- Required: 하람시 잇는집 2층 · 수선길 12 | Observed: 하람시 잇는집 2층 · 수선길 12 | Equal: True
- Required: 대상: 만 16세 이상 · 회차별 12명 | Observed: 대상: 만 16세 이상 · 회차별 12명 | Equal: True
- Required: 작은 생활용품 한 점을 가져와 주세요. | Observed: 작은 생활용품 한 점을 가져와 주세요. | Equal: True
- Required: 전기·배터리 제품과 위험한 물건은 받지 않습니다. | Observed: 전기·배터리 제품과 위험한 물건은 받지 않습니다. | Equal: True
- Required: 도구는 제공하며 부품 비용은 현장에서 안내합니다. | Observed: 도구는 제공하며 부품 비용은 현장에서 안내합니다. | Equal: True
- Required: 수리 여부는 상태 확인 후 결정하며 완성을 보장하지 않습니다. | Observed: 수리 여부는 상태 확인 후 결정하며 완성을 보장하지 않습니다. | Equal: True
- Required: 촬영은 동의한 참여자에 한해 진행합니다. | Observed: 촬영은 동의한 참여자에 한해 진행합니다. | Equal: True
- Required: 참가비 5,000원 · 현장 결제 | Observed: 참가비 5,000원 · 현장 결제 | Equal: True
- Required: 12월 2일까지 신청: haram-mend.example/join | Observed: 12월 2일까지 신청: haram-mend.example/join | Equal: True
- Required: 문의: 이웃 수리 운영팀 | Observed: 문의: 이웃 수리 운영팀 | Equal: True

Located evidence:
- content_form (5): 사진의 손/드라이버가 작은 나무 상자의 경첩 나사를 조이는 장면과 고쳐 쓰는 토요일의 큰 제목이 한 열을 공유한다. 이웃 수리 작업실이 받는 생활용품과 활동의 규모가 구체적으로 보인다.
- hierarchy (4): 320에서 왼쪽 행사명과 오른쪽 날짜, 하단 신청 블록이 명확한 큰 단위로 보인다. 720에서 전체 조건 문구를 읽을 수 있으며 하단 기한/URL도 충분히 크다. 다만 사진/행사명에서 신청까지 긴 본문 열을 거치는 구조여서 신청 최우선은 아니다.
- typography (4): 제목과 모집 부제의 굵은 검정 두 줄이 사진 상단에서 강한 덩어리를 만든다. 오른쪽 날짜/장소/자격의 굵기와 본문/신청의 크기를 구분했고, 본문 줄바꿈은 어절을 망가뜨리지 않는다.
- space (4): 세로 가는 선으로 사진/제목 열과 안내 열을 분리하고 양쪽 하단을 맞춘다. 오른쪽 문단의 반복 여백과 하단 신청/문의의 분리가 안정적이지만, 오른쪽 상단이 왼쪽 제목보다 아래에서 시작해 위쪽 안내 면의 여백이 조금 크다.
- image_material (4): native에서 목재의 거친 결, 반사하는 금속 경첩, 손의 피부와 드라이버가 구분된다. 나사에 공구가 닿는 위치와 손으로 상자를 받치는 장면이 설득력 있다. 경첩의 반사 세부와 거친 목재 일부는 복잡하지만 명백한 물체 경계 붕괴는 보이지 않는다.
- emotion_control (4): 흑백 사진과 무채색 글자는 전문적이면서 소박한 작업 안내의 느낌을 만든다. 손과 작은 수리 대상에 집중하고 색/효과를 추가하지 않아 참여 조건의 진지함과 충돌하지 않는다.
- ai_slop (4): 수리 동작과 큰 행사명의 결합은 범용 도구 장식보다 내용에 맞다. native에서도 뚜렷한 손 해부나 글자 합성 오류는 보이지 않는다. 두 열 흑백 편집과 큰 굵은 산세리프는 익숙한 안내 포스터 틀이므로 모든 편집 관계가 예외적으로 해결됐다고 단정하지 않는다.

Residuals:
- 신청 안내가 긴 오른쪽 본문의 하단에 놓임 → 제목/사진을 먼저 본 뒤 참여 주소로 이동하는 데 더 많은 시선 이동 필요 → 온라인 참여 전환을 최우선으로 삼으면 기한/주소 블록을 오른쪽 상단으로 이동할 수 있음. 현재 720에서는 쉽게 찾고 읽음.

Use readings:
- thumbnail320: 행사명/날짜/신청 블록이 먼저 보임. 전체 조건의 완전 판독은 720에서 확인.
- usage720: 14개 문구 모두 판독. 하단 기한/전체 주소 명확함.
- native: 수리 사진의 공구 접촉·경첩·손과 문단 관계 확인.
- event_date: 2026년 12월 5일 토요일
- deadline: 12월 2일까지 신청
- application_url: haram-mend.example/join
- location: 하람시 잇는집 2층 · 수선길 12

## X340

Mandatory PASS. Native 1024×1536, target 2:3, relative ratio error 0.00000%. All required copy legible at720; no extra copy observed.

Manual transcription:
- Required: 밤에 피는 정원 | Observed: 밤에 피는 정원 | Equal: True

Located evidence:
- content_form (4): 밤색 바탕에 밝은 연두색 한 송이의 꽃과 길게 굽은 줄기를 그린다. 정원의 원 마지막 획이 아래 줄기로 이어져 문구와 식물을 연결한다. 다만 일반적인 한 송이 꽃 도해이므로 밤에 피는이라는 구체적 시간 변화는 주로 색과 제목에 의존한다.
- hierarchy (4): 320에서도 밤에 피는/정원 두 줄 전체가 읽힌다. 위의 큰 꽃 윤곽을 먼저 보게 되지만 가운데 글자와 같은 밝은 선 색이어서 제목으로 이동하기 쉽다.
- typography (5): 가늘고 유연한 한글 획이 식물의 외곽선과 같은 표현을 쓰고, 원의 마지막 획이 줄기 곡선으로 이어져 글자와 이미지가 하나의 선 체계로 작동한다. 의도적인 손선의 변동은 판독을 훼손하지 않는다.
- space (4): 왼쪽 위의 넓은 꽃과 오른쪽 아래로 빠지는 줄기가 대각선 균형을 만든다. 가운데 왼쪽 글자 주변을 잎 곡선이 감싸고 하단 어두운 면을 충분히 남기지만, 위쪽 왼잎 끝과 밤 글자 사이의 간격은 작은 관계에서 다소 촘촘하다.
- image_material (4): native에서 외곽선의 굵기 변동과 가늘어지는 내부 잎맥이 일관된 선화로 보인다. 320에서는 가장 가는 잎맥/꽃잎 선 일부가 약해지지만 중요 외곽과 문구는 유지된다. 거칠음이 재질 오류나 무차별 효과로 보이지 않는다.
- emotion_control (5): 남색과 연두색 두 색, 비어 있는 면, 조용한 선 하나의 흐름으로 밤의 섬세한 정서를 만든다. 별도 빛/입자 효과 없이 꽃과 글자 선의 리듬만으로 표현을 통제한다.
- ai_slop (4): 원의 획을 식물 줄기로 이어 편집한 위치가 내용 맞춤의 근거다. 글자와 그림에 녹은 외곽이나 가짜 정보를 찾지 못했다. 한 송이 선화 꽃/어두운 바탕이라는 익숙한 틀은 남으며 낮은 효과량 자체를 높은 점수의 이유로 쓰지 않았다.

Residuals:
- 일반적인 한 송이 꽃 도해와 밤색 바탕 → 개화 시간이라는 구체적 발상은 주로 문구에 맡겨짐 → 선 체계를 유지한 채 봉오리/개화의 차이를 한 지점에 더할 수 있음. 새 장식이나 효과가 필요한 것은 아님.

Use readings:
- thumbnail320: 큰 꽃을 본 뒤 밤에 피는/정원 전체 판독. 가는 내부 선 일부는 약해짐.
- usage720: 유일한 제목 전체 판독.
- native: 정원의 원 획과 줄기 연결 및 선 굵기 변화 확인.

## Set diversity

Nearest-pair scores use the same 1–5 difference anchors as set diversity. They score differentiation, not which poster is better.

### title-only

Members: X641, X762, X300, X738, X340. Diversity: 4. Closest pair: X641, X300; differentiation score: 4.

X641의 밀착 꽃 사진/명암 대응 글자, X762의 봉오리→개화 세 단계/확대되는 글자, X300의 정원 길/이동하는 읽기 경로, X738의 획 자체를 식재 구획으로 만든 큰 블록 글자, X340의 한 선 식물/원 획에서 줄기로의 연결이 각각 다른 글자 역할과 공간을 만든다. 다섯 모두 어두운 바탕과 밝은 꽃/글자를 공유하고 세 출력에는 둥근 유기적 한글이라는 습관이 있어 다양성을 5로 단정하지 않는다.

두 출력은 어두운 녹색 식물, 밝은 꽃, 유기적 크림색/검정 한글의 정서를 공유한다. 하지만 X641은 한 꽃의 사진 같은 밀착 크롭과 면에 반응하는 두 색 글자, X300은 정원 길의 회화적 전경과 대각선 세 어절의 이동을 쓰므로 단순 색 교체가 아니다.

- X641/X300의 녹색 식물·밝은 꽃·어두운 바탕이 가장 가까운 정서 영역이다. 다양한 방식이지만 팔레트/식물 정서의 분산은 구조의 분산보다 작다.

### product

Members: X800, X847. Diversity: 5. Closest pair: X800, X847; differentiation score: 5.

같은 필수 제품 조건 안에서 X800은 접힘 전후를 보여 주고 X847은 휴대성의 장면을 보여 준다. 밝은 스튜디오 같은 비교 사진과 어두운 손/가방 생활 사진의 차이는 팔레트나 필터에 그치지 않는다. 다양성=5가 X800의 재질/AI-slop=3을 상쇄하지 않는다.

X800은 밝은 바닥의 두 상태 비교와 오른쪽의 큰 제품명, X847은 어두운 천 가방에 접힌 컵을 넣는 행동과 왼쪽의 큰 기능 문구다. 같은 제품의 색을 유지하면서 제품 설명/사용 장면, 글자 주역, 물체 크롭, 빛과 공간이 달라진다.

- X800의 원본 미세 질감 결함은 세트 다양성과 별개이며 그대로 유지한다. 두 장 모두 굵은 기능 문구와 작은 하단 출시 정보라는 광고 문법은 공유한다.

### invitation

Members: X770, X943. Diversity: 4. Closest pair: X770, X943; differentiation score: 4.

세로 3:4에서는 작업 동작/행사 정체성이 먼저, 정사각에서는 신청 행동이 먼저 오도록 정보 위계가 바뀐다. 흑백 실물 같은 사진과 선화 수리 도해, 검정 일색과 선택적인 파랑도 달라진다. 두 열 안내 구조와 익숙한 굵은 산세리프가 공통이라 5로 채점하지 않는다.

X770은 왼쪽 흑백 수리 사진/행사명, 오른쪽 날짜→조건→신청의 세로 열이다. X943은 상단 파란 신청/URL부터 시작하고 우상단 거울 수리 선화를 둔 다음 하단 두 열로 정보를 나눈다. 두 장 모두 밝은 바탕·굵은 산세리프·실용적 열 구조를 공유하지만 시선의 시작과 이미지 표현은 다르다.

- X943 URL–거울 외곽선의 근접 접촉은 다양성과 무관한 공간 마감 문제다. X770은 성공적으로 읽히지만 신청 블록까지의 경로가 더 길다.

## Actual viewed paths

- X800 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X800-native.png
- X800 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X800-usage720.png
- X800 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X800-thumbnail320.png
- X738 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X738-native.png
- X738 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X738-usage720.png
- X738 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X738-thumbnail320.png
- X847 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X847-native.png
- X847 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X847-usage720.png
- X847 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X847-thumbnail320.png
- X641 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X641-native.png
- X641 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X641-usage720.png
- X641 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X641-thumbnail320.png
- X300 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X300-native.png
- X300 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X300-usage720.png
- X300 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X300-thumbnail320.png
- X943 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X943-native.png
- X943 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X943-usage720.png
- X943 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X943-thumbnail320.png
- X762 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X762-native.png
- X762 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X762-usage720.png
- X762 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X762-thumbnail320.png
- X770 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X770-native.png
- X770 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X770-usage720.png
- X770 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X770-thumbnail320.png
- X340 native: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X340-native.png
- X340 usage720: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X340-usage720.png
- X340 thumbnail320: /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round5/blind-correction2/images/X340-thumbnail320.png
