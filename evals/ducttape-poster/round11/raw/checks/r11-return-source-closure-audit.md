# R11 returned-source closure audit

The ROOT helper compatibility failure is corrected at the existing evidence level. The before parser accepted 12 records and rejected all three M5 records with `Exactly one explicit returned source is required`. All 15 records now parse to their exact caller-recorded PNG, and all redundant representations agree.

The only helper changes are unfrozen ROOT `seal_single_five.py` and `close_production.py`. Exact before bytes, before/after hashes, complete diffs, rationale, and validation are retained under `checks/closure-helper-history/`; `r11-return-source-closure-fix.json` pins that history. No actor, frozen runtime, 19 frozen helper entries, recording method, native/critic budget, quality gate, or normalization changed. The 211 production/prepared-review files and 48 frozen pin rows were rechecked unchanged. Image bytes were hashed as opaque bytes; no pixels or quality scores were evaluated.

The added literal schemas are `explicit_returned_source_path`, `explicit_returned_png_paths`, and typed `metadata.hints` entries with `field == "result.output_hint"` inside the already supported metadata objects. Actual schemas are M1 `result_metadata.output_hint`; M2/M4 `returned_result_metadata.output_hint`; M3 `returned_metadata.output_hint` plus `explicit_returned_png_paths`; M5 `explicit_returned_source_path` plus `result_metadata.hints[0].value`. Every recognized scalar/list/hint representation must name the same single canonical absolute PNG. No manifest/cache/directory fallback exists. Twenty-one malformed/ambiguous/conflicting cases reject; fifteen positive schema cases and all 15 actual callers pass.

All 15 source identifiers join their caller-record persistence commands, `save-native --source` commands, manifest `source_argument`/`source.path`, source/original hashes, and full per-session generated PNG caches. All five fresh completion/CLI thread IDs agree; three PNGs per session cover exactly the recorded three calls. The table identifies CLI `command_execution` items in each maker's preserved `trace.jsonl`, with 1-based start/completion lines. These IDs are not native MCP event IDs.

| Role | Stage | Caller persistence | save-native |
|---|---|---|---|
| R11-C1-M1 | initial | item_10 21/22 | item_11 23/24 |
| R11-C1-M1 | repair-1 | item_16 32/33 | item_17 34/35 |
| R11-C1-M1 | repair-2 | item_22 43/44 | item_23 45/46 |
| R11-C1-M2 | initial | item_12 25/26 | item_13 27/28 |
| R11-C1-M2 | repair-1 | item_18 36/37 | item_19 38/39 |
| R11-C1-M2 | repair-2 | item_24 47/48 | item_25 49/50 |
| R11-C1-M3 | initial | item_12 24/25 | item_13 26/27 |
| R11-C1-M3 | repair-1 | item_19 36/37 | item_20 38/39 |
| R11-C1-M3 | repair-2 | item_25 47/48 | item_26 49/50 |
| R11-C1-M4 | initial | item_14 28/29 | item_15 30/31 |
| R11-C1-M4 | repair-1 | item_19 37/38 | item_20 39/40 |
| R11-C1-M4 | repair-2 | item_24 46/47 | item_25 48/49 |
| R11-C1-M5 | initial | item_11 23/24 | item_12 25/26 |
| R11-C1-M5 | repair-1 | item_18 35/36 | item_19 37/38 |
| R11-C1-M5 | repair-2 | item_24 46/47 | item_25 48/49 |

Direct native imagegen invocation/result events are absent from the preserved CLI traces. The maker argv uses `--ephemeral`; no persistent maker raw rollout/native event was found in the limited initial lookup. This audit authenticates existing caller serialization/save-native/session/cache/source/manifest joins; it does not independently authenticate the direct native tool return or semantic image viewing. No stronger native-event claim is introduced.

The actual sequence is preserved in `checks/r11-production-closure-failure-sequence.json`: the five maker sessions closed at pool closure `2026-10-08T07:03:59.152407+00:00`; ROOT production provenance closure then failed on the unsupported M5 schema; ROOT nevertheless built the gallery and prepared the initial review packet/three jobs before checking the failed result. Those prepared files remain byte-identical. This is a ROOT closure/preparation sequencing error, not a maker, quality, or raw source-record failure. Exact closure/preparation command timestamps are not invented from filesystem timestamps.

The former `reviews`-directory-absence proxy could not truthfully pass after preparation. The replacement checks strict preparation-only inventory and fixed job bindings, rejects any output directory/launch/trace/completion/report or unknown review artifact, and rejects live frozen-runner/review-exec processes. Actual observed critic sessions, start artifacts, and live critic/runner processes were zero. Eight synthetic start-evidence cases reject. The closure result records that the review directory and prepared jobs already existed, and that completed ROOT provenance closure did not precede review preparation. It checks before actual critic starts. Absence within the frozen runner protocol/file/process evidence does not authenticate arbitrary unrecorded activity.

The seal now pins completed ROOT production provenance closure and this failure-sequence record, preserves prepared-file pins, and requires every actual fresh critic start timestamp to follow corrected production closure. Both the direct-native-event visibility limit and the premature preparation sequence propagate to final-evidence limits. No production closure, seal, archive, native image call, or critic was executed by this audit. ROOT must rerun `close_production.py`, check its success, then launch the existing three fresh initial critic jobs.

Validation status: `PASS_SAME_EXISTING_EVIDENCE_LEVEL`. The standalone metadata/opaque-byte verifier and its full result are saved in the helper history. It executes only extracted parser/proof functions and isolated synthetic fixtures; it never executes closure or seal.
