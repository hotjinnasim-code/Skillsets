# Delivery reliability analysis

The current delivery rule is already explicit. Repeating stronger prose in section 5 is unlikely to address the whole problem. The smallest useful change is to make delivery a top-level completion condition, turn maker handoff into a stable artifact contract, and prepare the final response from that contract.

## Evidence and plausible mechanisms

- **Production dominates the entry point.** The opening promises five generated posters and stresses style and first-generation quality (SKILL.md:8–12). The default invocation prompt is a long design brief without image display or original-download requirements (openai.yaml:4). Delivery appears only at SKILL.md:82–90. A completion summary can therefore remain the salient output pattern after a long production sequence. This is a plausible instruction-salience mechanism, not a finding about any particular GPT Work runtime.
- **The handoff is free-form and overloaded.** parallel-production.md:37 combines paths, NONE, dimensions, counts, reviews, remaining issues, conditional display/download references, and selection history in one paragraph. The coordinator must reconstruct the per-role selection and the usable references from narrative output. That leaves room for references to be absent, associated with a preview, or lost while summarizing. Line 47 correctly assigns final delivery to the coordinator, but provides no stable intermediate response artifact.
- **File existence and user delivery are different states.** SKILL.md:88 explicitly recognizes this distinction, including internal maker paths. It asks the coordinator to obtain real user-dialog references when missing, but the skill has no deterministic acquisition method across all environments. A valid maker path may be inaccessible to the parent; a parent-readable local file may still lack a user-download reference in GPT Work. More prose cannot manufacture that capability.
- **The previous test isolates the easy stage.** delivery/report.md:5–13 shows correct drafts from existing local fixtures and path/hash/dimension checks. Line 15 explicitly limits the claim to answer construction and local identity, excluding live GPT Work rendering/downloading. This does not establish omission rates after a full production/handoff run, nor identify the cause of the user's actual failures.

No failing runtime transcript, loaded-skill version, tool result, attachment transfer, or rendered final answer was inspected. Stale packaging, partial skill loading, inaccessible references, tool behavior, and final-answer instruction noncompliance remain unseparated possibilities.

## Smallest practical structural improvement

1. Put a short output contract immediately below the skill title: “Completion means the coordinator’s final answer individually displays every suitable selected poster and directly below it supplies that same selected original’s download link and pixel dimensions. A saved file or maker/tool output alone is incomplete.” Keep section 5 for environment-specific details.
2. Replace the lengthy default_prompt with a concise invocation that activates the skill, preserves the user's content and requested count, requests distinct styles, and explicitly names the image + original-link + dimensions final output. Let the skill carry design detail instead of duplicating it in the invocation.
3. Require one small handoff record per requested role: role ID; SELECTED/NONE; selected original path or actual returned file reference; width/height; actual display reference; actual original-download reference; delivery status (ready/needs transfer/blocked); remaining issue. Preserve attempt history separately. Missing references remain missing; they must never be fabricated from an internal path or assumed URL scheme.
4. After collection, create a ready-to-send response artifact whose ordered cards already contain each image, its matching original link and dimensions, plus unresolved roles. The coordinator's final step is to send this prepared content through the current conversation's supported media/file mechanism. A response.md can serve Markdown-capable environments; native-media environments need equivalent actual media blocks/references.

## Deterministic preparation helper

A small helper could validate role coverage, unique selected files, readable accessible files, returned dimensions and optional hashes; distinguish previews from selected originals; reject missing required fields; and assemble consistent response cards. This removes repeated manual reconstruction and can plausibly reduce omissions, but no reduction is measured here.

The helper must fail visibly if SELECTED lacks delivery-ready references. It cannot open inaccessible cloud/subagent files, move attachments into the current conversation without an available transfer tool, mint a valid GPT Work link, establish live user reachability from a local existence check, or force the model to send its prepared output. Do not silently omit such roles or regenerate images for a delivery-only failure. A preparation helper is an omission guard, not a universal delivery mechanism.

A follow-up evaluation should include the whole handoff-to-final path, missing references, parent-inaccessible paths, preview/original mismatches, partial NONE roles, and actual rendered/downloadable GPT Work outputs when that environment is available. Report fixture construction success separately from live delivery success.

Exact reviewed source paths, SHA-256 pins, and line ranges are recorded in read-pins.json. No production skill or repository file was edited.
