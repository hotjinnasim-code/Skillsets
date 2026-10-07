# Independent correction1 assembly audit

Read-only follow-up of the current checker, procedural extension, closed correction summary, `assemble_final14.py`, known-fail fourteen-image output, retained Round 4 sources, and planned `archive_round5.py`. No generation, image editing, new review, raw rewrite, existing script edit, or live-repository edit was performed. The new files from this follow-up are this note and the separately requested `retained-five-bindings.json`.

## Verified result

Running the actual checker with `--wave correction1 --procedural-extension planning/correction1-procedural-extension.json` returns exit **1**, **recorded-evidence integrity PASS**, and **predeclared quality gate FAIL**. Integrity errors are `[]`. The recomputed image bindings, all critic observations, lower-score records, set records, disagreements, gate failures and review procedures exactly equal the corresponding saved closed-summary payloads.

| Recorded observation | Verified count |
| --- | ---: |
| Current selected images | 9 |
| Current critics, including original failed-order craft | 4 |
| Current image × critic records | 36 |
| Current seven-dimension score observations | 252 |
| Current image scores below 4 | 27 |
| Core image scores below 4 | 18 |
| Noncore image scores below 4 | 9 |
| Set-diversity failures | 4 |
| Final assembly selected images | 14 |
| Final assembly image × critic records | 51 |
| Final assembly located gate failures | 22 |
| Final assembly other sub-4 scores | 9 |
| Recorded assembly binding errors | 0 |

All four current invitation-diversity scores are 3; garden and product diversity are 4 for all four critics. No averaging, critic exclusion or historical whole-set FAIL substitution was observed. The final assembly remains `predeclared_gate_pass=false`. Its saved current-summary and prior-evidence SHA references match the actual files.

## Procedural extension and observation preservation

The original craft preflight retains `order_compliant=false` and the failed-save disclosure. Its original nine image observations and all scores remain authoritative. Editorial, portfolio and fresh craft_ordered have valid recorded action-before-copy attestations; craft_ordered supplements the procedure rather than replacing the original craft scores. All four critics remain in the quality gate.

All current JSON, Markdown and preflight source SHA references match their existing files. The checker now handles the actual list/dictionary preflight variants and nested nearest-pair records. Method/order attestations obtained from unchanged Markdown are hashed and identified as attestations; this does not independently prove temporal order, actual viewing or semantic accuracy. The extension is embedded in the closed summary, although its input path/SHA is not separately listed in the summary's `inputs` object. Preserve the original extension file in the closed archive alongside the embedded content.

## Retained five: independently verified and saved bindings

`retained-five-bindings.json` contains the exact selected C01/C02/N01/N02/H03 sources, 15 native/720/320 view bindings, 15 image × critic records, three retained set records, relevant prior review procedures/preflight records and 63 explicit source files. Its initial saved SHA is `23dba7db47a352f79c631a807e1981f88a90bb36e7ccb4099f678fc8c9346c4f`.

Every retained selected native SHA agrees with the original mapping, packet, anonymous native viewed by the critics, and prior final evidence. All retained QA hashes agree with `view_file_hashes_at_binding`; 720-width and 320-longside dimensions were checked. Every relevant reviewer log covers the exact bound native/720/320 paths, with explicit usage/thumbnail aliases.

The explicit prior archive raw-report paths resolve from the prior final evidence's relative `raw_report` fields. Those archived reports and Markdown files are byte-identical to their original blind-wave source paths. No basename fallback was used. All retained per-image scores, mandatory/copy records, evidence and residuals agree with their raw reports. All retained set observations agree in every raw field, including membership, diversity, nearest pair, evidence and residuals. C01/C02 have diversity 4/5/4; N01/N02 have 5/4/4. H03 remains a singleton with no invented pair-diversity condition.

The bundle also preserves relevant original packet, mapping, protocol and D/d-final action/preflight files, plus the full prior closed metadata pins. Complete prior wave packets/reports/procedure metadata refer to unselected comparators as well. This is an explicit selected-five image archive scope, not a promise to preserve all prior native calls or every comparison image.

Bundle fields intended for root consumption:

- `selected_images[role].views[view]`: exact `path`, `sha256`, `dimensions`.
- `selected_images[role].reviewers[profile]`: explicit prior-archive and original raw paths/SHA, full raw image observation and selected view records.
- `sets[case].reviewers[profile]`: raw report absolute path/SHA and full raw set observation.
- `review_procedure[wave]`: complete prior procedure metadata, exact source inputs and selected preflight/view records.
- `files[]`: explicit source `path`, `sha256`, `kind` for portable source-to-blob indexing.

## Concrete omissions in the originally inspected assembly/archive implementation

These are verification or portability omissions, not observed correction1 source mismatches. Root has accepted follow-up repairs independently; this audit did not edit the tools.

1. The assembler hashes current raw reports but originally did not recompare each summary observation with the corresponding raw image's scores/mandatory/evidence/residuals. The current closed payload passes an independent recomputation today; a standalone future assembly should perform that comparison rather than trusting an `integrity=PASS` string.
2. Building a role dictionary originally collapses duplicate choice roles. Selected manifest SHA, manifest role/stage/final path, dimensions and selected binding stage/phase need exact checks in addition to native SHA. The actual correction1 selected records match their sources; the code-level checks were incomplete.
3. The original final14 assembly omitted retained native/720/320 view bindings and retained review procedures/preflights. Retained sets kept relative raw paths without absolute/SHA verification. The new selected-five bundle supplies these missing bindings without changing any raw review.
4. The originally planned archive copied retained raw JSON/Markdown and selected natives but omitted retained QA images and relevant prior packet/mapping/protocol/preflight inputs. Its portable index would therefore not resolve those retained review dependencies. Consume and SHA-verify the selected-five bundle's explicit files, and retain full prior pin files as raw metadata while stating the selected-image archival scope.
5. The archive currently refuses any failed final gate. This is appropriate for avoiding a PASS label on the known-fail selection, but a finite evaluation that terminates with FAIL still needs preservation under an explicit FAIL status. Do not turn an archive's existence into a quality PASS assertion.
6. The archive should reject a destination within the source root before traversing `r.rglob`, since a newly created archive inside that root can be rediscovered during traversal. The intended external evaluation-archive destination avoids this issue.

No archive was executed by this audit. A future final wave with three fresh critics should carry its exact current-nine records plus these unchanged five; the closed four-critic correction1 FAIL remains preserved history. Mixed C/D/E evidence must remain explicit. Recorded metadata integrity PASS does not certify visual quality, actual viewing, authorship, physical product performance, print suitability, universal future results or fresh all-E performance.
