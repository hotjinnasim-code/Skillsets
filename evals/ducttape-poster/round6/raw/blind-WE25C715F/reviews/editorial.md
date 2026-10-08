# Editorial review

Reviewer: editorial. Order compliant: true.

## Method

Manual visual transcription from exact provided image paths. Read review-protocol.md and preflight.json first; actually opened all five preflight usage720 images with view_image(detail="original"), saved reviews/editorial-action-first.json, and read that saved file back before opening packet.json or full supplied copy. That first record is preserved unchanged. After reading the full request/copy/conditions, actually opened each of the five packet images at native, usage720, and thumbnail320 with view_image(detail="original"): fifteen packet-stage calls, recorded below. Read every full supplied string manually from usage720 pixels and cross-checked the native views; observed strings retain visually read punctuation and spacing, with wrapped lines joined for the single-string schema. Equality ignores whitespace only and preserves case and punctuation. Thumbnail views were actually inspected; small-word/punctuation limitations are recorded per image and do not substitute for usage720 readings. The viewer accepted original detail for every call; no tool error or missing view occurred. Provided thumbnail320 files have 320-pixel maximum height/extent, yielding widths of 213, 256, or 320 pixels, rather than all being 320 pixels wide. PNG headers were read only to verify dimensions/ratios, not for text extraction. No OCR, cropped/resized substitutes, web, connectors, agents, other review files, or image edits were used. Only the three editorial review files were created. No claim is made about authorship, actual physical mechanics, capacity, or print performance. Seven dimensions are assessed separately without a total or average; bright color and 3D are assessed by execution and relevance, not prohibited by genre. closest_pair.score uses the diversity scale (1=repetition, 5=strongly distinct), applied to the nearest two members.

## Actual packet-stage image views

| Image | View | Exact path |
| --- | --- | --- |
| X1059 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X1059-native.png |
| X1059 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X1059-usage720.png |
| X1059 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X1059-thumbnail320.png |
| X7358 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X7358-native.png |
| X7358 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X7358-usage720.png |
| X7358 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X7358-thumbnail320.png |
| X3429 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3429-native.png |
| X3429 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3429-usage720.png |
| X3429 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3429-thumbnail320.png |
| X3882 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3882-native.png |
| X3882 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3882-usage720.png |
| X3882 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3882-thumbnail320.png |
| X3815 | native | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3815-native.png |
| X3815 | usage720 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3815-usage720.png |
| X3815 | thumbnail320 | /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/blind-WE25C715F/images/X3815-thumbnail320.png |

The five earlier usage720 calls and unchanged first readings are in `editorial-action-first.json`.

## X1059

Mandatory pass: true. Issues: [] (no mandatory failure observed).

All required copy legible at720: true.

All ten supplied strings were manually readable at 720×900, including the entire exclusion, two-line response sentence, and URL through “&slot=pm”. Preparation is enlarged at middle-left; the language/exclusion/eligibility block is smaller but clear. At 256×320, title, preparation, deadline, and URL remain prominent; fine punctuation in the smaller explanatory lines is less dependable than at usage720. Native 1122×1402 gives a 4:5 relative ratio error of about 0.0357%, within 1%. No omitted required string, altered non-whitespace punctuation/case, unrequested wording, or QR code was observed.

### Uncertainties

- Fine punctuation in the smaller explanatory lines is not independently dependable at the 256×320 thumbnail; no unresolved usage720 copy ambiguity was observed.

### Full manual transcription

| Exact required string | Observed string | Equal after whitespace normalization only |
| --- | --- | --- |
| 이름 바꾸는 물건들 | 이름 바꾸는 물건들 | true |
| OBJECT NAME EXCHANGE | OBJECT NAME EXCHANGE | true |
| 2026.11.21(토) 13:30–16:00 | 2026.11.21(토) 13:30–16:00 | true |
| 가상 공간 여울실험실 2층 / YEOUL LAB | 가상 공간 여울실험실 2층 / YEOUL LAB | true |
| 한국어·English, 어느 언어로 적어도 좋아요. | 한국어 · English, 어느 언어로 적어도 좋아요. | true |
| 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | true |
| 깨지기 쉬운 물건과 음식은 받지 않아요. | 깨지기 쉬운 물건과 음식은 받지 않아요. | true |
| 만 16세 이상 · 무료 · 24명 | 만 16세 이상 · 무료 · 24명 | true |
| 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | true |
| yeoul.example/NAME?lang=ko&slot=pm | yeoul.example/NAME?lang=ko&slot=pm | true |

### Separate scores and located evidence

| Dimension | Integer score (1–5) | Visible evidence |
| --- | --- | --- |
| content_form | 4 | At usage720, the blank paper tag and wooden peg at the right of the enlarged bring-one-object sentence connect naming to an ordinary small item. The rust-red cord also frames the lower instructions. This is topic-led, although the tag itself does not visibly depict an exchange. |
| hierarchy | 4 | The title occupies the top fifth; date and venue follow directly below. The three-line bring-one-object instruction at middle-left and red deadline/URL at the bottom give preparation and response their own entry points. At thumbnail320 these still register, but the preparation block competes strongly with the main title. |
| typography | 3 | At usage720 the Korean and condensed English titles are clear, and the preparation line breaks keep whole words intact. Nearly every body line remains heavy, however, and the red-to-black change inside “1개를” splits the emphasis within one grammatical unit. A clearer distinction between instruction, explanation, and eligibility would improve reading rhythm. |
| space | 3 | At usage720 the right-side tag balances the large left instruction, and the lower text shares an inset left edge. The bottom URL nearly spans the canvas, while two cord fragments curl along otherwise open areas; the jump from the broad title block to the inset lower block is functional but less settled than the tag-stack version. |
| image_material | 3 | At native size the wood grain, spring highlights, paper surface, and soft tag shadow are distinct and generally coherent. The rust cord visibly fades into the background near the center-left end below the instruction, and the separate left-edge strand terminates below the deadline. These transitions weaken the otherwise concrete material rendering. |
| emotion_control | 4 | The restrained cream, black, and rust palette supports a practical, approachable event. The enlarged imperative and deadline have communicative jobs. The blank tag is calmer than the dense type around it; the treatment is controlled rather than dependent on many effects. |
| ai_slop | 3 | The tag and bring instruction are specific to this content, and no fake logo or microtext appears. At native size, the fading cord end below the instruction reads as an unresolved image/text masking transition, while the mostly all-bold type remains a familiar general event package. This residual prevents a high-end conclusion; it does not identify authorship. |

### Residuals

- Native cord fades into the blank ground below the large preparation block and ends separately at the left bottom → the object rendering loses material continuity → give the strand a deliberate visible termination or a clear occlusion instead of a soft disappearance.
- At usage720 the red/black emphasis divides “1개를” and most lower text is equally bold → grammatical and information roles compete → keep the noun phrase’s emphasis intact and reduce secondary-line weight while retaining every supplied character.
- Bottom URL spans almost the full width → little lateral breathing room compared with inset body text → align the response block to a deliberate shared margin without reducing phone legibility.

## X7358

Mandatory pass: true. Issues: [] (no mandatory failure observed).

All required copy legible at720: true.

All ten supplied strings were manually readable at 720×1080. The blue tag carries language, preparation, exclusion, and eligibility; the final tag carries the whole wrapped deadline and complete URL. White-on-blue letters remain clear. At 213×320 the card grouping survives, but fine punctuation and several small-body words cannot be independently verified with the same confidence. Native 1024×1536 is exactly 2:3. No omitted required string, altered non-whitespace punctuation/case, unrequested wording, or QR code was observed.

### Uncertainties

- Fine punctuation and some small-body words are not independently dependable at the 213×320 thumbnail; no unresolved usage720 copy ambiguity was observed.

### Full manual transcription

| Exact required string | Observed string | Equal after whitespace normalization only |
| --- | --- | --- |
| 이름 바꾸는 물건들 | 이름 바꾸는 물건들 | true |
| OBJECT NAME EXCHANGE | OBJECT NAME EXCHANGE | true |
| 2026.11.21(토) 13:30–16:00 | 2026.11.21(토) 13:30–16:00 | true |
| 가상 공간 여울실험실 2층 / YEOUL LAB | 가상 공간 여울실험실 2층 / YEOUL LAB | true |
| 한국어·English, 어느 언어로 적어도 좋아요. | 한국어 · English, 어느 언어로 적어도 좋아요. | true |
| 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | true |
| 깨지기 쉬운 물건과 음식은 받지 않아요. | 깨지기 쉬운 물건과 음식은 받지 않아요. | true |
| 만 16세 이상 · 무료 · 24명 | 만 16세 이상 · 무료 · 24명 | true |
| 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | true |
| yeoul.example/NAME?lang=ko&slot=pm | yeoul.example/NAME?lang=ko&slot=pm | true |

### Separate scores and located evidence

| Dimension | Integer score (1–5) | Visible evidence |
| --- | --- | --- |
| content_form | 5 | The entire information structure is printed on four large name-tag shapes: title, event details, blue preparation/conditions card, and response card. Rope holes, a small key, and a binder clip make the connection between naming and brought objects visible without extra wording. The concept governs both the picture and the editorial grouping. |
| hierarchy | 4 | At usage720 the title tag leads into the date/venue tag, then the blue card isolates preparation and exclusions, and the last cream tag contains the full response sentence and URL. At thumbnail320 the same four stages remain visible, although the blue-card sentences and URL need the larger view for dependable punctuation reading. |
| typography | 4 | At native and usage720 the type follows each card’s slight tilt, while white-on-blue instructions remain clear. Thin rules separate exclusion and eligibility without adding invented information. The bring-one-object line extends much nearer the blue card’s right edge than the other lines, leaving its internal spacing slightly tight. |
| space | 4 | The stacked tags create a consistent downward rhythm and separate the response card from conditions. Rope enters at the left and the key/clip balance the right side. At usage720 the blue preparation sentence ends roughly a dozen pixels from the card’s right edge, unlike its generous left inset; this is the main small-space weakness. |
| image_material | 4 | At native size, braided rope, punched holes, cream paper grain, blue paper, gold key, and black clip have distinguishable surfaces and readable edges. The shadows consistently separate cards from the background, and printed text follows card planes. No obvious melted edge or random material merger is visible; this is a visual finding, not a physical-performance claim. |
| emotion_control | 4 | Blue marks the practical rules; cream carries the title, venue, and response, with a thin coral backing adding a limited accent. Props are small and subordinate to usable information. The material staging suits an approachable naming activity without requiring a monochrome treatment. |
| ai_slop | 4 | The repeated tags are an editorial device directly tied to object names, and their contents are purposefully grouped rather than filled with decorative pseudo-information. Letterforms, rope detail, and distinct object surfaces stay coherent at native size. The tabletop styling is familiar and the crowded right end of the preparation line remains, so the execution is strong rather than flawless. |

### Residuals

- Usage720 preparation line nearly reaches the blue tag’s right edge → the most practical instruction has tighter internal space than other lines → slightly reduce this line or reflow it at whole-word boundaries while preserving the exact sentence.
- At the 213×320 thumbnail, blue-card sentences and the response URL are very small → punctuation-level verification cannot rely on this view → retain usage720 as the dependable copy reading view; preserve the clear four-card grouping if adapting smaller.

## X3429

Mandatory pass: true. Issues: [] (no mandatory failure observed).

All required copy legible at720: true.

All ten supplied strings were manually readable at 720×1080, including the language sentence split over two lines beside the empty box, the exclusion, full bottom deadline, and entire orange URL. At 213×320 the title, spoon, date, and orange response destination are clear landmarks, while the very small deadline cannot support confident word-and-punctuation verification. Native 1024×1536 is exactly 2:3. No omitted required string, altered non-whitespace punctuation/case, unrequested wording, or QR code was observed.

### Uncertainties

- The semantic role of the two empty outlined fields is ambiguous from pixels; no unrequested printed wording is visible.
- The full deadline cannot be independently verified word-for-word at the 213×320 thumbnail; it is clear at usage720.

### Full manual transcription

| Exact required string | Observed string | Equal after whitespace normalization only |
| --- | --- | --- |
| 이름 바꾸는 물건들 | 이름 바꾸는 물건들 | true |
| OBJECT NAME EXCHANGE | OBJECT NAME EXCHANGE | true |
| 2026.11.21(토) 13:30–16:00 | 2026.11.21(토) 13:30–16:00 | true |
| 가상 공간 여울실험실 2층 / YEOUL LAB | 가상 공간 여울실험실 2층 / YEOUL LAB | true |
| 한국어·English, 어느 언어로 적어도 좋아요. | 한국어·English, 어느 언어로 적어도 좋아요. | true |
| 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | true |
| 깨지기 쉬운 물건과 음식은 받지 않아요. | 깨지기 쉬운 물건과 음식은 받지 않아요. | true |
| 만 16세 이상 · 무료 · 24명 | 만 16세 이상 · 무료 · 24명 | true |
| 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | true |
| yeoul.example/NAME?lang=ko&slot=pm | yeoul.example/NAME?lang=ko&slot=pm | true |

### Separate scores and located evidence

| Dimension | Integer score (1–5) | Visible evidence |
| --- | --- | --- |
| content_form | 3 | A single spoon clearly supplies an ordinary small object, and the blank frames may suggest places for names. However, the broad frame under the title and the smaller frame beside the language sentence are detached from the spoon and from one another; the act of changing or exchanging a name is less clearly expressed than in the tag or handover posters. |
| hierarchy | 3 | At thumbnail320 the large Korean/English title, spoon, and date are the main landmarks. At usage720 the language note interrupts the route between image and date; preparation and exclusion sit together farther down, with orange isolating the URL. All copy is readable, but the empty frames occupy attention before participation instructions. |
| typography | 3 | At usage720 the two-column Korean/English title is legible, and the lower copy keeps intact sentences. Date, venue, preparation, and exclusion all use similarly forceful dark bold type, making their different roles depend mainly on position. The long deadline near the bottom is appreciably smaller; its punctuation is not dependable at the narrow thumbnail. |
| space | 2 | At usage720 a wide empty outlined strip around y320–384 and a second empty box around y552–614 reserve substantial space without a visible connection to an action. The spoon is neatly fitted between them, but useful participation information is concentrated below y660. The contrast between vacant boxes and the dense lower block is insufficiently resolved. |
| image_material | 4 | At native size the spoon bowl and handle share a consistent brushed-metal surface, a clear rim, and a soft green-tinted shadow. The background and dark type are comparatively flat; no visible edge melting or illegible pseudo-lettering appears. The 3D object itself is well executed and is not penalized merely for being metallic. |
| emotion_control | 3 | Pale green and dark green produce a calm but bright field; orange gives the response URL an obvious role. The spoon stays a single focal object. The two empty outlined boxes add a form-like mood whose purpose is uncertain, reducing precision rather than adding necessary emotion. |
| ai_slop | 3 | At native and usage720 the spoon rendering and text are technically coherent. The disconnected empty frames imitate information fields without a supplied filling instruction, and the giant bold title plus centered object plus lower prose stack can support many unrelated events. This is visible generic packaging, not evidence of who made it; no high-end conclusion is warranted. |

### Residuals

- Usage720 has two empty outlined fields disconnected from the spoon and each other → they resemble fill-in information without an explained action and reserve space ahead of practical instructions → integrate them visibly as paired blank name labels or remove them and recover room for participation details; add no copy.
- Lower date, venue, preparation, and exclusion are similarly bold → the different action roles flatten together → introduce a clearer weight/spacing hierarchy within the exact supplied text.
- The long deadline is extremely small at the 213×320 thumbnail → its complete punctuation and words are not reliably independently readable there → preserve its confirmed usage720 legibility and give the response group more room in a smaller adaptation.

## X3882

Mandatory pass: true. Issues: [] (no mandatory failure observed).

All required copy legible at720: true.

All ten supplied strings were manually readable at 720×900. Preparation, exclusion, eligibility, full one-line deadline, and complete URL are present in distinct lower rows. At 256×320, the handover scene and main type remain clear; the smallest deadline and explanatory punctuation need the usage view for reliable transcription. Native 1122×1402 gives a 4:5 relative ratio error of about 0.0357%, within 1%. No omitted required string, altered non-whitespace punctuation/case, unrequested wording, or QR code was observed.

### Uncertainties

- Small deadline/explanatory punctuation is not independently dependable at the 256×320 thumbnail; no unresolved usage720 copy ambiguity was observed.

### Full manual transcription

| Exact required string | Observed string | Equal after whitespace normalization only |
| --- | --- | --- |
| 이름 바꾸는 물건들 | 이름 바꾸는 물건들 | true |
| OBJECT NAME EXCHANGE | OBJECT NAME EXCHANGE | true |
| 2026.11.21(토) 13:30–16:00 | 2026.11.21(토) 13:30–16:00 | true |
| 가상 공간 여울실험실 2층 / YEOUL LAB | 가상 공간 여울실험실 2층 / YEOUL LAB | true |
| 한국어·English, 어느 언어로 적어도 좋아요. | 한국어 · English, 어느 언어로 적어도 좋아요. | true |
| 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | true |
| 깨지기 쉬운 물건과 음식은 받지 않아요. | 깨지기 쉬운 물건과 음식은 받지 않아요. | true |
| 만 16세 이상 · 무료 · 24명 | 만 16세 이상 · 무료 · 24명 | true |
| 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | true |
| yeoul.example/NAME?lang=ko&slot=pm | yeoul.example/NAME?lang=ko&slot=pm | true |

### Separate scores and located evidence

| Dimension | Integer score (1–5) | Visible evidence |
| --- | --- | --- |
| content_form | 4 | In the top half two people face one another across a table and hand over a small wooden object with a blank tag. Naming and exchange are both visible, while the lower rows supply event and participation details. The scene directly explains this particular activity, though the smiling educational-illustration vocabulary is familiar. |
| hierarchy | 4 | The centered title is framed by the two heads; the handover draws the eye down to date and venue. At usage720 the enlarged bring-one-object sentence stands above a separately ruled exclusion row, eligibility row, and deadline/URL block. At thumbnail320 title, exchange scene, and date still read first; the fine deadline punctuation requires the usage view. |
| typography | 3 | At usage720 the centered title and English subtitle are well contained between the figures, and all full sentences are readable. Nearly every lower line is bold and centered, with coral rules giving eligibility and exclusion similar row status. The response sentence is the smallest full-width row; changing body weight and spacing would improve the practical scan. |
| space | 4 | Figures are intentionally cropped at both side edges, leaving a clear central channel for title and object. The coral tabletop is a clean boundary between scene and information. Lower rules and centered rows have consistent side margins, though the response block near the bottom has less breathing room than the date panel. |
| image_material | 4 | At native size black contours, simplified skin/blue clothing, wood grain, and coral tabletop belong to a coherent illustrated system. The tag and object remain distinct at the handover, and line weights do not randomly change into photorealistic surfaces. Simplified finger lines are treated as stylization; the image does not establish real handling mechanics. |
| emotion_control | 4 | Friendly faces, matched blue clothing, and a warm coral table suit a small collaborative activity. The expressive elements all support the handover scene; there is no gratuitous glow or unrelated decoration. The familiar cartoon warmth is appropriate but not unusually distinctive. |
| ai_slop | 4 | The handover, attached blank tag, and title occupying the gap between people give the image a content-specific composition. No fake labels, broken Korean strokes, or conspicuous material mergers are visible at native size. The generic smiling-character vocabulary and all-bold ruled footer remain editorial limitations, but they do not create an obvious synthesis defect. |

### Residuals

- Usage720 footer uses bold centered rows and equal-looking coral separators for several different roles → eligibility, exclusions, and response feel similarly important → distinguish explanatory weight and reserve stronger emphasis/space for preparation and response.
- The bottom full-sentence deadline is much smaller than the date and bring instruction at thumbnail320 → detailed response reading needs the usage view → redistribute a little footer space to the response block without adding wording.

## X3815

Mandatory pass: true. Issues: [] (no mandatory failure observed).

All required copy legible at720: true.

All ten supplied strings were manually readable at 720×720. The date and venue cross the center seam; preparation, exclusion, eligibility, full deadline, and complete URL remain clearly readable against both colors. At 320×320 the large text survives well, but the deadline is the smallest sentence and its punctuation is less dependable than at usage720. Native 1254×1254 is exactly 1:1. No omitted required string, altered non-whitespace punctuation/case, unrequested wording, or QR code was observed.

### Uncertainties

- The smallest deadline punctuation is less dependable at the 320×320 thumbnail; no unresolved usage720 copy ambiguity was observed.

### Full manual transcription

| Exact required string | Observed string | Equal after whitespace normalization only |
| --- | --- | --- |
| 이름 바꾸는 물건들 | 이름 바꾸는 물건들 | true |
| OBJECT NAME EXCHANGE | OBJECT NAME EXCHANGE | true |
| 2026.11.21(토) 13:30–16:00 | 2026.11.21(토) 13:30–16:00 | true |
| 가상 공간 여울실험실 2층 / YEOUL LAB | 가상 공간 여울실험실 2층 / YEOUL LAB | true |
| 한국어·English, 어느 언어로 적어도 좋아요. | 한국어·English, 어느 언어로 적어도 좋아요. | true |
| 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | 이름을 바꾸고 싶은 작은 물건 1개를 가져오세요. | true |
| 깨지기 쉬운 물건과 음식은 받지 않아요. | 깨지기 쉬운 물건과 음식은 받지 않아요. | true |
| 만 16세 이상 · 무료 · 24명 | 만 16세 이상 · 무료 · 24명 | true |
| 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | 11.18(수) 18:00까지 아래 주소로 참가 의사를 남겨주세요. | true |
| yeoul.example/NAME?lang=ko&slot=pm | yeoul.example/NAME?lang=ko&slot=pm | true |

### Separate scores and located evidence

| Dimension | Integer score (1–5) | Visible evidence |
| --- | --- | --- |
| content_form | 3 | The large orange binder clip is a plausible example of a small brought object, and it bridges the yellow-green and blue halves. Korean and English occupy opposite halves above it. This can suggest connection, but the color split and clip do not make renaming as explicit as a tag or handover does; much of the concept rests on the title. |
| hierarchy | 3 | At thumbnail320 both language titles and the orange clip dominate the upper field, then the large date begins the lower reading block. At usage720 preparation, exclusion, eligibility, deadline, and URL are readable. Similar boldness across those lower rows gives fewer cues to what to bring versus what is excluded, and the two language headlines compete at the first glance. |
| typography | 3 | At usage720 the three-line Korean title and three-line English title are legible, but the long “EXCHANGE” is much narrower in character proportion than “OBJECT” and “NAME.” The body, exclusion, and eligibility all use heavy dark type with little weight contrast. The deadline and URL are packed into the final two rows; a more deliberate weight and width system would help. |
| space | 3 | The split is exact at center and the clip overlaps it with clear separation from the title letters. The full-width date/venue and subsequent left-aligned groups are orderly. The background seam runs through the middle of several text lines, while the last two rows sit close together and near the bottom edge; these relationships are workable but visually busy. |
| image_material | 4 | At native size orange painted metal, bright wire handles, dark inner faces, and the soft shadow are visibly differentiated. Clip edges are clean and type remains crisp. The strong color and 3D treatment are acceptable on execution grounds; pixels cannot certify the clip’s actual mechanics or the poster’s printing performance. |
| emotion_control | 3 | Yellow-green, blue, navy, and orange establish a brisk, conspicuous mood. The orange clip is the sole object accent, so the image is not overloaded with effects. The same visual force applied to both headlines and most body lines produces sustained intensity rather than a nuanced invitation. |
| ai_slop | 3 | At native size no conspicuous garbled letters or melted object edge is visible. The split-color field, large shiny stationery object, and oversized heavy sans titles form a familiar general promotional package; there is little additional visual evidence of changing an object’s name. Refine the object/type relationship and information weights rather than simply changing the 3D surface. This is not an authorship judgment. |

### Residuals

- Top bilingual titles and the shiny clip dominate at thumbnail320 while renaming is carried mainly by wording → the package is less specific to the activity → connect the existing blank-object/name idea more directly to the clip and type, without adding text or a QR code.
- At usage720 “EXCHANGE” is strongly condensed and all lower copy is heavy → the typography feels driven by fitting and sustained emphasis → use a consistent title-width strategy and differentiate preparation, exclusions, and response weights.
- The central color seam crosses lower sentences and the deadline/URL rows are close together near the bottom → background division and dense response text compete → soften or reposition the division within a deliberate information layout and increase response spacing while keeping all copy legible.

## Set R6-C2

Exact members: X7358, X3882, X3815, X3429, X1059.

Diversity: 3 (integer 1–5).

All five members were inspected in all three views. X7358 turns every information group into a physical name tag; X3882 depicts an actual handover between people; X1059 pairs a blank peg-held tag with a dominant preparation sentence and curving cord; X3429 uses a single spoon with detached outlined fields; X3815 uses opposed bilingual title columns and a clip over a split-color field. These are more than color variants, but large heavy sans titles, familiar everyday props, large date/venue blocks, and bold lower copy recur across the set. The strongest content integration is X7358’s tag structure (content_form 5); the weakest spatial resolution is X3429’s empty frames versus crowded lower information (space 2), and X3815 is less topic-specific. Both 2:3 posters, both 4:5 posters, and the single square are present: five members, with every native ratio within 1%. Every member carries all ten supplied strings legibly at usage720, without added wording or QR code. The full distribution supports diversity 3; no dimension scores are summed or averaged.

Closest pair: X3429 and X3815; score: 2 (1=repetition, 5=strongly distinct).

Both use oversized dark bold Korean at upper left with a large English block at upper right, a single reflective everyday object in the upper/middle field, a prominent full-width date/venue below, then similarly heavy left-aligned participation prose and a bottom URL. X3429 substitutes a green field, spoon, and empty frames; X3815 substitutes yellow-green/blue halves and an orange clip. Those changes distinguish them, but the title/object/logistics skeleton and text roles remain close. Score 2 uses the stated repetition-to-distinction scale, not a quality total.

### Set residuals

- X3429 and X3815 retain a closely related oversized-type/single-object/lower-prose structure → variety relies partly on color and object substitution → develop a more distinct role for type or object in one direction while preserving the required copy and ratios.
- All five use heavy sans body copy, even when their imagery differs → practical roles often separate by position rather than typographic contrast → give preparation, exclusion, eligibility, and response distinct but legible treatments across the directions.
- X3429’s detached empty fields and X1059’s fading cord remain visible weaknesses; X3815 retains generic split-color/stationery packaging → the set cannot be described as uniformly high-end → resolve these content/space/material relationships before adding effects.
- Thumbnail word-level confidence varies with the actual 213/256/320-pixel widths → thumbnails are insufficient as universal copy proofs → rely on the actually read usage720 views for the required legibility finding.

