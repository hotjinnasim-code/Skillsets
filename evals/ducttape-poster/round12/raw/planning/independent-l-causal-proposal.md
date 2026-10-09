# Candidate L: generalization audit after closed R11 / K

This is a proposal, not a runtime edit or a new evaluation. Runtime K and the closed R11 artifacts were read only. No generation, actor launch, extra case, test, re-selection, re-score, or Git mutation was performed. The proposed changes address rendered relationships and the maker's own QA; they do not prescribe an image, medium, palette, title size, or fixed set of five styles.

## Closed evidence and limits

The two whole-phase closure records confirm that all three critics closed in both phases. Initial: 0 PASS / 5 FAIL / 0 NA. Selected: 2 PASS / 3 FAIL / 0 NA. All mandatory conditions passed; each critic's set diversity was 4 in each phase. There are 30 image-profile records and 210 valid scores across the two phases. All five makers selected repair-2 after their own initial plus two repairs, for 15 total calls. The selected set remains FAIL. Source, procedure and recording gates are PASS; no critic feedback was used for another actor correction.

Evidence read directly:

- [Initial whole-phase closure](ducttape-poster-round11/reviews/R11-C1/initial/whole-phase-closure.json), [selected whole-phase closure](ducttape-poster-round11/reviews/R11-C1/selected/whole-phase-closure.json), [closed report](ducttape-poster-round11/report.md).
- All six actual `*.observations.json` critic records, including each low rating's located evidence and the selected editorial / portfolio evidence that disagrees with craft.
- Each maker's actual initial / repair-1 / repair-2 `call-input.json`, `inspection.json` and available `parent-comparison.json`, assignment and selection records.
- Runtime `SKILL.md` and all four reference files. In this audit, selected M2 thumbnail320 and usage720, and selected M3 and M5 native images were physically displayed. This is not a claim that this auditor displayed every R11 asset. Root's separate whole-image inspection is not replaced by these focused views.

The selected lows are only craft: M2 hierarchy 3; M3 hierarchy 3 and image_material 3; M5 image_material 3 and ai_slop 3. Editorial and portfolio give every selected quality item at least 4. Their disagreement is a substantive limit, not a reason to erase the valid low ratings. This one development observation does not establish that the proposed L will pass the next request.

## What failed, and why K was insufficient

### M2: a planned date-first route was treated as proof of a usable hierarchy

Craft initially identified competition between the salmon date/time field, Korean identity band and English on the photograph. The selected craft evidence again locates these three strong anchors and describes enlarged modules competing. Editorial explicitly calls the selected composition a usable date-first sequence, while also noting the title competes with the schedule. Portfolio likewise accepts the date-first sequence.

The maker's own usage QA describes `date/time → Korean name/activity → six factual rows` and says all eleven entries read once. Its two actual repair prompts chiefly try to restore assigned photo widths, margins, the paper bridge and factual type size. The last prompt preserves date-first and asks for larger / more open facts, but its own selected observation still says date/time are larger than planned. Neither the usable written sequence nor individual legibility tests whether the rendered anchors actually guide the viewer in that sequence.

K already says to choose the first and next information, avoid equally strong competing blocks, and redesign big relationships. Adding those same exhortations would not address this gap. The needed change is to identify the actual leading and competing anchors from the rendered thumbnail, then verify the selected secondary route at usage size. A legitimate date-led design can pass this test. Craft's sentence that event identity should lead is not a universal title-first instruction and should not become one.

Sources: [selected craft](ducttape-poster-round11/reviews/R11-C1/selected/cli/craft/craft.observations.json), [selected editorial](ducttape-poster-round11/reviews/R11-C1/selected/cli/editorial/editorial.observations.json), [selected portfolio](ducttape-poster-round11/reviews/R11-C1/selected/cli/portfolio/portfolio.observations.json), [M2 initial QA](ducttape-poster-round11/production/R11-C1-M2/stages/initial/inspection.json), [M2 final prompt](ducttape-poster-round11/production/R11-C1-M2/stages/repair-2/call-input.json), [M2 final QA](ducttape-poster-round11/production/R11-C1-M2/stages/repair-2/inspection.json).

### M3: readable corner groups did not establish whole-information retrieval

The selected craft hierarchy evidence accepts the clear central title but locates schedule / venue / entry, English / activity, participation, and preparation in four distant groups without a strong secondary practical route. Editorial accepts the hierarchy while noting the broader scan; portfolio accepts it while noting travel between upper-left and both lower corners. Thus dispersed layouts remain legitimate, but their retrieval route needs evidence beyond the fact that the groups are individually readable.

The assignment plans a central first anchor, attendance above left, then a sweep along the common lower baseline. Actual maker QA repeatedly inventories the four-row attendance group and two lower pairs and states all eleven entries are readable at 720px. The two repairs protect all corner positions and focus on the block. The records do not show an actual viewer route from the central anchor to attendance and onward, or the visual cue that moves attention between the separated participation groups.

K already contains a paragraph explicitly distinguishing local legibility from whole retrieval. Its implementation in this maker's records remained an inventory. L should require a short actual route observation with the visible cue for each necessary transition, and record an unresolved transition even when every line reads. It should not force one information panel, a linear column, or a title→date order.

Sources: the selected craft / editorial / portfolio records above; [M3 assignment](ducttape-poster-round11/production/R11-C1-M3/assignment.json), [M3 final QA](ducttape-poster-round11/production/R11-C1-M3/stages/repair-2/inspection.json), [M3 final comparison](ducttape-poster-round11/production/R11-C1-M3/stages/repair-2/parent-comparison.json).

### M3 and M5: material / contact finish improved while depicted output correspondence remained uncertain

Initial editorial ratings locate positive/negative or shape-placement inconsistencies in M1, M3, M4 and M5, giving image_material and ai_slop 3. This was a recurring relationship issue across distinct styles, not evidence that one medium is defective. In selected M3, craft locates the narrower fitted branch on the tapered gray block versus the broader paper branch and says the scratch finish does not resolve their construction. In selected M5, craft distinguishes a connected looping relief from three detached swept paper strokes; it explicitly ties the low AI-slop score to this construction rather than vivid color, illustration or texture.

M3 already noticed nonmatching features initially. Its first repair improves woodlike sides; its own QA then correctly states that light branch / dark field versus dark paper branch remains inconsistent. Its second prompt explicitly asks for matching forks, leaves, berries and mirror transfer. The comparison records the polarity improvement but also says branch features still do not fully correspond. This is important: merely adding “matching” or a more precise physical instruction was already tried. The remaining problem is incomplete implementation and selection under a finite budget, not an absent prompt adjective.

M5's first repair improves the sheet boundary but leaves woodlike bevel and separated block. The final local repair replaces those with teal body, rounded corner and a peel lip. Its own QA calls the relief / print matching and identifies contact as improved, while exact registration remains inferred. Craft's final observation identifies a more consequential topology mismatch. Local material plausibility and an apparent seam are weak substitutes for comparing the key marks themselves.

K already covers action relationships, owned grips, material consistency, direct before/after viewing and repairing structure. The general missing distinction is **co-presence / similarity versus correspondence** when the image depicts one thing producing or transforming into another. L should make the maker choose a few visual invariants necessary to that relation, compare the actual pair under their different viewpoints, and report what is only inferred. Repair priority should follow the rendered relation's importance, rather than a long list of differences from planning coordinates or extra softness / contact detail.

Sources: [initial editorial](ducttape-poster-round11/reviews/R11-C1/initial/cli/editorial/editorial.observations.json), selected craft above; [M3 repair-1 QA](ducttape-poster-round11/production/R11-C1-M3/stages/repair-1/inspection.json), [M3 repair-2 prompt](ducttape-poster-round11/production/R11-C1-M3/stages/repair-2/call-input.json), M3 final comparison above; [M5 repair-2 prompt](ducttape-poster-round11/production/R11-C1-M5/stages/repair-2/call-input.json), [M5 final QA](ducttape-poster-round11/production/R11-C1-M5/stages/repair-2/inspection.json), [M5 final comparison](ducttape-poster-round11/production/R11-C1-M5/stages/repair-2/parent-comparison.json).

## Scope and interpretation safeguards

- A represented input / action / result relation needs coherent visual evidence only when that relation is part of the current brief or chosen concept. A static product, abstract graphic, concert image, expressive type poster, collage or intentional surreal scene does not acquire a workflow-diagram or literal-mechanics requirement.
- Correspondence is not 2D pixel identity. Viewpoint, foreshortening, reflection, crop, stylization and the depicted transformation can legitimately change contours. Compare the concept's necessary features; do not penalize ordinary perspective differences or demand microscopic registration.
- A light or dark drawn area alone does not establish which surface is raised, recessed or inked. The display, relief construction and stated relation matter together. Stylized positive/negative choices can be intentional; record ambiguity instead of declaring an unsupported physical impossibility. This does not revise the closed editorial or craft scores.
- A lifted / revealed tool beside a completed result can explain an action. Do not force active pressure transfer, a peel seam or a flexible corner in every depiction. Firm rubber can be plausible; softness is not a universal material gate.
- A date, image, title or multiple deliberate entry points may lead. Dense, loud, playful, rough, commercial and experimental directions remain valid when their chosen visual and practical roles work. “Quiet” is not a high-end default.
- User-specified genre, geometry, separation, sequence, reference role, preservation, type-only constraint, count and ratio retain precedence. Ordinary plan coordinates are implementation guidance. A change from them is not itself a defect when rendered function improves and genuine direction distinction survives.
- The high-end goal remains the seven-item per-critic gate and whole-set diversity gate. Maker QA is evidence for bounded production decisions, not a new critic, new score system or substitute for independent evaluation. Valid lows, NA and uncertainty remain preserved.

## Minimal exact suggested runtime text

Recommend three edited files. Do not modify `visual-research.md` or `evaluation-loop.md`: whole studio / Canva research, fresh critics, whole-five closure, score gates, finite 1+2 call limits and development / held-out separation already have the needed rules. No new styles, scores, fields, actor stages, tests or reference quotas are proposed.

### 1. `references/art-direction.md`: one conditional correspondence paragraph

Insert after the paragraph beginning `하나의 행사·과정·경험에 속한 여러 행동을 함께 보여 줄 때는`:

> 화면에서 어떤 대상·행동이 다른 대상이나 결과를 만들어 내거나 바꾸는 관계를 보여 줄 때는 함께 등장한다는 사실과 실제 대응의 근거를 구별한다. 현재 발상을 성립시키는 핵심 특징과 의도적으로 달라지는 특징을 먼저 정하고, 실제 이미지의 양쪽을 그 기준으로 대조한다. 연결·분리, 주요 부분의 배치, 경계·방향 등 필요한 특징은 시점·크롭·반사·변형·추상화의 차이를 고려해 확인하며, 같은 색·질감이나 대략적인 모양만으로 대응을 통과시키지 않는다. 표현상 확인되지 않는 작동은 추정으로 남기고 표면의 밝고 어두움만으로 물리적 오류를 단정하지 않는다. 이 관계가 필요 없는 구성에 새 과정·인과·물리 장면을 추가하지 않는다.

This generalizes input / action / output correspondence while keeping image style and intentional transformation open. It does not embed relief-printing conventions as poster defaults.

### 2. `references/art-direction.md`: replace the existing distributed-information paragraph with an executable observation

Replace the paragraph beginning `필수 정보가 여러 구역에 분산되면`:

> 계획 설명을 판독의 근거로 삼지 않고 축소 보기에서 실제 첫 앵커와 경쟁하는 큰 요소를 짚는다. 사용 크기에서는 관객이 현재 목적에 필요한 카피 전체를 찾는 경로를 실제로 따라가며, 다음 목적지로 이동하게 하는 화면 단서를 확인한다. 필수 정보가 여러 구역에 있으면 각 항목의 판독과 전체 정보를 찾아 쓰는 흐름을 구별한다. 선택한 첫 역할과 다음 유용한 정보가 이어지지 않거나 무관한 구역을 반복해서 훑어야 하면 그룹·강약·공간 관계부터 고친다. 제목·이미지·날짜나 의도한 여러 진입점 모두 가능하며, 한 정보 패널·열이나 고정된 제목→일정 순서를 강요하지 않고 사용자 지정 순서를 우선한다.

This replaces a broad existing instruction with a concrete action. It does not impose a linear route on every poster or interpret M2's date-led design as inherently wrong.

### 3. `references/art-direction.md`: replace the repair paragraph with priority and verification rules

Replace the paragraph beginning `보정은 눈에 보이는 원인 하나를 우선한다`:

> 보정은 실제 결과에서 영향이 큰 원인을 우선한다. 사용자 보존 조건 위반을 제외하면 계획 좌표에서 벗어났다는 사실보다 내용의 핵심 관계와 실제 정보 검색의 실패를 먼저 본다. 필수 조건 → 읽기·구성 → 글자·이미지 마감 순서로 실패 위치, 깨진 관계, 다음 결과에서 확인할 변화와 보존할 장점을 짧게 정한다. 보정 뒤에는 같은 보기에서 그 관계를 전후 대조하고 전체 카피·조건·정보 경로도 다시 확인한다. 재질·접촉·질감이 좋아져도 필요한 대응이나 읽는 흐름이 남으면 미해결로 기록한다. 같은 국소 지시로 관계가 해결되지 않았고 호출이 남아 있으면 사용자 조건과 방향의 구분을 지키며 필요한 시점·경계·그룹·비중까지 재설계한다. 최신 파일이나 더 매끈한 표면을 자동 채택하지 않고 전체 내용·판독·마감을 더 잘 유지한 결과를 선택한다. 한도를 소진한 미완성은 그대로 알리며 하이엔드라고 단정하지 않는다.

K already grants maker redesign authority; this adds when to use it and what must be checked. It does not add a third repair or authorize another actor to continue a closed image.

### 4. `SKILL.md`: one link back to the operative checks

In section 4, after the first QA paragraph, add:

```markdown
각 항목이 따로 읽히거나 재질이 정교하다는 이유로 전체 관계까지 통과시키지 않는다. [아트디렉션](references/art-direction.md)의 방법으로 실제 첫·다음 앵커, 필요한 카피 전체를 찾는 경로, 해당되는 대상·행동·결과의 대응을 확인한다.
```

This ensures the main workflow invokes the detailed method; it adds no new style requirement.

### 5. `references/parallel-production.md`: one short maker observation requirement

In `제작자 한 명의 범위`, after the paragraph beginning `내장 이미지 도구로 단일 평면 포스터 한 장을 실제 생성한다`, add:

> 자기 검수에는 실제 이미지의 첫·다음 앵커와 필요한 카피 전체를 찾은 경로, 해당되는 경우 대응하는 대상 사이의 핵심 특징 비교를 짧게 남긴다. 항목별 판독이나 “같은 모티프”라는 설명으로 관계 검수를 대신하지 않는다. 보정의 국소 마감이 개선돼도 남은 관계 실패를 중앙에 전달한다.

This is an operational maker QA note using already required views. It does not require peer images, external critics, fresh actor sessions or a new record schema.

## Adoption and verification boundary

The recommendation is to change how existing production judgments are made, rather than lengthen generator prompts with more finish adjectives. Relational requirements were already in several R11 native prompts; generator compliance remains uncertain. L should not promise a passed next set because these instructions exist.

R11 is closed development evidence for this proposal. If adopted, freeze the concrete L files and changed-text record before any new whole-five request. Preserve the actual R11 lows and disagreements. Close the next complete five-image production and both required evaluation phases within the unchanged finite bounds before interpreting its result or beginning another candidate. The proposal has not been run or validated on another brief.
