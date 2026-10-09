# General-rule audit after closed R9

This is a read-only audit of candidate I and the proposed J mechanisms, followed by a bounded recheck of the applied J changes. It uses the closed R9 report, selected packet and all three selected critics’ recorded observations. It does not rescore images, inspect future R10 images, run makers/reviewers or modify the skill. Suggested locations below refer to candidate I as read on 2026-10-08.

**Finding:** all four proposed changes are justified as general rules. They concern request interpretation, occupied area and reading order, object/action continuity, and optical copy fidelity. None requires a fixed palette, quiet composition, smaller title, mandatory tape, five fixed media or a new runtime review stage. The changes can fit into the existing planning and seven-item inspection.

The closed result stays unchanged: selected PASS 0 / FAIL 4 / NA 1; set NA. M1/M2 have all seven scores at 4 from editorial and craft. Portfolio gives all five `image_material: 3` and style FAIL because it reads the skill invocation as a duct-tape material direction. The selected packet records client styles as `mode: open` and explicitly says `스타일은 맡길게`; no explicit tape treatment is listed. This interpretation mismatch is a future briefing issue, not grounds to replace its critic, erase a finding or replay R9 with relaxed gates. Independently, craft retains M3 typography null after one exact revisit, craft retains M4 image/material 3 and AI-slop 3, and portfolio retains M5 hierarchy 3 and space 3. Every critic rates diversity 4. The initial recording-related NA remains preserved and is separate from these selected-image findings.

| Proposed rule | Evidence and generality | Guardrail |
| --- | --- | --- |
| Separate skill invocation from actual style/material | The open-style R9 request was read as literal tape by portfolio. The same failure can occur with any named tool or workflow. | Preserve explicit material/style directions; do not turn every mention into a style requirement or dismiss an actual material request. |
| Plan usable area and reading priority at the actual ratio | M5's large title, equally strong schedule and heavy structure leave logistics in a narrow panel. This is a relationship among content, occupied area and viewing size, rather than a defect unique to horizontal posters. | Reallocate or reduce competing mass where needed. A strong title, prominent schedule or architectural frame remains valid when it supports a clear scan and readable practical information. |
| Resolve contacts, ownership and continuation before/after stylization | M4's microphone shaft, overlapping grips and cream circular marks fail to resolve into clear relations. Similar ambiguity applies to handles, supports, tools, body overlaps and mechanical joins. | Require legible function/action within the selected expression system. Do not demand photographic anatomy, prohibit expressive marks or remove necessary multi-person actions. |
| Make punctuation optically distinguishable without altering copy | M3's thick short range bar remains hyphen/en-dash ambiguous. The same issue affects punctuation, character proportions and gaps across fonts and treatments. | Preserve literal copy. Judge what pixels show; never claim a raster reveals an underlying Unicode code point. |

## Concise wording and placement

1. **SKILL.md, section 1, near lines 14–16:** put the invocation distinction where the brief is parsed, rather than only in aesthetic advice.

   > 스킬명·도구 호출 문구와 실제 스타일·소재 지시를 구분한다. 스킬을 부른 것만으로 같은 이름의 소재를 요구했다고 해석하지 않으며, 사용자가 명시한 스타일·소재·제외 조건은 제작 명세와 검수 조건에 그대로 전달한다.

   The interpretation must reach both makers and future reviewers as part of the ordinary brief. Merely adding a sentence to art-direction advice leaves the original invocation wording available for the same mistaken requirement. A short interpreted requirement is enough; no new schema or approval step is needed for normal production.

2. **SKILL.md line 32 and art-direction.md line 63:** replace the current “explicit type-only request conflicts, ask allowed range” behavior. It creates an unnecessary approval round and contradicts the user's explicit scope. Make nonglyph content a default that yields to an explicit typography-only direction.

   > 비문자 시각 요소를 사용자가 금지하거나 타이포그래피만 요청한 경우에는 그 조건을 따르고, 글자의 구조·비례·공간·읽는 흐름으로 내용과 방향의 차이를 구현한다. 그 외에는 내용의 핵심을 맡는 실질적인 비문자 시각 요소를 설계한다.

   This does not remove R9's required nonglyph content: its frozen case explicitly requires it. Prospective explicit type-only requests should have applicable conditions established before generation and review, rather than receiving a later exception or score waiver.

3. **Art-direction.md lines 7/13 or 34; compact reinforcement in SKILL.md line 26:** extend the existing actual-copy plan instead of creating a separate layout deliverable.

   > 요청 비율에서 실제 카피 묶음의 폭·줄 수·사용 크기 판독과 주제 이미지의 식별 면적을 함께 계획한다. 필수 안내가 좁아지거나 큰 블록들이 첫 시선을 경쟁하면, 안내 글자를 줄이기 전에 정보 영역을 다시 배분하고 프레임·다른 블록의 비중을 조정한다.

   “비중을 조정한다” is preferable to an unconditional “heavy frames must be simplified.” M5's frame is grounded in the bridge concept, so the transferable defect is unresolved allocation and competition. No specific title ratio, margin, coordinate, line count, frame thickness or area quota is justified by this one observation.

4. **Art-direction.md line 11 for planning and line 61 for inspection; brief reinforcement in SKILL.md line 52:** express the contact check as short relational reasoning, rather than a mandatory written action graph for every poster.

   > 손·도구·물체가 연결되는 장면에서는 누가 무엇을 잡거나 지지하는지, 겹침 뒤에서 구조가 어떻게 이어지는지 정한다. 평면화·크롭·인쇄 흔적을 적용한 뒤에도 그 관계와 행동이 읽히는지 확인한다. 필요한 복잡성은 유지하고 모호한 소유·접촉·연속성만 해결한다.

   This covers M4 without banning close portraits, overlapping hands, ink-like marks or microphones. Abstract/nonphysical imagery needs consistency in its own visual logic; it should not acquire a universal requirement for physically realistic construction.

5. **Art-direction.md typography row at line 55 and optical inspection at line 61:** join punctuation to existing proportion and spacing checks.

   > 문장부호는 확정 카피를 바꾸지 않고, 글자의 비례·무게·주변 간격을 조정해 사용 크기에서 필요한 구별이 보이게 한다. 원본을 다시 봐도 형태 구별이 불확실하면 불확실성을 남기며, 래스터에서 문자 코드의 출처를 확인했다고 하지 않는다.

   Avoid a rule to “use an en dash for times” or a universal dash-length specification. The existing literal-copy requirement already determines the requested character; the missing control is its rendered optical distinction in the chosen type system.

## Remaining scope and limits

The current eight-dimension research table already covers image/style, viewpoint/crop, layout/space, color, typography, hierarchy, material/production and emotion/audience. Its studio-plus-Canva routing is already appropriate for R9's neighborhood event. Keep it intact. None of the R9 findings supports reducing reference analysis to typography or adding another source quota.

Keep AI-slop as its own seventh quality criterion. M4's local construction can legitimately affect both image/material and AI-slop; the latter must remain a concrete visual finding rather than a medium blacklist or an authorship detector. Existing warnings against monochrome, paper and minimalism as automatic quality signals already provide the needed balance.

Shared heavy sans-serif lettering and recurring audience/screen imagery limit exceptional diversity, but all three critics still find five complete systems and assign diversity 4. Do not respond with a five-font or five-media quota. The existing comparison of structure, viewpoint, image/type roles and reading flow should remain the diversity mechanism.

These are prospective safeguards, not proof that candidate J is high quality across all cases. The bounded next test is one request producing five genuinely different styles, with the whole set closed before a subsequent one-request/five-image test. This audit does not launch that test or prescribe additional campaign outputs.

## Applied J bounded recheck

The actual changes to `SKILL.md`, `art-direction.md` and `evaluation-loop.md` were compared with the closed candidate-I snapshot. The invocation interpretation reaches review before scoring. Actual-ratio allocation retains strong type and heavy structures when the reading path works. The contact rule preserves requested actions and necessary complexity, and optical punctuation fidelity retains literal copy and raster uncertainty. Existing eight-dimension research, studio/Canva routing, separate AI-slop criterion, five-maker production and finite correction workflow are unchanged. No fixed media list, palette, coordinate quota, quietness quota or new review stage appears.

One small routing gap remains in this first applied wording: the nonglyph default now starts **“열린 요청에서는”** in both the skill and art-direction. This may exempt a narrowly specified style from substantive imagery even when the user did not ask for a typography-only poster. The general default should apply unless the user explicitly requests type-only or excludes nonglyph elements. For example, replace that opening with **“사용자가 글자만의 구성이나 비문자 요소 제외를 명시하지 않은 경우에는”** at both sites, while retaining the explicit override that follows. This is a consistency correction, not a request to impose imagery on a type-only brief.

An optional wording refinement is to tie the art-direction warning about a narrow panel with small practical type to actual readability: **“필수 정보를 좁은 칸의 판독이 어려운 작은 글자로 밀어 넣지 않는다.”** The present context already favors allocation over shrinking, but this form avoids an unintended blanket ban on readable small information.

Sources: [candidate I SKILL.md](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/snapshots/candidate-i/SKILL.md), [current art direction](/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster/references/art-direction.md), [closed R9 report](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round9/report.md), [selected packet](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/reviews/R9-C1/selected/packet.json), [portfolio observations](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/reviews/R9-C1/selected/cli/portfolio/portfolio.observations.json), [craft observations](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/reviews/R9-C1/selected/cli/craft/craft.observations.json), [editorial observations](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/reviews/R9-C1/selected/cli/editorial/editorial.observations.json).
