#!/usr/bin/env python3
"""Write pinned full-request critic packets/jobs; never launch or score a review.

Use a corpus {cases:[...]} or one literal case object. Every maker in this supplied
scope must be terminal before any job is emitted. Use a fresh output phase path;
readiness, packets, prompts and reuse mappings are exclusive immutable evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import evidence_io as evidence
import summarize as summary_helper

ROOT = Path(__file__).resolve().parent
PROFILES = ("editorial", "craft", "portfolio")
VIEWS = ("native", "usage720", "thumbnail320")


def read(path):
    value = json.loads(Path(path).read_bytes())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def value_sha(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def resolve(path, base):
    p = Path(path)
    return (p if p.is_absolute() else base / p).resolve(strict=True)


def pinned(value, base):
    p = resolve(value["path"], base)
    actual = evidence.pin(p)
    if actual["sha256"] != value.get("sha256"):
        raise ValueError(f"Changed pinned bytes: {p}")
    return actual


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    evidence.exclusive_json(path, value)


def ratio(value):
    pair = [int(x) for x in value.split(":")] if isinstance(value, str) and re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", value) else value
    if not isinstance(pair, list) or len(pair) != 2 or any(type(x) is not int or x <= 0 for x in pair):
        raise ValueError(f"Invalid literal requested aspect ratio: {value!r}")
    return pair


def roles(case):
    n = case.get("count")
    if type(n) is not int or n <= 0:
        raise ValueError("Case count must be the positive actual user-requested count")
    result = case.get("roles")
    if result is None:
        ratios = case.get("ratios")
        if not isinstance(ratios, list) or len(ratios) != n:
            raise ValueError("Standalone case needs one explicit ratio per requested role")
        result = [{"role_id": f"{case['case_id']}-M{i+1}", "ordinal": i+1, "ratio": ratios[i], "assets": []} for i in range(n)]
    if not isinstance(result, list) or len(result) != n:
        raise ValueError("Exactly the requested number of roles must be declared")
    result = sorted(result, key=lambda x: x.get("ordinal", 0))
    if [r.get("ordinal") for r in result] != list(range(1, n+1)) or len({r.get("role_id") for r in result}) != n:
        raise ValueError("Roles need distinct IDs and consecutive literal ordinals")
    for role in result:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", str(role.get("role_id", ""))):
            raise ValueError("Unsafe role ID")
        ratio(role.get("ratio"))
        if not isinstance(role.get("assets", []), list):
            raise ValueError("Role assets must be an array")
    return result


def terminal(production, role, case_id):
    role_id = role["role_id"]
    folder = production / role_id
    result = {"role": role_id, "closed": False, "outcome": "open", "errors": [], "stages": []}
    try:
        choices = [p for p in (folder / "selection.json", folder / "unavailable.json") if p.is_file()]
        if len(choices) != 1:
            raise ValueError("Exactly one selection.json or unavailable.json terminal is required")
        terminal_path = choices[0]
        data = read(terminal_path)
        if data.get("role") != role_id:
            raise ValueError("Terminal role identity mismatch")
        if "case_id" in data and data["case_id"] != case_id:
            raise ValueError("Terminal case identity mismatch")
        stages = evidence.stage_inventory(folder)
        if not stages:
            raise ValueError("Terminal role has no actual native attempt")
        returned = failed = 0
        for stage in stages:
            stage_dir = folder / "stages" / stage
            inputs = evidence.input_pins(stage_dir, role_id, stage)
            mp, fp = stage_dir / "manifest.json", stage_dir / "failure.json"
            if mp.is_file() == fp.is_file():
                raise ValueError(f"{stage}: exactly one returned/failure outcome required")
            row = {"stage": stage, "input_pins": inputs}
            if mp.is_file():
                m = read(mp)
                if m.get("kind") != "native_evidence" or m.get("role") != role_id or m.get("stage") != stage or m.get("outcome") != "returned" or type(m.get("native_call_count")) is not int or m.get("native_call_count") != 1 or m.get("native_byte_preserved") is not True:
                    raise ValueError(f"{stage}: native manifest identity/outcome mismatch")
                if m.get("input_pins") != inputs:
                    raise ValueError(f"{stage}: input pins changed since preservation")
                for key in ("original", "final", "usage720", "thumbnail320"):
                    item = m.get("files", {}).get(key)
                    if item != evidence.image_pin(item["path"]):
                        raise ValueError(f"{stage}: changed {key} artifact/dimensions")
                source = pinned(m["source"], mp.parent)
                if source["sha256"] != m["files"]["original"]["sha256"] or source["sha256"] != m["files"]["final"]["sha256"]:
                    raise ValueError(f"{stage}: native source/original/final bytes differ")
                row.update(outcome="returned", manifest=evidence.pin(mp), files=m["files"], source=m["source"])
                returned += 1
            else:
                f = read(fp)
                if f.get("role") != role_id or f.get("stage") != stage or f.get("outcome") != "failure" or type(f.get("native_call_count")) is not int or f["native_call_count"] != 1 or not isinstance(f.get("error"), str) or not f["error"]:
                    raise ValueError(f"{stage}: recorded failure identity/count required")
                if any((stage_dir / n).exists() for n in evidence.FILES):
                    raise ValueError(f"{stage}: failure may not conceal returned artifacts")
                row.update(outcome="failure", failure=evidence.pin(fp))
                failed += 1
            result["stages"].append(row)
        counts = {"native_calls": len(stages), "returned": returned, "failed": failed, "repair_calls": len(stages)-1}
        if data.get("counts") != counts or any(type(x) is not int for x in data.get("counts", {}).values()):
            raise ValueError("Terminal actual attempt counts do not join the complete stage inventory")
        if terminal_path.name == "selection.json":
            if data.get("kind") != "role_selection":
                raise ValueError("Invalid selection kind")
            selected = next((r for r in result["stages"] if r["stage"] == data.get("selected_stage")), None)
            if not selected or selected["outcome"] != "returned" or data.get("selected_manifest") != selected["manifest"] or data.get("selected_native_sha256") != selected["source"]["sha256"] or data.get("selected_files") != selected["files"]:
                raise ValueError("Selected binding differs from actual native manifest")
            sealed = data.get("stages")
            if not isinstance(sealed, list) or len(sealed) != len(stages):
                raise ValueError("Selection dropped an unselected/failure stage")
            for actual, saved in zip(result["stages"], sealed):
                if saved.get("stage") != actual["stage"] or saved.get("outcome") != actual["outcome"] or saved.get("input_pins") != actual["input_pins"]:
                    raise ValueError("Selection stage identity/input inventory mismatch")
                if actual["outcome"] == "returned":
                    if saved.get("manifest") != actual["manifest"]:
                        raise ValueError("Selection stage manifest mismatch")
                    # Byte-check inspection/comparison pins without reading creator claims.
                    pinned(saved["inspection"], folder)
                    if actual["stage"] != "initial":
                        pinned(saved["parent_comparison"], folder)
                elif saved.get("failure") != actual["failure"]:
                    raise ValueError("Selection failure inventory mismatch")
            result["selected_stage"] = selected["stage"]
            result["outcome"] = "selection"
        else:
            if data.get("kind") != "role_unavailable" or data.get("case_id") != case_id or data.get("closed") is not True or data.get("outcome") != "unavailable" or stages != list(evidence.STAGES) or returned != 0 or failed != 3:
                raise ValueError("unavailable.json is valid only after all three actual attempts failed")
            sealed = data.get("stages")
            if not isinstance(sealed, list) or len(sealed) != 3:
                raise ValueError("Unavailable terminal must preserve all three failures")
            for actual, saved in zip(result["stages"], sealed):
                if any(saved.get(key) != actual[key] for key in ("stage", "outcome")) or pinned(saved["failure"], folder) != actual["failure"]:
                    raise ValueError("Unavailable terminal failure/input inventory mismatch")
                for key in ("call_input", "pre_call"):
                    if pinned(saved["input_pins"][key], folder) != actual["input_pins"][key]:
                        raise ValueError("Unavailable terminal input pin changed")
            result["outcome"] = "unavailable"
        result.update(closed=True, terminal=evidence.pin(terminal_path), counts=counts)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        result["errors"].append(str(exc))
    return result


def client_style(case):
    if not isinstance(case.get("request"), str) or not case["request"]:
        raise ValueError("Literal complete client request is required")
    conditions = case.get("conditions", [])
    styles = case.get("styles", [])
    if not isinstance(conditions, list) or any(not isinstance(c, str) for c in conditions):
        raise ValueError("Literal case conditions must be a string array")
    if not isinstance(styles, (list, str)):
        raise ValueError("Literal client styles must be an array or string")
    return case["request"] + "\n\nLiteral client styles:\n" + (styles if isinstance(styles, str) else json.dumps(styles, ensure_ascii=False)) + "\n\nLiteral mandatory client conditions:\n" + "\n".join(conditions)


def assets(case_roles, corpus_base):
    unique, pins, layouts = {}, [], []
    for role in case_roles:
        for asset in role.get("assets", []):
            if not isinstance(asset, dict) or asset.get("ready") is not True:
                raise ValueError("Every requested source asset must be explicitly ready")
            native = pinned({"path": asset["actual_path"], "sha256": asset["sha256"]}, corpus_base)
            manifest = pinned({"path": asset["manifest_path"], "sha256": asset["manifest_sha256"]}, corpus_base)
            key = asset.get("asset_id")
            item = dict(asset, actual_path=native["path"], manifest_path=manifest["path"])
            if key in unique and unique[key] != item:
                raise ValueError("Conflicting source asset identity")
            if key not in unique:
                unique[key] = item
                pins.extend((native, manifest))
                if "measured_layout" in asset:
                    layouts.append({"asset_id": key, "measured_layout": asset["measured_layout"], "manifest": manifest})
    return list(unique.values()), pins, layouts


def context(packet):
    # Strict reuse: stage, source-manifest and exact view paths must also match.
    # A byte-identical repair with new provenance conservatively gets fresh critics.
    return {k: packet[k] for k in ("case_id", "candidate_label", "expected_count", "full_request", "literal_case_sha256", "normalization", "requirements", "copy", "review_rules", "critic_rubric", "ratio_policy", "helper_pins", "source_assets", "protected_layouts", "images")}


def complete_reuse(initial_dir, packet):
    pp, sp = initial_dir / "packet.json", initial_dir / "summary.json"
    if not pp.is_file():
        return None, "initial packet not present"
    first = read(pp)
    if context(first) != context(packet):
        return None, "full evaluation context differs"
    if not sp.is_file():
        return None, "identical full context awaits complete first three raw reviews/summary"
    data = read(sp)
    n = packet["expected_count"]
    if data.get("procedure_gate") != "PASS" or data.get("procedure_errors") or data.get("raw_packet") != first or data.get("counts", {}).get("observed_image_profile_records") != 3*n or data["counts"].get("valid_integer_1_to_5_score_values") != 21*n:
        raise ValueError("Initial summary is not a complete valid-procedure three-critic record")
    pinned(data["packet"], sp.parent)
    if resolve(data["packet"]["path"], sp.parent) != pp.resolve():
        raise ValueError("Initial summary points at another packet")
    reviews = data.get("reviews", {})
    if set(reviews) != set(PROFILES):
        raise ValueError("Initial summary does not contain exactly the fixed three critics")
    sessions, retained = [], {}
    for profile in PROFILES:
        review = reviews[profile]
        if review.get("procedure_errors") or review.get("set", {}).get("errors") or any(r.get("errors") for r in review.get("images", {}).values()) or set(review.get("images", {})) != {i["image_id"] for i in packet["images"]}:
            raise ValueError("Initial critic incomplete/invalid; never replace or drop it for reuse")
        raw_pin = pinned(review["raw_report"], sp.parent)
        prov = review["provenance"]
        lp = pinned(prov["launch_pin"], sp.parent)
        cp = pinned(prov["completion_pin"], sp.parent)
        tp = pinned(prov["trace_pin"], sp.parent)
        completion = read(cp["path"])
        events = [json.loads(line) for line in Path(tp["path"]).read_text().splitlines() if line.strip()]
        starts = [e.get("thread_id") for e in events if e.get("type") == "thread.started"]
        session = prov.get("derived_session_id")
        if starts != [session] or not isinstance(session, str) or completion.get("session_ids") != starts or completion.get("exit_code") != 0 or completion.get("input_pins_unchanged") is not True or not summary_helper.fresh_exec_argv(completion.get("argv")):
            raise ValueError("Initial exact trace/completion session provenance failed")
        if completion.get("reports", {}).get(profile+".json", {}).get("sha256") != raw_pin["sha256"]:
            raise ValueError("Initial completion/report join changed")
        for item in completion.get("input_pins", []):
            pinned(item, Path(cp["path"]).parent)
        pinned(completion["reports"][profile+".md"], Path(cp["path"]).parent)
        sessions.append(session)
        retained[profile] = {"raw_report": raw_pin, "launch": lp, "completion": cp, "trace": tp, "actual_session_id": session}
    if len(set(sessions)) != 3:
        raise ValueError("Initial complete critics are not three unique sessions")
    return {"kind": "complete_whole_case_reuse", "initial_packet": evidence.pin(pp), "initial_summary": evidence.pin(sp), "retained_critics": retained, "mapping": [{"image_id": i["image_id"], "role": i["role"], "initial_stage": i["stage"], "selected_stage": i["stage"], "native_sha256": i["views"]["native"]["sha256"]} for i in packet["images"]], "low_or_na_gates_retained": True, "context_sha256": value_sha(context(packet))}, None


def prompt(packet_path, case_path, profile, packet, input_pins, output_dir):
    n = packet["expected_count"]
    return f"""You are one fresh independent R7 {profile} critic. This is a real bounded visual assessment of the exact supplied request, not production or a report template.
Read only these explicitly pinned inputs; do not follow other paths embedded inside manifests:
{json.dumps(input_pins, ensure_ascii=False, indent=2)}

Literal complete client request:
{packet['full_request']}

Read {packet_path} and {case_path}; obey the exact pinned review_rules.md schema and critic_rubric.md. Assess only client-specified style/conditions. No coordinator intent, maker interpretation or prior score is supplied. Per-image style_requirement is literal and must be copied exactly into mandatory.style.checked_requirement. Each image.ratio_requirement is its own requested aspect ratio; use the explicitly declared R7 integer-rounding policy and report actual native dimensions truthfully.

Actually view every supplied source asset and read any protected-layout measurement manifest before fidelity judgments. Record truthful procedure.source_assets_viewed entries with asset_id/path/sha256/viewed, and procedure.protected_layouts_read pins when applicable. Then actually view all {n} poster members in packet order, each native/usage720/thumbnail320: all {3*n} exact poster views BEFORE the first transcription judgment, any image score or set-diversity score. Attest truthfully to the method and order; no invented opens, tool serialization or thread ID. Do not use author intent to infer an invisible scene.

Score ALL seven dimensions independently using the rubric's 1–5 anchors and nonempty located evidence arrays. Do not fill a target score, average away a weak dimension or omit low records. Preserve first raw observed copy, the predeclared normalized comparison, layout observations and ambiguity separately. URLs are separate protected entries. A genuine ambiguity permits one exact pinned revisit with both reads kept; unresolved ambiguity -> NA. Do not manufacture omitted glyphs from optical spaces or soft line wrapping.

Required image mandatory keys are exactly text/style/ratio/no_type_only/substantive_visual. Style status must roll up every literal applicable client condition; optional conditions[] outside mandatory can explain details but cannot replace that gate. Substantive nonglyph content is required: lettering alone, whitespace, a tiny ornament or backdrop texture does not meet it. Requested style fidelity is mandatory; do not impose a fixed style or anti-3D rule.

Write actual raw reports only to {output_dir/(profile+'.json')} and {output_dir/(profile+'.md')}. The JSON profile is {profile!r}, case_id={packet['case_id']!r}, wave={packet['wave']!r}, session_id=null. Include every requested image's exact image_id/role/stage/case_id/profile and all seven located evidence arrays. procedure uses fresh_session/all_views_before_scoring/order_compliant booleans, viewed_count={3*n}, and a truthful method. viewed must list every exact ordered packet view with its pinned path/hash. Include full exact count-fidelity and set membership. For N>=2 give diversity 1–5 with evidence for every member; for N=1 use diversity:null and not_applicable_reason:'single requested image'. If actual viewing is impossible, record false procedure/NA and unjudgable scores null with reasons; never fabricate successful viewing or scores.

Do not generate/edit images, access credentials, spawn, fork, resume, inspect peer reviews, R6/other rounds, plans, maker self-inspections or unpinned files. Do not write launch/completion/trace or any file beyond your two reports; the runner owns provenance. No raw report exists yet and no PASS/score placeholder may be treated as an observation.
"""


def prepare(args):
    corpus_path = Path(args.corpus).resolve(strict=True)
    corpus = read(corpus_path)
    cases = corpus.get("cases", [corpus])
    if not isinstance(cases, list) or not cases:
        raise ValueError("Nonempty cases array or one literal case required")
    production = Path(args.production).resolve(strict=True)
    out = Path(args.out).resolve()
    readiness_path = out / (args.wave+"-stage-readiness.json")
    if readiness_path.exists():
        raise ValueError("Readiness already exists; use a fresh output scope")
    planned, inventories = [], {}
    for case in cases:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", str(case.get("case_id", ""))):
            raise ValueError("Safe literal case_id required")
        for role in roles(case):
            if role["role_id"] in inventories:
                raise ValueError("A requested role is duplicated across the corpus")
            planned.append(role["role_id"])
            inventories[role["role_id"]] = terminal(production, role, case["case_id"])
    barrier = all(r["closed"] for r in inventories.values())
    readiness = {"schema_version": 1, "kind": "critic_preparation_readiness", "wave": args.wave, "corpus": evidence.pin(corpus_path), "candidate_label": args.candidate_label, "planned_roles": planned, "planned_role_count": len(planned), "closed_role_count": sum(r["closed"] for r in inventories.values()), "all_makers_closed": barrier, "maker_inventory": inventories, "cases": {}, "jobs": [], "launched": False}
    helpers = {name: evidence.pin(ROOT/name) for name in ("evidence_io.py", "summarize.py", "run_agent.py", "prepare_reviews.py")}
    rules_pin, rubric_pin = evidence.pin(ROOT/"review_rules.md"), evidence.pin(ROOT/"critic_rubric.md")
    ratio_policy = evidence.pin(ROOT/"planning/ratio-policy-before-generation.json")
    for case in cases:
        cid, cr = case["case_id"], roles(case)
        phase_dir = out / cid / args.wave
        if phase_dir.exists():
            raise ValueError(f"Refusing phase overwrite: {phase_dir}")
        state = {"status": "UNREADY", "expected_count": case["count"], "roles": [r["role_id"] for r in cr], "images": [], "errors": [], "jobs": [], "first_outcomes": []}
        for role in cr:
            inventory = inventories[role["role_id"]]
            first = next((s for s in inventory["stages"] if s["stage"] == "initial"), None)
            state["first_outcomes"].append({"role": role["role_id"], "outcome": first["outcome"] if first else "missing", "manifest": first.get("manifest") if first else None, "failure": first.get("failure") if first else None})
            stage = "initial" if args.wave == "initial" else inventory.get("selected_stage")
            row = next((s for s in inventory["stages"] if s["stage"] == stage), None)
            entry = {"image_id": role["role_id"], "role": role["role_id"], "stage": stage, "ready": bool(inventory["closed"] and row and row["outcome"] == "returned")}
            if entry["ready"]:
                entry.update(source_manifest=row["manifest"], views={v: row["files"]["original" if v == "native" else v] for v in VIEWS}, ratio_requirement=ratio(role["ratio"]))
            else:
                state["errors"].append(f"{role['role_id']}: requested {args.wave} outcome unavailable; member retained")
                entry["failure"] = row.get("failure") if row else None
            state["images"].append(entry)
        if not barrier:
            state["errors"].append("No critic starts before every maker in this supplied scope is terminal")
        try:
            source_assets, asset_pins, layouts = assets(cr, corpus_path.parent)
            style = client_style(case)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            state["errors"].append(f"Client/asset readiness: {exc}")
            source_assets, asset_pins, layouts, style = [], [], [], ""
        if state["errors"]:
            write(phase_dir / "readiness.json", state)
            readiness["cases"][cid] = state
            continue
        case_path = phase_dir / "case.json"
        # A single literal client case only; no corpus/source/evaluation-plan labels.
        client_case = {k: case[k] for k in ("case_id", "request", "copy", "count", "ratios", "styles", "conditions") if k in case}
        write(case_path, client_case)
        images = [{k: v for k, v in i.items() if k != "ready"} for i in state["images"]]
        for image in images:
            image["style_requirement"] = style
        requirements = {"style": style, "ratio": images[0]["ratio_requirement"], "ratio_rounding": "nearest-integer-single-edge", "no_type_only": True}
        if "pixel_dimensions" in case:
            requirements.update(pixel_dimensions=case["pixel_dimensions"], ratio_rounding="exact")
        packet = {"schema_version": 1, "case_id": cid, "candidate_label": args.candidate_label or case.get("candidate"), "wave": args.wave, "expected_count": case["count"], "critic_profiles": list(PROFILES), "full_request": case["request"], "literal_case_sha256": value_sha(client_case), "normalization": summary_helper.NORMALIZATION, "copy": case["copy"], "requirements": requirements, "review_rules": rules_pin, "critic_rubric": rubric_pin, "ratio_policy": ratio_policy, "helper_pins": helpers, "source_assets": source_assets, "protected_layouts": layouts, "images": images}
        packet_path = phase_dir / "packet.json"
        write(packet_path, packet)
        errors, _, _ = summary_helper.validate_packet(packet, packet_path.resolve())
        if errors:
            state["errors"].extend(errors)
            write(phase_dir / "readiness.json", state)
            readiness["cases"][cid] = state
            continue
        state.update(status="READY", packet=evidence.pin(packet_path), context_sha256=value_sha(context(packet)))
        if args.wave == "selected":
            initial_root = Path(args.initial_root).resolve() if args.initial_root else out
            initial_dir = initial_root / cid / "initial"
            try:
                reuse, reason = complete_reuse(initial_dir, packet)
                if reuse:
                    write(phase_dir / "reuse.json", reuse)
                    state.update(mode="COMPLETE_FIRST_THREE_REUSED", reuse=evidence.pin(phase_dir/"reuse.json"))
                elif reason == "identical full context awaits complete first three raw reviews/summary":
                    state.update(status="UNREADY", mode="AWAITING_COMPLETE_FIRST_REVIEW")
                    state["errors"].append(reason)
                else:
                    state.update(mode="THREE_FRESH_COMPLETE_CRITICS", reuse_reason=reason)
            except (ValueError, OSError, KeyError, TypeError) as exc:
                state.update(status="UNREADY", mode="INVALID_INITIAL_REUSE_EVIDENCE")
                state["errors"].append(str(exc))
        else:
            state["mode"] = "THREE_FRESH_COMPLETE_CRITICS"
        if state["status"] == "READY" and state["mode"] == "THREE_FRESH_COMPLETE_CRITICS":
            input_paths = [packet_path, case_path, ROOT/"review_rules.md", ROOT/"critic_rubric.md", ROOT/"summarize.py", ROOT/"run_agent.py", Path(ratio_policy["path"])] + [Path(p["path"]) for p in asset_pins]
            for image in images:
                input_paths.append(Path(image["source_manifest"]["path"]))
                input_paths.extend(Path(image["views"][v]["path"]) for v in VIEWS)
            input_paths = list(dict.fromkeys(p.resolve(strict=True) for p in input_paths))
            input_pins = [evidence.pin(p) for p in input_paths]
            for profile in PROFILES:
                output_dir = phase_dir / "cli" / profile
                prompt_path = phase_dir / "prompts" / (profile+".txt")
                prompt_path.parent.mkdir(parents=True, exist_ok=True)
                with prompt_path.open("x", encoding="utf-8") as handle:
                    handle.write(prompt(packet_path.resolve(), case_path.resolve(), profile, packet, input_pins, output_dir.resolve()))
                job = {"case_id": cid, "wave": args.wave, "profile": profile, "prompt_file": str(prompt_path.resolve()), "output_dir": str(output_dir.resolve()), "inputs": [str(p) for p in input_paths], "expected_outputs": [profile+".json", profile+".md"]}
                job_path = phase_dir / "jobs" / (profile+".json")
                write(job_path, job)
                state["jobs"].append(evidence.pin(job_path))
                readiness["jobs"].append(evidence.pin(job_path))
        write(phase_dir / "readiness.json", state)
        readiness["cases"][cid] = state
    readiness["ready_case_count"] = sum(c["status"] == "READY" for c in readiness["cases"].values())
    readiness["planned_case_count"] = len(cases)
    write(readiness_path, readiness)
    return {"readiness": evidence.pin(readiness_path), "all_makers_closed": barrier, "planned_roles": len(planned), "closed_roles": readiness["closed_role_count"], "ready_cases": readiness["ready_case_count"], "planned_cases": len(cases), "jobs_written": len(readiness["jobs"]), "launched": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus", required=True)
    p.add_argument("--production", "--production-root", dest="production", required=True)
    p.add_argument("--out", "--out-root", dest="out", required=True)
    p.add_argument("--wave", choices=("initial", "selected"), required=True)
    p.add_argument("--candidate-label")
    p.add_argument("--initial-root", help="explicit prior preparation root for complete first-review reuse")
    args = p.parse_args()
    try:
        result = prepare(args)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
