# Selected v2 recording integration

This is a future selected instrumentation change. Keep the original initial freeze and all three initial NA records authoritative. The overall cap stays six critics: three initial v1 and the already planned three selected v2. No additional actor, replacement critic, native call, cap reset, pixel edit, or initial post-completion export is authorized.

The root sealer/verifier should dispatch the frozen v1 auditor for initial and the separately frozen v2 auditor for selected using each packet's recorded helper pins. Preserve the original v4 summary, rubric, normalization, source-attestation audit, score floors, complete five-member/three-critic gates, and effective NA behavior. V2 bindings certify only recording relationships and recognized export execution. They do not promote initial raw scores into missing v4 export records or promote a synthetic NA fixture into visual success.

Files to freeze before selected preparation and actors:

- `method-selected-v2/compact_critic_adapter.py`
- `method-selected-v2/audit_compact_bindings.py`
- `method-selected-v2/prepare_reviews_compact.py`
- `method-selected-v2/README.md`
- `method-selected-v2/compact-recording-addendum.md`
- `method-selected-v2/test_selected_recording_v2.py`
- `method-selected-v2/ROOT-INTEGRATION.md`
- `method-selected-v2/verification.json` after its metadata verification record exists

Run the metadata-only verification:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/method-selected-v2/test_selected_recording_v2.py
```

After reviewing these sources and confirming whole initial closure, root can write a separate exclusive selected helper freeze with this command. It does not prepare jobs or launch actors. The original freeze is referenced and byte-checked, never rewritten:

```sh
python3 - <<'PY'
import datetime, hashlib, json
from pathlib import Path
root = Path('/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9')
def pin(path):
    path = Path(path).resolve(strict=True)
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
initial_path = root/'planning/critic-recording-helper-freeze.json'
initial = json.loads(initial_path.read_bytes())
assert all(pin(row['path']) == row for row in initial['files'])
names = ('compact_critic_adapter.py', 'audit_compact_bindings.py', 'prepare_reviews_compact.py',
         'README.md', 'compact-recording-addendum.md', 'test_selected_recording_v2.py',
         'ROOT-INTEGRATION.md', 'verification.json')
value = {'kind': 'selected_recording_v2_helpers_before_selected_critics',
         'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'files': [pin(root/'method-selected-v2'/name) for name in names],
         'original_initial_helper_freeze': pin(initial_path),
         'production_and_quality_freeze': initial['production_and_quality_freeze'],
         'recording_method_schema_version': 2, 'raw_observation_schema_version': 1,
         'pin_schema': 'path-sha256-bytes-v2',
         'scope': 'already planned three future selected critics only',
         'overall_critic_cap': 6, 'initial_v1_critics': 3, 'selected_v2_critics': 3,
         'initial_records_immutable': True, 'quality_gates_unchanged': True}
with (root/'planning/selected-recording-v2-helper-freeze.json').open('x', encoding='utf-8') as handle:
    json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
    handle.write('\n')
PY
```

The preparer API is unchanged except that only `--wave selected` is accepted:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/method-selected-v2/prepare_reviews_compact.py --corpus CORPUS --production PRODUCTION --out FRESH_PREPARATION_ROOT --wave selected --candidate-label I --initial-root ORIGINAL_PREPARATION_ROOT
```

Preparation writes readiness, packet, three prompts and three job JSON files exclusively; it never launches. The changed method context prevents reuse of the v1 initial record. The new packet declares `compact_recording.schema_version:2`, `pin_schema:path-sha256-bytes-v2`, all new helper paths, and the unchanged raw schema 1. The frozen runner can execute these jobs without any source change. Its path/hash-only receipts remain valid; supplied byte counts, when present, are checked. All raw packet pins and adapter provenance contain exact path/hash/bytes.

Critics must run the exact literal `functions.exec` command generated in their prompt before their own completion. The adapter API is unchanged:

```sh
PYTHON PINNED_ADAPTER --packet EXACT_PACKET --observations EXACT_PROFILE_OBSERVATIONS --output-dir EXACT_EXISTING_CRITIC_DIRECTORY
```

Audit the completed selected record with:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round9/method-selected-v2/audit_compact_bindings.py --packet SELECTED_PACKET --report-dir SELECTED_PHASE/cli --output NEW_SELECTED_BINDING_AUDIT
```

Python APIs remain `audit_profile(packet_path, profile, folder, access=...)`, `audit(packet_path, report_dir, access=...)`, `adapter_command(packet, packet_path, observations_path, output_dir)`, and `ByteAccess(reader=...)` or `ByteAccess(path_map=...)`. Archive CLI mode retains `--archive-map EXPLICIT_MAP_JSON` and has no host-path fallback. `ByteAccess.checked_pin(value, require_size=False)` accepts the frozen runner's hash-only receipts and validates any supplied size. Passing `require_size=True` also requires the byte count. Neither archive lookup nor export invents a viewed receipt.
