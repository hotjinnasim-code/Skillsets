# Runtime staffing limit, recorded before independent review

At approximately 2026-10-07 22:33–22:35 UTC, root twice attempted a fresh `r6_c4_m3` with `fork_turns:none`; both were rejected with `agent thread limit reached`. A known older baseline worker follow-up also could not be resumed. A nested fresh child attempt by R6-C4-M1 was rejected with the same error. No image call was made for any rejected assignment.

Available completed R5 craft worker was successfully resumed for the ONE R6-C4-M3 role, with prior R5 history explicitly retained and no R6 peer output or critique supplied. This is an existing worker assigned a new case, not a fresh context. Its earlier R5 reviewer history cannot be erased by a prompt. Current skill/cases/directions/call ceilings remain frozen. Remaining work will use actual available workers and preserve staffing/procedural limitations; do not claim fresh contexts where workers were resumed, and do not count self-author reviews as independent external reviews.

No external R6 critic has been dispatched. Any deviation from the predeclared fresh three-critic whole-case procedure must be reported separately from visual scores; do not rewrite phase-plan.json or promote partial/contaminated review to full independent PASS. All 20 newly scheduled images will still be preserved and reported.

## Fresh external review recovery, before dispatch

The installed Codex CLI 0.159.0 supports a separate non-interactive `exec` session. A capability-only probe (no R6 images, no critic scoring) successfully wrote/read its own probe.json and confirmed `functions.view_image`. Its first launch rejected an approval flag in the wrong position before running; second launch moved the global flag before `exec` and completed. Both launch logs are retained. No credentials or model settings were read or changed; CLI uses saved authentication and its configured default model.

External critics will therefore run as fresh `codex --no-daemon ... exec --ephemeral --json` sessions, one opaque five-image packet and one profile per session, with no resume/fork/earlier conversation. Three fresh sessions per whole case stage, maximum 24 primary assignments, same action-first/full-copy/15-view/rubric protocol and no feedback to production. Only concurrency transport changes; the predeclared score gates, images, byte bindings, first/final separation and stopping rules stay intact. Root will preserve launch prompts, command argv, timestamps, session/event traces, exit status and raw reports. A missing or invalid review stays invalid, not a high-end PASS. Separate CLI sessions are not collaboration-tool spawns, and their actual transport will be identified.

Official workflow sources consulted for this recovery: [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) (fresh exec, JSONL events, output files, saved authentication) and [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) (captured behavioral traces and separate rubric review). These are procedural sources; they are not new poster-design reference research.

## Actual closure and dispatch

All 20 role selections were closed before review. The recorded resumed-maker exceptions are R6-C4-M3 (`/root/r5_tc3_craft`), R6-C4-M4 (`/root/r5_tc3_portfolio`) and R6-C4-M5 (`/root/round5_final_evidence_audit`). Their retained histories are disclosed in production-closed-registry.json. No extra generation was authorized by this recovery.

At 2026-10-07 22:59:12 UTC the 24-assignment primary review runner began, maximum three active fresh CLI sessions. Dispatch-plan.json pins the production closure; each launch/completion pins its three packet inputs and three raw outputs. CLI launch defaults are not evidence that the CLI used the root conversation's model. Exact saved-session identities are checked from JSONL thread.started events. Semantic image viewing and transcription remain critic observations; mechanical trace evidence is reported separately.
