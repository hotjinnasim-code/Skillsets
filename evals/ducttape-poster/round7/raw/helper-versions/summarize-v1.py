#!/usr/bin/env python3
"""Summarize three raw critics without replacing low records or inferring viewing.

No model calls, image decoding, score averaging, raw-report rewriting or overwrite.
Packet.expected_count is the literal user-requested count, not an expansion target.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

DIMENSIONS = ("content_form", "hierarchy", "typography", "space", "image_material", "emotion_control", "ai_slop")
VIEWS = ("native", "usage720", "thumbnail320")
STATUSES = ("PASS", "FAIL", "NA")
NORMALIZATION = "nfc-ws-optical-v1"
URL = re.compile(r"(?i)(?:https?://|www\.)\S+")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve(path, base):
    if not isinstance(path, str) or not path:
        raise ValueError("missing explicit path")
    result = Path(path)
    return (base / result if not result.is_absolute() else result).resolve(strict=True)


def read_json(path):
    raw = Path(path).read_bytes()
    return json.loads(raw), {"path": str(Path(path).resolve(strict=True)), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def pin(value, base, errors, label):
    try:
        if not isinstance(value, dict) or not re.fullmatch(r"[0-9a-f]{64}", str(value.get("sha256", ""))):
            raise ValueError("missing lowercase SHA-256 pin")
        path = resolve(value.get("path"), base)
        if not path.is_file():
            raise ValueError("not a file")
        actual = digest(path)
        if actual != value["sha256"]:
            raise ValueError("bytes disagree with pinned SHA-256")
        return {"path": str(path), "sha256": actual, "bytes": path.stat().st_size}
    except (ValueError, OSError) as exc:
        errors.append(f"{label}: {exc}")
        return None


def text(value):
    return isinstance(value, str) and bool(value.strip())


def integer(value, low=1, high=5):
    return type(value) is int and low <= value <= high


def normalize(raw, entry, *, fixed=None):
    """Only the predeclared NFC/whitespace/optical policy; never erase word spaces."""
    if not isinstance(raw, str):
        raise ValueError("transcription must be a string")
    value = unicodedata.normalize("NFC", raw.replace("\r\n", "\n").replace("\r", "\n"))
    keep_newlines = entry["fixed_newlines"] if fixed is None else fixed
    if keep_newlines:
        value = "\n".join(re.sub(r"[^\S\n]+", " ", line).strip() for line in value.split("\n"))
    else:
        value = re.sub(r"\s+", " ", value).strip()
    if entry["kind"] == "text":
        # URL-bearing required entries are rejected at packet validation. Protect
        # contiguous unexpected URL tokens as well; never rewrite their slashes.
        pieces, previous = [], 0
        for match in URL.finditer(value):
            pieces.append(re.sub(r" *([·/]) *", r"\1", value[previous:match.start()]))
            pieces.append(match.group())
            previous = match.end()
        pieces.append(re.sub(r" *([·/]) *", r"\1", value[previous:]))
        value = "".join(pieces)
    return value


def located(value, errors, label, image_ids=None):
    if not isinstance(value, list) or not value:
        errors.append(f"{label}: nonempty located evidence required")
        return
    for index, item in enumerate(value):
        if not isinstance(item, dict) or item.get("view") not in VIEWS or not text(item.get("location")) or not text(item.get("observation")):
            errors.append(f"{label}[{index}]: view, location and observation required")
        if image_ids is not None and (not isinstance(item, dict) or item.get("image_id") not in image_ids):
            errors.append(f"{label}[{index}]: packet member identity required")


def dimensions(path):
    with open(path, "rb") as handle:
        head = handle.read(24)
    if len(head) != 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError("not a PNG IHDR header")
    return struct.unpack(">II", head[16:24])


def validate_packet(packet, packet_path):
    errors, bindings = [], []
    base = packet_path.parent
    if not isinstance(packet, dict):
        raise ValueError("packet must be a JSON object")
    n = packet.get("expected_count")
    if type(n) is not int or n < 1:
        errors.append("expected_count must be the positive integer actual user-requested count")
        n = 0
    if type(packet.get("schema_version")) is not int or packet.get("schema_version") != 1 or not text(packet.get("case_id")) or not text(packet.get("wave")) or not text(packet.get("full_request")):
        errors.append("packet needs schema_version=1 and literal full_request/case_id/wave")
    if packet.get("normalization") != NORMALIZATION:
        errors.append("normalization was not predeclared as nfc-ws-optical-v1")
    profiles = packet.get("critic_profiles")
    if not isinstance(profiles, list) or len(profiles) != 3 or any(not text(p) or not re.fullmatch(r"[A-Za-z0-9_.-]+", p) for p in profiles) or len(set(profiles)) != 3:
        errors.append("exactly three distinct simple critic profiles required")
    rules_pin = pin(packet.get("review_rules"), base, errors, "review_rules")
    entries = packet.get("copy")
    if not isinstance(entries, list) or not entries:
        errors.append("copy must be a nonempty literal-entry array")
        entries = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not text(entry.get("text")) or entry.get("kind") not in ("text", "url") or type(entry.get("fixed_newlines")) is not bool:
            errors.append(f"copy[{index}]: text/kind/fixed_newlines required")
        elif entry["kind"] == "text" and URL.search(entry["text"]):
            errors.append(f"copy[{index}]: URL-bearing copy must use kind=url to protect slash fidelity")
    requirements = packet.get("requirements", {})
    ratio = requirements.get("ratio") if isinstance(requirements, dict) else None
    if not isinstance(requirements, dict) or not text(requirements.get("style")) or requirements.get("no_type_only") is not True or not isinstance(ratio, list) or len(ratio) != 2 or any(type(x) is not int or x <= 0 for x in ratio):
        errors.append("literal style, positive integer ratio pair and no_type_only=true required")
    images = packet.get("images")
    if not isinstance(images, list):
        images = []
    if len(images) != n:
        errors.append("packet image count differs from the actual requested count")
    ids, roles = [], []
    for index, image in enumerate(images):
        label = f"images[{index}]"
        if not isinstance(image, dict):
            errors.append(f"{label}: object required")
            continue
        image_id, role, stage = image.get("image_id"), image.get("role"), image.get("stage")
        if not text(image_id) or not text(role) or stage not in ("initial", "repair-1", "repair-2"):
            errors.append(f"{label}: image_id/role/stage required")
        ids.append(image_id)
        roles.append(role)
        if "style_requirement" in image and not text(image["style_requirement"]):
            errors.append(f"{label}: assigned style_requirement must be literal text")
        manifest_pin = pin(image.get("source_manifest"), base, errors, f"{label}/manifest")
        manifest = None
        if manifest_pin:
            try:
                manifest, _ = read_json(manifest_pin["path"])
                if manifest.get("kind") != "native_evidence" or manifest.get("role") != role or manifest.get("stage") != stage or manifest.get("outcome") != "returned" or type(manifest.get("native_call_count")) is not int or manifest.get("native_call_count") != 1 or manifest.get("native_byte_preserved") is not True:
                    errors.append(f"{label}: manifest identity/outcome mismatch")
                if not isinstance(manifest.get("files"), dict) or not isinstance(manifest.get("input_pins"), dict):
                    errors.append(f"{label}: manifest files/input_pins objects required")
                    manifest = None
            except (ValueError, OSError, AttributeError) as exc:
                errors.append(f"{label}: invalid native manifest: {exc}")
                manifest = None
        views, source = {}, None
        source_base = Path(manifest_pin["path"]).parent if manifest_pin else base
        if manifest:
            source = pin(manifest.get("source"), source_base, errors, f"{label}/returned-source")
            for key in ("call_input", "pre_call"):
                pin(manifest.get("input_pins", {}).get(key), source_base, errors, f"{label}/manifest/{key}")
            original = pin(manifest.get("files", {}).get("original"), source_base, errors, f"{label}/original")
            final = pin(manifest.get("files", {}).get("final"), source_base, errors, f"{label}/final")
            if source and original and final and not (source["sha256"] == original["sha256"] == final["sha256"]):
                errors.append(f"{label}: source/original/final native SHA mismatch")
        if not isinstance(image.get("views"), dict) or set(image["views"]) != set(VIEWS):
            errors.append(f"{label}: exactly native/usage720/thumbnail320 views required")
        for view in VIEWS:
            declared = image.get("views", {}).get(view) if isinstance(image.get("views"), dict) else None
            view_pin = pin(declared, base, errors, f"{label}/{view}")
            if view_pin:
                try:
                    size = dimensions(view_pin["path"])
                    if any(type(declared.get(k)) is not int for k in ("width", "height")) or list(size) != [declared.get("width"), declared.get("height")]:
                        errors.append(f"{label}/{view}: PNG dimensions do not match declared view")
                    view_pin.update(width=size[0], height=size[1])
                    key = "original" if view == "native" else view
                    artifact = manifest.get("files", {}).get(key) if manifest else None
                    if not isinstance(artifact, dict) or str(resolve(artifact.get("path"), source_base)) != view_pin["path"] or artifact.get("sha256") != view_pin["sha256"] or artifact.get("width") != size[0] or artifact.get("height") != size[1]:
                        errors.append(f"{label}/{view}: view does not join exact manifest artifact")
                except (ValueError, OSError, TypeError) as exc:
                    errors.append(f"{label}/{view}: {exc}")
                views[view] = view_pin
        bindings.append({"image_id": image_id, "role": role, "stage": stage, "source_manifest": manifest_pin, "source": source, "views": views})
    if len(set(str(x) for x in ids)) != len(ids) or len(set(str(x) for x in roles)) != len(roles):
        errors.append("packet images/roles must be distinct; no request may be dropped or duplicated")
    return errors, bindings, rules_pin


def validate_provenance(profile, report, report_pin, packet, packet_path, bindings, rules_pin, completions_dir):
    errors, provenance = [], {}
    folder = completions_dir / profile
    try:
        launch, launch_pin = read_json(folder / "launch.json")
        completion, completion_pin = read_json(folder / "completion.json")
        provenance.update(launch=launch, launch_pin=launch_pin, completion=completion, completion_pin=completion_pin)
        if not isinstance(launch, dict) or not isinstance(completion, dict):
            raise ValueError("launch/completion objects required")
        required_launch = ("started_utc", "argv", "fresh_session", "case_id", "wave", "profile", "prompt", "input_pins")
        for key in required_launch:
            if key not in launch or completion.get(key) != launch[key]:
                errors.append(f"{profile}: completion does not preserve launch field {key}")
        for key, expected in (("case_id", packet.get("case_id")), ("wave", packet.get("wave")), ("profile", profile)):
            if launch.get(key) != expected:
                errors.append(f"{profile}: launch {key} mismatch")
        argv = launch.get("argv")
        if launch.get("fresh_session") is not True or not isinstance(argv, list) or len(argv) < 3 or any(not isinstance(x, str) for x in argv) or Path(argv[0]).name not in ("codex", "codex.exe") or argv[1] != "exec" or "--ephemeral" not in argv or any(re.search(r"(?:^|[-=])(resume|fork)(?:$|=)", x, re.I) for x in argv):
            errors.append(f"{profile}: actual fresh exec --ephemeral argv required; resume/fork forbidden")
        if type(completion.get("exit_code")) is not int or completion["exit_code"] != 0 or completion.get("input_pins_unchanged") is not True:
            errors.append(f"{profile}: exit zero and unchanged input pins required")
        for key in ("started_utc", "completed_utc"):
            if not text(completion.get(key)):
                errors.append(f"{profile}: recorded {key} required")
        try:
            started = datetime.fromisoformat(completion["started_utc"].replace("Z", "+00:00"))
            ended = datetime.fromisoformat(completion["completed_utc"].replace("Z", "+00:00"))
            if started.tzinfo is None or ended.tzinfo is None or ended < started:
                raise ValueError("ordered timezone-aware timestamps required")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"{profile}: launch/completion timestamps invalid: {exc}")
        pin(launch.get("prompt"), folder, errors, f"{profile}/prompt")
        inputs = launch.get("input_pins")
        resolved_inputs = []
        if not isinstance(inputs, list) or not inputs:
            errors.append(f"{profile}: input_pins array required")
        else:
            for index, item in enumerate(inputs):
                actual = pin(item, folder, errors, f"{profile}/input_pins[{index}]")
                if actual:
                    resolved_inputs.append((actual["path"], actual["sha256"]))
        needed = [(str(packet_path), digest(packet_path))]
        if rules_pin:
            needed.append((rules_pin["path"], rules_pin["sha256"]))
        for binding in bindings:
            needed.extend((v["path"], v["sha256"]) for v in binding["views"].values())
        if not set(needed).issubset(set(resolved_inputs)):
            errors.append(f"{profile}: packet, rules and every exact view must be declared launch input pins")
        reports = completion.get("reports", {})
        json_pin = pin(reports.get(f"{profile}.json") if isinstance(reports, dict) else None, folder, errors, f"{profile}/raw JSON")
        pin(reports.get(f"{profile}.md") if isinstance(reports, dict) else None, folder, errors, f"{profile}/raw Markdown")
        if not json_pin or not report_pin or (json_pin["path"], json_pin["sha256"]) != (report_pin["path"], report_pin["sha256"]):
            errors.append(f"{profile}: CLI completion raw JSON pin does not match supplied raw report")
        trace_pin = pin(completion.get("trace"), folder, errors, f"{profile}/trace")
        session = None
        if trace_pin:
            events = []
            for line in Path(trace_pin["path"]).read_text(encoding="utf-8").splitlines():
                if line.strip():
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        raise ValueError("trace event must be a JSON object")
                    events.append(event)
            starts = [e for e in events if e.get("type") == "thread.started"]
            completed = sum(e.get("type") == "turn.completed" for e in events)
            if len(starts) != 1 or not text(starts[0].get("thread_id")):
                errors.append(f"{profile}: exactly one actual thread.started ID required")
            else:
                session = starts[0]["thread_id"]
            if type(completion.get("turn_completed_count")) is not int or completion["turn_completed_count"] != completed or completed < 1:
                errors.append(f"{profile}: completion count must match actual completed turns and be >=1")
            if any(e.get("type") in ("turn.failed", "error") for e in events):
                errors.append(f"{profile}: trace contains a failed turn/error")
            if completion.get("session_ids") != ([session] if session else []):
                errors.append(f"{profile}: completion session IDs do not match actual trace")
            if report.get("session_id") is not None and report.get("session_id") != session:
                errors.append(f"{profile}: raw report claimed session does not match actual trace")
        provenance.update(trace_pin=trace_pin, derived_session_id=session,
                          viewing_limit="freshness/completion are trace-backed; semantic viewing/order remain critic attestations")
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f"{profile}: provenance unavailable/invalid: {exc}")
    return errors, provenance


def transcription_checks(data, entries, views, errors, label):
    comparisons, outcomes = [], []
    transcriptions = data.get("transcriptions")
    if not isinstance(transcriptions, list) or len(transcriptions) != len(entries):
        errors.append(f"{label}: exact required-copy transcription count required")
        return [], "NA"
    for index, (entry, item) in enumerate(zip(entries, transcriptions)):
        here = f"{label}/copy[{index}]"
        if not isinstance(item, dict) or not isinstance(entry, dict) or item.get("required") != entry.get("text") or not isinstance(item.get("raw_observed"), str):
            errors.append(f"{here}: literal required and raw observed strings must be retained")
            outcomes.append("NA")
            continue
        raw = item["raw_observed"]
        ambiguity = item.get("ambiguity")
        unresolved = bool(ambiguity)
        revisit = item.get("revisit")
        if revisit is not None:
            if not ambiguity or not isinstance(revisit, dict) or revisit.get("view") not in VIEWS or type(revisit.get("resolved")) is not bool or not isinstance(revisit.get("raw_observed"), str) or not text(revisit.get("reason")) or not text(revisit.get("resolution")):
                errors.append(f"{here}: one ambiguity-triggered, explained exact-asset revisit required")
            else:
                view = views.get(revisit["view"], {})
                if revisit.get("path") != view.get("path") or revisit.get("sha256") != view.get("sha256"):
                    errors.append(f"{here}: revisit does not name the exact pinned view")
                if revisit["resolved"]:
                    raw, unresolved = revisit["raw_observed"], False
        try:
            normalized_required = normalize(entry["text"], entry)
            normalized_observed = normalize(raw, entry)
            equal = normalized_required == normalized_observed
            glyph_equal = normalize(entry["text"], entry, fixed=False) == normalize(raw, entry, fixed=False)
            computed = {"copy_index": index, "initial_raw_observed": item["raw_observed"], "comparison_raw_observed": raw, "normalized_required": normalized_required, "normalized_observed": normalized_observed, "equal": equal, "glyph_word_punctuation_equal_ignoring_layout_newlines": glyph_equal, "fixed_newlines": entry["fixed_newlines"], "unresolved_ambiguity": unresolved, "revisit": revisit}
            comparisons.append(computed)
            if item.get("normalized_required") != normalized_required or item.get("normalized_observed") != normalized_observed or type(item.get("equal")) is not bool or item["equal"] != equal:
                errors.append(f"{here}: recorded normalization/equal disagrees with predeclared computation")
            layout = item.get("layout")
            if not isinstance(layout, dict) or layout.get("status") not in STATUSES or not text(layout.get("observations")):
                errors.append(f"{here}: layout status/observations must be separate")
                outcomes.append("NA")
            elif unresolved or layout["status"] == "NA":
                outcomes.append("NA")
            elif not equal or layout["status"] == "FAIL":
                outcomes.append("FAIL")
            else:
                outcomes.append("PASS")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"{here}: normalization invalid: {exc}")
            outcomes.append("NA")
    extra_ambiguities = data.get("ambiguities")
    if not isinstance(extra_ambiguities, list):
        errors.append(f"{label}: ambiguities array required")
    else:
        for ambiguity in extra_ambiguities:
            index = ambiguity.get("copy_index") if isinstance(ambiguity, dict) else None
            linked = next((c for c in comparisons if c["copy_index"] == index), None)
            if not isinstance(ambiguity, dict) or type(index) is not int or not text(ambiguity.get("description")) or ambiguity.get("resolved") is not True or not linked or not isinstance(linked.get("revisit"), dict) or linked["revisit"].get("resolved") is not True or linked["unresolved_ambiguity"]:
                outcomes.append("NA")
    issues = data.get("issues")
    if not isinstance(issues, list):
        errors.append(f"{label}: issues array required")
    elif issues:
        outcomes.append("FAIL")
    result = "NA" if "NA" in outcomes else "FAIL" if "FAIL" in outcomes else "PASS"
    if data.get("status") != result:
        errors.append(f"{label}: mandatory text status contradicts comparisons/layout/ambiguity/issues")
    return comparisons, result


def image_record(record, image, profile, packet, binding):
    errors, comparisons = [], []
    label = f"{profile}/{image.get('image_id')}"
    if not isinstance(record, dict):
        return {"errors": [f"{label}: missing raw image record"], "gate": "NA", "raw": record, "computed_transcriptions": []}
    for key, expected in (("image_id", image.get("image_id")), ("role", image.get("role")), ("stage", image.get("stage")), ("case_id", packet.get("case_id")), ("profile", profile)):
        if record.get(key) != expected:
            errors.append(f"{label}: copied {key} mismatch")
    scores, evidence = record.get("scores"), record.get("evidence")
    if not isinstance(scores, dict) or set(scores) != set(DIMENSIONS):
        errors.append(f"{label}: exactly seven named score values required")
    if not isinstance(evidence, dict) or set(evidence) != set(DIMENSIONS):
        errors.append(f"{label}: exactly seven located evidence arrays required")
    for dimension in DIMENSIONS:
        if not isinstance(scores, dict) or not integer(scores.get(dimension)):
            errors.append(f"{label}/{dimension}: integer 1-5 score required")
        located(evidence.get(dimension) if isinstance(evidence, dict) else None, errors, f"{label}/{dimension}")
    mandatory = record.get("mandatory")
    statuses = []
    if not isinstance(mandatory, dict) or set(mandatory) != {"text", "style", "ratio", "no_type_only", "substantive_visual"}:
        errors.append(f"{label}: complete mandatory condition records required")
        mandatory = mandatory if isinstance(mandatory, dict) else {}
    for condition in ("text", "style", "ratio", "no_type_only", "substantive_visual"):
        value = mandatory.get(condition)
        if not isinstance(value, dict) or value.get("status") not in STATUSES:
            errors.append(f"{label}/{condition}: PASS/FAIL/NA status required")
            statuses.append("NA")
            continue
        statuses.append(value["status"])
        if condition == "text":
            comparisons, _ = transcription_checks(value, packet.get("copy", []), binding.get("views", {}), errors, f"{label}/text")
        elif condition == "ratio":
            native = binding.get("views", {}).get("native", {})
            observed = [native.get("width"), native.get("height")]
            if not isinstance(value.get("observed_dimensions"), list) or any(type(x) is not int for x in value["observed_dimensions"]) or value.get("observed_dimensions") != observed:
                errors.append(f"{label}/ratio: observed dimensions disagree with exact native")
            ratio = packet.get("requirements", {}).get("ratio")
            if isinstance(ratio, list) and len(ratio) == 2 and all(type(x) is int for x in observed + ratio):
                correct = observed[0] * ratio[1] == observed[1] * ratio[0]
                if value["status"] != ("PASS" if correct else "FAIL"):
                    errors.append(f"{label}/ratio: status contradicts native/required ratio")
        else:
            located(value.get("evidence"), errors, f"{label}/{condition}")
            if condition == "style" and value.get("checked_requirement") != image.get("style_requirement", packet.get("requirements", {}).get("style")):
                errors.append(f"{label}/style: literal assigned style was not checked")
    if not isinstance(record.get("residuals"), list):
        errors.append(f"{label}: residuals array required")
    gate = "NA" if errors or "NA" in statuses else "FAIL" if "FAIL" in statuses or any(scores[d] < 4 for d in DIMENSIONS) else "PASS"
    return {"gate": gate, "errors": errors, "scores": scores, "mandatory": mandatory, "computed_transcriptions": comparisons, "raw": record}


def summary(args):
    packet_path = Path(args.packet).resolve(strict=True)
    packet, packet_pin = read_json(packet_path)
    packet_errors, bindings, rules_pin = validate_packet(packet, packet_path)
    profiles = packet.get("critic_profiles") if isinstance(packet.get("critic_profiles"), list) else []
    supplied = {}
    for specification in args.report:
        profile, separator, path = specification.partition("=")
        if not separator or profile in supplied:
            raise ValueError("--report is an exclusive PROFILE=PATH mapping")
        supplied[profile] = Path(path).resolve(strict=False)
    if len(profiles) != 3 or set(supplied) != set(profiles):
        raise ValueError("supply exactly the three packet critic profiles; no replacement or extra critic")
    completions_dir = Path(args.completions_dir).resolve(strict=True)
    images = packet.get("images", []) if isinstance(packet.get("images"), list) else []
    image_ids = [i.get("image_id") for i in images if isinstance(i, dict)]
    global_errors, reviews, sessions = list(packet_errors), {}, []
    n = packet.get("expected_count") if type(packet.get("expected_count")) is int and packet["expected_count"] > 0 else 0
    observed_records, score_slots, valid_scores = 0, 0, 0
    for profile in profiles:
        procedure_errors = []
        try:
            raw, raw_pin = read_json(supplied[profile])
            if not isinstance(raw, dict):
                raise ValueError("raw report must be an object")
        except (ValueError, OSError) as exc:
            # Keep a byte pin even when the raw JSON cannot be parsed.
            path = supplied[profile]
            raw = {}
            raw_pin = ({"path": str(path), "sha256": digest(path), "bytes": path.stat().st_size, "available": True}
                       if path.is_file() else {"path": str(path), "sha256": None, "bytes": None, "available": False})
            procedure_errors.append(f"{profile}: raw report is not usable JSON: {exc}")
        if type(raw.get("schema_version")) is not int:
            procedure_errors.append(f"{profile}: integer schema version required")
        for key, expected in (("schema_version", 1), ("case_id", packet.get("case_id")), ("wave", packet.get("wave")), ("profile", profile)):
            if raw.get(key) != expected:
                procedure_errors.append(f"{profile}: raw {key} identity mismatch")
        procedure = raw.get("procedure", {})
        if not isinstance(procedure, dict) or any(procedure.get(k) is not True for k in ("fresh_session", "all_views_before_scoring", "order_compliant")) or type(procedure.get("viewed_count")) is not int or procedure["viewed_count"] != 3 * n or not text(procedure.get("method")):
            procedure_errors.append(f"{profile}: truthful full {3*n}-view before-scoring/order attestations required")
        expected_views = [(b["image_id"], view, b["views"].get(view, {}).get("path"), b["views"].get(view, {}).get("sha256")) for b in bindings for view in VIEWS]
        viewed = raw.get("viewed")
        actual_views = []
        if isinstance(viewed, list):
            for item in viewed:
                if not isinstance(item, dict):
                    procedure_errors.append(f"{profile}: malformed viewed entry")
                    continue
                try:
                    path = str(resolve(item.get("path"), supplied[profile].parent))
                except (ValueError, OSError):
                    path = item.get("path")
                actual_views.append((item.get("image_id"), item.get("view"), path, item.get("sha256")))
        if actual_views != expected_views:
            procedure_errors.append(f"{profile}: viewed sequence must match all exact ordered packet member/views, without omissions or extras")
        provenance_errors, provenance = validate_provenance(profile, raw, raw_pin, packet, packet_path, bindings, rules_pin, completions_dir)
        procedure_errors.extend(provenance_errors)
        if provenance.get("derived_session_id"):
            sessions.append(provenance["derived_session_id"])
        raw_images = raw.get("images")
        if not isinstance(raw_images, dict) or set(raw_images) != set(image_ids):
            procedure_errors.append(f"{profile}: every actual requested role must have one raw image record, with no extras")
        records = {}
        if isinstance(raw_images, dict):
            observed_records += len(raw_images)
            for record in raw_images.values():
                if isinstance(record, dict) and isinstance(record.get("scores"), dict):
                    score_slots += len(record["scores"])
                    valid_scores += sum(integer(value) for value in record["scores"].values())
        for image, binding in zip(images, bindings):
            if isinstance(image, dict):
                records[image.get("image_id")] = image_record(raw_images.get(image.get("image_id")) if isinstance(raw_images, dict) else None, image, profile, packet, binding)
        set_errors = []
        set_data = raw.get("set")
        diversity_gate = "NA"
        if not isinstance(set_data, dict) or set_data.get("members") != image_ids or type(set_data.get("requested_count")) is not int or set_data.get("requested_count") != n:
            set_errors.append(f"{profile}: set must list every requested member in order and exact requested_count")
            set_data = set_data if isinstance(set_data, dict) else {}
        count_fidelity = set_data.get("count_fidelity")
        if not isinstance(count_fidelity, dict) or count_fidelity.get("status") != "PASS" or type(count_fidelity.get("observed_count")) is not int or type(count_fidelity.get("required_count")) is not int or count_fidelity.get("observed_count") != n or count_fidelity.get("required_count") != n or count_fidelity.get("issues") != []:
            set_errors.append(f"{profile}: mandatory explicit count fidelity must be PASS for the exact requested count")
        if n == 1:
            if "diversity" not in set_data or set_data.get("diversity") is not None or set_data.get("not_applicable_reason") != "single requested image":
                set_errors.append(f"{profile}: one requested image requires explicit null diversity and its reason")
            else:
                diversity_gate = "NOT_APPLICABLE"
        else:
            if not integer(set_data.get("diversity")):
                set_errors.append(f"{profile}: integer 1-5 diversity required")
            located(set_data.get("evidence"), set_errors, f"{profile}/set", image_ids)
            evidence_ids = {item.get("image_id") for item in set_data.get("evidence", []) if isinstance(item, dict)} if isinstance(set_data.get("evidence"), list) else set()
            if evidence_ids != set(image_ids):
                set_errors.append(f"{profile}: diversity evidence must cover every requested member")
            if not set_errors:
                diversity_gate = "PASS" if set_data["diversity"] >= 4 else "FAIL"
        if not isinstance(set_data.get("residuals"), list):
            set_errors.append(f"{profile}: set residuals array required")
        if set_errors:
            diversity_gate = "NA"
        reviews[profile] = {"raw_report": raw_pin, "raw_data": raw, "provenance": provenance, "procedure_errors": procedure_errors, "images": records, "set": {"gate": diversity_gate, "errors": set_errors, "raw": set_data}}
        global_errors.extend(procedure_errors)
    if len(sessions) != 3 or len(set(sessions)) != 3:
        global_errors.append("three unique actual fresh CLI sessions required")
    image_gates = {}
    for image_id in image_ids:
        gates = [reviews[p]["images"].get(image_id, {}).get("gate", "NA") for p in profiles]
        image_gates[image_id] = "NA" if global_errors or "NA" in gates else "FAIL" if "FAIL" in gates else "PASS"
    diversity_gates = [reviews[p]["set"]["gate"] for p in profiles]
    set_gate = "NA" if global_errors or "NA" in image_gates.values() or "NA" in diversity_gates else "FAIL" if "FAIL" in image_gates.values() or "FAIL" in diversity_gates else "PASS"
    return {
        "schema_version": 1, "kind": "bounded_critic_summary", "case_id": packet.get("case_id"), "wave": packet.get("wave"),
        "packet": packet_pin, "raw_packet": packet, "normalization": NORMALIZATION, "bindings": bindings,
        "procedure_gate": "NA" if global_errors else "PASS", "procedure_errors": global_errors,
        "image_gates": image_gates, "image_gate_counts": {s: sum(g == s for g in image_gates.values()) for s in STATUSES},
        "set_gate": set_gate, "diversity_applicable": n >= 2,
        "counts": {"requested_images": n, "packet_images": len(images), "critics": len(profiles), "expected_views_per_critic": 3*n, "expected_image_profile_records": 3*n, "observed_image_profile_records": observed_records, "expected_score_values": 21*n, "observed_score_slots": score_slots, "valid_integer_1_to_5_score_values": valid_scores},
        "reviews": reviews,
        "limits": ["PASS applies only to these observed pinned requests and candidate, not unseen-case quality", "fresh-session/byte provenance are checked; semantic viewing/order and visual evidence are critic attestations", "all raw low/invalid records retained; no critic replacement, mean-score cancellation or generated evaluation"]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True)
    parser.add_argument("--report", action="append", required=True, metavar="PROFILE=PATH")
    parser.add_argument("--completions-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        print("ERROR: output already exists; raw summary is immutable", file=sys.stderr)
        return 1
    try:
        result = summary(args)
        with open(output, "x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"output": str(output.resolve()), "sha256": digest(output), "procedure_gate": result["procedure_gate"], "image_gate_counts": result["image_gate_counts"], "set_gate": result["set_gate"], "counts": result["counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
