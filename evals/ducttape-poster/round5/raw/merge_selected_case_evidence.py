#!/usr/bin/env python3
"""Merge closed garden5 with complete material cases and a predeclared G control.

Read-only for all inputs. Writes only the explicitly requested new output file.
Exit 0: selected gate PASS; 1: FAIL/rejected bindings; 2: malformed inputs.
"""
import argparse
import copy
import datetime as dt
import hashlib
import json
import struct
import sys
from pathlib import Path

DIMS = ("content_form", "hierarchy", "typography", "space", "image_material", "emotion_control", "ai_slop")
CORE = {"content_form", "typography", "image_material", "ai_slop"}
CASES = {"title-only": {"G01", "G02", "G03", "G04", "G05"},
         "product": {"P01", "P02"}, "invitation": {"H01", "H02"}}
VIEWS = ("native", "usage720", "thumbnail320")
G_PLAN_SHA256 = "96160b13510366e678e1f7d2769374e22366e07baa9d3ebf1785bbd492f2a3a8"
G_CASES_SHA256 = "af995f8bd218ef2e49b3933a0403db2d50ccaab996cea38b7cbc489751c8a8bb"
CONTROL_CASE = "type-only-control"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def resolved(value, base):
    path = Path(value)
    return (path if path.is_absolute() else base / path).resolve()


def png_size(path):
    data = Path(path).read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("Not PNG with IHDR: " + str(path))
    return list(struct.unpack(">II", data[16:24]))


def norm(value):
    return " ".join(str(value).split())


def nonempty(value):
    return bool(value.strip()) if isinstance(value, str) else isinstance(value, list) and bool(value) and all(nonempty(x) for x in value)


def closest_pair(record):
    pair = record.get("closest_pair", record.get("nearest_pair", []))
    members = pair.get("members", []) if isinstance(pair, dict) else pair
    score = record.get("closest_pair_diversity", record.get("closest_pair_score", pair.get("score", pair.get("diversity")) if isinstance(pair, dict) else None))
    return members, score


def reviewer_profile(record):
    value = record.get("reviewer", record.get("profile"))
    return value.get("profile") if isinstance(value, dict) else value


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ("garden-summary", "material-summary", "selection", "output"):
        ap.add_argument("--" + name, type=Path, required=True)
    args = ap.parse_args()
    output = args.output.resolve()
    errors, records, bindings, set_records, procedures = [], [], [], [], {}
    source_refs, source_pins, excluded = {}, [], {}
    raw_cache = {}

    def require(ok, message):
        if not ok:
            errors.append(message)

    def pin(path, expected, label):
        require(Path(path).is_file(), "Missing " + label + ": " + str(path))
        if Path(path).is_file():
            actual = sha(path)
            require(isinstance(expected, str) and actual == expected, "SHA changed/missing " + label + ": " + str(path))
            return actual
        return None

    def raw(path, expected, label):
        path = Path(path).resolve()
        pin(path, expected, label)
        if path not in raw_cache:
            raw_cache[path] = read(path)
        return raw_cache[path]

    def metadata_pins(value, base, context="", found=None):
        """Verify explicit metadata file/hash pairs; never derive a score."""
        found = [] if found is None else found
        if isinstance(value, dict):
            pairs = [("path", "sha256"), ("source_path", "source_sha256"), ("supplement_path", "supplement_sha256")]
            pairs += [(k[:-7], k) for k in value if k.endswith("_sha256") and k[:-7] in value]
            for path_key, hash_key in pairs:
                if isinstance(value.get(path_key), str) and isinstance(value.get(hash_key), str):
                    pp = resolved(value[path_key], base)
                    pin(pp, value[hash_key], "source metadata " + context)
                    if "supplement" in context.lower() or "supplement" in str(pp).lower():
                        found.append({"path": str(pp), "sha256": value[hash_key]})
            for key, item in value.items():
                metadata_pins(item, base, context + "/" + key, found)
        elif isinstance(value, list):
            for item in value:
                metadata_pins(item, base, context, found)
        return found

    try:
        paths = {"garden": args.garden_summary.resolve(), "material": args.material_summary.resolve()}
        selection_path = args.selection.resolve()
        # Do not overwrite an input, source evidence, or an existing artifact.
        if output != Path("/dev/null") and output.exists():
            raise ValueError("Output already exists; choose a new output path")
        require(output not in {*paths.values(), selection_path}, "Output is an input path")
        sources = {key: read(path) for key, path in paths.items()}
        gate = sources["garden"]["predeclared_gate_text"]
        require(gate == sources["material"]["predeclared_gate_text"], "Source seven/core gate texts differ")
        require(all(x in gate for x in CORE) and ">=4" in gate and "diversity" in gate, "Unrecognized core/diversity gate")
        require(sources["garden"]["wave"] == "correction2", "Garden must use the closed correction2 wave")
        require(sources["garden"]["wave"] != sources["material"]["wave"], "Garden and material source waves must differ")
        choices_list = read(selection_path)["selected"]
        choices = {x["role"]: x for x in choices_list}
        expected_roles = set().union(*CASES.values())
        require(len(choices_list) == len(choices) == 9 and set(choices) == expected_roles, "Selection must contain exact nine unique roles")
        root = Path(__file__).resolve().parent
        g_plan_path = (root / "continuation-g/planning/phase-plan.json").resolve()
        g_cases_path = (root / "continuation-g/planning/cases.json").resolve()
        material = sources["material"]
        g_transfer_required = (resolved(material["inputs"]["plan"], paths["material"].parent) == g_plan_path
                               or any(x.get("role") == "T01" or x.get("case_id") == CONTROL_CASE for x in material["image_bindings"]))
        review_cases = dict(CASES)
        if g_transfer_required:
            review_cases[CONTROL_CASE] = {"T01"}
            require(resolved(material["inputs"]["plan"], paths["material"].parent) == g_plan_path
                    and material["inputs"]["plan_sha256"] == G_PLAN_SHA256, "G material/control must pin the exact predeclared G plan")
            pin(g_plan_path, G_PLAN_SHA256, "predeclared G plan")
            pin(g_cases_path, G_CASES_SHA256, "predeclared G cases")
            singleton = material.get("predeclared_singleton_cases", {}).get(CONTROL_CASE, {})
            require(singleton.get("role") == "T01"
                    and singleton.get("source_plan") == {"path": str(g_plan_path), "sha256": G_PLAN_SHA256}
                    and singleton.get("source_cases") == {"path": str(g_cases_path), "sha256": G_CASES_SHA256},
                    "Material source lacks exact T01 singleton predeclaration pins")

        contexts = {}
        for key, source in sources.items():
            require(source["recorded_evidence_integrity"] == "PASS" and not source.get("integrity_errors"), key + " source integrity is not PASS")
            for closed_pin in source.get("closed_source_pin_checks", []):
                closed_path = resolved(closed_pin["path"], paths[key].parent)
                pin(closed_path, closed_pin.get("expected_sha256", closed_pin.get("sha256")), key + " historical closed pin")
            profiles = source["critics"]
            supplement_pins = metadata_pins(source, paths[key].parent)
            require(len(profiles) == len(set(profiles)) == 3, key + " source must contain exactly three critics")
            source_refs[key] = {"path": str(paths[key]), "sha256": sha(paths[key]), "source_review_wave": source["wave"],
                                "historical_status": source.get("status"), "historical_quality_gate": source.get("predeclared_core_diversity_gate"),
                                "historical_image_critic_record_count": source.get("image_critic_record_count"),
                                "historical_core_below4_count": source.get("core_below4_count"),
                                "historical_diversity_below4_count": source.get("diversity_below4_count")}
            inputs = source["inputs"]
            for field in ("packet", "mapping", "plan"):
                path = resolved(inputs[field], paths[key].parent)
                pin(path, inputs[field + "_sha256"], key + " " + field)
                source_pins.append({"source": key, "path": str(path), "sha256": inputs[field + "_sha256"]})
            packet_path = resolved(inputs["packet"], paths[key].parent)
            packet = read(packet_path)
            plan = read(resolved(inputs["plan"], paths[key].parent))
            require(tuple(plan["review"]["seven_dimensions"]) == DIMS, key + " plan seven dimensions differ")
            require(plan["review"]["unchanged_core_gate"] == gate, key + " plan core gate differs from summary")
            mapping_doc = read(resolved(inputs["mapping"], paths[key].parent))
            mapping_list = mapping_doc["mapping"] if isinstance(mapping_doc, dict) else mapping_doc
            mapping = {x["role"]: x for x in mapping_list}
            require(len(mapping_list) == len(mapping), key + " duplicate mapped role")
            image_list = packet["images"]
            packet_images = {x["image_id"]: x for x in image_list}
            require(len(packet_images) == len(image_list), key + " duplicate packet anonymous ID")
            by_role = {x["role"]: x for x in source["image_bindings"]}
            require(len(by_role) == len(source["image_bindings"]), key + " duplicate summary role")
            contexts[key] = {"packet_path": packet_path, "packet": packet, "packet_images": packet_images, "plan": plan,
                             "mapping": mapping, "by_role": by_role, "profiles": profiles, "supplement_pins": supplement_pins}
            included_cases = {"title-only"} if key == "garden" else {"product", "invitation"}
            if key == "material" and g_transfer_required:
                included_cases.add(CONTROL_CASE)
                require(plan.get("status") == "PREDECLARED_BEFORE_FIRST_G_NATIVE_CALL"
                        and plan.get("scope", {}).get("additional_control_role") == "T01"
                        and "no diversity or closest pair score" in plan.get("scope", {}).get("singleton_rule", ""),
                        "G plan does not predeclare this singleton control")
                require(mapping_doc.get("predeclared_cases") == {"path": str(g_cases_path), "sha256": G_CASES_SHA256},
                        "G material mapping cases source differs")
                definition = next(x for x in read(g_cases_path)["cases"] if x.get("review_case_id") == CONTROL_CASE)
                brief = packet["cases"].get(CONTROL_CASE, {})
                require(brief.get("request") == definition["request"] and brief.get("copy") == definition["copy"]
                        and brief.get("expected_count") == 1 and brief.get("source_case_id") == definition["id"]
                        and brief.get("singleton_diversity") == "not_applicable", "G control packet brief differs from frozen declaration")
                source_pins.append({"source": key, "path": str(g_cases_path), "sha256": G_CASES_SHA256})
            included_roles = set().union(*(review_cases[c] for c in included_cases))
            if key == "material":
                require(set(by_role) == set(mapping) == included_roles,
                        "Material source must review exactly complete product/invitation cases plus the required predeclared control, when applicable")
                require(set(packet["cases"]) == set(packet["sets"]) == included_cases,
                        "Material packet case coverage differs")
            historical_excluded_roles = set(by_role) - included_roles
            excluded[key] = {"roles": sorted(historical_excluded_roles), "case_ids": sorted({x["case_id"] for x in source["image_bindings"] if x["role"] in historical_excluded_roles}),
                             "source_summary_ref": source_refs[key],
                             "all_scores_below4": [copy.deepcopy(x) for x in source.get("all_scores_below4", []) if x.get("role") in historical_excluded_roles],
                             "excluded_case_gate_failures": [copy.deepcopy(x) for x in source.get("located_gate_failures", []) if x.get("role") in historical_excluded_roles or x.get("case_id") not in included_cases and x.get("kind") == "diversity"],
                             "scope": "Historical excluded cases remain in the exact source summary/raw archive. No scores were rewritten or included selectively within a case."}
            for profile in profiles:
                proc = copy.deepcopy(source["review_procedure"][profile])
                label = source["wave"] + "/" + profile
                require(label not in procedures, "Composite reviewer label collision: " + label)
                report_path = resolved(proc["raw_report"], paths[key].parent)
                report = raw(report_path, proc["raw_report_sha256"], label + " procedure raw")
                require(reviewer_profile(report) == profile, label + " raw reviewer identity differs")
                if proc.get("raw_markdown_sha256"):
                    pin(resolved(proc["raw_markdown"], paths[key].parent), proc["raw_markdown_sha256"], label + " method/order Markdown")
                preflight_path = resolved(proc["action_first_record"], paths[key].parent)
                preflight = raw(preflight_path, proc["action_first_sha256"], label + " preflight")
                require(preflight == proc["action_first_raw_observations"], label + " preflight raw/preserved record differs")
                require(reviewer_profile(preflight) == profile, label + " preflight reviewer differs")
                require(report.get("viewed", []) == proc["recorded_view_entries"], label + " raw/procedure view records differ")
                require(nonempty(proc.get("manual_method_attestation")), label + " manual transcription attestation missing")
                if key == "material":
                    require(proc.get("valid_action_first_attestation") is True and not proc.get("explicit_procedural_failure_retained"), label + " material invitation preflight is not valid")
                proc.update({"source_review_wave": source["wave"], "source_profile": profile, "profile": label,
                             "source_summary_ref": source_refs[key], "included_cases": sorted(included_cases), "included_roles": sorted(included_roles)})
                procedures[label] = proc

        for case, roles in review_cases.items():
            key = "garden" if case == "title-only" else "material"
            source, ctx = sources[key], contexts[key]
            case_bindings = [x for x in source["image_bindings"] if x["case_id"] == case]
            require(len(case_bindings) == len(roles) and {x["role"] for x in case_bindings} == roles, case + " source case is incomplete")
            require(case in ctx["packet"]["sets"], case + " packet set missing")
            members = {x["image_id"] for x in case_bindings}
            packet_set = ctx["packet"]["sets"][case]
            require(set(packet_set["members"]) == members and len(packet_set["members"]) == len(roles) == packet_set["expected_count"], case + " packet set membership/count differs")
            require(ctx["packet"]["cases"][case]["expected_count"] == len(roles), case + " packet brief count differs")
            labels = [source["wave"] + "/" + p for p in ctx["profiles"]]
            for role in sorted(roles):
                choice, original_binding = (ctx["mapping"][role] if role == "T01" else choices[role]), ctx["by_role"][role]
                mapped = ctx["mapping"][role]
                # Mappings record the original selected manifest and full lineage choice.
                for field in ("role", "stage", "sha256", "width", "height", "manifest_sha256"):
                    require(choice.get(field) == mapped.get(field), role + " selection/mapping differs: " + field)
                for field in ("final_native", "manifest"):
                    require(resolved(choice[field], selection_path.parent) == resolved(mapped[field], ctx["packet_path"].parent.parent), role + " selected mapped path differs: " + field)
                require(choice.get("phase") == mapped.get("phase"), role + " selection/mapping phase differs")
                if key == "material" and role in {"P01", "H01"}:
                    require(choice.get("phase") == "F", role + " material selection is not new F lineage")
                if key == "material" and g_transfer_required:
                    expected_phase = "F" if role in {"P01", "H01"} else "G"
                    require(choice.get("phase") == expected_phase, role + " G material/control phase differs")
                    require(choice.get("stage") in {"initial", "repair-1", "repair-2"}, role + " unexpected selected stage")
                    expected_manifest = root / ("continuation-" + expected_phase.lower()) / "production" / role / choice["stage"] / "manifest.json"
                    require(resolved(choice["manifest"], selection_path.parent) == expected_manifest.resolve(),
                            role + " manifest is outside its predeclared phase/role lineage")
                fp = resolved(choice["final_native"], selection_path.parent)
                require(fp == resolved(original_binding["selected_native"], paths[key].parent), role + " selected source path differs from closed summary")
                require(choice["sha256"] == original_binding["native_sha256"], role + " selected native SHA differs from closed summary")
                require(choice["stage"] == original_binding["stage"], role + " selected stage differs from closed summary")
                pin(fp, choice["sha256"], role + " selected native")
                manifest_path = resolved(choice["manifest"], selection_path.parent)
                manifest = raw(manifest_path, choice["manifest_sha256"], role + " selected manifest")
                require(manifest["role"] == role and manifest["stage"] == choice["stage"], role + " manifest role/stage differs")
                require(resolved(manifest["final"]["path"], manifest_path.parent) == fp and manifest["final"]["sha256"] == choice["sha256"], role + " manifest final differs")
                require(png_size(fp) == [choice["width"], choice["height"]] == [manifest["width"], manifest["height"]], role + " native dimensions differ")
                ident = original_binding["image_id"]
                require(mapped["image_id"] == ident and mapped["case_id"] == case, role + " anonymous case/mapping differs")
                packet_image = ctx["packet_images"][ident]
                require(packet_image["case_id"] == case, role + " packet case differs")
                require(set(original_binding["views"]) == set(VIEWS), role + " not exact native/720/320 views")
                mapping_qa = {resolved(p, ctx["packet_path"].parent.parent): h for p, h in mapped["qa_hashes"].items()}
                for view in VIEWS:
                    rec = original_binding["views"][view]
                    vp = resolved(rec["path"], paths[key].parent)
                    require(vp == resolved(packet_image[view], ctx["packet_path"].parent), role + " packet/view path differs: " + view)
                    require(rec["sha256"] == mapping_qa.get(vp), role + " mapping/view SHA differs: " + view)
                    pin(vp, rec["sha256"], role + " " + view)
                    dimensions = png_size(vp)
                    require(dimensions == rec["dimensions"], role + " view dimensions differ: " + view)
                    if view == "native":
                        require(rec["sha256"] == choice["sha256"] and dimensions == [choice["width"], choice["height"]], role + " anonymous native differs")
                    else:
                        require(dimensions[0] == 720 if view == "usage720" else max(dimensions) == 320, role + " QA size differs: " + view)
                rows = [x for x in source["image_critic_records"] if x["role"] == role]
                require(len(rows) == 3 and {x["profile"] for x in rows} == set(ctx["profiles"]), role + " not three complete raw critics")
                for row in rows:
                    profile = row["profile"]
                    label = source["wave"] + "/" + profile
                    require(row["image_id"] == ident, role + " critic anonymous ID differs")
                    report_path = resolved(row["raw_path"], paths[key].parent)
                    report = raw(report_path, row["raw_sha256"], role + "/" + profile + " raw report")
                    require(report_path == resolved(procedures[label]["raw_report"], paths[key].parent), role + " procedure/image raw source differs")
                    obs = report["images"][ident]
                    for field in ("mandatory", "scores", "evidence"):
                        require(obs[field] == row[field], role + "/" + profile + " raw observation differs: " + field)
                    require(obs.get("residuals", []) == row.get("residuals", []), role + "/" + profile + " raw residuals differ")
                    require(set(row["scores"]) == set(DIMS) and all(type(row["scores"][d]) is int and 1 <= row["scores"][d] <= 5 for d in DIMS), role + " invalid seven scores")
                    require(set(row["evidence"]) == set(DIMS) and all(nonempty(row["evidence"][d]) for d in DIMS), role + " missing evidence")
                    require(type(row["mandatory"].get("pass")) is bool and "issues" in row["mandatory"] and "uncertainties" in row["mandatory"], role + " invalid mandatory/uncertainty record")
                    required = ctx["packet"]["cases"][case]["copy"]
                    transcription = row["mandatory"]["transcription"]
                    require([x["required"] for x in transcription] == required, role + " all-item copy coverage differs")
                    for item in transcription:
                        require(type(item["equal"]) is bool and item["equal"] == (norm(item["required"]) == norm(item["observed"])), role + " transcription equality differs")
                    views = {(x["image_id"], x["view"], resolved(x["path"], ctx["packet_path"].parent)) for x in report["viewed"]}
                    for view in VIEWS:
                        require((ident, view, resolved(original_binding["views"][view]["path"], paths[key].parent)) in views, role + "/" + profile + " lacks recorded bound view: " + view)
                    merged_row = copy.deepcopy(row)
                    merged_row.update({"profile": label, "source_profile": profile, "review_wave": source["wave"], "source_review_wave": source["wave"], "case_id": case})
                    records.append(merged_row)
                b = copy.deepcopy(original_binding)
                b.update({"critic_profiles": labels, "review_wave": source["wave"], "source_summary_ref": source_refs[key],
                          "manifest": str(manifest_path), "manifest_sha256": choice["manifest_sha256"], "phase": choice.get("phase")})
                bindings.append(b)
            rows = [x for x in source["all_set_records"] if x["case_id"] == case]
            require(len(rows) == 3 and {x["profile"] for x in rows} == set(ctx["profiles"]), case + " not three complete set critics")
            for row in rows:
                profile = row["profile"]
                report = raw(resolved(row["raw_path"], paths[key].parent), row["raw_sha256"], case + "/" + profile + " set raw")
                obs = report["sets"][case]
                # All original raw fields must remain exact. Additional normalized
                # or append-only supplement metadata must not replace raw fields.
                require(all(k in row and row[k] == v for k, v in obs.items()), case + "/" + profile + " raw set observation differs")
                require(set(obs["members"]) == members and len(obs["members"]) == len(roles), case + " raw selected set membership differs")
                if case != CONTROL_CASE:
                    require(type(obs["diversity"]) is int and 1 <= obs["diversity"] <= 5, case + " invalid diversity score")
                require(nonempty(obs.get("evidence")), case + " missing raw set evidence")
                pair, score = closest_pair(obs)
                if case == CONTROL_CASE:
                    require("diversity" in obs and obs["diversity"] is None and obs.get("closest_pair") == []
                            and all(obs.get(k) is None for k in ("closest_pair_diversity", "closest_pair_score", "nearest_pair_score")),
                            "Predeclared singleton must retain null diversity/pair score and [] pair")
                    require(row.get("normalized_closest_pair_members") == [] and row.get("normalized_closest_pair_score") is None,
                            "Singleton source normalization differs")
                    pair, score = [], None
                elif score is None:
                    score = row.get("normalized_closest_pair_score")
                    require(bool(ctx["supplement_pins"]), case + "/" + profile + " missing numeric nearest-pair raw score has no pinned append-only supplement")
                    require(row.get("normalized_closest_pair_members", pair) == pair, case + "/" + profile + " supplemented nearest-pair members differ")
                if case != CONTROL_CASE:
                    require(len(pair) == len(set(pair)) == 2 and set(pair) <= members and type(score) is int and 1 <= score <= 5, case + " invalid nearest pair")
                merged_row = copy.deepcopy(row)
                merged_row.update({"profile": source["wave"] + "/" + profile, "source_profile": profile, "review_wave": source["wave"],
                                   "source_review_wave": source["wave"], "normalized_closest_pair_members": pair, "normalized_closest_pair_score": score,
                                   "member_sha256": {x["image_id"]: x["native_sha256"] for x in case_bindings}})
                set_records.append(merged_row)

        require(len(bindings) == (10 if g_transfer_required else 9)
                and len(records) == (30 if g_transfer_required else 27)
                and len(set_records) == (12 if g_transfer_required else 9), "Composite selected/control coverage differs")
        failures, below4, set_below4, disagreements, other_disagreements = [], [], [], [], []
        for row in records:
            mandatory = row["mandatory"]
            if mandatory["pass"] is not True or any(x["equal"] is not True for x in mandatory["transcription"]):
                failures.append({"profile": row["profile"], "image_id": row["image_id"], "role": row["role"], "kind": "mandatory", "record": mandatory})
            for dim, score in row["scores"].items():
                if type(score) is int and score < 4:
                    rec = {"profile": row["profile"], "image_id": row["image_id"], "role": row["role"], "dimension": dim,
                           "score": score, "core": dim in CORE, "evidence": row["evidence"][dim], "review_wave": row["review_wave"]}
                    below4.append(rec)
                    if dim in CORE:
                        failures.append(dict(rec, kind="core"))
        for row in set_records:
            for field, score in (("diversity", row["diversity"]), ("closest_pair", row["normalized_closest_pair_score"])):
                if type(score) is int and score < 4:
                    set_below4.append({"profile": row["profile"], "case_id": row["case_id"], "field": field, "score": score,
                                       "gated": field == "diversity", "members": row["members"], "evidence": row["evidence"]})
            if type(row["diversity"]) is int and row["diversity"] < 4:
                failures.append(dict(row, kind="diversity"))
        for b in bindings:
            observations = [x for x in records if x["role"] == b["role"]]
            for dim in DIMS:
                values = {x["profile"]: x["scores"][dim] for x in observations}
                if len(set(values.values())) > 1:
                    disagreements.append({"image_id": b["image_id"], "role": b["role"], "dimension": dim, "raw_scores": values})
            values = {x["profile"]: x["mandatory"]["pass"] for x in observations}
            if len(set(values.values())) > 1:
                other_disagreements.append({"image_id": b["image_id"], "role": b["role"], "field": "mandatory.pass", "raw_values": values})
        for case in review_cases:
            observations = [x for x in set_records if x["case_id"] == case]
            for field, output_field in (("diversity", "diversity"), ("normalized_closest_pair_members", "closest_pair"), ("normalized_closest_pair_score", "closest_pair_score")):
                values = {x["profile"]: x[field] for x in observations}
                if len({json.dumps(v, sort_keys=True) for v in values.values()}) > 1:
                    target = disagreements if field == "diversity" else other_disagreements
                    target.append({"case_id": case, "dimension" if field == "diversity" else "field": output_field,
                                   "raw_scores" if field == "diversity" else "raw_values": values})
        for label, proc in procedures.items():
            included_ids = {b["image_id"] for b in bindings if label in b["critic_profiles"]}
            proc["selected_view_entries"] = [x for x in proc["recorded_view_entries"] if x["image_id"] in included_ids]
        transfer = None
        if g_transfer_required:
            transfer_bindings = [x for x in bindings if x["role"] == "T01"]
            transfer_records = [x for x in records if x["role"] == "T01"]
            transfer_sets = [x for x in set_records if x["case_id"] == CONTROL_CASE]
            transfer_failures = [x for x in failures if x.get("role") == "T01" or x.get("case_id") == CONTROL_CASE]
            transfer_procedures = {k: copy.deepcopy(v) for k, v in procedures.items() if v["source_review_wave"] == material["wave"]}
            transfer_ids = {x["image_id"] for x in transfer_bindings}
            for proc in transfer_procedures.values():
                proc["included_cases"], proc["included_roles"] = [CONTROL_CASE], ["T01"]
                proc["selected_view_entries"] = [x for x in proc["recorded_view_entries"] if x["image_id"] in transfer_ids]
            transfer = {"scope": "Required G T01 transfer control, separate from selected14. All three complete raw critics and every mandatory/core gate apply; singleton diversity/pair scores do not apply. No failing control may be excluded.",
                        "status": "FAIL" if errors or transfer_failures else "PASS",
                        "recorded_evidence_integrity": "FAIL" if errors else "PASS",
                        "predeclared_transfer_gate": "FAIL" if errors or transfer_failures else "PASS",
                        "source_summary_ref": copy.deepcopy(source_refs["material"]),
                        "source_plan": {"path": str(g_plan_path), "sha256": G_PLAN_SHA256},
                        "source_cases": {"path": str(g_cases_path), "sha256": G_CASES_SHA256},
                        "closed_source_pin_checks": copy.deepcopy(source_pins + material.get("closed_source_pin_checks", [])),
                        "image_bindings": transfer_bindings, "image_critic_records": transfer_records,
                        "all_set_records": transfer_sets, "review_procedure": transfer_procedures,
                        "located_gate_failures": transfer_failures,
                        "all_scores_below4": [x for x in below4 if x.get("role") == "T01"],
                        "other_sub4": [x for x in below4 if x.get("role") == "T01" and not x["core"]],
                        "disagreements": [x for x in disagreements if x.get("role") == "T01" or x.get("case_id") == CONTROL_CASE],
                        "other_recorded_disagreements": [x for x in other_disagreements if x.get("role") == "T01" or x.get("case_id") == CONTROL_CASE]}
            bindings = [x for x in bindings if x["role"] != "T01"]
            records = [x for x in records if x["role"] != "T01"]
            set_records = [x for x in set_records if x["case_id"] != CONTROL_CASE]
            below4 = [x for x in below4 if x.get("role") != "T01"]
            disagreements = [x for x in disagreements if x.get("role") != "T01" and x.get("case_id") != CONTROL_CASE]
            other_disagreements = [x for x in other_disagreements if x.get("role") != "T01" and x.get("case_id") != CONTROL_CASE]
            for label, proc in procedures.items():
                included_ids = {b["image_id"] for b in bindings if label in b["critic_profiles"]}
                proc["selected_view_entries"] = [x for x in proc["recorded_view_entries"] if x["image_id"] in included_ids]
        result = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "wave": "selected-cases-" + sources["garden"]["wave"] + "+" + sources["material"]["wave"],
                  "status": "FAIL" if errors or failures else "PASS", "recorded_evidence_integrity": "FAIL" if errors else "PASS",
                  "predeclared_core_diversity_gate": "FAIL" if errors or failures else "PASS",
                  "scope": "Complete unchanged garden5 from closed correction2 plus complete product2/invitation2 from the closed material wave, including new F P01/H01 and exactly bound retained P02/H02. Each case includes every raw observation from all three critics. Quality gate is recomputed only for these included cases; excluded historical failures remain in exact source summaries and raw archives. Mixed-version evidence, no universal/all-F/authorship/physical/print certification. Recorded path/order/evidence claims are attestations, not proof of actual viewing or visual truth.",
                  "inputs": {"selection": str(selection_path), "selection_sha256": sha(selection_path)}, "source_summary_refs": source_refs,
                  "historical_original_summary_hashes": {key: value["sha256"] for key, value in source_refs.items()},
                  "excluded_historical_case_evidence": excluded, "predeclared_gate_text": gate, "procedural_extension": None,
                  "critics": list(procedures), "quality_gate_critic_scope": "Each selected image/case uses its own complete three composite wave/profile critics",
                  "valid_required_action_first_profiles": [sources["material"]["wave"] + "/" + p for p in contexts["material"]["profiles"]],
                  "selected_image_count": len(bindings), "image_critic_record_count": len(records), "score_observation_count": sum(len(x["scores"]) for x in records),
                  "below4_image_score_count": len(below4), "core_below4_count": sum(x["core"] for x in below4),
                  "noncore_below4_count": sum(not x["core"] for x in below4), "diversity_below4_count": sum(x["kind"] == "diversity" for x in failures),
                  "integrity_errors": errors, "closed_source_pin_checks": source_pins + [copy.deepcopy(x) for s in sources.values() for x in s.get("closed_source_pin_checks", [])],
                  "image_bindings": bindings, "review_procedure": procedures, "image_critic_records": records, "all_scores_below4": below4,
                  "all_set_records": set_records, "all_set_score_observations_below4": set_below4, "disagreements": disagreements,
                  "other_recorded_disagreements": other_disagreements, "located_gate_failures": failures}
        if transfer is not None:
            result["required_transfer_evidence"] = transfer
            result["predeclared_transfer_gate"] = transfer["predeclared_transfer_gate"]
            result["scope"] = "Complete unchanged garden5 plus complete product2/invitation2 from the closed material wave, bound F P01/H01 and G P02/H02. Required G T01 singleton transfer remains separate from selected14 and every mandatory/core failure also fails this composite gate. Every raw observation from all three critics remains, including noncore scores and historical excluded-case failures. Mixed-version selected evidence; no universal/all-G/authorship/physical/print certification. Recorded path/order/evidence claims are attestations, not proof of actual viewing or visual truth."
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"status": result["status"], "recorded_evidence_integrity": result["recorded_evidence_integrity"],
                          "quality_gate": result["predeclared_core_diversity_gate"], "images": len(bindings), "records": len(records),
                          "integrity_errors": errors, "located_gate_failures": len(failures)}, ensure_ascii=False))
        return 1 if result["status"] == "FAIL" else 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({"status": "FAIL", "recorded_evidence_integrity": "FAIL", "input_error": type(exc).__name__ + ": " + str(exc),
                          "integrity_errors_before_input_error": errors}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
