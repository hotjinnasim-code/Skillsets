# R7 closure/archive helper audit

Scope: read-only source inspection of `seal_round7.py`, `archive_round7.py`, `verify_archive.py`, `build_gallery.py`, frozen `summarize.py`, v2 preparer, source checker, and existing actual production manifests/completions. No images generated, source changed, scores read or evaluation outcome invented. This report is the only file written. Actual critic integration/portable replay is still pending.

## Findings to address before closure

1. **Portable replay can crash on a retained NA record.** `verify_archive.py:53` indexes `record['scores']`. Frozen `summarize.py:image_record` legitimately returns an NA missing-record object with no `scores` key. Preserve the same absence using a presence check plus `.get()` comparison rather than requiring a field the frozen engine does not create. This is an archive-validator repair only; keep raw NA evidence and original summary unchanged.

2. **Reuse binding is not independently checked at final closure/replay.** `seal_round7.py:62–74` trusts readiness.mode and pins the reuse file without validating its mapping or selected packet against the initial packet. `verify_archive.py:44–45` skips the second reference to the same summary without validating selected packet/reuse context. The v2 preparer already enforces exact whole-case context, native/stage/view identities and three actual critics; closure and portable replay should check those bindings again, including N=1, to detect stale/mismatched reuse metadata. No fresh critic is needed to validate a genuine existing binding.

3. **Inventory freshness and denominator membership need explicit joins.** Current sealer correctly requires native inventory PASS/20/no open roles and exact v2 SHA. It should additionally join each inventory row's completion path/SHA/session to the currently sealed completion and assert image-gate keys equal the case's declared role IDs, rather than only checking case/total cardinality. Current actual v2 schema uses `image_id == role_id`, so there is no present key mismatch; this is a missing validation guard.

4. **Portable archive verifier should reject symlink escape.** Mapping relative paths reject `..` and absolute paths, but `actual.is_file()` follows symlinks. Add a resolved-path-within-archive check and symlink rejection if claiming no external host paths are required.

## Confirmed properties and limits

- Native-source closure requirement and hard-coded actual v2 preparer digest are already present in the inspected sealer; original v1 source remains separately frozen.
- Frozen summarizer gates use image_id, while actual v2 packets assign each image_id the exact requested role_id; role membership can therefore be checked directly without renaming scores or reports.
- Complete initial three-critic reuse supports N=1, with null diversity and the original single-image reason. Low/NA quality gates are retained when procedure is valid; invalid initial procedure becomes unready instead of replacement.
- Actual unique review sessions/records/scores are counted once, while projected selected records can reuse initial summaries. Supplemental source-attestation NA overrides the combined gate while keeping original v4 gates.
- Archive copies preserve the complete raw tree and authoritative external pins by exact bytes; current filename/path alias replay does not modify raw files, copy, scores or thresholds. Source checker uses unchanged raw source identifiers consistently and only reads archived packet/reports.
- Gallery uses relative paths, records missing selected files as missing, and makes no independent PASS claim. Its displayed native size and digest come from selection metadata; it should be built only after full production closure.
- The sealer currently requires exactly one session even for every actual critic completion. A real failure before thread.started would block closure; if encountered, report and preserve it as NA rather than inventing a session.

No whole-phase PASS or portability PASS is claimed by this source audit. Run actual archive/replay integration once all real reviews have closed.
