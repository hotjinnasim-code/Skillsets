#!/usr/bin/env python3
"""Preserve exact returned PNG bytes and seal inspected, bounded role evidence.

Use the bundled Python with Pillow. This helper neither calls an image model nor
claims that an image was viewed; inspection.json is the maker's recorded evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

STAGES = ("initial", "repair-1", "repair-2")
FILES = ("original.png", "final.png", "usage-720.png", "thumbnail-320.png", "manifest.json")


def fail(message):
    raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pin(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        fail(f"Not a file: {path}")
    return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size}


def load(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"Expected JSON object: {path}")
    return value


def png_dimensions(path):
    with open(path, "rb") as handle:
        head = handle.read(24)
    if len(head) != 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        fail(f"Not a PNG with an IHDR header: {path}")
    width, height = struct.unpack(">II", head[16:24])
    if width <= 0 or height <= 0:
        fail(f"Invalid PNG dimensions: {path}")
    return width, height


def image_pin(path):
    result = pin(path)
    result["width"], result["height"] = png_dimensions(path)
    return result


def exclusive_json(path, value):
    # O_EXCL is intentional: a selected stage or raw record is never replaced.
    with open(path, "x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def identity(value, role, stage, path, required=False):
    for key, expected in (("role", role), ("stage", stage)):
        if (required or key in value) and value.get(key) != expected:
            fail(f"{path}: {key} does not match {expected!r}")


def stage_inventory(role_dir):
    stages_dir = role_dir / "stages"
    if not stages_dir.is_dir():
        fail(f"Create stage inputs first: {stages_dir}")
    entries = list(stages_dir.iterdir())
    if any(not p.is_dir() or p.name not in STAGES or p.is_symlink() for p in entries):
        fail("stages/ may contain only initial, repair-1, repair-2 real directories")
    present = [s for s in STAGES if (stages_dir / s).exists()]
    if len(present) > 3 or present != list(STAGES[:len(present)]):
        fail("Stage sequence must be initial, then at most repair-1 and repair-2")
    return present


def checked_pin(value, label):
    if not isinstance(value, dict) or not isinstance(value.get("path"), str):
        fail(f"Missing pin: {label}")
    actual = pin(value["path"])
    if actual["sha256"] != value.get("sha256"):
        fail(f"Changed pinned bytes: {label}")
    if "bytes" in value and actual["bytes"] != value["bytes"]:
        fail(f"Changed pinned size: {label}")
    return actual


def input_pins(stage_dir, role, stage):
    result = {}
    for key, name in (("call_input", "call-input.json"), ("pre_call", "pre-call.json")):
        path = stage_dir / name
        value = load(path)
        identity(value, role, stage, path)
        result[key] = pin(path)
    return result


def save_native(args):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", args.role):
        fail("role must be a simple stable identifier")
    role_dir = Path(args.role_dir).resolve(strict=True)
    if (role_dir / "selection.json").exists():
        fail("Role is finalized; no new native stages are allowed")
    present = stage_inventory(role_dir)
    if args.stage not in present:
        fail("The selected stage must already contain call-input.json and pre-call.json")
    stage_dir = role_dir / "stages" / args.stage
    index = STAGES.index(args.stage)
    for earlier in STAGES[:index]:
        prior = role_dir / "stages" / earlier
        if (prior / "manifest.json").is_file() == (prior / "failure.json").is_file():
            fail(f"Earlier stage needs exactly one returned/failure outcome: {earlier}")
    if any((stage_dir / name).exists() for name in FILES) or (stage_dir / "failure.json").exists():
        fail("Refusing to overwrite an existing outcome or native/QA artifact")
    inputs = input_pins(stage_dir, args.role, args.stage)
    source_argument = Path(args.source)
    if not source_argument.is_absolute():
        fail("--source must be the exact absolute path returned by the native tool")
    source = source_argument.resolve(strict=True)
    if source == stage_dir or source.parent == stage_dir:
        fail("Returned native source must precede helper output")
    source_pin = image_pin(source)
    created = []
    try:
        for name in ("original.png", "final.png"):
            target = stage_dir / name
            with open(source, "rb") as src, open(target, "xb") as dst:
                created.append(target)
                shutil.copyfileobj(src, dst)
            if sha(target) != source_pin["sha256"]:
                fail("Native copy differs from the returned source")
        with Image.open(stage_dir / "original.png") as native:
            if native.format != "PNG" or native.size != (source_pin["width"], source_pin["height"]):
                fail("Decoded PNG dimensions disagree with the header")
            native.load()
            if getattr(native, "n_frames", 1) != 1:
                fail("Animated PNG is outside the single native poster contract")
            width, height = native.size
            qa_specs = {
                "usage-720.png": min(1.0, 720 / width),
                "thumbnail-320.png": min(1.0, 320 / max(width, height)),
            }
            for name, scale in qa_specs.items():
                size = (max(1, round(width * scale)), max(1, round(height * scale)))
                target = stage_dir / name
                with open(target, "xb") as handle:
                    created.append(target)
                    reduced = native.resize(size, Image.Resampling.LANCZOS)
                    reduced.save(handle, format="PNG")
        if sha(source) != source_pin["sha256"]:
            fail("Returned source changed during preservation")
        files = {
            "original": image_pin(stage_dir / "original.png"),
            "final": image_pin(stage_dir / "final.png"),
            "usage720": image_pin(stage_dir / "usage-720.png"),
            "thumbnail320": image_pin(stage_dir / "thumbnail-320.png"),
        }
        manifest = {
            "schema_version": 1, "kind": "native_evidence", "role": args.role,
            "stage": args.stage, "outcome": "returned", "native_call_count": 1,
            "saved_at_utc": datetime.now(timezone.utc).isoformat(),
            "saved_at_semantics": "helper preservation time; not native tool start/end",
            "source_argument": str(source_argument), "source": source_pin,
            "input_pins": inputs, "files": files,
            "native_byte_preserved": files["original"]["sha256"] == files["final"]["sha256"] == source_pin["sha256"],
            "qa": {"method": "Pillow LANCZOS, PNG, downsampling only", "usage720": "width <=720", "thumbnail320": "long side <=320"},
        }
        for key, pinned in inputs.items():
            checked_pin(pinned, key)
        exclusive_json(stage_dir / "manifest.json", manifest)
        created.append(stage_dir / "manifest.json")
    except Exception:
        for target in reversed(created):
            target.unlink(missing_ok=True)
        raise
    return {"role": args.role, "stage": args.stage, "manifest": pin(stage_dir / "manifest.json"), "source_sha256": source_pin["sha256"]}


def finalize(args):
    role_dir = Path(args.role_dir).resolve(strict=True)
    if (role_dir / "selection.json").exists():
        fail("selection.json already exists; it is immutable")
    stages = stage_inventory(role_dir)
    if args.selected_stage not in stages:
        fail("Selected stage is missing")
    records, role = [], None
    for stage in stages:
        folder = role_dir / "stages" / stage
        manifest_path, failure_path = folder / "manifest.json", folder / "failure.json"
        if manifest_path.is_file() == failure_path.is_file():
            fail(f"{stage} needs exactly one returned manifest or failure.json")
        path = manifest_path if manifest_path.is_file() else failure_path
        outcome = load(path)
        stage_role = outcome.get("role")
        if not isinstance(stage_role, str) or not stage_role:
            fail(f"Missing role identity: {path}")
        role = role or stage_role
        identity(outcome, role, stage, path, required=True)
        inputs = input_pins(folder, role, stage)
        record = {"stage": stage, "outcome": "returned" if manifest_path.is_file() else "failure", "input_pins": inputs}
        if manifest_path.is_file():
            if outcome.get("kind") != "native_evidence" or outcome.get("outcome") != "returned" or type(outcome.get("native_call_count")) is not int or outcome.get("native_call_count") != 1 or outcome.get("native_byte_preserved") is not True:
                fail(f"Invalid native manifest: {path}")
            for key in ("call_input", "pre_call"):
                if outcome.get("input_pins", {}).get(key) != inputs[key]:
                    fail(f"{stage}: input pin changed since native save")
            source_pin = checked_pin(outcome.get("source"), f"{stage}/source")
            files = outcome.get("files", {})
            for key, name in (("original", "original.png"), ("final", "final.png"), ("usage720", "usage-720.png"), ("thumbnail320", "thumbnail-320.png")):
                item = files.get(key)
                if not isinstance(item, dict) or item.get("path") != str((folder / name).resolve(strict=True)) or item != image_pin(folder / name):
                    fail(f"{stage}: missing or changed {key} artifact")
            if source_pin["sha256"] != files["original"]["sha256"] or source_pin["sha256"] != files["final"]["sha256"]:
                fail(f"{stage}: source/original/final native bytes differ")
            inspection_path = folder / "inspection.json"
            inspection = load(inspection_path)
            identity(inspection, role, stage, inspection_path, required=True)
            expected_paths = [files[key]["path"] for key in ("original", "usage720", "thumbnail320")]
            if inspection.get("actual_viewed") is not True or inspection.get("actual_view_paths") != expected_paths:
                fail(f"{stage}: actual inspection must name original, usage720, thumbnail320 in that order")
            if not isinstance(inspection.get("raw_observed_text"), list) or not isinstance(inspection.get("residuals"), list):
                fail(f"{stage}: inspection needs raw_observed_text and residuals arrays")
            record.update(manifest=pin(manifest_path), source=outcome["source"], files=files, inspection=pin(inspection_path))
            if stage != "initial":
                comparison_path = folder / "parent-comparison.json"
                comparison = load(comparison_path)
                identity(comparison, role, stage, comparison_path, required=True)
                parent = records[-1]
                if comparison.get("parent_stage") != parent["stage"] or comparison.get("parent_outcome") != parent["outcome"]:
                    fail(f"{stage}: comparison must name the immediate parent's actual outcome")
                if parent["outcome"] == "returned":
                    if comparison.get("parent_manifest_sha256") != parent["manifest"]["sha256"] or comparison.get("parent_native_sha256") != parent["source"]["sha256"]:
                        fail(f"{stage}: comparison has incorrect parent pins")
                elif comparison.get("parent_failure_sha256") != parent["failure"]["sha256"]:
                    fail(f"{stage}: comparison has incorrect failure pin")
                if not isinstance(comparison.get("changes"), list) or not isinstance(comparison.get("residuals"), list):
                    fail(f"{stage}: parent comparison needs changes and residuals arrays")
                record["parent_comparison"] = pin(comparison_path)
        else:
            if outcome.get("outcome") != "failure" or type(outcome.get("native_call_count")) is not int or outcome.get("native_call_count") != 1 or not isinstance(outcome.get("error"), str) or not outcome["error"]:
                fail(f"{stage}: failure.json needs outcome=failure, native_call_count=1 and recorded error")
            if any((folder / name).exists() for name in FILES):
                fail(f"{stage}: failure outcome may not hide native/QA artifacts")
            # Failure records are preserved, never relabeled as a returned image.
            record["failure"] = pin(failure_path)
            record["failure_metadata"] = outcome
        records.append(record)
    chosen = next(r for r in records if r["stage"] == args.selected_stage)
    if chosen["outcome"] != "returned":
        fail("A failed call cannot be the selected stage")
    counts = {"native_calls": len(records), "returned": sum(r["outcome"] == "returned" for r in records), "failed": sum(r["outcome"] == "failure" for r in records), "repair_calls": len(records) - 1}
    selection = {
        "schema_version": 1, "kind": "role_selection", "role": role,
        "selected_stage": args.selected_stage, "selected_manifest": chosen["manifest"],
        "selected_native_sha256": chosen["source"]["sha256"], "selected_files": chosen["files"],
        "selected_inspection": chosen["inspection"], "counts": counts, "stages": records,
        "sealed_at_utc": datetime.now(timezone.utc).isoformat(),
        "inspection_semantics": "recorded maker attestations; helper does not view or score images",
        "native_timing_semantics": "caller-recorded pre-call/input pins only; saved_at is not a native interval",
    }
    exclusive_json(role_dir / "selection.json", selection)
    return {"selection": pin(role_dir / "selection.json"), "selected_stage": args.selected_stage, "counts": counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    save = sub.add_parser("save-native")
    save.add_argument("--role", required=True)
    save.add_argument("--stage", choices=STAGES, required=True)
    save.add_argument("--source", required=True)
    save.add_argument("--role-dir", required=True)
    seal = sub.add_parser("finalize")
    seal.add_argument("--role-dir", required=True)
    seal.add_argument("--selected-stage", choices=STAGES, required=True)
    args = parser.parse_args()
    try:
        result = save_native(args) if args.command == "save-native" else finalize(args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
