# Frozen K runtime audit

Scope: read-only audit of the six `Skillsets/skills/ducttape-poster` runtime files, the ducttape-poster README section, and the permitted `ducttape-poster-round11/snapshots/candidate-k` files. All six runtime files are byte-identical to the frozen snapshot. No production images, maker results, critic outputs, scores, or other round11 files were inspected. No actor/native calls, runtime edits, or Git mutations were performed. This is a static audit, not a quality PASS or a revalidation of historical counts.

## Blockers

No confirmed static blocker found. The written contract covers the requested general behavior:

- Whole studio visual systems and actual Canva template pixels for mainstream requests, rather than typography-only research (`SKILL.md:24`; `visual-research.md:3–20`).
- Five structurally different directions, explicit-style precedence, and avoidance of both familiar effect packages and a replacement quiet-paper/serif formula (`SKILL.md:28–38`; `art-direction.md:42–53`).
- Five actual maker roles within available capacity, no recursive makers or concurrency bypass, complete-set checks, and truthful fallback when collaboration is unavailable (`parallel-production.md:11–29`).
- One complete case before the next, preservation of the entire set, no new 20-image campaign by default, finite correction budgets including failed/central calls, and no budget reset through renamed versions (`evaluation-loop.md:7, 19–25, 74–80`).
- Copy/spacing/symbol uncertainty, original-versus-use-size inspection, honest maximum-resolution limitations, and no universal quality guarantee (`SKILL.md:48, 54, 60, 66–68`; `evaluation-loop.md:35–42, 82`).

The README preserves historical failures and NA, scopes earlier successes to their fixed versions/cases, and does not assert a K PASS (`README.md:44–50`). Its historical outcome counts were not independently checked in this restricted audit and must remain tied to their existing evidence.

## Optional next-candidate improvements

1. **Make independent context transport explicit.** `parallel-production.md:17` prohibits peer-image/prompt access; `evaluation-loop.md:15, 23` prohibits injected conclusions and demands blinded independent evaluators. These semantic requirements are sound. The coordinator reports that actual evaluation actors use fresh CLI sessions, so there is no established execution defect. For reuse with other collaboration tools, one short instruction to start fresh/filtered actor contexts would prevent accidental full-history inheritance of peer outputs, versions, prior verdicts, or scores. Do not change frozen K or call this a current failure.

2. **Close the measured-ratio check explicitly.** `SKILL.md:20, 48, 66` preserves requested ratios and reads actual dimensions, but the delivery step does not explicitly compute and compare the returned aspect ratio. A future revision can require `width/height` comparison, correction within the existing budget where supported, and disclosure of any unresolved mismatch. Report exact returned pixels; avoid treating a prompted “16:9” label or resize as proof of native ratio/detail. The evaluation loop already treats ratio as mandatory (`evaluation-loop.md:29`).

3. **Carry copy ambiguity into ordinary maker returns.** Evaluation uncertainty is detailed and appropriately bounded (`evaluation-loop.md:35–42`), and raster Unicode limits are acknowledged (`art-direction.md:71`). A short normal-production return distinction—confirmed copy versus ambiguous symbol/word with location and inspected display size—would reduce overconfident “copy checked” summaries (`parallel-production.md:23`). This need not import the full evaluation schema into routine production.

4. **Scope anti-copy wording to research inspirations.** `art-direction.md:36` has an absolute ban on importing a specific composition, while `SKILL.md:20, 50` and `art-direction.md:67` correctly honor user-requested composition preservation. Their intent is compatible because reference roles differ. A future wording clarification can explicitly distinguish researched inspirations from user-provided preservation/edit targets, preventing the anti-copy sentence from being used to discard a clear user request.

5. **Preserve 16:9 coverage without implying validation.** The evaluation loop supports different ratios but does not name 16:9 in its example constraint coverage (`evaluation-loop.md:17`). Future evaluation planning should explicitly retain at least one complete 16:9 case when horizontal quality is part of the authorized goal. The README’s failed/NA horizontal results should remain visible; they are not evidence that frozen K or future horizontal requests pass.

No recommendation here authorizes one-image patch claims, another actor run, a runtime thaw, or a quality guarantee.

