# D continuation final metadata audit

Status: **PASS_OBSERVED_SIX_CALL_METADATA_WITH_VERIFICATION_GAPS_AND_PENDING_FINAL_CLOSEOUT**.

Six completed D native calls: initial and repair-1 for C02/P01/H02. Parent reported final repair-2 dispatch beginning after this snapshot; this report is not the completed D9 final selection audit.

Six completed D native calls pass exact saved-input object comparison, observed pre-call timing, source/native/final byte identity, recorded hash fields, PNG structure, dimensions and ratio tolerance. All six PNG chunk CRC checks pass. The initial H02 prompt.txt contains one extra terminal LF; its exact call-input.json matches the actual manifest input and the difference is already disclosed. P01 supplemental call-input-actual.json files were saved after the calls; separate call-input.json records predate both starts.

| Slot/stage | Actual PNG | Relative ratio error | Native SHA-256 |
|---|---:|---:|---|
| C02/initial | 1536×1024 | 0.000000% | `a2dffaa1da3ccb9c6aaa6ec80b4433adbbdc5d46110c30d6a535d480c5eb2e6c` |
| C02/repair-1 | 1536×1024 | 0.000000% | `c4146aa2372201e729f0784a871059625becf6a426dbeff4c2284249f5612afb` |
| P01/initial | 1122×1402 | 0.035663% | `7a05e63451729817e1915a7fe20ed31ce44fd5d7e3c3a2d219b66c3963804033` |
| P01/repair-1 | 1122×1402 | 0.035663% | `3ff11beb0fe38e771677706b01e655bfd40867d44a2385ec56be7280dc83b5a5` |
| H02/initial | 1254×1254 | 0.000000% | `b77ae3460f01e60b061f999db860de3a392e9710fba78acb983a099d48c41f42` |
| H02/repair-1 | 1254×1254 | 0.000000% | `77f0bccac07b86bba7ff4bc5476bfefe39726f55629aa3599bd03b589d7b6d4e` |

The frozen D tree is exactly six files and all declared hashes and sizes match. The live repository skill remains exact candidate C. Five files are byte identical between C and D; only references/art-direction.md differs. Repository D snapshot copies match. The frozen tree mtimes precede the earliest recorded D call; this supports the declared order without certifying immutable tool chronology.

The immutable C ledger SHA-256 is `4511964a4895fdaa605c3ee4a4c5e5e36005141614203affe5e0817f7ca03ced`; round3 is `0c243b3488d10bdb3d70bf6c3963319313e7998a18cdb3315d3c9b891846ec6a`. Both match D phase-plan and their repository copies. C32+D6=38≤42; round3 34+C32+D6=72≤76. The declared D9 boundary produces41≤42 and75≤76. Each D slot currently has one correction, within the two-correction limit. All six native calls omit both reference keys; first corrections are recorded as fresh regenerations.

The earliest evaluation’s20 calls remain separately reported by the original report (line16), and its report/evidence files are unchanged from repository HEAD. They are outside the round3+round4 cap76. Their hashes are recorded in the JSON.

Recomputed native-call interval concurrency matches the existing38-call record: C32, D6, maximum3. The capacity is3; default maker roles are5 logical roles. This does not prove five simultaneous native calls or five simultaneously active makers.

All six copied production manifests match. The earlier completed sync comparison passed; during final audit writing, three mutable source files changed after that sync (planning/root-view-log.json, call-ledger.json and validate_d.py), and six additional planning files await sync. The immutable C/R3 hashes still match. These mutable closeout files require later repository sync; fresh review files were excluded. The canonical validator returned INCOMPLETE with no errors and only the expected pending final-selection.json. Missing pending selection is not a failure.

## Located verifier coverage gaps

- **delivery_preflight_not_bound_original** (compose_delivery_evidence.py:18-25,39-45,75-77): Original scanned composer did not load action-first readings, preflight records or closed-wave summary; recorded native/usage/thumbnail coverage alone was included in the final predeclared gate. The original output could assert a final gate while omitting the predeclared action-first procedure. Closeout: Recheck the updated composer and verify raw first-reading coverage, exact packet paths, declared saved-before-packet evidence and its explicitly limited chronology scope after all final reviews close.
- **review_view_bytes_and_aliases_original** (compose_delivery_evidence.py:34-42; summarize_d.py original view-coverage block): Original composer matched native bytes, then counted exact view labels only. It did not verify viewed paths or usage/thumbnail derivative hashes. Native hash binding does not bind every displayed review asset. False failure for usage720/thumbnail320 aliases, or false recorded coverage for a wrong view path or derivative, was possible. Closeout: Recheck only the declared label aliases, exact packet paths and derivative hashes in the updated tools, with unchanged raw reports.
- **review_independence_and_closure_declaration** (compose_delivery_evidence.py:1,12,18-25,44-45,67-68): Closed independent reviews are described in strings; the scanned code has no closure assertion, distinct-agent identity check, forbidden-context/tool-history check, or full-report immutable hash binding. These process claims require additional recorded evidence and cannot be certified by the composer alone. Closeout: List exact report hashes and reviewer identities by wave, verify required roles are distinct within each wave, and separate recorded process compliance from exhaustive tool-history certification.
- **composer_schema_gate_fail_open** (compose_delivery_evidence.py:49-53,56-76): Original composer loops whatever score keys exist without requiring all seven dimensions, four core keys, 1–5 numeric finite scores, located evidence for every dimension, or exact declared 14 slots and six case membership sets. Cardinalities alone are asserted. A missing core score or incomplete set membership can evade the original final gate. Closeout: Bind a complete validated wave summary or assert the unchanged rubric schema and exact expected slot/case sets explicitly.
- **validate_precall_scope** (validate_d.py:35-46): Validator compares manifest prompt with prompt.txt after removing terminal newlines; it never reads call-input.json, call-input-actual.json, saved-input timestamps or prompt hashes. It cannot certify the separately requested exact pre-call input relationship. Current six inputs were independently checked in this audit. Closeout: Retain independent exact-object/input hash/time checks for any repair-2 calls; preserve the disclosed initial H02 terminal-LF difference.
- **validate_final_selection_provenance** (validate_d.py:61-65): Validator accepts any existing r-relative or absolute selected file with a matching hash after checking only three role labels; it does not require the selection to reference its own enumerated role/stage final.png or bind independent reviews/preflight. PASS is a native metadata result, not final-selection provenance or quality validation. Closeout: Verify each final selection against the exact own-role native manifest and the closed review mapping, packet and reports.
- **validate_count_and_portability_scope** (validate_d.py:23-25,55-60; sync_d.py:8-10,28): Validator enumerates three declared roles and at most repair-1/2; unrelated production role trees are not searched, several derived ledger/plan fields and concurrency/live-C boundary are not checked. Copied repository evidence uses manifests/<stage>/<role>.json and snapshots/candidate-d while validate_d expects production-d and candidate-d-skill plus a sibling external round3 folder. It does not count arbitrary unlisted manifest trees, certify concurrency, or run self-contained against the repository evidence layout. The actual canonical snapshot was independently fully enumerated and compared. Closeout: Use the canonical source root for this validator; independently enumerate all actual native manifest records, cap arithmetic, frozen/live boundary and repository copies.

These are verifier coverage findings, not proof that the recorded process or outputs failed. No current production metadata blocker was found.

## Required subsequent closeout

- Re-enumerate final native calls and validate new repair-2 exact input records, byte chains, dimensions, ratios, two-correction bound and concurrency/caps.
- Verify D final-selection and round4 final-delivery selection exact role/stage native hash provenance after blind review closes.
- Read the updated composer and verify exact native/derivative/report byte bindings and documented preflight scope; keep process metadata separate from visual judgments.
- Compare newly synced repository evidence and final selected manifests, preserving immutable closed C/R3 and earliest20 evidence.

The updated validator and delivery composer were independently read after the original static scan. The validator now checks exact call-input.json equality, role/stage, background, raw copy presence, UTC intervals/prefile mtimes, all four hash fields and own-role selected native path/manifest binding. The composer now handles only the declared usage720/thumbnail320 aliases, exact packet paths and complete unique coverage; D raw first-reading IDs/paths and declared saved-before-packet evidence; and native/usage/thumbnail hashes at binding time. It explicitly excludes exhaustive history and independent-identity certification.

These fixes resolve the original input/provenance and alias/path/preflight coverage findings at code level. Derivative hashes are at-binding hashes, not view-time hashes. The composer still requires separate complete seven-score schema/exact slot-set membership validation and reviewer identity/closure evidence. The parent will run full-nine native metadata and final review-binding validation after all final artifacts close. No pending final-selection file is counted as a failure.

## Limits

- No image generation, image editing, skill edits, review edits or image viewing performed.
- No active blind review reports read; no review score critique or visual quality judgment.
- File mtimes and recorded saved-before/start times are mutable metadata and do not independently certify exhaustive tool-call chronology.
- Hash identity, PNG dimensions and byte preservation do not prove exact visible copy, image material quality, physical operation, print suitability, or universal output quality.
- Known source/native/final paths were checked in the canonical workspace; repository previews are reduced exports rather than native originals.
- Original static coverage findings are preserved with post-scan code resolutions in JSON. Final repair-2 calls, final selections, binding execution and repository sync remain for parent closeout.
