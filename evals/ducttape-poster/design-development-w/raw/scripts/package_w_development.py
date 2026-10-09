"""Package closed W development after R20 itself has been exactly archived.

Preparation only until explicitly executed after full-five closure and archive
verification. No image tool, renderer, test, evaluator or source script is run.
"""
from pathlib import Path
import datetime
import hashlib
import json


TASK = Path(__file__).resolve().parents[1]
DEST = TASK / "Skillsets/evals/ducttape-poster/design-development-w"
ROUND_SOURCE = TASK / "work/round20"
ROUND_ARCHIVE = TASK / "Skillsets/evals/ducttape-poster/round20"
TEXT_SUFFIXES = {".json", ".md", ".txt", ".py", ".yaml", ".diff"}
SNAPSHOTS = (
    "history/first-generation-sketch-w/before-v",
    "history/first-generation-sketch-w/adopted-w",
)
CLOSED_TEXT_ROOTS = (
    "history/w-draft",
    "history/w-scope-audit",
)
NAMED_TEXT = (
    "history/first-generation-sketch-w/adoption.json",
    "drafts/w-five-design/plan.json",
    "drafts/w-five-design/rationale.md",
    "drafts/w-five-design/prepare_plan.py",
    "history/w-publication-prep/review.md",
    "scripts/prepare_w_workspace.py",
    "scripts/freeze_w_r20.py",
    "scripts/package_w_development.py",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def local_file(path, boundary=TASK):
    path = Path(path)
    require(path.is_absolute(), f"Absolute local path required: {path}")
    require(not path.is_symlink(), f"Symlink is outside this exact-file scope: {path}")
    resolved = path.resolve(strict=True)
    require(resolved.is_relative_to(boundary.resolve(strict=True)), f"Path outside scope: {path}")
    require(resolved.is_file(), f"File required: {path}")
    for parent in path.parents:
        if parent == boundary:
            break
        require(not parent.is_symlink(), f"Symlink parent is outside this scope: {parent}")
    return resolved


def pin(path):
    path = local_file(path)
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def load(path):
    return json.loads(local_file(path).read_text(encoding="utf-8"))


def check_pin(record):
    actual = pin(Path(record["path"]))
    require(actual["sha256"] == record["sha256"], f"Pinned hash changed: {record['path']}")
    if "bytes" in record:
        require(actual["bytes"] == record["bytes"], f"Pinned byte length changed: {record['path']}")
    return actual


def prerequisities():
    # All preflight checks finish before creating any development-archive path.
    closure_path = ROUND_SOURCE / "planning/full-five-closure.json"
    closure = load(closure_path)
    require(closure.get("candidate") == "W" and closure.get("case") == "R20-C1", "R20 W closure identity required")
    require(closure.get("one_request") is True and closure.get("requested_images") == 5, "One closed requested five is required")
    require(closure.get("all_actors_closed") is True, "All R20 actors must be closed first")
    require(set(closure.get("waves", {})) == {"initial", "selected"}, "Retain both closed original waves")

    index_path = ROUND_ARCHIVE / "archive-index.json"
    verification_path = ROUND_ARCHIVE / "byte-verification.json"
    index = load(index_path)
    verification = load(verification_path)
    require(verification.get("all_copy_hashes_match") is True, "R20 archive byte verification is required")
    require(Path(index["source_root"]).resolve(strict=True) == ROUND_SOURCE.resolve(strict=True), "R20 archive source binding differs")
    rows = index["files"]
    require(verification.get("copied_files") == len(rows), "R20 archive inventory count differs")
    by_source = {}
    for row in rows:
        source = local_file(Path(row["source_absolute"]), ROUND_SOURCE)
        rel = Path(row["archive_relative"])
        require(not rel.is_absolute() and ".." not in rel.parts and rel.parts[0] == "raw", "Invalid R20 archive relative path")
        archived = local_file(ROUND_ARCHIVE / rel, ROUND_ARCHIVE)
        require(source.relative_to(ROUND_SOURCE) == Path(*rel.parts[1:]), "R20 source/archive path mismatch")
        require(str(source) not in by_source, f"Duplicate R20 source row: {source}")
        source_pin = pin(source)
        archive_pin = pin(archived)
        require(source_pin["sha256"] == archive_pin["sha256"] == row["sha256"], f"R20 byte mismatch: {source}")
        require(source_pin["bytes"] == archive_pin["bytes"] == row["bytes"], f"R20 byte length mismatch: {source}")
        by_source[str(source)] = row
    require(str(closure_path.resolve(strict=True)) in by_source, "Full-five closure is absent from verified R20 raw archive")

    # Guide originals, specifications, actual-font manifests and corrections
    # belong only to round20/raw. Keep every authored coordinator file there.
    coordinator = ROUND_SOURCE / "coordinator"
    require(coordinator.is_dir(), "R20 authored coordinator evidence is required")
    for path in sorted(coordinator.rglob("*")):
        require(not path.is_symlink(), f"Unexpected coordinator symlink: {path}")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            require(str(path.resolve(strict=True)) in by_source, f"Guide record missing from R20 raw archive: {path}")

    # No quality outcome or diversity score is a packaging prerequisite.
    return closure, index, by_source, [pin(closure_path), pin(index_path), pin(verification_path)]


def collect_sources():
    paths = []
    snapshot_sets = []
    for relative in SNAPSHOTS:
        root = TASK / relative
        require(root.is_dir() and not root.is_symlink(), f"Closed snapshot required: {root}")
        members = []
        for path in sorted(root.rglob("*")):
            require(not path.is_symlink(), f"Unexpected snapshot symlink: {path}")
            if path.is_file():
                members.append(path)
                paths.append(path)
        require(len(members) == 12, f"Expected exact twelve-file W version snapshot: {root}")
        snapshot_sets.append({p.relative_to(root).as_posix(): pin(p) for p in members})
    require(set(snapshot_sets[0]) == set(snapshot_sets[1]), "Before/adopted snapshot paths differ")
    changed = sorted(k for k in snapshot_sets[0] if snapshot_sets[0][k]["sha256"] != snapshot_sets[1][k]["sha256"])
    adoption = load(TASK / "history/first-generation-sketch-w/adoption.json")
    require(adoption.get("candidate") == "W" and adoption.get("previous") == "V", "Adoption identity differs")
    require(changed == sorted(adoption["changed_files"]), "Actual W changed paths differ from adoption record")
    for record in adoption["runtime"]:
        check_pin(record)
    check_pin(adoption["draft"])
    check_pin(adoption["scope_review"])
    for relative in CLOSED_TEXT_ROOTS:
        root = TASK / relative
        require(root.is_dir() and not root.is_symlink(), f"Closed text record required: {root}")
        for path in sorted(root.rglob("*")):
            require(not path.is_symlink(), f"Unexpected text-record symlink: {path}")
            if path.is_file():
                paths.append(path)
    paths.extend(TASK / relative for relative in NAMED_TEXT)
    require(len(paths) == len(set(paths)), "Duplicate W archive source")
    rows = []
    for path in sorted(paths):
        path = local_file(path)
        require(path.suffix in TEXT_SUFFIXES, f"Non-text file is excluded from W development archive: {path}")
        data = path.read_bytes()
        data.decode("utf-8")
        require(b"\0" not in data, f"Binary data is outside W development scope: {path}")
        source_relative = path.relative_to(TASK).as_posix()
        rows.append({"source_absolute": str(path), "source_relative": source_relative,
                     "archive_relative": "raw/" + source_relative,
                     "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return rows, changed


def related_round_records(index, prerequisite_pins):
    rows = []
    for row in index["files"]:
        path = Path(row["source_absolute"]).resolve(strict=True)
        rel = path.relative_to(ROUND_SOURCE).as_posix()
        if rel.startswith("coordinator/") or rel.startswith("planning/") or rel == "report.md":
            rows.append({"source_absolute": str(path), "round20_archive_relative": row["archive_relative"],
                         "link_from_development_archive": "../round20/" + row["archive_relative"],
                         "sha256": row["sha256"], "bytes": row["bytes"], "copied_into_this_archive": False})
    return {"kind": "locator_to_exact_verified_round20_records", "prerequisite_pins": prerequisite_pins,
            "records": rows, "individual_guides_duplicated": 0,
            "limits": ["These locators do not reconstruct semantic viewing or certify future native font application.",
                       "R20 raw retains the actual guides, all native attempts, reviews, scores, failures and uncertainties."]}


def wave_table(closure):
    lines = ["| Stage | PASS | FAIL | NA | Set | Procedure |", "| --- | ---: | ---: | ---: | --- | --- |"]
    for name in ("initial", "selected"):
        wave = closure["waves"][name]
        counts = wave.get("image_gate_counts", {})
        cells = [name] + [str(counts.get(k, "unavailable")) for k in ("PASS", "FAIL", "NA")]
        cells += [str(wave.get("set_gate", "unavailable")), str(wave.get("procedure_gate", "unavailable"))]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_json(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main():
    require(Path.cwd().resolve(strict=True).is_relative_to(TASK.resolve(strict=True)), "Run only inside Ducttape Poster")
    require(not DEST.exists() and not DEST.is_symlink(), "New W archive destination required; existing evidence is preserved")
    closure, round_index, _, prerequisite_pins = prerequisities()
    rows, changed = collect_sources()
    related = related_round_records(round_index, prerequisite_pins)
    timestamp = utc()
    for row in rows:
        source = local_file(Path(row["source_absolute"]))
        target = DEST / row["archive_relative"]
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        require(hashlib.sha256(data).hexdigest() == row["sha256"], f"Closed W source changed during copy: {source}")
        with target.open("xb") as handle:
            handle.write(data)
        require(pin(target)["sha256"] == row["sha256"], f"W archive byte mismatch: {target}")
    for row in rows:
        require(pin(Path(row["source_absolute"]))["sha256"] == row["sha256"], "Closed W source changed during packaging")
    for record in prerequisite_pins:
        check_pin(record)
    write_json(DEST / "related-round20-records.json", related)
    write_json(DEST / "archive-index.json", {
        "schema_version": 1, "archive_kind": "closed_general_instruction_and_design_development",
        "archived_utc": timestamp, "source_root": str(TASK), "files": rows,
        "raw_inventory_exclusions": [], "changed_runtime_paths": changed,
        "source_artwork_copied": 0, "font_binaries_copied": 0,
        "individual_round20_guides_copied": 0, "prerequisite_pins": prerequisite_pins,
        "limits": ["Exact named W text/code history only; original source artwork and font binaries are excluded.",
                   "R20 per-guide and production/evaluation evidence is retained once in round20/raw and linked separately.",
                   "Byte verification is not visual quality replay, causal proof, transfer proof, universal success or authorship detection.",
                   "Earlier draft/scope/adoption/plan claims remain their original historical records."]})
    write_json(DEST / "byte-verification.json", {
        "verified_utc": timestamp, "copied_files": len(rows), "copied_bytes": sum(r["bytes"] for r in rows),
        "all_copy_hashes_match": True, "all_closed_source_bytes_unchanged_during_copy": True,
        "round20_archive_reverified": True, "quality_replayed": False, "source_scripts_executed": False,
        "images_opened_or_generated": 0, "scores_assigned": 0, "runtime_modified": False,
        "readme_modified": False, "git_staged_committed_or_pushed": False})
    report = f"""# Candidate V → W general development archive

This package preserves {len(rows)} exact text/JSON/code files ({sum(r['bytes'] for r in rows):,} bytes) from W's before/adopted twelve-file snapshots, draft, independent scope review, actual adoption and prospective five-direction plan. [SHA-256 inventory](archive-index.json) and [byte verification](byte-verification.json) identify the exact historical bytes. The five changed documents connect complex supplied prose and practical information to an authored actual-font planning sketch, with content-specific image geometry before first native generation when an existing suitable runtime is available. Simple/no-copy/unsupported-runtime requests retain positive native-brief fallback. Client references and explicit choices remain authoritative.

[W draft](raw/history/w-draft/review.md) · [Independent scope review](raw/history/w-scope-audit/review.md) · [Adoption](raw/history/first-generation-sketch-w/adoption.json) · [Before V](raw/history/first-generation-sketch-w/before-v/SKILL.md) · [Adopted W](raw/history/first-generation-sketch-w/adopted-w/SKILL.md) · [Original five-direction plan](raw/drafts/w-five-design/plan.json) · [Original rationale](raw/drafts/w-five-design/rationale.md)

R20 was fully closed and its archive reverified before this package was created. Its original outcomes below are read from the pinned [full-five closure](../round20/raw/planning/full-five-closure.json), without rescoring, averaging, replacing critics or altering any threshold:

{wave_table(closure)}

Reported native calls: {closure.get('native_calls', 'unavailable')}; returned: {closure.get('returned', 'unavailable')}; failed: {closure.get('failed', 'unavailable')}; repair calls: {closure.get('repair_calls', 'unavailable')}. Initial selection and uncorrected-first-result evidence remain in the original closure; a repaired result is not a new style or first-generation success. Raw per-critic diversity, low/NA scores, errors and uncertainty remain in [round20](../round20/report.md).

The authored per-direction guide specs, SVG/PNG originals, actual-font manifests, preparation/technical adjustments and viewing records are retained once under round20/raw. [Exact related-record locators](related-round20-records.json) identify their paths and hashes; they are not duplicated into this development package. These new coded planning assets are separate from client artwork and native final posters. Their font-file usage and planned coordinates do not certify native final font application, anatomy/material finish, protected client layout or a quality pass.

W's static scope review and its pre-generation plan/adoption claims are design hypotheses in their original time and scope. The actual R20 outcome does not establish a held-out success rate, an isolated effect of W versus changed planning/guides, universal high-end results or AI authorship detection. This package executes no renderer, source script, native generator, critic or test and modifies no runtime, README or Git state. Original source artwork and font binaries are not included here; no claim is made about unrelated older archive contents.
"""
    with (DEST / "report.md").open("x", encoding="utf-8") as handle:
        handle.write(report)
    print(json.dumps({"destination": str(DEST), "copied_files": len(rows),
                      "source_artwork_copied": 0, "font_binaries_copied": 0,
                      "individual_round20_guides_duplicated": 0}))


if __name__ == "__main__":
    main()
