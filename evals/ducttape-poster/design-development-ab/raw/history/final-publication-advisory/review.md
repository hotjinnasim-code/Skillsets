# Final publication advisory

Three actionable items remain before the actual commit/main merge:

1. **Finalize R24 publication text after closure.** README:61 correctly says AB quality is pending today, and the PR draft:9 deliberately contains a publication-blocking R24 placeholder. Replace that placeholder with the actual closed outcome, counts, uncertainty, and verification references; update the README and link the archived R24 report. The checker scans local links and literal secret markers, but has no pending-marker/completion check and never reads the PR draft. A checker PASS cannot close this item. No quality PASS is presumed or required by this advisory.
2. **Publish the final index, not the currently staged predecessor.** All eight unstaged README/runtime files have different index and working hashes. Twenty-one untracked entries include current reference/layout files, scripts, research/development records, and rounds 15–23. The checker reads working bytes and accepts links merely because targets exist on disk (lines 47–76,85–92); it explicitly defers commit verification (line 110). Stage the intended final files after finalization, then compare the staged/committed runtime and linked-report tree to the intended freeze. A commit of the current index would omit these newer bytes and untracked deliverables.
3. **Correct the PR draft's exclusion claim.** Draft:3 groups the default information template with clay/object repetitions as merely lowered priority. The live policy, accurately summarized in README:13, excludes the defined template by default; repetitions receive lower priority. State those separately, with explicit user-scope overrides retained.

The 33 current README local file targets exist within Skillsets; no broken file target was found. Git metadata is wholly within README, the ducttape skill, and its evaluations (4,000 status entries). The checker fixed output does not yet exist.

Limits: Advisory only; the checker/tests were not run, no images or current critic output were viewed, no publication occurred, and no files outside this advisory directory were changed. Link anchors, final staged bytes, and later R24 results remain unverified.
