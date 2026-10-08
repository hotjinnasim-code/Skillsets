from reviewlib import *
import datetime

ind=json.loads((O/'independent-checks.json').read_text())
audit=json.loads((O/'portable-audit.stdout.json').read_text())
fixtures=json.loads((O/'auditor-control-flow-checks.json').read_text())
pins=json.loads((O/'pinned-verification.json').read_text())
metrics=json.loads((O/'raw-observation-metrics.json').read_text())
e=js('raw/planning/final-evidence.json')
def loc(rel,line=None,pointer=None):
    return {'path':str(A/rel),'archive_relative_path':rel,**({'line':line} if line else {}),**({'json_pointer':pointer} if pointer else {})}
def evidence(rel,claim,line=None,pointer=None):
    return {**loc(rel,line,pointer),'claim':claim,'sha256':hashlib.sha256((A/rel).read_bytes()).hexdigest()}

findings=[
 {'id':'FT-01','severity':'HIGH','title':'Portable audit accepts incorrect copied observation identities',
  'classification':'reproduced_control_flow_fixture','source_locations':[loc('raw/audit_portable_archive.py',490),loc('raw/audit_portable_archive.py',494),loc('raw/combine_evidence.py',168)],
  'concern':'The portable auditor selects the raw observation using binding.image_id and compares only mandatory/scores/evidence/residuals. It never compares the copied observation role, case_id or image_id with the enclosing role/case/binding, or the complete copied record with its summary record.',
  'reproduction':'Changing only final-evidence images.R6-C1-M1.reviewers[0].role to R6-C1-M2, or its image_id to X8943, yields status PASS, exit 0, no evidence_errors. The real read-only archived bytes are verified first; the JSON alteration is injected only into the reader return value.',
  'impact':'The standalone audit can accept an incorrect structural observation association despite its stated no-waiver rule. The current archive has no such mismatch: every one of its 120 copied records was independently joined to the summary, binding and exact raw observation. The combiner has a stronger identity check, which is not a substitute for the portable audit.',
  'observed_in_unmodified_archive':False,'earlier_finding_relation':'TA-01 partially addressed; selected native/manifest joins fixed, copied-observation identity check still incomplete.'},
 {'id':'FT-02','severity':'MEDIUM','title':'Portable audit omits the completion session-ID join',
  'classification':'reproduced_control_flow_fixture','source_locations':[loc('raw/audit_portable_archive.py',405),loc('raw/audit_portable_archive.py',414),loc('raw/cli_provenance.py',34)],
  'concern':'The portable auditor joins thread.started only to procedure.cli_session_id. It does not also require completion.cli_session_id to match that trace event. It also does not require a completed turn in its trace acceptance loop, although the source-side cli_provenance checker does.',
  'reproduction':'Replacing only the in-memory W1BAF76CA/editorial completion.cli_session_id with wrong-completion-session yields PASS, exit 0 and no evidence_errors. The missing completed-turn condition is a static concern, not separately mutated in this review.',
  'impact':'An internally inconsistent completion identity can pass the portable validator. All 24 actual completions match their launch, aggregate completion entry, procedure, unique thread.started event and completed turn; no actual wrong session is alleged.',
  'observed_in_unmodified_archive':False,'earlier_finding_relation':'TA-02 largely fixed upstream and in current records; portable session acceptance remains weaker.'},
 {'id':'FT-03','severity':'HIGH','title':'Invalid-terminal branch skips truthful count and per-image gate validation',
  'classification':'reproduced_control_flow_fixture','source_locations':[loc('raw/audit_portable_archive.py',483),loc('raw/audit_portable_archive.py',529),loc('raw/audit_portable_archive.py',534),loc('raw/audit_portable_archive.py',535)],
  'concern':'When terminal evidence is already invalid, the auditor checks its overall NOT_ASSESSABLE label but skips its 120-observation consistency check. It never recomputes individual accepted image PASS/FAIL or compares declared per-stage record/score/image-gate totals with observed records. Partial invalid stages may be retained, but their declared counts must remain accurate.',
  'reproduction':'Dropping one C2 final copied observation while leaving declared totals and summaries unchanged returns PASS with 119 observed records. Independently, relabelling the valid adverse R6-C1-M1 final image as PASS returns PASS while original scores and mandatory observations remain adverse.',
  'impact':'Evidence-only mode can conceal missing copied evidence or a false individual PASS/count in otherwise retained invalid evidence. The real archive has the correct 60/60 records, 420/420 scores and 1 PASS/14 FAIL/5 NOT_ASSESSABLE counts. The tested relabel was in memory only; no score or archived gate was changed.',
  'observed_in_unmodified_archive':False,'earlier_finding_relation':'TA-05 partly fixed by honest current terminal evidence, but standalone archive acceptance still omits relevant consistency checks.'},
 {'id':'FT-04','severity':'MEDIUM','title':'Failed-initial sealing branch remains unsupported',
  'classification':'static_concern','source_locations':[loc('raw/seal_case.py',14),loc('raw/seal_case.py',15),loc('raw/combine_evidence.py',5),loc('raw/planning/final-evidence.json',pointer='/unsupported_utility_branches'),loc('report.md',935)],
  'concern':'The sealer unconditionally opens production/ROLE/initial/manifest.json and m.final for the first selection. A legitimately recorded initial failure has failure.json instead, so this branch cannot seal a complete first-case failure representation even when a bounded repair returns an image.',
  'reproduction':'Static control-flow review only; no native failure was created or replayed. The actual call inventory contains 47 successes and zero failures.',
  'impact':'The generic utility does not fully handle a promised failed-initial run. This limitation is explicitly disclosed in the final evidence and delivered report; it causes no missing current image and no later image was substituted for an initial.',
  'observed_in_unmodified_archive':False,'earlier_finding_relation':'TA-05 failed-initial subfinding remains, now honestly disclosed.'},
 {'id':'FT-05','severity':'INFO','title':'Retained equality annotations invalidate C2 without proving missing glyphs',
  'classification':'reproduced_metadata_discrepancy','source_locations':[loc('raw/summarize.py',38),loc('raw/summarize.py',239),loc('raw/planning/transcription-discrepancies.json',pointer='/rows'),loc('raw/planning/procedural-recovery-decisions.json',pointer='/decisions')],
  'concern':'Six original C2 assignments across first/final contain 16 equal=true annotations contradicting the unchanged whitespace-collapse comparator; all 16 preserve the same non-whitespace characters.',
  'reproduction':'Recomputed every original required/observed/equal transcription triple and matched all 16 diagnostic rows and their raw-report pins exactly.',
  'impact':'Both C2 stages and their five images remain NOT_ASSESSABLE. No primary comparator, raw observation or score was rewritten; zero additional assignments were dispatched because the allowed single remedial assignment could not supply all three valid profiles. This is a procedural/equality-record finding, not an independent visual judgment.',
  'observed_in_unmodified_archive':True,'code_defect':False}
]
checks=[
 {'id':'C01','status':'PASS','name':'Pinned inputs and immutable archive bytes','evidence':[{'pinned_files':21,'pins_matching':sum(p['match'] for p in pins)},evidence('archive-index.json','1125 unique original source identifiers, 902 unique indexed confined files, all exact SHA256; 1077 raw-source entries and 1125 required-source entries resolved without source fallback.')], 'details':{'index_and_required_byte_checks':ind['checks_executed'],'failed_checks':0}},
 {'id':'C02','status':'PASS','name':'Exact archived portable auditor execution','evidence':[evidence('raw/audit_portable_archive.py','Executed exact pinned script with python -B against this archive, exit 0; stdout and empty stderr captured in full only under output directory.'),evidence('checks/portable-audit.json','Retained auditor result matches the new baseline result exactly.')],'details':audit},
 {'id':'C03','status':'PASS','name':'Independent selected/source/native/manifest joins','evidence':[evidence('raw/planning/final-evidence.json','All 40 first/final sealed rows match evidence rows, summary bindings, private mappings, anonymous packet paths, closed outcome identity and exact native/manifest/QA pins.'),evidence('raw/planning/production-closed-registry.json','All20 final rows match closed ordinary role selections and staffing registry pins.')],'details':{'roles':20,'cases':4,'first_final_rows':40}},
 {'id':'C04','status':'PASS','name':'Every closed stage including unused repairs','evidence':[evidence('raw/planning/calls-closed.json','47 closed returned calls, 0 failures, 0 missing/pending; counts, own stages, pre-call pins, exact saved inputs, immediate parent references, source/original/final equality, dimensions, all47 inspections and all27 repair comparisons checked. All268 absolute PNG references in inspection/comparison records resolve to the same stage or immediate own parent.'),evidence('raw/planning/final-evidence.json','First/final native union has 33 hashes; 14 unused native stages outside that union are retained. 13 of 60 unused attempts are retired.')],'details':{'all_attempts':47,'role_call_counts_min':1,'role_call_counts_max':3,'unused_returned_stages':14,'retired_unexecuted_attempts':13,'failed_attempt_branch_in_this_archive':'not exercised','inspection_comparison_paths_checked':268}},
 {'id':'C05','status':'PASS','name':'Whole-case closure SHA changes and review decisions','evidence':[evidence('raw/planning/final-evidence.json','Complete five-role first/final SHA dictionaries change in all four cases; changed-member counts C1=2, C2=3, C3=4, C4=4. All have distinct waves and disjoint three-session first/final groups.')],'details':ind['case_closures']},
 {'id':'C06','status':'PASS','name':'Exact emitted CLI reports, input pins and sessions','evidence':[evidence('raw/cli-reviews/dispatch-plan.json','24 finite unique primary wave/profile jobs; concurrency3, no automatic retry, exact production-close pin.'),evidence('raw/cli-reviews/all-completed.json','All24 results equal individual completions; all launch fields unchanged; exact three report pins, prompt, stderr, trace, sealed packet/preflight/protocol pins verified. Every exit code0, one distinct thread.started and a completed turn, no turn.failed, no model override/resume/fork; recorded launch after all20 production close.')],'details':{'completed_assignments':24,'unique_sessions':24,'runtime_assignment_valid':24,'procedurally_accepted_case_stages':6,'procedurally_invalid_case_stages':2,'valid_assignment_origin_is_not_visual_procedure_validity':True,'missing_completions':[]}},
 {'id':'C07','status':'PASS','name':'Raw seven-score and set-observation preservation','evidence':[evidence('raw/planning/final-evidence.json','Every120 copied image records equals the corresponding exact raw mandatory/scores/evidence/residuals record; each has seven integer1–5 scores. All24 copied whole-set observations match raw members/diversity/closest_pair/evidence/residuals. No averaging or independent rescoring.')],'details':{'image_critic_counts':ind['image_critic_counts'],'raw_score_counts':ind['raw_score_counts'],'raw_observation_metrics':metrics}},
 {'id':'C08','status':'PASS','name':'Raw-derived current image and case gates','evidence':[evidence('raw/planning/final-evidence.json','Independent application of declared mandatory/copy/core>=4 gate reproduces both-stage 1 PASS,14 FAIL,5 NOT_ASSESSABLE. Only R6-C4-M4 passes in both stages. C1/C3/C4 case gates FAIL; C2 NOT_ASSESSABLE. Overall NOT_ASSESSABLE and recorded integrity FAIL retained.')],'details':ind['image_gate_counts']},
 {'id':'C09','status':'PASS','name':'Portable path confinement','evidence':[evidence('raw/audit_portable_archive.py','Every index path is relative, traversal-free and symlink-free; original identifiers are normalized lexically then mapped only to archive bytes.',30),{'fixture_results':'Rejects POSIX absolute path, traversal, Windows absolute/backslash path and even an in-root symlink before file reading; all five output-directory-only fixtures rejected.'}]},
 {'id':'C10','status':'FAIL','name':'Portable auditor rejects every tested structural/count/gate inconsistency','evidence':[{'artifact':str(O/'auditor-control-flow-checks.json'),'rejections':'Wrong native/manifest binding, wrong whole-case change flag and absent unused stage are rejected.','unexpected_acceptances':fixtures['unexpected_acceptances']}],'details':'FT-01 through FT-03 remain. In-memory reader-return fixtures exercise rejection logic separately from byte authenticity; the real input archive was never modified.'},
 {'id':'C11','status':'PASS','name':'Delivery claims and score/link tables','evidence':[evidence('report.md','All20 role/gate headings and final three-by-seven score tables match metadata; 20/20 initials and selected images, 33 reviewed union, 47 total calls, 24 sessions, C2 invalidity and three resumed makers honestly disclosed.'),evidence('gallery.html','Parsed HTML only, never rendered: all20 cards, gates, 420 final scores, selected and initial native links and usage720 src links match metadata and resolve within archive.'),evidence('findings.md','Separately states four contexts, both actual recorded peaks3, missing serialized image-tool events, whitespace-only diagnostic limits and unchanged comparator/observations.')],'details':{'gallery_cards':20,'resumed_roles':ind['resumed_roles'],'native_peak':3,'cli_peak':3,'request_contexts':4}},
 {'id':'C12','status':'PASS','name':'Comparator and procedural discrepancy disclosure','evidence':[evidence('raw/summarize.py','Primary normalization remains whitespace collapse; preserved earlier input version contains the identical comparator.',38),evidence('raw/planning/transcription-discrepancies.json','16/16 mismatch rows independently reproduced; same non-whitespace characters is diagnostic only.'),evidence('raw/planning/procedural-recovery-decisions.json','Two C2 stages invalid across allthree profiles; preserve records, no finite limit reset, no extra critic assignment.')],'details':{'transcription_discrepancies':16,'whitespace_only':16}},
 {'id':'C13','status':'PASS','name':'Recorded dimensions and honest resolution/viewing limits','evidence':[evidence('report.md','Maximum supported resolution was requested, only returned pixels recorded; no maximum-resolution/print/authorship certification.',933),evidence('raw/planning/review-trace-inventory.json','All24 raw traces reproduce the stated inventory and actual CLI peak3; zero recognized serialized image-view events, 15 declared main views per critic, 360 total stated view records. These are observations, not actual view/order proof.')],'details':{'all47_native_dimension_counts':ind['native_dimension_counts'],'native_peak_is_not_maker_session_concurrency':True,'semantic_viewing_and_full_order':'NOT_ASSESSABLE'}},
 {'id':'C14','status':'PASS','name':'Prompt wrapper discrepancy kept distinct from exact tool input','evidence':[evidence('raw/audit_portable_archive.py','Nine prompt.txt wrappers contain one additional terminal LF. Exact call-input JSON equals embedded manifest tool arguments; no bytes rewritten; adapter explicitly reported by portable auditor.',313)],'details':ind['prompt_extra_terminal_lf']}
]
earlier=[
 {'id':'TA-01','assessment':'PARTIALLY_ADDRESSED','evidence':'Current packet173–180, summary134–139 and combiner78–118/123–184/243–271 enforce source/native/manifest and complete set/session decisions. All actual rows pass. FT-01 is the remaining portable copied-record identity gap.'},
 {'id':'TA-02','assessment':'PARTIALLY_ADDRESSED','evidence':'Runner43–44 refuses preexisting own raw files; cli_provenance8–50 and summary172–176 bind exact emitted records. All24 actual assignments pass independent checks. FT-02 remains in portable completion/session acceptance.'},
 {'id':'TA-03','assessment':'ADDRESSED_FOR_CURRENT_RECORDED_HISTORY','evidence':'derive_inventory132–260 and audit301–362 traverse every outcome including all14 unreviewed native stages. Missing unused stage rejected. No failed outcome exists in the actual archive; generic failed-initial sealing remains FT-04.'},
 {'id':'TA-04','assessment':'ADDRESSED','evidence':'confined_path30–46 rejects absolute, traversal, backslash and symlink paths before reads; no source fallback. Independent all-index checks and five rejection fixtures pass.'},
 {'id':'TA-05','assessment':'PARTIALLY_ADDRESSED','evidence':'Current C2 data is preserved as NOT_ASSESSABLE; complete raw scores and recovery decision retained. Missing-review error schemas improved. FT-03 audit truthfulness gap and FT-04 failed-initial sealing remain; no missing current primary review.'},
 {'id':'TA-06','assessment':'ADDRESSED','evidence':'Closed staffing registry and report921 disclose three resumed makers C4-M3/M4/M5. Current source build_delivery61/156 derives the exception list; the earlier static report had only one documented exception. Fresh external CLI runtime claims remain separate.'}
]
limitations=[
 'No poster pixels were displayed or decoded. PNG bytes were hashed and only IHDR dimensions interpreted. No visual rescore, score optimization, generation or image editing occurred.',
 'No archive/input bytes were modified, no original source absolute path or earlier-round directory was inspected, no source-path fallback, web/connector access, credentials/runtime configuration read or agent spawn occurred. Retained prior closure metadata was read only through this archive index.',
 'All hashes establish byte identity against supplied pins and the index, not external authenticity, hidden/overwritten/unrecorded tool history, commit ancestry, authorship, or semantic source independence.',
 'Recorded native interval peak3 and CLI process interval peak3 are independently reproduced. They do not establish producer-session concurrency, exact image-tool scheduling, or actual image viewing.',
 'Zero recognized serialized CLI image-tool events occur in the available traces. Stated view records/manual transcriptions/order_compliant flags and partial command indices are attestations. Neither missing events nor available path records prove actual viewing, absence of viewing, complete order or semantic reading.',
 'The three resumed makers retain previous context; archival disclosure is verified, uncontaminated maker context is not proven. Four requests with five roles each are four request contexts, not twenty independent requests.',
 'All47 current calls returned native images. Generic failed-initial sealing remains unsupported and disclosed. No failed-native branch, unchanged full-set reuse branch or live procedural-recovery launch was exercised by this actual run.',
 'Control-flow fixtures inject metadata after archived-byte verification and are not a rebuilt cryptographically self-consistent alternate archive. Their unexpected acceptances reproduce local validator gaps only; none alleges corruption of actual pinned metadata.',
 'The retained earlier static tooling audit includes report, inputs, prompt, trace, stderr and final text but no launch.json or completion.json in its archived folder. Its six findings are reviewed as static evidence; its fresh-session/completion provenance is not authenticated by that folder.',
 'This active final reviewer launcher completion/final.txt is created by its parent after this turn exits; it is not part of the input archive and cannot yet be verified in this report. Current production/critic completion records are all present.',
 'Supported maximum native resolution, print suitability, real product function, human authorship, future quality and untested logo/screen/user-reference transfer are not certified.'
]

files=json.loads((O/'files-read.json').read_text())
unchanged=[]
for f in files:
    actual=hashlib.sha256((A/f['archive_relative_path']).read_bytes()).hexdigest()
    if actual!=f['sha256']:unchanged.append(f['path'])
    f['access_scope']='byte_hash_and_PNG_header_only_no_pixel_view' if f['path'].endswith('.png') else 'archived_text_metadata_or_code_bytes_read_and_hashed; semantic review is limited to checks cited above'
assert not unchanged
(O/'input-unchanged-check.json').write_text(json.dumps({'files_rehashed':len(files),'changed_files':unchanged,'status':'PASS'},indent=2)+'\n')

report={'schema_version':1,'review_type':'fresh_independent_final_technical_evidence_review','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'archive':str(A),'output_directory':str(O),'technical_integrity':'FAIL',
 'technical_integrity_basis':'Material archived auditor rejection gaps FT-01 and FT-03 remain, plus FT-02 and the disclosed unsupported sealer branch FT-04. This FAIL is a tooling-integrity judgment, not a visual failure or allegation of corrupted current evidence.',
 'current_archive_byte_integrity':'PASS','current_archive_association_integrity':'PASS','current_archive_count_and_delivery_consistency':'PASS',
 'portable_auditor_baseline':audit,'checks':checks,'findings':findings,'earlier_six_static_findings':earlier,
 'archived_visual_procedural_gate':{'archive_mode':'evidence-only','recorded_evidence_integrity':'FAIL','overall_visual_quality_gate':'NOT_ASSESSABLE','initial_image_gate_counts':ind['image_gate_counts']['first'],'final_image_gate_counts':ind['image_gate_counts']['final'],'case_gates':{c['case_id']:c['case_gates'] for c in ind['case_closures']},'passing_image_both_stages':'R6-C4-M4','raw_records_first_final':[60,60],'raw_scores_first_final':[420,420],'invalid_case_stages':['R6-C2/first','R6-C2/final'],'invalid_profiles_each_stage':['editorial','craft','portfolio'],'equality_discrepancies':16,'whitespace_only_discrepancies':16,'additional_assignments':0,'raw_observations_and_scores_unchanged':True,'portable_auditor_47_raw_final_failures_unit':'Failing accepted role/profile records plus set/profile diversity records; not 47 failed images.'},
 'missing_or_incomplete':{'scheduled_roles':[],'closed_native_outcomes':[],'primary_cli_completions':[],'emitted_primary_reports':[],'unsupported_generic_branch':'Failed initial native sealer branch: disclosed; no current failure exists.','retained_prior_static_audit_missing_files':['raw/planning/tooling-audit/launch.json','raw/planning/tooling-audit/completion.json'],'active_final_review_parent_completion':'Not yet available before this reviewer turn exits; outside input archive.'},
 'limitations':limitations,'files_read':files,'pinned_verification':pins,'input_unchanged_verification':{'status':'PASS','files_rehashed':len(files),'changed_files':[]},
 'output_artifacts':{name:{'path':str(O/name),'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()} for name in ['portable-audit.complete-output.txt','portable-audit.stdout.json','portable-audit.stderr.txt','portable-audit-execution.json','independent-checks.json','independent-pin-checks.json','auditor-control-flow-checks.json','raw-observation-metrics.json','inspection-path-checks.json','input-unchanged-check.json']},
 'reports_written_and_read_back':True}

md=f'''# Independent final technical evidence review

**Technical integrity: FAIL.** The supplied archive's current bytes, associations, counts and delivery claims independently pass. The failure concerns remaining defects in the archived validation code: it can return PASS for incorrect observation/session identities and inaccurate retained counts or image gates. No actual pinned record is alleged to have those defects, and no archive bytes or scores were changed.

The exact pinned portable auditor exited **0 / PASS**, with no byte or evidence errors. Its full output is saved in [portable-audit.complete-output.txt](portable-audit.complete-output.txt). Its separately reported evidence binding integrity is **FAIL**, reflecting the retained invalid review procedure; overall visual quality is **NOT_ASSESSABLE**. This baseline does not override the rejection gaps found below.

| Independently checked current evidence | Result |
| --- | --- |
| Pinned inputs | All 21 supplied SHA256 pins match |
| Portable archive | 1,125 source identifiers; 902 distinct indexed files; every byte pin confined and matched |
| Closed production | All 20 roles; 47 returned native calls; no failed/pending/missing call or selection; 13 unused attempts retired |
| All-stage coverage | 47 native hashes, 47 inspections, 27 repair comparisons; all stages checked, including 14 outside the first/final review union |
| Exact associations | All 40 first/final selection rows join to canonical stage, manifest, native/source bytes, summary, anonymous mapping and packet |
| Changed final sets | All four changed: C1 2 members, C2 3, C3 4, C4 4; separate disjoint three-session first/final groups |
| CLI provenance | All 24 jobs and individual/aggregate completions; exact emitted JSON/Markdown/preflight and three input pins; 24 unique session events, completed turns, exit 0 |
| Raw preservation | First 60 records / 420 scores; final 60 / 420; all seven unaveraged integer scores and mandatory/evidence/residual/set records match raw reports |
| Delivered gallery/report | All 20 card identities, gates, native/initial/use-size links and final score tables agree with metadata; confined links exist |
| Actual recorded concurrency | Native call interval peak 3; CLI process interval peak 3; producer-session overlap is not established |
| Input immutability | All {len(files)} archive files read were rehashed unchanged at completion |

The separately preserved visual/procedural result is:

| Stage | Image PASS | Image quality FAIL | NOT_ASSESSABLE | Whole-case gates |
| --- | ---: | ---: | ---: | --- |
| First | 1 | 14 | 5 | C1 FAIL; C2 NOT_ASSESSABLE; C3 FAIL; C4 FAIL |
| Final | 1 | 14 | 5 | C1 FAIL; C2 NOT_ASSESSABLE; C3 FAIL; C4 FAIL |

Only R6-C4-M4 has an individual PASS in both stages. These are recomputed metadata gates under the archived rule, not new aesthetic judgments. The auditor's “47 raw final failures” counts failing role/profile and set/profile records, not 47 failed images.

**Remaining code findings**

1. **FT-01 — HIGH, reproduced control-flow gap.** [audit_portable_archive.py:490]({A}/raw/audit_portable_archive.py:490) chooses the raw record using the binding ID; [line 494]({A}/raw/audit_portable_archive.py:494) checks four payload fields but omits the copied record's role/case/image identity. Separate in-memory fixtures declaring another role or image ID both return PASS with no errors. All 120 actual copied records were independently checked and are correct. The upstream combiner's stronger identity check does not repair the standalone portable validator.
2. **FT-02 — MEDIUM, reproduced control-flow gap.** [audit_portable_archive.py:414]({A}/raw/audit_portable_archive.py:414) compares the trace session only with the procedure, omitting completion.cli_session_id. An inconsistent completion session ID returns PASS. Its trace loop also omits a completed-turn requirement, a static concern; [cli_provenance.py:34]({A}/raw/cli_provenance.py:34) does require these joins upstream. All 24 actual completions and completed turns match.
3. **FT-03 — HIGH, reproduced invalid-terminal consistency gap.** [audit_portable_archive.py:529]({A}/raw/audit_portable_archive.py:529) skips observation-count consistency when the terminal result is already invalid, and does not recompute individual image gates or declared per-stage totals. Dropping one C2 final copied record while keeping declared totals returns PASS with **119** observations. A separate fixture falsely relabelling an adverse accepted C1 image PASS also returns PASS. Evidence-only retention permits honest partial evidence; it cannot permit inaccurate counts or false gates. Actual archived totals/gates are correct.
4. **FT-04 — MEDIUM, static concern retained and disclosed.** [seal_case.py:15]({A}/raw/seal_case.py:15) still unconditionally opens the initial manifest/native. An initial failure has failure.json, so generic failed-initial sealing remains unsupported. [report.md:935]({A}/report.md:935) and final-evidence explicitly disclose it. The current run has zero failed native calls and no substituted initial image.

Reproductions altered only JSON objects returned in memory after the confined reader verified real bytes. They did not rebuild a byte-consistent alternate archive, alter inputs, change a score, or view pixels. The source archive's ordinary native/manifest substitution, incorrect changed-set flag and missing unused-stage outcome are rejected. All five traversal/absolute/backslash/symlink fixtures are also rejected. Full results: [auditor-control-flow-checks.json](auditor-control-flow-checks.json).

| Earlier static finding | Reassessment |
| --- | --- |
| TA-01 selected/source/first-final joins | Main joins fixed and current data verified; FT-01 copied identity gap remains in portable audit |
| TA-02 raw CLI origin/session pins | Upstream origin checks and actual24 pins verified; FT-02 portable completion session check remains |
| TA-03 unused/failed history | Complete current all47 inventory enforced; 14 unreviewed stages included; no failed call exists here |
| TA-04 path containment | Addressed: confinement precedes reads; no source fallback; rejection fixtures pass |
| TA-05 honest failure paths | Current C2 NOT_ASSESSABLE handling works; FT-03 and unsupported failed-initial sealer remain |
| TA-06 resumed-maker disclosure | Addressed: report and registry disclose C4-M3, C4-M4 and C4-M5 |

C2 first/final retain all three original profiles and their scores. Recomputing original transcription triples reproduces **16/16 whitespace-only equality discrepancies**: equal=true conflicts with the unchanged whitespace-collapse comparator, while non-whitespace characters match. The earlier retained summarizer contains the same primary comparator. No observations were rewritten or diagnostic whitespace removal substituted for the gate. Both stages stay NOT_ASSESSABLE; no additional assignments were launched because one allowed remedial assignment could not supply three valid reports. This does not prove missing glyphs. Nine native prompt.txt wrappers also have one extra terminal LF; the saved call-input JSON remains exact, and the auditor explicitly lists these adapters.

The report honestly describes **four request contexts**, not twenty independent requests, and **three resumed makers**. All47 native headers reproduce 28 images at 1024×1536, 4 at 1122×1402, 10 at 1254×1254, and 5 at 1536×1024. Maximum supported resolution was requested, but only returned dimensions are established.

There are **zero recognized serialized image-view items** in all24 CLI traces. The 360 declared main views, transcription statements, order flags and partially visible command order are reviewer records. They prove neither actual semantic viewing/full order nor absence of viewing. Runtime/file/session joins are separate from visual attestation. No pixels were displayed or decoded, and no external source, earlier-round directory, credentials/configuration, web, connector or agent was used. Retained prior-closure metadata was resolved only through the archive index. Hashes do not authenticate external history, commit ancestry, hidden calls, authorship, real product function, print suitability or future quality.

All current primary critic completions and emitted reports exist. The retained earlier static audit folder has no launch.json or completion.json; its runtime freshness/completion is not authenticated here. The active final-review parent's completion record is created only after this reviewer turn exits and is outside the input archive. Failed-initial sealing, unchanged-case review reuse and actual procedural-recovery launches were not exercised by the current run.

[report.json](report.json) includes every check, exact finding location, explicit limitations, the separate archived gate and actual SHA256 for all {len(files)} files read. Both final reports were written and read back.
'''
(O/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(O/'report.md').write_text(md)
back=json.loads((O/'report.json').read_text());backmd=(O/'report.md').read_text()
assert back['technical_integrity']=='FAIL' and len(back['files_read'])==len(files)
assert back['reports_written_and_read_back'] is True and backmd==md
verification={'status':'PASS','reports_read_back':[{'path':str(O/name),'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest(),'bytes':(O/name).stat().st_size} for name in ['report.json','report.md']]}
(O/'report-readback-verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps({'technical_integrity':back['technical_integrity'],'current_archive_byte_integrity':back['current_archive_byte_integrity'],'current_archive_association_integrity':back['current_archive_association_integrity'],'findings':len(findings),'files_read':len(files),'reports_read_back':True,'archived_visual_gate':back['archived_visual_procedural_gate']['overall_visual_quality_gate']},indent=2))
