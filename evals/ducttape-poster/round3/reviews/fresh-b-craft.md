# Blind B — independent craft review

## Scope and actual inspection

I used only `blind-b/README.md`, `cases.json`, `rubric.md`, `native-metadata.json`, and the images in `native/`, `usage/`, and `thumb/`. I did not inspect mappings, production sources, prompts, skill versions, production notes, prior reports, or other reviewers. No image generation or production-image edits were performed.

All 11 images were individually viewed at all three supplied sizes, not substituted with a collage: **33 complete image views**. Native PNG dimensions were also read directly and agreed with the supplied metadata.

| Images actually viewed | Native | Usage | Thumbnail |
|---|---:|---:|---:|
| H1, H2, H3, H4, H5 — each individually | 1024 × 1536 | 720 × 1080 | 213 × 320 |
| K1 | 1536 × 1024 | 720 × 480 | 320 × 213 |
| K2 | 1024 × 1536 | 720 × 1080 | 213 × 320 |
| R1, R2 — each individually | 1122 × 1402 | 720 × 900 | 256 × 320 |
| W1, W2 — each individually | 1254 × 1254 | 720 × 720 | 320 × 320 |

Additional actual native-pixel inspections used nearest-neighbor enlargement of these regions, without altering the native files: R1 date line `(365,1235)–(651,1305)`; R2 date line `(378,1240)–(647,1305)`; W1 time range `(624,771)–(929,827)`; W2 punctuation `(328,961)–(755,1008)`; W2 skate truck/toe stop `(446,637)–(905,904)`; K2 tong/bottle contacts `(543,343)–(727,580)`. An initial combined crop output was truncated; the listed regions were subsequently inspected successfully as individual images. Scores below use the full native, usage, and thumbnail views as well as these successful close views.

## Mandatory checks — pass, fail, and uncertainty kept separate

**Visible pass:** counts, ratios, requested subjects, explicit product appearance, and explicit chrome/neon/3D requirements are satisfied. No definite omitted, added, substituted, or misspelled copy was found. All specified information is readable in the supplied 720-pixel-wide usage views. The very small policy and URL text at 320 pixels is not treated as a mandatory failure; that size is the rubric's first-glance test.

**Definite mandatory failure:** none observed.

**Uncertainty:** native raster pixels do not establish the Unicode codepoint of a short horizontal range dash. The R1/R2 `11.10–11.30` and W1/W2 `20:00–23:00` ranges visibly have a centered horizontal range mark, correct numbers, and no visible spaces around it. Close inspection did not establish a definite hyphen-versus-en-dash error. W2's middle separators and both colon dots are square-shaped in the chosen type; this is a visible typographic choice, not sufficient evidence of replacing `·` with a different codepoint. I therefore record visible-copy passes with these limited source-character uncertainties, rather than invent a definite error. This is not a blanket uncertainty about otherwise clearly read Korean words, dates, English names, or URLs.

| Image(s) | Required count / ratio / style and subject | Result |
|---|---|---|
| H1–H5 | Five supplied title-only posters; each 2:3; only `밤에 피는 정원` | Pass. All five show precisely the requested readable title and no other visible copy. Ratio = 0.6666667, relative error 0%. |
| K1 | Landscape 3:2 cleanup recruitment; deadline and address easy to find | Pass. Ratio = 1.5, relative error 0%. Yellow bottom strip makes deadline/address especially prominent. |
| K2 | Portrait 2:3 cleanup recruitment; deadline and address easy to find | Pass. Ratio = 0.6666667, relative error 0%. Green bottom strip gives both a clear, readable action location. |
| R1, R2 | Two portrait 4:5 posters; photograph-like handleless cup; dark green silicone body; translucent white lid; no real brand/logo or lettering on product | Visible pass. Both bodies are dark green and matte, both lids are translucent white, both cups are handleless, and product surfaces have no visible text/logo. Actual ratio = 1122/1402 = 0.8002853; relative error from 4:5 = **0.03566%**, within the specified 1% tolerance. `350 mL` appears as requested; the image cannot verify real internal capacity. Named FOLN is the requested fictional poster name. |
| W1, W2 | Two square 1:1 night-event posters; title in 3D; reflective chrome and strong neon in both | Pass. Both have square dimensions, deep extruded Korean title forms, reflective metallic faces, and strong cyan/magenta illumination. These expressly requested effects are not a style violation. |

### Exhaustive visible-copy comparison

`P` = present and visually matches in the native and readable in the 720-pixel usage view. `P/U` = visible match with the limited Unicode uncertainty described above. The table tests the complete requested phrase, including readable punctuation, digits, capitalization, and URL spelling. No extra caption, fake small print, or unrequested display copy was observed.

| Garden copy | H1 | H2 | H3 | H4 | H5 |
|---|:---:|:---:|:---:|:---:|:---:|
| 밤에 피는 정원 | P | P | P | P | P |

| Cleanup copy | K1 | K2 |
|---|:---:|:---:|
| 우리 바다, 함께 줍는 토요일 | P | P |
| 하람 해변 정화 참여자 모집 | P | P |
| 2026년 11월 21일 토요일 | P | P |
| 오전 9시 30분 집결 · 낮 12시 종료 | P | P |
| 하람시 물결마당 앞 · 파도길 8 | P | P |
| 대상: 만 14세 이상 누구나 · 선착순 40명 | P | P |
| 집게와 수거 봉투는 제공됩니다. | P | P |
| 개인 장갑, 마실 물, 모자를 준비해 주세요. | P | P |
| 우천 시 취소되며 신청자에게 전날 문자로 안내합니다. | P | P |
| 참가비 무료 · 봉사 확인서는 발급하지 않습니다. | P | P |
| 11월 18일까지 신청: haram-wave.example/join | P | P |
| 문의: 바다정화 운영팀 | P | P |

| Product copy | R1 | R2 |
|---|:---:|:---:|
| FOLN | P | P |
| Fold Cup | P | P |
| 가볍게 접고, 다시 펼치다 | P | P |
| 350 mL · 접이식 실리콘 컵 | P | P |
| 2026.12.01 RELEASE | P | P |
| 온라인 사전 주문 11.10–11.30 | P/U | P/U |
| foln.example/store | P | P |

| Night-event copy | W1 | W2 |
|---|:---:|:---:|
| 밤의 활주 | P | P |
| 롤러스케이트 나이트 | P | P |
| 2026.12.12 · 20:00–23:00 | P/U | P/U |
| 루나 플로어 · 하람시 유성로 19 | P | P/U |
| 입장 15,000원 · 장비 대여 포함 | P | P/U |
| 예약: moonroll.example | P | P |

## Per-image scores

The rubric's 1–5 scale is used directly: 3 = functioning; 5 = exceptionally resolved. There is **no total or average**. C = content/form; H = information hierarchy; T = typography; S = space; F = image/material finish; E = emotion/control; A = resistance to generic or defective AI-slop traces. A is not an authorship judgment.

| Image | C | H | T | S | F | E | A |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| H2 | 4 | 3 | 3 | 4 | 4 | 4 | 4 |
| H3 | 4 | 4 | 3 | 4 | 4 | 4 | 4 |
| H4 | 3 | 4 | 4 | 4 | 4 | 3 | 3 |
| H5 | 5 | 4 | 4 | 5 | 4 | 4 | 4 |
| K1 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| K2 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| R1 | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| R2 | 4 | 4 | 4 | 4 | 4 | 4 | 3 |
| W1 | 4 | 4 | 4 | 4 | 4 | 5 | 4 |
| W2 | 3 | 4 | 4 | 4 | 4 | 4 | 3 |

### H1

- **C4:** The central climbing stem rises from visible soil into the title and three open white trumpets. The letters and vine share a growth structure; the pale blooms against navy support the night subject.
- **H4:** At 320 pixels the broad title in the upper-middle arrives before the fine botanical detail. There is only one requested message, and it remains unambiguous at 720 pixels.
- **T4:** Uneven rounded cream terminals and generous word gaps remain clear while curling stems pass behind and around the letter groups. Counterspaces in `밤`, `정`, and `원` remain open.
- **S4:** Upper blooms balance left and right of the title, and the narrow lower stem preserves large lateral dark areas. The compact soil footing anchors the unusually tall plant. The title fills almost the whole width without being clipped.
- **F4:** Petal folds, heart-shaped leaf veins, buds, and soil use a coherent fine illustrative rendering. The main stem and bloom bases visibly connect; this is not a bouquet of detached cutouts.
- **E4:** Cream/navy and a restrained number of blooms create quiet nocturnal growth. Tendril curls decorate the title but do not overwhelm it.
- **A4:** The title/vine interaction is specific enough to avoid a bare stock-flower overlay. The botanical vocabulary is familiar, and the soil is very busy at native size, but no pseudo-text or conspicuous broken structure was found.

### H2

- **C4:** The enormous foreground trumpet and receding smaller blooms give the impression of entering an actual dark garden. The black opening in the vegetation is used for the title rather than adding a separate panel.
- **H3:** At thumbnail size the foreground flower wins the first glance; the small central title is secondary. Its contrast and clean negative area make it readable at usage size, but it does not carry the poster as strongly as H1/H5.
- **T3:** The regular light sans line in the central opening is clean and correctly spaced, yet mostly functions as a caption placed on the photograph. Its proportions and rhythm do little with the large petal sweep surrounding it.
- **S4:** The left/bottom bloom crop establishes near/far depth, the right-edge bloom balances that weight, and the central dark area has a deliberate role. No accidental crop through title glyphs occurs.
- **F4:** Fine translucent petal ridges, textured leaves, soft distant blooms, and consistent dark illumination support the photograph-like system. The foreground flower's throat and stamens remain plausible.
- **E4:** Dark foliage, subdued white petals, and the empty central opening keep a controlled night mood without unrelated sparkles or scenic accessories.
- **A4:** The image uses subject-specific macro depth rather than a generic decorative effects bundle. The result still resembles a photographic garden caption; that limits its typographic ambition, not its visible authenticity or origin.

### H3

- **C4:** Revealing three root systems beneath the night flowers supplies a more specific idea than flowers alone. The title occupies the underground zone, linking the garden's visible and hidden structures.
- **H4:** The large upper bloom is the image focus, followed by the bold cream lower title. At 320 pixels the title remains strong despite the dense roots behind it.
- **T3:** Heavy uniform sans glyphs read decisively, but the single broad line mainly overlays the root drawing. The root columns and title spacing do not develop a comparably tailored typographic rhythm; some intricate central roots are simply obscured.
- **S4:** Three unequal flower heights form a convincing triangle. The horizontal soil level and three branching root masses establish clear above/below zones and keep the lower title from floating arbitrarily.
- **F4:** Fine petal contours, veins, bud sheaths, crowns, and branching roots share a consistent engraving-like vocabulary. Root crowns visibly continue into the stalks. The more granular soil is a somewhat heavier texture, but not a structural failure.
- **E4:** Bone-colored linework and near-black ground produce a controlled nocturnal, specimen-like atmosphere. The light outlines emphasize bloom forms rather than indiscriminate glow.
- **A4:** The underground view and continuous root structure are meaningful subject choices. Uniform root intricacy and familiar specimen symmetry remain, but there is no fake labeling or detached botanical body.

### H4

- **C3:** The title above cream flowers clearly conveys a garden. The night idea is carried principally by the navy background; the front-facing, uniformly bright assorted blooms do not make the main decisions feel as specific as H1's climbing structure or H5's path.
- **H4:** The large upper title has immediate contrast at 320 pixels, followed by the prominent central flower. The title-only brief stays simple and readable at 720 pixels.
- **T4:** The rounded display strokes, open counters, even visual word spacing, and wide title placement work comfortably with the broad petal shapes. There is no awkward Korean character construction.
- **S4:** Tall central and left flowers, a large right flower, and smaller lower flowers make a balanced rising garden mass. The top field gives the title enough air, while the bottom-edge foliage crop feels deliberate.
- **F4:** Flat green leaf planes, fine vein lines, cream petal folds, and navy/yellow stamens share a consistent illustrative finish. Visible stem/calyx attachments are sufficient. The dense lower leaves become a pattern rather than a clearly layered spatial garden, which keeps this below 5.
- **E3:** The regular bright flower display is pleasant and controlled, but relatively neutral. Beyond the background color, few local choices make a particular night atmosphere or opening-bloom moment.
- **A3:** The lower foliage carpet, evenly scattered pale flowers, and recurring blue stamen bundles resemble a broadly reusable botanical-print arrangement. This is a content-specificity limitation; flat illustration itself is not being penalized and no counterfeit microcopy is present.

### H5

- **C5:** The winding path makes the viewer move through the garden. Its central broad bend becomes the title's actual place, so the headline, negative space, crop, and planting arrangement all follow the same idea.
- **H4:** At 320 pixels the pale S-shaped path and dark title are immediately distinguishable. Smaller blossoms become texture at that scale, while the full title remains comfortably readable at 720 pixels.
- **T4:** The dark rounded title takes a slight directional tilt within the path bend. It is sized to the walk's width without colliding with planting edges. Its letters retain clean counters and do not imitate an unreadable painted-ground perspective.
- **S5:** The path enters below, expands at the text, and leaves toward the upper right. Large dark leaf masses in the upper left and lower right balance the pale path. Cropping the garden on every edge convincingly suggests a larger place.
- **F4:** Leaf clusters, varied pale blossoms, dark layered planting, and the softly textured lavender path use a coherent painted system. Small repeated flower marks are visible natively, but do not become malformed pseudo-detail.
- **E4:** Cool foliage and selective cream blooms create a quiet night walk, with sufficient contrast for the path and text. The planting stays subordinate to the route.
- **A4:** The image gives the title a subject-specific spatial role rather than simply adding it over flowers. Decorative cluster repetition is still visible, so this is not a defect-free 5.

### K1

- **C4:** A gloved hand and tongs lift a crushed bottle above an open collection bag beside the shoreline. This explicitly illustrates the requested action and supplied equipment rather than a general marine landscape.
- **H4:** Title and recruitment line lead at upper left; event details form a readable left column; the high-contrast yellow deadline/URL strip is the clearest action target. At 320 pixels the action strip still separates from the body. Policies are readable at 720 pixels.
- **T4:** Strong navy sans type, consistent left starts, sensible size steps, and a single large URL line withstand the dense copy. The heaviest headline is tightly packed, particularly around `함께 줍는`, but the glyphs and word boundaries remain readable.
- **S4:** The diagonal shore separates a broad text field from the right-side action illustration. The bottle and bag meet over the strip without cutting into the longest body line; the footer spans the width as a stable terminus.
- **F4:** Foam, sand, glove knit, metal shafts, transparent crushed bottle, and faceted bag are differentiated within one illustrated style. The tongs visibly touch the bottle, and the hand encloses the handle. The bag's lower support is cropped by the footer, not visibly absent.
- **E4:** Bright water and the yellow action strip support approachable participation and clear urgency. No extra slogan, unrelated sea mascot, or visual celebration distracts from the request.
- **A4:** The actual pickup gesture and handled material give the illustration a role. There is no fake fine print, anomalous lettering, or obvious unconnected tool. It remains a fairly conventional recruitment layout, which affects pair diversity separately.

### K2

- **C4:** The real-looking dirty bottle, gloved hand, tongs, and bag enact the cleanup. Daylight beach context is specific and understandable without reading the complete body copy.
- **H4:** The upper sky carries the title; date/time head the cream body area; the green footer clearly groups deadline, URL, and inquiry. At 720 pixels all policies and the complete URL remain comfortably readable.
- **T4:** The upper heavy green title and lower black/white text use a clean, consistent sans system. Dates receive a useful size/weight step. Long Korean policy lines remain intact and do not collide with the right edge.
- **S4:** The diagonal tool connects upper-right hand to center bottle and lower bag. The sky allows the headline to breathe; the split between picture, details, and action block is clear. This is orderly but conventional.
- **F4:** Glove knit, silver shafts, dirt-speckled crushed plastic, bag folds, shallow water, and distant rock depth are differentiated. A close view confirms two visible tong contacts at the bottle neck/body; the asymmetric tip shapes are not enough to declare the tool impossible.
- **E4:** The bright shore and clean information panel make participation approachable. The hand demonstrates the activity while the green footer supplies an appropriately firm action cue.
- **A4:** No pseudo-type or unmistakable contact failure was found. The image and information have a useful subject-specific relationship; the stock-like beach-photo framing remains a limit on originality and on this pair's diversity.

### R1

- **C5:** A hand presses the lid of the expanded cup while a compact cup sits behind it. The dominant image visibly stages the fold action promised by `가볍게 접고, 다시 펼치다`, making the photograph serve the claim rather than only display a product.
- **H4:** Brand/name at upper right, pressing gesture at center-left, large slogan below, then capacity/release/order/URL form a clear sequence. The thumbnail communicates brand and folding gesture; the full information is readable at 720 pixels.
- **T4:** English brand proportions, heavier Korean slogan, medium specification line, and enlarged release date distinguish roles with consistent dark-green type. The lower information block has clear left alignment and the URL remains legible.
- **S4:** The entering forearm and horizontal hand balance the upper-right brand, while the small compact cup fills the right middle without competing with the hero. The product's grounding shadow separates it from the information field.
- **F4:** Matte fine-grained green silicone, translucent white lid edges, skin/nail detail, and table contact shadows are coherent. Thumb/fingers visibly touch the lid. The expanded/compact forms have different visible fold arrangements; a static image does not fully prove how every ring nests, but I found no definite impossible construction.
- **E4:** The gray studio and green type keep attention on a tactile action. Skin warmth gives scale and contact without adding unrelated lifestyle props.
- **A4:** The demonstrative hand gives this packshot a distinct role. There are no surface logos, pseudo-labels, extra handles, obvious floating contacts, or malformed visible fingers. Familiar gray studio styling remains below a 5.

### R2

- **C4:** Standing and compact forms side by side plainly explain the folding product. This is an effective catalog demonstration, though less specific than R1's active pressure gesture.
- **H4:** Oversized FOLN/Fold Cup leads, the slogan follows, products occupy the center, and specifications/date/order/URL share the bottom. Every lower line is readable at 720 pixels; the thumbnail retains brand and the two-state comparison.
- **T4:** Broad heavy English and Korean display text is proportionate to the two cup silhouettes. Capacity and URL use a smaller readable size, while the release date remains emphatic. The left alignment and margins are consistent.
- **S4:** Similar lid widths connect the two states, while unequal height produces an understandable comparison. Both bases have grounding shadows on the same gray table. The tall headline occupies a large share of the top, but does not overlap the product.
- **F4:** Tapered folds, matte silicone grain, translucent lids, smooth rim ellipses, and soft tabletop shadows are coherent. The low compact form visibly retains layered rings. No handle, product text, or obviously disconnected lid is present.
- **E4:** The controlled neutral setting and green typography suit a practical small object. Restraint is effective here, but is not itself evidence of exceptional craft.
- **A3:** Two product states on a gray studio plane below a huge sans name constitute a widely reusable catalog package. Clean surfaces and correct-looking structure avoid conspicuous synthetic errors, but this alternative contributes little distinct editorial specificity beyond the product type.

### W1

- **C4:** A circular rink boundary, two worn skates entering at upper left, and a title resting within the ring connect the event to movement and an actual skating place. The requested chrome is part of that spatial idea.
- **H4:** The chrome title dominates at 320 pixels, followed by the white subtitle and grouped details below it. Date, location, price, and reservation are readable at 720 pixels against dark floor.
- **T4:** Korean title blocks remain legible despite deep bevels and extrusion; `밤`, `의`, `활`, and `주` retain correct distinguishable structures. Flat white support type avoids reflective-detail interference and has coherent line grouping.
- **S4:** The ring frames both title and information; upper-left feet introduce asymmetry and movement. Extruded letter bases have visible dark/contact zones, and the large open floor above the title gives the skates room.
- **F4:** Cyan/pink edge reflections, reflective silver faces, worn floor line/scratches, boots, laces, wheels, and light-tube brackets are coherent. Multiple wheels and floor reflections are visible; no definite wheel or boot-contact failure was found.
- **E5:** The circular boundary and opposing neon colors produce a concentrated energetic night mood. The few small metallic glints have a plausible role rather than becoming a scatter of gratuitous sparkle props.
- **A4:** The rink circle, actual feet, and physical title grounding make the required neon/chrome specific to skating. The cyan/magenta vocabulary is familiar, but that alone is not a defect. No counterfeit small copy is present.

### W2

- **C3:** A single pristine skate on a neon corridor clearly identifies roller skating, but the overall composition resembles a skate product advertisement more than a particular shared night event. The required copy supplies most of the event meaning.
- **H4:** Huge chrome title, white subtitle, central skate, and a dark footer make an obvious sequence. Details are stronger than in many spectacle posters and remain readable at 720 pixels.
- **T4:** Chrome Hangul forms are correctly structured with visible counters and consistent depth. The lower heavy white sans text is clean and aligned. Square colon/middle-dot shapes are consistent punctuation styling; their codepoints remain uncertain as recorded above.
- **S4:** Symmetric rails and converging floor reflections center the skate, while the full-width footer cleanly carries logistics. The title/subtitle/skate are tightly stacked in the upper three quarters, but no letter or boot is accidentally clipped.
- **F4:** Seams, eyelets, laces, reflective trucks, wheels, toe stop, chrome bevels, and neon reflections remain coherent on close inspection. **The fourth wheel is partly occluded behind the front assembly and toe stop; it is not missing.** The toe stop has a visible mount and sits above the wheel contact plane, so I do not claim it is unsupported or impossible.
- **E4:** Strong pink/cyan lighting delivers the expressly requested night spectacle. It is controlled around title, rails, and skate, though the empty corridor has less lived event energy than W1's feet and rink.
- **A3:** Giant chrome header + symmetric neon tunnel + pristine centered object is a familiar effects package. The limitation is that these choices remain broadly transferable to other product/event subjects, not that neon/chrome is automatically forbidden. No definite fake microtext or severe structural glitch was found.

## Set diversity

| Set | Score | Concrete differences and remaining habit |
|---|---:|---|
| Garden H1–H5 | **4** | H1 makes the vine surround the title; H2 uses macro photographic depth with a small caption in a vegetation opening; H3 reveals roots and places text underground; H4 stacks display title above flat flowers; H5 makes an overhead S-path carry the title. These are genuine compositional/typographic roles, not just recolors. H1/H4/H5 still share rounded display lettering and the whole set repeatedly favors pale flowers against dark cool foliage. |
| Cleanup K1/K2 | **3** | Illustration versus photograph is a real image-language change; the landscape text/side-picture arrangement differs from the portrait picture/body stack. Both still use a hand entering upper right, diagonal tongs, crushed bottle over white bag, top-left title, and a full-width action strip. The alternative thinking is distinguishable but retains the same stock gesture and reading skeleton. |
| Product R1/R2 | **3** | R1's hand gives the photograph an action; R2's two static silhouettes give a catalog comparison. Brand position changes. Both retain the same gray table/background, dark-green sans typography, expanded/compact pair, and bottom release/order block. The hand is more than a surface change, but the pair does not establish two fully different design systems. |
| Night W1/W2 | **3** | W1 is an oblique circular rink with feet and a title seated on the floor; W2 is a frontal corridor with a pristine isolated skate and an upright top header. The contact/perspective roles differ. Both repeat the same chrome letter vocabulary, pink/cyan illumination, highly scratched glossy floor, and centered white support type. |

**Complete-production diversity: 3.** This is not an average of the row scores. The garden case supplies several substantial alternative mechanisms, while the three two-image cases retain clear structural habits. Changing subjects across briefs is not counted as evidence of independent alternatives within a brief.

## Strongest, weakest, and smallest useful repairs

**Strongest overall single image: H5.** Its path makes content, type location, negative space, and crop work as one idea. The 4–5 evidence for content, typography, finish, and slop resistance is specifically documented above; it also visibly passes its title-only and ratio requirements. **Strongest demonstration for an information-bearing brief: R1**, because the pressing hand makes the folding claim concrete while retaining all required readable information. R1's range-dash Unicode uncertainty remains open.

**Weakest single image: H4.** It is readable and coherent and passes its mandatory requirements, but its assorted uniformly bright blooms make the night idea and specific composition less developed than its lettering and clean edges. W2 is also weaker in content specificity and generic-package resistance despite satisfying the expressly requested spectacle. These weaknesses are not cancelled by H5/R1 or by any average.

Smallest cause-specific repairs, if another iteration is wanted:

- **H2:** Increase the central title modestly or tune its proportions to the central opening/petal sweep. The current regular small line works as a caption; a full photo replacement is unnecessary.
- **H3:** Retune title width/spacing against the three root columns, or clear a narrower title band in the root drawing. Preserve the underground idea rather than adding more decorative texture.
- **H4:** Let the existing central opening bloom determine a more selective nocturnal emphasis, and subordinate one competing lower bloom. This would make `밤에` affect local focus and brightness, instead of only the navy field. No repair is needed for flat illustration as a style.
- **R2:** To strengthen this alternative, use the already shown height difference as the governing comparison in type/space instead of the same oversized-brand/gray-packshot skeleton. Keep the required copy and product appearance; adding props would not address the actual limitation.
- **W2:** To strengthen event meaning with a small image-level change, introduce an actual skating/contact gesture in the existing central scene or change the skate's role from display object to evidence of use. Do not remove required chrome/neon, and do not "fix" a supposedly missing wheel: the close inspection resolved that concern.
- **Exact-copy assurance for R1/R2/W1/W2:** If editable text exists, verify only the uncertain range dash and W2 separator codepoints against the supplied strings. Recompose just those characters if necessary. The raster review does not justify regenerating entire posters or asserting that they are definitely wrong.
- **Pair diversity:** Further surface variations would not resolve the repeated hand/tong/bag composition, gray cup pair, or neon corridor package. Change one alternative's governing image/type role within each pair, keeping its required information and ratios.

The rubric's higher-end signal is supported for some individual images, especially H5 and R1, but **the complete production does not cleanly clear that bar**: complete-production diversity is 3, and H2/H3/H4/R2/W2 have the concrete lower-scored dimensions recorded above. This review evaluates these visible outputs at these sizes. It does not identify human versus machine authorship, certify print suitability, prove product volume, or establish future success rates for other requests.
