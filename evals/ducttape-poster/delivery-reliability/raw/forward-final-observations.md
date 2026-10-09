# Final independent forward results

All 44 independent structural scenarios passed on stable helper SHA-256 `f9f3b9efa6a9fba884d37653c032a4167551bb07380b7c7e1aa2f17369a6878c`. The exact helper bytes and the contract available at run time are preserved in `helper-under-test.py` and `delivery-contract-under-test.md`. Every invocation used the bundled Python with `-B`; raw input manifests, exact argv, SHA, exit codes, stdout, stderr, emitted response and report are preserved in each case directory.

- Five existing local selected originals: `READY`, five distinct image/original-link pairs with dimensions.
- Single selected edited original: `READY`, one pair; the prior original is absent and download SHA matches the selected edit.
- Four selected plus one NONE: `PARTIAL`, four pairs with the NONE reason preserved and no image promoted for that role.
- Dialog mode using scheme-bearing simulated strings and declared dimensions, no local source: `READY`, both references `supplied_unverified`, source unavailability preserved in the report.
- Missing dialog refs, explicit dialog null refs, explicit local null refs, missing dimensions, missing preview and mismatched declared dimensions: `NOT_READY` with reviewable response/report output.
- Readable truncated, CRC-corrupt or non-image local originals remain blocked even when dialog references are supplied. A thumbnail or prior original used as local original-download target is rejected by byte/SHA mismatch.
- Eight unsafe-reference scenarios and nine malformed-schema scenarios return input error exit 1 without emitting delivery cards.
- Existing directories, files, broken symlinks and a previously prepared output directory are refused; sentinel contents and prior output hashes remain unchanged.

Prepared cards each place the original download link and pixel dimensions immediately under their individual image. Blocked cards omit raw local paths and parser/OSError diagnostics; details remain available in `delivery.json`. All emitted reports explicitly say preparation does not confirm display/download in the user's conversation and that the checks do not perform full image decoding or visual review.

The scheme-less simulated-identifier case expects `NOT_READY` under the clarified Markdown-target contract. It does not fabricate a link from an opaque native media handle. The native media/attachment fallback still requires evaluation in the actual target environment. No actual GPT Work media/download reference was available, so these local structural tests do not demonstrate live GPT Work inline display or original download.

The initial 43/44 run remains unchanged at `../run-20261009T064223255410Z/`, including its earlier supported-reference assumption and raw blocked result. `run-provenance.md` explains the clarified expectation. Original fixture JSON and original/preview image SHA and byte counts remained unchanged in both runs. No repository code or docs were changed by this tester; all new tests, artifacts and notes are in this forward-independent tree.
