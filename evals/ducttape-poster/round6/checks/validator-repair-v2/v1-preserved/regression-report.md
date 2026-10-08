# Standalone auditor regression result

The independent final technical review remains **FAIL** and is preserved in `original-sources/report.md` and `original-sources/report.json`. The patched standalone utility regression result is **PASS**; these are different findings.

The original 13 fixture cases and 11 additional cases all meet their expected result. The added cases cover copied case/profile identities, first/final score and record counts, image/case gate relabeling, acceptance/unavailability bypasses, recorded summary profiles, and missing `turn.completed`.

The actual archive audit passes in **evidence-only** mode. It preserves 120 first/final observation records and 840 all-seven score values. Recomputed image pass counts remain {'first': 1, 'final': 1}; raw accepted final mandatory/core/diversity failures remain 47. The source review integrity remains **FAIL**, and the terminal gate remains **NOT_ASSESSABLE**.

All 938 existing archive files were rehashed before and after and are identical. The original auditor, fixture, fixture report, helper and independent review reports match their preserved source snapshots. Only files in this fixes folder were created or changed. No commit or archive edit was performed.

The patch is limited to FT-01–03 provenance, identity, count, gate and completed-session assertions. It retains prior-history validation and launch freshness checks. Generic failed-initial sealing remains unmodified and unexercised; this closed dataset contains 47 native calls and 24 review assignments with all initials returned. Explicit genuinely unavailable NA stages retain accurate zero counts rather than manufactured records.

No pixels were displayed or decoded, and no visual assessment was performed. The original auditor's byte hashes and PNG header dimension checks remain in use. These fixtures exercise post-reader control flow, not a byte-consistent alternate archive. Hash/session provenance does not prove semantic viewing, chronology or historical authenticity.
