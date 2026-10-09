# Delivery contract audit

Reviewed current `Skillsets` at commit `94ea7c51ac23b62b1bcb944057a6fbbba0f0139b`; exact file and excerpt hashes are in `audit-status.json`. Repository status was clean. This is a text-contract review; no repository files were edited, images generated, CLI agents run, or publication attempted.

## Finding

`SKILL.md` section 5 already requests showing each final image with a download link and dimensions. It does not explicitly require that outcome in the **parent's final user-facing answer**. The parallel handoff supplies selected paths or `NONE`, but does not require the native media and original download handles needed to surface a subagent's result. A summary can therefore satisfy the handoff while the user sees no poster or usable original link. The README's resolution paragraph has no delivery promise.

## Smallest recommended change

1. Strengthen section 5's opening delivery sentence: the final user-facing answer must visibly present **every suitable selected poster individually** and pair each with its **actual selected original's download link and measured pixel size**, using the current environment's supported native media or image/file rendering. The parent must forward subagent media and download handles into that answer; a subagent-only display, path summary, or textual completion report does not fulfill delivery.
2. Extend the existing parallel handoff sentence with the selected original's actual renderable media/file handle and actual original download handle. Label any preview, contact sheet, crop, or layout guide separately so it cannot replace the selected original. Add the same parent responsibility to the existing final-assembly sentence.
3. Add one short delivery promise to the README's existing resolution paragraph: suitable selected originals appear individually in the final answer with original downloads and actual dimensions.

Keep this outcome-based. Do not mandate `sandbox:`, an absolute local path, or a fabricated platform URL as universally valid syntax. Use handles actually returned or exposed by the current environment. Renaming or copying the preserved original is acceptable; resampling a preview does not make it an original.

## Actionable edge cases

- Match the requested roles and count. Display every suitable selection; report `NONE`/failed roles and their reasons without presenting rejected attempts as completed posters or manufacturing replacements to fill the count.
- A one-image edit delivers that one selected edited original, with its own display and original download. It must not trigger a fresh five-poster delivery.
- If a subagent returns only a private local path or a preview handle, the parent must expose the preserved original through an actually supported user-accessible media/file mechanism. If that is unavailable, state the delivery limitation and retain the original; do not claim an original download exists or invent a URL. This is distinct from a design role being `NONE`.

No runtime evidence was collected, so this audit supports the wording fix, not a claim that GPT Work rendering or downloads have been verified.
