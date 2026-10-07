#!/usr/bin/env python3
"""Read-only blind-wave evidence validation and unaveraged gate summary.

The packet is the selection. Raw critics are authoritative. This checks recorded
bindings/coverage, not whether view calls happened or visual opinions are correct.
JSON goes to stdout; no files are written. Exit 0 = PASS, 1 = FAIL, 2 = input error.
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
# These exact documents preceded the first G native call. A one-member packet
# alone cannot waive an existing multiset gate or declare a new control later.
G_PLAN_SHA256 = "96160b13510366e678e1f7d2769374e22366e07baa9d3ebf1785bbd492f2a3a8"
G_CASES_SHA256 = "af995f8bd218ef2e49b3933a0403db2d50ccaab996cea38b7cbc489751c8a8bb"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text())


def norm(s):
    return " ".join(str(s).split())


def nonempty(v):
    return bool(v.strip()) if isinstance(v, str) else isinstance(v, list) and bool(v) and all(nonempty(x) for x in v)


def png_size(p):
    d = p.read_bytes()[:24]
    if len(d) != 24 or d[:8] != b"\x89PNG\r\n\x1a\n" or d[12:16] != b"IHDR":
        raise ValueError("Not a PNG with IHDR: " + str(p))
    return struct.unpack(">II", d[16:24])


def resolve(value, base):
    p = Path(value)
    return (p if p.is_absolute() else base / p).resolve()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--wave", default="initial", help="initial, correction1, correction2, etc.; selects blind-WAVE")
    ap.add_argument("--packet", type=Path)
    ap.add_argument("--mapping", type=Path)
    ap.add_argument("--reviews-dir", type=Path)
    ap.add_argument("--plan", type=Path)
    ap.add_argument("--procedural-extension", type=Path)
    a = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", a.wave):
        ap.error("--wave must contain only letters, digits, underscore or hyphen")
    root = a.root.resolve()
    wave = root / ("blind-" + a.wave)
    packet_path = (a.packet or wave / "packet.json").resolve()
    mapping_path = (a.mapping or root / "planning" / (a.wave + "-blind-mapping.json")).resolve()
    reviews_dir = (a.reviews_dir or wave / "reviews").resolve()
    plan_path = (a.plan or root / "planning/phase-plan.json").resolve()
    errors, binding_records, critic_records, below4, set_records, gate_failures = [], [], [], [], [], []
    procedures, source_pins, singleton_cases = {}, [], {}
    profiles=PROFILES; extension=None; allowed_order_violations=set(); required_valid_actions=set(PROFILES)

    def require(ok, message):
        if not ok:
            errors.append(message)

    def bind(p, expected, label):
        require(p.is_file(), "Missing " + label + ": " + str(p))
        if not p.is_file():
            return None
        actual = sha(p)
        require(isinstance(expected, str) and actual == expected, "SHA mismatch/missing pin " + label + ": " + str(p))
        return actual

    try:
        packet, mapping_doc, plan = read(packet_path), read(mapping_path), read(plan_path)
        if a.procedural_extension:
            extension=read(a.procedural_extension.resolve())
            require(extension.get("wave")==a.wave,"Procedural extension wave mismatch")
            require(extension.get("profiles")==["editorial","craft","portfolio","craft_ordered"],"Unexpected extension profiles")
            require(extension.get("explicit_allowed_order_violation")==["craft"],"Unexpected order exception")
            require(extension.get("required_valid_action_first_profiles")==["editorial","portfolio","craft_ordered"],"Extension lacks original three valid action readings")
            profiles=tuple(extension["profiles"]);allowed_order_violations=set(extension["explicit_allowed_order_violation"]);required_valid_actions=set(extension["required_valid_action_first_profiles"])
        pin_plans = [plan_path]
        initial_closed_plan = root / "continuation-e/planning/phase-plan.json"
        if a.wave == "initial" and initial_closed_plan.is_file() and initial_closed_plan.resolve() != plan_path:
            pin_plans.append(initial_closed_plan.resolve())
        for pin_plan_path in pin_plans:
            pin_plan = read(pin_plan_path)
            for pin in pin_plan.get("prior_closed_records_pinned", []) + pin_plan.get("closed_initial_reviews_pinned", []):
                pp = resolve(pin["path"], pin_plan_path.parent)
                actual = bind(pp, pin["sha256"], "closed source record")
                source_pins.append({"plan": str(pin_plan_path), "path": str(pp), "expected_sha256": pin["sha256"], "actual_sha256": actual})
        review_plan = plan["review"]
        require(review_plan["independent_reviewers"] == 3, "Plan reviewer count is not three")
        require(tuple(review_plan["seven_dimensions"]) == DIMS, "Plan seven dimensions changed")
        gate_text = review_plan["unchanged_core_gate"]
        require(all(k in gate_text for k in CORE) and ">=4" in gate_text and "diversity" in gate_text,
                "Unsupported/unrecognized predeclared gate text")
        mapping = mapping_doc["mapping"] if isinstance(mapping_doc, dict) else mapping_doc
        images = packet["images"]
        image_ids = [x["image_id"] for x in images]
        mapping_ids = [x["image_id"] for x in mapping]
        require(len(image_ids) == len(set(image_ids)), "Duplicate packet image ID")
        require(len(mapping_ids) == len(set(mapping_ids)), "Duplicate mapping image ID")
        require(set(mapping_ids) == set(image_ids), "Packet/mapping image IDs differ")
        by_id = {x["image_id"]: x for x in images}
        by_map = {x["image_id"]: x for x in mapping}
        require(len({x.get("role") for x in mapping}) == len(mapping), "Duplicate/missing selected role in mapping")

        for item in images:
            ident = item["image_id"]
            m = by_map.get(ident, {})
            case = item["case_id"]
            require(case in packet["cases"], ident + " unknown case")
            require(m.get("case_id") == case, ident + " mapping case differs")
            native_hash = m.get("native_sha256", m.get("sha256"))
            if "sha256" in m:
                require(m["sha256"] == native_hash, ident + " native SHA fields disagree")
            selected_path = resolve(m["final_native"], root)
            bind(selected_path, native_hash, ident + " selected native")
            qa = m.get("qa_hashes", {})
            qa_pins = {resolve(k, root): v for k, v in qa.items()}
            record = {"image_id": ident, "role": m.get("role"), "stage": m.get("stage"), "version": m.get("version"),
                      "case_id": case, "selected_native": str(selected_path), "native_sha256": native_hash, "views": {}}
            for view in VIEWS:
                vp = resolve(item[view], packet_path.parent)
                actual = bind(vp, qa_pins.get(vp), ident + " " + view)
                size = png_size(vp) if vp.is_file() else None
                record["views"][view] = {"path": str(vp), "sha256": actual, "dimensions": size}
                if view == "native":
                    require(actual == native_hash, ident + " anonymous native differs from selected native")
                    require(size == (item["width"], item["height"]), ident + " packet native dimensions disagree")
                    require(size == (m.get("width"), m.get("height")), ident + " mapping native dimensions disagree")
                    n, d = map(int, item["target_ratio"].split(":"))
                    require(size is not None and abs(size[0] / size[1] / (n / d) - 1) <= .01, ident + " ratio error >1%")
                elif size:
                    require(size[0] == 720 if view == "usage720" else max(size) == 320, ident + " wrong QA dimensions " + view)
                    require(abs(size[0] / size[1] / (item["width"] / item["height"]) - 1) <= .01, ident + " distorted QA ratio " + view)
            binding_records.append(record)

        for case, s in packet["sets"].items():
            expected = [x["image_id"] for x in images if x["case_id"] == case]
            require(len(s["members"]) == len(set(s["members"])), case + " duplicate set member")
            require(set(s["members"]) == set(expected), case + " packet set membership differs from image cases")
            require(len(expected) == s["expected_count"] == packet["cases"][case]["expected_count"], case + " expected set count mismatch")
        require(set(packet["sets"]) == {x["case_id"] for x in images}, "Packet set/case coverage differs")

        for case, declared in packet["cases"].items():
            if declared.get("expected_count") != 1:
                continue
            require(case == "type-only-control", "Unsupported singleton case: " + case)
            if case != "type-only-control":
                continue
            frozen_plan = root / "continuation-g/planning/phase-plan.json"
            frozen_cases = root / "continuation-g/planning/cases.json"
            require(plan_path == frozen_plan.resolve() and sha(plan_path) == G_PLAN_SHA256,
                    "Singleton must use the exact predeclared G plan")
            actual_cases = bind(frozen_cases, G_CASES_SHA256, "predeclared singleton cases")
            cases_pin = {"path": str(frozen_cases.resolve()), "sha256": G_CASES_SHA256}
            require(isinstance(mapping_doc, dict) and mapping_doc.get("predeclared_cases") == cases_pin,
                    "Singleton mapping cases source pin differs")
            rule = plan.get("scope", {}).get("singleton_rule", "")
            require(plan.get("status") == "PREDECLARED_BEFORE_FIRST_G_NATIVE_CALL"
                    and plan.get("scope", {}).get("additional_control_role") == "T01"
                    and "T01" in plan.get("scope", {}).get("new_original_roles", [])
                    and "no diversity or closest pair score" in rule, "Singleton exception was not predeclared")
            definition = next(x for x in read(frozen_cases)["cases"] if x.get("review_case_id") == case)
            require(definition["id"] == "constrained-type-only-transfer" and definition["expected_final_count"] == 1
                    and definition["slots"] == [{"id": "T01", "ratio": "2:3"}], "Singleton frozen case declaration differs")
            require(declared.get("request") == definition["request"] and declared.get("copy") == definition["copy"]
                    and declared.get("source_case_id") == definition["id"] and declared.get("review_case_id") == case
                    and declared.get("singleton_diversity") == "not_applicable", "Singleton packet brief differs from predeclared case")
            members = [x for x in mapping if x.get("case_id") == case]
            require(len(members) == 1 and members[0].get("role") == "T01" and members[0].get("phase") == "G",
                    "Singleton must bind exactly the G T01 control")
            singleton_cases[case] = {"role": "T01", "source_plan": {"path": str(plan_path), "sha256": G_PLAN_SHA256},
                                     "source_cases": cases_pin, "rule": rule,
                                     "scope": "No diversity/pair observation applies; all seven image scores and every critic's mandatory/core gates remain required."}
            source_pins.append({"plan": str(plan_path), "path": str(frozen_cases.resolve()),
                                "expected_sha256": G_CASES_SHA256, "actual_sha256": actual_cases})

        action_path = packet_path.parent / "action-first.json"
        action_packet = read(action_path)
        action_images = {x["image_id"]: x for x in action_packet["images"]}
        expected_action_ids = {x["image_id"] for x in images if x["case_id"] == "invitation"}
        require(set(action_images) == expected_action_ids, "Action-first packet does not cover exactly the invitation set")
        raw_reports = {}
        for profile in profiles:
            raw_path = reviews_dir / (profile + ".json")
            report = read(raw_path)
            md_path=raw_path.with_suffix(".md");md_text=md_path.read_text() if md_path.is_file() else "";md_preamble=md_text.split("|")[0]
            raw_reports[profile] = report
            identity=report.get("reviewer");identity=identity.get("profile") if isinstance(identity,dict) else identity
            require(identity == profile, profile + " reviewer identity mismatch")
            require(set(report["images"]) == set(image_ids), profile + " reviewed image coverage differs from selected packet")
            require(set(report["sets"]) == set(packet["sets"]), profile + " set review coverage differs")
            language = " ".join(str(v) for k, v in report.items() if k in
                                {"normalization", "transcription_method", "transcription_convention", "copy_transcription_method", "method","attestations"})+"\n"+md_preamble
            require(any(x in language.lower() for x in ["manual","independently transcribed","independent copy transcription","수동","판독·전사"]),profile+" lacks recorded visual transcription attestation")
            viewed = report.get("viewed", [])
            viewed_triples = {(v.get("image_id"), v.get("view"), resolve(v["path"], packet_path.parent)) for v in viewed}
            for entry in viewed:
                ident, view = entry.get("image_id"), entry.get("view")
                expected_view = "usage720" if view == "action-first720" else view
                require(ident in by_id and expected_view in VIEWS, profile + " unknown recorded viewed image/view")
                if ident in by_id and expected_view in VIEWS:
                    require(resolve(entry["path"], packet_path.parent) == resolve(by_id[ident][expected_view], packet_path.parent),
                            profile + " extra/unbound recorded view path " + ident + "/" + str(view))
            for ident in image_ids:
                for view in VIEWS:
                    vp = resolve(by_id[ident][view], packet_path.parent)
                    require((ident, view, vp) in viewed_triples, profile + " lacks recorded actual " + ident + "/" + view + " path")

            preflight_path = reviews_dir / (profile + "-action-first.json")
            preflight = read(preflight_path)
            identity=preflight.get("reviewer");identity=identity.get("profile") if isinstance(identity,dict) else identity
            require(identity == profile, profile + " preflight reviewer identity mismatch")
            readings = preflight.get("readings",preflight.get("observations_before_full_copy",preflight.get("observations",preflight.get("images",[]))))
            if isinstance(readings,list):
                require(len({x["image_id"] for x in readings})==len(readings),profile+" duplicate preflight image IDs")
                readings={x["image_id"]:x for x in readings}
            require(set(readings) == expected_action_ids, profile + " action-first reading coverage differs")
            order_report = str({k: v for k, v in report.items() if "order" in k or k in {'method','attestations'}})+"\n"+md_preamble
            order_preflight = str({k: v for k, v in preflight.items() if "order" in k or k in {'method','preflight_before_copy','preflight_before_full_copy'}})
            false_order=report.get("order_compliant") is False or preflight.get("order_compliant") is False
            valid_order=(not false_order and ("True" in order_preflight or "before" in order_preflight.lower()) and ("True" in order_report or "before" in order_report.lower() or "→" in order_report))
            if profile in allowed_order_violations:
                require(false_order,profile+" explicitly permitted failed order must remain disclosed false")
            else:
                require(valid_order,profile+" lacks compliant action-before-copy attestation")
            for ident, reading in readings.items():
                if ident not in by_id:
                    continue
                aliases = {"date": ("event_date", "eventdate", "observed_event_date"), "deadline": ("application_deadline", "deadline", "observed_application_deadline"),
                           "url": ("full_application_url", "fullURL", "url", "observed_full_application_url","full_application_url_observed","observed_full_url")}
                values = {key: next((reading[k] for k in names if k in reading), None) for key, names in aliases.items()}
                require(all(nonempty(v) for v in values.values()), profile + " incomplete date/deadline/full URL reading " + ident)
                require("uncertainty" in reading or "uncertainties" in reading, profile + " missing preflight uncertainty " + ident)
                paths = reading.get("actual_view_paths", reading.get("actualpaths", [reading.get("actual_view_path",reading.get("path",reading.get('viewed_path')))]))
                expected_path = resolve(by_id[ident]["usage720"], packet_path.parent)
                require(expected_path in {resolve(p, packet_path.parent) for p in paths if p}, profile + " preflight path not actual bound720 " + ident)
                require(resolve(action_images[ident]["usage720"], packet_path.parent) == expected_path, ident + " action-first image path differs")
                copy = packet["cases"][by_id[ident]["case_id"]]["copy"]
                require(any(norm(values["date"]) == norm(c) for c in copy), profile + " preflight event date differs from copy " + ident)
                action_copy = next((c for c in copy if ".example/" in c), "")
                expected_url = re.search(r"(?:https?://)?[A-Za-z0-9][A-Za-z0-9.-]*\.example/\S+", action_copy)
                require(expected_url is not None and values["url"] == expected_url.group(), profile + " preflight full URL differs " + ident)
                deadline_prefix=norm(action_copy.split(":", 1)[0]);deadline_reading=norm(values["deadline"]).rstrip(":")
                # This field asks for the deadline, not the adjacent action verb.
                # Exact full-copy transcription is checked independently below.
                require(deadline_reading in {deadline_prefix, deadline_prefix.removesuffix(" 신청")}, profile + " preflight deadline differs " + ident)

            procedures[profile] = {"raw_report": str(raw_path), "raw_report_sha256": sha(raw_path),
                                   "action_first_record": str(preflight_path), "action_first_sha256": sha(preflight_path),
                                   "action_first_raw_observations": preflight, "recorded_view_entries": viewed,
                                   "manual_method_attestation": language,"raw_markdown":str(md_path),"raw_markdown_sha256":sha(md_path) if md_path.is_file() else None,
                                   "order_attestations": {"main_report": order_report, "preflight": order_preflight},
                                   "valid_action_first_attestation":valid_order,"explicit_procedural_failure_retained":profile in allowed_order_violations,
                                   "coverage_check": "Recorded native/720/320 paths matched every selected anonymous image"}

            for ident, obs in report["images"].items():
                if ident not in by_id:
                    continue
                scores, mandatory, evidence = obs["scores"], obs["mandatory"], obs["evidence"]
                require(set(scores) == set(DIMS), profile + " not exactly seven scores " + ident)
                require(all(type(scores.get(k)) is int and 1 <= scores[k] <= 5 for k in DIMS), profile + " scores not integer1–5 " + ident)
                require(set(evidence) == set(DIMS) and all(nonempty(evidence.get(k)) for k in DIMS), profile + " missing located evidence field " + ident)
                require(type(mandatory.get("pass")) is bool, profile + " mandatory flag not Boolean " + ident)
                require("issues" in mandatory and "uncertainties" in mandatory, profile + " missing mandatory issue/uncertainty record " + ident)
                expected_copy = packet["cases"][by_id[ident]["case_id"]]["copy"]
                transcription = mandatory.get("transcription", [])
                require([x.get("required") for x in transcription] == expected_copy, profile + " missing/altered/all-item transcription coverage " + ident)
                copy_failed = False
                for t in transcription:
                    require(nonempty(t.get("observed")) and type(t.get("equal")) is bool, profile + " invalid manual observation " + ident)
                    equal = norm(t.get("required", "")) == norm(t.get("observed", ""))
                    require(t.get("equal") == equal, profile + " recorded equality contradicts transcription " + ident)
                    copy_failed |= not equal
                rec = {"profile": profile, "image_id": ident, "role": by_map[ident].get("role"),
                       "raw_path": str(raw_path), "raw_sha256": sha(raw_path), "mandatory": mandatory,
                       "scores": scores, "evidence": evidence, "residuals": obs.get("residuals", [])}
                critic_records.append(rec)
                if mandatory.get("pass") is not True or copy_failed:
                    gate_failures.append({"profile": profile, "image_id": ident, "kind": "mandatory", "record": mandatory})
                for dim, score in scores.items():
                    if type(score) is int and score < 4:
                        low = {"profile": profile, "image_id": ident, "role": by_map[ident].get("role"),
                               "dimension": dim, "score": score, "core": dim in CORE, "evidence": evidence.get(dim)}
                        below4.append(low)
                        if dim in CORE:
                            gate_failures.append(dict(low, kind="core"))

            supplement_path=reviews_dir/(profile+'-nearest-pair-supplement.json');supplement=read(supplement_path) if supplement_path.is_file() else None
            if supplement:
                require(supplement.get('reviewer')==profile,profile+' nearest-pair supplement reviewer differs')
                source=supplement.get('raw_report',{});source=source if isinstance(source,dict) else {}
                require(supplement.get('raw_report_sha256',source.get('sha256'))==sha(raw_path),profile+' supplement does not pin closed raw report')
                require(resolve(supplement.get('raw_report_absolute',source.get('path','')),reviews_dir)==raw_path.resolve(),profile+' supplement pins another raw report')
                require(set(supplement.get('sets',{}))==set(report['sets']),profile+' supplement set coverage differs')
            for case, obs in report["sets"].items():
                require(set(obs["members"]) == set(packet["sets"][case]["members"]) and len(obs["members"]) == len(packet["sets"][case]["members"]),
                        profile + " reviewed set membership differs " + case)
                if case in singleton_cases:
                    require("diversity" in obs and obs["diversity"] is None, profile + " singleton diversity must be null " + case)
                    require(obs.get("closest_pair") == [], profile + " singleton closest pair must be [] " + case)
                    require(all(obs.get(k) is None for k in ("closest_pair_diversity", "closest_pair_score", "nearest_pair_score")),
                            profile + " singleton pair score must be null/absent " + case)
                    require(nonempty(obs.get("evidence")), profile + " missing located singleton evidence " + case)
                    set_records.append(dict(obs, profile=profile, case_id=case, raw_path=str(raw_path), raw_sha256=sha(raw_path),
                                            normalized_closest_pair_members=[], normalized_closest_pair_score=None,
                                            singleton_predeclaration=singleton_cases[case]))
                    continue
                require(type(obs.get("diversity")) is int and 1 <= obs["diversity"] <= 5, profile + " invalid diversity score " + case)
                pair=obs.get("closest_pair",[]); pair_members=pair.get("members",[]) if isinstance(pair,dict) else pair
                require(len(pair_members)==2 and len(set(pair_members))==2 and set(pair_members)<=set(obs["members"]),profile+" invalid nearest pair "+case)
                closest=obs.get("closest_pair_diversity",obs.get("closest_pair_score",pair.get("score",pair.get('diversity')) if isinstance(pair,dict) else None))
                supplemental_binding=None
                if closest is None and supplement:
                    item=supplement['sets'][case];require(item['members']==pair_members,profile+' supplement nearest-pair members differ '+case);require(nonempty(item.get('evidence')),profile+' supplement evidence missing '+case);closest=item.get('score');supplemental_binding={'path':str(supplement_path),'sha256':sha(supplement_path),'raw_observation':item,'scope':'Append-only original reviewer completion of missing noncore nearest-pair numeric observation; original seven image/set-diversity scores unchanged.'}
                require(type(closest) is int and 1 <= closest <= 5, profile + " missing nearest-pair integer score " + case)
                require(nonempty(obs.get("evidence")), profile + " missing diversity evidence " + case)
                rec = dict(obs, profile=profile, case_id=case, raw_path=str(raw_path), raw_sha256=sha(raw_path),normalized_closest_pair_members=pair_members,normalized_closest_pair_score=closest)
                if supplemental_binding:rec['closest_pair_supplement']=supplemental_binding
                set_records.append(rec)
                if type(obs.get("diversity")) is int and obs["diversity"] < 4:
                    gate_failures.append(dict(rec, kind="diversity"))

        disagreements = []
        for ident in image_ids:
            for dim in DIMS:
                values = {p: raw_reports[p]["images"][ident]["scores"].get(dim) for p in profiles}
                if len(set(values.values())) > 1:
                    disagreements.append({"image_id": ident, "role": by_map[ident].get("role"), "dimension": dim, "raw_scores": values})
        for case in packet["sets"]:
            values = {p: raw_reports[p]["sets"][case].get("diversity") for p in profiles}
            if len(set(values.values())) > 1:
                disagreements.append({"case_id": case, "dimension": "diversity", "raw_scores": values})
        other_disagreements = []
        for ident in image_ids:
            flags = {p: raw_reports[p]["images"][ident]["mandatory"]["pass"] for p in profiles}
            if len(set(flags.values())) > 1:
                other_disagreements.append({"image_id": ident, "field": "mandatory.pass", "raw_values": flags})
        for case in packet["sets"]:
            for field in ("closest_pair", "closest_pair_score"):
                values={p:next(x for x in set_records if x["profile"]==p and x["case_id"]==case)["normalized_closest_pair_members" if field=="closest_pair" else "normalized_closest_pair_score"] for p in profiles}
                if len({json.dumps(v, sort_keys=True) for v in values.values()}) > 1:
                    other_disagreements.append({"case_id": case, "field": field, "raw_values": values})
        set_below4 = []
        for rec in set_records:
            for field, score in (("diversity", rec["diversity"]), ("closest_pair", rec["normalized_closest_pair_score"])):
                if type(score) is int and score < 4:
                    set_below4.append({"profile": rec["profile"], "case_id": rec["case_id"], "field": field, "score": score,
                                       "gated": field == "diversity", "members": rec["members"], "evidence": rec["evidence"]})
        for profile in required_valid_actions:require(procedures.get(profile,{}).get("valid_action_first_attestation") is True,profile+" missing valid required action-first")
        result = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "wave": a.wave,
                  "status": "FAIL" if errors or gate_failures else "PASS",
                  "recorded_evidence_integrity": "FAIL" if errors else "PASS",
                  "predeclared_core_diversity_gate": "FAIL" if gate_failures or errors else "PASS",
                  "scope": "Structural recorded-evidence and exact SHA bindings only. View-path/order claims and manual located visual observations are critic attestations; this script cannot prove actual viewing, temporal order, semantic location, visual quality, authorship, physical mechanics, print suitability, or universal future capability. Raw scores are authoritative; no averages, consensus rewrites, or nearest-pair threshold added to the declared gate.",
                  "inputs": {"packet": str(packet_path), "packet_sha256": sha(packet_path), "mapping": str(mapping_path),
                             "mapping_sha256": sha(mapping_path), "plan": str(plan_path), "plan_sha256": sha(plan_path)},
                  "procedural_extension":extension,"valid_required_action_first_profiles":sorted(required_valid_actions),"quality_gate_critic_scope":"All listed critics, including disclosed failed-order craft; no scores excluded",
                  "predeclared_gate_text": gate_text, "selected_image_count": len(image_ids), "critics": list(profiles),
                  "image_critic_record_count": len(critic_records), "score_observation_count": sum(len(r["scores"]) for r in critic_records),
                  "below4_image_score_count": len(below4), "core_below4_count": sum(r["core"] for r in below4),
                  "noncore_below4_count": sum(not r["core"] for r in below4),
                  "diversity_below4_count": sum(r["kind"] == "diversity" for r in gate_failures),
                  "integrity_errors": errors, "closed_source_pin_checks": source_pins, "image_bindings": binding_records, "review_procedure": procedures, "image_critic_records": critic_records,
                  "all_scores_below4": below4, "all_set_records": set_records, "all_set_score_observations_below4": set_below4,
                  "disagreements": disagreements, "other_recorded_disagreements": other_disagreements,
                  "located_gate_failures": gate_failures}
        if singleton_cases:
            result["predeclared_singleton_cases"] = singleton_cases
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["status"] == "FAIL" else 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as e:
        print(json.dumps({"wave": a.wave, "status": "FAIL", "recorded_evidence_integrity": "FAIL",
                          "predeclared_core_diversity_gate": "FAIL", "input_error": type(e).__name__ + ": " + str(e),
                          "integrity_errors_before_input_error": errors}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
