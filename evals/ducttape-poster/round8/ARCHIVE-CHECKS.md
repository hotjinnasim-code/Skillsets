# Closed candidate I archive integration

Commands run:

```sh
cd /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round8
python3 -B archive_single_five.py --destination /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round8-archive
python3 -B verify_archive.py --archive /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round8-archive --output /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round8-archive/portable-replay.json
cd /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round8-archive
python3 -B integration-checks.py
```

Results: 345 mapped source byte checks, 310 distinct hashes, 331 physical indexed files, and two frozen v4 summaries replayed. Initial remains PASS2/FAIL3/NA0, set FAIL; selected remains PASS5/FAIL0/NA0, set PASS. Source attestation gates remain PASS. All 14 returned native originals and 56 stage PNG files are retained unchanged, with six raw critic JSON records and every other original source-tree file. Fourteen external native-cache identifiers map to already retained raw originals.

The archived gallery contains five images and 21 link references to 16 unique existing contained files, including report.md. All links passed. Full replay using the copied verifier and frozen modules passed while original candidate/native-cache metadata and content access were blocked; attempted original-host accesses: zero.

`synthetic-metadata-fixtures/` is outside real raw evidence and explicitly marked synthetic. Wrong observed source path, wrong observed source hash, and unknown raw viewed host path fixtures all retained NA with exact copied fixture bytes. The unknown viewed path fixture changes only report metadata and its synthetic completion pin; original image bytes and seven-score records remain unchanged. Its sole procedure error is the expected viewed-sequence mismatch. Copied provenance does not represent any new critic session.

Machine-readable results: `portable-replay.json`, `portable-replay-host-blocked.json`, and `archive-integration-checks.json`. Fixture sources and exact-byte retained copies are documented by their SHA-256 inventories in the last result. These auxiliary checks and synthetic fixtures are outside the indexed real raw tree.

Semantic viewing remains an attestation. This development request does not certify unseen requests. No client-asset preservation or one-image editing was exercised. No image changes, new posters or new critic sessions were made for these archive checks.
