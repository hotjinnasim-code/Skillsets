# Final runtime and evidence audit

Scope: read-only instruction/artifact consistency and recorded production evidence. No generation, child agents, repository edits, visual-quality certification, or exhaustive verification of tool history. Only this report and `evidence-validator.py` were written outside the repository.

**PASS — live skill instructions.** No remaining concrete contradiction found for default five roles, explicit quantity/ratio overrides, explicit neon, five logical makers versus the three-worker limit, one-image follow-up, complete worker packets, nonrecursive one-image worker scope, peer isolation, common user references, native tool schema, shared two-correction limit, or failed outputs. Relevant rules: `SKILL.md:10,17–21,44,47–54,64,69,71–73`; `references/parallel-production.md:3,9,11,15,17,23,25`. Full scenario reasoning is in `runtime-audit.md`. The later default-five wording is qualified by the explicit quantity override; no universal style ban or approval step was inferred.

**PASS — skill identity and structure.** All six live files, the external candidate-B snapshot, and the repository candidate-B snapshot match `planning/candidate-b-hashes.json` byte for byte. The repository hash manifest matches it. Skill frontmatter and `agents/openai.yaml` parse successfully; five local Markdown links resolve.

**PASS — current recorded evidence.** The validator's final preselection run checked 187 unique image paths, native dimensions/hashes, preserved tool-source/original/final equality, recorded QA image dimensions and any provided hashes, supported native call arguments, exact ledger paths, and repository preview dimensions/hashes. All required paths exist. Evidence JSON covers 16 initial images (prior five plus candidate-A eleven), eleven fresh candidate-B images, and seven final repair/regeneration images.

**PASS — current call accounting.** C02's seventh repair now has a manifest and final file. Recorded calls are **34 = prior 5 + candidate A 11 + fresh B 11 + final repairs 7**, below the global 38-call cap. No earlier pending repair was counted as a completed output. The original-slot post-initial budgets are:

| Slots | Recorded post-initial calls |
| --- | --- |
| G01, G02, G04, C01, C02, P01, N01 | 2 each |
| G03, G05, P02, N02 | 1 each |

Fresh B calls count as first post-initial regenerations; budgets are not reset between versions or workers. Every finalized B/repair manifest corresponds to exactly one ledger call, with no orphan or duplicate call path.

**PENDING — selected final eleven.** `final-selection.json` is absent at this audit point while supplemental review continues. The validator reports this as a warning by default; `--require-selection` makes absence a failure. Once it exists, the validator checks exactly one selected image per original slot, frozen snapshot and source-root identity, selection/evidence correspondence, exact selected native and preview paths, dimensions, hashes, and equality of source/repository selection copies when both exist.

Limitations: hashes and dimensions establish file identity, not readable Korean, reference fidelity, aesthetics, or a high-end quality gate. Production-native sizes are not claimed as 4K or verified maximum resolution. Product images preserve the returned 1122×1402 pixels, a disclosed small deviation from exact 4:5. The instruction-only audit cannot prove future worker compliance; the recorded ledger cannot prove absence of unrecorded tool calls. Three simultaneous makers were supported and documented; five simultaneous makers were not tested.

Run the final read-only check after selection:

```sh
python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round3/evidence-validator.py \
  --source-root /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round3 \
  --live-skill /Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster \
  --evidence-root /Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round3 \
  --require-selection
```

The script writes no artifacts and exits nonzero for failed checks. It resolves external native paths against `--source-root`, previews against `--evidence-root`, and manifest-relative paths against each exact manifest directory; it never searches by basename or modifies images.
