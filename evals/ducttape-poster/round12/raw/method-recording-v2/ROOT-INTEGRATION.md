# Prospective R10 recording v2 integration

Freeze this same recording helper chain together with runtime J before any R10 production. Both initial and selected packets declare method schema 2, `pin_schema:path-sha256-bytes-v2`, and actual raw observation schema 1. Initial and selected use identical method/helper locations; no phase-only change is introduced. No R9 raw record, prior score, missing export, archive, or actor is altered.

The root must provide and pin its base `evidence_io.py`, frozen v4 `summarize.py`, `run_agent.py`, rules/rubric, and `planning/ratio-policy-before-generation.json`. Verification also compares unchanged producer/preparer core functions with root's `prepare_reviews_v2.py`. This method expects the existing literal full-five contract, exact native/usage720/thumbnail320 packet metadata, closed maker barrier, three fixed fresh profiles, original finite review rules, and strict full-context reuse. It never calls a maker, image model, runner, or review actor.

Root sealer/verifier integration must use the frozen method-recording-v2 auditor for both phases based on recorded helper pins. Keep the frozen v4 summary and original source-attestation audit separate. A recording binding PASS proves byte relationships and recognized adapter invocation only; semantic viewing, source fidelity, quality thresholds and effective NA remain controlled by their original gates. No changes to those gates or summary thresholds are made here.

Method files to include in the pre-production freeze:

- `method-recording-v2/compact_critic_adapter.py`
- `method-recording-v2/audit_compact_bindings.py`
- `method-recording-v2/prepare_reviews_compact.py`
- `method-recording-v2/README.md`
- `method-recording-v2/compact-recording-addendum.md`
- `method-recording-v2/test_recording_v2.py`
- `method-recording-v2/ROOT-INTEGRATION.md`
- `method-recording-v2/verification.json`

Run metadata-only verification:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round10/method-recording-v2/test_recording_v2.py
```

Root can write a separate exclusive method freeze before production with this command, then bind it into the broader runtime J/production/quality freeze. The command does not prepare jobs or launch actors:

```sh
python3 - <<'PY'
import datetime, hashlib, json
from pathlib import Path
root = Path('/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round10')
def pin(path):
    path = Path(path).resolve(strict=True)
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
names = ('compact_critic_adapter.py', 'audit_compact_bindings.py', 'prepare_reviews_compact.py',
         'README.md', 'compact-recording-addendum.md', 'test_recording_v2.py',
         'ROOT-INTEGRATION.md', 'verification.json')
value = {'kind': 'r10_recording_v2_helpers_before_production',
         'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'files': [pin(root/'method-recording-v2'/name) for name in names],
         'base_helpers': [pin(root/name) for name in ('evidence_io.py', 'summarize.py', 'run_agent.py',
                                                   'prepare_reviews_v2.py', 'review_rules.md', 'critic_rubric.md',
                                                   'planning/ratio-policy-before-generation.json')],
         'recording_method_schema_version': 2, 'raw_observation_schema_version': 1,
         'pin_schema': 'path-sha256-bytes-v2', 'phases': ['initial', 'selected'],
         'scope': 'prospective R10 only, same helper chain in both phases',
         'quality_gates_unchanged': True, 'prior_records_immutable': True}
with (root/'planning/recording-v2-helper-freeze.json').open('x', encoding='utf-8') as handle:
    json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
    handle.write('\n')
PY
```

Prepare initial jobs using the new method directly:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round10/method-recording-v2/prepare_reviews_compact.py --corpus CORPUS --production PRODUCTION --out PREPARATION_ROOT --wave initial --candidate-label J
```

Prepare selected with the same source and an explicit initial preparation root when needed:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round10/method-recording-v2/prepare_reviews_compact.py --corpus CORPUS --production PRODUCTION --out FRESH_PREPARATION_ROOT --wave selected --candidate-label J --initial-root INITIAL_PREPARATION_ROOT
```

Preparation writes readiness, packet, prompts and job JSON exclusively; it never launches. The unchanged runner consumes the exact three-report job contract: `PROFILE.observations.json`, `PROFILE.json`, and `PROFILE.md`. Its immutable path/hash-only launch/completion receipts are supported. Any supplied byte count is checked; adapter packet/raw/provenance pins always include the exact byte count.

A critic exclusively writes its own raw schema 1 observations, then invokes the exact literal pinned adapter command generated in its prompt, through `functions.exec` / `tools.exec_command` before its own CLI completion. The adapter API is unchanged:

```sh
PYTHON PINNED_ADAPTER --packet EXACT_PACKET --observations EXACT_PROFILE_OBSERVATIONS --output-dir EXACT_EXISTING_CRITIC_DIRECTORY
```

Audit either completed fresh phase with:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/nahyeonbin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round10/method-recording-v2/audit_compact_bindings.py --packet PHASE_PACKET --report-dir PHASE/cli --output NEW_BINDING_AUDIT
```

For a valid complete whole-context reuse record, use `--packet SELECTED_PACKET --reuse REUSE_JSON --output NEW_AUDIT`. Reuse requires the entire original valid three-critic record and exact identical full context; unfavorable records are retained. Identical context awaiting a complete valid original record remains unready. A changed context can receive only the already permitted fresh selected three. No partial reuse, initial replacement, post-completion export or additional review is authorized.

Python APIs remain `audit_profile(packet_path, profile, folder, access=...)`, `audit(packet_path, report_dir, access=...)`, `audit_reuse(selected_packet_path, reuse_path, access=...)`, `adapter_command(packet, packet_path, observations_path, output_dir)`, and `ByteAccess(reader=...)` or `ByteAccess(path_map=...)`. Archive CLI mode uses `--archive-map EXPLICIT_MAP_JSON` and has no host-path fallback. `ByteAccess.checked_pin(value, require_size=False)` supports hash-only runner receipts and validates any supplied size; `require_size=True` additionally requires it. Unknown raw viewed paths stay strings and never become archive aliases or successful view receipts.

Verification creates only temporary synthetic text metadata. Maker inventory and PNG validation are explicitly mocked; the real preparer, raw pin schema, shell adapter and audit execute. Synthetic trace events model pre-completion invocation and use clearly synthetic IDs. Both phases retain unavailable views, NA judgments, and null scores/diversity. Explicit archive-reader replay and wrong-binding/absent/late invocation tests validate recording mechanics without images, visual quality claims, actors, or real case jobs.
