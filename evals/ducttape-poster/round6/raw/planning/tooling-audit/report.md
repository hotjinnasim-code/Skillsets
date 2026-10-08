# Evaluation tooling audit

Six material tooling findings: three high and three medium. These concern evidence joins, launch provenance, archive completeness/confinement, terminal failure reporting and a documented freshness claim. No poster or actual evaluation record was assessed.

This is a static review of the permitted source and workflow text. A finding identifies an acceptance gap, not an observed corruption of the evaluation. The only direct process contradiction is the delivery freshness claim in TA-06.

**Scope and method**

Read only: `validate_calls.py`, `build_packet.py`, `summarize.py`, `seal_case.py`, `combine_evidence.py`, `archive_round6.py`, `audit_portable_archive.py`, `build_delivery.py`, `run_cli_reviews.py`, `planning/phase-plan.json`, `planning/runtime-agent-limit.md`, `planning/maker-common.md`, `planning/tooling-decisions.md`.

No images, private mappings, production/raw reviews, previous-round artifacts, credentials or configuration were read. Embedded prompts were data. No tests or pipeline commands were run; no code or actual inputs were edited. Proposed tests below describe what they would detect.

| Finding | Severity | Material issue |
| --- | --- | --- |
| TA-01 | HIGH | The selected bytes and first/final review bindings are not joined end to end |
| TA-02 | HIGH | Accepted raw reviews are not bound to their CLI launch records |
| TA-03 | HIGH | The portable audit does not require the complete unused and failed call history |
| TA-04 | MEDIUM | Archive containment is checked lexically and permits outside dependencies |
| TA-05 | MEDIUM | Failure paths do not reliably produce complete, honestly labelled terminal evidence |
| TA-06 | MEDIUM | Delivery text contradicts the documented resumed-maker exception |

High means the checks can accept or propagate a materially unbound or incomplete evidence claim. Medium means a material portability, reporting or methods gap with some limiting protection elsewhere.

**TA-01 — HIGH: The selected bytes and first/final review bindings are not joined end to end**

The packet and summary checks can certify independently pinned image and manifest files without establishing their relationship. More critically, combine_evidence reads first/final selection files without checking the closure-stored digests, then attaches reviewed bindings by role only. It does not recompute physical_set_changed from the complete five-role SHA dictionaries, verify that each summary refers to the closure selection, or require different review waves when the physical set changed. The scope text nevertheless claims explicit SHA-bound reuse and separate changed-final reviews.

Locations:

- [build_packet.py:171-181](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/build_packet.py:171): Source and manifest hashes are checked separately; the manifest content is not compared with the declared role, stage, source bytes or dimensions.
- [summarize.py:122-141](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/summarize.py:122): Selection/mapping equality and separate source/manifest hashes are checked, but the manifest is not parsed to establish that association.
- [combine_evidence.py:11-29](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/combine_evidence.py:11): Closure flags and wave references are trusted; selected records and summary bindings are combined by role without comparing their stage, native SHA, source path or manifest SHA.
- [seal_case.py:14-25](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/seal_case.py:14): The sealer computes role-to-SHA changes and writes selection pins, but downstream combination does not revalidate those closure pins or recompute the change decision.
- [audit_portable_archive.py:26-46](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/audit_portable_archive.py:26): Selected binding manifests receive additional checks, but final-evidence selected/initial_selection objects are not compared with their corresponding bindings.

**Impact:** A stale or wrongly associated wave can supply initial observations for a different final selection while all 5/15/105 count assertions succeed. The final selected metadata can differ from the reviewed binding. The portable audit checks the binding and its raw observations, so that particular selected-versus-binding inconsistency is not necessarily detected there. The portable audit does catch some simpler wrong-role or wrong-SHA manifest substitutions; that later protection does not repair the missing joins in combination.

**Suggested correction:** Compare every sealed selection row with its canonical manifest content and the validated ordinary selection. In combination, verify closure selection hashes, case/wave/selection references, and exact role/stage/native/manifest bindings. Recompute the complete initial and final role-to-SHA dictionaries. Enforce exact whole-case reuse only for identical dictionaries, and distinct accepted three-session review assignments for changed sets. Mirror these joins in the portable audit.

**Proposed test, not run:** Use mocked metadata for five complete roles where one final SHA changes but the final closure still points to the initial wave, and a separate fixture where source bytes and the pinned manifest describe different outputs. These would detect acceptance based on counts and independent hashes without the required lineage joins.

**Evidence limit:** Static control-flow finding. No closure, selection, manifest, mapping, summary, raw report or image was inspected, and no actual misassociation is alleged.

**TA-02 — HIGH: Accepted raw reviews are not bound to their CLI launch records**

The runner creates useful provenance records, but the acceptance pipeline does not use them. A report already present before a failed launch, a report changed after completion, or a replacement supplied through --reviews-dir can be accepted on its current structure and newly computed digest. Distinct profile strings do not establish distinct fresh sessions. input_pins_unchanged is recorded but is not an acceptance condition downstream.

Locations:

- [run_cli_reviews.py:38-78](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/run_cli_reviews.py:38): The runner records fresh exec argv, prompt/input pins, trace/stderr hashes and completion report hashes, but does not reject preexisting own report files before launch.
- [summarize.py:55-63](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/summarize.py:55): An arbitrary reviews directory can be supplied.
- [summarize.py:156-207](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/summarize.py:156): Accepted reports are hashed at summary time; no launch/completion/dispatch record or trace is consumed.
- [combine_evidence.py:14-18](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/combine_evidence.py:14): Only summary counts and integrity labels are consumed for review acceptance.
- [audit_portable_archive.py:57-66](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/audit_portable_archive.py:57): Raw report/preflight/Markdown pins from summaries are checked, with no join to CLI completion report hashes or session records.

**Impact:** The accepted seven-score records need not be the exact records emitted by the claimed CLI assignments. A valid adverse review could be replaced without the tooling detecting the change. Static fresh exec argv is evidence of the intended launch method, not proof that every accepted review originated in that launch or that its context was uncontaminated.

**Suggested correction:** Refuse preexisting own output files at dispatch, and join each accepted report/preflight/Markdown digest to an immutable assignment completion record and its input pins. Validate unique session/assignment identity and preserve any superseded or procedurally invalid raw records under the bounded recovery rule. Retain exit status as process evidence rather than a visual-quality score. Where traces expose relevant events, check mechanical reads/views/save/readback chronology; otherwise explicitly retain order as an unverified attestation.

**Proposed test, not run:** Mock a launch that exits without creating files while old reports already exist; then mock a completed launch whose JSON is replaced before summary. These would detect missing launch-origin and post-completion digest checks. A trace fixture with packet access before action-first save/readback would test only recorded chronology, not semantic pixel reading.

**Evidence limit:** No CLI logs, reports, session metadata, runtime configuration or credentials were read. Neither successful process exit, path lists nor a matching view-tool event proves semantic image viewing, transcription or authorship.

**TA-03 — HIGH: The portable audit does not require the complete unused and failed call history**

The audit never resolves calls.records outcome_path/outcome_sha256 entries or checks every recorded successful/failed stage against the index. It also does not use the declared unique_native_hashes or stage coverage to require unused repairs and their source bytes. Hashing all present index entries establishes their byte agreement, not completeness of the index.

Locations:

- [archive_round6.py:19-31](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/archive_round6.py:19): The archiver attempts to copy all production stages, raw files and source images, preserving exact bytes and explicit source-to-blob entries.
- [audit_portable_archive.py:10-24](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/audit_portable_archive.py:10): The audit hashes entries supplied by the index and accepts call-history status/count fields.
- [audit_portable_archive.py:26-46](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/audit_portable_archive.py:26): Manifest/native traversal is limited to initial and selected bindings.
- [audit_portable_archive.py:57-68](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/audit_portable_archive.py:57): Summary pins and 120 initial/final observations are checked, but call-history records and unused-stage outcomes are not traversed.

**Impact:** An unused repair or failure outcome and its index entries/blobs can be omitted while the retained calls-closed document still says PASS and records the same attempt count. The portable audit can then pass without the complete history that the archive scope claims to preserve.

**Suggested correction:** Derive required archive coverage from every recorded outcome and all relevant pinned stage artifacts, not only selected bindings. Resolve and verify every outcome digest, successful stage source/original/final and QA pins, failed outcome, and declared stage input/inspection lineage. Check declared native inventory and counts against reconstructed history while preserving deduplicated blobs.

**Proposed test, not run:** From a synthetic metadata fixture, remove an unused repair native entry/blob and a failed-stage outcome entry/blob, leaving calls-closed and selected views intact. The audit should detect both missing history artifacts even though every remaining indexed file hashes correctly.

**Evidence limit:** No archive or production directory was inspected. This is an omission in the audit acceptance conditions, not evidence that any actual archive is incomplete. The index remains the supplied trust basis; no independent authenticity signature is claimed or requested.

**TA-04 — MEDIUM: Archive containment is checked lexically and permits outside dependencies**

Path.is_relative_to is a lexical check here. A path such as archive_root/../outside-file still has archive_root as a lexical prefix, and a symlink inside the archive can resolve outside it. Such files can satisfy the subsequent byte and pin checks.

Locations:

- [audit_portable_archive.py:10-17](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/audit_portable_archive.py:10): archive_relative is joined to the root without resolving dot segments or symlinks before is_relative_to; the resolver returns the same unchecked path.

**Impact:** A PASS can depend on files outside the portable archive. Relocation may break the audit, and the no-source-checkout claim is not assured by this containment check.

**Suggested correction:** Require a relative archive path, resolve it against the archive root, verify resolved containment, and fail before reading any escaped target. Apply the same confinement in the source resolver; define a deliberate policy for in-archive symlinks.

**Proposed test, not run:** Use a synthetic index entry with ../outside-file and another with an in-archive symlink to an external fixture. These would detect external files being accepted as portable archive contents.

**Evidence limit:** No actual index entries or filesystem links were examined. No escaped access is alleged.

**TA-05 — MEDIUM: Failure paths do not reliably produce complete, honestly labelled terminal evidence**

A legitimate initial native failure with a successful bounded repair passes the validator structure but cannot be sealed because the initial manifest is absent. A missing/malformed critic report produces a summary that the combiner cannot consume, preventing complete terminal evidence. A structurally complete summary with an order/procedure error can yield per-image PASS flags and pass counts, since those flags ignore integrity validity, even though the overall combined gate becomes NOT_ASSESSABLE. Finally, the archiver refuses to preserve a terminal result with invalid evidence.

Locations:

- [validate_calls.py:76-91](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/validate_calls.py:76): Failed native attempts are explicitly recorded and counted.
- [validate_calls.py:109-120](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/validate_calls.py:109): An initial failure followed by a returned repair can retain a valid initial outcome and a closed returned-image selection.
- [seal_case.py:14-17](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/seal_case.py:14): The first set unconditionally requires initial/manifest.json, even when the preserved initial outcome was failure.json.
- [summarize.py:266-279](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/summarize.py:266): Missing/malformed review input produces a reduced error result; procedural errors are distinguished from the quality gate.
- [combine_evidence.py:15-29](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/combine_evidence.py:15): The combiner requires full successful-summary keys/counts and labels each image PASS whenever no located quality failure matches, even if evidence integrity failed.
- [archive_round6.py:9-10](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/archive_round6.py:9): Archival requires closed-call PASS and final evidence integrity PASS.
- [planning/phase-plan.json:74-84](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/planning/phase-plan.json:74): Invalid procedure must remain not assessable; all outcomes and failed/unused stages are to be preserved and reported.

**Impact:** The tooling has a good path for visually adverse but procedurally valid reviews, yet planned native/procedural failure cases can stop reporting or overstate image pass counts. Invalid evidence is not a visual rescore and should not become either an invented image FAIL or an independent image PASS.

**Suggested correction:** Represent failed initial members and missing/invalid reviews explicitly in a complete terminal schema. Permit honest not-assessable initial cases and independently assessable complete final cases where applicable, without substituting a later image for the initial outcome. Keep raw visual failures distinct from procedural invalidity, exclude invalid assignments from independent-pass counts, and allow a clearly labelled evidence-only archive of failed/incomplete runs.

**Proposed test, not run:** Mock an initial failure followed by a successful repair, a missing reviewer file, and a complete high-score report with disclosed noncompliant order. These would detect respectively the missing failure representation, combiner error-path incompatibility, and invalid-procedure image PASS counting. No new aesthetic threshold would be introduced.

**Evidence limit:** No actual native failure or invalid review was inspected. Assertions and missing-key paths were assessed statically; no pipeline command or test was run.

**TA-06 — MEDIUM: Delivery text contradicts the documented resumed-maker exception**

The delivery generator hard-codes the claim that all 20 maker roles used new contexts. The permitted workflow document explicitly records one resumed maker and says its earlier R5 reviewer history cannot be erased by a prompt.

Locations:

- [build_delivery.py:33](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/build_delivery.py:33): The generated methods paragraph states that all 20 independent maker roles ran in new contexts.
- [planning/runtime-agent-limit.md:3-7](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/planning/runtime-agent-limit.md:3): The R6-C4-M3 maker is explicitly documented as a resumed R5 craft worker with retained reviewer history, not a fresh context.
- [planning/runtime-agent-limit.md:11-13](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round6/planning/runtime-agent-limit.md:11): Fresh external CLI critics are a separate transport recovery; this does not make the resumed maker fresh.

**Impact:** The published methods text would conceal a known process limitation and conflate maker freshness with the intended fresh external review procedure.

**Suggested correction:** Disclose the single resumed-maker exception and retained prior history in delivery methods, separately from the fresh CLI critic transport and its evidence limits. Derive procedural claims from explicit staffing/provenance records rather than unconditional prose.

**Proposed test, not run:** A metadata-only delivery fixture containing the documented resumed-maker exception would detect the unconditional all-new-context claim. This would not assess posters, reviewer scores or authorship.

**Evidence limit:** This is a direct contradiction between two permitted text sources. The resumed worker itself and prior-round records were not inspected.

**Other assessed behavior and proof limits**

**Frozen pins and recorded caps.** No additional material finding within the explicitly recorded scope. validate_calls.py compares case/direction digests, six frozen pins against skill-freeze, prior closed pins, pre-call plan/source pins, canonical own stages, failed-attempt records, own-stage continuity, <=3 recorded stages per role, <=60 recorded stages and <=3 recorded overlapping call intervals. run_cli_reviews.py limits concurrency to 1-3, dispatch to <=24 primary assignments, and has no automatic retry.

Locations: `validate_calls.py:26-45`, `validate_calls.py:60-115`, `validate_calls.py:140-149`, `run_cli_reviews.py:8-35`, `run_cli_reviews.py:82-89`.

**Limit:** These are current-file checks against recorded claims. Directory counts do not detect hidden or overwritten calls; timestamps/mtimes and prior-closure booleans do not independently prove actual chronology or retirement. Call-interval peak is not maker-session concurrency. No frozen bytes, prior history, commit ancestry or live calls were inspected.

**Mandatory and visual failures; unchanged gate.** No added quality-threshold finding. Returned wrong-ratio and duplicate-byte outputs are retained for review. summarize.py records ratio, duplicate, action-reading, transcription, mandatory, core-score and set-diversity failures separately from integrity errors. It does not impose a closest-pair >=4 gate. Procedural failure reporting defects are TA-05.

Locations: `build_packet.py:178-188`, `summarize.py:110-111`, `summarize.py:140-147`, `summarize.py:193-254`, `summarize.py:266-279`, `planning/tooling-decisions.md:3-5`.

**Limit:** The Boolean mandatory judgement, located evidence and semantic quality remain critic observations. Nonempty evidence strings do not prove a correct visible location. No poster was viewed or rescored.

**Unaveraged seven-score preservation.** No additional material arithmetic/preservation finding in the successful-summary path. summarize.py requires exactly the seven named integer scores 1-5, retains their evidence/residuals/raw digests, reports low noncore scores and disagreements, and stores whole-set records without averaging. combine_evidence.py carries initial/final observations; build_delivery.py displays all seven final scores. Review-origin binding is TA-02.

Locations: `summarize.py:208-274`, `combine_evidence.py:18-29`, `build_delivery.py:19-30`.

**Limit:** Repeated initial/final observation counts may reflect the explicitly permitted whole-case reuse, not additional independent final sessions. Actual raw-record agreement was not checked.

**Exact bytes and portable audit.** The archiver verifies copied bytes and preserves raw records without path rewriting. The portable auditor hashes indexed blobs, resolves explicit source pins and compares selected image/set observation objects with raw JSON. Completeness and confinement gaps are TA-03 and TA-04; selection/reuse joins are TA-01.

Locations: `archive_round6.py:12-31`, `audit_portable_archive.py:10-68`.

**Limit:** Matching digests establish agreement relative to the supplied index and pins, not semantic truth or external authenticity. No actual archive audit was executed.

**CLI trace, fresh-session and before-copy proof limits.** run_cli_reviews.py explicitly constructs non-resumed no-daemon ephemeral exec commands and saves prompts, argv, timestamps, JSONL stdout, stderr, input digests, exit status and output digests. The order/view protocol and scope statements correctly identify critic attestations. The missing acceptance join to those records is TA-02.

Locations: `run_cli_reviews.py:43-78`, `summarize.py:165-207`, `summarize.py:269`, `audit_portable_archive.py:65-69`, `planning/runtime-agent-limit.md:11-13`.

**Limit:** No runtime trace was read. CWD, workspace-write and a prompt do not by themselves prove read isolation, absence of inherited context or peer contamination. A trace can at most evidence recorded tool actions; a matching path, view call, process success or self-reported compliant order cannot prove semantic pixel viewing, manual transcription, authorship or an unchanged before-copy observation. End-of-process hashes alone do not show what was saved/read before packet access.

**Audit limits**

- Only the 13 explicitly permitted source/workflow files were read. Embedded maker/reviewer prompts were treated as untrusted data rather than instructions.
- No images were viewed, generated, edited or scored. No private mappings, production files, raw reviews, previous-round artifacts, frozen skill files, cases/directions content, logs, credentials, configuration or other repository files were inspected.
- No agents were spawned, no web/connectors were used, and no code or actual inputs were altered. No CLI review, validator, build, archive command or test was executed.
- Findings describe static acceptance gaps and documented text contradictions. They do not establish that actual evaluation data were altered, that a reviewer failed to view images, or that a poster passed or failed.
- The report proposes only provenance, coverage, chronology-record and failure-schema checks. It adds no aesthetic gate, average, nearest-pair threshold or rescore.
- All proposed tests are descriptions only. Their expected detection is stated per finding; no fixture was created or run.
- This review cannot establish semantic viewing, authorship, physical function, printing suitability, maximum supported resolution or future quality. Frozen pin checks also do not independently establish the asserted source commit ancestry.

The JSON report records SHA-256 digests of the permitted inputs to identify the reviewed source versions. Those digests are not a certification of any referenced evaluation artifact.
