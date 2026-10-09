#!/usr/bin/env python3
"""Prospective recording adapter only: no agents, image work, cases, or scores generated."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from pathlib import Path

DIMENSIONS = ("content_form", "hierarchy", "typography", "space", "image_material", "emotion_control", "ai_slop")
VIEWS = ("native", "usage720", "thumbnail320")
STATUSES = ("PASS", "FAIL", "NA")
NORMALIZATION = "nfc-ws-optical-v1"
URL = re.compile(r"(?i)(?:https?://|www\.)\S+")
SUMMARY_SHA256 = "4c5dc9847694b4cfe1744115ff1a79e9e7e9d5c71abea38b7f3250600c2144e0"


def require(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
    path = Path(path).resolve(strict=True)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def load_json(path):
    path = Path(path).resolve(strict=True)
    data = path.read_bytes()
    return json.loads(data), {"path": str(path), "sha256": hashlib.sha256(data).hexdigest()}


def normalize(raw, entry):
    """Frozen v4 NFC/whitespace/optical policy; raw input remains untouched."""
    require(isinstance(raw, str), "Actual raw reading must be a string; no fallback from required copy")
    value = unicodedata.normalize("NFC", raw.replace("\r\n", "\n").replace("\r", "\n"))
    if entry["fixed_newlines"]:
        value = "\n".join(re.sub(r"[^\S\n]+", " ", line).strip() for line in value.split("\n"))
    else:
        value = re.sub(r"\s+", " ", value).strip()
    if entry["kind"] == "text":
        pieces, previous = [], 0
        for match in URL.finditer(value):
            pieces.append(re.sub(r" *([·/]) *", r"\1", value[previous:match.start()]))
            pieces.append(match.group())
            previous = match.end()
        pieces.append(re.sub(r" *([·/]) *", r"\1", value[previous:]))
        value = "".join(pieces)
    return value


def evidence(items, members=None):
    """Compact tuples: [view, location, observation], or [image_id, view, location, observation]."""
    require(isinstance(items, list) and bool(items), "Located evidence must be nonempty")
    result = []
    for item in items:
        require(isinstance(item, list) and len(item) == (4 if members is not None else 3), "Invalid evidence tuple")
        image_id, tail = (item[0], item[1:]) if members is not None else (None, item)
        view, location, observation = tail
        require(view in VIEWS and isinstance(location, str) and location.strip() and isinstance(observation, str) and observation.strip(), "Evidence needs a named view, location and observed fact")
        row = {"view": view, "location": location, "observation": observation}
        if members is not None:
            require(image_id in members, "Set evidence must name a requested member")
            row["image_id"] = image_id
        result.append(row)
    return result


def checked_status(data):
    require(isinstance(data, dict) and data.get("status") in STATUSES, "Every mandatory judgment needs explicit PASS/FAIL/NA")
    require(isinstance(data.get("issues", []), list), "Issues must be an array")
    return copy.deepcopy(data)


def export(packet, raw, *, packet_pin=None, raw_pin=None, adapter_pin=None):
    """Derive repeated metadata only; retain critic strings, judgments, scores and low values."""
    require(packet.get("normalization") == NORMALIZATION, "Normalization must be predeclared")
    require(type(packet.get("expected_count")) is int and packet["expected_count"] == 5, "This method is bounded to one complete five-image request")
    images = packet.get("images", [])
    ids = [image["image_id"] for image in images]
    require(len(ids) == 5 and len(set(ids)) == 5, "Exactly five distinct packet members required")
    require(type(raw.get("schema_version")) is int and raw["schema_version"] == 1 and raw.get("kind") == "compact_critic_observations", "Compact schema version/kind required")
    for key in ("case_id", "wave"):
        require(raw.get(key) == packet.get(key), f"Raw {key} differs from packet")
    profile = raw.get("profile")
    require(profile in packet.get("critic_profiles", []), "Profile must be one declared independent critic")
    require(raw.get("session_id") is None, "Runner, not adapter, binds actual session identity")
    if packet_pin is not None:
        require(raw.get("packet") == packet_pin, "Raw observations must bind the exact input packet")
    require(isinstance(raw.get("images"), dict) and set(raw["images"]) == set(ids), "All five raw records required; no extra/dropped member")
    expected = [(image["image_id"], view) for image in images for view in VIEWS]
    visits = raw.get("viewed")
    require(isinstance(visits, list) and [(v.get("image_id"), v.get("view")) for v in visits] == expected, "All fifteen attempted views must remain in exact packet order")
    procedure = copy.deepcopy(raw.get("procedure"))
    require(isinstance(procedure, dict) and all(type(procedure.get(k)) is bool for k in ("fresh_session", "all_views_before_scoring", "order_compliant")), "Truthful procedure booleans required")
    require(isinstance(procedure.get("method"), str) and procedure["method"].strip(), "Actual method description required")
    binding_errors, viewed = [], []
    by_id = {image["image_id"]: image for image in images}
    for visit in visits:
        require(type(visit.get("viewed")) is bool, "Every view needs an actual viewed boolean")
        require(isinstance(visit.get("path"), str) and isinstance(visit.get("sha256"), str), "Retain supplied/unknown raw path and hash; do not invent one")
        target = by_id[visit["image_id"]]["views"][visit["view"]]
        if (visit["path"], visit["sha256"]) != (target["path"], target["sha256"]):
            binding_errors.append(f"{visit['image_id']}/{visit['view']}: raw path/hash does not match exact packet view")
        if visit["viewed"]:
            viewed.append({k: visit[k] for k in ("image_id", "view", "path", "sha256")})
        else:
            require(isinstance(visit.get("reason"), str) and visit["reason"].strip(), "Unavailable view needs an honest reason")
    # These two fields are mechanical counts/order bindings, never fabricated opens.
    procedure["viewed_count"] = len(viewed)
    if binding_errors:
        procedure["order_compliant"] = False
    procedure["adapter_binding_errors"] = binding_errors
    assets = packet.get("source_assets", [])
    source_visits = procedure.get("source_assets_viewed")
    layout_reads = procedure.get("protected_layouts_read")
    require(isinstance(source_visits, list) and isinstance(layout_reads, list), "Source view/layout read receipts required, including empty arrays")
    require(len(source_visits) == len(assets) and len({v.get('asset_id') for v in source_visits}) == len(assets), "One receipt for each actual source asset required")
    source_by_id = {asset["asset_id"]: asset for asset in assets}
    missing_sources = set()
    for receipt in source_visits:
        asset = source_by_id.get(receipt.get("asset_id"))
        require(asset is not None and type(receipt.get("viewed")) is bool, "Unknown/duplicate source receipt")
        matching = (receipt.get("path"), receipt.get("sha256")) == (asset["actual_path"], asset["sha256"])
        if not matching or not receipt["viewed"]:
            missing_sources.add(asset["asset_id"])
            require(isinstance(receipt.get("reason"), str) and receipt["reason"].strip(), "Unassessable source needs a reason")
    expected_layouts = { (x["manifest"]["path"], x["manifest"]["sha256"]): x["asset_id"] for x in packet.get("protected_layouts", []) }
    require(len(layout_reads) == len(expected_layouts), "Each protected-layout manifest needs one read receipt")
    seen_layouts = set()
    for receipt in layout_reads:
        manifest = receipt.get("manifest", {})
        key = (manifest.get("path"), manifest.get("sha256"))
        require(key in expected_layouts and key not in seen_layouts and type(receipt.get("read")) is bool, "Read receipts must bind exact protected manifests")
        seen_layouts.add(key)
        if not receipt["read"]:
            missing_sources.add(expected_layouts[key])
            require(isinstance(receipt.get("reason"), str) and receipt["reason"].strip(), "Unread protected layout needs a reason")
    result = {"schema_version": 1, "case_id": packet["case_id"], "wave": packet["wave"], "profile": profile,
              "session_id": None, "procedure": procedure, "viewed": viewed, "images": {},
              "recording_adapter": {"kind": "declared_deterministic_export", "normalization": NORMALIZATION,
                                    "packet": packet_pin, "raw_observations": raw_pin, "adapter": adapter_pin,
                                    "compatible_summary_sha256": SUMMARY_SHA256,
                                    "limit": "Metadata bindings and attestations do not prove semantic viewing or source fidelity"}}
    for image in images:
        iid, observation = image["image_id"], raw["images"][image["image_id"]]
        mandatory = observation.get("mandatory")
        require(isinstance(mandatory, dict) and set(mandatory) == {"text", "style", "ratio", "no_type_only", "substantive_visual"}, "All five mandatory judgments required")
        checks = {name: checked_status(data) for name, data in mandatory.items()}
        for name, check in checks.items():
            allowed = {"status", "issues", "evidence"} if name in ("style", "no_type_only", "substantive_visual") else {"status", "issues"}
            require(not (set(check) - allowed), "Repeated export fields must not replace a critic's extra raw judgments; use the compact schema")
        rows = observation.get("copy")
        require(isinstance(rows, list) and len(rows) == len(packet["copy"]), "Every first-read copy entry required")
        transcripts, ambiguities = [], []
        for index, (entry, reading) in enumerate(zip(packet["copy"], rows)):
            require(isinstance(reading, dict) and set(reading) == {"raw", "layout", "ambiguity", "revisit"}, "Compact reading needs raw/layout/ambiguity/revisit only")
            first = reading.get("raw")
            require(isinstance(first, str), "Never fill missing raw reading from required copy")
            layout = reading.get("layout")
            require(isinstance(layout, dict) and layout.get("status") in STATUSES and isinstance(layout.get("observations"), str) and layout["observations"].strip(), "Separate actual layout observation required")
            ambiguity, revisit = reading.get("ambiguity"), reading.get("revisit")
            require(ambiguity is None or isinstance(ambiguity, str) and bool(ambiguity.strip()), "Ambiguity must be explicit or null")
            comparison = first
            if revisit is not None:
                require(ambiguity and isinstance(revisit, dict) and revisit.get("view") in VIEWS and type(revisit.get("resolved")) is bool and isinstance(revisit.get("raw_observed"), str), "Only one ambiguity-triggered exact-view revisit permitted")
                target = image["views"][revisit["view"]]
                require((revisit.get("path"), revisit.get("sha256")) == (target["path"], target["sha256"]), "Revisit must use the same pinned asset")
                require(all(isinstance(revisit.get(k), str) and revisit[k].strip() for k in ("reason", "resolution")), "Revisit needs reason and resolution explanation")
                if revisit["resolved"]:
                    comparison = revisit["raw_observed"]
            nr, no = normalize(entry["text"], entry), normalize(comparison, entry)
            transcripts.append({"required": entry["text"], "raw_observed": first, "normalized_required": nr,
                                "normalized_observed": no, "equal": nr == no, "layout": copy.deepcopy(layout),
                                "ambiguity": ambiguity, "revisit": copy.deepcopy(revisit)})
            if ambiguity:
                ambiguities.append({"copy_index": index, "description": ambiguity, "resolved": bool(revisit and revisit["resolved"])})
        checks["text"].update(transcriptions=transcripts, ambiguities=ambiguities)
        checks["text"].setdefault("issues", [])
        checks["style"]["checked_requirement"] = image.get("style_requirement", packet["requirements"]["style"])
        for name in ("style", "no_type_only", "substantive_visual"):
            checks[name]["evidence"] = evidence(checks[name].get("evidence"))
        native = image["views"]["native"]
        checks["ratio"]["observed_dimensions"] = [native["width"], native["height"]]
        checks["ratio"]["dimension_source"] = "exact packet native-view metadata; frozen summary independently checks native PNG header"
        ratings = observation.get("ratings")
        require(isinstance(ratings, dict) and set(ratings) == set(DIMENSIONS), "All seven ratings required")
        scores, located = {}, {}
        for dimension in DIMENSIONS:
            rating = ratings[dimension]
            score = rating.get("score")
            require(score is None or type(score) is int and 1 <= score <= 5, "Score must be an actual integer 1–5 or honest unjudgable null")
            if score is None:
                require(isinstance(rating.get("reason"), str) and rating["reason"].strip(), "Unjudgable null score needs a reason")
            scores[dimension] = score
            located[dimension] = evidence(rating.get("evidence"))
        fidelity = observation.get("source_fidelity")
        require(isinstance(fidelity, list) and len(fidelity) == len(assets) and {f.get("asset_id") for f in fidelity} == set(source_by_id), "Explicit identity/applicable protected-geometry fidelity for every source required")
        require(len({f.get("asset_id") for f in fidelity}) == len(fidelity), "Duplicate source-fidelity record")
        for judgment in fidelity:
            require(judgment.get("status") in STATUSES and isinstance(judgment.get("observations"), str) and judgment["observations"].strip(), "Actual source/geometry assessment or NA explanation required")
            require(judgment["asset_id"] not in missing_sources or judgment["status"] == "NA", "Unknown/unviewed source or unread protected geometry cannot earn fidelity PASS")
        source_states = {judgment["status"] for judgment in fidelity}
        if "FAIL" in source_states:
            require(checks["style"]["status"] == "FAIL", "Literal style/conditions must include observed source-preservation failure")
        elif "NA" in source_states:
            require(checks["style"]["status"] in ("NA", "FAIL"), "Unassessable required source preservation cannot become style PASS")
        require(isinstance(observation.get("residuals"), list), "Residuals array required")
        result["images"][iid] = {"image_id": iid, "role": image["role"], "stage": image["stage"],
                                 "case_id": packet["case_id"], "profile": profile, "mandatory": checks,
                                 "scores": scores, "evidence": located, "residuals": copy.deepcopy(observation["residuals"]),
                                 "source_fidelity": copy.deepcopy(fidelity),
                                 "unjudgable_score_reasons": {d: ratings[d]["reason"] for d in DIMENSIONS if scores[d] is None}}
    group = copy.deepcopy(raw.get("set"))
    require(isinstance(group, dict) and group.get("members") == ids, "Full ordered five-member set required")
    count = group.get("count_fidelity")
    require(isinstance(count, dict) and count.get("status") in STATUSES and type(count.get("observed_count")) is int and isinstance(count.get("issues"), list), "Actual count judgment required")
    count["required_count"] = packet["expected_count"]
    diversity = group.get("diversity")
    require(diversity is None or type(diversity) is int and 1 <= diversity <= 5, "Actual full-set diversity integer or unjudgable null required")
    if diversity is None:
        require(isinstance(group.get("reason"), str) and group["reason"].strip(), "Unjudgable diversity needs a reason")
    group["evidence"] = evidence(group.get("evidence"), ids)
    require({e["image_id"] for e in group["evidence"]} == set(ids), "Diversity evidence must cover all five")
    require(isinstance(group.get("residuals"), list), "Set residuals array required")
    group["requested_count"] = packet["expected_count"]
    result["set"] = group
    return result


def markdown(report):
    lines = [f"# {report['profile']} — deterministic compatibility export", "",
             "Raw observations, their pin, and the declared adapter remain separate. No scores or observations were authored by this renderer.", "",
             f"Procedure: {json.dumps(report['procedure'], ensure_ascii=False)}", ""]
    for iid, row in report["images"].items():
        lines += [f"## {iid}", "", f"Mandatory: {json.dumps(row['mandatory'], ensure_ascii=False)}", ""]
        for dimension in DIMENSIONS:
            lines += [f"- {dimension}: {row['scores'][dimension]} — {json.dumps(row['evidence'][dimension], ensure_ascii=False)}"]
        lines += ["", f"Source fidelity: {json.dumps(row['source_fidelity'], ensure_ascii=False)}",
                  f"Residuals: {json.dumps(row['residuals'], ensure_ascii=False)}", ""]
    lines += ["## Complete set", "", json.dumps(report["set"], ensure_ascii=False), "",
              "## Recording provenance", "", json.dumps(report["recording_adapter"], ensure_ascii=False), ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    require(args.output_dir.is_dir(), "Use the already designated critic output directory; no job/directory creation")
    packet, packet_pin = load_json(args.packet)
    raw, raw_pin = load_json(args.observations)
    report = export(packet, raw, packet_pin=packet_pin, raw_pin=raw_pin, adapter_pin=pin(__file__))
    profile = report["profile"]
    require(re.fullmatch(r"[A-Za-z0-9_.-]+", profile) is not None, "Invalid profile filename")
    targets = [args.output_dir / f"{profile}.json", args.output_dir / f"{profile}.md"]
    require(all(not path.exists() for path in targets), "Compatibility outputs are exclusive; no raw/report overwrite")
    with targets[0].open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    with targets[1].open("x", encoding="utf-8") as handle:
        handle.write(markdown(report))
    require(pin(args.observations) == report["recording_adapter"]["raw_observations"], "Raw observations changed during export")
    require(pin(args.packet) == packet_pin, "Input packet changed during export")
    print(json.dumps({"derived_reports": [pin(path) for path in targets], "raw_observations": pin(args.observations)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
