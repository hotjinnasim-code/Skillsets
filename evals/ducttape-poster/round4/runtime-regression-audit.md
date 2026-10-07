# Runtime regression audit — frozen candidate C

No runtime blocker found in the frozen live instructions; one optional wording improvement. Recorded runtime supports the three-maker fallback, with the stated coverage limits.

## Blockers

None found.

## Optional suggestion

- **O1 — Default count wording:** `references/parallel-production.md:11` still says to preserve five roles/five final images after line 3 establishes the user count override. Later five-only shorthand in `SKILL.md` and the UI default prompt has the same minor clarity risk. Prefer “requested total (default five)” at the concurrency fallback sentence. This is not a blocker: `SKILL.md:10,17,20`, the one-image maker contract and `parallel-production.md:3` make precedence executable.

## No-change passes

- **P1 — Default makers and concurrency:** The coordinator must assign five distinct one-image maker agents by default; all five run simultaneously if maker capacity permits. Lower capacity runs the supported number and queues remaining roles without creating other chats to bypass limits. Evidence: `SKILL.md:10`; `references/parallel-production.md:3,9,11`.
- **P2 — User count and one-image follow-up:** Explicit quantity overrides the default, aspect ratios are allocated within that total, and a one-image follow-up changes only the named image and requested part. Count ownership is central. Evidence: `SKILL.md:10,17,20,68,70,71`; `references/parallel-production.md:3,9`.
- **P3 — Ownership and recursion:** The coordinator owns exact copy, common constraints and distinct organizing relationships. Makers own concrete composition within their assigned one-image direction and report changes. Maker mode forbids recursive maker spawning. Evidence: `references/parallel-production.md:7,9,15,19`.
- **P4 — Peer output isolation and actual references:** Makers cannot read or reuse peer images/prompts; new calls do not automatically inherit earlier directions. Real user references are preserved and their role is specified using the current tool schema. Evidence: `SKILL.md:46,47,52,53`; `references/parallel-production.md:15`.
- **P5 — Exact copy and user style:** Exact spelling, spacing, numeric values, names, punctuation and fixed line breaks are retained. The new dense-copy editing guidance also preserves user-specified order. Explicit neon, chrome, 3D and other styles remain mandatory. Evidence: `SKILL.md:17,21,44,45`; `references/art-direction.md:25,49,51,59`.
- **P6 — Image tool and resolution claims:** Instructions require a real built-in image call and current supported arguments. A maximum-resolution prompt is explicitly distinguished from actual output control or proof; returned dimensions must be checked and upscaling is not original detail. Evidence: `SKILL.md:46,48,49,50,62,72`.
- **P7 — No repair budget reset:** Regeneration counts toward two automatic corrections per image. Coordinator and maker calls are combined; duplicate concurrent repair is prohibited and failed roles continue only within the remaining budget. Evaluation retains ordinary limits. Evidence: `SKILL.md:63,66`; `references/art-direction.md:83,85`; `references/parallel-production.md:17,19,23,25`; `references/evaluation-loop.md:47`.
- **P8 — Content direction comparison without templates or bans:** The changed comparison checks content identification, usable copy, organization and the nearest direction before dispatch. It accepts direct photographs, quiet titles, familiar type and a shared reading order when other spatial/editorial relationships differ. No color, effect, photograph, print style or font automatically passes or fails. Maker layouts are not centrally cloned. Evidence: `SKILL.md:27,28,34,38`; `references/art-direction.md:15,17,19,23,25,29,57,59,61`; `references/parallel-production.md:7,15`; `references/visual-research.md:72`.
- **P9 — Finite round4 evaluation scope:** The permitted case file explicitly declares a new user-requested phase, 14 initial outputs, at most two automatic repairs per new output, a 42-call phase cap and a 76-call combined cap including 34 historical calls. This is disclosed additional evaluation, not a silent extension of the historical budget. Evidence: `evals/ducttape-poster/round4/cases.yaml:17-32`.
- **P10 — References and metadata:** All six relative Markdown links in the live skill package resolve. UI metadata uses the correct skill token and is consistent with default production; metadata and evaluation-loop.md are unchanged against main. Evidence: `SKILL.md:27,33,35,43,76`; `references/evaluation-loop.md:39`; `agents/openai.yaml:1-4`; `git diff main -- skills/ducttape-poster`.

## Recorded runtime and limits

The permitted roster records 14 distinct maker agents, five distinct makers for the default case, three supported/actual simultaneous makers (four agents including coordinator), and three overlapping recorded native-call intervals. This supports the required capacity fallback. The case requests total 14 outputs: one default five, four explicit two-image cases and one new single-image case.

- The execution roster records 14 distinct makers, five distinct makers for the default case, three supported simultaneous makers, three actual concurrent makers, and three overlapping recorded native-call intervals. These aggregates support fallback execution. Raw timing/call logs were outside this audit and were not independently reconstructed.
- The permitted cases cover default five outputs, explicit two-output cases and one new single-image case. They contain no one-image follow-up edit. That behavior passes instruction review but is not runtime-verified here. A five-simultaneous execution is also untested because the recorded environment supports three makers.
- The standard skill-creator quick_validate.py was attempted with shell Python and bundled Python. Both stopped before validation because PyYAML is unavailable. No packages were installed. Local link existence and the simple frontmatter/metadata structure were checked directly; these do not replace the unavailable validator.
- No images, blind packets/mappings, image review reports, production prompts, manifests, call ledger or visual-quality evidence were opened. This audit makes no claim about generated-image quality or native tool-call argument compliance in recorded productions.

## Scope and inspection

Read-only audit against `main` at `b9895426b0f07e8b68b16e8748808085d5f8bcbc` (also HEAD). The live diff is four files, 21 insertions/11 deletions. No repository files changed and no image calls were made. The JSON companion records live file hashes.

Actual files read:

- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster/SKILL.md`
- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster/references/art-direction.md`
- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster/references/parallel-production.md`
- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster/references/evaluation-loop.md`
- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster/references/visual-research.md`
- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/skills/ducttape-poster/agents/openai.yaml`
- `/Users/nahyeonbin/.codex/skills/.system/skill-creator/SKILL.md`
- `/Users/nahyeonbin/.codex/skills/.system/skill-creator/references/openai_yaml.md`
- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round4/cases.yaml`
- `/Users/nahyeonbin/Desktop/_Codex/Skillsets/evals/ducttape-poster/round4/planning/execution-roster.json`

The standard validator was executed at `/Users/nahyeonbin/.codex/skills/.system/skill-creator/scripts/quick_validate.py`; it failed before validation on its PyYAML import.
