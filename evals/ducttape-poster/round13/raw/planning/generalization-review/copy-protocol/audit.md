**Closed R12 fidelity and selection audit — independent advisory diagnosis**

This audit supports a narrow prospective workflow lesson: keep the observed reading, the declared comparison, the reading uncertainty, and the selection decision separate. It does not support changing the closed normalization, replacing a critic, or treating a maker’s matching transcription as independent confirmation. **The existing initial set remains NA and the selected set remains FAIL. This audit cannot make either set PASS.** No new quality ratings or replacement gate were produced.

I inspected the evidence after knowing the request, plan, maker observations and review findings. My viewing was informed advisory inspection, not blind reading or another scored critic session. I wrote only this file in the authorized `copy-protocol` directory. I did not generate/edit images, invoke a model API, mutate Git, contact agents, launch subagents, run a recording adapter/summarizer, export new canonical critic reports, or change Skillsets or R12 files. The pinned skill files were read as evidence, not executed as a production workflow.

The evidence root used below is `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12`.

**Preserved outcomes and the two fidelity disagreements**

The closed [final evidence](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/planning/final-evidence.json) and [report](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/report.md) record:

| Pool | M1 | M2 | M3 | M4 | M5 | Set |
| --- | --- | --- | --- | --- | --- | --- |
| initial | PASS | PASS | PASS | NA | FAIL | NA |
| selected | PASS | FAIL | FAIL | FAIL | FAIL | FAIL |

All six recorded diversity values are 4, and all six count-fidelity records are PASS for five members. Those findings do not cancel an individual low rating, mandatory FAIL, or unresolved NA. The recorded initial NA has precedence over the concurrent M5 FAIL; it is not an assertion that the initial pool had no observed failure. The preserved totals are 30 image/profile records and 210 score slots, with 210 valid scores, across six review sessions.

[`review_rules.md`](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/review_rules.md) pins `nfc-ws-optical-v1`. NFC and whitespace-run collapse preserve word spaces; soft wrapping becomes whitespace when `fixed_newlines:false`. Only exact middle dot `·` and slash `/` on `kind:"text"` entries have the declared surrounding-space exception. An en dash has no such exception. URLs are separately declared and do not receive the optical exception. Punctuation classes are not interchangeable. One exact-asset revisit can retain a resolved reading; an unresolved actual ambiguity remains NA. I read the matching implementation in `normalize`, `transcription_checks`, `image_record`, and `summary` in [`summarize.py`](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/summarize.py:99), without executing it.

| Record | Preserved time reading, zero-based copy index 4 | Preserved result |
| --- | --- | --- |
| M2 maker, initial / repair-1 / repair-2 | `14:00–16:30` in every recorded first read and comparison | Recorded equality true; no text issues. Initial dash ambiguity recorded resolved after native revisit. |
| M2 initial, all three critics | `14:00–16:30` | Mandatory text/style PASS; typography 4. |
| M2 selected, craft and editorial | `14:00–16:30` | Mandatory text/style PASS; typography 4. |
| M2 selected, portfolio | First read and resolved native revisit both `14:00 – 16:30` | Mandatory text/style FAIL; typography 3; layout PASS. |
| M4 maker, all three stages | `14:00–16:30` | Recorded equality true; no text ambiguities. |
| M4 initial, craft and portfolio | `14:00–16:30` | Mandatory text/style PASS; typography 4. |
| M4 initial, editorial | First read and unresolved native revisit both `14:00-16:30` | Mandatory text/style NA; typography 4; layout PASS. |
| M4 selected, all three critics | `14:00–16:30` | Mandatory text/style PASS; typography 4. Editorial space 3 still makes M4 selected FAIL. |

M2 selected portfolio’s [raw record](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/reviews/R12-C1/selected/cli/portfolio/portfolio.observations.json) describes visible full gaps flanking the dash, narrower digit gaps, and uncertainty about spaces versus optical kerning before the one revisit. Its revisit names the selected native SHA `386c0057589fdf31b626c7ec2e6b9f344a9b8bb1473d3ee3db04069aa61186a2`, retains the spaced reading and marks `resolved:true`. Under the frozen rule, the retained observed string and required `14:00–16:30` remain unequal. This is an internally relevant comparison consequence, not an invitation to strip dash spaces retrospectively.

In my actual M2 native and usage720 views, both initial and selected have conspicuous clear gaps on either side of the horizontal time separator. The selected illustration has stronger outlines and lacks the initial coral rays; the time line remains visibly gapped. This makes the portfolio concern understandable. It does not prove that repair introduced spaces: the initial is already visibly gapped, its critics recorded an unspaced reading, and the two pools have different assessment sessions. I cannot settle whether the gaps represent encoded spaces, kerning, generated glyph placement, or a difference in transcription judgment. The maker and other critics’ contrary readings remain evidence, not records to erase.

M4 initial editorial’s [raw record](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/reviews/R12-C1/initial/cli/editorial/editorial.observations.json) preserves its tentative hyphen reading and `resolved:false` after one revisit of native SHA `615ad92d715513ea4d9269d552e933718cc6985bf21da6c678dc335865b5db11`. The maker’s located observation calls the mark longer than a short hyphen and reads an en dash, while expressly disclaiming Unicode certification. I saw complete times separated by a short horizontal mark in the initial tabletop schedule; selected also shows a horizontal separator. Raster morphology does not let this audit authenticate U+002D versus U+2013. The initial editorial NA therefore remains unresolved in the closed evidence even though other observers accepted the reading. Selected is another asset and another pool; its accepted reading cannot resolve initial retrospectively.

I disagree with interpreting either issue as authenticated raster Unicode or with dismissing a retained adverse reading by majority vote. I also do not infer dishonesty or supplied-copy contamination from agreement with the required string. The records contain first-read attestations and actual disagreements; they do not isolate why those readings differ. A legible schedule, a layout PASS, and fidelity uncertainty can coexist.

**Selection uncertainty and a limited prospective lesson**

The five selection files preserve three returned calls per maker, two repairs, and zero returned-call failures: 15 attempts total. M1 selected initial; M2–M5 selected repair-2. The [plan](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/coordinator/R12-C1/plan.json) explicitly treats coordinates/type as suggestions, permits redesign for actual clarity, and distinguishes plan measurements from rendered reading.

M2’s recorded selection reason prefers cleaner outlines/reduced texture and removed rays over initial, and prefers repair-2 over repair-1 because repair-1’s 1671×941 native dimensions exceed the declared rounding tolerance. Its maker still records tonal variation and the unspaced time as matching. The prompts already request exact copy and preserved spacing; the repairs focus on material and ratio, not a diagnosed dash-spacing defect. This supports checking the complete returned copy again during selection, rather than assuming a protected-copy instruction guarantees preservation. It does not establish that instructions were absent or that another wording would succeed.

M4’s reason prefers the restored two-line identity/activity, cleaner scene, contained shirt and visible fabric junction, while retaining size/density limitations. Its selected editorial space 3 concerns the staggered schedule and participation blocks; craft and portfolio retain space 4. I saw the two distinct tabletop groups, but do not adjudicate that aesthetic disagreement or turn a common grid into a universal requirement.

The remaining selected failures must also survive any discussion of these two fidelity issues: all three critics give M3 image_material 3 and ai_slop 3 for dense repeated surface detail; M5 retains editorial hierarchy/space/emotion_control 3 and portfolio space/ai_slop 3. I saw the stronger repeated textile detail in M3 selected and the inward-ending left forearm in M5 selected. These observations support comparing the whole returned result, not claiming an isolated repair caused each low rating. M1’s selection of initial already shows that latest-stage adoption was not universal.

The pinned [art direction](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/snapshots/candidate-l/references/art-direction.md) and [evaluation loop](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/snapshots/candidate-l/references/evaluation-loop.md) already require small-symbol clarity, fixed-spacing preservation, raw readings separate from comparison, bounded exact-asset revisits, and whole-result selection. The justified recommendation is prospective reinforcement of those operations, not a demonstrated missing rule or a proven fix:

1. Establish which copy, spacing, line breaks and visual relationships the user actually protects before production. Keep flexible planning geometry separate.
2. During future inspection, retain the actual first read with its visible gaps/wraps and location before comparison; compare that retained read, not the requested string or repair promise. Record space-versus-kerning and glyph-class uncertainty explicitly when unresolved.
3. Use the predeclared revisit limit on the same asset when applicable. Keep uncertainty after an inconclusive revisit; do not obtain a preferred reading by repeated opening, regeneration, or changing exceptions.
4. During future bounded repair selection, compare complete returned copy, practical reading, image relationships and finish against the parent and earlier options. Explain remaining tradeoffs. A local improvement does not establish whole-image improvement or predicted critic PASS.

| Future request type | Conditional application of the lesson | Evidence limit |
| --- | --- | --- |
| Exact supplied copy | Preserve first reading and apply the frozen literal/normalization contract; distinguish mismatch from ambiguity. | Directly relevant to this R12 request. |
| No text | Check actual absence of unwanted text; do not invent a copy-transcription requirement, title, or schedule. Retain visual selection observations. | No no-text output was tested here. |
| User-fixed spacing/newlines | Preserve the user’s protected arrangement. Improve clarity through permissible size, proportion, contrast and surrounding layout; do not insert spaces or presume an optical exception authorizes a change. Any future comparison contract must be fixed compatibly before the test. | R12 declares all eleven entries `fixed_newlines:false`; it is not a test of a separate fixed-spacing/newline mode. |
| Mixed scripts | Read each script, numerals and punctuation as displayed; retain language-specific uncertainty without transliteration or wholesale space removal. | R12 has Korean, uppercase English and numerals, not arbitrary script coverage. |
| Unconstrained design | Evaluate the user’s actual communication/visual intent and returned relationships; do not create an exact-copy restriction, compulsory schedule, process diagram or fixed grid. | R12 has open style but eleven exact entries and explicit scene/action constraints; it is not wholly unconstrained. |

These are conditional workflow recommendations, not claims that they have been tested across those modes. They do not authorize a new image test, a runtime edit, normalization relaxation, rescore, critic replacement, or post-session export. Even hypothetical resolution of M2’s fidelity question would leave the other selected failures intact.

**Whole-pool closure and anonymous-label scope**

For the recorded scope, both pools contain the actual requested five roles. I read the linked [production closure](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/planning/single-five-production-closure.json): the last maker completion is 08:49:58.810353 UTC; production validation closes at 08:50:49.034721 UTC and records no prepared review jobs/directory or actual critic sessions at that check. The first critic launches are at 08:52:28 UTC. This supports all five maker selections and recorded production validation preceding review preparation/starts, within the recorded file/process scope. It does not authenticate arbitrary unrecorded activity or native concurrency.

I also read the membership/label fields in both actual packet files and the six launch/completion metadata records. Each critic observation lists all five members and fifteen ordered views. Mechanical comparison found their ninety initial view receipts matched the respective ordered packet path/SHA lists, and current image bytes matched the pins. This is receipt/byte verification, not proof of another observer’s semantic viewing or pre-score thought order. All six completion records report exit zero, one completed turn, unchanged inputs, and six distinct session IDs. I did not reread the JSONL traces. The closed report’s procedure/source/recording PASS remains its recorded finding, not a newly issued procedural gate.

Initial reviews complete by 09:02:37.611868 UTC; selected launches are at 09:03:31 UTC. Four selected native hashes change, so the selected pool has three fresh complete reviews, including M1, rather than reusing only M1’s scores. Both final-evidence reuse flags are false. Nine unique initial/selected assets yield 27 distinct image files and 30 phase-view slots because M1 initial supplies both pools. This does not turn the 15 returned stages into 15 independent styles or increase the case denominator above one.

The [prospective label declaration](/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12/planning/prospective-critic-label.json), timestamped 08:30:31 UTC with zero critic sessions, declares `anonymous-single-five` for both phases. I confirmed that exact label in both actual packets. It masks literal candidate L in that field before reviews. Raw R12 case/role identities and paths remain visible, as does required copy; it does not provide universal anonymity, copy-blindness, or an authenticated absence of version inference. The report explicitly limits historical R11’s K labeling; I did not inspect R11. The reported earlier three-of-five gallery is disclosed as preparation history and not critic input; I did not open that gallery/history, so I do not independently certify that assertion. The checked five-member packets, rather than that partial gallery, support the pool-membership finding.

**What I physically read and viewed**

“Read” here means content displayed to this auditor. Parsing/hashing a whole JSON file does not mean I semantically read every field. Large outputs that were truncated were supplemented with smaller relevant projections; I claim only the scopes below. None of the linked external studio/Canva works was opened, and no reference-image research was performed in this audit.

| Evidence under the root above | Actual semantic reading scope |
| --- | --- |
| `report.md`; `review_rules.md`; `planning/prospective-critic-label.json` | Complete displayed text. |
| `snapshots/candidate-l/SKILL.md`; `references/parallel-production.md`, `visual-research.md`, `art-direction.md`, `evaluation-loop.md` under that same snapshot | Complete displayed text of these five evidence documents. |
| `summarize.py` | Lines 1–122 and 333–570, plus function/gate search results; not the entire program or its provenance-validator body. |
| `planning/final-evidence.json` | Top-level structure, header/pins/counts/limits, maker terminals/counts/selection metadata, both complete stage gate objects, and inventory structure. Not every detailed caller record. |
| `raw-score-matrices.json` | All thirty score vectors, wave/role/profile/source/reuse fields and totals; the embedded summary pins were not a semantic read of the canonical summaries. |
| `coordinator/R12-C1/plan.json` | Request, copy, count, common constraints, authority/scope/scale/index/line conventions, planning checks; all five direction content/style/typography/nearest comparisons; relevant punctuation/search excerpts. Not every reference-transfer, layout coordinate or line-measurement object. |
| `checks/root-whole-five-visual-views.json` | Complete recorded view inventory, notes and limits. Its ROOT attestation is separate from my own actual viewing below. |
| `reviews/R12-C1/{initial,selected}/cli/{craft,editorial,portfolio}/{profile}.observations.json` — exactly six files | All procedure methods/flags, member/count/diversity and all thirty rating/status records; M2/M4 time raw/layout/ambiguity/revisit, mandatory issues, typography evidence and residuals in every session; all low-rating evidence/residuals in other images. Receipt sequences were displayed/projected and mechanically joined to packets. Not every other copy entry or every high-rating evidence paragraph. |
| `production/R12-C1-M{1,2,3,4,5}/selection.json` — five files | Selected stage/hash/files, call counts, retained three-stage identities/outcomes/native hashes, sealing and attestation semantics. Not every nested stage pin. |
| `production/R12-C1-M{1,2,3,4,5}/stages/{initial,repair-1,repair-2}/inspection.json` — fifteen files | All first-read strings, text-check metadata, time transcription/comparison/ambiguity/revisit, ratio, residuals and located observations; displayed first-read/display-limit/revisit/selection fields. Not every other full transcription or every other mandatory subobject. |
| Same fifteen stage directories, `call-input.json` | Complete prompts and actual exposed input parameters, including repair reference paths. |
| Additional linked `planning/single-five-production-closure.json` | Complete displayed closure record. Source/cache paths inside it were not opened. |
| Additional `reviews/R12-C1/{initial,selected}/packet.json` | Labels, case/wave/count/profiles, rules/helper pins, copy/requirements, all member/stage/native-hash lists, empty source/protected arrays and recording execution declaration. Not a complete semantic read of all packet fields. |
| Additional six critic directories, `launch.json` and `completion.json` — twelve files | Start/end/session/completion/identity/immutability metadata. Report byte pins were mechanically checked; prompts/traces/canonical critic reports were not semantically read. |

I physically opened **27 distinct poster files**, each once with `tools.view_image({detail:"original"})` and displayed the returned image. In each directory below I viewed exactly `original.png`, `usage-720.png`, and `thumbnail-320.png` in that order. These nine directories are the complete inventory, in my actual directory-view order:

| Directory under the evidence root | Three actual files viewed | Recorded view dimensions |
| --- | --- | --- |
| `production/R12-C1-M2/stages/initial` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M2/stages/repair-2` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M4/stages/initial` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M4/stages/repair-2` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M1/stages/initial` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M3/stages/initial` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M3/stages/repair-2` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M5/stages/initial` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |
| `production/R12-C1-M5/stages/repair-2` | `original.png`, `usage-720.png`, `thumbnail-320.png` | 1672×941; 720×405; 320×180 |

I did not view any repair-1 images, M1 repair-2 images, separate `final.png` aliases, source-cache originals, galleries, or user/reference images. Statements about those unviewed repairs are attributed to the read records. I did not make fifty-five new copy transcriptions, rescore the set, or conduct a blinded retrieval test. Current packet rules/helper/image pins and completed-report pins checked without discrepancies; the thirty matrix score vectors matched the six raw-observation files. A before/after check across this audit's write found all 96 snapshotted R12 evidence/image files unchanged. These checks verify recorded bytes/joins and do not authenticate raster text encoding, actual manufacturing, AI authorship, unseen-request quality, or isolated causal effects.
