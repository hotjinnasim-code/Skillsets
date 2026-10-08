#!/usr/bin/env python3
"""Read-only SHA/record validator and unaveraged R6 quality gate summary.

Outputs JSON to stdout or an exclusively created --output file. No raw review is
rewritten. Exit 0 = complete PASS; 1 = gate/integrity failure; 2 = input error.
Viewing and chronology remain critic attestations, never script certificates.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

DIMS = ("content_form", "hierarchy", "typography", "space", "image_material", "emotion_control", "ai_slop")
CORE = {"content_form", "typography", "image_material", "ai_slop"}
PROFILES = ("editorial", "craft", "portfolio")
VIEWS = ("native", "usage720", "thumbnail320")
ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def resolve(value, base=ROOT):
    path = Path(value)
    return (path if path.is_absolute() else base / path).resolve()


def norm(text):
    return " ".join(str(text).split())


def nonempty(text):
    return isinstance(text, str) and bool(text.strip())


def png_size(path):
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("Invalid native/QA PNG: " + str(path))
    return struct.unpack(">II", data[16:24])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--reviews-dir", type=Path)
    ap.add_argument("--output", type=Path, help="Exclusively create; an existing output is refused")
    args = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.wave):
        ap.error("Unsafe wave name")
    wave = ROOT / ("blind-" + args.wave)
    mapping_path = ROOT / "private" / (args.wave + "-mapping.json")
    packet_path = wave / "packet.json"
    reviews_dir = (args.reviews_dir or wave / "reviews").resolve()
    errors, failures, pins, image_bindings, critic_records, set_records, procedures, low_scores = [], [], [], [], [], [], {}, []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def bind(path, expected, label):
        path = path.resolve()
        require(path.is_file(), "Missing " + label + ": " + str(path))
        actual = sha(path) if path.is_file() else None
        require(isinstance(expected, str) and actual == expected, "Missing/mismatched SHA " + label + ": " + str(path))
        record = {"kind": label, "path": str(path), "expected_sha256": expected, "actual_sha256": actual}
        pins.append(record)
        return actual

    try:
        mapping_doc, packet = read(mapping_path), read(packet_path)
        require(mapping_doc["wave"] == args.wave, "Mapping wave differs")
        source_paths = {}
        for kind in ("selection", "plan", "cases"):
            pin = mapping_doc[kind]
            source_paths[kind] = resolve(pin["path"])
            bind(source_paths[kind], pin["sha256"], kind)
        plan, cases_doc, selection_doc = (read(source_paths[k]) for k in ("plan", "cases", "selection"))
        require(plan["cases"]["sha256"] == mapping_doc["cases"]["sha256"] and resolve(plan["cases"]["path"]) == source_paths["cases"], "Plan/cases pins differ")
        expected_pins = [dict(plan["cases"], kind="cases")] + [dict(p, kind="frozen_skill") for p in plan["frozen_skill_files"]]
        require(expected_pins == mapping_doc["frozen_source_pins"] and bool(plan["frozen_skill_files"]), "Frozen skill/source pin declaration differs or is empty")
        for pin in expected_pins:
            bind(resolve(pin["path"]), pin["sha256"], pin["kind"])
        review_plan = plan["review"]
        require(review_plan["independent_reviewers"] == 3 and tuple(review_plan["seven_dimensions"]) == DIMS, "Reviewer count/seven dimensions changed")
        gate_text = review_plan["unchanged_core_gate"]
        require(all(k in gate_text for k in CORE) and ">=4" in gate_text and "diversity" in gate_text, "Unsupported core/diversity gate")
        for path, expected in mapping_doc["packet_files"].items():
            bind(resolve(path), expected, "sealed packet file")
        require(set(mapping_doc["packet_files"]) == {str(wave / name) for name in ("packet.json", "preflight.json", "review-protocol.md")}, "Sealed packet file coverage differs")
        cases = {c["id"]: c for c in cases_doc["cases"]}
        require(len(cases) == len(cases_doc["cases"]), "Duplicate frozen case ID")
        rolemap = {s["id"]: (c["id"], s["ratio"]) for c in cases.values() for s in c["slots"]}
        selected = {s["role"]: s for s in selection_doc["selected"]}
        require(len(selected) == len(selection_doc["selected"]), "Duplicate physical selection role")
        images, mapping = packet["images"], mapping_doc["mapping"]
        by_id, by_map = ({x["image_id"]: x for x in entries} for entries in (images, mapping))
        ids = set(by_id)
        require(len(ids) == len(images) and len(by_map) == len(mapping) and ids == set(by_map), "Duplicate or differing packet/mapping IDs")
        require(len({x["role"] for x in mapping}) == len(mapping), "Repeated selected role")
        if len({x["sha256"] for x in mapping}) != len(mapping):
            failures.append({"kind": "duplicate_native_bytes_across_roles", "evidence": "Distinct scheduled roles returned identical preserved bytes; diversity cannot pass."})
        require(set(packet["cases"]) == set(packet["sets"]) == {x["case_id"] for x in images}, "Packet case/set coverage differs")
        for cid, declared in packet["cases"].items():
            original = cases[cid]
            require(declared == {"request": original["request"], "copy": original["copy"], "expected_count": 5}, "Packet exact request/full copy differs: " + cid)
            require(original["expected_final_count"] == 5 and len(original["slots"]) == 5, "R6 case does not declare five slots: " + cid)
            members = [x["image_id"] for x in images if x["case_id"] == cid]
            declared_members = packet["sets"][cid]["members"]
            require(len(members) == len(declared_members) == len(set(declared_members)) == 5 and set(members) == set(declared_members)
                    and packet["sets"][cid]["expected_count"] == 5, "Case exact membership/count differs: " + cid)
            require({m["role"] for m in mapping if m["case_id"] == cid} == {s["id"] for s in original["slots"]}, "Selected case slot coverage differs: " + cid)
        for ident, item in by_id.items():
            mapped = by_map[ident]
            role, cid = mapped["role"], item["case_id"]
            require(cid == mapped["case_id"] == rolemap[role][0] and item["target_ratio"] == rolemap[role][1], "Mapped role/case/ratio differs: " + ident)
            require({k: mapped[k] for k in selected[role]} == selected[role], "Physical selection record changed: " + ident)
            require(mapped["sha256"] == mapped["native_sha256"], "Native SHA fields disagree: " + ident)
            source = resolve(mapped["final_native"])
            manifest = resolve(mapped["manifest"])
            bind(source, mapped["sha256"], ident + " source native")
            bind(manifest, mapped["manifest_sha256"], ident + " source manifest")
            record = {"image_id": ident, "role": role, "case_id": cid, "stage": mapped["stage"], "source_native": str(source),
                      "source_manifest": str(manifest), "source_manifest_sha256": mapped["manifest_sha256"], "native_sha256": mapped["sha256"], "views": {}}
            require(set(mapped["qa_hashes"]) == {item[v] for v in VIEWS}, "QA pin coverage differs: " + ident)
            for view in VIEWS:
                path = resolve(item[view], wave)
                actual = bind(path, mapped["qa_hashes"].get(str(path)), ident + " " + view)
                size = png_size(path)
                record["views"][view] = {"path": str(path), "sha256": actual, "dimensions": list(size)}
                if view == "native":
                    require(actual == mapped["sha256"] and size == (item["width"], item["height"]) == (mapped["width"], mapped["height"]), "Native bytes/dimensions differ: " + ident)
                    numerator, denominator = map(int, item["target_ratio"].split(":"))
                    if abs((size[0] / size[1]) / (numerator / denominator) - 1) > .01:
                        failures.append({"kind": "mandatory_ratio", "image_id": ident, "actual": list(size), "required": item["target_ratio"]})
                else:
                    require(size[0] == 720 if view == "usage720" else max(size) == 320, "Wrong QA scale: " + ident + "/" + view)
                    require(abs((size[0] / size[1]) / (item["width"] / item["height"]) - 1) <= .01, "Distorted QA ratio: " + ident + "/" + view)
            image_bindings.append(record)

        preflight_packet = read(wave / "preflight.json")
        action = {x["image_id"]: x for x in preflight_packet["images"]}
        expected_action = {ident for ident, item in by_id.items() if cases[item["case_id"]].get("action_fields", {})}
        require(set(action) == expected_action and len(action) == len(preflight_packet["images"]), "Preflight packet coverage differs")
        for ident, entry in action.items():
            require(entry["usage720"] == by_id[ident]["usage720"] and entry["fields"] == list(cases[by_id[ident]["case_id"]]["action_fields"]), "Preflight actual720/action field names differ: " + ident)
        raw_reports = {}
        for profile in PROFILES:
            raw_path = reviews_dir / (profile + ".json")
            md_path = reviews_dir / (profile + ".md")
            preflight_path = reviews_dir / (profile + "-action-first.json")
            report, preflight = read(raw_path), read(preflight_path)
            raw_sha, md_sha, preflight_sha = sha(raw_path), sha(md_path), sha(preflight_path)
            raw_reports[profile] = report
            require(nonempty(md_path.read_text()), profile + " empty Markdown review")
            require(report["reviewer"] == preflight["reviewer"] == profile, profile + " reviewer identity differs")
            require(type(report.get("order_compliant")) is bool and type(preflight.get("order_compliant")) is bool, profile + " missing Boolean order attestation")
            require(report.get("order_compliant") is True and preflight.get("order_compliant") is True, profile + " disclosed/missing compliant preflight-before-copy order")
            require(nonempty(report.get("method")) and any(word in report["method"].lower() for word in ("manual", "independently transcribed", "수동", "판독", "전사")), profile + " missing manual visual transcription method")
            require(nonempty(preflight.get("method")), profile + " missing preflight method")
            require(set(report["images"]) == ids and set(report["sets"]) == set(packet["sets"]), profile + " exact image/set review coverage differs")

            def validate_views(entries, expected, label):
                require(isinstance(entries, list), profile + " actual viewed records must remain a list: " + label)
                triples = []
                for entry in entries:
                    ident, view, path = entry["image_id"], entry["view"], resolve(entry["path"], wave)
                    require(ident in by_id and view in VIEWS, profile + " unknown actual view " + label)
                    if ident in by_id and view in VIEWS:
                        require(path == resolve(by_id[ident][view], wave), profile + " unbound actual viewed path: " + ident + "/" + view)
                    triples.append((ident, view, str(path)))
                require(set(triples) == expected, profile + " actual view record coverage differs: " + label)
                return entries

            expected_views = {(ident, view, str(resolve(item[view], wave))) for ident, item in by_id.items() for view in VIEWS}
            validate_views(report["viewed"], expected_views, "native/720/320")
            expected_preflight_views = {(ident, "usage720", str(resolve(by_id[ident]["usage720"], wave))) for ident in expected_action}
            validate_views(preflight["viewed"], expected_preflight_views, "preflight720")
            readings = preflight["readings"]
            require(isinstance(readings, list), profile + " preflight readings must remain a list")
            readings_by_id = {x["image_id"]: x for x in readings}
            require(len(readings_by_id) == len(readings) and set(readings_by_id) == expected_action, profile + " preflight exact action/empty reading coverage differs")
            action_failures = []
            for ident, reading in readings_by_id.items():
                fields = cases[by_id[ident]["case_id"]]["action_fields"]
                require(resolve(reading["path"], wave) == resolve(by_id[ident]["usage720"], wave), profile + " preflight reading is not bound actual720: " + ident)
                require(set(reading["fields"]) == set(fields) and all(isinstance(v, str) for v in reading["fields"].values()), profile + " preflight field coverage/type differs: " + ident)
                require(isinstance(reading.get("uncertainties"), list), profile + " missing preflight uncertainty list: " + ident)
                for field, expected in fields.items():
                    observed = reading["fields"].get(field)
                    if norm(observed) != norm(expected):
                        failure = {"profile": profile, "image_id": ident, "kind": "action_reading", "field": field, "required": expected, "observed": observed, "raw_sha256": preflight_sha}
                        failures.append(failure)
                        action_failures.append(failure)
            procedures[profile] = {"raw_report": str(raw_path), "raw_report_sha256": raw_sha, "raw_markdown": str(md_path), "raw_markdown_sha256": md_sha,
                                   "preflight": str(preflight_path), "preflight_sha256": preflight_sha, "preflight_raw_observations": preflight,
                                   "recorded_actual_views": report["viewed"], "method": report["method"], "order_compliant": report.get("order_compliant"),
                                   "preflight_order_compliant": preflight.get("order_compliant"), "action_reading_failures": action_failures}
            for ident, observation in report["images"].items():
                if ident not in by_id:
                    continue
                scores, evidence, mandatory = observation["scores"], observation["evidence"], observation["mandatory"]
                require(set(scores) == set(DIMS) and all(type(scores.get(d)) is int and 1 <= scores[d] <= 5 for d in DIMS), profile + " scores must be exactly seven integers1–5: " + ident)
                require(set(evidence) == set(DIMS) and all(nonempty(evidence.get(d)) for d in DIMS), profile + " seven located evidence fields missing: " + ident)
                require(isinstance(observation.get("residuals"), list), profile + " missing residual list: " + ident)
                require(type(mandatory.get("pass")) is bool and isinstance(mandatory.get("issues"), list) and isinstance(mandatory.get("uncertainties"), list), profile + " malformed mandatory/issue/uncertainty record: " + ident)
                use = mandatory.get("use_readings", {})
                require(isinstance(use, dict) and type(use.get("all_required_copy_legible_at720")) is bool and nonempty(use.get("observations")), profile + " missing actual720 copy legibility reading: " + ident)
                required_copy = cases[by_id[ident]["case_id"]]["copy"]
                transcription = mandatory["transcription"]
                require([t.get("required") for t in transcription] == required_copy, profile + " exact full-copy transcription coverage differs: " + ident)
                copy_failures = []
                for item in transcription:
                    require(isinstance(item.get("observed"), str) and type(item.get("equal")) is bool, profile + " invalid manual transcription type: " + ident)
                    equal = norm(item.get("required", "")) == norm(item.get("observed", ""))
                    require(item.get("equal") == equal, profile + " recorded equality contradicts transcription: " + ident)
                    if not equal:
                        copy_failures.append(item)
                record = {"profile": profile, "image_id": ident, "role": by_map[ident]["role"], "case_id": by_id[ident]["case_id"],
                          "raw_path": str(raw_path), "raw_sha256": raw_sha, "mandatory": mandatory, "scores": scores, "evidence": evidence, "residuals": observation.get("residuals")}
                critic_records.append(record)
                if mandatory.get("pass") is False or copy_failures or use.get("all_required_copy_legible_at720") is False:
                    failures.append({"profile": profile, "image_id": ident, "kind": "mandatory", "record": mandatory, "copy_failures": copy_failures, "raw_sha256": raw_sha})
                for dimension, score in scores.items():
                    if type(score) is int and score < 4:
                        low = {"profile": profile, "image_id": ident, "role": by_map[ident]["role"], "dimension": dimension, "score": score,
                               "core": dimension in CORE, "evidence": evidence.get(dimension), "raw_sha256": raw_sha}
                        low_scores.append(low)
                        if dimension in CORE:
                            failures.append(dict(low, kind="core"))
            for cid, observation in report["sets"].items():
                if cid not in packet["sets"]:
                    continue
                members = observation["members"]
                require(len(members) == len(set(members)) == 5 and set(members) == set(packet["sets"][cid]["members"]), profile + " exact set members differ: " + cid)
                diversity = observation.get("diversity")
                pair = observation["closest_pair"]
                require(type(diversity) is int and 1 <= diversity <= 5, profile + " diversity must be integer1–5: " + cid)
                require(isinstance(pair, dict) and len(pair["members"]) == len(set(pair["members"])) == 2 and set(pair["members"]) <= set(members)
                        and type(pair.get("score")) is int and 1 <= pair["score"] <= 5 and nonempty(pair.get("evidence")), profile + " invalid closest pair members/score/evidence: " + cid)
                require(nonempty(observation.get("evidence")) and isinstance(observation.get("residuals"), list), profile + " missing diversity evidence/residuals: " + cid)
                record = dict(observation, profile=profile, case_id=cid, raw_path=str(raw_path), raw_sha256=raw_sha)
                set_records.append(record)
                if type(diversity) is int and diversity < 4:
                    failures.append(dict(record, kind="diversity"))

        disagreements = []
        for ident in by_id:
            for dimension in DIMS:
                values = {p: raw_reports[p]["images"].get(ident, {}).get("scores", {}).get(dimension) for p in PROFILES}
                if len({json.dumps(v) for v in values.values()}) > 1:
                    disagreements.append({"image_id": ident, "dimension": dimension, "raw_scores": values})
        for cid in packet["sets"]:
            values = {p: raw_reports[p]["sets"].get(cid, {}).get("diversity") for p in PROFILES}
            if len({json.dumps(v) for v in values.values()}) > 1:
                disagreements.append({"case_id": cid, "dimension": "diversity", "raw_scores": values})
        quality = "FAIL" if failures else ("PASS" if not errors else "NOT_ASSESSABLE")
        result = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "wave": args.wave, "status": "PASS" if not errors and not failures else "FAIL",
                  "recorded_evidence_integrity": "FAIL" if errors else "PASS", "predeclared_core_diversity_gate": quality,
                  "scope": "Exact SHA/record structure checks only. Actual viewed-path records and preflight-before-copy chronology remain critic attestations; this script cannot prove viewing, order, semantic location, visual quality, authorship, physical mechanics, print suitability or future capability. Raw scores remain authoritative. No averages, consensus rewrite, or extra nearest-pair score threshold.",
                  "predeclared_gate_text": gate_text, "inputs": {"packet": str(packet_path), "packet_sha256": sha(packet_path), "mapping": str(mapping_path), "mapping_sha256": sha(mapping_path)},
                  "selected_image_count": len(images), "critics": list(PROFILES), "image_critic_record_count": len(critic_records), "score_observation_count": sum(len(r["scores"]) for r in critic_records),
                  "integrity_errors": errors, "source_pin_checks": pins, "image_bindings": image_bindings, "review_procedure": procedures, "image_critic_records": critic_records,
                  "all_scores_below4": low_scores, "core_below4_count": sum(r["core"] for r in low_scores), "noncore_below4_count": sum(not r["core"] for r in low_scores),
                  "all_set_records": set_records, "diversity_below4_count": sum(r["kind"] == "diversity" for r in failures), "disagreements": disagreements, "located_gate_failures": failures}
        code = 0 if result["status"] == "PASS" else 1
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        result = {"wave": args.wave, "status": "FAIL", "recorded_evidence_integrity": "FAIL", "predeclared_core_diversity_gate": "FAIL" if failures else "NOT_ASSESSABLE",
                  "input_error": type(error).__name__ + ": " + str(error), "integrity_errors": errors, "located_gate_failures": failures,
                  "source_pin_checks": pins, "image_critic_records": critic_records, "review_procedure": procedures}
        code = 2
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.resolve().open("x") as stream:
            stream.write(content)
    else:
        sys.stdout.write(content)
    return code


if __name__ == "__main__":
    sys.exit(main())
