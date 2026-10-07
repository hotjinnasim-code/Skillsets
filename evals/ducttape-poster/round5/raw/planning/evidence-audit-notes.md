# Round 5 independent evidence audit

Audit of the D/E phase plans, both per-phase validators, combined call audit, closed initial packet/mapping/reviews/summary, and prior Round 4 final delivery evidence. Read-only audit of existing records; no image generation, image editing, visual rescoring, review rewriting, or production changes. The two new files from this task are this note and `../summarize_blind.py`.

## Verified closed initial result

The actual closed initial package returns **recorded-evidence integrity PASS / predeclared core-and-diversity gate FAIL**. This was verified by running the new script against existing files, not synthetic or mock fixtures.

| Observation | Verified count |
| --- | ---: |
| Selected anonymous images | 9 |
| Raw critics | 3 |
| Image × critic records | 27 |
| Seven-dimension score observations | 189 |
| Image scores below 4 | 16 |
| Core image scores below 4 | 9 |
| Noncore image scores below 4 | 7 |
| Set-diversity observations below 4 | 5 |
| Nearest-pair observations below 4, retained but not an added gate | 8 |
| Score/diversity disagreements | 19 |
| Additional nearest-pair identity/score disagreements | 2 |

All 27 saved summary score records agree with the corresponding raw reviews. The complete 16 lower image-score records, including evidence and core flags, exactly match `initial-three-critic-summary.json`. All critics recorded successful mandatory checks; that does not erase the lower craft/quality scores.

Core failures remain:

- `G01 / X232`: editorial content_form=3; portfolio content_form=3 and ai_slop=3.
- Retained prior `H02 / X531`: typography=3 for all three critics.
- `P01 / X441`: editorial typography=3.
- `H01 / X230`: craft image_material=3 and ai_slop=3.
- Product set diversity=3 for all three critics; invitation diversity=3 for editorial and portfolio, and 4 for craft. Garden diversity=4 for all three critics, although all critics' nearest-pair scores are 3.

The first audit message to root incorrectly mixed prior Round 4 counts into this initial wave. It was promptly corrected after direct enumeration. **The authoritative initial numbers are 16 image sub-4 observations = 9 core + 7 noncore, plus 5 diversity failures.** Prior Round 4 separately has 17 located gate failures and 3 other sub-4 scores.

## Accounting omissions identified in the originally read validators

Root is independently repairing these existing tools; this note records the findings rather than modifying them.

1. Both per-phase validators iterate only declared roles and `initial`, `repair-1`, `repair-2`. Calls or partial records under unknown roles/stages can escape counting. A skipped repair stage can also evade sequential-lineage checks: `previous` can still refer to the initial stage when a later stage exists. The combined audit checks unknown stages only within declared roles and also misses unknown roles.
2. E's per-phase validator checks prior closed-history pins but omits `closed_initial_reviews_pinned`; the combined audit does check that list.
3. `combined-call-audit.py` returns exit 0 for `INCOMPLETE`. A consumer using exit status alone can mistake missing records for a finished audit. Both per-phase validators make incomplete success an explicit `--allow-incomplete` choice.
4. The combined audit trusts `native_call_count`, manifest times and final SHA fields. It does not itself establish integer count=1, final file existence/bytes, actual recorded arguments, source/original/final equality, required-copy prompt inclusion, ratio, or sequential own-image references. It must be used together with both per-phase validators.
5. D's original `whole_recorded_history=95+D` becomes a misleading whole-history label once E starts. E correctly avoids computing a whole total locally. Whole recorded history must be `95 + D completed records + E completed records`; partially started calls remain separately visible until manifests close. Counts are recorded evidence, not exhaustive external tool history.
6. Phase caps, whole caps, and overlap constraints should be derived from both predeclared plans rather than merely hard-coded labels. Interval overlap is based on manifest timestamps and is not proof of the actual runtime scheduler. Five garden maker roles are logical roles; the environment cap is three simultaneously.
7. Source hashes, file mtimes and prompt inclusion cannot certify actual applied skill version, actual maximum supported resolution, or visible copy quality. A one-second input-mtime allowance and saved invocation fields are limited recorded metadata. Repair records using a conversation-image reference cannot establish exact target bytes from that field alone; supplied local own-image references permit stronger binding. Regeneration still belongs to the existing original's correction budget.

At the 2026-10-07 19:30:38 UTC read-only snapshot, D had 10 completed recorded manifests plus a partial P02 repair-1; E had 3 completed recorded manifests. Combined audit reported `INCOMPLETE`, recorded total 108, and interval peak 3, with exit 0. These counts were a transient progress snapshot, not the eventual final totals.

## Binding and assembly requirements for current 9 and final 14

The initial summary already preserves raw scores, but it is not a complete selected-delivery proof: its records alone do not validate the mapping SHA pins, native/720/320 files, all-item manual transcriptions, action-first records, or actual recorded view-path coverage. The closed E plan pins the initial raw review JSON/Markdown/preflight files; the initial packet, mapping and review protocol are not included in that closed pin list. Preserve and explicitly hash those inputs in the closed assembly as well.

For each newly selected current-nine image, bind role, phase/version, stage, anonymous ID, native path, dimensions and actual SHA to its selected source. Check anonymous native identity and all three QA SHA pins. Do not relabel the failed D G01 as E, or the old closed H02 as the fresh E H02. D originals repaired with E guidance retain D accounting and lineage. The planned current selection is mixed evidence: E G01 plus D G02–G05, E H02 plus D H01, and D P01/P02. It is not a fresh all-E five-maker test.

For every selected image, carry all three authoritative raw critic sources with raw report SHA, all seven integer scores, full mandatory record/manual transcriptions, all seven evidence fields and residual/uncertainty records. Carry the native/720/320 viewed paths and separate immutable action-before-copy preflight records for the current invitation pair. A recorded path and order attestation support audit scope; they cannot prove that a view happened or that the asserted temporal order was followed.

The final fourteen need **current nine plus retained `C01`, `C02`, `N01`, `N02`, `H03`** from the exact prior selections, not the prior fourteen's overall gate result copied wholesale. Prior final evidence binds C01/C02 to D/d-final and N01/N02/H03 to C/wave1. Those five retained images have no recorded core sub-4 scores. Their prior unchanged two-member set diversity observations are C01/C02: editorial=4, craft=5, portfolio=4; N01/N02: editorial=5, craft=4, portfolio=4. H03 is a singleton, so preserve its individual evidence and do not invent a nearest-pair diversity requirement.

Every current set-diversity record must bind to **the complete selected member SHA set** from its actual review wave. Replacing an image invalidates reuse of a diversity judgment about the old membership, even if the remaining images are unchanged. The prior coast/neon membership is unchanged and can retain its exact closed set records. Keep every lower score and disagreement in the final assembly; no average, best-image substitute or consensus rewrite satisfies the declared gate.

## Neutral summary script

Run from the Round 5 root:

```sh
python3 summarize_blind.py --wave initial
python3 summarize_blind.py --wave correction1
```

Defaults are `blind-WAVE/packet.json`, `planning/WAVE-blind-mapping.json`, `blind-WAVE/reviews/{editorial,craft,portfolio}.json` and corresponding `PROFILE-action-first.json`, plus the D predeclared phase plan. Alternate existing layouts can be specified through `--packet`, `--mapping`, `--reviews-dir`, `--plan`, and `--root`.

The script reads only and writes JSON to stdout. It verifies selected native/QA SHA and dimensions, exact packet/mapping/set coverage, three reviewer identities, all seven integer scores and evidence fields, all-item manual-copy records, recorded native/720/320 path coverage, action-first date/deadline/full-URL readings and path records, and closed source pins. For the initial wave it also verifies the E plan's closed initial review pins. It emits every raw seven-score/mandatory/evidence/residual record, every set record, all lower scores, immutable preflight observations, and raw disagreements. Exit 0 means PASS, 1 means FAIL, and 2 means unreadable/malformed input. An unfinished wave does not silently pass.

Actual initial verification: exit **1**, integrity errors **[]**, selected bindings **9**, closed pin entries **17** (including repeated prior-history pins from the two plans), recorded integrity **PASS**, declared gate **FAIL**. The stdout summary is deliberately not saved by this audit task, preserving the requirement to create only the notes and optional script.

The script's integrity PASS is explicitly structural: nonempty located-evidence fields and manual-view/order claims are preserved critic attestations, not a second independent visual inspection. Its visual gate uses the raw critics' observed scores and mandatory flags. None of these records establishes authorship, physical product operation/capacity, print suitability, or universal future quality.
