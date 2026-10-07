# Round 3 runtime instruction audit

Scope: instruction consistency only. Read `SKILL.md`, `references/parallel-production.md`, `agents/openai.yaml`, and the art-direction, evaluation-loop, and visual-research references. No image generation, collaborator execution, or repository edits were performed. This is not evidence of image quality or measured behavioral success.

Result: **PASS for the requested instruction scenarios.** No concrete contradictory or missing rule was identified. **FAIL: none.** **Uncertainty:** actual tool execution, worker compliance, reference transfer, returned dimensions, and output quality remain untested.

| Scenario | Result and evidence |
| --- | --- |
| Sparse title-only new request produces five roles/images | PASS — `SKILL.md:8–10,16,20`; `parallel-production.md:3,11`. A request with no printable copy may ask for the missing copy; an explicit text-free poster can proceed. |
| Explicit two images with two ratios stays exactly two | PASS — `SKILL.md:17,20` prioritizes requested quantity and allocates multiple ratios inside that quantity; `parallel-production.md:3` matches role count to it. The later five-role wording in `parallel-production.md:11` describes the default established at line 3, not a quantity override. |
| Explicit neon is honored | PASS — `SKILL.md:17,21,35,68`; `art-direction.md:25,45`; `evaluation-loop.md:37`. Generic-effect preferences do not override explicit style. |
| Three available workers versus five is reported truthfully | PASS — `SKILL.md:10,44`; `parallel-production.md:11,25`; `evaluation-loop.md:13`. Five logical roles can run in batches, with actual concurrency reported separately. Actual available worker capacity must be derived from the current tool schema, including coordinator occupancy. |
| One-image follow-up does not launch a new set of five | PASS — `SKILL.md:10,69,72`; `parallel-production.md:3,9`. |
| Complete worker packet and one-image scope | PASS — `parallel-production.md:9` requires original request, full finalized copy, mandatory conditions/ratios, assigned direction, single final image scope, relevant instructions, and actual references with roles. |
| No recursive five-by-five production | PASS — `parallel-production.md:9` explicitly prohibits recursive maker spawning and centralizes total quantity. |
| Independent production without peer-image influence | PASS — `SKILL.md:48`; `parallel-production.md:15` prohibits reading peer images/prompts or using them as new-generation references. Root comparison occurs afterward at line 23. |
| Common user reference reaches every worker/call | PASS — `SKILL.md:48,53–54`; `parallel-production.md:9,15`. Required user references are preserved separately from prior generated drafts; unavailable references must be resolved. |
| Native tool schema; no invented size parameters or 4K guarantee | PASS — `SKILL.md:47,49–51,63`. A prompt-only maximum-resolution request is explicitly not proof of achieved maximum resolution; actual dimensions are checked where files exist. |
| At most two corrections across worker and root | PASS — `SKILL.md:64`; `parallel-production.md:17,19,23`; `art-direction.md:85`. Regeneration counts, worker/root calls share the same per-image history, and the same image is not corrected simultaneously by two workers. |
| Failed worker cannot count a nonexistent output | PASS — `SKILL.md:73`; `parallel-production.md:25`. `SKILL.md:67` permits counting an existing imperfect image while disclosing defects; it does not supersede the explicit prohibition on counting ungenerated images or nonexistent files. |

`agents/openai.yaml:4` expresses the default five-agent invocation, available-concurrency handling, and explicit-style fidelity. Quantity and follow-up exceptions are supplied by the authoritative skill instructions above. No runtime success is inferred from this interface text.
