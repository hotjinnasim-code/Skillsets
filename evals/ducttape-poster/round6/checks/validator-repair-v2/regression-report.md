# Standalone auditor v2

**PASS** for the patched standalone utility regressions. The original independent final technical **FAIL** is preserved and is not replaced by this result.

Only two FT03 gaps were patched: the canonical summary path is derived from the closure wave, including when the reference declares an unavailable stage; and full initial/final PASS, FAIL and NOT_ASSESSABLE distributions must exactly match the individual gates, with exact nonnegative integer counts and no extra keys.

The prior 13 and 11 fixtures plus eight v2 cases all meet their expectations (32 cases total). The new cases include empty/repointed missing-summary paths, changed distributions holding PASS fixed, Boolean counts, unknown keys and negative counts.

The actual archive audit remains **PASS** in evidence-only mode, with 120 records and 840 all-seven score values. The terminal gate remains **NOT_ASSESSABLE**. The recomputed distributions remain {'first': {'PASS': 1, 'FAIL': 14, 'NOT_ASSESSABLE': 5}, 'final': {'PASS': 1, 'FAIL': 14, 'NOT_ASSESSABLE': 5}}.

All 24 v1 files and its exact manifest are unchanged; all 965 existing archive files are unchanged. The v1 source, manifest and reports remain preserved in their original folder and copied under `v1-preserved`. `immutability-check.json`, `manifest.json` and `v1-to-v2.patch` record the boundaries and hashes. No original archive/checks, critics, observations, images, selections or skills changed, and no commit was made.

These are post-reader control-flow tests, not alternate byte-consistent archives. No image was displayed or decoded and no score was reassessed. Hashes and metadata do not certify semantic viewing/order or authorship. Generic failed-initial sealing remains unchanged and outside this bounded fix.
