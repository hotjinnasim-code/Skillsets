#!/usr/bin/env python3
"""Join sealed selections and accepted review assignments without rescoring.

Missing/invalid review evidence is retained and reported as NOT_ASSESSABLE.
The current round has twenty returned initials. The generic failed-initial
sealing utility branch is unsupported: no later image is substituted for it.
This validates provenance, not whether a critic actually looked or in what order.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

DIMS = ("content_form", "hierarchy", "typography", "space", "image_material", "emotion_control", "ai_slop")
CORE = ("content_form", "typography", "image_material", "ai_slop")
PROFILES = ("editorial", "craft", "portfolio")


def objects(value):
    return value if isinstance(value, list) else []


def mapping(value):
    return value if isinstance(value, dict) else {}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve(path, root):
    value = Path(path)
    return (value if value.is_absolute() else root / value).resolve()


def load(path, errors, label):
    try:
        value = json.loads(Path(path).read_text())
        if not isinstance(value, dict):
            raise ValueError("expected JSON object")
        return value
    except (OSError, ValueError, TypeError) as exc:
        errors.append(label + ": " + str(exc))
        return {}


def check(ok, errors, message):
    if not ok:
        errors.append(message)


def pin(value, root, errors, label):
    if not isinstance(value, dict) or not isinstance(value.get("path"), str):
        errors.append(label + " missing path/SHA pin")
        return None
    path = resolve(value["path"], root)
    try:
        actual = sha(path)
    except OSError as exc:
        errors.append(label + ": " + str(exc))
        return path
    check(isinstance(value.get("sha256"), str) and actual == value["sha256"], errors, label + " SHA differs")
    return path


def rows_for(document, roles, cid, errors, label):
    rows = document.get("selected", [])
    if not isinstance(rows, list):
        rows = []
    result = {x.get("role"): x for x in rows if isinstance(x, dict)}
    check(len(rows) == len(result) == 5 and set(result) == set(roles), errors, label + " exact five-role coverage differs")
    for role, row in result.items():
        check(row.get("case_id") == cid and role in roles, errors, label + " role/case differs: " + str(role))
    return result


def selection_binding(row, role, cid, root, errors, label):
    """Validate the native/manifest association and return metadata-only fallback."""
    if not row or not row.get("final_native") or not row.get("manifest"):
        errors.append(label + " unsupported failed/missing initial member; no image substitution")
        return None
    stage = row.get("stage")
    canonical = root / "production" / role / str(stage)
    manifest_path = pin({"path": row["manifest"], "sha256": row.get("manifest_sha256")}, root, errors, label + " manifest")
    source = pin({"path": row["final_native"], "sha256": row.get("sha256")}, root, errors, label + " native")
    check(manifest_path == (canonical / "manifest.json").resolve() and source == (canonical / "final.png").resolve(), errors, label + " canonical stage paths differ")
    m = load(manifest_path, errors, label + " manifest content") if manifest_path else {}
    check((m.get("role"), m.get("case_id"), m.get("stage")) == (role, cid, stage), errors, label + " manifest role/case/stage differs")
    check((m.get("width"), m.get("height")) == (row.get("width"), row.get("height")) and all(type(row.get(k)) is int and row[k] > 0 for k in ("width", "height")), errors, label + " dimensions differ")
    for name in ("final", "original", "tool_source"):
        entry = m.get(name, {})
        path = pin(entry, root, errors, label + " " + name)
        check(entry.get("sha256") == row.get("sha256"), errors, label + " " + name + " bytes differ from selected native")
        if name == "final":
            check(path == source, errors, label + " manifest final source differs")
        if name == "original":
            check(path == (canonical / "original.png").resolve(), errors, label + " original canonical path differs")
    views = {"native": {"path": str(source), "sha256": row.get("sha256"), "dimensions": [row.get("width"), row.get("height")]}}
    for name in ("usage720", "thumbnail320"):
        q = m.get("qa_views", {}).get(name, {})
        path = pin(q, root, errors, label + " " + name)
        if path:
            views[name] = {"path": str(path), "sha256": q.get("sha256"), "dimensions": [q.get("width"), q.get("height")]}
    return {"image_id": None, "role": role, "case_id": cid, "stage": stage, "source_native": str(source),
            "source_manifest": str(manifest_path), "source_manifest_sha256": row.get("manifest_sha256"),
            "native_sha256": row.get("sha256"), "views": views}


def binding_equal(binding, row, root):
    try:
        return all(binding.get(k) == row.get(k) for k in ("role", "case_id", "stage")) and (
            resolve(binding["source_native"], root) == resolve(row["final_native"], root)
            and resolve(binding["source_manifest"], root) == resolve(row["manifest"], root)
            and binding["native_sha256"] == row["sha256"]
            and binding["source_manifest_sha256"] == row["manifest_sha256"]
            and binding["views"]["native"]["sha256"] == row["sha256"]
            and binding["views"]["native"]["dimensions"] == [row["width"], row["height"]])
    except (KeyError, TypeError, ValueError):
        return False


def review_stage(summary, wave, expected_pin, rows, roles, cid, root, errors):
    check(summary.get("wave") == wave, errors, cid + " summary wave differs")
    check(summary.get("recorded_evidence_integrity") == "PASS", errors, cid + " summary procedure/integrity is not PASS")
    errors.extend(str(x) for x in objects(summary.get("integrity_errors")))
    declared = [x for x in objects(summary.get("source_pin_checks")) if isinstance(x, dict) and x.get("kind") == "selection"]
    check(len(declared) == 1 and all(resolve(x.get("path", ""), root) == resolve(expected_pin.get("path", ""), root)
          and x.get("expected_sha256") == x.get("actual_sha256") == expected_pin.get("sha256") for x in declared), errors, cid + " summary selection pin differs from closure")
    bindings = summary.get("image_bindings", [])
    bindings = bindings if isinstance(bindings, list) else []
    by_role = {b.get("role"): b for b in bindings if isinstance(b, dict)}
    check(len(bindings) == len(by_role) == 5 and set(by_role) == set(roles), errors, cid + " summary binding five-role coverage differs")
    ids = {b.get("image_id") for b in bindings if isinstance(b, dict)}
    check(None not in ids and len(ids) == 5, errors, cid + " anonymous binding IDs differ")
    for role in roles:
        check(binding_equal(by_role.get(role, {}), rows.get(role, {}), root), errors, cid + " exact selected role/stage/native/manifest binding differs: " + role)
    procedures = summary.get("review_procedure", {})
    procedures = procedures if isinstance(procedures, dict) else {}
    check(set(procedures) == set(PROFILES), errors, cid + " accepted three-profile procedure coverage differs")
    sessions = []
    for profile in PROFILES:
        proc = procedures.get(profile, {})
        check(isinstance(proc, dict) and proc.get("cli_assignment_valid") is True, errors, cid + "/" + profile + " CLI assignment not accepted")
        if not isinstance(proc, dict):
            proc = {}
        session = proc.get("cli_session_id")
        check(isinstance(session, str) and bool(session.strip()), errors, cid + "/" + profile + " accepted CLI session missing")
        if isinstance(session, str) and session.strip():
            sessions.append(session)
        for name in ("cli_completion", "cli_launch", "cli_trace"):
            pin(proc.get(name), root, errors, cid + "/" + profile + " " + name)
        check(proc.get("order_compliant") is True and proc.get("preflight_order_compliant") is True, errors, cid + "/" + profile + " order attestation invalid/missing")
    check(len(sessions) == len(set(sessions)) == 3, errors, cid + " accepted sessions are not distinct")
    records = summary.get("image_critic_records", [])
    records = records if isinstance(records, list) else []
    check(summary.get("selected_image_count") == 5 and summary.get("image_critic_record_count") == len(records) == 15,
          errors, cid + " actual image-critic count differs")
    check(summary.get("score_observation_count") == sum(len(mapping(x.get("scores"))) for x in records if isinstance(x, dict)), errors, cid + " declared score observation count differs")
    pairs = []
    for record in records:
        if not isinstance(record, dict):
            errors.append(cid + " malformed critic record")
            continue
        profile, role = record.get("profile"), record.get("role")
        pairs.append((profile, role))
        binding, proc = by_role.get(role, {}), mapping(procedures.get(profile))
        check(role in roles and profile in PROFILES and record.get("case_id") == cid and record.get("image_id") == binding.get("image_id"), errors, cid + " observation role/profile/image binding differs")
        check(record.get("raw_path") == proc.get("raw_report") and record.get("raw_sha256") == proc.get("raw_report_sha256"), errors, cid + " observation raw report pin differs")
        scores = record.get("scores", {})
        check(isinstance(scores, dict) and set(scores) == set(DIMS) and all(type(scores[d]) is int and 1 <= scores[d] <= 5 for d in DIMS), errors, cid + " seven integer score schema differs")
        check(type(mapping(record.get("mandatory")).get("pass")) is bool, errors, cid + " mandatory Boolean missing")
    check(len(pairs) == len(set(pairs)) == 15 and set(pairs) == {(p, role) for p in PROFILES for role in roles}, errors, cid + " exact three-by-five observation coverage differs")
    sets = summary.get("all_set_records", [])
    sets = sets if isinstance(sets, list) else []
    check(len(sets) == 3 and {x.get("profile") for x in sets if isinstance(x, dict)} == set(PROFILES), errors, cid + " exact three set records missing")
    for record in sets:
        if not isinstance(record, dict):
            errors.append(cid + " malformed set record")
            continue
        check(record.get("case_id") == cid and len(record.get("members", [])) == 5 and set(record.get("members", [])) == ids,
              errors, cid + " set member binding differs")
        check(type(record.get("diversity")) is int and 1 <= record["diversity"] <= 5, errors, cid + " diversity integer missing")
    return by_role, records, sets, sessions


def image_gate(records, failures, binding, valid):
    if not valid:
        return "NOT_ASSESSABLE"
    if any(isinstance(x, dict) and (x.get("role") == binding["role"] or x.get("image_id") == binding["image_id"]) for x in objects(failures)):
        return "FAIL"
    for record in records:
        mandatory = record["mandatory"]
        if mandatory["pass"] is False or mandatory.get("use_readings", {}).get("all_required_copy_legible_at720") is False or any(x.get("equal") is False for x in mandatory.get("transcription", [])):
            return "FAIL"
        if any(record["scores"][d] < 4 for d in CORE):
            return "FAIL"
    return "PASS"


def combine(root):
    root = Path(root).resolve()
    global_errors = []
    plan = load(root / "planning/phase-plan.json", global_errors, "phase plan")
    cases = load(root / "planning/cases.json", global_errors, "cases").get("cases", [])
    closed = load(root / "planning/calls-closed.json", global_errors, "calls closed")
    check(closed.get("status") == "PASS" and closed.get("call_phase") == "CLOSED", global_errors, "native call validation is not closed/PASS")
    registry_path = root / "planning/production-closed-registry.json"
    registry = load(registry_path, global_errors, "production closed registry")
    ordinary = {x.get("role"): x for x in registry.get("roles", [])}
    startup_errors = list(global_errors)
    images, sets, refs, closure_refs = {}, {}, {}, {}
    first_records, final_records, session_waves = [], [], {}
    for case in cases:
        cid, roles = case["id"], [x["id"] for x in case["slots"]]
        case_errors = list(startup_errors)
        check(len(roles) == len(set(roles)) == 5, case_errors, cid + " expected five roles differ")
        closure_path = root / "planning" / (cid + "-ordinary-closed.json")
        closure = load(closure_path, case_errors, cid + " closure")
        closure_refs[cid] = {"path": str(closure_path), "sha256": sha(closure_path) if closure_path.is_file() else None}
        check(closure.get("case_id") == cid and closure.get("external_critics_not_yet_dispatched") is True, case_errors, cid + " closure identity/pre-review close differs")
        selections, fallback = {}, {}
        for stage in ("first", "final"):
            path = pin(closure.get(stage + "_selection"), root, case_errors, cid + " " + stage + " closure selection")
            document = load(path, case_errors, cid + " " + stage + " selection") if path else {}
            selections[stage] = rows_for(document, roles, cid, case_errors, cid + " " + stage)
            fallback[stage] = {role: selection_binding(selections[stage].get(role), role, cid, root, case_errors, cid + "/" + stage + "/" + role) for role in roles}
        for role in roles:
            record = ordinary.get(role, {})
            path = pin({"path": record.get("selection"), "sha256": record.get("sha256")}, root, case_errors, role + " closed ordinary selection")
            selection = load(path, case_errors, role + " ordinary selection") if path else {}
            row = selections["final"].get(role, {})
            # Retain raw maker field aliases; accept only the same canonical
            # selected-stage path and reject conflicting simultaneous fields.
            ordinary_manifest = selection.get("manifest", selection.get("manifest_path"))
            check(not ("manifest" in selection and "manifest_path" in selection)
                  or selection["manifest"] == selection["manifest_path"],
                  case_errors, role + " conflicting ordinary manifest aliases")
            check(selection.get("role") == role and selection.get("case_id") == cid and selection.get("selected_stage") == row.get("stage")
                  and selection.get("selected_native") == row.get("final_native") and selection.get("sha256") == row.get("sha256")
                  and ordinary_manifest == row.get("manifest") and (selection.get("width"), selection.get("height")) == (row.get("width"), row.get("height")),
                  case_errors, role + " final row differs from closed ordinary selection")
        dictionaries = {stage: {role: row.get("sha256") for role, row in rows.items()} for stage, rows in selections.items()}
        complete = all(set(dictionaries[s]) == set(roles) and all(isinstance(v, str) for v in dictionaries[s].values()) for s in ("first", "final"))
        changed = dictionaries["first"] != dictionaries["final"] if complete else None
        check(complete and type(closure.get("physical_set_changed")) is bool and closure["physical_set_changed"] == changed,
              case_errors, cid + " whole role-to-SHA change decision differs/is incomplete")
        waves = closure.get("review_waves", {})
        check(isinstance(waves.get("first"), str) and isinstance(waves.get("final"), str) and ((waves.get("first") != waves.get("final")) if changed else (waves.get("first") == waves.get("final"))),
              case_errors, cid + " changed/reuse review wave decision differs")
        stage_data = {}
        for stage in ("first", "final"):
            errors = list(case_errors)
            wave = waves.get(stage)
            path = root / "planning" / ("summary-" + str(wave) + ".json")
            summary = load(path, errors, cid + "/" + stage + " summary")
            expected_pin = closure.get(("first" if stage == "final" and changed is False else stage) + "_selection", {})
            bindings, records, set_records, sessions = review_stage(summary, wave, expected_pin, selections[stage], roles, cid, root, errors)
            for session in sessions:
                previous = session_waves.setdefault(session, wave)
                check(previous == wave, errors, cid + " accepted CLI session reused for a different review wave: " + session)
            refs[cid + "/" + stage] = {"path": str(path), "sha256": sha(path) if path.is_file() else None, "wave": wave,
                "reuse_complete_initial_three": stage == "final" and changed is False, "available": bool(summary),
                "accepted": not errors, "accepted_session_ids": sessions if not errors else [], "input_error": summary.get("input_error")}
            stage_data[stage] = {"summary": summary, "errors": errors, "bindings": bindings, "records": records, "sets": set_records, "sessions": sessions}
        if changed:
            check(len(stage_data["first"]["sessions"]) == len(stage_data["final"]["sessions"]) == 3
                  and set(stage_data["first"]["sessions"]).isdisjoint(stage_data["final"]["sessions"]), stage_data["final"]["errors"], cid + " changed final does not have three fresh distinct accepted sessions")
        else:
            check(refs[cid + "/first"]["path"] == refs[cid + "/final"]["path"] and refs[cid + "/first"]["sha256"] == refs[cid + "/final"]["sha256"]
                  and stage_data["first"]["sessions"] == stage_data["final"]["sessions"], stage_data["final"]["errors"], cid + " unchanged set did not reuse exact complete initial three")
        first_records.extend(stage_data["first"]["records"])
        final_records.extend(stage_data["final"]["records"])
        case_gates = {}
        for role in roles:
            member = {"case_id": cid, "selected": selections["final"].get(role), "initial_selection": selections["first"].get(role),
                "ordinary_selection": {"path": ordinary.get(role, {}).get("selection"), "sha256": ordinary.get(role, {}).get("sha256")}}
            for stage, prefix in (("first", "initial_"), ("final", "")):
                data = stage_data[stage]
                reviewed = data["bindings"].get(role)
                binding = reviewed if binding_equal(reviewed or {}, selections[stage].get(role, {}), root) else fallback[stage][role]
                obs = [x for x in data["records"] if isinstance(x, dict) and x.get("role") == role]
                failures = objects(data["summary"].get("located_gate_failures"))
                located = [x for x in failures if isinstance(x, dict) and (x.get("role") == role or (binding and binding.get("image_id") is not None and x.get("image_id") == binding["image_id"]))]
                valid = not data["errors"]
                member[prefix + "binding"] = binding
                member[prefix + "binding_provenance"] = "summary_joined" if binding is reviewed else "sealed_selection_metadata_only"
                member[prefix + "binding_assessable"] = valid
                member[prefix + "reviewers"] = obs
                member[("initial" if stage == "first" else "final") + "_image_gate"] = image_gate(obs, failures, binding, valid)
                member[("first" if stage == "first" else "final") + "_located_failures"] = located
            images[role] = member
        for stage in ("first", "final"):
            data = stage_data[stage]
            gate = "NOT_ASSESSABLE" if data["errors"] else ("PASS" if all(images[role][("initial" if stage == "first" else "final") + "_image_gate"] == "PASS" for role in roles)
                and all(record["diversity"] >= 4 for record in data["sets"]) and not data["summary"].get("located_gate_failures") else "FAIL")
            if not data["errors"] and data["summary"].get("predeclared_core_diversity_gate") != gate:
                data["errors"].append(cid + "/" + stage + " summary gate contradicts unchanged raw-record gate")
                gate = "NOT_ASSESSABLE"
                for role in roles:
                    images[role][("initial" if stage == "first" else "final") + "_image_gate"] = "NOT_ASSESSABLE"
                    images[role][("initial_" if stage == "first" else "") + "binding_assessable"] = False
            case_gates[stage] = gate
            refs[cid + "/" + stage]["accepted"] = not data["errors"]
            refs[cid + "/" + stage]["accepted_session_ids"] = data["sessions"] if not data["errors"] else []
            global_errors.extend(data["errors"])
        sets[cid] = {"name": case["name"], "roles": roles, "physical_set_changed": changed, "initial_case_gate": case_gates["first"], "final_case_gate": case_gates["final"],
            "initial_reviewers": stage_data["first"]["sets"], "final_reviewers": stage_data["final"]["sets"],
            "initial_failures": stage_data["first"]["summary"].get("located_gate_failures", []), "final_failures": stage_data["final"]["summary"].get("located_gate_failures", []),
            "initial_disagreements": stage_data["first"]["summary"].get("disagreements", []), "final_disagreements": stage_data["final"]["summary"].get("disagreements", []),
            "initial_all_scores_below4": stage_data["first"]["summary"].get("all_scores_below4", []), "final_all_scores_below4": stage_data["final"]["summary"].get("all_scores_below4", []),
            "review_procedure": {s: stage_data[s]["summary"].get("review_procedure", {}) for s in ("first", "final")},
            "review_integrity_errors": {s: stage_data[s]["errors"] for s in ("first", "final")}}
    errors = list(dict.fromkeys(global_errors))
    final_gates = [s["final_case_gate"] for s in sets.values()]
    overall = "NOT_ASSESSABLE" if errors or "NOT_ASSESSABLE" in final_gates else ("PASS" if final_gates and all(g == "PASS" for g in final_gates) else "FAIL")
    return {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "source_commit": plan.get("source_commit"),
        "recorded_evidence_integrity": "FAIL" if errors else "PASS", "predeclared_core_diversity_gate": overall,
        "scope": "All declared complete five-role cases retained, without averages or subset choice. Closure selection pins and exact role/stage/native/manifest/source associations joined. Whole role-to-SHA change recomputed; changed waves require disjoint accepted CLI sessions, unchanged sets reuse exactly the initial three. Missing/invalid procedure yields NOT_ASSESSABLE, never image PASS. Available failures, scores and disagreements remain recorded. Hashes establish provenance, not actual viewing/order, authorship, physical function, printing or future quality.",
        "images": images, "sets": sets, "summary_refs": refs, "closure_refs": closure_refs,
        "selected_image_count": sum(bool(x.get("selected", {}).get("final_native")) for x in images.values() if isinstance(x.get("selected"), dict)),
        "initial_returned_image_count": sum(bool(x.get("initial_selection", {}).get("final_native")) for x in images.values() if isinstance(x.get("initial_selection"), dict)),
        "expected_image_count": sum(len(c.get("slots", [])) for c in cases),
        "firstpass_image_pass_count": sum(x["initial_image_gate"] == "PASS" for x in images.values()), "final_image_pass_count": sum(x["final_image_gate"] == "PASS" for x in images.values()),
        "initial_image_gate_counts": {gate: sum(x["initial_image_gate"] == gate for x in images.values()) for gate in ("PASS", "FAIL", "NOT_ASSESSABLE")},
        "final_image_gate_counts": {gate: sum(x["final_image_gate"] == gate for x in images.values()) for gate in ("PASS", "FAIL", "NOT_ASSESSABLE")},
        "firstpass_image_critic_records": len(first_records), "final_image_critic_records": len(final_records),
        "firstpass_score_observations": sum(len(mapping(x.get("scores"))) for x in first_records if isinstance(x, dict)),
        "final_score_observations": sum(len(mapping(x.get("scores"))) for x in final_records if isinstance(x, dict)),
        "integrity_errors": errors, "call_validation": {"path": str(root / "planning/calls-closed.json"), "sha256": sha(root / "planning/calls-closed.json") if (root / "planning/calls-closed.json").is_file() else None},
        "production_registry": {"path": str(registry_path), "sha256": sha(registry_path) if registry_path.is_file() else None},
        "unsupported_utility_branches": ["Generic failed-initial sealing is unsupported; absent initial images remain NOT_ASSESSABLE and are never replaced by final images."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = combine(args.root)
    output = args.output or args.root / "planning/final-evidence.json"
    with output.resolve().open("x") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({k: result[k] for k in ("recorded_evidence_integrity", "predeclared_core_diversity_gate", "firstpass_image_pass_count", "final_image_pass_count", "firstpass_image_critic_records", "final_image_critic_records")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
