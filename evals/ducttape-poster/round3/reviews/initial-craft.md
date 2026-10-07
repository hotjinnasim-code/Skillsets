# Blind initial craft, type, and copy review

Reviewed only `blind-initial/cases.json`, `rubric.md`, and all 16 anonymous native, usage, and thumbnail images. Every native was inspected at original resolution; every supplied 720 px usage image and 320 px long-edge thumbnail was also inspected. No author, version, process, skill, or prompt mapping was consulted. Scores are separate judgments, never averaged. A higher AI-slop-prevention score means better control of observable design and synthesis defects, not a claim about authorship.

The strongest craft candidate is **T4**: the dry brush lettering, petal edges, and diagonal branch use a consistent mark system and keep the title readable at the small view. **P1** is the strongest functional product concept because its expanded and collapsed views explain the name and tagline directly. **S5 is the weakest specific poster**: a visually rich botanical corridor dominates its only required message. **C1** is complete and usable but its small supporting copy keeps typography below the high-end floor.

## Mandatory conditions and full copy audit

Native raster sizes, read from the actual image files:

| Case | Quantity and ratio | Result |
|---|---|---|
| Garden | Two independent sets of five alternatives; no quantity or ratio specified in the raw request. All ten are 1024 × 1536. | Ten title-only alternatives inspected. No campaign-unity requirement applied. |
| Coast | C1 1536 × 1024; C2 1024 × 1536. | Exactly two; one exact 3:2 landscape and one exact 2:3 portrait. |
| FOLN | P1 and P2 each 1122 × 1402. | Exactly two portrait images. Visually 4:5; mathematically 1122 × 1402 is not exact 4:5. Ideal height at this width is 1402.5 px, so the difference is ordinary half-pixel raster rounding, not a visible aspect change. If strict integer-ratio compliance is intended, this remains a technical qualification. |
| Moonroll | N1 and N2 each 1254 × 1254. | Exactly two; both exact 1:1. Both use conspicuous extruded 3D title letters, reflective chrome faces/bevels, and strong neon lights and reflections. |

### Garden title-only copy

All ten contain the complete characters of **밤에 피는 정원**, in the correct sequence, with no extra displayed copy. Nine have clear normal word-boundary spacing or line wrapping. S5 needs the qualification below.

| ID | Actual title arrangement | Copy and boundary result |
|---|---|---|
| S1 | 밤에 / 피는 / 정원 | Complete; normal word-boundary line wraps. Flower stems attach to strokes without replacing a required letter. |
| S2 | 밤에 피는 정원 | Complete in one horizontal line; spaces between the three words are clear. |
| S3 | 밤에 / 피는 / 정원 | Complete; normal word-boundary line wraps. |
| S4 | 밤에 피는 / 정원 | Complete; wrap occurs before 정원. |
| S5 | A single vertical column: 밤, 에; gap; 피, 는; gap; 정, 원 | All characters are present and the larger gaps preserve the three linguistic word groups. This reads as vertical typesetting rather than a wrong phrase. However, the rubric expressly permits unrequested **line breaks at word boundaries**, and this arrangement also separates syllables inside each word. Literal boundary compliance is therefore uncertain; do not record an unconditional boundary pass. |
| T1 | 밤에 / 피는 / 정원 | Complete; normal word-boundary line wraps along the central path. |
| T2 | 밤에 피는 정원 | Complete. Expanded syllable tracking is present, but visibly larger spaces still separate the three words. |
| T3 | 밤에 / 피는 / 정원 | Complete; normal word-boundary line wraps. |
| T4 | 밤에 피는 / 정원 | Complete. Brush forms remain recognizable; the angled word positioning does not remove or substitute a syllable. |
| T5 | 밤에 / 피는 / 정원 | Complete; normal word-boundary line wraps. The floral band touches the title region but does not obscure a required character. |

S5's title can be read in the native and at 720 px after locating the center column, but is not reliably recoverable on a quick 320 px first glance. The defect is prominence and practical reading, not an invented missing phrase.

### Coast copy, checked in both originals

“Confirmed” below means the whole phrase, including the number, punctuation, and Korean word groups, is visible. C1 wraps the cancellation sentence after 신청자에게, which is a valid word boundary. C2 keeps it on one line. No required phrase is missing or visibly changed.

| Required phrase | C1 | C2 |
|---|---|---|
| 우리 바다, 함께 줍는 토요일 | Confirmed | Confirmed; wrap after 바다, |
| 하람 해변 정화 참여자 모집 | Confirmed | Confirmed |
| 2026년 11월 21일 토요일 | Confirmed | Confirmed |
| 오전 9시 30분 집결 · 낮 12시 종료 | Confirmed | Confirmed |
| 하람시 물결마당 앞 · 파도길 8 | Confirmed | Confirmed |
| 대상: 만 14세 이상 누구나 · 선착순 40명 | Confirmed | Confirmed |
| 집게와 수거 봉투는 제공됩니다. | Confirmed | Confirmed |
| 개인 장갑, 마실 물, 모자를 준비해 주세요. | Confirmed | Confirmed |
| 우천 시 취소되며 신청자에게 전날 문자로 안내합니다. | Confirmed, two lines | Confirmed |
| 참가비 무료 · 봉사 확인서는 발급하지 않습니다. | Confirmed | Confirmed |
| 11월 18일까지 신청: haram-wave.example/join | Confirmed; dominant bottom banner | Confirmed; dominant bottom banner |
| 문의: 바다정화 운영팀 | Confirmed | Confirmed |

At 720 px, C2's support lines are straightforward to read. C1's right-hand support column is considerably smaller, particularly the preparation, cancellation, and confirmation-certificate lines. I can recover them at that view, but they demand more concentration than the headline and application banner. This is a marginal screen-reading result, not a clean omission or spelling failure. At 320 px both retain the topic and action banner, while supporting policy copy becomes small; the rubric does not require full detail reading at thumbnail size.

### FOLN copy and product constraints, checked in both originals

| Required phrase | P1 | P2 |
|---|---|---|
| FOLN | Confirmed; small upper-left mark | Confirmed; large upper-left mark |
| Fold Cup | Confirmed | Confirmed |
| 가볍게 접고, 다시 펼치다 | Confirmed, including comma and word groups | Confirmed, including comma and word groups |
| 350 mL · 접이식 실리콘 컵 | Confirmed, including mL case and middle dot | Confirmed, including mL case and middle dot |
| 2026.12.01 RELEASE | Confirmed | Confirmed |
| 온라인 사전 주문 11.10–11.30 | Confirmed; decimal dates and visible en dash match | Confirmed; decimal dates and visible en dash match |
| foln.example/store | Confirmed | Confirmed |

Both look like studio product photographs: the surfaces, rim ellipses, local highlights, and contact shadows are coherent. Both cups are handleless, with a dark green matte body and a frosted/translucent white lid. The body shape and matte texture plausibly represent silicone; the image cannot verify the physical material or actual 350 mL capacity. Capacity is correctly stated in the copy. No surface lettering, recognizable actual brand, or actual logo is visible; FOLN appears as the supplied fictional poster text.

P1 makes the folding proposition concrete with an expanded cup above right and a collapsed disk below left. Their top diameters and lid profiles are reasonably compatible under the perspective. P2 shows a single expanded cup; its accordion geometry still signals folding. The visible lid detailing differs across the pair: P1 has a thinner concentric rim with small molded-looking tabs, while P2 has a broader plain frosted skirt. These are observable differences, but the images alone do not establish an impossible product or prove the two geometries identical. For a same-product launch, this leaves a modest identity-control uncertainty, separate from either image's individual finish.

All seven copy lines remain readable at 720 px. Product form and product name survive the 320 px first glance in both. P1 gives the function more immediate visibility; P2 gives the fictional brand more immediate visibility.

### Moonroll copy and requested effects, checked in both originals

| Required phrase | N1 | N2 |
|---|---|---|
| 밤의 활주 | Confirmed in 3D title, including distinct 밤의 / 활주 words | Confirmed in 3D title, including distinct 밤의 / 활주 words |
| 롤러스케이트 나이트 | Confirmed | Confirmed |
| 2026.12.12 · 20:00–23:00 | Confirmed, including time range and separators | Confirmed, including time range and separators |
| 루나 플로어 · 하람시 유성로 19 | Confirmed | Confirmed |
| 입장 15,000원 · 장비 대여 포함 | Confirmed, including comma, 원, and inclusion wording | Confirmed, including comma, 원, and inclusion wording |
| 예약: moonroll.example | Confirmed | Confirmed |

Both satisfy the requested chrome, 3D, and strong neon conditions. N1 uses lime and magenta rails, colored rim reflections, a reflective floor, and visibly thick title extrusion. N2 uses magenta/cyan tubes, mirrorlike chrome title faces, and an intensely reflected rink. These effects were explicitly requested, so their presence is not an automatic slop penalty. The required information is clear at 720 px. At 320 px, the title, roller-skate theme, and reservation line remain identifiable.

N1's visible skate truck and wheel placement are coherent in the oblique crop. N2's toe stops, lacing, wheels, and sole/truck connections are plausible where visible; the rear skate has occluded components. I do not infer a missing wheel from occlusion or claim physically verified manufacturing geometry.

## Separate scores with located evidence

All dimensions use the rubric's 1–5 scale. “Craft” means image/material finish. “Slop control” means observable AI-slop prevention. Each cell gives the visible reason for its score. These are not summed into a rank.

| ID | Subject fit | Typography | Craft/material | Slop control |
|---|---|---|---|---|
| S1 | **5** — Flower stems grow directly out of the giant title's side strokes; the words act as the garden's structure against night purple. | **4** — Three very large word rows preserve Korean blocks and read immediately at 320 px. Broad, uneven character proportions work, though repeated heavy rows give limited rhythm. | **4** — Pale flowers and glyphs share one speckled printed surface; stems have clear connections and clean silhouettes. Grain does not destroy counters. | **4** — The type/flower junctions are content-specific and controlled. The six similar blossoms are repetitive ornaments, but not disconnected clutter or malformed filler. |
| S2 | **4** — The luminous white flower against a nearly black field makes the title's night-blooming image concrete, with a decisive lower-right crop. | **4** — Delicate cream Korean forms occupy the upper-left dark space with intact word gaps; the title remains readable at 320 px, though the image is the stronger first anchor. | **5** — At native scale, cool translucent petal folds, warmer stamens, and darker outer petals show coherent light and depth rather than a uniform glow. | **4** — One botanical subject and one controlled title line avoid ornamental overload. No obvious false microtext or incoherent petal lighting is visible; the photo/title separation is conventional. |
| S3 | **4** — The dark diagonal garden mass and coral blooms share the main composition with a coral title strip; the image and words point into the same field. | **4** — Three brush-rendered word rows are clear at all sizes and have sensible spacing; the title remains a distinct block rather than interacting extensively with the plant forms. | **4** — Gouache-like petal edges, leaf strokes, and the rough diagonal boundary share a consistent painted system. Stem overlaps remain plausible within illustration. | **4** — The brush type and botanical painting have compatible edges, with no fake detail copy. Dense foliage is repetitive but serves the actual garden subject. |
| S4 | **4** — Golden blooming stems traverse the black field; the branch diagonal explains the space around the upper-left title. | **4** — Bold yellow words read quickly and wrap at 정원; the spacing is clear, though the compact top-left title is a fairly conventional counterweight to the branch. | **4** — The black/yellow cut-paper relief has deliberate dark rims, leaf silhouettes, and consistent shallow shadows, visible at native size. | **4** — Limited motifs and a coherent relief language keep the flower centers and stems readable. The decorative branching is controlled rather than a pile of unrelated effects. |
| S5 | **4** — Two botanical banks create a deep blue corridor, a clear garden-space idea; the title occupies the path. | **2** — The only required message is small, muted blue, and syllable-stacked down the center. It is legible after searching at 720 px but nearly disappears at 320 px; boundary interpretation is also qualified. | **4** — The pale leaves, hanging trumpet flowers, and large blooms retain a consistent blue photographic/print vocabulary with intricate native detail. | **3** — Dense fine blossoms and two richly filled edges take priority over the actual message; the tiny title feels placed into an already-complete illustration. This is a content/editing problem, not an authorship diagnosis. |
| T1 | **5** — Flower-filled rectangular beds surround a dark zigzag path, with each title word occupying the path: the composition concretely turns the poster into a garden plan. | **4** — Cream bold words stay intact and readable at 320 px. Their slightly shifted centers follow the path and provide a clear downward reading sequence. | **4** — Painted flower beds, varied cream blossoms, and dark leaves use compatible brush edges and texture; corners and cropping support the bed geometry. | **4** — The path/beds/type relationship is specific and purposeful. Repeated white flowers provide planting rhythm rather than arbitrary stock ornament. |
| T2 | **4** — Pale plant silhouettes gather upward from the lower blue field, preserving a clear open space for the title and a nocturnal botanical mood. | **4** — The full horizontal phrase remains clear at 320 px; larger gaps distinguish words despite wide within-word tracking. The tracking is graceful but less assertive than the plant field. | **4** — Layered pale leaves and dark blue impressions follow a coherent cyanotype-like contrast system; the many stems have readable direction. | **4** — Botanical repetition is consistent and subject-relevant, with no nonsense copy or inconsistent simulated lighting. The treatment remains a familiar flower-field solution. |
| T3 | **4** — A single white trumpet bloom extends diagonally from a stem into dark space, while the title occupies the opposite top corner. The flower's opening supports the phrase clearly. | **4** — Three thin cream word rows have calm spacing and a clean upper-right alignment; full words remain readable at 320 px. The title and photo retain separate roles. | **5** — Papery petal ridges, folded rim highlights, softly shaded throat, and the green calyx form a coherent macro image at native scale. | **4** — The crop uses one subject and meaningful negative space; there is no unnecessary prop/effect package or false fine text. Its photograph-plus-title structure is conventional but controlled. |
| T4 | **5** — The ascending title gesture and descending flowering branch share the same diagonal energy; blooms and the word 정원 frame one another in the night field. | **4** — Recognizable brush forms preserve the whole phrase and word groups. Long terminal sweeps rhyme with leaves and petal tips, but 밤에 requires slightly more attention than the upright alternatives. | **5** — Native petal edges, leaf tips, dry stroke gaps, and lettering all use compatible paint drag on the same dark surface; the pale flowers are modeled without competing special effects. | **5** — The lettering's actual strokes and the botanical marks work together at both large and small scales. No filler text, gratuitous motifs, or conspicuous light/structure confusion is visible. |
| T5 | **4** — Oversized words become the main structure, with a luminous yellow bloom band inserted between 피는 and 정원, making flowering part of the reading sequence. | **4** — All three whole words remain emphatic at 320 px; the oversized block proportions and uneven baselines are legible and intentionally forceful. | **4** — Clean dark-purple glyph edges and simple pale-yellow floral silhouettes make a consistent flat graphic system. Petals and counters remain intact at native size. | **4** — The floral band has a defined role and the surface is controlled; no random textures or fake detail letters are added. It is less structurally intertwined than S1, but not defective for being graphic. |
| C1 | **5** — The gloved hand, grabber, bottle, bag, and shoreline describe the cleanup action directly, while the deadline/URL banner makes participation the endpoint. | **3** — Title and action banner are highly legible, and all copy is correct. The right support column at 720 px is small and tightly packed; important preparation/cancellation conditions take deliberate reading. | **4** — The illustrated tool hinge, bottle, glove, bag facets, and sea layers use a consistent printed-illustration finish. The action is structurally legible, without obvious fused parts. | **4** — Objects are selected for the actual cleanup and copy is real, not decorative microtext. Texture supports the illustration; the main weakness is information scaling rather than indiscriminate embellishment. |
| C2 | **4** — The bottle pickup photo gives a specific cleanup action, and the lower information panel naturally leads to the application bar. The photographic setup is effective but familiar. | **4** — Bold heading, grouped date/time/place, ordinary policy lines, and strong application bar produce a clear order at 720 px. Every phrase and URL remains readable. | **4** — Native glove knitting, grabber joints, crumpled bottle, bag folds, wet pebbles, and surf highlights form a plausible photographic scene with consistent lighting. | **4** — No extra badges or invented slogans compete with the real copy. The three small information icons have clear roles; no prominent anatomical/tool synthesis defect is visible. |
| P1 | **5** — Expanded and collapsed states directly explain “Fold Cup” and “접고, 다시 펼치다”; the two product placements make the folding claim visible without extra copy. | **4** — “Fold Cup” is the first type anchor; the Korean tagline and specification are grouped beneath it, with release/order/URL clearly readable at 720 px. The small FOLN is still identifiable at thumbnail size. | **4** — Matte green accordion folds, two compatible lid ellipses, frosted-white highlights, and grounded shadows look like product photography. Physical capacity/material are not established by appearance. | **4** — The second product state adds meaningful information instead of a spare prop. Blank product surfaces, intact copy, and controlled studio light avoid obvious synthetic filler. |
| P2 | **4** — A single enlarged expanded cup makes the fictional launch and product construction unmistakable; the rings suggest folding but show its action less directly than P1. | **4** — FOLN/Fold Cup establish hierarchy at the top; Korean benefit/spec copy sits beside the cup and the release/order/URL forms a readable bottom group. | **4** — The frosted lid visibly transmits green near its skirt; matte body grain, fold joints, base contact, and soft side shadow are plausible at native scale. | **4** — One product, complete text, and a controlled light field prevent ornamental overload. No surface lettering or visibly impossible handle/rim is introduced; cross-poster lid identity remains qualified. |
| N1 | **5** — The title lies along the diagonal skating lane and a cropped moving skate points through the same space; chrome type, neon rails, and the action share one spatial idea. | **4** — The Korean 3D blocks remain readable despite perspective; subtitle/date sit in a quiet top-left region and location/price/reservation in a quiet lower-left region. The full reservation is prominent. | **4** — Reflective bevels, colored edge highlights, floor sheen, wheel translucency, and the visible truck connect convincingly. Strong highlights sometimes flatten face detail, but do not erase the letters. | **4** — The requested effects are tied to the title and skating space, not pasted as unrelated icons. No fake fine copy or obvious wheel/tool structure error is visible; the reflective floor carries some broadly decorative streaking. |
| N2 | **4** — The chrome title, neon rink, and pair of quad skates make the night event immediate. This is a familiar frontal event arrangement, but it fulfills the explicit effect brief. | **4** — Large Korean title and subtitle dominate, with a clear lower-right four-line event/reservation group at 720 px. The line above reservation separates action from details. | **4** — Extruded chrome edges and pink/cyan reflections are coherent; skate laces, stops, trucks, wheels, and floor contact remain plausible where visible, with some rear components occluded. | **4** — Highly saturated chrome/neon is authorized and organized. The required letters and real event copy remain intact, and no extra visual gimmicks are needed to identify the subject. |

## Garden set preference, diversity, and uncertainty

**Preference: T, with moderate confidence.** T1's bed/path structure and T4's unified brush gesture are the most persuasive alternative concepts for the title. T3 has refined macro finish, T5 has a forceful graphic title, and T2 supplies a softer blue botanical direction. All five keep the required message readable in the 320 px first glance. S has strong S1, S2, S3, and S4 alternatives, but S5 loses the title's practical prominence and complicates the boundary check.

This preference does not mean that a photographic, cyanotype, cut-paper, minimal, or heavily lettered style is intrinsically superior. S4's black/yellow relief is a genuine direction unavailable in T; S1's literal floral growth from letters is more integrated than T5's floral band. A preference for paper relief or monumental print lettering could reasonably move the choice toward S. Nothing in the title-only raw request specifies a single intended emotional register, audience, or venue, so that part of preference is uncertain.

| Set | Diversity score | Located structural evidence |
|---|---|---|
| S | **5** | S1 makes giant letters into the plant support; S2 uses one macro flower and a small horizontal heading; S3 divides the page into a title strip and a painted garden wedge; S4 uses dimensional black/yellow relief; S5 uses a botanical corridor and a vertical title. These differ in type role, image mode, and spatial structure rather than color alone. S5's weakness does not erase the existence of that distinct direction. |
| T | **5** | T1 places words in paths between garden beds; T2 uses horizontal thin type over a rising blue plant field; T3 uses a diagonal macro flower with a word stack opposite; T4 interlocks brush gestures with a diagonal branch; T5 makes nearly full-page block lettering the main form. The differences survive removal of the color choices. |

These are independent alternatives, so neither set loses points for lacking campaign consistency. The raw garden request does not require photographic botanical identification or a verified list of night-blooming species; I do not add that condition retrospectively.

## Weakest result and cause-specific repair

**S5:** The failure is the allocation of attention. Nearly the full two side banks are bright, highly detailed botanical material, while the only message is a very small low-contrast vertical center column. At 320 px, the garden corridor arrives before any usable title; at 720 px, the viewer must search for the wording. This is not fixed by merely adding texture, sharpening the flowers, or changing the blue.

Keep the blue botanical corridor, but give its title a substantially larger, high-contrast presence in that corridor. Use three whole-word rows **밤에 / 피는 / 정원**, or a sufficiently large single horizontal phrase, so normal Korean word boundaries are unambiguous. Move or reduce some inner branches if needed to give the letters an actual margin. Verify the exact title at native size, its easy reading at 720 px, and its first-glance recognition at 320 px. This addresses both message prominence and the literal line-boundary uncertainty without discarding the legitimate visual direction.

**C1 secondary repair:** Increase the smallest right-hand policy text by reallocating a little space from the image or overly tall action/title bands, and widen the support column or use clearer vertical grouping. Preserve the already-strong deadline/URL banner and every exact policy phrase. The repair is information scaling, not a new illustration or effect package.

**P1/P2 production qualification:** If exact 4:5 raster arithmetic is required, output dimensions divisible into that ratio. If the pair is presented as one precise product model, reconcile the visible lid skirt/tab detail before treating geometric consistency as established.

## Scoped high-end floor signal

On this review's four requested dimensions, **S1–S4, T1–T5, C2, P1, P2, N1, and N2** have visible 4–5 evidence in each dimension. **S5 does not**: typography is 2 and slop control is 3. **C1 does not**: typography is 3 despite excellent topic/action fit. Both garden sets show structural diversity at 5, assessed independently.

T4 is the clearest craft candidate; P1 is the clearest product/function candidate; N1 is the strongest integration of the explicitly required 3D/chrome/neon style into the skating action. Their strengths do not establish a universal high-end success rate. Mandatory copy is visually complete throughout, but S5's syllable-stack boundary compliance and P1/P2's mathematically approximate ratio remain explicitly qualified. Product capacity, physical material, exact manufacturing geometry, and printing suitability are not proved by these images. The small test does not certify all requests, and another independent evaluator may reasonably assign a neighboring score to the conventional-but-controlled layouts.
