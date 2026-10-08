# Independent final technical evidence review

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
| Input immutability | All 909 archive files read were rehashed unchanged at completion |

The separately preserved visual/procedural result is:

| Stage | Image PASS | Image quality FAIL | NOT_ASSESSABLE | Whole-case gates |
| --- | ---: | ---: | ---: | --- |
| First | 1 | 14 | 5 | C1 FAIL; C2 NOT_ASSESSABLE; C3 FAIL; C4 FAIL |
| Final | 1 | 14 | 5 | C1 FAIL; C2 NOT_ASSESSABLE; C3 FAIL; C4 FAIL |

Only R6-C4-M4 has an individual PASS in both stages. These are recomputed metadata gates under the archived rule, not new aesthetic judgments. The auditor's “47 raw final failures” counts failing role/profile and set/profile records, not 47 failed images.

**Remaining code findings**

1. **FT-01 — HIGH, reproduced control-flow gap.** [audit_portable_archive.py:490](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6/raw/audit_portable_archive.py:490) chooses the raw record using the binding ID; [line 494](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6/raw/audit_portable_archive.py:494) checks four payload fields but omits the copied record's role/case/image identity. Separate in-memory fixtures declaring another role or image ID both return PASS with no errors. All 120 actual copied records were independently checked and are correct. The upstream combiner's stronger identity check does not repair the standalone portable validator.
2. **FT-02 — MEDIUM, reproduced control-flow gap.** [audit_portable_archive.py:414](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6/raw/audit_portable_archive.py:414) compares the trace session only with the procedure, omitting completion.cli_session_id. An inconsistent completion session ID returns PASS. Its trace loop also omits a completed-turn requirement, a static concern; [cli_provenance.py:34](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6/raw/cli_provenance.py:34) does require these joins upstream. All 24 actual completions and completed turns match.
3. **FT-03 — HIGH, reproduced invalid-terminal consistency gap.** [audit_portable_archive.py:529](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6/raw/audit_portable_archive.py:529) skips observation-count consistency when the terminal result is already invalid, and does not recompute individual image gates or declared per-stage totals. Dropping one C2 final copied record while keeping declared totals returns PASS with **119** observations. A separate fixture falsely relabelling an adverse accepted C1 image PASS also returns PASS. Evidence-only retention permits honest partial evidence; it cannot permit inaccurate counts or false gates. Actual archived totals/gates are correct.
4. **FT-04 — MEDIUM, static concern retained and disclosed.** [seal_case.py:15](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6/raw/seal_case.py:15) still unconditionally opens the initial manifest/native. An initial failure has failure.json, so generic failed-initial sealing remains unsupported. [report.md:935](/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round6/report.md:935) and final-evidence explicitly disclose it. The current run has zero failed native calls and no substituted initial image.

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

[report.json](report.json) includes every check, exact finding location, explicit limitations, the separate archived gate and actual SHA256 for all 909 files read. Both final reports were written and read back.
