# Single-five bounded requested-count evaluation contract

This protocol is for an explicitly requested skill experiment. It is not the default cost or workflow for ordinary poster work, and a PASS describes only the observed packet and version. Do not infer quality on unseen requests. Preserve every planned role, returned or failed native attempt, low score, raw review and procedural defect. Do not replace critics, drop requests, rename a role to reset its repair limit, or resample until PASS. Each candidate/version/case/role permits one initial native attempt plus at most two repairs, including failed attempts.

## Frozen input and complete viewing

Freeze a packet containing the exact user-requested N images before launching three fresh, independent critics. Do not silently expand an explicit one- or three-image request to five. Each critic evaluates the same ordered N members, each at native, usage720 and thumbnail320: all 3N exact views must be inspected before the first image score or diversity score. The current D1 case requests five and therefore still requires all fifteen views. Use the whole user request and each assigned style literally; do not infer the author's intent or translate an expressive genre into a safer genre. A first/final packet with any changed native hash requires a fresh complete three-critic evaluation. Reuse is allowed only when every member's native hash and the entire evaluation context are identical, with an explicit retained reference. A changed single image does not authorize partial reuse of the other members' scores.

The runner records launch/completion/JSONL trace evidence. Execution provenance can establish a fresh session, successful completion and immutable input/report bytes; it does not independently prove semantic image viewing. Each critic must also make a truthful viewing/order attestation. Do not claim a recognized image-view tool event unless the trace actually contains it. Unreadable or genuinely ambiguous views are NOT_ASSESSABLE (NA), not a guessed score or a fabricated glyph omission.

## Predeclared transcription

For every required copy entry, preserve the first raw observed text verbatim, the required literal text, the normalized comparison, layout observations and ambiguity separately. The normalization is `nfc-ws-optical-v1`:

- Apply Unicode NFC. Collapse each whitespace run to one ordinary space and trim outer whitespace. Preserve each explicit `\n` when `fixed_newlines:true`; collapse whitespace within each line, without merging lines. Otherwise a layout line break is whitespace, not a missing character.
- Preserve word spaces after that collapse. Do not erase all whitespace, invent a missing Hangul glyph from spacing alone, or merge differently spaced words to make equality pass.
- On `kind:"text"` entries only, remove optical spaces directly around the exact middle-dot `·` and slash `/`. Other punctuation characters remain distinct. URL entries must be separately declared `kind:"url"`; their slash, dot and word spacing receives no optical exception. A text entry containing a URL is an invalid packet, so a broken URL is never silently repaired by slash normalization.
- Record fixed-newline/layout fidelity separately from glyph/word/punctuation fidelity. Soft line wrapping and optical gaps are not evidence of a missing glyph. A genuine punctuation-class or glyph-class uncertainty is an ambiguity, not a definite transcription. Do not map a bullet, period, middle-dot, colon or lookalike to another punctuation class.

An ambiguity may trigger one revisit of the exact same pinned asset, never a regeneration. Preserve the initial read and the revisit `{view,path,sha256,raw_observed,resolution,resolved,reason}`. `resolution` explains the observed glyph class; `resolved` is a boolean. Use `revisit.raw_observed` for the final comparison only when `resolved:true`, while retaining the initial read unchanged. If `mandatory.text.ambiguities` is nonempty, each entry is `{copy_index,description,resolved}` and any claim of resolution must join the matching resolved transcription revisit. An unresolved ambiguity makes that image NA. No second revisit, repeated resampling, or retrospective change of the normalization rule is permitted.

## Packet schema

All paths are explicit existing file paths; hashes are lowercase SHA-256 of exact bytes. Relative paths resolve against the JSON file containing them. An input pin is `{path,sha256}`; an image-view pin also includes integer `width,height` matching its native-evidence manifest. Exactly N distinct image IDs and roles are mandatory. `expected_count` is the actual user's count, not a target invented by this protocol. An image may add `style_requirement` for its literal assigned direction; otherwise the common packet style is checked.

```json
{
  "schema_version": 1,
  "case_id": "R7-C1", "wave": "initial",
  "expected_count": 5,
  "critic_profiles": ["A", "B", "C"],
  "full_request": "literal complete user request",
  "review_rules": {"path": "/absolute/review_rules.md", "sha256": "..."},
  "normalization": "nfc-ws-optical-v1",
  "copy": [{"text": "literal copy", "kind": "text", "fixed_newlines": false}],
  "requirements": {
    "style": "literal assigned style requirement, including clay3D and Hangul treatment where requested",
    "ratio": [3, 2], "no_type_only": true
  },
  "images": [{
    "image_id": "R7-C1-M1", "role": "R7-C1-M1", "stage": "initial",
    "source_manifest": {"path": "/absolute/stages/initial/manifest.json", "sha256": "..."},
    "views": {
      "native": {"path": "/absolute/original.png", "sha256": "...", "width": 1536, "height": 1024},
      "usage720": {"path": "/absolute/usage-720.png", "sha256": "...", "width": 720, "height": 480},
      "thumbnail320": {"path": "/absolute/thumbnail-320.png", "sha256": "...", "width": 320, "height": 213}
    }
  }]
}
```

The example shows one member for brevity; a packet declaring `expected_count:5` must contain exactly five. Packets for explicit one- or three-image requests declare 1 or 3. Seven dimensions are exactly `content_form`, `hierarchy`, `typography`, `space`, `image_material`, `emotion_control`, `ai_slop`.

## Raw critic JSON schema

One untouched JSON and Markdown report per critic. Do not let a combiner rewrite a raw review. `session_id` may be `null` when it is not observable inside the critic; the summarizer derives it from the actual runner trace. A non-null claimed ID must match. Evidence entries are `{view,location,observation}` with a named pinned view, a concrete location and an observed fact. Scores are integers 1–5, never booleans or numeric strings. Every dimension requires located evidence. A high average cannot cancel any low dimension or mandatory failure.

```json
{
  "schema_version": 1, "case_id": "R7-C1", "wave": "initial", "profile": "A", "session_id": null,
  "procedure": {"fresh_session": true, "all_views_before_scoring": true, "viewed_count": 15, "order_compliant": true, "method": "truthful description of exact viewing"},
  "viewed": [{"image_id": "R7-C1-M1", "view": "native", "path": "/absolute/original.png", "sha256": "..."}],
  "images": {"R7-C1-M1": {
    "image_id": "R7-C1-M1", "role": "R7-C1-M1", "stage": "initial", "case_id": "R7-C1", "profile": "A",
    "mandatory": {
      "text": {"status": "PASS", "issues": [], "ambiguities": [], "transcriptions": [{
        "required": "literal copy", "raw_observed": "literal copy",
        "normalized_required": "literal copy", "normalized_observed": "literal copy", "equal": true,
        "layout": {"status": "PASS", "observations": "soft wrapping or fixed newlines observed separately"},
        "ambiguity": null, "revisit": null
      }]},
      "style": {"status": "PASS", "checked_requirement": "same literal packet style requirement", "evidence": [{"view": "native", "location": "...", "observation": "..."}], "issues": []},
      "ratio": {"status": "PASS", "observed_dimensions": [1536, 1024], "issues": []},
      "no_type_only": {"status": "PASS", "evidence": [{"view": "native", "location": "...", "observation": "substantive nonglyph scene/action/form that contributes to the requested message"}], "issues": []},
      "substantive_visual": {"status": "PASS", "evidence": [{"view": "native", "location": "...", "observation": "..."}]}
    },
    "scores": {"content_form": 4, "hierarchy": 4, "typography": 4, "space": 4, "image_material": 4, "emotion_control": 4, "ai_slop": 4},
    "evidence": {"content_form": [{"view": "native", "location": "...", "observation": "..."}], "hierarchy": [], "typography": [], "space": [], "image_material": [], "emotion_control": [], "ai_slop": []},
    "residuals": []
  }},
  "set": {"members": ["R7-C1-M1", "R7-C1-M2", "R7-C1-M3", "R7-C1-M4", "R7-C1-M5"], "requested_count": 5,
    "count_fidelity": {"status": "PASS", "observed_count": 5, "required_count": 5, "issues": []}, "diversity": 4,
    "evidence": [{"image_id": "R7-C1-M1", "view": "thumbnail320", "location": "whole composition", "observation": "specific relationship to the other four"}], "residuals": []}
}
```

Populate all 3N `viewed` entries, all N `images`, all seven nonempty evidence arrays per image, and (when N>=2) diversity evidence naming every member. For N=1, set `diversity:null` and `not_applicable_reason:"single requested image"`; do not fabricate a diversity score or turn this omission into a failed gate. Explicit count fidelity is mandatory for all N. Examples are structural, not default scores. Mandatory status is exactly `PASS`, `FAIL` or `NA`. A type or whitespace composition plus a tiny ornament does not meet `no_type_only`: the required nonglyph visual must be substantive. Material polish alone cannot replace the requested scene, action or genre. If the required ratio or copy is demonstrably wrong, report FAIL. If the exact asset cannot be judged, report NA and its reason. Do not use NA to hide an observed low score.

## Runner provenance and summary gates

`summarize.py --packet PACKET --report A=RAW_A --report B=RAW_B --report C=RAW_C --completions-dir ROOT --output NEW_OUTPUT` reads `ROOT/PROFILE/launch.json` and `completion.json` for each profile. Launch contains `started_utc,argv,fresh_session:true,case_id,wave,profile,prompt:{path,sha256},input_pins:[{path,sha256}]`. Completion preserves those fields and adds `completed_utc,exit_code,session_ids,turn_completed_count,input_pins_unchanged,trace:{path,sha256},reports:{"A.json":{path,sha256},"A.md":{path,sha256}}`. The actual `thread.started` trace ID is the session identity. Require `exec --ephemeral`, no resume/fork, exactly one fresh thread, at least one completed turn, exit zero, immutable declared inputs and raw report pins, and three unique sessions. Packet, rules and all 3N views must be launch input pins.

Each image PASS requires all seven scores >=4 from each of the three critics, each critic's mandatory text/style/ratio/no-type-only/substantive-visual PASS, and valid unambiguous evidence. Set PASS additionally requires exact count fidelity, every requested image gate PASS, and (for N>=2) diversity >=4 from all three critics. The five-member diversity threshold is unchanged. Invalid procedure, inconsistent recorded equality, missing evidence or unresolved actual ambiguity yields NA with the raw low records retained. A valid observed low score or mandatory failure yields FAIL. There is no mean-score gate.

The exclusive output contains every requested image gate, each critic's seven raw scores, mandatory/transcription data, raw report data and byte pins, source/view/manifest pins, procedure errors, all three diversity values (or explicit single-image applicability exclusions), and exact expected/observed record and score counts. One N-image stage has 3N image/profile records and 21N declared score slots. D1's five-image stage has fifteen records and 105 slots; two actually evaluated D1 stages have thirty records and 210 slots. Do not claim those totals for missing/invalid/raw-unreadable records.

## Native evidence helper

Before every native call create `ROLE_DIR/stages/STAGE/call-input.json` and `pre-call.json`; when they contain `role`/`stage`, identities must match. Save the complete actual tool input and recorded pre-call evidence before starting. Do not retrofit them after viewing the outcome. After a returned native call:

```sh
python3 evidence_io.py save-native --role R7-C1-M1 --stage initial --source /exact/returned/native.png --role-dir /absolute/role-dir
```

The helper preserves native bytes as `original.png` and `final.png`, makes only Pillow QA downsampling, and writes `manifest.json` with source/input/artifact hashes and PNG dimensions. `saved_at_utc` is helper preservation time, not a claimed tool interval. The caller retains actual native start/end/tool-result evidence; do not infer native concurrency from helper process intervals or filenames.

Every returned stage needs `inspection.json` with `{role,stage,actual_viewed:true,actual_view_paths:[exact original, exact usage720, exact thumbnail320],raw_observed_text:[],residuals:[]}`. Each returned repair also needs `parent-comparison.json` identifying the immediate parent stage/outcome, its `parent_manifest_sha256` and `parent_native_sha256` (or `parent_failure_sha256`), plus `changes:[]` and `residuals:[]`. Failed calls need `{role,stage,outcome:"failure",native_call_count:1,error:"actual recorded failure"}` in `failure.json`; keep their input, pre-call and failure metadata. They count toward the three-call cap and are not selectable.

`python3 evidence_io.py finalize --role-dir ROLE_DIR --selected-stage initial|repair-1|repair-2` verifies every stage and inspection, retains unselected and failed stages, and creates an exclusive `selection.json`. It refuses missing outcomes, overwrites, gaps and more than two repairs. No helper actually views, visually rescales scores, or generates images. Use later unseen requests as a frozen transfer test after development; do not feed their critic results back into that frozen candidate or claim this experiment proves all future requests high-end.
