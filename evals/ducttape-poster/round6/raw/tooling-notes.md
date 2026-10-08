# Round-six evidence tooling

`build_packet.py` and `summarize.py` operate only on recorded physical selections and critic outputs. They do not generate posters, select winners, repair images, resample after critic feedback, modify the frozen skill, or create ratings. The only image transformation is Pillow LANCZOS resizing to width 720 and longest side 320; anonymous natives retain exact source bytes.

Use the bundled Python at `/Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

## Frozen inputs and physical selection

Defaults are `planning/cases.json` and `planning/phase-plan.json`. The plan uses `cases:{path,sha256}`, a nonempty `frozen_skill_files:[{path,sha256}]` list, and `review:{independent_reviewers:3,seven_dimensions:[content_form,hierarchy,typography,space,image_material,emotion_control,ai_slop],unchanged_core_gate:string}`. Relative source paths resolve from this round-six root. The gate string retains all four core dimension names, `>=4`, and diversity.

Cases use `cases:[{id,request,copy:[exact_strings],expected_final_count:5,slots:[{id,ratio}],action_fields:{FIELD:exact_expected_reading}}]`. Omit `action_fields` or use `{}` for a nonaction case. The public preflight hides expected readings and full copy; it shows action field names and actual 720 paths only. A `copy` transcription retains exact required strings in original order; equality normalizes whitespace only.

Selection uses `selected:[{role,case_id,stage,final_native,sha256,width,height,manifest,manifest_sha256}]`. Every selected source native and manifest must already exist and match its pin. Complete cases require their exact five declared roles and unique native hashes. `--case` can select one complete case from a wider selection; no global twenty-image requirement is imposed on an individual wave.

```
python build_packet.py --wave first-case-a --selection planning/first-case-a-selection.json --case CASE_ID
python summarize.py --wave first-case-a --output planning/first-case-a-summary.json
```

Packets live in `blind-WAVE/`; the private source map lives in `private/WAVE-mapping.json`. Existing wave directories or mappings are refused. The builder stages copies and resizes in a temporary directory, rechecks source pins before sealing, and does not leave an incomplete public packet on failure. Treat every sealed input, mapping, preflight, protocol and critic raw as immutable. A failed attempt can leave a private mapping if the final directory rename itself fails; preserve it and choose a new wave instead of overwriting.

## Critic protocol and raw files

Each case needs three fresh profiles: editorial, craft, portfolio. Each profile saves `PROFILE-action-first.json` before opening `packet.json`, then `PROFILE.json` and `PROFILE.md`. A five-image case means fifteen actual native/720/320 view records per critic. The protocol gives the unchanged seven R5 anchors, AI-slop inspection details, diversity anchors, mandatory checks, full-copy transcription, residuals, and closest-pair schema. Expected gate targets and private source history are not in the packet.

Preflight uses `{reviewer,order_compliant,method,viewed:[{image_id,view:"usage720",path}],readings:[{image_id,path,fields:{FIELD:observed_string},uncertainties:[]}]}`. Nonaction cases still save unchanged `readings:[]` and `viewed:[]` before opening full copy. Main JSON retains the R5 reviewer/order/method/viewed/images/sets structure. `mandatory.use_readings` explicitly records `all_required_copy_legible_at720:boolean` and `observations:string`. The builder's `review-protocol.md` contains the complete schema.

An unchanged final physical set can reuse its initial review only through an explicit identical native/manifest/QA/packet binding; it must not be presented as a new critic run. For that case, run the initial wave summary and record the reuse separately. A changed complete final set requires a new anonymous wave and three fresh critics. These scripts do not silently reuse or redirect reviews between waves.

## Summary semantics and validation limits

The summary binds frozen plan/cases/skill sources, physical selection, source manifests and natives, private mapping, public packet/protocol/preflight, all native/QA bytes and dimensions, every raw JSON/Markdown/preflight SHA, and each raw score/transcription/set record. It requires exact seven integer 1–5 scores, complete anonymous image and set IDs, mandatory checks, all copy items, fifteen actual path records, and action-before-copy order attestations. The four core scores must each reach 4 for every image and every reviewer; case diversity must reach 4 for all three reviewers. Scores are never averaged. Closest-pair scores are retained with evidence but introduce no extra threshold. Noncore scores below 4 remain visible.

`recorded_evidence_integrity` and `predeclared_core_diversity_gate` are separate. A known quality failure stays `FAIL` even when another integrity check fails. Without a known quality failure, incomplete or invalid evidence leaves quality `NOT_ASSESSABLE`; it does not claim a pass. stdout is the default; `--output` creates exclusively and refuses overwrite. Exit 0 means complete PASS, 1 means integrity/quality FAIL, and 2 means an input error. Existing output can raise an exclusive-create error instead of returning a summary, so use a new filename.

Actual view entries and order attestations are the preserved critic records, not proof that a call or chronology occurred. The validator cannot prove semantic evidence locations, objective design quality, authorship, physical mechanics, print suitability, or universal future performance. The plan freezes the experiment before native calls; the scripts check SHA consistency and cannot independently prove that historical timing.

Both CLI help paths were checked with the bundled runtime. Python syntax, unchanged rubric text and safe missing-input/error behavior were checked without fabricated images or ratings. End-to-end packet construction and real critic summaries remain to be validated on the actual round-six artifacts when they exist.
