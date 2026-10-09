# R7-B05 · initial · craft

The supplied artwork is complete, prominent and recognizable, and all six protected copy entries match. The mandatory style check is **FAIL** because the artwork is slightly smaller and lower on the wall than pinned A1. Image material scores **3**; the other six dimensions each score **4**. No average is used.

## Procedure

In this fresh independent review, I verified SHA-256 and byte counts of the 13 explicitly pinned inputs and read the packet, case, rules, rubric, ratio policy and supplied asset/native manifests. I did not follow embedded manifest paths. I called tools.view_image through functions.exec and displayed the returned image with original detail, first for A1 original.png, then separately for R7-B05-M1 native original.png, usage-720.png and thumbnail-320.png in that exact packet order. All three poster displays completed before any transcription judgment or score. I then recorded the first observed six copy reads without a revisit. Native dimensions were read from PNG headers; source/poster blue bounds and mount-region centroids were compared using a Python standard-library PNG decoder, with no generated, edited or saved image. The packet declares no protected-layout measurements. Session/thread identity is not claimed; runner provenance remains external to this report.

- fresh_session: true
- all_views_before_scoring: true
- all_views_before_transcription: true
- order_compliant: true
- viewed_count: 3
- session_id: null
- protected_layouts_read: [] (none supplied)

Source viewed first: **A1**, `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/assets/A1/original.png`, SHA-256 `e3dfe1e4b6825d9456e0e6c072d110fe212b33ef67e4183034cebc849df45460`, viewed=true.

Asset manifest read: `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/assets/A1/manifest.json`, SHA-256 `16057e224f6c2211345306be6906bf4ef6abe51fb419e93d75d0216a85a74d1d`.

Native manifest read: `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B05-M1/stages/initial/manifest.json`, SHA-256 `6bc48dd7b86fa8af0decae127d82352cbe613d987f3b14769a06fe6baafe4cdb`.

Poster views displayed in order before transcription or scoring:

1. R7-B05-M1 / native — 1122×1402 — `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B05-M1/stages/initial/original.png` — SHA-256 `41c0d2d003c62e06384ee6f11cee7b6f924982990c689f36882855d7bae0cdf1`
2. R7-B05-M1 / usage720 — 720×900 — `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B05-M1/stages/initial/usage-720.png` — SHA-256 `14b2c8ec78bb73f6a9a8449bfe4e432438f7181b2e1581b97eeaece9dc294b12`
3. R7-B05-M1 / thumbnail320 — 256×320 — `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round7/production/R7-B05-M1/stages/initial/thumbnail-320.png` — SHA-256 `5ce51469ed2d0281f8bba97261089e7f83e93938ed27cd560c0f23b986251f4a`

## Literal style requirement checked

첨부한 `atelier-photo.jpg`를 중심으로 작가 오픈 스튜디오 포스터 1종을 만들어 주세요. 세로 4:5입니다. 사진 속 작품 전체가 충분한 크기의 비문자 시각 중심이어야 합니다. 작품의 비율과 색, 벽에 걸린 위치를 유지해 주세요. 작품을 새로 그리거나 다른 작품으로 바꾸지 마세요. 주변의 벽과 실제 작업실 분위기를 활용할 수 있지만, 가짜 작업 도구나 작가의 얼굴은 추가하지 마세요. 아래 문구를 모두 그대로 넣어 주세요. 날짜와 주소가 작품을 가리지 않게 읽혀야 합니다.

Literal client styles:
{"mode": "actual supplied synthetic photograph preservation"}

Literal mandatory client conditions:
첨부한 `atelier-photo.jpg`를 중심으로 작가 오픈 스튜디오 포스터 1종을 만들어 주세요.
세로 4:5입니다.
사진 속 작품 전체가 충분한 크기의 비문자 시각 중심이어야 합니다.
작품의 비율과 색, 벽에 걸린 위치를 유지해 주세요.
작품을 새로 그리거나 다른 작품으로 바꾸지 마세요.
주변의 벽과 실제 작업실 분위기를 활용할 수 있지만, 가짜 작업 도구나 작가의 얼굴은 추가하지 마세요.
아래 문구를 모두 그대로 넣어 주세요.
날짜와 주소가 작품을 가리지 않게 읽혀야 합니다.
Every role is one separate flat opaque poster at its specified ratio with all supplied copy.
Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels.
A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient.
The actual inputs are original authorized synthetic fixtures, not real client photographs or real products. Exact request attachment aliases map to authoritative native PNG paths. Preserve identity and specified properties; exact-pixel equality is not automatic.

## Mandatory checks

| Check | Status | Finding |
|---|---|---|
| text | PASS | All six protected comparisons are equal; no ambiguity or revisit. |
| style | FAIL | Wall placement changed: blue bounds are lower and slightly smaller than A1. |
| ratio | PASS | 1122×1402; rounded 4:5 under nearest-integer-single-edge, not mathematically exact. |
| no_type_only | PASS | Large complete wall-mounted blue artwork is substantive nonglyph content. |
| substantive_visual | PASS | Two-loop painted work, mounts and wall shadows support the open-studio content. |

Ratio calculation: 1122 differs from 1402×4/5=1121.6 by 0.4 px; 1402 differs from 1122×5/4=1402.5 by 0.5 px. Both meet the declared single-edge rounding boundary. Native bytes were not resized.

Source fidelity measurement: The whole artwork is visibly lower and slightly smaller than A1. With the identical blue-pixel criterion B-R>35, B-G>10, B>60, inclusive bounds change from A1 [123,239,975,1048] to poster [127,274,967,1071]: the top moves down 35 px and the bottom down 23 px, while the blue bounds shrink from 853×810 to 841×798. Brass-pixel centroid measurements in the two mount regions also move down about 33 and 25 px. This is a change to the requested wall placement, rather than evidence based only on unequal pixels.

The bounds use the same stated color criterion for both pinned native images. They measure visible blue pixels, not exact physical object dimensions; mount centroids are likewise color-region measurements. The visible and measured downward placement change is the definite failure. Identity, blue color and overall proportions are retained visually; unequal pixels alone do not establish replacement or a production method.

## Protected copy: first reads and comparison

Normalization: `nfc-ws-optical-v1` (NFC, whitespace runs collapsed, word spaces retained; only text-kind middle-dot/slash optical spacing exceptions; no such exception for the URL entry). All entries have fixed_newlines=false.

### Copy 1 · text

- Required: `작업실의 오후`
- First raw observed (native): `작업실의 오후`
- Normalized required: `작업실의 오후`
- Normalized observed: `작업실의 오후`
- equal: true
- Layout status: PASS. Native: one unbroken title line in the upper-left wall, approximately x110–675, y73–163. No fixed newline was requested.
- ambiguity: null; revisit: null

### Copy 2 · text

- Required: `김서안 오픈 스튜디오`
- First raw observed (native): `김서안 오픈 스튜디오`
- Normalized required: `김서안 오픈 스튜디오`
- Normalized observed: `김서안 오픈 스튜디오`
- equal: true
- Layout status: PASS. Native: one unbroken subtitle line immediately below the title, approximately x114–535, y192–234. No fixed newline was requested.
- ambiguity: null; revisit: null

### Copy 3 · text

- Required: `2026.11.28 14:00–19:00`
- First raw observed (native): `2026.11.28 14:00–19:00`
- Normalized required: `2026.11.28 14:00–19:00`
- Normalized observed: `2026.11.28 14:00–19:00`
- equal: true
- Layout status: PASS. Native: one unbroken date/time line below the complete artwork, approximately x118–605, y1134–1167. The time range contains the observed en dash; its glyph sidebearings are not transcribed as additional word spaces. No fixed newline was requested.
- ambiguity: null; revisit: null

### Copy 4 · text

- Required: `연희로 18길 24, 2층`
- First raw observed (native): `연희로 18길 24, 2층`
- Normalized required: `연희로 18길 24, 2층`
- Normalized observed: `연희로 18길 24, 2층`
- equal: true
- Layout status: PASS. Native: one unbroken address line below the date, approximately x118–470, y1192–1230. The word space before 18길, comma after 24 and space before 2층 are retained. No fixed newline was requested.
- ambiguity: null; revisit: null

### Copy 5 · text

- Required: `작품과 제작 과정을 함께 보는 시간`
- First raw observed (native): `작품과 제작 과정을 함께 보는 시간`
- Normalized required: `작품과 제작 과정을 함께 보는 시간`
- Normalized observed: `작품과 제작 과정을 함께 보는 시간`
- equal: true
- Layout status: PASS. Native: one unbroken supporting line below the address, approximately x119–611, y1264–1293. No fixed newline was requested.
- ambiguity: null; revisit: null

### Copy 6 · url

- Required: `방문 예약 example.org/atelier-afternoon`
- First raw observed (native): `방문 예약 example.org/atelier-afternoon`
- Normalized required: `방문 예약 example.org/atelier-afternoon`
- Normalized observed: `방문 예약 example.org/atelier-afternoon`
- equal: true
- Layout status: PASS. Native: one unbroken reservation/URL line at the bottom, approximately x119–764, y1315–1345. The domain period, slash and hyphen remain contiguous within the URL. This entire protected entry is kind:url, with no optical punctuation exception. No fixed newline was requested.
- ambiguity: null; revisit: null

## Every literal condition

- **PASS** — 첨부한 `atelier-photo.jpg`를 중심으로 작가 오픈 스튜디오 포스터 1종을 만들어 주세요. The complete large and small loops occupy most of the central field and visibly communicate the artist studio subject. They are substantial nonglyph content, with recognizable painted surfaces, mounts and shadows.
- **PASS** — 세로 4:5입니다. The native dimensions are 1122×1402, accepted for requested 4:5 by nearest-integer-single-edge rounding; the ratio is not mathematically exact.
- **PASS** — 사진 속 작품 전체가 충분한 크기의 비문자 시각 중심이어야 합니다. The complete large and small loops occupy most of the central field and visibly communicate the artist studio subject. They are substantial nonglyph content, with recognizable painted surfaces, mounts and shadows.
- **FAIL** — 작품의 비율과 색, 벽에 걸린 위치를 유지해 주세요. The whole artwork is visibly lower and slightly smaller than A1. With the identical blue-pixel criterion B-R>35, B-G>10, B>60, inclusive bounds change from A1 [123,239,975,1048] to poster [127,274,967,1071]: the top moves down 35 px and the bottom down 23 px, while the blue bounds shrink from 853×810 to 841×798. Brass-pixel centroid measurements in the two mount regions also move down about 33 and 25 px. This is a change to the requested wall placement, rather than evidence based only on unequal pixels.
- **PASS** — 작품을 새로 그리거나 다른 작품으로 바꾸지 마세요. The full recognizable two-loop ribbon form, central crossing, cobalt/ultramarine painted surface, two brass mounts and soft wall shadows remain visible. Its bounding-box proportions closely match A1; no substitute artwork is visible. The position drift is recorded separately.
- **PASS** — 주변의 벽과 실제 작업실 분위기를 활용할 수 있지만, 가짜 작업 도구나 작가의 얼굴은 추가하지 마세요. The supplied wall, blue work and mounts are present; no added fake working tools or artist face is visible.
- **PASS** — 아래 문구를 모두 그대로 넣어 주세요. All six protected entries match the literal copy under nfc-ws-optical-v1; raw observations and layouts are retained separately.
- **PASS** — 날짜와 주소가 작품을 가리지 않게 읽혀야 합니다. Both practical lines are legible at usage size and lie below, without overlapping, the complete artwork.
- **PASS** — Every role is one separate flat opaque poster at its specified ratio with all supplied copy. One separate flat portrait poster contains all supplied copy and its ratio passes the declared integer-rounding policy.
- **PASS** — Preserve the complete title/copy; do not invent additional copy, logos, sponsors or labels. Complete required title/copy is retained; no additional copy, sponsor, logo or label is visible.
- **PASS** — A substantive content-grounded non-glyph visual is required; glyph-only output, 3D type alone, texture and token ornament are insufficient. The complete large and small loops occupy most of the central field and visibly communicate the artist studio subject. They are substantial nonglyph content, with recognizable painted surfaces, mounts and shadows.
- **PASS** — The actual inputs are original authorized synthetic fixtures, not real client photographs or real products. Exact request attachment aliases map to authoritative native PNG paths. Preserve identity and specified properties; exact-pixel equality is not automatic. The full recognizable two-loop ribbon form, central crossing, cobalt/ultramarine painted surface, two brass mounts and soft wall shadows remain visible. Its bounding-box proportions closely match A1; no substitute artwork is visible. The position drift is recorded separately.

## Seven independent dimensions

| Dimension | Score |
|---|---:|
| content_form | 4 |
| hierarchy | 4 |
| typography | 4 |
| space | 4 |
| image_material | 3 |
| emotion_control | 4 |
| ai_slop | 4 |

### content_form — 4

- **usage720 · complete central artwork against the wall**: The supplied recognizable two-loop work is large and complete, and the surrounding wall, physical mounts and shadows give the open-studio announcement a specific visual subject.
- **native · top artist/open-studio subtitle and bottom supporting sentence**: The artist/open-studio identification and the line about seeing works and the making process tie the image to the stated event; the image does not supply an invisible working scene.

### hierarchy — 4

- **thumbnail320 · whole composition**: The blue sculpture occupies the main central field; the large bold title anchors the top and the date/address form a distinct lower block. The reading order and artwork focus survive thumbnail reduction.
- **usage720 · lower information block, y727–863**: Date and address use larger/heavier type than the supporting sentence and reservation URL, making the practical attendance information easy to locate without covering either loop.

### typography — 4

- **native · title at the top and six required copy entries across header/footer**: Hangul syllable forms are intact; all six observed entries match the protected literal strings under the declared normalization. Title weight, subtitle size and footer weights form a consistent sans-serif system.
- **usage720 · date/address and bottom reservation URL**: Date punctuation, the time-range en dash, address comma and contiguous example.org/atelier-afternoon are readable; the URL fits in one line with clear contrast against the light wall.
- **thumbnail320 · two smallest footer lines at the bottom**: The supporting sentence and URL become small at this view, while title, date and address remain identifiable. This limits exceptionally refined small-scale performance, without creating an observed missing glyph.

### space — 4

- **native · left edges of header and footer; wall gaps around artwork**: The header and footer share a left margin of roughly 110–120 px. The complete artwork sits between them with visible wall clearance, and the date begins below its lowest blue edge rather than overlapping it.
- **usage720 · subtitle-to-artwork gap and lower two footer groups**: The modest gap above the large loop and the larger grouping gap before the supporting sentence separate title, artwork and attendance details. The open wall within and to the right of the loops remains part of the photographic composition.

### image_material — 3

- **native · large diagonal blue two-loop artwork, approximately x127–967, y274–1071**: The full recognizable two-loop ribbon form, central crossing, cobalt/ultramarine painted surface, two brass mounts and soft wall shadows remain visible. Its bounding-box proportions closely match A1; no substitute artwork is visible. The position drift is recorded separately.
- **native · complete blue artwork and its two brass wall mounts; compare pinned A1 at the same 1122×1402 canvas size**: The whole artwork is visibly lower and slightly smaller than A1. With the identical blue-pixel criterion B-R>35, B-G>10, B>60, inclusive bounds change from A1 [123,239,975,1048] to poster [127,274,967,1071]: the top moves down 35 px and the bottom down 23 px, while the blue bounds shrink from 853×810 to 841×798. Brass-pixel centroid measurements in the two mount regions also move down about 33 and 25 px. This is a change to the requested wall placement, rather than evidence based only on unequal pixels.
- **native · painted ribbon faces, central overlap and right-loop shadow**: Visible brush variation, dark inner faces, the continuous central crossing and diffuse wall shadows make the local construction coherent. However, the source-preservation requirement remains unfinished because the wall position changed and the work was slightly reduced.

### emotion_control — 4

- **usage720 · blue painted surfaces, warm pale wall and diffuse shadows**: The saturated blue work against the quiet wall and soft light communicates a calm, intimate viewing environment appropriate to an artist open studio.
- **native · plain dark header and compact lower information block**: The restrained black type supports the artwork without introducing a theatrical mood or unrelated imagery. The emotional effect is coherent, though the type treatment is conventional rather than exceptionally specific.

### ai_slop — 4

- **native · entire wall scene and both ribbon loops**: No arbitrary decorative motifs, fabricated tools, faces, logos or unrelated props are visible. The loops, mounting points and shadows remain visually coherent; medium alone is not used as evidence of a defect.
- **usage720 · header, date/address and reservation footer**: The text blocks are clean and consistent, with no visible pseudo-text, duplicated labels or ornamental clutter. The measured placement change is treated as a fidelity issue, without inferring an unobserved production method.

## Residuals

- Preserve the supplied artwork wall placement and scale: the observed top boundary moves down 35 px, with a slight overall reduction.
- The supporting line and reservation URL are small at thumbnail320; the date/address hierarchy is still clear.

## Exact set record

- members: [R7-B05-M1]
- requested_count: 1
- count_fidelity: PASS; observed_count=1; required_count=1; issues=[]
- diversity: null
- not_applicable_reason: single requested image
- Set evidence: thumbnail320, whole composition — one complete requested member is assessed; no cross-member comparison applies.
- set residuals: []
